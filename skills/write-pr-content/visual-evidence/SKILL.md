---
name: visual-evidence
description: Add a pull request Markdown screenshot fragment for a UI change using an isolated Computer Use and browser-inspection workflow, with exact artifact paths.
---

# Visual Evidence

Use `$visual-evidence` only for a UI change and only when a browser runtime and
capture capability are available. If the browser cannot be isolated or a real
capture cannot be produced, return exactly `None`; never claim that a
screenshot exists.

Read the changed repository's `AGENTS.md` before operating the browser. Follow
its isolated Chrome, Browser CLI, Chrome DevTools, reset, and verification
workflow first. If those instructions are absent, use the repository's
documented browser workflow. Do not assume Playwright is available without an
explicit repository configuration. Keep capture permissions and runtime
availability as hard prerequisites.

Use and name the tools by responsibility. Keep the browser profile, tab, and
capture artifacts isolated from the user's normal browsing session.

| Tool | Responsibility | Rule |
| --- | --- | --- |
| Computer Use or the repository's documented computer-control tool | Navigate, click, fill, and reach the visible UI state | Use the isolated browser target only; do not use the user's normal profile |
| Configured Chrome DevTools MCP | Inspect snapshots, console, network, and the final visible state; capture screenshots when supported | Use the repository-provided server and target, not an unconfigured global endpoint |
| Browser CLI or the repository's runtime CLI | Apply UI test state, mock API scenarios, and reset the target | Use for state control, not as evidence that a screenshot was captured |
| Screenshot/capture facility | Write the actual PNG or other image artifact | If capture is unavailable or permission fails, return `None` |

Do not silently substitute Playwright or another browser tool. Use it only when
the repository explicitly configures it. Record the tool name, browser target,
and any session or target identifier needed to reproduce the capture.

Read the pull request template before choosing the fragment heading and
respect its placeholder. Return only the visual-evidence fragment, not the
whole PR and not the human-authored `Abstract`, `Description`, or `Issues`
sections. Do not add prose before or after it.

Capture an `After` image for a new UI feature. Capture both `Before` and
`After` images for a UI change or UI bug fix. Use only the exact local paths or
URLs produced by the capture workflow, with concise labels and useful alt
text. Include a video only when the user supplied a file or URL; do not create
or imply a video otherwise. Verify the relevant state before capturing and
reset or close the isolated browser according to the repository workflow. Do
not invent behavior, links, numbers, screenshots, or reproduction steps. Do
not copy the full PR template.

Print the exact repository-relative path for every captured artifact, and use
that same path in the Markdown link. Do not print a planned path for a file
that was not created. Include the path in the fragment so a reviewer can find
the source file even when the rendered image is unavailable.

Response format (shape only; replace placeholders with real captures and exact
paths):

```markdown
## Visual Evidence

| State | Tool and target | Screenshot | Artifact path |
| --- | --- | --- | --- |
| After | Computer Use + Chrome DevTools MCP (`<target-id>`) | ![After](<actual-after-path.png>) | `<actual-after-path.png>` |
```

For a UI change or bug fix, use the same format with `Before` and `After` rows.
For a new UI feature, include only the `After` row. The path must be the
actual output from the capture tool, for example
`artifacts/pr-visual-evidence/<change-id>/after.png`, not a guessed path.
