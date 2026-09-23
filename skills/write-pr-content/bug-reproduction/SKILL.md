---
name: bug-reproduction
description: Reconstruct evidence-backed bug reproduction steps for an underspecified bug fix when regression tests, commands, and the diff provide enough detail.
---

# Bug Reproduction

Use `$bug-reproduction` only for a bug fix whose issue or PR description does
not already clearly specify actor, setup, action, actual result, and expected
result. When all five are already clear, do not run this skill and return
`None`. If the issue is underspecified but the changed regression test,
executable command, and diff do not provide enough evidence to recover the
steps, return `None` rather than guessing.

Read the pull request template first and match its reproduction heading and
placeholder when present. Return only the reproduction Markdown fragment. Do
not generate the complete PR or fill the human-authored `Abstract`,
`Description`, or `Issues` sections. Do not add prose before or after the
fragment.

Reconstruct only what is supported by the regression test, its setup and
action, the command used to run it, and the changed diff. Include the actor,
setup, action, actual result, and expected result in a compact ordered list or
table. Preserve exact commands, paths, inputs, and observable outcomes when
they are available. Mark no inferred detail as fact: if any required field
cannot be supported, return `None`. Do not invent behavior, links, numbers,
screenshots, or reproduction steps beyond the evidence. Do not copy the full
PR template.

Response format (shape only; replace placeholders with evidence from the
regression test, command, and diff):

```markdown
## Reproduction

| Field | Evidence-backed value |
| --- | --- |
| Actor | `<actor from issue or test>` |
| Setup | `<exact setup, command, fixture, or state>` |
| Action | `<exact user or system action>` |
| Actual result | `<observed failure>` |
| Expected result | `<expected behavior from test or diff>` |
```
