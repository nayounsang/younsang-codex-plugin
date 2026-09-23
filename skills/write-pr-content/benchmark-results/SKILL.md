---
name: benchmark-results
description: Format evidence-backed performance results with only the software, dependency, device, browser, and physical environment dimensions relevant to the measured workload.
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

Present the fragment in this order:

1. `Environment`: only the environment dimensions that can affect the
   measurement.
2. `Benchmark`: workload or input size, baseline, after, and
   delta with its unit and direction.

Environment is not a fixed Node/npm checklist. Select the relevant dimensions
from this table before collecting values:

| Environment dimension | Examples | Include when |
| --- | --- | --- |
| Software and dependency versions | Runtime, package manager, benchmark runner, direct dependency versions | The implementation, resolver, compiler, runtime, or benchmark tool can affect the result |
| Program and browser versions | Electron, browser, Browser CLI, CDP client, driver | The measured path runs in that program or browser |
| Device and operating system | OS, kernel, architecture, CPU, GPU, memory, display, power or thermal mode | Hardware or operating-system scheduling can affect the result |
| Physical and operational conditions | Timestamp, timezone, locale, network region or latency, location, temperature, or power source | The workload depends on time, geography, network, thermal, or other physical conditions |

Do not collect unrelated values. Record only the precision needed to reproduce
the measurement, redact sensitive location or network details, and explain why
each non-obvious environment value is relevant.

Before running or comparing a benchmark, collect the environment with a
repository-local script or the commands in this table. Use the package manager
and benchmark runner actually used by the repository; do not run commands for
tools that are not installed or involved.

| Environment dimension | Collection command or script step | What to record |
| --- | --- | --- |
| OS and architecture | `uname -srmo` or the repository's platform command | OS, kernel, architecture |
| Runtime and package manager | `node --version`, `npm --version`, `pnpm --version`, or the detected manager's equivalent | Exact versions when used by the benchmark |
| Environment summary | `npm exec --yes envinfo -- --system --binaries --npmPackages <relevant packages>` or the repository-local environment collector | Sanitized non-secret settings and artifact path |
| npm diagnostics | `npm doctor` | Sanitized diagnostic artifact path and pass/fail summary when npm affects the run |
| Dependencies | `npm ls --depth=0` or the repository's package-manager equivalent | Exact resolved versions that affect the measured path |
| Benchmark runner | The configured runner's version command, such as the repository's `vitest`, `jest`, or custom benchmark command | Exact runner/tool version |
| Browser and automation | The exact browser executable, Browser CLI, CDP client, or driver version command | Exact program and browser versions when used |
| Physical or operational context | Test harness metadata or an explicit command such as `date -u`; use a coarse region or network measurement when needed | Relevant time, timezone, location, network, thermal, or power context |

Save raw command output outside the PR body, redact tokens, credentials,
private URLs, and unrelated environment values from `envinfo` and diagnostics,
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

### Environment

| Dimension | Value | Relevance |
| --- | --- | --- |
| `<software, device, or physical dimension>` | `<measured value>` | `<why this can affect the benchmark>` |
| Evidence artifact | `<repo-relative sanitized artifact path>` | `<commands or metadata used>` |

### Benchmark

| Workload | Baseline | After | Delta |
| --- | ---: | ---: | ---: |
| `<input size and workload>` | `<value + unit>` | `<value + unit>` | `<value + unit and direction>` |
```
