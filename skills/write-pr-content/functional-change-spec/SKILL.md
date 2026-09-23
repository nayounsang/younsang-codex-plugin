---
name: functional-change-spec
description: Write a pull request Markdown fragment describing observable functional behavior when the diff and tests provide sufficient evidence.
---

# Functional Change Spec

Use `$functional-change-spec` when a change has tests and a diff from which
observable behavior can be established. Do not activate this skill when the
behavior is only inferred from intent, comments, or an unverified issue
description. If the trigger is not satisfied, return exactly `None`.

Before writing, inspect the repository's pull request template. Match its
heading and `Spec` placeholder when present; if no template can be located,
return `None` instead of inventing the contract. The template is a format
constraint, not evidence for behavior.

Return only the `Spec` Markdown fragment. Describe externally observable
success, failure, boundary, or state-transition behavior and cite the smallest
useful evidence location, such as a regression test, changed test, or diff
path. Keep implementation details out unless they are part of the public
behavior. Do not write the whole PR, or the human-authored `Abstract`,
`Description`, or `Issues` sections.

Use only behavior supported by the inspected tests and diff. Do not invent
cases, outcomes, terminology, commands, links, numbers, screenshots, or
reproduction steps. Do not copy the full PR template. Do not add an
introductory or closing explanation around the fragment.

Response format (replace every placeholder with inspected evidence):

```markdown
## Spec

- When `<observable input or action>` occurs, `<observable result>` is shown
  or returned (`<test/path>:<line>`).
- When `<boundary or failure condition>` occurs, `<observable fallback>` is
  used (`<diff/path>`).
```
