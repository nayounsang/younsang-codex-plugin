# Verification and Synthesis

Reviewer outputs are candidates, not final findings. Keep the verification and synthesis stages separate from specialist reasoning.

## Candidate schema

Each reviewer should return records shaped like:

```yaml
candidate:
  category: correctness | security | performance | architecture | semantic-model | test-quality | dependency-candidate | ecosystem-candidate | operations
  priority: P0 | P1 | P2 | P3 | R1 | R2 | R3 | T1 | T2 | T3 | candidate
  status: proposed
  path: src/example.ts
  line: 42
  title: imperative title
  trigger: introduced | amplified | pre-existing
  evidence:
    - concrete code path or call relationship
    - concrete boundary, test, or resource consequence
  affected_path: concrete input or operating condition
  consequence: observable impact
  remedy: proportionate direction
  confidence: high | medium | low
  candidate_details:
    responsibility: null
    capability: null
    installed: yes | no | unknown
    sources: []
    caveats: []
```

## Independent verification

Verify candidates in parallel where possible. The verifier receives the candidate, relevant packet, and source code, but not the reviewer's persuasive narrative or intended conclusion. This reduces anchoring.

The verifier must check:

- the cited file, symbol, and line exist;
- the affected path is reachable or clearly conditional;
- the issue was introduced or amplified by the reviewed change;
- the evidence supports the stated consequence;
- the priority is proportional;
- the proposed direction addresses the cause rather than only the symptom.

Classify each candidate:

- **confirmed:** retain a defect candidate as a P, R, or T finding; retain a dependency or ecosystem candidate in its dedicated candidate section;
- **plausible:** retain a defect candidate as a Candidate risk when the trigger and path are concrete but one fact remains unverified; retain a dependency or ecosystem candidate with its confidence and caveats;
- **unsupported:** remove and record the reason internally.

For `dependency-candidate` and `ecosystem-candidate` records, additionally check:

- the changed code actually owns the stated responsibility;
- the proposed capability materially overlaps that responsibility;
- the source supports that the capability exists and is relevant;
- installed status is accurate and does not exclude an uninstalled but relevant candidate;
- caveats such as runtime, framework, bundle, or peer-dependency fit are stated when known.

Do not remove a security or performance candidate merely because it is unique to one reviewer. Remove it only when the path, code evidence, or change relationship cannot be supported.

## Synthesis

The synthesizer must:

1. group findings by same root cause, not merely matching keywords;
2. merge duplicate evidence while preserving the strongest affected path;
3. resolve factual conflicts by returning to the source code and manifest;
4. retain a unique finding when its evidence is independently sufficient;
5. calibrate P, R, and T priority separately;
6. move incompletely verified but concrete risks to `Candidate risks` rather than presenting them as confirmed;
7. keep dependency and ecosystem candidates in their dedicated sections rather than converting them into P/R findings without independent defect evidence;
8. disclose omitted context, partial coverage, skipped optional specialists, unavailable ecosystem sources, and unresolved uncertainty.

Do not require majority vote or multi-reviewer consensus. Consensus can reduce false positives but can also suppress a unique security, performance, or architecture issue.

## Final finding forms

Use:

```text
[P1] Imperative defect title — path/to/file.ts:line
```

or:

```text
[R2] Imperative structural or semantic title — path/to/file.ts:line
```

or, when the test-quality reviewer was activated:

```text
[T2] Imperative test-quality title — path/to/file.test.ts:line
```

Follow with a short paragraph containing the trigger, code-path evidence, consequence, and proportionate remedy. Candidate risks must state what is concrete and what remains unverified; do not assign them a P or R priority.

Dependency and ecosystem candidates should state the changed responsibility, candidate capability, source evidence, installed status when known, confidence, and relevant caveats. They are suggestions for follow-up review, not adoption mandates.

P priorities:

- `P0`: universal release blocker or critical failure;
- `P1`: urgent defect that should be fixed next;
- `P2`: ordinary defect that should be fixed;
- `P3`: low-impact defect still worth fixing.

R priorities:

- `R1`: serious boundary, dependency, or change-propagation problem;
- `R2`: material responsibility mixing, duplicated policy, semantic ambiguity, or test coupling;
- `R3`: concrete localized structural or naming improvement with limited current impact.

T priorities:

- `T1`: the test is misleading, proves the wrong behavior, or creates substantial false confidence;
- `T2`: the test combines independent scenarios, obscures the observable outcome, or is materially coupled to implementation details;
- `T3`: a concrete localized test-clarity or maintainability issue with limited current impact.
