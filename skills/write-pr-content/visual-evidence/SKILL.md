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

For a UI change or bug fix, obtain the `Before` state in this order:

1. Use a matching user-provided local `Before` artifact when one exists. It
   must describe the same target and state; do not relabel an unrelated image.
2. If no artifact was provided and the current worktree is clean, resolve the
   pre-change revision from the PR base and the current HEAD, record the
   current branch, HEAD, and status, stop the running app, and temporarily
   check out that revision in the current worktree. Capture `Before` with the
   same browser, viewport, fixture, and capture workflow, then restore the
   original branch and verify the recorded HEAD and clean status.
3. If the current worktree is dirty or cannot be safely restored, create a
   detached temporary worktree at the pre-change revision and run the same
   capture workflow there. Remove the temporary worktree after capture.
4. If none of these paths produces a valid `Before` capture, return exactly
   `None` instead of claiming a Before/After comparison.

Never overwrite or discard uncommitted work to obtain `Before`. If a checkout,
restore, app launch, or capture step fails, stop that path, preserve the user's
worktree, and use the next safe option.

Read the pull request template before choosing the fragment heading and
respect its placeholder. Return only the visual-evidence fragment, not the
whole PR and not the human-authored `Abstract`, `Description`, or `Issues`
sections. Do not add prose before or after it.

Capture an `After` image for a new UI feature. Capture both `Before` and
`After` images for a UI change or UI bug fix. Screenshot and image artifacts
must use exact repository-relative local paths produced by the capture
workflow; do not use a URL as an image artifact path. Include a video only
when the user supplied a file or URL, and keep that optional video link in a
separate field from screenshot artifact paths. Do not create or imply a video
otherwise. Verify the relevant state before capturing and reset or close the
isolated browser according to the repository workflow. Do not invent behavior,
links, numbers, screenshots, or reproduction steps. Do not copy the full PR
template.

Print the exact repository-relative path for every captured screenshot or image
artifact, and use that same path in the Markdown link. Do not print a planned
path for a file that was not created. Include the path in the fragment so a
reviewer can find the source file even when the rendered image is unavailable.

Response format (shape only; replace placeholders with real captures and exact
paths):

```markdown
## Visual Evidence

| State | Tool and target | Screenshot | Local artifact path |
| --- | --- | --- | --- |
| After | Computer Use + Chrome DevTools MCP (`<target-id>`) | ![After](<repo-relative-after-path.png>) | `<repo-relative-after-path.png>` |

| Optional user-provided video | Link |
| --- | --- |
| After walkthrough | `<user-provided-video-URL-or-local-file>` |
```

For a UI change or bug fix, use the same format with `Before` and `After` rows.
For a new UI feature, include only the `After` row. The path must be the
actual local output from the capture tool, for example
`artifacts/pr-visual-evidence/<change-id>/after.png`, not a guessed path. A
user-provided video URL is allowed only in the separate optional video field;
it is not a screenshot artifact path.
