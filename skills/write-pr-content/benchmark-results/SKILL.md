---
name: benchmark-results
description: Format evidence-backed performance results and their reproducible runtime, package, browser, and tool versions as a pull request Markdown fragment.
---

# Benchmark Results

Use `$benchmark-results` only for a performance change or when benchmark input
was explicitly provided for the change. If the change has no performance
intent, or the inputs do not contain measured environment, workload, baseline,
and after values sufficient to calculate the delta, return exactly `None`.

Read the pull request template first and respect its benchmark heading and
placeholder when present. Return only the benchmark fragment. Do not generate
the full PR or write human-authored `Abstract`, `Description`, or `Issues`
sections.

Present the available evidence in a concise table containing:

- environment;
- workload or input size;
- baseline;
- after;
- delta, with its unit and direction.

Before running or comparing a benchmark, collect the environment with a
repository-local script or the commands in this table. Use the package manager
and benchmark runner actually used by the repository; do not run commands for
tools that are not installed or involved.

| Component | Collection command or script step | What to record |
| --- | --- | --- |
| OS and architecture | `uname -srmo` or the repository's platform command | OS, kernel, architecture |
| Node.js | `node --version` | Exact runtime version |
| npm environment | `npm env` | Sanitized environment artifact path and relevant non-secret settings |
| npm diagnostics | `npm doctor` | Sanitized diagnostic artifact path and pass/fail summary |
| Package manager | Detected manager's version command, such as `npm --version`, `pnpm --version`, `yarn --version`, or `bun --version` | Exact package-manager version |
| Benchmark runner | The configured runner's version command, such as the repository's `vitest`, `jest`, or custom benchmark command | Exact runner/tool version |
| Browser | The exact browser executable used, such as `google-chrome --version` or `chromium --version`, or the browser session's reported version | Browser name, channel, and exact version when browser work is involved |
| Browser automation/driver | The configured Browser CLI, CDP client, or driver version command | Exact tool version when it affects the run |

Save raw command output outside the PR body, redact tokens, credentials,
private URLs, and unrelated environment values from `npm env` and diagnostics,
and print the sanitized artifact paths in the benchmark evidence. If a listed
tool is not part of the benchmark, mark it as not applicable instead of
inventing a version. A missing required environment value means the fragment
must be `None`.

Do not create, estimate, round, or silently normalize numbers. Preserve the
provided units and labels, identify the comparison direction when the evidence
supports it, and omit the fragment when required values are missing. Do not
claim statistical significance, causation, or reproducibility without evidence.
Do not invent behavior, links, screenshots, or reproduction steps. Do not copy
the full PR template. Do not add prose before or after the fragment.

Response format (shape only; replace placeholders with measured values and
actual artifact paths):

```markdown
## Benchmark Results

| Environment | Workload | Baseline | After | Delta |
| --- | --- | ---: | ---: | ---: |
| Node `<version>`, npm `<version>`, browser `<version or N/A>`, runner `<version>` | `<input size and workload>` | `<value + unit>` | `<value + unit>` | `<value + unit and direction>` |

| Environment evidence | Artifact path |
| --- | --- |
| Sanitized `npm env` and `npm doctor` output | `<repo-relative environment artifact path>` |
```
