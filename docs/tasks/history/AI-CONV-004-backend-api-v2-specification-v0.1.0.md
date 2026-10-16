# AI-CONV-004 — Backend API v2 specification (PROPOSED)

| Field | Value |
|---|---|
| Task | AI-CONV-004 |
| Document version | 0.1.0 — PROPOSED / NOT FROZEN |
| Document date | 2026-10-16 (Asia/Ho_Chi_Minh) |
| Status | SPECIFICATION CANDIDATE — INDEPENDENT REVIEW / HUMAN API POLICY DECISIONS PENDING |
| Tracking issue | [#121](https://github.com/nshaokiet/ai-ip-description-generator/issues/121) |
| Human authorization | `HUMAN-AI-CONV-004-BACKEND-V2-SPEC-PREPARATION-2026-10-16`, chat-origin approval **for documentation only** |
| Workflow | Workflow V1; Codex prepares candidate, Gemini 3.8 Flash High / Antigravity STRICT READ-ONLY independently reviews final SHA |
| Baseline | `main` at `ddc92f9a2d321e3e8507619276a200d35e7de696` (PR #120 merge) |
| Parent contracts | AI-CONV-001 v0.1.1; AI-CONV-002 internal orchestration v1.0.1; AI-CONV-003 synthetic authority overlay v1.0.0; released P2-002…P2-006 |
| Breaking change | No — design documentation only; no released v1 contract changes |
| Runtime, data, budget | No endpoint implementation, no provider calls, no real/confidential source, no production, no Render deployment, no Workflow V2 / Phase H activation |

## 1. Purpose and authorization boundary

This document proposes, but **does not approve or implement**, a possible Backend API v2 for inspection of already validated source-grounded USPTO-v2 offline artifacts, session/revision status and Human-review needs.

The Human explicitly authorized **preparing this specification only** on 2026-10-16, separately from a **conditional** AI-CONV-003 closeout. This authorization does not select an external API surface, architecture, identity policy, storage/persistence strategy, public Claims behavior, provider, deployment target or data-use policy. All substantive decisions in §10 remain **PENDING HUMAN**.

**Stop condition:** A reviewed docs PR or green CI is not approval to add an HTTP route, change a schema, wire AI-CONV-003 authority into Claims, migrate P2-005/P2-006, or send a paper to an AI provider. Any such work requires a separate explicit Human decision and later implementation authorization.

## 2. Verified as-is system (source, not proposal)

### 2.1 Existing HTTP boundary

At the baseline SHA:

| Current source | Existing behavior | Availability |
|---|---|---|
| `backend/app/api/routes/health.py` | `GET /health` → `{"status":"ok"}` | Included unconditionally in `create_app` |
| `backend/app/api/routes/documents.py` | `POST /api/documents`, strict single multipart `file` upload, HTTP 201, document identity and validation metadata | Included unconditionally |
| `backend/app/api/routes/local_orchestration.py` | `GET /api/documents/{document_id}` → document metadata | Included **only when** `Settings.enable_local_orchestration_api` is true |
| Same file | `POST /api/documents/{document_id}/process` → existing **v1** `analysis`, `draft`, `metadata` | Same feature-flag gate; not USPTO v2 |
| Same file | `POST /api/drafts/validate` → canonical v1 draft validation result | Same feature-flag gate |
| Same file | `POST /api/exports/docx` → v1 patent-draft DOCX | Same feature-flag gate |

The existing API route prefix is `/api` for document and local-orchestration routers. The environment flag `AI_IP_ENABLE_LOCAL_ORCHESTRATION_API` defaults to **false** (`backend/app/core/config.py`, `backend/app/main.py`). Local API request models reject undeclared fields through Pydantic `extra="forbid"`. `POST /api/documents` and `GET /health` alone do not establish USPTO-v2 processing or production readiness.

Do not rename existing routes as `/api/v2` or assume external availability merely from their presence in the repository. `backend/app/main.py` currently constructs a v1 core pipeline when the local-orchestration flag is enabled, not the AI-CONV-002 offline USPTO orchestrator.

### 2.2 Existing internal/offline boundary

- AI-CONV-002 `backend/app/services/uspto_offline_orchestration.py` is an **internal in-memory, source-bound, deterministic** orchestrator. Its contract is `ORCHESTRATION_CONTRACT_VERSION="1.0.1"`; it intentionally exposes **no HTTP route**, provider, network/database or persistent store.
- The released P2-002 → P2-003 → P2-004 → P2-005 (+ optional P2-006) path has strict staged source/session/revision and provenance validation. The seven original P2-005/P2-006 input identities are, in canonical order:
  1. `source_envelope`
  2. `structured_analysis`
  3. `reconstruction`
  4. `specification`
  5. `p2_003_generation_config`
  6. `supported_claims`
  7. `p2_004_generation_config`
- These are enforced by `validate_assembly_inputs` and mirrored by the `PROVENANCE_KEYS` in `uspto_offline_orchestration.py`; an enriched `reconstruction`, injected overlay, altered digest or eighth hidden argument is **not** equivalent to these original validated projections.
- AI-CONV-003 is an **additive synthetic/offline authority overlay**. Source-linked solution membership and scoped ESSENTIAL assertions may permit **SYSTEM/APPARATUS eligibility for further unchanged P2-004 checks**, but this is **not** approval to emit real-paper positive Claims. METHOD/PROCESS and COMPOSITION positive authority remain disabled.
- The authentic-style synthetic APP-002 chain validly yields `HUMAN_CONFIRMATION_REQUIRED` with `claims=[]`; P2-003 retains `claims_runtime_implemented=false`. This is expected **fail-closed**, not an error or unsupported promise.
- The published frontend/v1 routes and existing PDF/DOCX render contracts are unchanged. Neither AI-CONV-002 nor AI-CONV-003 is wired into public v1 FastAPI routes.

Canonical references: `docs/tasks/AI-CONV-001-source-grounded-uspto-v2-orchestration.md`, `docs/tasks/AI-CONV-002-offline-orchestration-implementation.md`, `docs/tasks/AI-CONV-003-claims-semantic-authority-specification.md`, `backend/app/services/uspto_document_package_validation.py` and `backend/app/services/uspto_offline_orchestration.py`.

## 3. Design alternatives (not Human-selected)

| Candidate | Proposed exposure | Benefit | Blockers / recommendation |
|---|---|---|---|
| **A — Status/read-only first** | Local-only, separately gated inspection of synthetic session status, revision and safe evidence/reference metadata, explicitly omitting raw source or substantive Claims | Smallest trust boundary; allows client workflow planning without pretending positive Claims | Must still decide session access and non-authenticated local threat model; **recommended for initial detailed contract exploration only**, not adopted |
| **B — Bounded synthetic review workflow** | Candidate POST create/advance revision and synthetic review decision endpoints, only under a new offline opt-in | Models Human review lifecycle and rejection semantics | Requires identity, authorization, persistence, CSRF/cross-session and audit decisions; synthetic actor is not authenticated; **do not implement until Human selects safeguards** |
| **C — Product Claims/export API** | Public positive Claims, document package/PDF/DOCX export, real Human approvals and real-paper processing | Product-value target | **DEFERRED / NOT AUTHORIZED**: new authority, versioned projection migration, real auth, data/privacy and production/provider approvals required |

**Tentative sequence for review:** define Candidate A's schema and negative tests first, record deferred Candidate B in the same design appendix, and explicitly exclude Candidate C. This recommendation is **not** a Human architecture decision.

## 4. Candidate API surface (ALL NOT IMPLEMENTED)

The `/api/v2` namespace is a **design placeholder**; prefix choice, exposure and authentication must be decided before release. Paths below are illustrative signatures, **not existing routes**, not permission to create them.

| Candidate endpoint | Proposed purpose | Proposed boundary |
|---|---|---|
| `GET /api/v2/sessions/{session_id}/status` | Return a non-sensitive synthetic session state, revision and review-required marker | Local-only, feature-disabled by default; ownership/authorization decision pending |
| `GET /api/v2/sessions/{session_id}/revisions/{revision}/evidence-index` | Return bounded evidence IDs/digests and safe source locator metadata | No arbitrary source prose/path leakage; reject stale/cross-session revision |
| `GET /api/v2/sessions/{session_id}/package-status` | Return `PACKAGE_VALID` / `CLAIMS_REVIEW_REQUIRED` style status, not a filing-ready representation | Never re-label `claims=[]` as a failure or invent positive eligibility |
| `POST /api/v2/sessions` | **Deferred B:** create synthetic session from already validated, source-bound objects | Not safe without scoped session, identity, storage and replay policy |
| `POST /api/v2/sessions/{session_id}/review-decisions` | **Deferred B:** submit scoped synthetic decision/supersession/revocation record | Not a real Human approval, must be disabled pending authn/authz and policy |
| `GET /api/v2/sessions/{session_id}/exports/{format}` | **Deferred C:** retrieve verified USPTO v2 artifact | Requires separate renderer, export authority and data-retention security decision |

No `POST` in this table is approved for implementation. No enabled endpoint may report successful Human approval purely from a boolean, checkbox, caller-supplied actor ID or public hash.

## 5. Candidate representation and validation rules

All types below are **proposed** versioned design objects; they have no released schema, server route, or frontend binding yet.

### 5.1 Example read-only response shape (illustrative; not contract)

```json
{
  "api_version": "2.0.0-proposal",
  "session_id": "synthetic-session-id",
  "revision": 1,
  "revision_token": "opaque-synthetic-revision-token",
  "stage": "CLAIMS_REVIEW_REQUIRED",
  "claims": {
    "status": "HUMAN_CONFIRMATION_REQUIRED",
    "count": 0,
    "product_runtime_enabled": false
  },
  "source_identity": {
    "document_id": "synthetic-document-id",
    "source_sha256": "synthetic-source-digest"
  },
  "review_required": true,
  "correlation_id": "synthetic-correlation-id"
}
```

**Illustrative only:** field names, string formats, token visibility, revision lifetime and exposure of digests/IDs are not approved. In an actual design, a token may need to be omitted from a GET result and handled as a server-side capability, depending on authentication/session policy. Do not promote the sample to an accepted wire schema.

### 5.2 Mandatory candidate invariants

- **Identity and scope:** Each request resolves a verified document, source SHA-256, exact session, revision and token; compare against retained trusted server state, not merely caller claims. Evidence references must be valid for the exact source and structural target.
- **Versioning:** Validate explicit API/schema versions and reject unknown/mixed versions. Do not silently coerce arbitrary `dict`, extra fields, unsupported families or enum values to authoritative states.
- **Stale/tamper fail-closed:** Invalid or stale session/revision/token, source/config/reconstruction digest mismatch, cross-document evidence or signature mismatch must never return positive authority. Cross-session replay and conflicts must have deterministic rejection.
- **Nonpromotion:** `UNKNOWN`, `OPTIONAL`, `CONDITIONAL`, inferred membership, missing evidence and client-submitted `confirmed=true` must not become `ESSENTIAL` or an eligible Claim. Revocation/supersession must invalidate any cached eligibility.
- **Read-only semantics:** A GET for status/evidence must not start a model run, advance a revision, render documents, authorize Claims or mutate authority/audit state. Existing cleanup semantics cannot be weakened.
- **Released-contract compatibility:** AI-CONV-002 and P2-005/P2-006 validation remains the source of truth; the seven-input projector stays exact. A hypothetical v2 authority-bearing projection requires a later **separately approved migration contract**, not an injected property.
- **Fail-closed output:** `CLAIMS_REVIEW_REQUIRED` and `HUMAN_CONFIRMATION_REQUIRED` + zero Claims are legitimate non-error outcomes. Preserve draft-only, non-filing and non-legal-advice notices; do not advertise issued USPTO B2 status.

## 6. Errors, revisions, concurrency and idempotency (proposal)

A public API error contract is **not yet decided**. A candidate must preserve existing v1 error behavior and propose separate versioned v2 codes. Possible semantic mappings requiring review: malformed/unknown field → 400/422; unauthorized/forbidden → 401/403 **only after an authentication policy exists**; document/session not found → 404 or privacy-preserving uniform 404; stale revision/conflict → 409; source/provenance contract invalid → 422; unavailable/disabled capability → 403/404/409 as determined by Human API policy. Exact wire status, name and error envelope are **PENDING**.

Proposed error envelope should contain only an allowlisted code, static safe message, correlation ID and bounded public field references; no source excerpt, credentials, filesystem paths, document titles, arbitrary attacker-supplied field names, secret tokens or stack traces.

A future mutation contract (Candidate B) would require optimistic revision preconditions and canonical request/decision digests, idempotency for retries, strict decision ordering, explicit supersession/revocation, immutable audit history and safe concurrent state transitions. It must not claim durable storage, atomic filesystem rollback or real Human authentication from the existing in-memory synthetic system.

## 7. Authentication, authorization, storage and data handling — unresolved

Current synthetic actor `SYNTHETIC_REVIEWER_001` is a test-only identity convention, **not an authenticated user, role-based access control or legal attestation**. Any externally accessible v2 endpoint needs separate choices about:
- Who may create/list/read a document/session, and how ownership is proved; default-deny in the absence of an approved mechanism.
- Who can inspect source/evidence vs submit/revoke Human decisions; user/tenant/resource ACL, audit and revocation.
- Where session/revision/decision state lives; retention, deletion, backups, concurrency, privacy and data classification.
- Local-only vs internal network vs public ingress, rate limits, abuse prevention, CORS/CSRF, authentication/session fixation.
- Secret/HMAC key custody and rotation, server-side canonical snapshots and source protection.
- Whether source data may ever include real or confidential papers and whether any AI provider is authorized (both currently **NO**).
- Whether any runtime/budget or deployment change is permitted (currently **NO**).

A feature flag by itself is not authentication/authorization. No public route or real-user workflow may be inferred from a synthetic test actor.

## 8. Backward compatibility and migration strategy

1. **No v1 behavior changed by this specification.** Existing `GET /health`, `POST /api/documents`, and feature-flagged `/api/documents/{id}`, `/api/documents/{id}/process`, `/api/drafts/validate`, `/api/exports/docx` remain exactly as released.
2. Proposed `/api/v2` is additive and **not currently registered**. No alias, hidden parameter, auto-upgrade or automatic fallback from v1 to v2.
3. Internal AI-CONV-002 session snapshots, P2-002 reconstruction and P2-003 specification remain immutable and source-bound. P2-004 standalone eligible Claims do not authorize v2 positive Claims output.
4. P2-005/P2-006 keep the **seven original** argument identities and projections. Do not pass an enriched reconstruction or overlay in their place; test byte-level and signature-level compatibility before considering separately approved migration.
5. Proposed versioned migration sequence (future Human choice only): inventory source data → choose trusted authority representation and access policy → define additive versioned projection with original source-bound evidence → independent threat/compatibility review → synthetic positive/negative fixtures → new contract-specific implementation authorization → CI / regression / safe release gate.
6. A future v2 implementation should not affect existing product runtime or deployed Render services unless separately authorized.

## 9. Proposed verification and acceptance matrix

The following are **tests to design**, not tests already implemented.

| ID | Proposed acceptance | Required negative tests |
|---|---|---|
| AC-01 | Actual v1 routes and feature-flag behavior explicitly inventoried | v2 route must be absent from deployed/current API |
| AC-02 | Candidate v2 read-only models versioned and strict | Unknown fields/enum/version, oversized values, malformed IDs |
| AC-03 | Exact source/session/revision/token scoping | Cross-document/session replay; stale revision; changed source/reconstruction/config digest |
| AC-04 | Evidence index never fabricates source membership | Foreign evidence, missing target, digest-only identity, inferred proximity |
| AC-05 | Zero Claims is valid `HUMAN_CONFIRMATION_REQUIRED` status | Auto-convert review-required into SUCCESS/eligible; filler Claims |
| AC-06 | Human review is fail-closed and explicitly scoped | Boolean approval, forged actor, reused decision, revoked/superseded cache, changed evidence |
| AC-07 | METHOD/PROCESS/COMPOSITION remain disabled | Config/field tampering to enable positive authority |
| AC-08 | P2-005/006 exact seven-input provenance unchanged | Hidden eighth input, substituted enriched reconstruction, altered released validator/signature |
| AC-09 | No authority leakage via safe errors/responses/logs | Raw source excerpts, personal paths, token leakage, disallowed error metadata |
| AC-10 | No v1 breaking behavior | Existing upload/process/validate/export regression, health, default feature-off behavior |
| AC-11 | No unauthorized execution | Provider network calls, external paper uploads, uncontrolled rendering, public routes, db writes |
| AC-12 | Version/rollout policy explicitly approved before implementation | No flag-only bypass of auth/data/deploy restrictions |

Evidence gates for a **future** implementation: targeted offline tests, full relevant P2-002…P2-006 + AI-CONV-002/003 regression, security/negative coverage, supported schema validation, source/contract hashes, baseline v1 API regression, independent fixed-SHA reviewer PASS, exact-head CI SUCCESS, Render OFF/no verify, and protected merge with exact-main postmerge CI. These are not acceptance evidence for currently non-existent v2 code.

## 10. Explicit Human decisions required before freezing or implementing

| Gate | Decision | Current status |
|---|---|---|
| HD-V2-01 | Adopt Candidate A, B or another scope; which operations may ever be externally reachable? | **PENDING HUMAN** |
| HD-V2-02 | Approve or reject `/api/v2` path, request/response/error-version contract and semantic statuses | **PENDING HUMAN** |
| HD-V2-03 | Choose real authn/authz, document/session ownership and Human decision role; whether local-only unauthenticated synthetic inspection is ever acceptable | **PENDING HUMAN** |
| HD-V2-04 | Decide in-memory vs durable persistence, retention and concurrency/idempotency guarantees | **PENDING HUMAN** |
| HD-V2-05 | Decide whether evidence metadata/source excerpts may be exposed and to whom; privacy classification | **PENDING HUMAN** |
| HD-V2-06 | Decide Claims runtime and versioned upstream reconstruction/provenance migration **separately**; preserve positive disabled default | **PENDING HUMAN** |
| HD-V2-07 | Decide output formats, approval/audit lifecycle, public vs local operation and rollout/rollback | **PENDING HUMAN** |
| HD-V2-08 | Any provider API/data/funding/deployment/production security authorization | **NOT AUTHORIZED** |
| HD-V2-09 | Freeze exact specification and authorize a separately scoped implementation task | **PENDING HUMAN** |

Do not interpret approval of **this documentation task** as decisions HD-V2-01…09. Document unanswered gates as blockers rather than silently choosing defaults.

## 11. Workflow V1 review, merge and next-task gates

**Specification-only deliverable:** this one Markdown file on a separate branch/PR, with explicit PROPOSED status. Documentation may clarify current task references if separately approved, but it must not alter code, tests, schemas, dependencies, FastAPI routing or public contracts.

- Codex/ChatGPT source audit must include actual route prefixes, opt-in feature flag, AI-CONV-001/002/003 and released P2-002…006. Never claim v2 exists.
- Independent **Gemini 3.8 Flash High / Antigravity STRICT READ-ONLY** must inspect exact reviewed SHA, source/line accuracy, unsupported claims, positive/negative ACs, migration, threat model, Human decisions and scope. Report actual model/profile, session/reuse and PASS / REQUEST CHANGES / BLOCKED.
- Before any docs PR merge: require exact-head CI SUCCESS, accurate diff scope, fresh main/head protection and Render `no/off`; resolve review findings and obtain Human policy/freeze decision if a merge would be represented as an **approved/frozen v2 design**. A purely proposed artifact must remain explicitly **PROPOSED** if merged only as a proposal.
- After merge, verify exact-main CI, doc lineage and issue status. Later v2 implementation remains STOP until **separate Human implementation authorization** on approved policy/contracts.
- AI-CONV-003 closeout, AI-CONV-002/#111, GOV-REVIEWER-001/#113, BLK-003, EVAL-001 product runtime, V2/Phase H and provider/production decisions remain independent; do not turn one into another's approval.

**Disposition as of 2026-10-16:** specification candidate only. AI-CONV-004 implementation **NOT STARTED**, candidate endpoints **NOT IMPLEMENTED**, Claims runtime **NOT ENABLED** and Human API-v2 architecture decisions **PENDING**.
