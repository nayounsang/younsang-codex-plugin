# Building a project context dossier

Use this guide before making broad documentation claims. The goal is to recover the repository's actual contracts without assuming a particular language, framework, package manager, or deployment model.

## 1. Inventory the documentation

Search tracked files first, then classify the relevant documents. Exclude dependency directories and generated output from the initial inventory unless they are directly relevant as evidence.

For each document, record:

| Field | What to determine |
| --- | --- |
| Path and format | Markdown, MDX, API reference, inline docs, examples, or other format |
| Audience and job | Who uses it and what they are trying to accomplish |
| Document type | Tutorial, how-to, reference, explanation, release/migration note, or overview |
| Authority | Canonical source, summary, mirror, generated output, redirect, or unknown |
| Entry/exit links | Where a reader arrives from and what the next useful step is |
| Freshness signals | Version selectors, dates, deprecation notes, branch state, or stale scaffold text |

Look for root overviews, package/module READMEs, docs-site source, examples, API references, changelogs, migration guides, navigation metadata, redirects, and contribution instructions. When a page is hidden from navigation, check its source and inbound links before calling it deleted or orphaned.

## 2. Recover implementation truth

Locate the smallest repository surfaces that define the claims under review. Common sources include:

- package or module manifests, dependency/version ranges, workspace definitions, export maps, binaries, and public entry points;
- public types, schemas, validation, serializers, defaults, error definitions, and configuration loaders;
- command registration, argument parsing, help output, routes, UI labels, forms, examples, and generated API metadata;
- focused tests, fixtures, snapshots, integration harnesses, and CI workflows;
- repository-level instructions describing supported environments, safe runtime checks, or generated-file ownership.

Use the project's own search tools when available. A broad text search should cover the exact spelling, casing, aliases, option names, and likely singular/plural variants of every important claim. Inspect callers and consumers, not only the declaration, when behavior depends on lifecycle, side effects, or surrounding state.

Keep generated files and dependency sources separate from maintained implementation. Generated output can confirm what a build emitted, but it is normally not the place to recommend edits. External ecosystem sources should be checked only after the repository evidence and should be authoritative for the ecosystem in question.

## 3. Map user journeys

For each audience-critical task, write a compact journey:

```text
entry point → prerequisites → install/setup → first successful result
            → common failure → recovery/reset → cleanup → next step
```

Identify which page owns each stage. Mark missing transitions, contradictory instructions, hidden prerequisites, environment assumptions, and steps that require a different identifier or version than an earlier step. For libraries, include import/export and lifecycle behavior. For CLIs, include working directory, positional arguments, flags, input/output shape, exit behavior, and session/target selection. For services or UIs, include startup, endpoint/route, authentication, state reset, and observable success.

Do not force these categories when they do not apply; adapt them to the project while preserving the end-to-end question: can the intended reader complete the task without guessing?

## 4. Build a claim/evidence matrix

Use one row per materially testable claim:

| Claim | Document location | Evidence source | Status | Verification gap |
| --- | --- | --- | --- | --- |
| Exact documented behavior | Path and heading | Symbol, schema, test, command, or URL | Implemented / documented / officially defined / runtime-observed / unverified | What remains unknown |

Prioritize claims that can make a task fail: imports, exported names, signatures, command syntax, flags, JSON/config shape, defaults, supported versions, permissions, URLs, identifiers, reset behavior, and safety warnings. Group repeated copies under one root cause and identify the canonical location to maintain.

## 5. Capture project vocabulary

Collect the names readers must use exactly: product and package names, public symbols, commands, flags, configuration keys, UI labels, protocol terms, resource identifiers, and lifecycle verbs. Determine each name from code, types, schemas, visible UI/CLI output, explicit project definitions, or authoritative ecosystem usage.

Report inconsistent naming only when the difference can confuse a task, contradicts a public contract, obscures a distinction, or leaves a project-specific term undefined. Do not rename an unfamiliar but valid ecosystem or project term merely to make it sound simpler.

## 6. Track context boundaries

Record what was intentionally not inspected and why: unrelated documentation, generated artifacts, unavailable runtime services, inaccessible private dependencies, expensive builds, unsupported environments, or out-of-scope product areas. A precise boundary is better than implying repository-wide certainty.
