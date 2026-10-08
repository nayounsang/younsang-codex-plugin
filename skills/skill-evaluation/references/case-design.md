# Case Design and Result Format

Use these fields to prepare human-reviewable case sets. The JSON is this skill's design format; convert approved cases to the execution format only if the selected runner requires it.

## Trigger set

Keep explicit invocation and automatic routing in separate cases. `expected_action` is one of `invoke_target`, `do_not_invoke`, or `invoke_other`; for `invoke_other`, name the expected skill. A case is not approved until the user confirms its expected action.

```json
{
  "schema_version": 1,
  "target_skill": "skill-name",
  "cases": [
    {
      "id": "auto-positive-01",
      "mode": "automatic",
      "prompt": "A realistic request that should select the target skill",
      "expected_action": "invoke_target",
      "expected_skill": "skill-name",
      "case_type": "positive",
      "reason": "Matches the skill's stated trigger",
      "boundary_pair_id": "pair-01",
      "basis": "stated in skill",
      "approved": false,
      "evidence_method": "local OTLP collector records codex.skill_invocation"
    }
  ]
}
```

Useful `case_type` values include `positive`, `hard_negative`, `minimal_pair`, `mixed_context`, `incomplete_input`, `cross_skill`, and `explicit_invocation`. Record `basis` as `stated in skill`, `confirmed by user`, or `inferred`. Do not score `approved: false` cases.

## Task quality set

Each success condition should express one observable fact. Keep expected and prohibited outcomes explicit, and make the verification method reproducible.

```json
{
  "schema_version": 1,
  "target_skill": "skill-name",
  "cases": [
    {
      "id": "task-happy-01",
      "prompt": "A realistic task request",
      "fixtures": ["fixtures/input.txt"],
      "initial_state": "A fresh workspace containing only the listed fixture",
      "success_conditions": [
        {
          "id": "output-exists",
          "condition": "The requested output file exists at the specified path",
          "verification": "Check the isolated workspace filesystem",
          "basis": "stated in skill",
          "approved": false
        }
      ],
      "prohibited_outcomes": [
        {
          "condition": "No file outside the isolated workspace is changed",
          "verification": "Compare the source workspace before and after",
          "basis": "confirmed by user",
          "approved": false
        }
      ],
      "rubric": null,
      "case_type": "happy_path",
      "side_effects": "none"
    }
  ]
}
```

For semantic checks, replace `rubric: null` with a user-approved rubric containing observable anchors for pass, partial, and fail. Do not invent a rubric after seeing outputs. Use unique case and assertion IDs. Keep fixture references inside the evaluation fixture directory.

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
| Case | Mode | Expected | Observed from local telemetry | Result | Evidence |
| ... |

For automatic-routing cases, count only target-skill invocation: `invoke_target` is positive; `do_not_invoke` and `invoke_other` are negative. An observed target invocation on a positive case is TP; no target invocation is FN. An observed target invocation on a negative case is FP; no target invocation is TN. Report counts only for approved, verified cases. Keep explicit-invocation cases outside these counts. Record which other skill, if any, was selected as per-case evidence; it does not change this target-specific classification.

Cross-skill routing: <per-case result>.

## Task quality results
| Case | Condition | With target skill | Baseline | Evidence |
| ... |

## Comparison and variability
<Per-case differences, repetitions, timing, token/tool use, and limits.>

## Unverified, failed, or skipped
<Case, reason, and effect on interpretation.>
```

Use `not applicable` rather than fabricate counts when a case category was not tested. Report task results as per-case outcomes and deltas; do not collapse them with trigger counts into an overall score. Include rates only with numerator, denominator, and the approved verified case IDs.
