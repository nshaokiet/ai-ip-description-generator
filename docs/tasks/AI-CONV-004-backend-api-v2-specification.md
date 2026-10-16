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

### 4.1 Finalization-draft network/HTTP boundary (NOT IMPLEMENTED, NOT FROZEN)

**Threat model:** Candidate A is for a single trusted same-process synthetic/offline test harness only; it is not multi-tenant and has no authenticated real Human. A local malicious process running under the same OS user, a compromised trusted harness, stolen bearer, malicious dependency or debug instrumentation remains capable of compromising this limited boundary. Do not claim the scheme solves those threats or is production identity.

- **Registration & binding:** propose a dedicated `AI_IP_ENABLE_LOCAL_SYNTHETIC_V2_API` opt-in **OFF** by default, separate from v1. Flag OFF means **do not register either route** (ordinary generic framework 404). When enabled in a future *separately authorized local test harness*, bind the actual HTTP listener to literal `127.0.0.1` or `::1` only. Reject true socket peers outside the exact loopback address family; neither `localhost` DNS resolution nor any forwarded header is evidence of peer identity. No proxy, container port publication, tunnel, reverse-proxy or Render listener.
- **Host/Origin:** require one normalized `Host` that equals the server's configured *literal* loopback host and port; reject DNS aliases (including `localhost`), wildcard, user-info, duplicate Host, invalid bracket/port or unexpected Host. This sacrifices convenience to prevent DNS rebinding. Reject any `Origin` header (no browser workflow approved), all `Forwarded`, `X-Forwarded-For`, `X-Forwarded-Host`, `X-Forwarded-Proto`, `X-Real-IP` or equivalent forwarded-source headers, and preflight `OPTIONS`; do not enable CORS. No Host/Origin validation can turn a public listener into a safe one.
- **Pre-router guard:** to prevent FastAPI/Pydantic's eager 422 parsing from leaking resource existence, any *hypothetical* adapter must run a trusted ASGI access gate before route matching and typed path/query conversion. Validate global request-size and peer/Host/Origin safely without revealing whether a session exists; reject absent or malformed Bearer uniformly before resource-specific error details. The precise authorization ordering (§5.1) is normative *within this design proposal*. No new ASGI middleware or route currently exists.
- **Allowed operations:** exactly the two listed GET routes. `HEAD`, `OPTIONS`, `POST`, `PUT`, `PATCH`, `DELETE` and any `/package-status`, export, review-write or capability-mint route are **NOT APPROVED**. Request bodies are not permitted. Unknown resource/route stays generic 404.
- **Access transport:** `Authorization: Bearer <capability>` proposed for both GETs, only header transport, not URL, cookie, response body, referrer, logs, file, remote proxy or environment variable. A flag, Host match, loopback peer and a synthetic actor ID are never authorization alone.

### 4.2 Capability and trusted-process model (candidate exact draft)

**No API bootstrap route and no cross-process delivery.** The only proposed initial use is a **single trusted in-process Python harness** that (i) creates a synthetic session through an existing internal/offline call, (ii) invokes a prospective trusted in-process capability issuer as an ordinary function, (iii) retains the capability transiently in the same process memory, and (iv) sends GETs through an in-process ASGI/TestClient transport. This explains how a token reaches a client **without any new HTTP issuance endpoint**. There is **no approved secure handoff to a separately launched CLI/web browser/process**. That capability is explicitly **DEFERRED** pending a separately reviewed OS-user/process IPC policy. This is a *specification*, not a claim such a function or route currently exists.

1. **Secret generation:** propose 32 cryptographically random bytes (256-bit CSPRNG) per capability, encoded as a **43-character unpadded base64url** Bearer secret; reject noncanonical encoding, duplicate/extra Authorization headers, control characters and arbitrary length. No plaintext token in retained state.
2. **Process key/verifier:** create a distinct 32-byte CSPRNG verifier key on process startup; keep only in process memory and do not persist, log or export it. Retain an HMAC-SHA256 keyed token verifier plus canonical trusted scope binding; use constant-time digest verification. No caller may supply trusted document/source/revision metadata. Process restart destroys key, sessions and all capabilities; child workers must not share or fork a supposedly isolated key/session snapshot. **Exactly one process / one trusted harness** is the proposed limit.
3. **Scope:** verifier record binds exact opaque synthetic session ID, retained document/source identity, currently authorized revision, GET-only permission, process incarnation and expiry. An attempt to use a valid bearer with a different session, document or superseded revision fails with non-enumerating authorization response. Do not use a source SHA or public hash as authority.
4. **Time:** measure absolute TTL using the process monotonic clock: capability expires at `created_monotonic + 900 seconds`, session at or before `created_monotonic + 3600 seconds`; the **earlier** expiry always wins. Never extend either expiry by GET or refresh-on-read. For revision change, revocation or trusted cleanup, invalidate the old verifier and associated cursors. Use deterministic comparisons at equality (expired at `now >= deadline`). Key rotation is process restart, or explicitly trusted lifecycle rekey invalidating all old capabilities; never rotate on GET.
5. **Capacity/retirement:** keep at most **50 active synthetic sessions per process**; trusted non-HTTP session creation over capacity fails closed with a typed *internal* error, **not** a newly invented HTTP 429. Periodic or explicit trusted lifecycle removes expired data out of the GET path. A GET can observe expiry but never alter verifier maps, run cleanup, evict, write disk/DB or call a provider.
6. **Secret custody and limitations:** trusted test code must avoid printing exception locals or logging Authorization. The design does not protect against same-user malicious local code, debugger access, unsafe OS process handoff or stealing an in-memory bearer; it is strictly synthetic non-production, not real-user attestation, authn/authz, legal approval or a security product.

**Human freeze blocker:** the above deliberately **does not approve** an OS IPC transport, separate CLI process, desktop browser or production listener. If use outside one trusted in-process harness becomes necessary, stop and request a new Human security/architecture decision.

### 4.3 Candidate evidence pagination and safe snapshot lifecycle

- Request on evidence GET: `limit` optional canonical base-10 integer string from **1 to 50**, default **25**; `cursor` optional **1..512** ASCII base64url string (no whitespace, duplicates, null coercion or unknown query parameters). Revision in path is canonical positive base-10 no-leading-zero string with numeric value <= 2,147,483,647.
- Trusted immutable evidence snapshot uses ascending canonical synthetic `evidence_id` order, tie-break on vetted digest. Page boundary must not depend on a mutable reconstruction or GET-side state changes.
- Proposed **stateless authenticated cursor**: base64url encoding of a canonical strictly versioned payload carrying only non-sensitive page position, snapshot identifier, revision, requested page size, scope-keyed binding and expiry, plus HMAC-SHA256 over that payload with an ephemeral **separate cursor-signing key**. It is *opaque as a client API contract*, **not confidential encryption**: base64url may reveal page position; **never put source content, document names/hashes, tokens, secret verifiers or underlying evidence identifiers inside the cursor**. Verify signature in constant time; reject tamper, foreign session/scope, page-size mismatch, expired snapshot/revision, stale cursor and oversized values. The exact representation and whether mere pagination position metadata is acceptable still need Human privacy freeze.
- An authorization-validated GET should be deterministic for the same retained snapshot, filter and cursor. Calculating an HMAC and returning a cursor is not an internal state mutation; no cursor-store write, secret mint, cleanup, model execution, render, export or database/file write. The signed cursor cannot grant rights without an independently valid Bearer capability.
- Evidence response contains only allowlisted synthetic `evidence_id` and **vetted synthetic-only safe digest**, with `items` 0..50 and nullable `next_cursor`; **no total count**, raw source/fingerprint, filename, freeform locator, claim prose or private seal. Unauthorized and expired callers see no metadata.

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

Exactly eight top-level allowlisted properties; `api_version="2.0.0"` is a **proposed future value** and is not an existing public contract. `stage` must be allowlisted from trusted offline orchestration and `claims_status` from trusted package state. `claims_count` is **zero for this Candidate A fail-closed status-only design**, never a count of unapproved internal P2-004 draft candidates or returned Claim text. `HUMAN_CONFIRMATION_REQUIRED` with zero Claims is a valid outcome, and product-runtime state is always `false`. Response is synthetic-only; never append source identity, raw source SHA, document filename, private decision seal, revision token or bearer capability.

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

**Candidate privacy-preserving HTTP map (not finally frozen, NO client API version negotiation):**

| Proposed HTTP code | Safe `code` | Scope and precedence |
|---|---|---|
| **200** | Success, no error envelope | Only after trusted listener, capability and session/revision checks |
| **404** | `session_unavailable` | Absent/expired/foreign/unauthorized session or capability, including malformed/absent bearer: *uniform generic response*, no existence oracle |
| **409** | `stale_revision` | Only after successful owner/capability authorization and mismatch against trusted current revision |
| **422** | `invalid_request` | Only after relevant capability authorization; malformed authorized query/limit/cursor/version, no FastAPI early-422 session leak |
| **404** | Generic framework route-not-found | Separate v2 flag OFF means routes unregistered; no custom `feature_disabled` error is promised or needed |
| **500** | `internal_error` | Sanitized static failure; never disclose exception/path/source |


**Authorization order proposal:** enforce peer/listener, Host and Origin/proxy policy and global size checks first; apply OFF flag; reject absent/malformed bearer uniformly; verify scoped capability ownership **before** revealing session-specific validation (including FastAPI/Pydantic path/query errors); then check current revision and bounded input; only then return status/evidence metadata. Malformed Host and pre-auth errors use safe generic responses without resource enumeration. Uniform error *status, body and observable behavior* must be tested, not inferred from return code alone.

**LOW L-01 disposition for v0.1.3 — resolved IN THE PROPOSAL, not implemented:** Candidate A has **no client-side API version negotiation**. The version is selected solely by the candidate `/api/v2` URL namespace; successful server responses contain the literal `"api_version": "2.0.0"` only. There is **no request version parameter, `Accept-Version`, `X-API-Version` or other version-negotiation header**. Unrecognized query parameters or client-supplied version metadata must never trigger a special `unsupported_api_version` response; after ownership verification, such supplied fields are treated as `422 invalid_request` under the strict allowlist. Before authorization, they must not cause an early 422 session-existence oracle. The previously undefined `unsupported_api_version` HTTP status/code is **not part of this v0.1.3 candidate taxonomy**, and future version negotiation is explicitly deferred to another Human-approved versioned contract. No enum, code, HTTP status or model for it should be implemented under Candidate A.

**All snippets are proposal samples only**, not actual running endpoints or already-released JSON Schema/OpenAPI files. No external authenticator exists here.

### 5.2 Mandatory candidate invariants

- **Identity and scope:** Each request resolves a verified document, source SHA-256, exact session, revision and token; compare against retained trusted server state, not merely caller claims. Evidence references must be valid for the exact source and structural target.
- **Versioning:** Candidate A has a fixed response literal `api_version="2.0.0"` and `/api/v2` route namespace, with **no client version-negotiation request field/header**. Extra or unrecognized client version fields are forbidden by the authorization-first strict input allowlist, not converted into a new error status. Do not coerce arbitrary values or authorize Claims based on a version field.
- **Stale/tamper fail-closed:** Invalid or stale session/revision/token, source/config/reconstruction digest mismatch, cross-document evidence or signature mismatch must never return positive authority. Cross-session replay and conflicts must have deterministic rejection.
- **Nonpromotion:** `UNKNOWN`, `OPTIONAL`, `CONDITIONAL`, inferred membership, missing evidence and client-submitted `confirmed=true` must not become `ESSENTIAL` or an eligible Claim. Revocation/supersession must invalidate any cached eligibility.
- **Read-only semantics:** A GET for status/evidence must not start a model run, advance a revision, render documents, authorize Claims or mutate authority/audit state. Existing cleanup semantics cannot be weakened.
- **Released-contract compatibility:** AI-CONV-002 and P2-005/P2-006 validation remains the source of truth; the seven-input projector stays exact. A hypothetical v2 authority-bearing projection requires a later **separately approved migration contract**, not an injected property.
- **Fail-closed output:** `CLAIMS_REVIEW_REQUIRED` and `HUMAN_CONFIRMATION_REQUIRED` + zero Claims are legitimate non-error outcomes. Preserve draft-only, non-filing and non-legal-advice notices; do not advertise issued USPTO B2 status.

### 5.3 Candidate explicit field grammar and request normalization (FINALIZATION DRAFT, NOT FROZEN)

| Candidate field / transport | Proposed precise accepted grammar and bounds | Fail-closed interpretation |
|---|---|---|
| Response `api_version` | **Literal string `"2.0.0"` only**, read from server-owned contract; path namespace `/api/v2` | No client version query or header. Any unexpected client `version`/version metadata is an unknown field (post-authorization `422 invalid_request`), not a special version-negotiation error |
| Path `session_id` | `^[A-Za-z0-9_-]{1,64}$` ASCII synthetic opaque identifier; server generated, no percent-decoding ambiguity | Never a credential; bind to active internal session/document scope |
| Evidence path `revision` | `^[1-9][0-9]{0,9}$`, numeric value **1..2,147,483,647**, no leading zero | Active server-side revision must match; stale authorized requester gets 409 |
| Evidence query `limit` | Optional canonical decimal `^(?:[1-9]|[1-4][0-9]|50)$`, **default 25** | Reject duplicates, 0/51+, float, exponent, whitespace, non-ASCII digits, coercion |
| Evidence query `cursor` | Optional unpadded base64url ASCII `^[A-Za-z0-9_-]{1,512}$`, canonical round-trip required | Constant-time authenticated cursor verification; bind scope, session, revision, page size, expiry; reject tamper after auth |
| `Authorization` | Exactly one header with literal scheme `Bearer ` + 43 unpadded base64url chars `[A-Za-z0-9_-]{43}` decoding to **32 bytes**; no duplicates or line folding | HMAC verifier scoped and checked in constant time; token NEVER returned/logged; no URL/cookie bootstrap |
| Response `claims_count` and `product_claims_runtime_enabled` | For current fail-closed Candidate A synthetic status: `claims_count=0`, `product_claims_runtime_enabled=false` | Never count internal tentative standalone P2-004 candidate claims as released product claims |
| `stage`, `claims_status`, `review_required` | Server-owned enum/boolean from retained immutable orchestration snapshot, with valid `CLAIMS_REVIEW_REQUIRED` / `HUMAN_CONFIRMATION_REQUIRED` example | Do not invent unknown stage enums, convert UNKNOWN/OPTIONAL/CONDITIONAL to ESSENTIAL, or accept caller-provided review flags |
| Evidence `items[]` | Array length **0..50**; item keys exactly `evidence_id`, `digest` with URL-safe bounded synthetic strings proposed **1..128** | Strict source-bound evidence validation; digest must be a **vetted synthetic-safe** value, not an unredacted real source hash |
| Evidence `next_cursor` | `null` or bounded authenticated cursor string | No total count, plaintext source ID, raw paper metadata, bearer secret or duplicate page |
| Error envelope | Exactly `code`, `message`, `correlation_id` only; correlation ID generated server-side, proposed ASCII `[A-Za-z0-9_-]{1,64}` | All message text static and bounded; no extra field path, stack trace, token, host header or user-reflected values |
| Unknown request field | GETs have **no body** and no query except `limit`/`cursor` on evidence route | No `Accept-Version`, `X-API-Version`, `?version` or accidental Pydantic extra-field coercion |
| Global envelope | Canonical UTF-8 JSON, strictly closed objects, bounded headers/path/query and response | Reject invalid Unicode/duplicate query/JSON fields; no positive Claims/runtimes, no file writes |

**No JSON Schema/OpenAPI file, route, middleware, secret, Pydantic model or test is created by this specification PR.** Regex/digest privacy, error-observability consistency, local Host configuration and exact enum sets need independent security review and separate Human final freeze.

## 6. Errors, revisions, concurrency and idempotency (proposal)

The proposed v0.1.3 error map and fail-closed authorization order are in §5.1: uniform `404 session_unavailable` when the untrusted requester cannot establish ownership, post-auth `409 stale_revision` and `422 invalid_request` for typed query/cursor violations, **generic framework 404 when feature OFF or route/method is unregistered**, and safe static 500. **No client version negotiation or `unsupported_api_version` error/status** is in scope, explicitly resolving prior reviewer L-01. The map, privacy equivalence and exact representation remain **UNFROZEN** pending independent review and explicit final Human security approval; released v1 errors are untouched.

Proposed error envelope contains **exactly three keys**: allowlisted static `code`, static safe `message`, and bounded server-issued `correlation_id`. **No field references** are included (they would violate the closed three-key schema); no source excerpts, credentials, paths, document titles, reflected values, tokens or stack traces.

A future mutation contract (Candidate B) would require optimistic revision preconditions and canonical request/decision digests, idempotency for retries, strict decision ordering, explicit supersession/revocation, immutable audit history and safe concurrent state transitions. It must not claim durable storage, atomic filesystem rollback or real Human authentication from the existing in-memory synthetic system.

## 7. Authentication, authorization, storage and data handling — unresolved

Current synthetic actor `SYNTHETIC_REVIEWER_001` is a test-only convention, **not an authenticated user, role-based access control or legal attestation**. Human authorized v0.1.3 **drafting** of the precise same-process capability/bootstrap and network threat assumptions in §4, but has **NOT finally frozen or accepted these controls as implemented security**. Only an isolated trusted same-process synthetic ASGI/TestClient proof-of-contract is proposed; **any separate CLI process, desktop browser, OS IPC, production/remote HTTP surface or real user is STOP** pending distinct security decisions. No GET route may be implemented under the present task authorization. Any hypothetical externally accessible endpoint (currently **NOT AUTHORIZED**) would additionally need:
- Who may create/list/read a document/session, and how ownership is proved; default-deny in the absence of an approved mechanism.
- Who can inspect source/evidence vs submit/revoke Human decisions; user/tenant/resource ACL, audit and revocation.
- Where session/revision/decision state lives; retention, deletion, backups, concurrency, privacy and data classification.
- Local-only vs internal network vs public ingress, rate limits, abuse prevention, CORS/CSRF, authentication/session fixation.
- Secret/HMAC key custody and rotation, server-side canonical snapshots and source protection.
- Whether source data may ever include real or confidential papers and whether any AI provider is authorized (both currently **NO**).
- Whether any runtime/budget or deployment change is permitted (currently **NO**).

A feature flag, synthetic actor and untrusted proxy header are not authentication/authorization. The detailed **v0.1.3 candidate** uses 256-bit transient bearer secrets, ephemeral same-process keyed verifiers, 15-minute capability TTL, maximum 60-minute synthetic session TTL and 50-session capacity, pending independent review and final Human freeze. These are **not implemented settings**, cannot be safely distributed across separate processes without another decision, and give no real-user security guarantee. Session retirement/revocation and key rotation are trusted non-GET lifecycle operations; no DB or persistent audit is selected. No public route or real-user workflow may be inferred.

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
| AC-23 | LOW L-01 resolved: version solely from `/api/v2` namespace; response `api_version="2.0.0"`; NO client version negotiation | `?version`, `X-API-Version`, `Accept-Version`, undefined `unsupported_api_version` or accidental pre-auth 422 |
| AC-24 | In-process trust-only bootstrap and no public/cross-process mint; bearer 32 CSPRNG bytes, canonical 43-char base64url | Browser/second process receives bearer, HTTP mint, bearer in URL/cookie/response/log, noncanonical encoding or duplicate Authorization |
| AC-25 | Ephemeral per-process 32-byte verifier key, HMAC-SHA256 derived verifier, constant-time checks and fail-closed restart/revocation | Forked/multiworker state, plaintext token retention, leaked key, compare timing, valid old token after restart/revision/expiry |
| AC-26 | Literal loopback host/port, peer validation, no forwarded headers/browser Origin/CORS; pre-router auth privacy | `localhost` DNS rebinding, duplicate Host, foreign socket peer, proxy spoofing, unwanted Origin/OPTIONS, typed FastAPI early 422 oracle |
| AC-27 | Strict schema/request regex, no client version header/param, no UNKNOWN authority promotion | Repeated malformed query, bad revision/limit, extra response keys, positive Claims, status inconsistency, unknown `api_version` |
| AC-28 | Cursor is integrity-protected, synthetic-safe, non-confidential base64url; bearer remains independent; GET stateless/read-only | Decoded cursor contains source IDs/hash/secret, old snapshot, cross-scope replay, page-size mismatch, GET writes cursor store |
| AC-29 | Capability 900s and session 3600s monotonic expiry; 50 process sessions, trusted lifecycle cleanup outside GET | Clock rollback acceptance, boundary equality, capacity bypass, client-induced eviction/secret rotation/cleanup on GET |

Evidence gates for a **future** implementation: targeted offline tests, full relevant P2-002…P2-006 + AI-CONV-002/003 regression, security/negative coverage, supported schema validation, source/contract hashes, baseline v1 API regression, independent fixed-SHA reviewer PASS, exact-head CI SUCCESS, Render OFF/no verify, and protected merge with exact-main postmerge CI. These are not acceptance evidence for currently non-existent v2 code.

## 10. Human decision ledger — v0.1.3 finalization-draft PREPARATION approved, NOT FROZEN

**Approval provenance:** [Candidate A policy selection #6207131354](https://github.com/nshaokiet/ai-ip-description-generator/issues/121#issuecomment-6207131354), [v0.1.2 detailed proposal preparation #6208917696](https://github.com/nshaokiet/ai-ip-description-generator/issues/121#issuecomment-6208917696), and [v0.1.3 finalization-draft preparation #6210611707](https://github.com/nshaokiet/ai-ip-description-generator/issues/121#issuecomment-6210611707). All are **limited documentation/review approvals**. Existing [new-session v0.1.2 corrective PASS receipt](https://github.com/nshaokiet/ai-ip-description-generator/pull/122#issuecomment-6210567224) is **historical only** and cannot approve v0.1.3.

| Gate | Human-authorized design direction for this FINALIZATION DRAFT | Still requiring separate explicit Human decision |
|---|---|---|
| **HD-V2-01** | Selected limited Candidate A: synthetic, local-only, informational GET, not B/C | No implementation, external network or real paper authorized |
| **HD-V2-02** | **AUTHORIZED TO SPECIFY:** exactly two GETs, fixed response version `"2.0.0"`, no client negotiation (**L-01 disposition**), strict 8-key status, 5/2-key index, 3-key errors, 404/409/422/500 candidate mappings | **PENDING FINAL WIRE CONTRACT FREEZE:** accept or revise exact schemas/regex/error privacy/Host failure handling after new independent review |
| **HD-V2-03** | **AUTHORIZED TO SPECIFY:** default-OFF flag, literal-loopback peer + Host/Origin/proxy restrictions, same-process CSPRNG bearer HMAC verifier, auth-before-routing | **PENDING FINAL SECURITY FREEZE:** approve same-process restriction, nonce/key custody/revocation, no OS IPC, header privacy and same-user attacker residual risk |
| **HD-V2-04** | **AUTHORIZED TO SPECIFY:** single process in-memory only, 15m capability, 60m session, 50-session cap, monotonic deadlines, no GET-side cleanup | **PENDING FINAL RESOURCE/CONCURRENCY FREEZE** and independent security review; no DB/durable state |
| **HD-V2-05** | **AUTHORIZED TO SPECIFY:** synthetic-safe IDs/digests, limit default 25/max 50, canonical cursor with no source secrets or total count | **PENDING FINAL PRIVACY FREEZE**, including digest allowlist and visible page-position leakage from base64url cursor |
| **HD-V2-06** | **CONFIRMED DISABLED:** product Claims runtime, positive METHOD/PROCESS/COMPOSITION, real-paper Claims and any migration of exact seven-input P2-005/P2-006 provenance | Any changed authority/provenance or positive real paper Claims require separate Human decision |
| **HD-V2-07** | **APPROVED POLICY:** GET informational reads only, no mutations, exports, provider, renderer or public rollout | No code, route, CI/released model or deployment authorized yet |
| **HD-V2-08** | **EXPLICITLY NOT AUTHORIZED:** real/confidential papers, live/paid AI, production/Render, public ingress, Workflow V2/Phase H | Any exception requires separate Human approval |
| **HD-V2-09** | **APPROVED NOW:** archive v0.1.2 byte-identically, prepare/docs-only PR #122 v0.1.3; obtain **NEW exact-SHA independent Gemini 3.8 Flash High STRICT READ-ONLY PASS and exact-HEAD CI SUCCESS** | **PENDING EXPLICIT FINAL Human wire/security FREEZE and later SEPARATE Human implementation authorization**; no automatic Ready/merge/Issue closure |

**Stop condition:** A new reviewer PASS and green CI validate only the *reviewed finalization-draft candidate*. They cannot satisfy the Human freeze requirement. The PR must remain DRAFT until Human separately decides the contract and the normal Workflow V1 merge gates are met. A proposed local TestClient bootstrap is **not** a grant to implement.

## 11. Workflow V1 review, merge and next-task gates

**Specification-only deliverable:** this v0.1.3 Markdown file **plus immutable historical v0.1.0, v0.1.1 and v0.1.2 archives** on the existing documentation-only PR branch, with explicit **POLICY APPROVED / WIRE CONTRACT PROPOSED / NOT FROZEN** status. Documentation may clarify current task references if separately approved, but it must not alter code, tests, schemas, dependencies, FastAPI routing or public contracts.

- Codex/ChatGPT source audit must include actual route prefixes, opt-in feature flag, AI-CONV-001/002/003 and released P2-002…006. Never claim v2 exists.
- Independent **Gemini 3.8 Flash High / Antigravity STRICT READ-ONLY** must inspect exact reviewed SHA, source/line accuracy, unsupported claims, positive/negative ACs, migration, threat model, Human decisions and scope. Report actual model/profile, session/reuse and PASS / REQUEST CHANGES / BLOCKED.
- Before any docs PR merge: require exact-head CI SUCCESS, accurate diff scope, fresh main/head protection and Render `no/off`; resolve review findings and obtain Human policy/freeze decision if a merge would be represented as an **approved/frozen v2 design**. A purely proposed artifact must remain explicitly **PROPOSED** if merged only as a proposal.
- After merge, verify exact-main CI, doc lineage and issue status. Later v2 implementation remains STOP until **separate Human implementation authorization** on approved policy/contracts.
- AI-CONV-003 closeout, AI-CONV-002/#111, GOV-REVIEWER-001/#113, BLK-003, EVAL-001 product runtime, V2/Phase H and provider/production decisions remain independent; do not turn one into another's approval.

**Disposition as of 2026-10-16:** Human approved Candidate A policy, detailed v0.1.2 drafting and **preparation of this v0.1.3 finalization draft only**. L-01 is dispositioned as **no client API version negotiation**, pending new fixed-SHA Gemini review and exact-head CI. **Final Human wire/security FREEZE and separate implementation authorization remain PENDING**; no backend/API route/schema changed, no runtime Claims, real source/provider or deployment authorized.
