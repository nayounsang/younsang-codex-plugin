# Test Quality Review

Use this rubric only when the reviewed change includes test files, specs, fixtures, mocks, or test helpers. It is a read-only review rubric: do not write, edit, or reformat tests.

Follow the repository's established language, naming, framework, and assertion conventions. Do not impose a spoken language or a project-specific style that the repository does not already use.

## Standard

Each test should prove one coherent scenario: one relevant actor or caller performs one action or flow under one condition and observes one outcome. Split a test when it proves independent behaviors, conditions, or outcomes.

Use Arrange, Act, Assert order:

1. **Arrange:** set up only the inputs, state, and collaborators needed for the scenario.
2. **Act:** perform the behavior under test once setup is complete.
3. **Assert:** verify the observable result of that behavior.

Keep multiple assertions together when they jointly establish one contract, such as the status, headers, and body of one response. Split assertions when they represent independent behaviors or outcomes.

Prefer the relevant user flow at the public boundary: what a UI user, CLI user, API consumer, or other product-facing caller does and observes. For pure functions, schemas, concurrency, and other behavior that cannot reasonably be expressed as a user flow, test the caller-facing technical contract instead.

## Dynamic test cases

Keep cases statically visible in the test file. Avoid generating a case list with `.map`, `.flatMap`, filtering, deduplication, or helpers when that hides which cases run, makes the suite grow unexpectedly, or prevents useful analysis.

Use parameterized tests when they express one shared scenario with the same Arrange, Act, and Assert shape and the rows remain easy to inspect. Prefer separately named tests when rows have different behavior, setup, or expected outcomes.

## Titles and observable outcomes

Test titles should state the condition and observable result. Words such as `correct`, `properly`, `appropriately`, `works`, or vague uses of `handles` are warning signs, not automatic violations.

Prefer titles such as:

```text
rejects a request when credentials are missing
returns no record when the requested identifier is absent
persists the updated value after a successful command
keeps a pending operation open after receiving an unrelated response
```

Do not report a title merely because it is not phrased in a preferred style. Report it when the title hides independent scenarios or makes the expected behavior materially unclear.

## Scenario separation

Do not hide independent scenarios behind conditional assertions in one test. If a test chooses different outcomes based on setup, split the conditions into separately named tests.

For example, prefer:

```ts
it("returns a response when the handler is enabled", async () => {
  const handler = createHandler({ enabled: true });

  await expect(sendRequest(handler)).resolves.toMatchObject({ status: 200 });
});

it("rejects the request when the handler is disabled", async () => {
  const handler = createHandler({ enabled: false });

  await expect(sendRequest(handler)).rejects.toThrow("disabled");
});
```

over a single test that branches between the two outcomes.

An enumerating title is a prompt to inspect the test, not an automatic failure. Split only when the listed actions, conditions, or outcomes are independently meaningful. A title describing one response's status, headers, and body may remain one scenario; a title describing creation, retrieval, and deletion usually should not.

## Review workflow

Before reporting an issue:

1. State the actor or caller, action, condition, and observable outcome represented by the test.
2. Confirm whether the test follows a user flow or a justified caller-facing technical contract.
3. Check that setup serves only that scenario.
4. Check that the Act phase performs the relevant behavior without unrelated actions.
5. Check that assertions focus on behavior rather than private helpers, incidental object shape, or call order unless those are the contract.
6. Check for hidden branches, generated cases, vague titles, and unnecessary implementation coupling.
7. Compare with neighboring tests and repository conventions before recommending a change.

## Finding criteria

Report a test-quality finding only when the issue is in a changed test-support file or test file and materially affects confidence, scenario clarity, failure diagnosis, or maintenance.

- `T1`: the test proves the wrong behavior, can pass while the intended behavior is broken, or combines conditions in a way that creates substantial false confidence;
- `T2`: the test hides independent scenarios, breaks meaningful AAA separation, obscures the observable outcome, or is materially coupled to implementation details;
- `T3`: a concrete localized issue in title clarity, static case visibility, setup scope, or test maintainability.

Do not report ordinary style preferences, a preferred assertion library, or a test that has more than one assertion when those assertions jointly establish one outcome.

## Test Quality Report

When this reviewer is activated, the final synthesis should include a short report stating:

- scenarios reviewed;
- whether AAA order was confirmed;
- whether the tests follow a user flow or a caller-facing technical contract;
- whether a technical-contract exception was used;
- any material test-quality findings and remaining coverage uncertainty.
