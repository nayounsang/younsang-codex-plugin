---
name: api-scenario-forge
description: Control MSW HTTP and WebSocket scenarios from an AI agent, then verify the resulting browser or Node application behavior end to end. Use when external API availability must be removed from development or when loading, failure, malformed, edge-case, or alternative API responses need to be exercised.
---

# API Scenario Forge

Use MSW Dev Tool as the runtime API scenario engine. Keep the application's MSW
handlers as the source of truth, change their behavior at runtime, and verify
the application result directly.

Use [detect-runtime.md](references/detect-runtime.md) and
[initialize-runtime.md](references/initialize-runtime.md) for runtime
readiness and setup rules.

Do not build or call a custom scenario MCP. Use:

- `@msw-dev-tool/browser-cli` for browser MSW scenario mutations.
- `@msw-dev-tool/node-cli` for Node MSW scenario mutations.
- The bundled `chrome-devtools` MCP only for browser inspection and E2E actions.

Before using CLI commands, read [api-reference.md](references/api-reference.md)
and the runtime checks in [detect-runtime.md](references/detect-runtime.md).
The linked CLI documentation is the source of truth for command syntax.

## Operating rules

- Inspect the target project before installing or editing anything.
- Preserve the project's package manager and existing MSW setup.
- Use exact package versions when installing dependencies and keep the lockfile.
- Never use a production API for passthrough verification. Use a local or staging API with non-sensitive data.
- Treat every browser tab and Node process as an isolated scenario target.
- Use handler IDs returned by `list`; do not hand-build IDs when the CLI returns one.
- Apply all mutations before interacting with the feature under test.
- If an apply command fails, stop and report the partial state. Do not continue verification blindly.
- Always reset the target in cleanup and verify the reset result.

## Phase 1: detect

Follow [detect-runtime.md](references/detect-runtime.md) to detect the runtime
and quickly validate whether the package and a live controllable session are
already present. Do not reinstall or re-integrate a runtime that passes those
checks.

If any required check fails, read and follow
[initialize-runtime.md](references/initialize-runtime.md), then return here
and run detection again. Do not continue to browser or Node scenario control
until a live controllable session is confirmed.

The CLI examples below use `pnpm exec` so locally installed devDependencies
are resolved. Substitute the package-manager wrapper from
[detect-runtime.md](references/detect-runtime.md) when the project uses npm,
Yarn, or Bun.

## Phase 2: browser target

The plugin bundles the Chrome DevTools MCP configuration in `.mcp.json`. Use
that project-provided MCP server for browser inspection; do not add a second
global Chrome DevTools MCP entry for this workflow. Start a dedicated Chrome
profile with remote debugging before using it:

```bash
open -na "Google Chrome" --args \
  --remote-debugging-address=127.0.0.1 \
  --remote-debugging-port=9222 \
  --user-data-dir=/private/tmp/chrome-debug-9222
```

Use the equivalent command for Windows or Linux. Never attach to the user's
normal browsing profile.

Start the application, then discover the tab running
`setupDevToolWorker(...handlers)` and `worker.start()`:

```bash
pnpm exec msw-dev-tool-browser tabs --cdp-url http://127.0.0.1:9222
target_id="<paste-the-id-of-the-tab-that-runs-setupDevToolWorker>"
cdp_args=(--cdp-url http://127.0.0.1:9222 --target "$target_id")
pnpm exec msw-dev-tool-browser session \
  "${cdp_args[@]}"
```

Keep `cdp_args` in the same shell session and use it for every subsequent
browser CLI command. Browser scenario state is tab-scoped.

Use the configured `chrome-devtools` MCP to navigate, click, fill, inspect
snapshots, read console output, inspect network activity, and take screenshots.
Use the browser CLI to mutate MSW state. Do not confuse these responsibilities.

## Phase 3: Node target

Start the Node process that runs `setupDevToolServer()`. Then discover and
select its PID:

```bash
pnpm exec msw-dev-tool sessions
pnpm exec msw-dev-tool --pid <pid> session
```

Run these commands from the same working directory that started the Node
process. Node session snapshots are stored relative to that directory. Use
`--pid <pid>` on every mutation. For parallel scenarios, run one isolated Node
process per scenario and keep their PIDs separate. If the application listens
on a port, assign a distinct port to each process.

After handler code changes, reset the process and confirm the JSON result has
`"pendingReset": false` before applying new runtime changes.

## Phase 4: apply a scenario

Start with discovery:

Read [api-reference.md](references/api-reference.md) before choosing the
command or JSON shape. The linked Browser CLI and Node CLI pages are the
source of truth; the examples below only show the workflow order.

```bash
pnpm exec msw-dev-tool-browser list "${cdp_args[@]}"
pnpm exec msw-dev-tool --pid <pid> list
```

For each selected handler, use one of these behaviors:

- `default`: original handler behavior.
- `delay`: indefinite loading state.
- `return null`: null response.
- `custom response`: previously saved custom response. You can freely configure the responses for the api.
- `network error`: network failure.
- HTTP status (`2xx`, `3xx`, `4xx`, `5xx`)

Example custom response:

```bash
pnpm exec msw-dev-tool-browser set-custom-response \
  '{"path":"/api/items","method":"get"}' \
  --json '{"status":"200","contentType":"application/json","response":"[]","delay":100}' \
  "${cdp_args[@]}"

pnpm exec msw-dev-tool-browser set-behavior \
  '{"path":"/api/items","method":"get"}' \
  'custom response' \
  "${cdp_args[@]}"
```

For malformed or defensive-programming cases, use a custom response string
with the desired status, content type, missing fields, unexpected types, or
invalid JSON. Keep the response intentional and document what the UI should
do with it.

Use temporary handlers only for exploratory endpoints that are not represented
by application handlers. After the runtime is initialized and the target has
passed detection, create them with the documented `add-temp` command. Then
verify the response through the application. Remove temporary handlers or reset
the target afterward.

## Phase 5: verify end to end

Verification must include both the API mutation and the application result.

1. Confirm the selected behavior with `get` or the command result.
2. Trigger the application flow through CDP for browser targets, or through the relevant Node request/test entrypoint.
3. Inspect the visible state, loading state, error state, fallback, retry path, or defensive rendering.
4. Inspect console errors and relevant network activity.
5. Capture a screenshot or machine-readable observation when it helps establish evidence.
6. Report the scenario, target ID/PID, observed response behavior, and verification result.

Do not call a scenario successful merely because the CLI mutation returned
`ok: true`; the application must visibly or programmatically exhibit the
expected behavior.

## Parallel scenarios

Parallelism is isolation, not repeated mutation of one target:

```text
browser scenario A -> Chrome tab A -> target A
browser scenario B -> Chrome tab B -> target B

node scenario A -> process A -> PID A
node scenario B -> process B -> PID B
```

Never apply two independent scenarios to the same tab or Node process. Use a
separate tab/process and a separate app port when necessary.

## Cleanup

Browser:

```bash
pnpm exec msw-dev-tool-browser reset "${cdp_args[@]}"
```

Node:

```bash
pnpm exec msw-dev-tool --pid <pid> reset
```

Inspect the reset JSON, confirm temporary handlers are removed and mocking is
enabled again, then close the dedicated browser profile or Node process.

## Failure handling

Report these as setup failures rather than test failures:

- the target project could not be initialized with an MSW Dev Tool runtime;
- `setupDevToolWorker` or `setupDevToolServer` is not running;
- the browser target does not contain an initialized Dev Tool session;
- the selected Node PID is stale or has a pending reset;
- a target disappeared during verification;
- a passthrough request would reach an unsafe or unknown backend.

When setup is incomplete, explain the smallest integration change needed and
stop before pretending that the scenario was verified.
