---
name: install-plannotator
description: Install Plannotator and its Codex integration on macOS, Linux, WSL, or Windows when the user explicitly asks to install it.
---

# Install Plannotator

When the user explicitly asks to install or update Plannotator, determine which operating system and shell they use, then execute the matching official installer command. For questions about Plannotator or plugin installation, do not run either installer. Do not merely show the command for the user to run when they ask for installation.

macOS, Linux, or WSL:

```bash
curl -fsSL https://plannotator.ai/install.sh | bash
```

Windows PowerShell:

```powershell
irm https://plannotator.ai/install.ps1 | iex
```

The installer detects Codex and configures its integration. Do not add a second Codex hook or copy the Plannotator skills yourself. Report whether the command succeeded and any next step printed by the installer. If the user uses Codex Desktop and the installer says to restart it, tell them to restart Codex Desktop before using the integration.
