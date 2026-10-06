# GOV-AGENT-001-B2 — MCP tools and state logic

Package version: **0.2.0** (from 0.1.0; additive functionality, no V1 breaking change).
Schema version: **3** (from 2; additive review-attempt/checkpoint metadata only).
Date: 2026-10-06. Implementer: Codex. Independent implementation review: **PENDING**.
Status: implementation handoff; no task closure or independent PASS is claimed.

Authorized B2 base / B1 PR #85 merge: `4e8e51b178f0f112c637b64f1472b3506ad455ba`.
B1 main CI: `37468063560`, completed / SUCCESS, push / main / exact merge SHA.
Reviewed B1 implementation: `1002cefc80c29ca7986fe5a1179dc50eac2719b1`.
Human supplied B1 independent review disposition: PASS / findings NONE / ready
for merge under current governance; no GitHub-native approval is inferred.

Authoritative specification: GOV-AGENT-001 **0.2.1**, byte-identical to reviewed
commit `130bc53831fef414df6cd9edf41089b2a600d00c`.
Human authorization: attached “GOV-AGENT-001 — Continue Full Workflow V2”,
current actions limited to B1 merge and B2 implementation/PR/review handoff.

## Persistence and tool behavior

- Explicit admin enrollment only; no historical V1 backfill or real-task enrollment.
- Assignments use deterministic per-role versions and expected-assignment replacement.
  Authorization/actor references are durably recorded in existing progress evidence.
  Replacement cannot take over a live implementation lease.
- Planner submits DRAFT/READY spec identities. Human/admin freeze consumes a terminal,
  non-revoked recorded Human-authorization row for the exact artifact/version/SHA.
  `metadata_json` must carry `human_authorized=true`, `committed_artifact_exists=true`,
  `spec_sha`, `spec_version`, `artifact_path`; source and reference must be supplied.
  These assertions are recorded claims, not external identity/Git verification.
- Freeze/supersession is transactional and uses `expected_frozen_spec_id`. Old specs
  and evidence remain history. A new spec releases the old execution lease and requires
  a new implementation start; the candidate pointer remains until an explicit transition.
- Implementer-only start mirrors assignment/task leases atomically and preserves
  legacy dependency, branch/worktree, freeze/blocker and quota protections.
- F-07 candidate recording implements NULL→B and A→B CAS inside BEGIN IMMEDIATE.
  Winning retries reuse matching immutable fields even with original expected A.
  Stale non-current targets fail and roll back their insertion. Reads use only the pointer.
- CI is immutable per task/reference; identical payload retries reuse it. Unknown task
  candidates fail; historical candidate observations are retained and marked stale.
- Durable `review_attempts.id` is the token returned by `review.start` and supplied as
  `review.submit.review_id`. The submitted result has its separate immutable
  `reviews.review_id`; use that result ID for verification subjects.
- Review type/assignment/author independence and exact current spec/base/candidate are
  checked at start and first submit. Duplicate identical submitted evidence returns the
  existing result, even if now historical; it does not create fresh applicable evidence.
  Tracked edits or blocking findings reject PASS. Re-review creates a new attempt.
  Security and Quality require separate agent/session IDs, though models may match.
- Admin verification recording validates typed same-task subjects, exact expected
  terminal record, next version, immediate supersession and provenance. REVOKE must
  be UNVERIFIED. There is no implicit promotion. External keys canonicalize repository
  casing: `owner/repo#PR@head_sha`, `owner/repo@merge_sha`. Authorization keys retain
  the supplied immutable authorization reference.
- Get-state/review views expose exact pointer and spec/assignment/candidate staleness,
  plus all verification records and applicability. External-subject applicability remains
  unevaluated. No authoritative effective-policy or merge readiness field is returned.
- Role checkpoints live in an additive side table. Historical checkpoints are untouched.
  Reviewer/Planner checkpoints do not acquire the implementation branch or lease.
  Only Implementer may use the legacy task-blocking handoff with V2 assignment metadata.

## Trust and phase limits

Identity, artifact existence, Human decisions, Git/CI/review truth and verifier provenance
remain trust-based supplied metadata. Recorded VERIFIED rows are never an authority
claim; views label `authority_validated=false`. No B3 merge computation/adapters,
role packages, skills, governance activation, pilot, AI-CONV, provider/API, deployment
or application changes are included. Budget/quota behavior is unchanged.

All MCP tests use isolated synthetic temporary databases. The connected MCP reports
`Unknown task: GOV-AGENT-001-B2`; no operational lease/enrollment is invented.
The repository CI currently runs application regression, not this MCP package;
local MCP command evidence is separate and must be checked during fixed-SHA review.

## Validation

Required commands: `npm run typecheck`, `npm test`, `npm run build`, `git diff --check`.
Preserved regression: 34 original V1/B1 cases. Added B2 cases are listed below.
Final local results: typecheck PASS; tests **71 pass / 0 fail / 0 skipped**;
build PASS; diff check PASS. The 37 added cases comprise 36 state/migration tests
and one real stdio/admin flow. No dependency was added or upgraded.

### Added state tests (36)

- explicit prospective enrollment is idempotent; conflicting enrollment and historical V1 backfill are rejected
- non-enrolled V1 tasks keep legacy operations, owner and state shape with additive version marker
- all four role identities and deterministic assignment history survive restart
- assignment retry is idempotent and conflicting authority reference is rejected
- concurrent incompatible role assignment produces precisely one winner
- spec DRAFT to READY is Planner-scoped, collision-safe and durable
- Human freeze requires exact artifact/version/SHA evidence and rejects Planner self-authorization
- freeze/supersession is atomic; old candidate/history cannot silently retarget the new spec
- implementation start rejects missing frozen spec and reviewers, protects collisions and main, retries idempotently
- V2 legacy renew/report/release/expiry paths preserve atomic assignment mirror and frozen-spec start requirements
- F-07 first candidate and A to B CAS retry remain immutable and restart-safe
- F-07 stale non-current transition rolls back inserted loser and leaves winning pointer intact
- F-07 concurrent A to B and A to C admits exactly one durable winner
- F-07 state resolves solely from pointer even when a higher ID/timestamp exists
- CI references retry idempotently, reject conflicting payload, and retain stale SHA history
- Security/Quality start are independent, type-safe and idempotent with durable pending state
- Implementer cannot review own candidate under a different reviewer role, even after lease release
- review submission validates attribution, blocked findings and tracked modifications; PASS is immutable
- candidate change stales old PASS/CI, prevents stale in-flight submit, preserves history after restart
- review BLOCKED and REQUEST_CHANGES are stored separately and cannot authorize merge lifecycle
- superseding reviewer assignment invalidates in-flight submission and historical PASS applicability
- verification append/revoke/re-attest is sequential, exact-current and restart-safe
- concurrent verification writers cannot fork or skip a version
- VERIFIED is provenance-validated only; no caller-requested implicit promotion or authority claim
- typed verification subjects validate same-task IDs, review type and canonical external keys
- V2 role checkpoints and Implementer handoff work at quota threshold, with legacy history unchanged
- V2 task state exposes precise assignments/spec/candidate/staleness without activating project governance
- B1 database with persisted spec/candidate/evidence upgrades additively to B2 and remains restart-safe
- Security and Quality cannot share role/session identity or consume each other as independent verdict
- a replaced Planner identity cannot self-authorize a freeze
- verification rejects cross-task subject links and cross-task supersession IDs
- canonical repository subject keys prevent casing aliases from forking verification identity
- a new frozen spec makes selected candidate, reviews and verification applicability stale without rewriting rows
- incompatible B2 migration rolls back version bookkeeping and preserves B1 data without reset
- version-3 metadata with incompatible attempt schema fails closed and preserves existing candidate
- verification recording detects a tampered/gapped chain and refuses further appends

### Added stdio/admin integration test (1)

- real stdio B2 tools and isolated admin enrollment/verification execute a complete recorded-evidence flow
