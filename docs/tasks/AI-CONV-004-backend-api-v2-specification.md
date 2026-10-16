# AI-CONV-004 — Backend API v2 specification (Candidate A policy approved; contract PROPOSED)

| Field | Value |
|---|---|
| Task | AI-CONV-004 |
| Document version | 0.1.3 — CANDIDATE A FINALIZATION-DRAFT PROPOSAL / NOT FROZEN / NO IMPLEMENTATION AUTHORITY |
| Document date | 2026-10-16 (Asia/Ho_Chi_Minh) |
| Status | FINALIZATION-DRAFT SPECIFICATION CANDIDATE — NEW INDEPENDENT REVIEW, CI AND EXPLICIT HUMAN FREEZE PENDING |
| Tracking issue | [#121](https://github.com/nshaokiet/ai-ip-description-generator/issues/121) |
| Human authorization | Specification preparation `HUMAN-AI-CONV-004-BACKEND-V2-SPEC-PREPARATION-2026-10-16`; bounded Candidate A selection `HUMAN-AI-CONV-004-CANDIDATE-A-POLICY-2026-10-16` — [Candidate A policy #6207131354](https://github.com/nshaokiet/ai-ip-description-generator/issues/121#issuecomment-6207131354); [detailed design drafting approval #6208917696](https://github.com/nshaokiet/ai-ip-description-generator/issues/121#issuecomment-6208917696); [v0.1.3 finalization-draft authorization #6210611707](https://github.com/nshaokiet/ai-ip-description-generator/issues/121#issuecomment-6210611707). **None authorizes final freeze or code implementation.** |
| Workflow | Workflow V1; Codex prepares candidate, Gemini 3.8 Flash High / Antigravity STRICT READ-ONLY independently reviews final SHA |
| Baseline | `main` at `ddc92f9a2d321e3e8507619276a200d35e7de696` (PR #120 merge) |
| Parent contracts | AI-CONV-001 v0.1.1; AI-CONV-002 internal orchestration v1.0.1; AI-CONV-003 synthetic authority overlay v1.0.0; released P2-002…P2-006 |
| Breaking change | No — Candidate A policy and proposed wire examples only; released v1 and USPTO stages unchanged |
| Runtime, data, budget | No endpoint implementation, no provider calls, no real/confidential source, no production, no Render deployment, no Workflow V2 / Phase H activation |

## 0. Version lineage and explicit limited Human authorization

| Version | Date | Change | Authorization / status |
|---|---|---|---|
| **0.1.0** | 2026-10-16 | Initial three-option Backend API v2 proposal and HD-V2-01…09 decision packet | [Preserved exact pre-decision artifact](history/AI-CONV-004-backend-api-v2-specification-v0.1.0.md); initial independent [Gemini-attributed specification PASS](https://github.com/nshaokiet/ai-ip-description-generator/pull/122#issuecomment-6207049807), no architecture freeze |
| **0.1.1** | 2026-10-16 | Candidate A policy-selected specification and initial security/negative-test requirements | [Byte-identical historical v0.1.1](history/AI-CONV-004-backend-api-v2-specification-v0.1.1.md); [attributed independent PASS on earlier SHA](https://github.com/nshaokiet/ai-ip-description-generator/pull/122#issuecomment-6208837151), not transferable |
| **0.1.2** | 2026-10-16 | Two GET detailed design; review integrity incident followed by corrective new-session PASS | [Byte-identical v0.1.2 history](history/AI-CONV-004-backend-api-v2-specification-v0.1.2.md); [false prior review blocked](https://github.com/nshaokiet/ai-ip-description-generator/pull/122#issuecomment-6210308524); [new-session corrective PASS receipt](https://github.com/nshaokiet/ai-ip-description-generator/pull/122#issuecomment-6210567224); accepted only for v0.1.2 |
| **0.1.3** | 2026-10-16 | L-01 disposition (no client version negotiation), exact candidate capability/Host/Origin/TTL/cursor/error rules, negative acceptance criteria and freeze decision checklist | [Human authorized new finalization draft ONLY](https://github.com/nshaokiet/ai-ip-description-generator/issues/121#issuecomment-6210611707); **new fixed-SHA reviewer PASS + exact-head CI required; final Human freeze and separate implementation authorization outstanding** |

**Human-selected design direction:** Candidate **A ONLY**, local-loopback, synthetic-only and GET/read-only. Candidate B (review writes, mutations) and C (real-paper/public Claims/exports) remain disabled and require separate explicit authorization. Product Claims stay disabled. Original seven-input P2-005/P2-006 provenance remains intact.

**Approval granularity:** Human approved Candidate A and detailed design for v0.1.2 and explicitly approved preparation of a v0.1.3 finalization draft to resolve LOW L-01. **None** is an implemented or final frozen contract. Exactly two GET routes, proposed values 15-minute capability, 60-minute session, 50 concurrent sessions and 25/50 evidence pagination are design candidates. Final capability bootstrapping, error/response contract freeze and implementation remain separately gated. Do not reclassify `PROPOSED` samples as released types or claim a user role/account exists.

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

## 3. Design alternatives (Candidate A selected for specification; B/C deferred)

| Candidate | Proposed exposure | Benefit | Blockers / recommendation |
|---|---|---|---|
| **A — Status/read-only first** | **HUMAN SELECTED POLICY**: loopback-only, default-disabled GET inspection of synthetic session/revision status and bounded IDs/digests, with no source prose, public Claims or mutable review state | Smallest trust boundary; supports strictly synthetic local inspection | **Policy approved; exact wire contract, scoped server-side capability guard and freeze still pending** |
| **B — Bounded synthetic review workflow** | Candidate POST create/advance revision and synthetic review decision endpoints, only under a new offline opt-in | Models Human review lifecycle and rejection semantics | Requires identity, authorization, persistence, CSRF/cross-session and audit decisions; synthetic actor is not authenticated; **do not implement until Human selects safeguards** |
| **C — Product Claims/export API** | Public positive Claims, document package/PDF/DOCX export, real Human approvals and real-paper processing | Product-value target | **DEFERRED / NOT AUTHORIZED**: new authority, versioned projection migration, real auth, data/privacy and production/provider approvals required |

**Human-approved sequence:** refine v0.1.3 into a reviewable finalization draft, specifically L-01, secure same-process bootstrap, strict protocol and negative tests; retain Candidate B as deferred and exclude Candidate C. **This does not freeze any wire-level endpoint or authorize implementation.**

## 4. Candidate A API surface — EXACTLY TWO PROPOSED GETs, NOT IMPLEMENTED

The Human approved the **detailed design as the basis of v0.1.2 drafting** in [Issue #121 #6208917696](https://github.com/nshaokiet/ai-ip-description-generator/issues/121#issuecomment-6208917696). These are **proposed**, not finally frozen or registered HTTP routes.

| Proposed operation | Allowlisted information only | Explicit prohibition |
|---|---|---|
| `GET /api/v2/sessions/{session_id}/status` | Safe synthetic session revision, stage, zero-Claims and Human-review-required metadata; package status folded into this response | No separate package-status route, package content, positive Claims, real source data or mutation |
| `GET /api/v2/sessions/{session_id}/revisions/{revision}/evidence-index` | Bounded page of synthetic `evidence_id` and vetted non-sensitive digest, exact revision binding | No prose, raw source fingerprints/locations, filenames, paths, raw evidence, unbounded listing or export |

The previously proposed third `GET .../package-status` is **DEFERRED / REMOVED FROM CANDIDATE A**. All review writes, POST session creation, document exports and public Claims belong to unapproved B/C future scopes; no hidden or alternative routes are allowed.

### 4.1 Candidate local security and request path (not frozen)

- Dedicated proposed `AI_IP_ENABLE_LOCAL_SYNTHETIC_V2_API` flag **OFF by default**, independent from existing local v1 opt-in. This setting **does not currently exist** in deployed code.
- Bind only to literal loopback `127.0.0.1` or `::1`, validate true transport peer. Strict Host allowlist for local listener; reject DNS rebinding, unexpected browser Origin, unapproved forwarded/proxy headers and non-loopback socket peers. Never trust `X-Forwarded-For` or a caller-supplied actor ID as proof of identity. No CORS broadening.
- Both GETs require `Authorization: Bearer <opaque-capability>` as a **candidate**. No query-string, cookie, URL fragment/path, GET response or public mint endpoint may supply this secret. Unauthenticated resource enumeration must fail uniformly.
- Guard is scoped server-side to session, document/source identity, active revision, read-only operations, expiry and revocation. Bearer possession is a synthetic **local capability**, **not real Human authentication**. A compromised same-user local process remains an explicit threat.
- JSON GETs are pure reads: **no session creation, cleanup write, key rotation, evidence reconstruction, Claims promotion, model/provider call, export, rendering, audit mutation, file/database write or outbound network access**. Expiry check is nonmutating; trusted internal lifecycle owns cleanup.

### 4.2 Candidate trusted in-process capability lifecycle (not implemented)

1. A future **trusted same-process** synthetic offline orchestrator creates an already source-bound internal session, with no HTTP session-creation path.
2. A trusted **in-process bootstrap** derives an unpredictable CSPRNG bearer capability after session creation. Only a trusted CLI/test harness receives secret material **out of band**, not through a new web endpoint. Exact bootstrap channel and OS-user/process threat boundary require later Human security freeze.
3. Store only a derived keyed verifier, not plaintext capability. Proposed HMAC-based scoped verifier uses a separately protected ephemeral process key and constant-time comparison; secure storage, rotation and canonical serialization require independent security review.
4. Bind verifier to session/document identity, revision applicability, read-only scope and absolute expiry. Revoke on trusted cleanup, supersession or revision invalidation. Reject cross-session/document/revision and replay of invalidated tokens; never log or reflect token or verifier.
5. Human-endorsed **proposal limits**: capability absolute TTL **15 minutes**; session in-memory TTL **no more than 60 minutes**; **maximum 50 concurrent synthetic sessions per process**. A capability cannot outlive its session. Session creation over capacity fails closed; GET never evicts.
6. The capability does **not** establish a real user/organization identity, durable audit, production authorization or permission to use real/confidential source data.

### 4.3 Pagination, privacy and atomic reads (candidate)

- Proposed evidence-index query parameters: `limit` optional strict integer **1..50**, default **25**; `cursor` optional bounded opaque authenticated cursor, no extra query fields. Cursor binds to **session, revision, bearer scope, deterministic evidence order, position and expiration**; reject stale, malformed, expired, tampered or cross-session/revision cursors.
- Proposed deterministic ascending `evidence_id` sort with stable digest tie-break; snapshot-pinned, bounded response. Return **no total count**. Do not expose raw source/document SHA, filenames, paths, locators, third-party data, source prose or secrets.
- GET reads a trusted immutable snapshot; concurrent revision changes fail closed without side effects. Successful retries while the snapshot is valid are deterministic. Expiry and state retirement occur only via trusted lifecycle, not during GET.

## 5. Candidate representation and validation rules

All types below are **proposed** versioned design objects; they have no released schema, server route, or frontend binding yet.

### 5.1 Candidate strict GET response schemas — proposal only, NOT RELEASED

**Status GET proposed HTTP 200 response** (all keys required, extra keys forbidden):

```json
{
  "api_version": "2.0.0",
  "session_id": "synthetic-session-id",
  "revision": 1,
  "stage": "CLAIMS_REVIEW_REQUIRED",
  "claims_status": "HUMAN_CONFIRMATION_REQUIRED",
  "claims_count": 0,
  "review_required": true,
  "product_claims_runtime_enabled": false
}
```

Exactly eight top-level allowlisted properties; `api_version="2.0.0"` is a **proposed future value** and is not an existing public contract. `stage` must be allowlisted from trusted offline orchestration and `claims_status` from trusted package state. `claims_count` is nonnegative metadata, never returned Claim text. `HUMAN_CONFIRMATION_REQUIRED` with zero Claims is a valid outcome, and product-runtime state is always `false`. Response is synthetic-only; never append source identity, raw source SHA, document filename, private decision seal, revision token or bearer capability.

**Evidence-index GET proposed HTTP 200 response** (all keys required, extras forbidden):

```json
{
  "api_version": "2.0.0",
  "session_id": "synthetic-session-id",
  "revision": 1,
  "items": [
    {"evidence_id": "synthetic-evidence-001", "digest": "synthetic-approved-digest"}
  ],
  "next_cursor": null
}
```

Exactly five top-level keys and two keys per evidence item, `items` length **0..50**, sorted by synthetic evidence ID. Digest is a **vetted synthetic-safe fingerprint**, not an actual paper/content/source hash disclosed by default. `next_cursor` is null or a bounded authenticated page cursor (not a bearer). An empty page is valid. **No total count, locator, source excerpts or raw document data.**

**Static safe error envelope — proposed only:**

```json
{
  "code": "session_unavailable",
  "message": "The session is unavailable.",
  "correlation_id": "synthetic-correlation-id"
}
```

Exactly three fields; `code` from a closed allowlist, `message` static, and `correlation_id` server-generated bounded safe ASCII, never client-provided. No trace, credentials, source text, file paths or arbitrary reflected input.

**Candidate privacy-preserving HTTP map (not finally frozen):**

| Proposed HTTP code | Safe `code` | Scope and precedence |
|---|---|---|
| **200** | Success, no error envelope | Only after trusted listener, capability and session/revision checks |
| **404** | `session_unavailable` | Absent/expired/foreign/unauthorized session or capability, including malformed/absent bearer: *uniform generic response*, no existence oracle |
| **409** | `stale_revision` | Only after successful owner/capability authorization and mismatch against trusted current revision |
| **422** | `invalid_request` | Only after relevant capability authorization; malformed authorized query/limit/cursor/version, no FastAPI early-422 session leak |
| **404** | `feature_disabled` or generic 404 | If router is absent when flag OFF, framework generic 404 must remain acceptable; do not promise custom JSON from an unregistered router |
| **500** | `internal_error` | Sanitized static failure; never disclose exception/path/source |
| **TBD** | `unsupported_api_version` | If version negotiation is needed; exact request-version mechanism remains a final freeze decision |

**Authorization order proposal:** enforce peer/listener, Host and Origin/proxy policy and global size checks first; apply OFF flag; reject absent/malformed bearer uniformly; verify scoped capability ownership **before** revealing session-specific validation (including FastAPI/Pydantic path/query errors); then check current revision and bounded input; only then return status/evidence metadata. Malformed Host and pre-auth errors use safe generic responses without resource enumeration. Uniform error *status, body and observable behavior* must be tested, not inferred from return code alone.

**All snippets are proposal samples only**, not actual running endpoints or already-released JSON Schema/OpenAPI files. No external authenticator exists here.

### 5.2 Mandatory candidate invariants

- **Identity and scope:** Each request resolves a verified document, source SHA-256, exact session, revision and token; compare against retained trusted server state, not merely caller claims. Evidence references must be valid for the exact source and structural target.
- **Versioning:** Validate explicit API/schema versions and reject unknown/mixed versions. Do not silently coerce arbitrary `dict`, extra fields, unsupported families or enum values to authoritative states.
- **Stale/tamper fail-closed:** Invalid or stale session/revision/token, source/config/reconstruction digest mismatch, cross-document evidence or signature mismatch must never return positive authority. Cross-session replay and conflicts must have deterministic rejection.
- **Nonpromotion:** `UNKNOWN`, `OPTIONAL`, `CONDITIONAL`, inferred membership, missing evidence and client-submitted `confirmed=true` must not become `ESSENTIAL` or an eligible Claim. Revocation/supersession must invalidate any cached eligibility.
- **Read-only semantics:** A GET for status/evidence must not start a model run, advance a revision, render documents, authorize Claims or mutate authority/audit state. Existing cleanup semantics cannot be weakened.
- **Released-contract compatibility:** AI-CONV-002 and P2-005/P2-006 validation remains the source of truth; the seven-input projector stays exact. A hypothetical v2 authority-bearing projection requires a later **separately approved migration contract**, not an injected property.
- **Fail-closed output:** `CLAIMS_REVIEW_REQUIRED` and `HUMAN_CONFIRMATION_REQUIRED` + zero Claims are legitimate non-error outcomes. Preserve draft-only, non-filing and non-legal-advice notices; do not advertise issued USPTO B2 status.

### 5.3 Candidate exact field/query constraints — still subject to Human freeze

| Domain | Proposed type / limit | Mandatory security behavior |
|---|---|---|
| `api_version` | Future proposed literal `"2.0.0"` in responses | No silent downgrade or implication that v2 is currently deployed |
| Path `session_id` | Opaque synthetic server-generated URL-safe ASCII, proposed 1..64 characters | Not a credential; bind to owned in-memory session |
| Path `revision` | Strict integer 1..2,147,483,647 | Reject stale/future, no coercion |
| Query `limit` | Optional integer 1..50, default 25 | Reject duplicate, negative, zero, 51+, float, scientific-notation and oversized values |
| Query `cursor` | Optional scoped opaque authenticated token, proposed max 512 ASCII chars | Bind to session, revision, capability, page position and expiry; no plain source IDs |
| `Authorization` | Candidate HTTP `Bearer` opaque per-session capability | Checked by trusted server-side verifier, no public bootstrap, URL/GET reflection or log |
| Status `stage` | Existing trusted orchestration enum | Never derived from caller parameters |
| Status `claims_status`, `claims_count` | Trusted enum and nonnegative bounded integer | `HUMAN_CONFIRMATION_REQUIRED` with zero is valid, no Claim text or essentiality promotion |
| Evidence `items[]` | Synthetic `evidence_id`, vetted synthetic-only bounded `digest` strings, each proposed 1..128 chars | No raw source fingerprint/locator/filename/content, deterministic sort, max 50 |
| Evidence `next_cursor` | null or authenticated scope-bound opaque token | No raw bearer, source excerpt, count, unbounded cursor |
| Error `code/message/correlation_id` | Static safe closed allowlist; correlation ID proposed 1..64 safe characters | No user/reflected header, path, stack or token |
| Every v2 model | Strict closed object with bounded serialization | Reject extra/mismatched fields, unsafe encodings, oversized header/body |

**No FastAPI route, Pydantic model, JSON Schema/OpenAPI file, implementation test, server setting, credential or deployment is added under this specification task.** Exact regex/enums, cursor verifier/key custody and privacy-equivalent error map remain subject to new independent review and final Human contract freeze.

## 6. Errors, revisions, concurrency and idempotency (proposal)

The candidate error map, response envelope and fail-closed authorization order are now proposed in §5.1. `404 session_unavailable` applies uniformly to missing/unauthorized sessions; only authorized requests may receive `409 stale_revision` or `422 invalid_request`. Feature-disabled behavior must avoid inventing a custom response if the router was never mounted. All status codes, privacy equivalence and error wire types remain **UNFROZEN** pending independent security review and explicit final Human approval; released v1 error handling is untouched.

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

A feature flag, synthetic actor and untrusted proxy header are not authentication/authorization. Human explicitly approved the numerical **15-minute capability TTL, maximum 60-minute synthetic session TTL and 50-session process capacity as drafting values for v0.1.2**; they are **not implemented settings or a frozen security contract**. Session retirement/eviction and capability revocation must be trusted internal lifecycle operations, never side effects of a GET; no DB or persistent audit is selected. No public route or real-user workflow may be inferred from a synthetic test actor.

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
| AC-17 | Candidate A has exactly two GETs; package status is folded into status | Third package-status route or any POST/review/export/Claims route accidentally reachable |
| AC-18 | Trusted in-process capability bootstrap and `Authorization` bearer privacy hold | Unauthenticated capability mint via HTTP, secret in URL/cookie/GET response/log, cross-session or revoked/revision replay, insecure verifier |
| AC-19 | 15-minute absolute capability, <=60-minute in-memory session, <=50 sessions/process enforced without GET mutation | Expired capability accepted; capability outlives session; 51st creation silently evicts/overflows; stale GET mutates cleanup |
| AC-20 | Evidence query default 25, limit 1..50, deterministic ID order, opaque bound cursor and no total count | 0/51/float/huge limit; tampered, expired, foreign or stale cursor; source/locator leak; ambiguous duplicate query |
| AC-21 | Authentication and privacy checks precede resource-specific validation; unauthorized resources uniformly opaque | FastAPI pre-auth 422 reveals session existence; 409 returned to unauthorized user; timing/status oracle; forged Host/forwarded header |
| AC-22 | Proposed status/evidence JSON strictly allowlisted, source-free and token-free | Extra `source_identity`, raw SHA, filename/path, bearer/revision token, secret/seal, source prose or unsafe digest appears |

Evidence gates for a **future** implementation: targeted offline tests, full relevant P2-002…P2-006 + AI-CONV-002/003 regression, security/negative coverage, supported schema validation, source/contract hashes, baseline v1 API regression, independent fixed-SHA reviewer PASS, exact-head CI SUCCESS, Render OFF/no verify, and protected merge with exact-main postmerge CI. These are not acceptance evidence for currently non-existent v2 code.

## 10. Human decision ledger — detailed v0.1.2 drafting approved, FINAL freeze pending

The Human approved both [Candidate A limited design policy #6207131354](https://github.com/nshaokiet/ai-ip-description-generator/issues/121#issuecomment-6207131354) and [detailed wire/security package for v0.1.2 specification drafting #6208917696](https://github.com/nshaokiet/ai-ip-description-generator/issues/121#issuecomment-6208917696). This approval enables **documentation and review, not a final accepted wire contract** or code.

| Gate | Approved as limited direction / reviewed design candidate | Still pending or explicitly excluded |
|---|---|---|
| **HD-V2-01** | **APPROVED:** synthetic local-loopback, GET-only Candidate A; B/C deferred | No endpoint implementation or public network |
| **HD-V2-02** | **DRAFTING DESIGN APPROVED:** exactly two proposed `/api/v2` GETs, safe JSON `api_version="2.0.0"` future, no-Claims statuses, candidate 404/409/422/500 errors | **PENDING separate Human FINAL WIRE FREEZE:** precise paths, schema/regex/version/error privacy mapping following new review |
| **HD-V2-03** | **DRAFTING DESIGN APPROVED:** default-OFF independent v2 flag, loopback/Host/Origin/proxy checks, trusted in-process out-of-band scoped bearer bootstrap, server-held keyed verifier | **PENDING separate Human SECURITY FREEZE:** actual bootstrap/OS-process trust, verifier storage/rotation, header and privacy model; no real authn/authz |
| **HD-V2-04** | **DRAFTING VALUES APPROVED:** ephemeral per-process, capability absolute TTL 15m, session max 60m, max 50 sessions, fail-closed revocation/expiry | **PENDING final review/freeze:** concurrency, capacity, timestamp and cleanup semantics; no DB |
| **HD-V2-05** | **DRAFTING VALUES APPROVED:** synthetic metadata only, page default 25/max 50, opaque revision/scope-bound cursor | **PENDING final review/freeze:** safe digest allowlist, pagination privacy, exact string format and exposure |
| **HD-V2-06** | **CONFIRMED DISABLED:** public product Claims runtime, METHOD/PROCESS/COMPOSITION positive authority, P2-005/P2-006 seven-input provenance migration | Any real Claims or altered source projection requires separate Human approval |
| **HD-V2-07** | **APPROVED POLICY:** informational GET only, no export/review write/provider/render and no GET-side state changes | No deployment or production, no mutating API |
| **HD-V2-08** | **NOT AUTHORIZED:** real/confidential research, paid/live AI, Render/production, public ingress and V2/Phase H | Separate explicit exception would be required |
| **HD-V2-09** | **APPROVED NOW:** archive reviewed v0.1.1 byte-identically, revise PR #122 to v0.1.2 docs-only, obtain NEW fixed-SHA Gemini 3.8 Flash High STRICT READ-ONLY review and exact-HEAD CI | **PENDING final Human acceptance/freeze of complete wire/security contract AND separate later implementation authorization** |

**Gate interpretation:** approval to **write and review** a proposed precise API design is **not** approval to implement or deploy it. Even after Gemini PASS and CI SUCCESS at new HEAD, PR #122 remains DRAFT until governance/Human determines whether and how to freeze/merge this proposed contract.

## 11. Workflow V1 review, merge and next-task gates

**Specification-only deliverable:** this v0.1.2 Markdown file **plus immutable historical v0.1.0 and v0.1.1 archives** on the existing documentation-only PR branch, with explicit **POLICY APPROVED / WIRE CONTRACT PROPOSED / NOT FROZEN** status. Documentation may clarify current task references if separately approved, but it must not alter code, tests, schemas, dependencies, FastAPI routing or public contracts.

- Codex/ChatGPT source audit must include actual route prefixes, opt-in feature flag, AI-CONV-001/002/003 and released P2-002…006. Never claim v2 exists.
- Independent **Gemini 3.8 Flash High / Antigravity STRICT READ-ONLY** must inspect exact reviewed SHA, source/line accuracy, unsupported claims, positive/negative ACs, migration, threat model, Human decisions and scope. Report actual model/profile, session/reuse and PASS / REQUEST CHANGES / BLOCKED.
- Before any docs PR merge: require exact-head CI SUCCESS, accurate diff scope, fresh main/head protection and Render `no/off`; resolve review findings and obtain Human policy/freeze decision if a merge would be represented as an **approved/frozen v2 design**. A purely proposed artifact must remain explicitly **PROPOSED** if merged only as a proposal.
- After merge, verify exact-main CI, doc lineage and issue status. Later v2 implementation remains STOP until **separate Human implementation authorization** on approved policy/contracts.
- AI-CONV-003 closeout, AI-CONV-002/#111, GOV-REVIEWER-001/#113, BLK-003, EVAL-001 product runtime, V2/Phase H and provider/production decisions remain independent; do not turn one into another's approval.

**Disposition as of 2026-10-16:** Human approved Candidate A policy and detailed **v0.1.2 drafting design only**. Independent Gemini review at new exact SHA, CI and explicit final wire/security contract freeze are still **PENDING**; API implementation is **NOT AUTHORIZED**, no backend/API routes/schemas changed, product Claims remain disabled. AI-CONV-004 implementation **NOT STARTED**, all proposed endpoints **NOT IMPLEMENTED**, product Claims runtime **NOT ENABLED**.
