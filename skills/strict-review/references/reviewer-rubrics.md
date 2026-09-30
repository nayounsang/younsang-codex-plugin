# Reviewer Rubrics and Dispatch

All core reviewers run for every review. The dispatch plan controls depth and optional specialist reviewers, not whether security, performance, or readability are examined. The test-quality, dependency/implementation candidate, and ecosystem/adoption reviewers are conditional. They produce scoped supplemental output and do not replace the always-on reviewers.

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

### Readability and maintainability

Review whether a future contributor can follow the changed behavior and make a local, correct change without reconstructing hidden state or unrelated layers. Read the complete enclosing function or type, not only the diff hunk. Trace the main success path and at least one meaningful branch through the values and state it changes.

For each changed function or method, make a brief responsibility inventory before concluding. State its primary purpose, list the distinct policies, transformations, state changes, and I/O it owns, and identify what independent change or actor would cause each to change. Treat two or more independently changing concerns in one function as an SRP candidate when the code shows they can vary separately and keeping them together causes a concrete cost, such as unrelated edits sharing a large branch structure, separate behaviors requiring coordinated retesting, or one policy change risking another. Do not count sequential steps that form one cohesive operation as separate responsibilities, and do not use a responsibility count or function length alone as proof.

Look for concrete comprehension and changeability barriers such as:

- control flow whose behavior depends on deeply nested branches, compound conditions, or state mutations spread across helpers;
- a function or module that mixes policy, orchestration, I/O, and representation conversion so one behavior cannot be understood or changed locally;
- indirection, generic helpers, or wrappers that obscure the actual operation without removing meaningful duplication or coupling;
- duplicated rules or split ownership that require coordinated edits to keep one behavior consistent;
- comments needed to narrate what complicated code does, where a simpler expression or clearer structure would communicate it directly.

Report an `R` finding only when the changed code provides a concrete example and a maintenance consequence, such as a rule that must be updated in multiple places, a branch whose state transition cannot be followed at its call boundary, or a behavior that cannot be tested without unrelated systems. Do not report personal style, line count, nesting, or complexity metrics by themselves. A single clear comprehension barrier with a direct consequence is enough; do not require a second signal for a localized readability finding. Prefer an actionable simplification direction over a wholesale rewrite.

### Architecture and refactoring

Always perform a structural pass. Classify issues as:

- **Introduced:** the change creates the structural problem.
- **Amplified:** the change increases existing duplication, coupling, or affected surface.
- **Pre-existing:** unrelated to the change; omit it unless the change relies on or exposes it.

Adding another independently changing responsibility to an existing multi-purpose function amplifies its structural problem. Assess the full function and report the new responsibility when the change expands the reasons that function must change, even if the surrounding complexity predates the review range.

Report an `R` finding when the issue is introduced or amplified, has concrete code evidence, has a change-propagation/testing/reliability/security/performance/operational consequence, and has a proportionate improvement direction. Normally corroborate a structural concern with two independent code-level signals. One signal is sufficient when it directly demonstrates a high-impact boundary violation or an unavoidable cross-layer change; explain that evidence and consequence explicitly. Do not use this structural corroboration rule to suppress a supported readability finding.

Use signals such as independent reasons to change, duplicated policy or state transitions, coordinated edits across layers, dependency-direction violations, abstraction leakage, mixed policy/orchestration/I/O responsibilities, or tests that require unrelated external systems. Line count, method length, dependency count, and familiar patterns are investigation signals only.

### Semantic naming and domain model

Always inspect new or renamed identifiers, types, services, modules, and public parameters. Classify them as stable entities, lifecycle states, roles/capabilities, commands/events, persistence/transport representations, or read models.

Report a semantic finding only when the name claims a narrower state, role, phase, or invariant; the code does not consistently enforce it; the symbol is used outside that implied context or causes duplicate models/adapters/branches/unclear ownership; and a more stable existing concept or repository vocabulary is available. A state-specific local variable is acceptable when its narrow scope and preceding code guarantee the state. A state-specific type is acceptable only when construction and boundaries enforce the invariant, allowed operations differ, and the abstraction reduces rather than duplicates branching or conversion.

## Reference grounding

- [Google: What to Look For In a Code Review](https://google.github.io/eng-practices/review/reviewer/looking-for.html) — checks complexity, design, naming, and tests; it also recommends reading broader file and system context to assess code health.
- [Google: The Standard of Code Review](https://google.github.io/eng-practices/review/reviewer/standard.html) — treats readability, maintainability, and understandability as code-health outcomes while distinguishing them from subjective style preferences.
- [SonarQube: Metric definitions](https://docs.sonarsource.com/sonarqube-server/10.4/user-guide/metric-definitions) — defines Cognitive Complexity as a measure of control-flow understandability. Use such metrics to locate code for inspection, never as findings by themselves.

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
