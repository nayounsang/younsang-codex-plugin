# Case Design and Result Format

Write human-reviewable test cases as one sentence in the evaluation plan. Use `When` and `Then`, with an optional `Who`. Include `Who` only when a specific user or persona is relevant to the case; omit generic actors such as “user” or “developer.” Codex supplies the concrete request in `When`, and the sentence states the expected observable behavior in `Then`. Include the relevant basis or verification detail in the sentence when it helps explain the expectation. Do not split a case into separate prompt, expected-result, criterion, or verification fields.

## Trigger set

Keep explicit invocation and automatic routing in separate cases. The `When` clause should contain the complete request Codex will submit. `Then` must unambiguously say that Codex invokes or does not invoke the target skill; derive `invoke_target` or `do_not_invoke` from this wording when reporting results. A case is not approved until the user confirms its expected behavior.

Example:

```markdown
- When `$younsang-codex-plugin:api-scenario-forge` is explicitly invoked, Codex invokes `api-scenario-forge`; record this separately from automatic-routing results.
```

## Task quality set

Use one sentence per task case. State the request in `When` and express the expected task outcome in `Then`. Include fixture or initial-state details in the sentence when they define the case. Keep expectations observable and disputed expectations unresolved until the user decides.

```markdown
- “격리된 테스트 앱에서 상세 API를 `404`로 설정하고 페이지를 열어 주세요”라고 요청하면, 페이지에 ‘찾을 수 없음’ 화면이 나타나고 캡처로 확인됩니다.
```

If a semantic outcome cannot be judged from the sentence alone, explain the unresolved interpretation to the user before approval; do not invent a rubric after seeing outputs. Use the approved case sentences to identify results in the report. Keep fixture references inside the evaluation fixture directory.

## Report format

```markdown
# Skill evaluation: <target>

## Run conditions
- Approved plan: <reference or summary>
- Codex version, local collector, model, permissions, and repetitions: <values>
- Workspace isolation and cleanup: <verified result; retained artifacts copied before cleanup>
- Persistent artifact directory: <approved path>
- Artifacts: <verified paths>

## Trigger results
| Case sentence | Mode | Expected | Observed from local telemetry | Result | Evidence |
| ... |

For automatic-routing cases, count only target-skill invocation: `invoke_target` is positive and `do_not_invoke` is negative. An observed target invocation on a positive case is TP; no target invocation is FN. An observed target invocation on a negative case is FP; no target invocation is TN. Report counts only for approved, verified cases. Keep explicit-invocation cases outside these counts. Other skill selections are outside the evaluation criteria.

## Task quality results
| Case sentence | Outcome | With target skill | Baseline | Evidence |
| ... |

## Comparison and variability
<Per-case differences, repetitions, timing, token/tool use, and limits.>

## Errors, failed, or skipped
<Case, reason, and effect on interpretation.>
```

Use `not applicable` rather than fabricate counts when a case category was not tested. Report task results as per-case outcomes and deltas; do not collapse them with trigger counts into an overall score. Include rates only with numerator, denominator, and the approved verified case sentences.
