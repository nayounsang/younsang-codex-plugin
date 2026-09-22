# Detect and validate the runtime

Use this reference before changing the target project. The goal is to quickly
distinguish "the package is installed" from "the MSW Dev Tool runtime is
actually connected and controllable".

## Static project checks

From the target project root, inspect the dependency manifest, lockfile, and
source code:

```bash
rg -n '"msw"|@msw-dev-tool/(core|browser-cli|node-cli)' package.json pnpm-lock.yaml yarn.lock package-lock.json bun.lockb bun.lock 2>/dev/null
rg -n 'setupWorker|setupServer|setupDevToolWorker|setupDevToolServer' . \
  -g '!node_modules' -g '!dist' -g '!build'
```

Interpret the result as follows:

- `msw` only: MSW exists, but MSW Dev Tool may not be integrated.
- `@msw-dev-tool/core` plus `setupDevToolWorker`: browser runtime is likely integrated.
- `@msw-dev-tool/core` plus `setupDevToolServer`: Node runtime is likely integrated.
- `browser-cli` or `node-cli` only: a control client exists, but it does not prove that a runtime session is active.
- No handler definitions: this is still usable through temporary custom handlers after the runtime is initialized.

The absence of existing MSW handlers is not a reason to skip initialization.
`add-temp` cannot create the MSW Dev Tool runtime; it only adds a temporary
handler after a browser bridge or Node session already exists.

## Fast browser validation

Use the target project's package manager to check that the CLI is installed:

```bash
pnpm exec msw-dev-tool-browser --help
```

Then check the dedicated Chrome/CDP endpoint and discover targets:

```bash
pnpm exec msw-dev-tool-browser tabs --cdp-url http://127.0.0.1:9222
```

Select a target that contains the running app and validate the runtime:

```bash
pnpm exec msw-dev-tool-browser session \
  --cdp-url http://127.0.0.1:9222 \
  --target "$target_id"
```

The target is ready only when the command returns a valid machine-readable
session result. A browser process or a discovered tab by itself is not enough.
The browser runtime must have completed both `setupDevToolWorker()` and
`worker.start()`.

## Fast Node validation

Check that the CLI is installed:

```bash
pnpm exec msw-dev-tool --help
```

List active sessions:

```bash
pnpm exec msw-dev-tool sessions
```

Select a live PID and inspect it:

```bash
pnpm exec msw-dev-tool --pid <pid> session
```

The Node runtime is ready only when a live session is listed and the selected
PID returns a valid session result. A dependency installation without a
running `setupDevToolServer()` process is not a ready target. The Node server
must also have called `server.listen()`, and the CLI must run from the same
working directory that started the Node process.

## Package-manager translation

Replace `pnpm exec` with the project's package-manager equivalent:

- npm: `npx --no-install`
- Yarn: `yarn exec`
- Bun: `bunx --no-install`

Do not use `npx` without `--no-install` for these validation commands: a
network download can make an apparently installed project look valid.
