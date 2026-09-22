# Reviewer Rubrics and Dispatch

All core reviewers run for every review. The dispatch plan controls depth and optional specialist reviewers, not whether security or performance are examined. The test-quality, dependency/implementation candidate, and ecosystem/adoption reviewers are conditional. They produce scoped supplemental output and do not replace the always-on reviewers.

## Common reviewer contract

Each reviewer must:

- inspect the changed code and its packet before forming a conclusion;
- trace at least one successful and one relevant failure or boundary path;
- cite concrete code, callers, consumers, tests, or external effects;
- distinguish introduced, amplified, and pre-existing conditions;
- return structured candidates, including an empty result when no issue is supported;
- avoid reporting style preferences, metrics alone, or hypothetical future requirements.

## Always-on reviewers

### Behavior and correctness

Check contracts, invariants, compatibility, empty and boundary inputs, duplicate requests, retries, timeouts, exception propagation, state transitions, partial failures, side-effect ordering, and resource release.

### Security

Always inspect changed trust boundaries, even when no obvious security keyword appears. Check authentication and authorization, ownership/tenant isolation, validation, injection, sensitive-data exposure, unsafe deserialization, redirects, file paths, code execution, secrets, logs, error responses, and security configuration. A single concrete security path is sufficient for a candidate; reviewer consensus is not required.

### Performance

Always inspect the cost model of changed behavior. Check repeated work, data size, query count, N+1 behavior, unbounded inputs, serialization, network/filesystem I/O, cache consistency, retries, timeouts, concurrency, memory, and hot paths. A concrete loop, I/O path, data-volume assumption, or resource consequence is enough for a candidate; do not require a second reviewer to agree.

### Architecture and refactoring

Always perform a structural pass. Classify issues as:

- **Introduced:** the change creates the structural problem.
- **Amplified:** the change increases existing duplication, coupling, or affected surface.
- **Pre-existing:** unrelated to the change; omit it unless the change relies on or exposes it.

Report an `R` finding when the issue is introduced or amplified, has at least two independent code-level signals, has a concrete change-propagation/testing/reliability/security/performance/operational consequence, and has a proportionate improvement direction.

Use signals such as independent reasons to change, duplicated policy or state transitions, coordinated edits across layers, dependency-direction violations, abstraction leakage, mixed policy/orchestration/I/O responsibilities, or tests that require unrelated external systems. Line count, method length, dependency count, and familiar patterns are investigation signals only.

### Semantic naming and domain model

Always inspect new or renamed identifiers, types, services, modules, and public parameters. Classify them as stable entities, lifecycle states, roles/capabilities, commands/events, persistence/transport representations, or read models.

Report a semantic finding only when the name claims a narrower state, role, phase, or invariant; the code does not consistently enforce it; the symbol is used outside that implied context or causes duplicate models/adapters/branches/unclear ownership; and a more stable existing concept or repository vocabulary is available. A state-specific local variable is acceptable when its narrow scope and preceding code guarantee the state. A state-specific type is acceptable only when construction and boundaries enforce the invariant, allowed operations differ, and the abstraction reduces rather than duplicates branching or conversion.

### General test and boundary concerns

The behavior and boundary reviewers may still report material missing coverage or contract risks for production changes. Do not apply the test-quality rubric unless the test-quality reviewer is activated.

## Conditional specialists

### Test quality reviewer

Activate this reviewer only when changed files include tests, specs, test fixtures, mocks, or test helpers. Inspect those files and the minimum implementation contract, callers, fixtures, and neighboring tests needed to judge them. Do not apply test-specific style or refactoring rules to production files when no test file is in scope.

Apply the full rubric in [test-quality-review.md](test-quality-review.md). In particular, check one coherent scenario per test, Arrange-Act-Assert order, observable-result titles, hidden branches, dynamic case visibility, unnecessary implementation coupling, and whether the test follows a user-facing flow or an appropriate caller-facing technical contract.

Do not require a specific spoken language. Follow the repository's existing language and naming conventions.

### Dependency and implementation candidate reviewer

Activate for changed production logic that implements a reusable capability, including utilities, parsing, validation, date/time handling, retry/backoff, serialization, authentication, UI primitives, state management, or similar concerns. This reviewer produces dependency candidates, not defects.

Read [dependency-candidate-review.md](dependency-candidate-review.md). Search both declared or installed dependencies and relevant internal utilities, and broader ecosystem capabilities that are not installed. Use the changed logic's responsibility as the query, not only package-name guesses. Keep every materially relevant candidate with its evidence, confidence, and caveats. Do not report a candidate merely because a package exists; it must materially overlap the changed responsibility. Do not require adoption or treat the candidate as a confirmed defect.

### Ecosystem and adoption reviewer

Activate when the change introduces or begins using a framework, library, plugin, adapter, or framework-specific configuration, or when changed logic enters a framework-specific boundary. Read [ecosystem-adoption-review.md](ecosystem-adoption-review.md).

Review broadly and shallowly across the relevant ecosystem: companion packages, peer dependencies, adapters, configuration, runtime boundaries, version compatibility, conventional integrations, and known framework constraints. This reviewer reports ecosystem candidates and missing-context questions; it does not perform a deep package audit or replace the core correctness/security review.

### Other conditional specialists

Add these reviewers when the manifest indicates relevant scope:

- database and migrations;
- API or event contract compatibility;
- concurrency and resource lifecycle;
- deployment, configuration, observability, or staged rollout.

An optional specialist may be skipped only with a recorded reason in the manifest and final coverage section.

## Dispatch policy

The manifest may use cheap deterministic signals—changed paths, imports, symbol names, schemas, and diff shapes—to deepen packets or select specialists. These signals must never disable the core security or performance reviewers. If classification is uncertain, use the deeper packet.
