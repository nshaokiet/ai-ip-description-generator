# Security Review — <TASK-ID>

Template version: 0.1.0 (first explicit version, 2026-11-18; GOV-REVIEWER-002).

Review type: SECURITY
Reviewer role: SECURITY_REVIEWER
Verdict: <PASS | REQUEST_CHANGES | BLOCKED>

## Review identity

| Field | Value |
|---|---|
| Task ID | `<TASK-ID>` |
| Reviewer agent identity | `<agent_id>` |
| Actual session ID | `<observed session ID>` |
| Actual model | `Gemini 4 Argon` (verify actual runtime; no implicit substitute) |
| Actual profile | `High` (verify actual runtime) |
| Fresh session / reused | `<YES/NO/UNKNOWN> / <YES/NO/UNKNOWN>` |
| Prior task/role context if reused | `<disclose or N/A>` |
| Reviewer permissions | `STRICT READ-ONLY` |
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
- [ ] Security and Quality have distinct actual reviewer identities/sessions; actual model/profile and freshness/reuse are recorded.
- [ ] If Gemini 4 Argon (High) is unavailable/unverifiable, STOP and obtain explicit Human authorization before substitution.
- [ ] Reviewer did not modify tracked implementation files.
- [ ] Any earlier PASS on a different implementation SHA was treated as stale.

## Verdict

`<PASS | REQUEST_CHANGES | BLOCKED>`

Rationale: `<concise evidence-based rationale>`

`provisional_ready != authoritative_merge_eligible`. A Security PASS is required
evidence where policy requires Security review, but it is not merge authorization
and does not replace authoritative/fresh pre-merge verification.

History: unversioned -> 0.1.0, 2026-11-18, Codex; record permanent Human model
selection and actual session/freshness; preserve all read-only, independent,
exact-SHA, CI/security and Human merge gates. No product/API or role-authority
breaking change. Source: [GOV-REVIEWER-002](../../docs/decisions/GOV-REVIEWER-002-permanent-reviewer-model.md).
