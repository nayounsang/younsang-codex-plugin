# Context Packets and Review Coverage

The reviewer's understanding must be bounded by explicit packets rather than a full-repository prompt. The repository snapshot and all file reads must be tied to the resolved review range so a dirty or moving worktree cannot change the evidence during review.

## Review manifest

Build one shared manifest before reviewer fan-out:

```yaml
review_manifest:
  base_commit: <merge-base>
  head_commit: <reviewed-head>
  changed_files: []
  changed_symbols: []
  changed_boundaries: []
  callers_and_consumers: []
  relevant_tests: []
  repository_vocabulary: []
  selected_specialists: []
  dependency_search_scope: []
  omitted_context: []
```

Inspect the complete changed files when practical, then retrieve only context relevant to each changed symbol: enclosing function/class, direct callers and consumers, sibling implementations, interfaces, schemas, tests, and external boundaries. Use existing repository instructions and conventions as evidence.

## Packet construction

Every reviewer receives:

1. the shared diff and changed-symbol list;
2. the reviewer-specific rubric;
3. relevant surrounding code and call relationships;
4. relevant tests and boundary information;
5. repository vocabulary and applicable instructions;
6. an explicit context budget and tool budget;
7. the required structured output schema.

Do not dump the whole repository into every packet. Do not use blind tail truncation. Prioritize context in this order:

1. changed code and enclosing control flow;
2. direct callers, callees, consumers, and side effects;
3. interfaces, schemas, contracts, and state definitions;
4. relevant tests and sibling implementations;
5. repository-wide conventions and documentation.

If a budget is reached, record the omitted path and why it was lower priority. A reviewer must not infer that omitted code is safe.

## Core packets

Use separate packets for the always-on reviewers:

- **Behavior:** changed control flow, success/failure paths, inputs, retries, state transitions, and external effects.
- **Security:** trust boundaries, identity, authorization, validation, secrets, sensitive data, code/data interpretation, and unsafe sinks.
- **Performance:** data volume, repeated work, I/O, query behavior, caching, retries, concurrency, memory, and hot paths.
- **Architecture:** responsibilities, dependency direction, change propagation, duplication, abstraction boundaries, and test seams.
- **Semantic model:** new or renamed symbols, domain vocabulary, state/role/entity distinctions, constructors, factories, and all relevant call sites.
- **Test quality, conditional:** changed test files, specs, fixtures, mocks, helpers, the minimum public contract under test, and neighboring tests.
- **Dependency candidates, conditional:** changed production logic, local dependency and utility inventory, capability-relevant imports and symbols, and broad ecosystem search results. Do not limit the packet to installed packages.
- **Ecosystem adoption, conditional:** introduced or newly used framework/library/plugin, relevant manifest and lockfile entries, framework configuration, runtime target, companion integrations, and version/peer-dependency context.

## Coverage ledger

Record, per changed file and core or activated specialist reviewer:

```yaml
coverage:
  - path: src/orders/OrderService.ts
    reviewer: architecture
    status: inspected | partial | omitted
    evidence_sources: []
    omission_reason: null
```

The final review must disclose partial or omitted context. A clean result with incomplete coverage is not equivalent to a clean result with complete coverage.

For dependency and ecosystem reviewers, also record the search source and whether external ecosystem lookup was available. A candidate search with only local repository sources is partial coverage for uninstalled capabilities.
