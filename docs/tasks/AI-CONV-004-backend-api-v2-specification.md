# AI-CONV-004 — Backend API v2 specification (Candidate A policy approved; contract PROPOSED)

| Field | Value |
|---|---|
| Task | AI-CONV-004 |
| Document version | 0.1.1 — HUMAN-APPROVED CANDIDATE A POLICY / WIRE CONTRACT NOT FROZEN |
| Document date | 2026-10-16 (Asia/Ho_Chi_Minh) |
| Status | POLICY-ALIGNED SPECIFICATION CANDIDATE — NEW INDEPENDENT REVIEW / FINAL HUMAN CONTRACT FREEZE PENDING |
| Tracking issue | [#121](https://github.com/nshaokiet/ai-ip-description-generator/issues/121) |
| Human authorization | Specification preparation `HUMAN-AI-CONV-004-BACKEND-V2-SPEC-PREPARATION-2026-10-16`; bounded Candidate A selection `HUMAN-AI-CONV-004-CANDIDATE-A-POLICY-2026-10-16` — [Issue #121 decision](https://github.com/nshaokiet/ai-ip-description-generator/issues/121#issuecomment-6207131354). **Neither authorizes implementation.** |
| Workflow | Workflow V1; Codex prepares candidate, Gemini 3.8 Flash High / Antigravity STRICT READ-ONLY independently reviews final SHA |
| Baseline | `main` at `ddc92f9a2d321e3e8507619276a200d35e7de696` (PR #120 merge) |
| Parent contracts | AI-CONV-001 v0.1.1; AI-CONV-002 internal orchestration v1.0.1; AI-CONV-003 synthetic authority overlay v1.0.0; released P2-002…P2-006 |
| Breaking change | No — Candidate A policy and proposed wire examples only; released v1 and USPTO stages unchanged |
| Runtime, data, budget | No endpoint implementation, no provider calls, no real/confidential source, no production, no Render deployment, no Workflow V2 / Phase H activation |

## 0. Version lineage and limited Human policy approval

| Version | Date | Change | Authorization / status |
|---|---|---|---|
| **0.1.0** | 2026-10-16 | Initial three-option Backend API v2 proposal and HD-V2-01…09 decision packet | [Preserved exact pre-decision artifact](history/AI-CONV-004-backend-api-v2-specification-v0.1.0.md); initial independent [Gemini-attributed specification PASS](https://github.com/nshaokiet/ai-ip-description-generator/pull/122#issuecomment-6207049807), no architecture freeze |
| **0.1.1** | 2026-10-16 | Reconcile explicit Human **Candidate A** limited policy selection; narrow read-only routes, local access/security floor, ephemeral sessions, safe synthetic metadata and test matrix; mark exact contract/freeze as outstanding | [Human decision receipt](https://github.com/nshaokiet/ai-ip-description-generator/issues/121#issuecomment-6207131354); **new fixed-SHA Gemini review and CI required**; no implementation authority |

**Human-selected design direction:** Candidate **A ONLY**, local-loopback, synthetic-only and GET/read-only. Candidate B (review writes, mutations) and C (real-paper/public Claims/exports) remain disabled and require separate explicit authorization. Product Claims stay disabled. Original seven-input P2-005/P2-006 provenance remains intact.

**Approval granularity:** Human approved the bounded policy package, **not** exact paths, JSON schemas, HTTP error mapping, capability/ownership implementation, deployment, an API-contract freeze or any code implementation. The specifications of these remaining choices below are **reviewable recommendations only**. Do not reclassify `PROPOSED` samples as released types or claim a user role/account exists.

## 1. Purpose and authorization boundary

This document proposes, but **does not approve or implement**, a possible Backend API v2 for inspection of already validated source-grounded USPTO-v2 offline artifacts, session/revision status and Human-review needs.

The Human approved specification preparation and then explicitly selected **limited Candidate A as a design-policy direction** (Issue #121 decision above). Loopback-only GET inspection, ephemeral synthetic state, bounded metadata, no Claims activation or migration, and no deployment/provider/data use are the approved constraints. **Exact wire paths/fields/errors, secure ownership/capability bootstrap, integration scope, final contract freeze and separate implementation authorization remain PENDING HUMAN.** Neither decision approved actual API routes or external exposure.

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
| **A — Status/read-only first** | **HUMAN SELECTED POLICY**: loopback-only, default-disabled GET inspection of synthetic session/revision status and bounded IDs/digests, with no source prose, public Claims or mutable review state | Smallest trust boundary; supports strictly synthetic local inspection | **Policy approved; exact wire contract, scoped server-side capability guard and freeze still pending** |
| **B — Bounded synthetic review workflow** | Candidate POST create/advance revision and synthetic review decision endpoints, only under a new offline opt-in | Models Human review lifecycle and rejection semantics | Requires identity, authorization, persistence, CSRF/cross-session and audit decisions; synthetic actor is not authenticated; **do not implement until Human selects safeguards** |
| **C — Product Claims/export API** | Public positive Claims, document package/PDF/DOCX export, real Human approvals and real-paper processing | Product-value target | **DEFERRED / NOT AUTHORIZED**: new authority, versioned projection migration, real auth, data/privacy and production/provider approvals required |

**Human-approved sequence:** refine Candidate A's proposed strict GET schemas and negative tests in v0.1.1, retain Candidate B as deferred and exclude Candidate C. **This does not freeze any wire-level endpoint or authorize implementation.**

## 4. Candidate A API surface (DESIGN POLICY SELECTED; ALL ROUTES NOT IMPLEMENTED)

The additive `/api/v2` namespace is an **approved design direction for specification drafting only**, not an accepted wire contract or registered route. Exact field/path naming, authentication/capability guard and HTTP status conventions are still pending Human freeze. Every path below is **illustrative, NOT IMPLEMENTED**, and conveys no permission to create it.

| Candidate endpoint | Proposed purpose | Proposed boundary |
|---|---|---|
| `GET /api/v2/sessions/{session_id}/status` | **Candidate A policy**: bounded synthetic stage/revision/review-needed status; no original document content | Local-loopback, feature OFF by default, protected by an independently selected server-side scoped ownership/capability guard |
| `GET /api/v2/sessions/{session_id}/revisions/{revision}/evidence-index` | **Candidate A policy**: bounded synthetic evidence IDs/digests only, deterministic sort/pagination to be specified | No raw source/prose, filenames, absolute paths, unbounded locators or secret tokens; reject stale/foreign evidence |
| `GET /api/v2/sessions/{session_id}/package-status` | **Candidate A policy**: status-only, preserving valid no-Claims and Human-review states | Never generate/render/approve a package, expose raw artifacts or re-label zero Claims as failure |
| `POST /api/v2/sessions` | **Deferred B:** create synthetic session from already validated, source-bound objects | Not safe without scoped session, identity, storage and replay policy |
| `POST /api/v2/sessions/{session_id}/review-decisions` | **Deferred B:** submit scoped synthetic decision/supersession/revocation record | Not a real Human approval, must be disabled pending authn/authz and policy |
| `GET /api/v2/sessions/{session_id}/exports/{format}` | **Deferred C:** retrieve verified USPTO v2 artifact | Requires separate renderer, export authority and data-retention security decision |

No `POST` in this table is approved for implementation. No enabled endpoint may report successful Human approval purely from a boolean, checkbox, caller-supplied actor ID or public hash.

### 4.1 Local-only access gate and proposed request/response semantics (NOT FROZEN)

**Human-approved security floor:** A future candidate implementation must remain **disabled by default** under a **separate** opt-in switch (not the existing v1 `AI_IP_ENABLE_LOCAL_ORCHESTRATION_API`), bind exclusively to loopback, deny non-loopback ingress, reject untrusted forwarding/Host/Origin paths, and expose no metadata to an untrusted process. A feature flag or client-claimed loopback address alone is never a proof of session ownership.

**Design proposal requiring later Human contract freeze:**
- A **server-generated, unpredictable, per-session scoped capability** (or a stronger explicitly selected local-session ownership guard) must be checked **server-side for every GET**. Do not mint, disclose, or refresh this authority through an unauthenticated GET, query string, response body, public URL, or synthetic actor ID; bootstrap from a trusted local application flow **out of band**, design still pending.
- The guard must bind at least capability scope, synthetic session ID, document/source identity, revision applicability and expiry. Store only safe keyed/opaque internal representations; compare securely and revoke/expire on cleanup, session change and revision invalidation. Exact token representation/storage/rotation and lifecycle remain **PENDING HUMAN**.
- Reject hostile `Host` headers/DNS rebinding, proxy spoofing (`X-Forwarded-For` cannot establish peer identity), unauthorized CORS/Origin, malformed/oversized identifiers, stale revision and token reuse across sessions. The concrete network peer/proxy trust model and controls are a **reviewable security requirement**, not a feature already present.
- Reads are non-mutating: no model call, subprocess, disk render, package assembly, audit approval, export, implicit session creation, synthetic decision signing or cleanup side effect triggered by client GET. Existing expired sessions may return a safe expired/not-found result without leaking their presence to unauthorized callers.
- Use canonical, deterministic bounded outputs; no traces, absolute paths, source content, filenames, raw HMAC material, capability tokens, private decision seals or other stored secrets. **Only synthetic IDs, stage/status, counts and carefully reviewed digests** may be proposed for disclosure.
- Responses for foreign, nonexistent, expired and unauthorized sessions should avoid enumeration through a uniform safe failure; choose exact `404/403` behavior, status-code matrix and correlation ID exposure only at a separate contract-freeze gate.

**Proposed GET-only v2 transport:** JSON over HTTP on **loopback only**, strict field allowlists with no `additionalProperties`, fixed version and types; a response is not a legal approval or filing-ready Patent B2 assertion. Exact endpoint names/HTTP statuses remain unfrozen. An external or public deployment cannot inherit these assumptions.

### 4.2 Deferred operations and explicit non-goals

Candidate B `POST` operations and Candidate C export/Claims endpoints in §4 are **historical design alternatives only**, not part of selected Candidate A; do not use the table as a build backlog. Candidate A cannot itself accept Human confirmations, change essentiality, sign/revoke decisions or promote P2-004 eligibility. No positive method/composition or real-paper Claims are authorized.

## 5. Candidate representation and validation rules

All types below are **proposed** versioned design objects; they have no released schema, server route, or frontend binding yet.

### 5.1 Example read-only response shape (illustrative; not contract)

```json
{
  "api_version": "2.0.0-proposal",
  "session_id": "synthetic-session-id",
  "revision": 1,
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

**Illustrative only:** field names, enum sets, formats, revision lifetime and safe disclosure of synthetic identifiers/digests are **not frozen**. In particular, the sample **intentionally omits revision/capability tokens**: they must never be returned by a GET as proof of authority. Access-control bootstrap and wire guard are independent design decisions. Real source hashes must not be surfaced simply because they are SHA-256 values. Do not promote this sample to a released schema.

### 5.2 Mandatory candidate invariants

- **Identity and scope:** Each request resolves a verified document, source SHA-256, exact session, revision and token; compare against retained trusted server state, not merely caller claims. Evidence references must be valid for the exact source and structural target.
- **Versioning:** Validate explicit API/schema versions and reject unknown/mixed versions. Do not silently coerce arbitrary `dict`, extra fields, unsupported families or enum values to authoritative states.
- **Stale/tamper fail-closed:** Invalid or stale session/revision/token, source/config/reconstruction digest mismatch, cross-document evidence or signature mismatch must never return positive authority. Cross-session replay and conflicts must have deterministic rejection.
- **Nonpromotion:** `UNKNOWN`, `OPTIONAL`, `CONDITIONAL`, inferred membership, missing evidence and client-submitted `confirmed=true` must not become `ESSENTIAL` or an eligible Claim. Revocation/supersession must invalidate any cached eligibility.
- **Read-only semantics:** A GET for status/evidence must not start a model run, advance a revision, render documents, authorize Claims or mutate authority/audit state. Existing cleanup semantics cannot be weakened.
- **Released-contract compatibility:** AI-CONV-002 and P2-005/P2-006 validation remains the source of truth; the seven-input projector stays exact. A hypothetical v2 authority-bearing projection requires a later **separately approved migration contract**, not an injected property.
- **Fail-closed output:** `CLAIMS_REVIEW_REQUIRED` and `HUMAN_CONFIRMATION_REQUIRED` + zero Claims are legitimate non-error outcomes. Preserve draft-only, non-filing and non-legal-advice notices; do not advertise issued USPTO B2 status.

### 5.3 Candidate field and error profiles — review targets, not approved wire contract

| Proposed field/domain | Candidate constraint | Required rejection / limitation |
|---|---|---|
| `api_version` | One explicitly selected supported version; `2.0.0-proposal` is non-production placeholder | Reject absent, unknown, mixed and downgrade-inconsistent versions |
| `session_id` | Server-generated opaque synthetic identifier, strict max length and syntax | Reject malformed or cross-session identifiers; not an access credential |
| `revision` and `stage` | Nonnegative bounded integer; allowlisted current orchestration enum | Reject stale/future revisions, unknown stages and inconsistent status combinations |
| `claims.status`, `claims.count` | Status-only; `HUMAN_CONFIRMATION_REQUIRED` with `count=0` is valid | Never return actual positive Claims or infer approval from status |
| `source_identity` / evidence-index | Only explicitly allowed synthetic IDs/digests after owner validation | No raw paper text, file names, freeform locators, absolute paths or third-party source metadata |
| `correlation_id` | Server-issued bounded identifier, if exposure later approved | Never disclose paths, credentials, stack traces or sensitive logs |
| Evidence page | Proposed deterministic ID order, bounded page size and total count | Reject unbounded reads, malformed pagination and cursor replay |

**Candidate error taxonomy (not accepted HTTP map):** `invalid_request`, `unsupported_api_version`, `session_unavailable`, `stale_revision`, `source_identity_mismatch`, `unsupported_operation`, `capability_rejected`, `feature_disabled`. These are static safe **proposed codes only**. Exact HTTP statuses, response envelope, privacy uniformity, retry semantics and the omission of sensitive diagnostic details require Human freeze.

## 6. Errors, revisions, concurrency and idempotency (proposal)

A public API error contract is **not yet decided**. A candidate must preserve existing v1 error behavior and propose separate versioned v2 codes. Possible semantic mappings requiring review: malformed/unknown field → 400/422; unauthorized/forbidden → 401/403 **only after an authentication policy exists**; document/session not found → 404 or privacy-preserving uniform 404; stale revision/conflict → 409; source/provenance contract invalid → 422; unavailable/disabled capability → 403/404/409 as determined by Human API policy. Exact wire status, name and error envelope are **PENDING**.

Proposed error envelope should contain only an allowlisted code, static safe message, correlation ID and bounded public field references; no source excerpt, credentials, filesystem paths, document titles, arbitrary attacker-supplied field names, secret tokens or stack traces.

A future mutation contract (Candidate B) would require optimistic revision preconditions and canonical request/decision digests, idempotency for retries, strict decision ordering, explicit supersession/revocation, immutable audit history and safe concurrent state transitions. It must not claim durable storage, atomic filesystem rollback or real Human authentication from the existing in-memory synthetic system.

## 7. Authentication, authorization, storage and data handling — unresolved

Current synthetic actor `SYNTHETIC_REVIEWER_001` is a test-only identity convention, **not an authenticated user, role-based access control or legal attestation**. Human approved **local-only Candidate A with a mandatory owner/capability guard design requirement**, but has **NOT chosen its exact construction or authenticated it**. No v2 GET route may be implemented before the guard is separately selected and frozen. Any hypothetical externally accessible endpoint (currently **NOT AUTHORIZED**) would need further decisions about:
- Who may create/list/read a document/session, and how ownership is proved; default-deny in the absence of an approved mechanism.
- Who can inspect source/evidence vs submit/revoke Human decisions; user/tenant/resource ACL, audit and revocation.
- Where session/revision/decision state lives; retention, deletion, backups, concurrency, privacy and data classification.
- Local-only vs internal network vs public ingress, rate limits, abuse prevention, CORS/CSRF, authentication/session fixation.
- Secret/HMAC key custody and rotation, server-side canonical snapshots and source protection.
- Whether source data may ever include real or confidential papers and whether any AI provider is authorized (both currently **NO**).
- Whether any runtime/budget or deployment change is permitted (currently **NO**).

A feature flag, synthetic actor and untrusted proxy header are not authentication/authorization. **Approved policy is ephemeral per-process storage only**, bounded TTL, no persistent database. Propose a configurable synthetic TTL (for example 15 minutes) as a test parameter; **no numeric retention limit is Human-approved yet**. No public route or real-user workflow may be inferred from a synthetic test actor.

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
| AC-13 | Candidate A traffic loopback-only, separate opt-in OFF, Host/Origin/forwarded header and peer checks documented | DNS rebinding, malicious Host, loopback claims through proxy, non-loopback connection, feature disabled |
| AC-14 | All GETs require a valid server-side scoped capability or approved stronger local ownership guard | ID guessing, forged boolean/synthetic actor, absent/expired/stolen/replayed or cross-session capability, bootstrap via public GET |
| AC-15 | Information disclosure is bounded and deterministic with strict v2 schema | Unbounded evidence enumeration, source hash/filename/path leakage, response tokens, freeform locators, oversized pagination |
| AC-16 | Read-only operations have no source/session mutation or outbound provider effects | GET invokes pipeline, export, approval, cleanup, credential mint, file write, DB or network call |

Evidence gates for a **future** implementation: targeted offline tests, full relevant P2-002…P2-006 + AI-CONV-002/003 regression, security/negative coverage, supported schema validation, source/contract hashes, baseline v1 API regression, independent fixed-SHA reviewer PASS, exact-head CI SUCCESS, Render OFF/no verify, and protected merge with exact-main postmerge CI. These are not acceptance evidence for currently non-existent v2 code.

## 10. Human decision ledger — limited policy selected; wire/freeze pending

Human explicitly approved the nine-part **bounded Candidate A policy package** in [Issue #121 receipt #6207131354](https://github.com/nshaokiet/ai-ip-description-generator/issues/121#issuecomment-6207131354). Do not collapse a design direction into exact API contract authority. Status means what the Human actually approved:

| Gate | Human-approved direction (2026-10-16) | Residual freeze/implementation gate |
|---|---|---|
| **HD-V2-01** | **APPROVED — Candidate A only**, synthetic, local-loopback, GET/read-only; B and C deferred | No approved API implementation or network ingress |
| **HD-V2-02** | **POLICY APPROVED:** additive candidate `/api/v2`, versioned strict JSON, safe errors and no-Claims statuses | **PENDING:** exact paths, fields, error HTTP codes, JSON Schema/OpenAPI and response privacy |
| **HD-V2-03** | **SECURITY FLOOR APPROVED:** loopback-only, new opt-in OFF, scoped server-side capability/ownership guard mandatory | **PENDING:** real capability bootstrap, lifetime, ownership binding, token custody, Host/Origin/proxy behavior and final authn/authz approval |
| **HD-V2-04** | **APPROVED:** per-process ephemeral synthetic sessions, bounded TTL/staleness; no persistent store | **PENDING:** exact TTL, bounds, concurrency/idempotency, cleanup safety and retry behavior |
| **HD-V2-05** | **APPROVED:** bounded synthetic IDs/status/digests; no prose/original names/absolute paths/unrestricted locator/tokens | **PENDING:** exact allowed fields, pagination, correlation ID and exposure of source digests |
| **HD-V2-06** | **CONFIRMED DISABLED:** product Claims OFF, METHOD/PROCESS/COMPOSITION positive OFF; SYSTEM/APPARATUS synthetic eligibility for further P2-004 only; seven-input provenance stays unchanged | Future positive Claims and versioned migration each need separate Human decision; **not authorized** here |
| **HD-V2-07** | **APPROVED:** GET-only informational operations; no review writes, exports, provider or state-changing GET; local synthetic tests only | No deployment, public rollout or mutation enabled; exact read-only response profiles require separate contract freeze |
| **HD-V2-08** | **EXPLICITLY NOT AUTHORIZED:** paid/live AI, real/confidential research, public network ingress, Render/production, security release | All remain prohibited until separate Human exception |
| **HD-V2-09** | **APPROVED TO PREPARE v0.1.1 AND REVIEW:** maintain v0.1.0 history, new fixed-SHA independent review and exact-head CI | **PENDING:** separate explicit Human acceptance/freeze of full wire/security contract and separate implementation task authorization |

**Authority check:** v0.1.1 is an **approved bounded-policy proposal**, **NOT** frozen Backend API v2 specification. The wire-format and capability designs in §§4–6 remain subject to explicit Human selection after independent review. No API implementation, actual credentials, runtime code, schema migration or deployment may follow from this ledger alone.

## 11. Workflow V1 review, merge and next-task gates

**Specification-only deliverable:** this v0.1.1 Markdown file **plus immutable historical v0.1.0 archive** on the existing documentation-only PR branch, with explicit **POLICY APPROVED / WIRE CONTRACT PROPOSED / NOT FROZEN** status. Documentation may clarify current task references if separately approved, but it must not alter code, tests, schemas, dependencies, FastAPI routing or public contracts.

- Codex/ChatGPT source audit must include actual route prefixes, opt-in feature flag, AI-CONV-001/002/003 and released P2-002…006. Never claim v2 exists.
- Independent **Gemini 3.8 Flash High / Antigravity STRICT READ-ONLY** must inspect exact reviewed SHA, source/line accuracy, unsupported claims, positive/negative ACs, migration, threat model, Human decisions and scope. Report actual model/profile, session/reuse and PASS / REQUEST CHANGES / BLOCKED.
- Before any docs PR merge: require exact-head CI SUCCESS, accurate diff scope, fresh main/head protection and Render `no/off`; resolve review findings and obtain Human policy/freeze decision if a merge would be represented as an **approved/frozen v2 design**. A purely proposed artifact must remain explicitly **PROPOSED** if merged only as a proposal.
- After merge, verify exact-main CI, doc lineage and issue status. Later v2 implementation remains STOP until **separate Human implementation authorization** on approved policy/contracts.
- AI-CONV-003 closeout, AI-CONV-002/#111, GOV-REVIEWER-001/#113, BLK-003, EVAL-001 product runtime, V2/Phase H and provider/production decisions remain independent; do not turn one into another's approval.

**Disposition as of 2026-10-16:** Human approved **limited Candidate A design policy** and preparation of this v0.1.1 revision. Exact wire contract/security bootstrap, freeze and implementation decisions **PENDING**. AI-CONV-004 implementation **NOT STARTED**, all proposed endpoints **NOT IMPLEMENTED**, product Claims runtime **NOT ENABLED**.
