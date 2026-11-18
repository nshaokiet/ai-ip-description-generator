# GOV-REVIEWER-002 — Permanent independent reviewer model

| Field | Value |
|---|---|
| Document ID / tracking reference | GOV-REVIEWER-002 (repository documentation reference, not an authentication token) |
| Version | 0.1.0 |
| Status | Human policy APPROVED / effective; separate documentation PR pending independent review, CI and Human merge authorization |
| Decision / effective date | 2026-11-18 |
| Decider | Human / Product Owner |
| Recorder | Codex / IMPLEMENTER; not independent reviewer |
| Scope | Permanent standing reviewer selection; documentation only |
| Authority source | Direct Human message in the current conversation, titled `PERMANENT HUMAN AUTHORIZATION — WORKFLOW V1 REVIEWER MODEL UPDATE`, repository nshaokiet/ai-ip-description-generator |
| Supersedes | The 2026-10-14 Gemini 3.8 Flash High standing selection in AGENTS.md §6.1 / GOV-REVIEWER-001; preserves historical reports |
| Remains effective until | Explicitly superseded by a subsequent Human decision |

## Human decision and immediate applicability

The Human explicitly states **APPROVED — PERMANENT**, replacing:

- OLD: Gemini 3.8 Flash High.
- NEW / **Standing Authorized Reviewer: Gemini 4 Argon (High)**.

The direct decision applies immediately to **all current and future independent
Security and Quality reviews**, including **DEP-SEC-20261118-001 / PR #165**.
For PR #165, the prior **REVIEW_MODEL_AUTHORIZATION_REQUIRED** blocker is resolved
by this model-selection authority. Gemini 4 Argon (High) may perform the actual
independent reviews in STRICT READ-ONLY mode. Availability, session identity,
review execution, verdicts and acceptance remain facts to verify, not facts
established by this authorization. No older report receives retroactive PASS or
model reattribution.

The policy is effective from the Human decision while this separate documentary
sync is pending. An unmerged documentation branch does not constitute a merge,
review result or runtime activation. This record attributes the actual Human
message; it does not invent a GitHub approval/comment, session ID, signed
authorization or MCP state. No external message permalink was supplied.

## Mandatory reviewer procedure

1. Verify the actual selected model **Gemini 4 Argon** and profile **High** before
   each review. No alias, profile downgrade or substitute is implicitly allowed.
2. If Gemini 4 Argon (High) is unavailable, mismatched or unverifiable, **STOP the
   affected review and request explicit Human authorization before substituting
   another model**. No automatic fallback.
3. Preserve **STRICT READ-ONLY**: no tracked/production writes, remediation,
   commit, push, merge, deployment or approval/task-state mutation by reviewers.
   Authorized isolated tests may create only owned temporary output under the
   existing read-only-review rules. Reviewer writes cannot satisfy independent
   PASS and must not be concealed.
4. Record actual model, profile, reviewer identity, actual session ID, review
   timestamp, fresh-session YES/NO/UNKNOWN, reuse YES/NO/UNKNOWN and prior
   task/role context for any reused session. Never infer freshness from a model
   label. Missing/unverifiable identity or independence blocks the affected gate.
5. Maintain **independent Security and Quality evidence** with distinct actual
   reviewer identities/sessions and separately authored reports/verdicts. Neither
   uses the other's verdict as proof. Model equality does not establish identity
   or independence; Implementer self-check is not independent review.
6. Review the same immutable final HEAD with exact repository/base/HEAD/spec,
   changed-file scope, tests/CI/security evidence, source-cited findings and
   PASS / REQUEST CHANGES / BLOCKED. A new candidate SHA requires applicable fresh
   CI/review; no old-SHA PASS is reused for changed content.
7. Preserve every CI/security gate, unresolved-finding rule, fresh PR/base/head
   verification, expected-head protection and applicable Human merge gate. This
   authorization does not merge any PR or authorize deployment. **This separate
   documentation-only PR must not merge without Human authorization.**

Workflow V1 remains the path for an authorized unenrolled task. V2 activation,
enrollment, role assignment, separate streams and MANUAL_EXTERNAL requirements
remain unchanged. Model selection is not task authorization, authenticated
identity, API funding, provider-runtime selection, Claims activation, production
security acceptance or permission to use real/confidential research.

## Documentation scope and verification boundary

This update changes AGENTS.md §6.1, the reviewer-selection guide, ADR-003 through
an explicit addendum, Security/Quality report templates, the agent-package
documentation pointer and README status. Historical model names, verdicts and
finding history remain intact. Product source, dependencies/lockfiles,
validators/tests, workflow configuration, activation markers and policies for
provider/Claims/data are outside this documentation diff.

AGENTS.md is versioned **0.6.2 -> 0.6.3**. The existing
`tools/validate_workflow_v2_governance.py` hard-codes a current metadata phrase
`| Version | 0.6.2 |`; its structural check therefore needs a separately
authorized code/test alignment to accept the newer document version. Do not
retain a false current version, insert obsolete metadata merely to satisfy the
check, suppress the failure or alter validator/test code in this documentation
PR. Record the actual check result; required CI stays mandatory before merge.
The inherited frontend dependency-security gate is also not waived; separate
PR #165 retains its own review and Human merge requirements.

Validation here proves document scope/links and existing package/governance
checks only. It does not run Gemini, authenticate a session, create independent
PASS or waive an unsuccessful gate. Record new HEAD/TREE/PR/hosted results in
the publication handoff after they exist; no future SHA is fabricated here.

Actual local checks on this candidate: `agents/validate_skills.py` PASS (14/14
P0 skills). The combined existing governance/package suites report **79 PASS,
5 FAIL**; all five failures arise from the hard-coded AGENTS metadata version
(including the old-version mutation test). The standalone governance validator
is **BLOCKED / exit1**, missing the obsolete current-version phrase. These are
real unresolved validation failures, not a CI exception or independent verdict.

## Version history

| Old | New | Date | Author | Change / reason / authority | Breaking change |
|---|---|---|---|---|---|
| None | 0.1.0 | 2026-11-18 | Codex | Record permanent Human reviewer-model replacement and documentary scope; direct Human message above | No product/API or role-authority change; prior selection explicitly superseded |

## Handoff

Task ID: GOV-REVIEWER-002 (documentation tracking ID)
Agent: Codex / IMPLEMENTER
Reviewer: Gemini 4 Argon (High), independent Security and Quality, STRICT READ-ONLY; not invoked / PENDING
Status: Human policy effective; documentation candidate; no merge or project Completed claim
Version: 0.1.0
Work completed: Canonical standing selection, source-attributed permanent decision, separate actual-session/freshness templates and documentation pointers
Files affected: Documentation-only PR diff; PR164/165 implementation branches unchanged
Evidence checked: Direct Human authorization; verified main; AGENTS §6.1, ADR-003, GOV-REVIEWER-001, actual template/validator sources
Findings: Legacy version-specific validator requires separate authorized alignment; all unsuccessful/missing CI/review gates remain blocking
Decisions: Permanent selection effective 2026-11-18; PR165 model-only blocker resolved; no model substitution without explicit Human authorization
Issues: Documentation independent review/CI and explicit Human merge authorization remain; MCP operational tools unavailable, no lease/state invented
Security impact: Reviewer selection only; STRICT READ-ONLY, independent exact-HEAD evidence, CI/security and Human merge gates preserved
Recommended next action: ChatGPT coordinate actual independent Security/Quality reviews with the authorized model; Human decide any separate metadata-validator alignment and later merge; no automatic merge

API budget USD0. Provider NOT_RUN. Product Claims DISABLED. Semantic readiness
NOT_DETERMINED. Live spend enforcement NOT_IMPLEMENTED.
