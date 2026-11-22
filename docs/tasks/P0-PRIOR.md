# P0-PRIOR — Controlled Manual Prior Art Evidence Workflow

| Field | Value |
|---|---|
| Version / date |0.1.0 /22/11/2026 Asia/Saigon |
| Owner / implementer | Nguyễn Song Hào Kiệt — Independent Developer /Codex |
| Authority | Actual Human CONTINUE INTEGRATION & P0 BUSINESS DEVELOPMENT, Priority C, current22/11/2026 conversation; no fabricated receipt/retrospective approval |
| Workflow / status | New task-specific authorized V1 scope; no V2 history/enrollment/lease asserted; IMPLEMENTED_CANDIDATE /OFFLINE_VERIFIED /INTEGRATION_PENDING /BLOCKED_REVIEW, not Completed |
| Base / branch | main6bb947c1cf67bcfb3ffc935b3a3fafcafb87f0af /feature/p0-prior-manual-evidence-20261122 |
| Business objective | A specialist records per-paper manual search evidence, decides stop/continue with incomplete-search warnings, preserves auditable source binding |
| Budget / activation | USD0; no search engine, provider calls, external fetching, Claims activation or deployment |
| Dependencies | Existing DocumentStorage/DocumentRegistry/upload validation/hash helper, bounded immutable review snapshots/canonical JSON. No import of unmerged169 or168 policy |
| Scope / risk | One native offline workflow plus unit/integration/security tests; HIGH data/provenance/decision risk; separate exact-HEAD Security AND Quality required |

## Minimum data contract, fixed before implementation

Native immutable references: opaque reference ID, PATENT/NON_PATENT kind, citation, source, ISO retrieval date, optional HTTPS URL, relevant passage/similarities/differences. All free text bounded; URLs validated but never fetched; entered citations remain USER_RECORDED_NOT_VERIFIED. Retrieval date is the user's reported date, not independently verified evidence.

Manual search record: search scope, limitations, optional search terms, INCOMPLETE or MANUAL_SEARCH_RECORDED, tuple of references. INCOMPLETE may have no references but needs explicit scope/limits; recorded search needs references. No novelty/patentability/exhaustiveness conclusion is generated.

Workflow derives paper SHA256 from actual registered upload bytes under existing storage lease, never accepts a caller-asserted source hash. Dossier revision is maintained by this service (not a global draft/analysis revision). All updates/decisions require expected dossier revision and a trusted-host authorization callback bound to actor/context/owner/source/revision/dossier digest/action/reason. Wrong owner, stale revision, changed/missing/expired original or missing authority fails closed.

State: no record → explicit manual record → Human STOP or CONTINUE; any content revision invalidates continuation. Incomplete CONTINUE is allowed with mandatory `Prior Art Search Incomplete` warning. Even recorded coverage remains non-exhaustive/unverified. Assessment is metadata, not a bearer token, legal acceptance or activation of existing drafting routes.

Audit: immutable ordered actor/context/action/reason/actual UTC timestamp/source/dossier digests with chained hashes, bounded process-local history and snapshots. Hashes establish internal consistency, not authenticated Human identity. No extra paper storage, durable-case DB or retention-policy change; original source TTL remains effective. Future durable history belongs to P1-CASE.

## Acceptance / verification

1. Existing actual PDF/DOCX upload → manual record → explicit incomplete continuation/stop → source/revision-bound assessment under no-provider tripwire.
2. Citation/date/URL/type/size/duplicate-ID validation; no URL opening, DNS or SDK use.
3. Source tamper/expiry/removal/foreign-owner/stale update and stale continuation rejected.
4. Callback errors/reentrancy and capacity/clock failures deny without leaking input. Returned snapshots cannot mutate stored evidence.
5. Updates invalidate decisions; last actual Human decision determines the current revision's continuation. Warned drafts remain subject to other auth/integrity/confidentiality gates.
6. No dependency/fixture/gold/CI/security-threshold/provider-route/Claims changes. Existing architecture reused; browser/provider consumer integration remains separately gated.

Reviewer package after final commit includes exact BASE/HEAD/TREE/diff/tests/log hashes/risk assessment, actual Gemini4 Argon(High) separate Security/Quality sessions, STRICT READ-ONLY. Current Antigravity UI runtime failed twice after reset; BLOCKED_REVIEW unless actual access/reports become available. No fabricated PASS.165 historical AUTHORIZATION_PROVENANCE_NOT_VERIFIED and168 NOT_EFFECTIVE preserved.

Changelog new0.1.0,22/11/2026,Codex: minimum scoped contract/acceptance recorded before implementation; additive native workflow, no existing API/policy breaking change.

## Executed evidence and current boundary

Actual local final tests: **84PASS/0FAIL/0SKIP**,4.87s:51 new prior-art cases +26 existing parser +7 provider-tripwire regressions;1 existing deprecation warning. Existing synthetic PDF/DOCX bytes were uploaded through actual /api/documents, then manual dossiers/decisions checked against registry SHA and leased bytes. No live provider, DNS or URL fetch. Original51 cases include scopes/limits/citations, missing/stale/foreign input, source tamper/delete/TTL, audit mutation, callback/source/capacity reentrancy, bad clock and no-authority failures.

P0-CONF169 remains a separate unmerged candidate and was reverified89PASS, not connected here. No provider/drafting/browser route integration is claimed. Native assessment is explanatory metadata and is not accepted as an authorization token. Date validation uses valid ISO calendar dates no later than the trusted UTC clock date; dates remain user-recorded evidence.

Security integration probe: all49 canonical frontend Git blobs equal165HEAD4186b7a in a disposable169-based checkout (Git clean filters account for Windows CRLF). Full/prod audit0, tree exit0, security135PASS, lint/typecheck/build PASS, browser81PASS. This is counterfactual self-verification, not a merged implementation, canonical dependent CI or independent review. The actual current-main graph remains vulnerable until legitimate165 integration. No dependency workaround introduced.

## Section20 handoff

```text
Task ID: P0-PRIOR
Agent: Codex
Reviewer: actual Gemini4 Argon(High) Security AND Quality requested; NOT_RUN
Status: IMPLEMENTED_CANDIDATE /OFFLINE_VERIFIED /INTEGRATION_PENDING /BLOCKED_REVIEW
Version: task0.1.0 /native data contract1.0.0
Work completed: existing upload-to-manual evidence-to-explicit STOP/CONTINUE native workflow, immutable source-bound audit and warnings
Files affected: manual_prior_art.py, test_manual_prior_art.py, P0-PRIOR.md, README.md, Control Center
Evidence checked: main6bb947c, actual registered synthetic PDF/DOCX,84 local tests, source/clock/authority/audit negatives
Findings: main Next audit blocker; reviewer runtime unavailable; browser/provider integration and durable-case audit not implemented
Decisions: standalone authorized V1 task; no unaccepted code/policy dependency; no168 activation or retrospective165 authorization
Issues: required exact-final-HEAD hosted CI/security/reviews and applicable integration gates remain
Security impact: manual input only; no fetching/provider/Claims/real paper/deployment; original source TTL preserved
Recommended next action: genuine final-SHA Security/Quality reviews; legitimate165 acceptance/integration; separately gated consumer wiring
```
