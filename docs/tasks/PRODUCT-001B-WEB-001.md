# PRODUCT-001B-WEB-001 — browser contract and implementation gates

| Field | Value |
|---|---|
| Version / date / author | 0.1.0 / 2026-11-05 Asia/Saigon / Codex |
| Task / resume keyword | PRODUCT-001B-WEB-001 / RESUME-PRODUCT-001B-WEB-001 |
| Status | DRAFT FOR HUMAN SECURITY/DESIGN REVIEW; NOT FROZEN; RUNTIME NOT STARTED |
| Authorization | Human START-PRODUCT-001B-WEB-001: verify foundation, reconcile dependencies and prepare contract; phase4 expressly conditional on security design, fixture admission and implementation-scope approval |
| Workflow | V1; MCP registration/lease UNVERIFIED, no enrollment/state fabricated |
| Parent contract | [PRODUCT-001B0.2.0](PRODUCT-001B-trusted-local-review-presenter.md); this is its concrete web increment, not a second product pipeline |
| Planning base | Foundation151 `bc991c7ad2f42635b523ecff24daf77a3027fb93`, tree `197f59197aaa8cf8673e70cf5cc394e393c4ff86` |
| Accepted code baseline | main `478f7d30b6c89f7d4dc8cade2d8a9365b974ec75`, tree `b440f3021c39c9504cd49753dae63acfc1a3a0ed` |
| Evidence | [Dated source/CI receipt](../qa/product-001b-web-001-foundation-20261105.json) |

The product remains a Next.js + FastAPI WEBSITE: upload PDF/DOCX → process →
source-linked review → validated revision → separate Human decisions → validate
→ render/download four USPTO v2 DRAFT files. No live AI, confidential paper,
terminal-first product, duplicate pipeline/schema/renderer or deployment.

## 1. Foundation and dependency readiness

| Dependency | Implemented / accepted evidence | Remaining gate and disposition |
|---|---|---|
| DEP-001/147 | MERGED; main478f7d3 has reviewed4c30d37 tree unchanged; exact-main [CI42038735811](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/42038735811) SUCCESS | Read actual refs/CI again before integration; no security waiver |
| Foundation151 | bc991c7 is normal merge of e2f4b7b and accepted main478f7d3. [CI42041866712 attempt2](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/42041866712/attempts/2) SUCCESS; artifact13424296589 downloaded/digest/content checked: full/prod0, security73+2PASS | Exact-bc991c7 independent Gemini review PENDING; zero native reviews and no report found in checked local backup/GitHub handoff. Keep Draft; old00f3833 PASS is not current review. No merge in this task unless actual gates become evidenced |
| PRODUCT-001A/149 | Candidate `cf9097fda4688db08fd505e21fcbf3c0e53a9d5c` contains OfflineSyntheticWorkflow, C1 bound-review extension and synthetic fixture/test package | OPEN/DRAFT, conflicting with current main; hosted41848393889 FAILURE, native reviews0; external report provenance remains limited per [reconciliation](PRODUCT-001A-review-reconciliation.md). Not accepted/on main. No automatic merge/cherry-pick |
| C2 REVISION-004/146 | Candidate `29daeb208f7736a448297f699e674192c124c7da`; Human accepted OptionA architecture and authorized specification-only integration | OPEN/DRAFT/CONFLICTING, CI40078806412 FAILURE. Architecture acceptance did not authorize application code or fixtures. Same-process/no-browser boundary remains; B is a separately approved transport increment, not silent C2 amendment |
| C1 core | `backend/app/services/preapi_source_custody.py` on main: trusted same-process upload/revise/review/render/download, original/source/digest checks, idle1800s/absolute7200s | Core exists; browser auth/owner binding and A's custody_review.py/get_review_projection additions are not supplied by main alone. Broader C1 governance closeout remains distinct from current security-main CI success |
| P2-005/P2-006 | `uspto_document_package.py`, package validation and `uspto_offline_renderer.py` on main; seven-original validation and four exact filenames/MIME | Internal/synthetic callable services, not a browser authorization boundary or semantic/filing acceptance |
| Existing Next/FastAPI v1 | Existing UploadPanel, ResultWorkspace, AnalysisView, EvidenceCard, ReviewItemsView, v1 document/process/validate/single-DOCX routes; opt-in local orchestration | v1 routes do not provide B's per-session custody-bound four-file flow. Reuse components/services, keep old modes working |
| Public synthetic export demo | Existing SyntheticUSPTOExports and static sample capability/exports | Fixed representative output only. Cannot satisfy two-source upload-to-export acceptance |
| PR150 | d88201a5 remains OPEN/DRAFT; no edits/closure/merge | Preserve other-agent proposal;151 remains preferred foundation |

Both main and151 hosted SUCCESS are CI evidence, not new independent-review
verdicts. Attempt1 of151's42041866712 failed HTTP401 from the pinned snapshot;
attempt2 succeeded unchanged after a separately Human-directed single retry.
Preserve that failure; do not rename it HTTP503. Older42034588440 did fail503.

## 2. Approved now, proposed, blocked

| Work | Authority / state |
|---|---|
| Read-only verification, source comparison, dependency matrix, DTO/security/fixture proposals, documentation commit/Draft handoff | Authorized by START-PRODUCT-001B-WEB-001; performed in this documentary increment |
| Foundation151 integration/closeout | Conditional: actual fixed-bc991c7 review plus scope/CI/governance/expected-head gates; currently review missing |
| Security design/transport/owner/session/data-lifecycle changes | PROPOSED below; Human approval required by phase4 and AGENTS§19 |
| Fixture generation/admission/use for B | Proposed identities/content below; B admission not granted, second-content bytes/hash absent; no fixture materialized by this task |
| Runtime/auth/routes/UI implementation | BLOCKED until D01–D07 decisions, frozen spec and accepted dependencies or explicitly reviewed dependent integration |
| 146/149 merge | Not authorized merely by this task; each exact-SHA review/CI/provenance/authorization gate remains |
| Provider/real-data/persistence/deployment/Claims authority | Excluded; provider budget0, semantic acceptance NOT_DETERMINED, production readinessNO |

This version is a concrete proposed contract, not an approved freeze. Do not
label its status FROZEN until Human accepts the exact version/commit and fixture
admission record. Later content changes require versioned supersession/review.

## 3. Proposed transport, session and authorization design (D01–D03)

### 3.1 Host configuration and login

Propose one operator, one process, volatile state, one configured browser origin:
`https://localhost:3443`. TLS must be configured/tested before use; no browser HTTP
exception is proposed. Next is a same-origin thin server proxy to a loopback-only
FastAPI opt-in factory; public/default app and Render remain unchanged. Direct
backend product transport is denied without a host-configured, server-only proxy
credential, stripped/replaced by Next and never forwarded to browser/logs.
Upstream URL is fixed configuration, never a request parameter. No external IdP,
new service or package is proposed. If existing tools cannot meet approved TLS
setup without new dependency, stop and obtain a concrete scope decision.

The trusted host supplies `authorize_browser_login(prelogin_binding)` through an
out-of-band local operator-authentication channel. Proposed pairing: browser gets
a short-lived non-authoritative pairing selector and HttpOnly prelogin cookie;
the authenticated local operator confirms that exact binding in the host control
channel. Browser polling cannot approve itself. No public admin/login-approval
endpoint, request-supplied actor, C1 token or AI-CONV capability authenticates it.
The exact host authenticator/control-channel deployment needs Human approval;
unconfigured/unavailable authorizer denies login. Operator setup is administration,
not a terminal replacement for the browser product journey.

Prelogin lifetime60s, maximum2 pending bindings; successful login rotates/discards
prelogin state and creates a new independent 256-bit random browser session.
Cookies: `__Host-aiip_prelogin` / `__Host-aiip_web`, Secure, HttpOnly,
SameSite=Strict, Path=/, no Domain. Authenticated session absolute lifetime1800s;
reads never renew it. Cookie Max-Age follows the server deadline. Expiry is always
checked server-side, independent of browser cookie persistence. CSRF tokens are
distinct random256-bit synchronizer tokens, held only in browser memory, rotated
at login; no credentials in URL/localStorage/sessionStorage or bundles.

### 3.2 Request policy

Exact configured Host and source Origin are checked on every mutation, including
login/upload/logout. Reject absent/foreign/null/duplicate Origin for mutations;
no Referer-only fallback in this proposed mode. Verify a synchronizer token in
`X-AIIP-CSRF` against the correct prelogin/authenticated server session. Require
same-origin Fetch Metadata where present; SameSite/CORS alone is not sufficient.
Reads/downloads require owner/session and exact Host; require same-origin fetch
metadata or matching Origin when sent, rejecting foreign/null Origin. Downloads
use authenticated fetch; no cross-origin credentialed CORS or wildcard allowlist.
Next strips untrusted forwarding/internal-auth headers and forwards only the
configured mapping; FastAPI validates the private proxy transport separately.

Cookie session lookup determines the sole principal and owns one
OfflineSyntheticWorkflow instance. Its invocation callback checks the exact
request principal AND session generation, never merely any logged-in user.
Every document/view/operation/artifact selector is scoped to this owner/session;
possession is not authority. Two logins create distinct scopes even for one local
operator. No client owner/actor/context/provider/config/runtime/fixture allowlist
field is trusted. Opaque browser selectors are independent random identifiers,
never serialized ProductSessionRef, registry/C1/coordinator IDs or capabilities.

All responses use Cache-Control:no-store and X-Content-Type-Options:nosniff;
no-store Next fetch/server rendering, no service-worker caching. Source strings
render as text; no dangerouslySetInnerHTML, executable Markdown or source URLs.
Use CSP/frame restrictions compatible with the approved local mode; no source
content can navigate, submit commands or approve decisions.

Design references checked 2026-11-05: host cookie prefix restrictions in
[MDN Set-Cookie](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie),
and stateful synchronizer-token/Origin guidance in
[OWASP CSRF prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html).
These support design choices, not project authorization or test results.

## 4. Proposed resource and lifecycle policy (D03)

| Boundary | Proposed hard limit / behavior |
|---|---|
| Source upload | Exactly1 PDF or DOCX, no text fields; file≤10MiB, total multipart≤10MiB+64KiB; stream64KiB chunks; reject before unbounded buffering |
| Existing parser limits | Preserve APP-00110MiB/50PDFpages; DOCX2048entries/100MiBtotal expanded/50MiBentry/ratio1000; reject encrypted/macro/external relationships/no-text/unsupported sources using existing validator |
| Login/document capacity | 2 active browser sessions globally;4 A documents per session,8 globally; reject capacity before allocating more state |
| Retained review data | A's existing complete-original limits:8MiB serialized,100000nodes,depth64, individual string≤1MiB; no truncation for approval. Aggregate retained payload accounting≤128MiB |
| Storage | Aggregate source bytes≤80MiB, owned output staging+committed files≤256MiB; reject/rollback on capacity, no adoption of arbitrary directories |
| Requests | At most2 active requests/session,1 CPU/parse/render operation globally; reads60/min/session, mutations12/min/session, process/render2/min/session;429 safe response with Retry-After |
| JSON | Mutation JSON≤64KiB; proposed text-edit command≤32edits, each replacement≤4096UTF8bytes; reject excess before decode/derivation |
| Deadlines | Process60s, validate30s, render120s, request upload30s; no late publication after timeout/logout/restart/revision change |
| Existing custody | Keep C1 idle1800s/absolute7200s. Effective access expires at minimum of browser, custody and source-storage deadlines; browser login cannot extend custody/storage |
| Restart/logout/expiry | Revoke server authority immediately; discard selectors/CSRF/view/manifest; abort owned A sessions and clean owned storage. Refresh cannot reconstruct decisions from browser state |

Deadline enforcement is a design obligation, not an existing A guarantee. Heavy
work must run with a bounded resource/operation fence and a cancellation strategy
that can terminate/reap its worker before releasing capacity. Worker executes
existing parser/renderer functions on server-owned inputs, not a new pipeline;
authority/commit stays in the parent and is checked again before publication.
Propose one stdlib multiprocessing spawn worker per heavy operation, one globally;
parent sends only the bounded read-only inputs/owned staging path needed by the
existing parsing/render function, never session callbacks or capabilities. Parent
checks the deadline, terminates/kills and joins the child on timeout, then checks
source hashes/session generation/current revision before atomic publication.
Supported-host OS memory-limit mechanism and512MiB worker-memory ceiling are
explicit D03 decisions still needing design review; unsupported enforcement must
deny enabling this mode, not silently fall back to an unbounded thread.
Specify/review the exact local worker mechanism before implementation; if it
requires changes outside approved B adapter scope, stop/re-plan. A thread timeout
alone does not prove termination or resource cleanup. No external queue/service.

Revoke login in the session registry independently of a busy A lock. Increment an
operation generation so late work cannot publish; cleanup may finish later, but
access stays revoked. Cleanup failure is reported/quarantined, not silently
accepted. Only positively service-owned paths may be removed, with no symlink
following/path escape. Existing source-storage TTL is not silently extended.

## 5. Proposed versioned browser routes and DTOs

Browser prefix `/api/product-web/v1`; server-only FastAPI prefix
`/internal/product-web/v1` through the fixed Next mapping. These are proposed,
default OFF, not registered by this documentary PR. Every JSON object is strict
(`extra=forbid` recursively for transport objects); protocol version is
`product-web/1.0.0`. Existing canonical business schemas remain authoritative.

| Method / relative route | Request | Success | Required guard / side effect |
|---|---|---|---|
| GET `/session/bootstrap` | none |200 BootstrapDTO; prelogin cookie | Exact Host/local transport; bounded anonymous pairing/CSRF bootstrap only, no product access/review/render |
| POST `/session` | LoginDTO |200 SessionDTO; rotated auth cookie | Prelogin cookie/CSRF/Origin plus out-of-band host approval of exact pairing binding; otherwise403 |
| GET `/session` | none |200 SessionDTO without rotating tokens | Authenticated cookie/owner; no custody TTL renewal |
| DELETE `/session` | `{}` |204, cookies cleared | Auth/CSRF/Origin; revoke all owned documents/work before cleanup |
| GET `/documents` | none |200 `{documents:DocumentDTO[]}` | Only current owner, max4 |
| POST `/documents` | multipart `file` only |201 DocumentDTO, revision0/stateUPLOADED | Auth/CSRF/Origin, resource guard, existing storage/validator/registry; server computes immutable SHA and verifies admitted bytes |
| POST `/documents/{document}/process` | VersionDTO, expected_revision0 |200 DocumentDTO, stateREADY/revision1 | Owner/current upload, actual registry/C1/A start with pinned synthetic runtime; no provider/network |
| GET `/documents/{document}` | none |200 DocumentDTO | Owner/session/expiry/current authority, safe status only |
| GET `/documents/{document}/review` | none |200 ReviewDTO | Verify source/original digests/current revision; complete inert projection; no approval/TTL refresh |
| POST `/documents/{document}/revisions` | EditDTO |200 DocumentDTO for new revision | Owner/CSRF/current view+revision; apply typed edit to retained analysis, canonical validate then A.revise; invalidate all prior decisions/validation/export |
| POST `/documents/{document}/content-review` | DecisionDTO |200 ReviewStateDTO | Affirmative content decision on exact presented view; actor/context server-derived |
| POST `/documents/{document}/claims-acknowledgment` | DecisionDTO |200 ReviewStateDTO | Separate affirmative incomplete-Claims decision after content review, exact same current view; never batch/auto-default |
| POST `/documents/{document}/validate` | VersionViewDTO |200 ValidationDTO | Recheck owner/source/view/all originals; validate without implicitly approving/rendering |
| POST `/documents/{document}/render` | VersionViewDTO |200 ExportDTO | Current positive validation AND content decision AND incomplete-Claims acknowledgment if required; A/C1/P2 recheck all invariants and atomically render all4 |
| GET `/documents/{document}/artifacts/{artifact}` | none |200 binary, exact MIME/disposition | Owner/session/current revision/source/private manifest/expiry/path/digests rechecked immediately before bytes; no rendering |
| DELETE `/documents/{document}` | VersionDTO |204 | Owner/CSRF/Origin/current revision; revoke then abort/owned cleanup |

No GET approves, edits or initiates rendering. Bootstrap allocates only bounded
anonymous login state; it grants no product authority. Retry of a decision/render
must re-check current revision and explicit action; a network failure never means
approval succeeded. UI refetches safe status after ambiguous outcomes.

### 5.1 Exact transport shapes

Types below are proposed transport wrappers, not copies of P2/C1 schemas.
`selector` is base64url encoding of32 random bytes; `sha256` is64 lowercase hex;
`revision` is integer≥0; timestamps are UTC RFC3339. No secret/internal value is
accepted just because it is a syntactically valid selector/hash.

```text
BootstrapDTO = {schema_version, pairing_id:selector, csrf_token:selector,
                expires_in_seconds:60}
LoginDTO = {schema_version, pairing_id:selector}
SessionDTO = {schema_version, authenticated:true, csrf_token:selector,
              expires_at:timestamp, mode:"SYNTHETIC_DRAFT", document_count:int[0..4]}
DocumentDTO = {schema_version, document:selector, revision, source:{file_name:string,
               media_type:PDF|DOCX_MIME, size_bytes:int>0, sha256},
               state:UPLOADED|READY|REVIEWED|VALIDATED|RENDERED|FAILED,
               expires_at:timestamp, synthetic_draft:true, filing_ready:false}
VersionDTO = {schema_version, expected_revision:revision}
VersionViewDTO = {schema_version, expected_revision:revision, view:selector}
EditDTO = {schema_version, expected_revision:revision, view:selector,
           edits:[{path:string, value:string}]}    # 1..32, replace only
DecisionDTO = {schema_version, expected_revision:revision, view:selector,
               acknowledge:true}                 # false/missing never approves
ReviewStateDTO = {schema_version, document:selector, revision, view:selector,
                  content_reviewed:bool, claims_incomplete:bool,
                  claims_acknowledged:bool, validated:bool, export_ready:bool}
ValidationDTO = {schema_version, document:selector, revision, valid:true,
                 issues:[{code:IssueCode, pointer:safe_public_pointer}],
                 synthetic_draft:true, filing_ready:false}
PublicArtifact = {artifact:selector, filename:EXACT_FILE_ENUM,
                  media_type:EXACT_MIME_ENUM, size_bytes:int>0, sha256}
ExportDTO = {schema_version, document:selector, revision, source_sha256:sha256,
             artifacts:PublicArtifact[exactly4 distinct],
             synthetic_draft:true, filing_ready:false, human_review_required:true}
```

IssueCode is the closed set SCHEMA_INVALID, GROUNDING_INVALID, SOURCE_CHANGED,
PACKAGE_INVALID, CLAIMS_INCOMPLETE, REVIEW_MISSING, RESOURCE_LIMIT. Public issue
pointers are server-produced canonical JSON Pointers into the safe DTO, at most256
characters, never echoed arbitrary client keys/values. Positive validation returns
valid=true; negative package validation returns422 VALIDATION_FAILED, leaves
validated=false and creates no export.

All keys in a listed shape are required; absent optional content occurs only
inside the canonical JSON original values where absent/null must remain distinct.
`schema_version` is the literal `product-web/1.0.0`. Invalid enum/types/extra keys
fail closed. Binary success has no JSON envelope. No client-supplied actor,
context, owner, source digest, private manifest hash, configuration, original
records or arbitrary server path can replace server state.

### 5.2 Complete review and edit contract

`ReviewDTO={schema_version,document,revision,source_sha256,view,view_sha256,
records,authority_redactions,review_state,synthetic_draft:true,filing_ready:false}`.
`records` has exactly the seven C1 PROVENANCE_KEYS:
`source_envelope`, `structured_analysis`, `reconstruction`, `specification`,
`p2_003_generation_config`, `supported_claims`, `p2_004_generation_config`.
Each value is `{public_value:JSONValue, public_sha256:sha256}`; `review_state`
uses ReviewStateDTO. `view_sha256` binds this complete public view only. Server
retains exact seven original objects/digests plus the private A snapshot hash.
An independent random public view selector maps to that exact private revision/
snapshot; no A/C1 authority identity or revision-token hash is serialized.

Build an explicit field mapping: transform registry document references into
per-document public aliases consistently in document_metadata/evidence; omit
internal coordinator/custody/owner/ref/token/path/callback/manifest authority
fields. Report every such authority-only redaction as
`{pointer:safe_public_pointer,reason:"SERVER_AUTHORITY_ONLY"}` without its value.
Preserve all business text, evidence IDs/types/locators/excerpts, arrays/order,
null/absent distinctions, warnings, missing/conflict markers and Claims status.
Metadata namespace remapping is explicit, not silent truncation. Any unclassified
field or inability to represent the complete admitted business content safely
rejects the review and disables decisions. Raw source and projection are never
logged. Completeness/redaction inventory is a required pre-freeze design review.

UI shows all seven records and evidence, with safe pagination/expanders. It must
load the full bounded view before enabling either decision; server binds decisions
to that view, without claiming to prove a Human actually read every character.
No source-driven commands, links or stored browser decisions.

Initial proposed edit allowlist: existing `/title_candidates/<index>/title` and
`/title_candidates/<index>/rationale` string leaves in retained structured_analysis.
No array insertion/removal, arbitrary JSON Patch, prototype keys, escaped pointer
aliases, metadata/evidence/grounding/Claims/config edits or replacement originals.
This narrow first increment is proposed for Human scope acceptance, not silently
assumed sufficient for broader author-answer editing. Server checks exact numeric
index/canonical pointer, applies replacements to its own copy, validates existing
canonical schema/grounding rules then calls A.revise with the full validated
analysis. Evidence/grounding labels cannot be upgraded; re-review is mandatory.
Editing does not establish semantic/source-fact acceptance. No-op/invalid edit
leaves current revision/decisions unchanged; successful edit invalidates every
prior view/decision/validation/manifest/download binding. Two-tab stale edits409.

### 5.3 Error schema

All failures return `{schema_version,error:{code,message,correlation_id,
issues:[{code,pointer}]}}`; message from fixed safe text, correlation_id random,
no body/secret/path/ID echo. No framework validation traceback/input dump.

| Status | Codes / semantics |
|---|---|
|400 | BAD_REQUEST, UNSUPPORTED_QUERY; malformed JSON/header ambiguity |
|401 | SESSION_UNAVAILABLE; missing/expired/revoked auth, restart |
|403 | ORIGIN_REJECTED, CSRF_REJECTED, LOGIN_NOT_APPROVED; no details about another owner |
|404 | RESOURCE_UNAVAILABLE; same response for missing/foreign document/view/artifact |
|409 | STALE_REVISION, REVIEW_REQUIRED, CLAIMS_ACK_REQUIRED, VALIDATION_REQUIRED, OPERATION_BUSY |
|413 | RESOURCE_LIMIT; request/projection/resource admission overflow |
|415 | UNSUPPORTED_MEDIA_TYPE |
|422 | SOURCE_NOT_ADMITTED, DOCUMENT_INVALID, EDIT_INVALID, VALIDATION_FAILED; safe field pointers only |
|429 | CAPACITY, RATE_LIMIT; fixed Retry-After |
|500 | OPERATION_FAILED, CLEANUP_FAILED; revoked access stays revoked |
|504 | OPERATION_TIMEOUT; fenced/reaped result cannot publish/export |

Do not reveal whether a foreign resource exists. Render/validation returning a
negative business result never creates approval or advertises artifacts.

## 6. Validation and exact four-artifact contract (D04)

A's current public methods are start/review/acknowledge/revise/render/download/
abort. A separate validate-without-render method is **absent**. Proposed additive
public facade/C1 validation command must call the existing P2-005 assembler and
validator under the same current-owner/revision/original checks and lock/fence;
it must not use private `_get` from HTTP code or copy assembly logic. Retain only
a server-owned validation receipt bound to current revision/private snapshot.
Render still revalidates; a prior positive result never authorizes stale export.
This additive service change needs the approved implementation scope after A
acceptance or explicit dependent integration; no A code is changed here.

| Filename | MIME |
|---|---|
| B2_REFERENCE_PREVIEW.pdf | application/pdf |
| B2_REFERENCE_PREVIEW.docx | application/vnd.openxmlformats-officedocument.wordprocessingml.document |
| USPTO_APPLICATION_DRAFT.pdf | application/pdf |
| USPTO_APPLICATION_DRAFT.docx | application/vnd.openxmlformats-officedocument.wordprocessingml.document |

Use existing renderer FILES and custody MIME, not a duplicated enum with different
semantics. All four must be nonempty valid PDF/DOCX bytes; verify signatures,
package parseability, size and SHA-256. Private A manifest includes source,
document/custody/revision/private snapshot and artifact digests; retain/recheck it
server-side. Public artifact selectors map to the current private manifest and
exact filename, never a path/query token. Check complete bundle at render and
each download, including missing/symlink/tampered peer files, source rehash and
all seven-original digests. No partial bundle advertised. On corruption revoke
export and require fresh valid render; do not serve cached bytes. Content-Disposition
uses fixed ASCII allowlisted filename; no ranges/cache/conditional304 in increment1.

Every view/output remains DRAFT, synthetic_draft=true, filing_ready=false,
Human-review-required. Content approval and incomplete-Claims acknowledgment
are distinct actions, not patentability, semantic, legal or filing acceptance.

## 7. Fixture admission proposal (D05) — not materialized/approved

| Proposed source | Distinct content / identity | Admission state |
|---|---|---|
| PDF-A: controller | Existing A controller.pdf candidate:1015bytes, SHA256 `9bc8d4e20b2b88d2df0780294069e048b96c09a22a7012baa1efe5ba7f523975`; known A fixture policy says REVIEW_PENDING_NOT_C2_PILOT_APPROVAL | Candidate only, not B/C2 admission |
| DOCX-B: membrane flow separator | Proposed newly authored synthetic separation module with membrane/feed/collection terms and fabricated clearly labeled synthetic parameters; technically different from controller actuator/sensor feedback content | Bytes/size/hash/generator provenance PENDING, no file created or used here |

Existing controller.pdf/controller.docx variants of one source do not satisfy
two-content proof. Before fixture use, materialize candidate bytes only within
authorized scope, review provenance/rights/synthetic labels and final generators,
record exact name/MIME/size/hash and approve both identities. Constructor-pinned
allowlist only; request may not manufacture admission. Offline extraction runtime
must derive source-specific fixture analysis from the actual verified envelope,
check registered source hash and evidence IDs/locators, and refuse unknown bytes.
Never return the public fixed representative P2 sample for both documents.
Output-content assertions must distinguish controller markers from membrane
markers, preserve their source digest and show the approved edit in the new
revision. This remains synthetic test behavior, not arbitrary-paper AI extraction.

## 8. Implementation slices and concrete module plan (D06)

| Order / slice | Existing or proposed paths | Work after gates |
|---|---|---|
| B0 dependency admission | PR151/149/146, their task/receipt records | Accept each applicable review/CI/provenance/scope disposition independently; do not merge unrelated PRs as a bypass |
| B1 session/transport | Proposed backend/app/api/product_web.py, backend/app/services/product_web_sessions.py; opt-in wiring in backend/app/main.py; proposed frontend/src/app/api/product-web/v1/[...segments]/route.ts | Strict DTO/error mapping, Host/Origin/CSRF/login/owner/capacity; no public/default route activation. Existing auth/config policy changes only after D01–D03 |
| B2 orchestration bridge | A's backend/app/services/product_synthetic_workflow.py and custody_review.py after acceptance; main preapi_source_custody.py, document_storage.py, document_registry.py, document_parsing.py | Reuse start/review/revise/ack/render/download; additive validate facade, safe public mapping, operation fencing/owned cleanup; no duplicate extraction/assembly/render |
| B3 request models/client | Proposed backend/app/schemas/product_web.py; existing frontend/src/lib/types/contracts.ts and frontend/src/lib/api/client.ts (or adjacent productWeb.ts) | Versioned transport wrappers referencing canonical business validation; retain v1/demo contracts, derive/reconcile client types from admitted API schema |
| B4 review UI | Proposed frontend/src/app/product-web/page.tsx; reuse/adapt existing UploadPanel, WorkflowProgress, AnalysisView, EvidenceCard, GroundingBadge, ReviewItemsView/ResultWorkspace | Safe seven-record/source navigator, narrow typed editor, separate explicit decision controls, validation/export state and stale/logout/restart UX; no fixed-demo output substitution |
| B5 resource execution | Proposed backend/app/services/product_web_operations.py plus minimal approved existing-service hooks | Bounded resource worker/fence, no late commit, immediate session revoke and verified owned cleanup; exact mechanism reviewed before code |
| B6 tests/fixtures | Proposed tests/backend/test_product_web_*.py, tests/fixtures/product-web/v1.0.0/manifest.json and admitted bytes; proposed frontend/tests/product-web.spec.ts (align existing test discovery before implementation) | W01–W12 and targeted negative cases below; existing A/C1/v1/P2/CI remain required |

No new package/service/provider, business schema, Claims text policy or renderer
is authorized by this plan. File names in proposed rows are not claimed to exist.

## 9. Acceptance and test matrix — PLANNED / NOT RUN

| B0.2 AC | Required proof / cases |
|---|---|
| W01 | Explicit Human admission of two actual byte identities with distinct technical content; upload/MIME/hash/source registry/C1 agreement; reject different/altered bytes |
| W02 | Real Chromium UI for each PDF-A/DOCX-B: upload→process→inspect7records→accepted edit→re-review→separate Claims acknowledgment if required→validate→render→download4. Parse all8files with PDF/DOCX parsers; distinguish technical markers/source/revision/hash/MIME/size, no fixed sample substitution |
| W03 | Full business-field inventory/order/null/absent/evidence locators survives; classified authority fields only remapped/redacted; XSS/HTML/Markdown/URL/prototype payloads inert; incomplete view cannot approve |
| W04 | Unreviewed render denied; content decision cannot satisfy incomplete-Claims acknowledgment; false/missing/refresh/GET/Enter cannot approve; actor server-derived |
| W05 | Valid edit rotates revision and invalidates both decisions, validation, manifest, old views/downloads; invalid/no-op edit preserves state; two-tab edit/decision/render races fail stale |
| W06 | Two browser contexts with distinct scopes; foreign document/view/artifact selectors get uniform404; wrong cookie, forged internal IDs/C1/AI-CONV capabilities cannot authenticate |
| W07 | Exact TLS/cookie attributes, host/header ambiguity, missing/null/foreign Origin, missing/wrong CSRF and prelogin/login-CSRF/pairing attacks; direct-backend proxy bypass denied; default routes OFF |
| W08 | Time travel across login/C1 idle/absolute/source expiry between each action; reads do not renew; restart/logout/abort revokes immediately even with busy worker; cleanup failure quarantined and visible |
| W09 | Capture browser requests/responses/errors/DOM/JS bundles/storage and sanitized server logs: no internal handle/ref/token/hash/private path/proxy credential; safe MIME/disposition/no-store |
| W10 | Wrong-source/revision/manifest/artifact bytes, all four digest checks, truncated/absent peer, symlink and traversal/encoded path attempts fail closed; parse actual file bytes |
| W11 | Exact upload/JSON/node/session/global memory/storage/rate/cancellation/deadline caps; hard worker termination/reaping and late-result fence; no hidden queue or partial record/approval |
| W12 | Provider/network tripwire throughout both flows; existing A/C1/v1/P2 regression, security73+2, frontend lint/typecheck/build, main+fixed-source browser/demo checks and required CI/artifact gates; actual independent Security AND Quality verdicts on same final SHA per B0.2.0, with required identities/sessions scoped by governance |

Tests must record failed/skipped/blocked separately. Component tests cannot replace
real upload/browser/render evidence. No test or new review PASS is claimed by this
spec. Never reuse a review after implementation/spec SHA changes.

## 10. Freeze decisions and next gates

| Decision | Concrete Human acceptance needed before affected runtime work |
|---|---|
| D01 | Approve HTTPS localhost3443, fixed loopback proxy trust, no HTTP exception/default-public routes, exact host authenticator/pairing trust channel |
| D02 | Approve cookie/session owner isolation, CSRF/Origin/Host policy, public projection/classified authority mapping and no browser storage of authority |
| D03 | Approve exact caps/TTLs/deadlines, bounded worker/commit fence, revocation/cleanup and volatile restart behavior; no persistence |
| D04 | Approve exact routes/DTO/errors, narrow title/rationale edit allowlist and additive validate-without-render facade; all other originals/config/Claims remain server-owned |
| D05 | Approve concrete fixture materialization/admission procedure and then both final byte identities; second fixture hash currently PENDING |
| D06 | Approve B1–B6 implementation boundaries after accepted A/C1/C2 disposition or an explicitly reviewed dependent-integration plan; no implicit146/149 merge |
| D07 | Freeze exact spec version/commit after independent security/design review and record actual Human authorization reference; implementation review/CI/merge authority stays separately conditional |

First obtain actual bc991c7 foundation review and close its gates without changing
that head merely to update status. This planning branch is stacked on151 to keep
its delta reviewable while preserving151/150. Existing CI triggers PRs to main
only: a stacked PR to151 may have no PR workflow run. Any manual branch CI is
validation only, never a substitute for required main-target PR CI after retarget.
After authorized foundation merge, normal integrate/retarget this branch without
shared-history rewrite, refresh evidence and obtain applicable final-SHA review/CI.

Resume: **RESUME-PRODUCT-001B-WEB-001**. Read this spec, current checkpoint and
Draft handoff; refresh main/151/149/146; keep unapproved runtime work blocked.

Task ID: PRODUCT-001B-WEB-001
Agent: Codex — authorized verification/contract planner; future implementer conditional
Reviewer: Gemini3.8 Flash High / Antigravity STRICT READ-ONLY; actual new model/profile/session/reuse/verdict PENDING
Status: Contract/dependency plan prepared; freeze/runtime/fixture admission/review PENDING, implementation BLOCKED
Version: 0.1.0
Work completed: Verified foundation/main CI/artifact, reconciled actual service gaps and prepared DTO/security/export/module/test contracts
Files affected: This spec, safe QA receipt and documentary README/checkpoint/review handoff only
Evidence checked: AGENTS0.6.2, context/system spec, B0.2.0/web decision, exact151/149/146 sources, live refs/checks/artifact and existing validators/services/UI
Findings: Foundation exact-SHA review absent; A/bound-review extension unmerged; independent validate method absent; C2 scope not browser/fixture approval
Decisions: Human phase4 gates preserved; all new security/fixture/runtime choices proposed, no policy activation
Issues: D01–D07, accepted dependencies, final fixture hashes and final-SHA independent review/required CI
Security impact: Documentation only; no runtime/auth/provider/deploy changes or sensitive evidence publication
Recommended next action: Independent design review plus concrete Human decisions; implement only admitted slice after gate evidence

0.1.0 created 2026-11-05 by Codex. Breaking change: No runtime change;
proposed new transport/security policy requires explicit approval before code.
