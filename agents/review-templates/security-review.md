# Security Review — <TASK-ID>

Review type: SECURITY
Reviewer role: SECURITY_REVIEWER
Verdict: <PASS | REQUEST_CHANGES | BLOCKED>

## Review identity

| Field | Value |
|---|---|
| Task ID | `<TASK-ID>` |
| Reviewer agent/session | `<agent_id>` |
| Model/profile, if relevant | `<model_profile or N/A>` |
| Specification version/artifact | `<version/path>` |
| Specification SHA | `<40-char SHA>` |
| Base SHA | `<40-char SHA>` |
| Implementation SHA | `<40-char SHA>` |
| Review timestamp/reference | `<timestamp/reference>` |
| Tracked implementation files modified by reviewer | `false` |

## Files / diff reviewed

- `<file, diff range, or immutable diff reference>`

## Tests and evidence inspected

- `<test/CI/evidence reference and observed result>`

Evidence-level note: `RECORDED != VERIFIED`. For each material Git, CI, review,
authorization, or provenance claim, state the observed verification level/source.
Do not infer authoritative verification from MCP recording alone.

## Security findings

| ID | Severity | Evidence | Finding | Required resolution |
|---|---|---|---|---|
| SEC-001 | `<CRITICAL/HIGH/MEDIUM/LOW/INFO>` | `<file/test/evidence>` | `<finding>` | `<resolution or N/A>` |

If there are no findings, replace the example row with `None`.

## Blocking findings

Count: `<0 or positive integer>`

- `<blocking finding IDs or None>`

## Independence checks

- [ ] Review targets the exact implementation SHA shown above.
- [ ] Reviewer identity is independent from the Implementer for this review stream.
- [ ] Security verdict was authored independently from the Quality verdict.
- [ ] Reviewer did not modify tracked implementation files.
- [ ] Any earlier PASS on a different implementation SHA was treated as stale.

## Verdict

`<PASS | REQUEST_CHANGES | BLOCKED>`

Rationale: `<concise evidence-based rationale>`

`provisional_ready != authoritative_merge_eligible`. A Security PASS is required
evidence where policy requires Security review, but it is not merge authorization
and does not replace authoritative/fresh pre-merge verification.
