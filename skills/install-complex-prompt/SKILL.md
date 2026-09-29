---
name: install-complex-prompt
description: Install or update Codex Complex Prompt for Codex CLI when the user asks to set it up.
---

# Install Codex Complex Prompt

When the user asks to install or update Codex Complex Prompt, check that the current environment matches this repository's supported setup before running the installer. For questions or usage help, explain the setup without installing it.

This project supports macOS on an Apple M1 Mac with Codex CLI. The CLI installer requires Node.js 24 or later and `npx`.

1. Inspect the environment using `uname -s`, `uname -m`, `sysctl -n machdep.cpu.brand_string`, `node --version`, `npx --version`, and `codex --version`.
2. Continue only when the OS is macOS (`Darwin`), the architecture is `arm64`, the CPU brand identifies Apple M1, Codex CLI is available, and Node.js is version 24 or later. If a requirement is missing, stop and tell the user what to install or which environment is unsupported.
3. For an installation request, run the upstream documented install command:

   ```bash
   npx @codex-complex-prompt/cli-bridge hook install
   ```

If the user asks to preview the installation without installing, run only:

```bash
npx @codex-complex-prompt/cli-bridge hook install --dry-run
```

Report the preview and stop; do not follow it with the install command unless the user then asks to install. The upstream CLI accepts `--dry-run` and prints the Codex config, skill, and prompt changes it would make.

4. After successful installation, tell the user to restart Codex CLI. If Codex asks them to review the hook, have them inspect and trust it through `/hooks`, then start a new thread and invoke `$complex-prompt`.

The installer adds Codex Complex Prompt's hooks and `$complex-prompt` skill. It preserves existing hooks. Do not install it in Codex App or on an unsupported operating system or architecture.
