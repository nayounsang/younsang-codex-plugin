---
name: reference-links
description: Return a pull request Markdown fragment of related references that were actually used to understand or implement the change.
---

# Reference Links

Use `$reference-links` only when the work actually consulted a related issue,
existing pull request, GitHub documentation, RFC, or relevant article. Exclude
the issue or ticket directly being resolved. If there are no qualifying
references, return exactly `None`.

Read the pull request template first and use its reference-links heading or
placeholder when available. Return only that Markdown fragment; never generate
the complete PR and never write `Abstract`, `Description`, or `Issues` for the
author.

Use the exact URLs and titles supplied by the inspected material. Make each
link title explain what was referenced and how it informed the change. Add a
single short explanation only when the title alone is not enough. Do not add
generic homepages, guessed URLs, unrelated links, or claims that were not
supported by the linked material. Do not invent behavior, numbers,
screenshots, or reproduction steps. Do not copy the full PR template. Do not
add prose before or after the fragment.

Response format (shape only; use only exact references actually consulted):

```markdown
## References

- [`<descriptive reference title>`](<exact URL>) — `<what this reference
  informed>`
```
