---
name: visual-evidence
description: Add a pull request Markdown screenshot fragment for a UI change, or report which capability is missing when evidence cannot be captured.
---

# Visual Evidence

Use `$visual-evidence` only for a UI change. Before capturing, inspect the
tools and task context available in the current session and determine whether
they provide a complete path to the requested evidence. Do not assume a browser
runtime is required: the target may be a browser, desktop app, or another UI
that the available tools can access.

Consider all currently exposed capabilities, including MCP tools, app
integrations, browser or desktop control, test tooling, and screenshot or image
artifact features. Examples are illustrative, not an allowlist. Do not prefer
or select a tool just because its name appears here. Base the choice on the
tools actually exposed in this session and their descriptions.

Tool presence alone does not establish that capture is possible. For the
chosen route, verify that it can:

- access the target UI in the needed state and perform any required interaction;
- produce an actual screenshot image that can be inspected in the response or
  read as a file;
- when it saves a file, write the image to the required location and make that
  file readable from the current work environment;
- when the task requires it, isolate the browser or app session, select the
  correct target, and reset or close it afterward.

Treat capture as available only when the route satisfies the needs of this
task, including a real image artifact that can be verified and saved at an
exact repository-relative path. If the task is not a UI change, return exactly
`None`. If it is a UI change but no exposed route can produce and verify the
required artifact, do not install or configure tools automatically. Explain
which capability is missing and why it is needed; do not report `None` as if a
capture attempt succeeded, and never claim a screenshot or path exists when it
does not. In this case, return a concise status message instead of a PR
artifact fragment.

Read the changed repository's `AGENTS.md` before operating its UI. Follow its
instructions for the selected target and workflow. When using a browser, use
the repository's documented browser workflow when one exists. Keep required
permissions and runtime access as hard prerequisites; do not infer access from
tool availability alone.

Use and name the tools by the responsibilities they actually perform. Keep
the target session and capture artifacts separate from the user's normal
browser or app session whenever the available workflow supports isolation and
the task requires it. Record the chosen tool names, target, and any session or
target identifier needed to reproduce the capture. Do not silently claim that
a state-control or inspection tool captured an image; verify the image output
itself.

For a UI change or bug fix, obtain the `Before` state in this order:

1. Use a matching user-provided local `Before` artifact when one exists. It
   must describe the same target and state; do not relabel an unrelated image.
2. If no artifact was provided and the current worktree is clean, resolve the
   pre-change revision from the PR base and the current HEAD, record the
   current branch, HEAD, and status, stop the running app, and temporarily
   check out that revision in the current worktree. Capture `Before` with the
   same target, size, data fixture, and capture workflow, then restore the
   original branch and verify the recorded HEAD and clean status.
3. If the current worktree is dirty or cannot be safely restored, create a
   detached temporary worktree at the pre-change revision and run the same
   capture workflow there. Remove the temporary worktree after capture.
4. If none of these paths produces a valid `Before` capture, do not claim a
   Before/After comparison. Explain that the required `Before` artifact could
   not be captured and which capability or safe path was unavailable.

Never overwrite or discard uncommitted work to obtain `Before`. If a checkout,
restore, app launch, or capture step fails, stop that path, preserve the user's
worktree, and use the next safe option.

Read the pull request template before choosing the fragment heading and
respect its placeholder. Return only the visual-evidence fragment, not the
whole PR and not the human-authored `Abstract`, `Description`, or `Issues`
sections. When a valid artifact is available, do not add prose before or after
the fragment. The missing-capability status message described above is the
exception.

Capture an `After` image for a new UI feature. Capture both `Before` and
`After` images for a UI change or UI bug fix. Screenshot and image artifacts
must use exact repository-relative local paths produced by the capture
workflow; do not use a URL as an image artifact path. Include a video only
when the user supplied a file or URL, and keep that optional video link in a
separate field from screenshot artifact paths. Do not create or imply a video
otherwise. Verify the relevant state before capturing and reset or close the
isolated target session according to the repository workflow. Do not invent behavior,
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
| After | `<tool name(s) and target>` | ![After](<repo-relative-after-path.png>) | `<repo-relative-after-path.png>` |

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
