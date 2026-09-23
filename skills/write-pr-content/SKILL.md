---
name: write-pr-content
description: Index the focused Markdown fragment skills used to document pull request changes; invoke a child skill for the requested fragment instead of using this package as a standalone PR writer.
---

# Pull Request Markdown Components

This directory is a component index. It does not draft or assemble a complete
pull request, and it does not add a new PR-writing workflow. Invoke the child
skill that matches the evidence available for the change:

- [functional-change-spec](functional-change-spec/SKILL.md) — observable
  behavior extracted from tests and diff.
- [change-diagram](change-diagram/SKILL.md) — an external behavior flow or
  state change that benefits from a diagram.
- [reference-links](reference-links/SKILL.md) — related issues, PRs, docs,
  RFCs, or articles actually used as references.
- [benchmark-results](benchmark-results/SKILL.md) — measured performance
  results for a performance change.
- [visual-evidence](visual-evidence/SKILL.md) — captured before/after UI
  evidence when an isolated browser environment is available.
- [bug-reproduction](bug-reproduction/SKILL.md) — evidence-backed reproduction
  steps reconstructed for an underspecified bug report.

Each child decides independently whether its trigger is satisfied and returns
`None` otherwise. Do not combine the child outputs here or use this index to
fill human-authored PR sections such as Abstract, Description, or Issues.
