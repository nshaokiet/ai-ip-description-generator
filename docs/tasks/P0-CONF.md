# P0-CONF — bounded offline confidentiality decisions

| Field | Value |
|---|---|
| Version / date |0.1.2 /28/11/2026 Asia/Saigon |
| Owner / implementer | Nguyễn Song Hào Kiệt — Independent Developer /Codex |
| Authority | Actual Owner AUTONOMOUS PROJECT CONTINUATION22/11/2026, C1 P0.1; current conversation, no fabricated original receipt or retrospective approval |
| Workflow | Authorized new unenrolled V1 task; no V2 migration/enrollment/lease claimed. AGENTS unchanged;168 NOT_EFFECTIVE |
| Status | RECONCILED_CANDIDATE /EXACT_HEAD_CI_PENDING /FRESH_DUAL_REVIEW_PENDING; not Completed |
| Base / branch | accepted main `3b3891f5452083bf09cc4f10388b7145d73ea5c4` / `feature/p0-conf-offline-consent-20261122` |
| Business objective | Bind explicit Human egress consent to actual paper revision, payload, purpose and destination before future provider/search integration |
| Current evidence reused | Canonical SHA256 helper from supported_draft_claims_validation; bounded immutable JSON snapshot from custody_review; existing no-provider tripwire |
| Missing scope addressed | Native offline decision store only, independent of unmerged164/165/166/167/168. Actual routes/providers/website workflow remain unwired |
| Complexity / risk | M /HIGH confidentiality: require independent Security AND Quality on final immutable HEAD/TREE |
| Funding | FREE — CAN IMPLEMENT NOW; USD0; no provider/network/real-paper/deploy |
| Proposed PR scope | One additive service, functional/negative tests, this task record, README status and Control Center pointer. No new dependency/schema/feature flag or global policy |

## Current authorized integration — 28/11/2026

Human continuation explicitly authorizes reconciling accepted PR164 main into this existing PR, scope-preserving conflict resolution, offline tests, normal commit/push, CI/security verification, Draft PR updates and independent review coordination. Original 22/11 authorization and implementation remain preserved; this is prospective integration authority, not retrospective approval.

Accepted PR164 merge `3b3891f5452083bf09cc4f10388b7145d73ea5c4`, TREE `2252e514c339de12bd2d43a02ae5650e93b8ed13`, exact-main CI46124575472 SUCCESS and [closeout](https://github.com/nshaokiet/ai-ip-description-generator/pull/164#issuecomment-7236596530) establish the integration baseline. Original candidate HEAD `df356efbf44d0b99d586eec2ca860eb0cee6330f` is the other merge parent. Runtime confidentiality and its tests must remain byte-identical to that candidate; accepted website/publication, leases, dependencies and snapshot fixes remain unchanged. Resolve only README/Control Center documentary conflicts by preserving both dated records.

This cycle uses the Human-authorized **Gemini 4 Argon (Medium)** override, separate Security and Quality sessions, STRICT READ-ONLY, exact final BASE/HEAD/TREE, complete original reports plus identical backups/digests and actual execution evidence. Earlier High requests and old pending/failing CI below are dated history. No reviewer dispatch or PASS is claimed. Human prohibits Computer Use; if a direct reviewer connector is unavailable, prepare two copy-ready prompts for the exact candidate. Coordinator must read both complete reports and compare technical descriptions to immutable source.

Current gates: fresh exact-HEAD CI/security artifact and fresh independent dual review PENDING. Each immutable result belongs in the PR/evidence receipt. Keep PR Draft; any required new exact-candidate Human merge decision is preserved. No provider callsites are wired by this merge: consent remains a callable offline service, not proof the accepted website enforces egress consent or complete cross-session transport integration. No runtime/policy/dependency expansion, real data, paid call, Claims activation, precommit implementation or role-reversal activation.

The original acceptance criteria below remain unchanged. Version 0.1.1 -> 0.1.2, 28/11/2026, Codex: factual integration/review-baseline reconciliation, no consent API or policy change; Breaking change: No.

## Acceptance criteria and implementation

- Default missing classification/consent/authority denies; PUBLIC classification also does not imply egress consent. Upload/display are not consent.
- Trusted host authorizer must explicitly accept the complete immutable requested action: owner/actor/context/source/revision/classification/payload hash/destination/purpose/expiry. Caller-provided actor string alone is not authenticated identity or permission.
- Exact payload hash checked with reused canonical JSON/SHA256 and bounded snapshot; same JSON key order variations may match, changed content cannot. Source hash/revision/document/owner/purpose/destination cannot cross scopes.
- Classification/revision change invalidates consent, lower revision cannot roll back, same-revision source substitution denied. Revoke clears grants; expiry (including during authorization), callback error, invalid host clock or reentrant state mutation deny.
- Bounded process-local records/scopes; immutable receipt with actual UTC clock time, actor, context and scope. No raw source/query/payload stored or logged; no receipt accepted as bearer authority. Persistent audit/history belongs to P1-CASE.
- No endpoint/provider/search activation, actual egress, billing, Claims runtime, auth policy replacement, dependency change or production deployment. The service is functional offline infrastructure, **not proof existing provider paths are protected**.

Trusted host responsibilities before separately reviewed integration: authenticated principal and genuine Human action, authoritative custody/source revision, safe preview of exact outgoing payload, registered destination-to-transport mapping, immediate recheck before send, durable receipt/retention if required. This module neither verifies external identity nor prevents a host from bypassing an unintegrated guard; caller assertions alone are not external truth.

## Test plan and evidence

`pytest tests/backend/test_confidentiality.py tests/backend/test_extraction_runtime.py tests/backend/test_draft_runtime.py tests/backend/test_preapi_provider_tripwire.py -q -p no:cacheprovider`, Python3.12 Windows, live flags0. Actual final local result: **89PASS/0FAIL/0SKIP**,11.00s, comprising36 confidentiality tests +21 extraction +25 draft +7 tripwire contracts,1 existing deprecation warning. Immutable SHA/TREE and hosted CI are in PR receipt; no future commit SHA embedded here. Tests cover success, fail-closed authority, public/unpublished classification, exact scope/source/payload binding, mutation/revocation/reclassification, expiry, bounded inputs/capacity, clock/callback errors and zero SDK/network activity. Provider regressions remain unmodified.

Existing base source full-suite evidence from same-day REALIGN inventory:1266PASS/3SKIP (Windows), MCP158PASS, frontend lint/typecheck/security75PASS. These are **baseline**, not substitutes for new-candidate CI. Next16.4.1 audit1MODERATE/0HIGH/CRITICAL remains on main; build SecurityFatalError/browser blocked.165 remediation candidate exists but is unmerged; this task does not duplicate dependency upgrades or waive gates. Fresh exact-HEAD hosted CI required, expected result must be read rather than assumed.

## Required independent review package

Actual final PR HEAD/TREE/BASE must be read from GitHub, including all5 changed paths. Requested reviewers: Gemini4 Argon(High), Antigravity STRICT READ-ONLY; separate Security/Quality identities and actual sessions/transcripts, fresh separate verdicts, no inherited PASS, no tracked writes. Security: callback authority binding, no implicit public/upload consent, scope/revocation/expiry/revision safety, no payload storage/leak/activation. Quality: actual callable behavior, negative/contract coverage, honest standalone-vs-integrated boundary, reuse of existing primitives, bounded scope.

Antigravity IDE exists, but approved computer-use access failed twice including reset (sandbox/helper error and Node process exit); no dispatch/model/session verified. **BLOCKED_REVIEW**, not PASS. MCP server task/lease unavailable: BLOCKED BY TOOL CAPABILITY/NOT_VERIFIED, no invented state. No merges or Ready transitions until actual reviews/CI/security and applicable Human/platform gates pass.168 remains separate Owner decision. Historical165 AUTHORIZATION_PROVENANCE_NOT_VERIFIED is untouched.

## Next action and Section20 handoff

Review this candidate on immutable final SHA; accept existing security remediation/dependency gates and handle status-document conflicts with167 by preserving both dated records only through authorized integration. No code depends on an unaccepted branch. Next business consumer P0-PRIOR/manual evidence and website egress integration requires accepted contracts; do not stack an expanding runtime workflow on unreviewed consent. Keep draft-export auth/revision/integrity/confidentiality gates; Claims OFF and API budget0.

```text
Task ID: P0-CONF
Agent: Codex
Reviewer: Security AND Quality, Gemini4 Argon(High) requested; execution unavailable
Status: IMPLEMENTED_CANDIDATE /INTEGRATION_PENDING /BLOCKED_REVIEW
Version: 0.1.1
Work completed: callable offline classification/grant/check/revoke, immutable scoped receipts, fail-closed tests
Files affected: confidentiality.py, test_confidentiality.py, P0-CONF.md, README.md, Control Center
Evidence checked: existing digest/snapshot/tripwire contracts, new functional tests, actual PR CI in receipt
Findings: existing next audit/build blocker; integration not yet wired; volatile storage is not durable audit
Decisions: existing V1 scope only, no168 activation/paid/Claims/egress/deployment
Issues: genuine independent reviews/tool access, required CI/security and applicable integration gates pending
Security impact: additive offline helper only; existing provider callsites unchanged and not newly protected
Recommended next action: exact-final-HEAD independent reviews, accepted security remediation, then separately scoped consumer integration
```

Changelog: new0.1.0,22/11/2026,Codex,actual Owner P0.1 continuation; additive offline module, no existing API/schema/policy breaking change.

0.1.0→0.1.1,22/11/2026,Codex: self-check callback reentrancy capacity edge fixed by post-authorization capacity recheck; added regression, final local89PASS/0FAIL/0SKIP. Prior45c9799/88PASS preserved as superseded history; no independent verdict inferred. Breaking changeNo.
