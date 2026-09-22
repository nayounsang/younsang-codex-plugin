# Dependency and Implementation Candidate Review

Use this rubric only for changed production logic that implements a reusable capability. The output is a broad candidate inventory, not a claim that the code is defective or that a package must be adopted.

## Search objective

Find relevant capabilities that the change reimplements or could reasonably reuse. Search both:

1. capabilities already declared, installed, imported, or implemented internally;
2. relevant capabilities available in the broader ecosystem even when they are not installed.

Use the logic's responsibility as the search query, not only names remembered by the reviewer. Candidate areas include date/time, parsing, validation, serialization, retry/backoff, HTTP, caching, crypto/authentication, state management, UI primitives, focus/keyboard behavior, positioning, and similar reusable concerns.

## Search passes

### Local capability pass

Inspect manifests, lockfiles, workspace packages, direct imports, exported symbols, internal utilities, existing abstractions, and neighboring implementations. Confirm whether a candidate is already installed or available inside the repository.

### Ecosystem capability pass

When ecosystem lookup is available, search current package metadata, official documentation, framework ecosystems, and trusted catalogs for capabilities that match the changed responsibility. Verify that a named package or library actually exists and provides the claimed capability; do not rely on memory alone. If external lookup is unavailable, retain local results and disclose that uninstalled ecosystem coverage is partial.

Search broadly across plausible capability categories, but do not perform a deep audit of every package or compare implementation internals. The goal is recall-oriented candidate generation.

## Candidate criteria

Keep a candidate when:

- the changed code has a concrete responsibility;
- the proposed dependency or internal utility materially overlaps that responsibility;
- the candidate is supported by repository evidence or a current ecosystem source;
- a useful caveat can be stated when fit depends on runtime, framework, bundle, license, or peer dependencies.

Do not create a candidate merely because a popular package exists. Do not require the candidate to be installed. Do not turn a candidate into a P/R finding unless a separate reviewer establishes a concrete defect, security issue, or material structural consequence.

Examples of the intended search shape include checking for date/time libraries when date arithmetic is handwritten, UI primitive libraries such as Base UI or Radix when focus/overlay behavior is implemented directly, and ecosystem utilities such as an existing toolkit when equivalent helpers are reimplemented.

## Candidate record

Return records shaped like:

```yaml
dependency_candidate:
  path: src/example.ts
  responsibility: date range and timezone calculation
  capability: date/time utility library
  candidate: date-fns
  installed: no
  evidence:
    - changed function manually parses and compares calendar values
    - current ecosystem source documents the matching capability
  confidence: medium
  caveats:
    - confirm timezone requirements and runtime/bundle policy
```

Retain all materially relevant candidates. Rank or group them for readability, but do not silently drop lower-confidence candidates when their responsibility match is concrete.
