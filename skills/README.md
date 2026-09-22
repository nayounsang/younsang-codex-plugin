# Skill bundle contract

Each child directory of `skills/` is an independent Codex skill. A valid
skill package contains:

```text
skills/<skill-name>/
├── SKILL.md
├── agents/       # optional agent metadata
├── references/   # optional supporting guidance
├── scripts/      # optional skill-owned tooling
└── assets/       # optional skill-owned assets
```

Keep all paths in a skill relative to that skill's directory. The parent
plugin discovers the complete `skills/` directory through
`.codex-plugin/plugin.json`.
