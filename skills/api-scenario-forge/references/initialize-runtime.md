# Initialize the runtime

Read this document only when [detect-runtime.md](detect-runtime.md) shows that
the target project is missing a package, runtime integration, or a controllable
MSW Dev Tool session. Do not repeat initialization when detection already
passes.

## Install the target-project dependencies

Install into the application under test, not into the API Scenario Forge
plugin repository. Preserve the detected package manager and lockfile.

If `msw` is absent from the target project's dependency manifest, include it
in the installation.

Browser runtime:

```bash
pnpm add -D --save-exact @msw-dev-tool/core @msw-dev-tool/browser-cli msw
```

Node runtime:

```bash
pnpm add -D --save-exact @msw-dev-tool/core @msw-dev-tool/node-cli msw
```

If `msw` is already present, omit it from both commands. Preserve its existing
version and dependency section; do not replace it with an unversioned or
`--save-exact` installation.

Browser runtime:

```bash
pnpm add -D --save-exact @msw-dev-tool/core @msw-dev-tool/browser-cli
```

Node runtime:

```bash
pnpm add -D --save-exact @msw-dev-tool/core @msw-dev-tool/node-cli
```

Translate the command to npm, Yarn, or Bun when appropriate. Install
`@msw-dev-tool/react` only when the user explicitly wants the human-facing
browser UI. Do not change the existing `msw` version or move it between
`dependencies` and `devDependencies`.

## Integrate an existing handler set

For a browser app, replace the MSW worker setup while preserving the existing
handlers:

```ts
import { setupDevToolWorker } from "@msw-dev-tool/core/browser";

const worker = await setupDevToolWorker(...handlers);
await worker.start({ onUnhandledRequest: "bypass" });
```

For a Node app:

```ts
import { setupDevToolServer } from "@msw-dev-tool/core/node";

const server = await setupDevToolServer(...handlers);
server.listen();
```

Both setup functions are asynchronous. Preserve the application's existing
startup ordering and make sure the process does not begin using the API before
the runtime is ready.

The browser `worker.start()` and Node `server.listen()` calls are required even
when the handler list is empty. They activate the interception runtime; the
CLI cannot create a usable session before that activation.

## Initialize without code-defined handlers

Code-defined handlers are optional. If the project has no handler definitions,
initialize an empty runtime and create temporary handlers through the CLI.

Browser:

```ts
import { setupDevToolWorker } from "@msw-dev-tool/core/browser";

const worker = await setupDevToolWorker();
await worker.start({ onUnhandledRequest: "bypass" });
```

Node:

```ts
import { setupDevToolServer } from "@msw-dev-tool/core/node";

const server = await setupDevToolServer();
server.listen();
```

## Start and re-check

Start the application's normal development or Node command. For a browser app,
also start the dedicated Chrome remote-debugging profile described in the
skill. For a Node app, keep the process running and use its PID.

Return to [detect-runtime.md](detect-runtime.md) and rerun the fast validation
commands. Initialization is complete only when the relevant browser target or
Node PID returns a valid session result.
