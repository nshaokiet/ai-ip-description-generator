# PRODUCT-001B-WEB-001 — browser contract and implementation gates

| Field | Value |
|---|---|
| Version / date / author | 0.1.1 / 2026-11-06 Asia/Saigon / Codex |
| Task / resume keyword | PRODUCT-001B-WEB-001 / RESUME-PRODUCT-001B-WEB-001 |
| Status | DRAFT FOR HUMAN SECURITY/DESIGN REVIEW; NOT FROZEN; RUNTIME NOT STARTED |
| Authorization | Human START-PRODUCT-001B-WEB-001: verify foundation, reconcile dependencies and prepare contract; phase4 expressly conditional on security design, fixture admission and implementation-scope approval |
| Remediation authority | Human REVIEW REMEDIATION; documentary/evidence only, v0.1.1 completed2026-11-06 |
| Review | Prior reported Gemini4 Argon High advisory REQUEST CHANGES; new selected-default Gemini3.8 Flash High review PENDING |
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

### 3.1 Host configuration, offline TLS and pairing (F-WEB-04/07)

Propose one local operator, one parent process with volatile authority, browser
origin `https://localhost:3443`, and a thin same-origin Next proxy to loopback-only
FastAPI. Both B route sets are opt-in and absent from the default/public app and
Render static mode. A fixed backend URL and server-only proxy credential are
host configuration; Next strips/replaces caller internal-auth/forwarding/sample
headers. Browser never receives that credential. No external IdP/package/service.

Proposed `frontend/tools/product-web-local-https.mjs` uses stdlib `node:https`
with an already-provisioned local key/certificate and the installed Next request
handler. TLS material lives outside Git, restricted to the host account; no
mkcert/npm download, automatic CA trust-store change, production key or external
certificate lookup. CI creates an ephemeral localhost/SAN certificate offline
with an already-available approved tool (OpenSSL on the Linux runner); Windows
requires approved pre-provisioned material or that existing tool, never a network
fallback. Missing tool/certificate/key/SAN or unsupported local setup denies B
startup. No `next start --experimental-https` assumption. This wrapper changes
neither deployed Render mode nor the existing v1 HTTP Playwright project.

**Bootstrap is POST, not GET.** `POST /session/bootstrap` is the only unauthenticated
browser mutation exception to synchronizer-token validation: exact Host, exact
Origin, `Sec-Fetch-Site:same-origin`, `X-AIIP-Bootstrap:1`, JSON content type and
private proxy transport are mandatory before allocation. GET/HEAD bootstrap405
and browser prefetch create no state. One live prelogin per cookie binding,
**8 global pending bindings**, absolute TTL60s, allocation rate12/minute globally;
expired bindings are reaped first. Repeating POST with a valid prelogin cookie
returns the same pairing selector/CSRF/deadline and cookie, not a new binding or
extended TTL. Existing authenticated cookie returns its authenticated session
status, never overwrites it. Parallel first requests without a cookie may create
bounded separate bindings; only the current exact cookie can complete its own
pairing. Test this race and 2 concurrent browser contexts; no automatic approval.
Actual2 authenticated sessions/global remains separate from8 pending prelogins.
Exhaustion429 is fail-closed, not a promise to resist a compromised local OS user.

**Out-of-band host control proposal:** add `product_web_host_control.py` and a
pairing-only administrative CLI. Parent binds a local control endpoint outside
HTTP: Linux AF_UNIX in an owner-only0700 directory/socket0600 with peer-UID check;
Windows local named pipe with current-user/logon-SID DACL and remote clients
rejected. Both require a random256-bit control key in an owner-only file/Windows
ACL, never a CLI argument, browser value, log or committed fixture. Framed JSON
messages are at most4KiB, strict fields, HMAC-SHA256 authenticated, contain the
server-instance challenge nonce and exact pairing selector, and are one-use with
at most5s challenge lifetime. Invalid peer/ACL/MAC/replay/expired instance fails.
No Python pickle on this channel and no HTTP admin/approve route.

The local operator compares the current browser pairing selector and invokes
`approve <selector>` through this protected control channel. Parent validates the
exact live prelogin binding and marks it approved, not logged in. A subsequent
browser `POST /session` still needs that binding's HttpOnly cookie, Origin/Host
and synchronizer token; login then rotates/discards prelogin state, consumes the
approval and creates independent session/owner/CSRF values. The selector alone
cannot log in. No request-supplied actor, C1 token or AI-CONV capability is auth.
Host OS-account authentication is the explicit local trust boundary, not a claim
of multi-user production identity. D01 approval of this channel is still needed.

Playwright's trusted host harness owns the protected control endpoint/key and
uses the SAME authenticated IPC approval path for each browser pairing selector.
It cannot send an HTTP approval or select a test-only always-true authorizer.
Negative harness cases omit/wrong-key/replay approvals; two independent browser
contexts receive separate owners. Test control material remains ephemeral.

Cookies `__Host-aiip_prelogin` / `__Host-aiip_web`: Secure, HttpOnly,
SameSite=Strict, Path=/, no Domain. Session is random256-bit, absolute TTL1800s;
reads never renew it. Cookie Max-Age follows the server deadline. Distinct256-bit
CSRF tokens stay in browser memory and rotate at login; no credentials in URLs,
localStorage/sessionStorage/bundles/logs. An unavailable host authorizer/ACL/IPC
or TLS setup denies login. Administration is not a terminal product pipeline.

### 3.2 Request policy

Exact configured Host and source Origin are checked on every mutation, including
login/upload/logout/bootstrap. Only the strictly guarded bootstrap exception in
§3.1 precedes a synchronizer token; every other mutation requires the correct
prelogin or authenticated synchronizer token. Reject absent/foreign/null/duplicate Origin for mutations;
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

## 4. Parent-owned authority, source lifecycle and bounded execution (D03)

### 4.1 Limits and memory semantics

| Boundary | Proposed limit / behavior; no runtime result claimed |
|---|---|
| Upload |1 PDF/DOCX, no text fields; file10MiB, multipart10MiB+64KiB; stream64KiB; existing50PDFpages/DOCX2048entries/100MiBexpanded/50MiBentry/ratio1000 and rejection rules unchanged |
| Capacity |2 authenticated browser sessions,4 A documents/session,8 globally; reserve capacity before work;1 heavy worker globally |
| Parent retained payload |128MiB aggregate accounted retained JSON payload, not a claim that the entire Python/Next process RSS is capped128MiB; existing8MiB originals/100000nodes/depth64/string1MiB limits retained |
| Worker allocation envelope |512MiB via platform-native mechanism below; report the actual measured address-space/committed-memory metric and peak RSS separately, not an unsupported cross-platform physical-RAM equivalence |
| Aggregate B processes | Proposed1536MiB host allocation/charged-memory budget for dedicated B parent+Next+worker, in addition to128MiB payload accounting. Linux delegated cgroupv2 memory.max=1536MiB/swap.max=0; Windows dedicated host Job Object JobMemoryLimit=1536MiB with nested worker512MiB job. Human D03 must accept these new explicit budget/metric semantics; no native test or activation claimed |
| Storage |80MiB pre-process source storage;256MiB total owned output/staging; no second raw-source copy retained after process |
| Requests |2 active requests/session; reads60/min/session, mutations12/min/session, process/render2/min/session;429 with fixed Retry-After |
| JSON/edit |64KiB JSON;1..32 replacements, each4096UTF8bytes maximum plus canonical field limits (title500characters); no arbitrary JSON Patch |
| Deadlines |Upload30s, process60s, validate30s, render120s; parent monotonic deadlines, worker kill/reap and late-result rejection |
| Lifetimes |Browser absolute1800s; existing C1 idle1800s/absolute7200s. Pre-process source expiry applies only while upload exists; post-process min(browser,C1 deadlines), not a deleted-file storage deadline |

| Supported host | Enforced proposed mechanism and required future evidence |
|---|---|
| Linux |Child bootstrap uses `resource.setrlimit(RLIMIT_AS,(512MiB,512MiB))` before heavy imports/data. Read limit back; perform a bounded near/over-limit allocation probe on the supported Python/Ubuntu build. RLIMIT_AS bounds address space, not RSS. Missing resource/RLIMIT_AS/readback/probe failure denies startup |
| Windows |Parent creates a private unnamed Job Object via stdlib ctypes/Win32, sets `JOB_OBJECT_LIMIT_PROCESS_MEMORY` and `JOB_OBJECT_LIMIT_JOB_MEMORY` to512MiB, `JOB_OBJECT_LIMIT_ACTIVE_PROCESS` to1 and `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`. Attach child while its lightweight entry waits at a gate, verify membership/limits then release data/heavy imports. Assignment/nested-job/ACL/readback/probe failure denies startup; no breakaway or unlimited-thread fallback |
| Other/unsupported |B remains OFF. No claim of tested feasibility until native-host probes, valid parse/render below the limit, forced over-limit failure and reaping are evidenced |

Windows Job Object memory is committed virtual memory; Linux RLIMIT_AS is virtual
address space. Neither is mislabeled as a universal resident-RAM cap. Peak RSS and
parent/child totals must also be measured in acceptance; if512MiB is insufficient
for the admitted workload, STOP and obtain a new versioned D03 decision, never
silently increase it. The512MiB envelope and these semantics remain proposed.

### 4.2 Split-phase protocol (F-WEB-01)

Current A.start holds A's RLock across C1 work; current C1 intake uses short global
reservation locks and current C1.render holds a record lock while rendering.
Neither A/C1 instance, lock, registry, storage object, callback, owner/session,
revision token nor manifest can be pickled into a spawn worker. For B choose a
reviewed lightweight stdlib subprocess launcher, not a spawned copy of the ASGI
main module: isolated Python entry imports only its limit/gate code before data
and business imports. No multiprocessing reconstruction of the application is
assumed; request/result transport is bounded bytes/JSON. Child has no
custody authority and cannot set RENDERED. Returning renderer files alone is not
an A/C1 state transition.

The dedicated host launcher places only B service processes in its own group/job;
it never assigns or constrains the IDE/other agents. Lack of delegated cgroup,
nested Job Object support, aggregate enforcement/readback or startup probes
denies B startup. Aggregate charged-memory/commit metrics and observed RSS are
reported separately. The1536MiB proposal is not a measured acceptance result or
authority to allocate/change running services.

Proposed additive APIs (names are design interfaces, not implemented files):
A `prepare_start/complete_start`, `prepare_validate/complete_validate`,
`prepare_render/complete_render`, and cancellation; matching C1 prepare/commit/
cancel hooks and a pure parsing helper split from DocumentPreparationService.
Existing same-process default behavior remains available; HTTP uses only public
admitted facade methods, never private `_get` or an out-of-band renderer bypass.

| Phase | Required parent/worker behavior |
|---|---|
| Prepare, parent |Check exact principal/generation, deadline, source or current originals/revision/review state; reserve one operation/capacity slot; acquire source lease for intake or snapshot complete7originals for validate/render. Build a parent-only ticket containing owner/session-generation, operation epoch, private revision/snapshot/original digests, deadlines and owned staging reservation. Release A/C1 locks before heavy execution; ticket never enters IPC |
| Execute, child |Lightweight fresh-process entry waits for native limits/gate. Receive only bounded inert JSON inputs/configuration and a validated read-only leased source handle/path for parse, or complete originals/package plus owned stage path for render. Reuse existing parser, admitted synthetic runtime and P2 pure functions; no Flask/FastAPI app, auth callback, provider, session state, C1 instance or network. Response via bounded bytes/JSON, never unpickle worker-controlled result objects |
| Validate candidate, parent |Keep the record unpublished. Check result size/type/schema, source identity, actual before/after intake-byte hash, seven original digests and existing canonical/P2 validation. Verify staged four-file set/signatures/sizes/hashes/paths. Do not trust worker-returned owner/revision/state/manifest; parent reconstructs authority. Expensive validation is outside record locks against captured immutable data |
| Commit, parent |Under the ordered short session→A→C1 locks, re-check live generation/operation epoch/deadline/current private revision/originals/reviews, then compare-and-commit. Intake publishes a usable A handle only after source cleanup succeeds; validation records only a bound positive receipt; render atomically promotes its owned staging and sets C1 package/manifest/output_directory/state=RENDERED before A constructs ProductExport. No fabricated RENDERED state or private bypass |
| Cancel/expire/revise/logout |Revoke session/operation epoch in parent registry immediately (no waiting on a heavy A lock); invalidate pending tickets. Signal child, terminate/kill entire worker Job/process and join/reap before releasing worker capacity. Discard late pipe output; clean only owned stage/leased upload as applicable. Failed cleanup leaves access revoked and quarantines storage. Only bounded commit critical sections may precede revoke's linearization |

For Linux's pure worker no descendant process creation is permitted; enforce and
test the process-group/child policy. Windows ActiveProcessLimit1 and job teardown
cover descendants. Parent death must not leave a publishable worker result;
watchdog/parent-channel-close path reaps/exits on Linux, kill-on-job-close on Windows.
Timeout does not release capacity while work continues. Staging promotion is
parent-only; a stale/aborted completion cannot overwrite a newer revision/export.
Authorize/commit lock ordering and callbacks must avoid registry↔A lock inversion.
These hooks/refactors in A/C1/document_parsing are explicit D06 scope, NOT granted
by this documentary patch. Native worker/cancellation feasibility tests are planned,
not implementation PASS.

### 4.3 Two source-lifecycle phases (F-WEB-02)

- **Revision0 / UPLOADED:** raw bytes and metadata live in DocumentStorage and
  DocumentRegistry. Verify hash/MIME/size/admitted identity before parse and
  before intake commit, keep the storage lease during the worker, and check the
  original upload deadline at completion even though a lease defers sweeping.
  DELETE/logout/timeout releases the lease before storage.delete; on_removed
  removes registry metadata. No A session exists yet, so do not call A.abort(ref).
- **Committed revision≥1:** existing C1.commit_upload deletes raw upload after
  retaining its envelope/originals; main wiring uses on_removed=registry.remove.
  A failed deletion revokes custody with CLEANUP_FAILED. Do not retain another raw
  copy in B or require a nonexistent file's hash/deadline on later operations.
  Subsequent checks bind `record.source_sha256` to retained
  `source_envelope.document_metadata.sha256`, exact internal document identity,
  all7 original canonical digests, current revision/reviews and private manifest.
  Output integrity rehashes the actual complete four-file set and returned bytes.

Restart/logout/expiry never reconstruct authority from files, browser storage or
an earlier view. Pre-process TTL and post-process custody TTL are different
lifecycles. Positive validation is not cached source-file ownership. No late
state publication after a cancelled generation's linearization; already-delivered
bytes cannot be recalled, so download authorization/digest checks occur again
immediately before delivery.

Native references for this proposal: [Python3.12 resource](https://docs.python.org/3.12/library/resource.html#resource.RLIMIT_AS),
[Microsoft Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects)
and [extended memory limits](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_extended_limit_information).
They establish API semantics, not tested feasibility or Human approval.
For aggregate Linux accounting see [kernel cgroupv2](https://docs.kernel.org/admin-guide/cgroup-v2.html):
memory.max can be exceeded transiently before reclaim/OOM enforcement. Acceptance
measures the documented controller behavior and cleanup, not an invented strict
instantaneous RSS equivalence across operating systems.

## 5. Proposed versioned browser routes and DTOs

Browser prefix `/api/product-web/v1`; server-only FastAPI prefix
`/internal/product-web/v1` through the fixed Next mapping. These are proposed,
default OFF, not registered by this documentary PR. Every JSON object is strict
(`extra=forbid` recursively for transport objects); protocol version is
`product-web/1.0.0`. Existing canonical business schemas remain authoritative.

| Method / relative route | Request | Success | Required guard / side effect |
|---|---|---|---|
| POST `/session/bootstrap` | `{schema_version}` |200 BootstrapDTO; new/reused prelogin cookie | Exact Host/Origin/Fetch Metadata/custom bootstrap header/private proxy; no prior CSRF required only here;8pending slots, per-cookie idempotency, no product access |
| POST `/session` | LoginDTO |200 SessionDTO; rotated auth cookie | Prelogin cookie/CSRF/Origin plus out-of-band host approval of exact pairing binding; otherwise403 |
| GET `/session` | none |200 SessionDTO without rotating tokens | Authenticated cookie/owner; no custody TTL renewal |
| DELETE `/session` | `{}` |204, cookies cleared | Auth/CSRF/Origin; revoke all owned documents/work before cleanup |
| GET `/documents` | none |200 `{documents:DocumentDTO[]}` | Only current owner, max4 |
| POST `/documents` | multipart `file` only |201 DocumentDTO, revision0/stateUPLOADED | Auth/CSRF/Origin, resource guard, existing storage/validator/registry; server computes immutable SHA and verifies admitted bytes |
| POST `/documents/{document}/process` | VersionDTO, expected_revision0 |200 DocumentDTO, stateREADY/revision1 | Owner/current upload, parent prepare/worker/commit hooks with pinned app-level synthetic runtime, source lease+cleanup; no whole A object in child |
| GET `/documents/{document}` | none |200 DocumentDTO | Owner/session/expiry/current authority, safe status only |
| GET `/documents/{document}/review` | none |200 ReviewDTO | Verify source/original digests/current revision; complete inert projection; no approval/TTL refresh |
| POST `/documents/{document}/revisions` | EditDTO |200 DocumentDTO for new revision | Owner/CSRF/current view+revision; apply admitted typed edit to retained analysis; validate/derive via parent-owned revision hooks, invalidate all prior decisions/validation/export |
| POST `/documents/{document}/content-review` | DecisionDTO |200 ReviewStateDTO | Affirmative content decision on exact presented view; actor/context server-derived |
| POST `/documents/{document}/claims-acknowledgment` | DecisionDTO |200 ReviewStateDTO | Separate affirmative incomplete-Claims decision after content review, exact same current view; never batch/auto-default |
| POST `/documents/{document}/validate` | VersionViewDTO |200 ValidationDTO | Require content review plus incomplete-Claims ack when needed, current view/provenance/7digests; validate without file output or implicit approval |
| POST `/documents/{document}/render` | VersionViewDTO |200 ExportDTO | Current positive validation AND content decision AND incomplete-Claims acknowledgment if required; A/C1/P2 recheck all invariants and atomically render all4 |
| GET `/documents/{document}/artifacts/{artifact}` | none |200 binary, exact MIME/disposition | Owner/session/current revision/retained source provenance/private manifest/expiry/path/all4digests rechecked immediately before bytes; no rendering |
| DELETE `/documents/{document}` | VersionDTO |204 | Owner/CSRF/Origin/current revision; revision0 releases/deletes upload+registry, revision>=1 cancels ticket/aborts owned A custody |

No GET approves, edits, allocates pairing or initiates rendering. POST bootstrap
allocates only bounded anonymous login state; it grants no product authority. Retry of a decision/render
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
               state:UPLOADED|PROCESSING|READY|CLAIMS_ACK_REQUIRED|REVIEWED|VALIDATED|RENDERED|FAILED,
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
                 warnings:[{code:WarningCode, pointer:safe_public_pointer}],
                 synthetic_draft:true, filing_ready:false}
PublicArtifact = {artifact:selector, filename:EXACT_FILE_ENUM,
                  media_type:EXACT_MIME_ENUM, size_bytes:int>0, sha256}
ExportDTO = {schema_version, document:selector, revision, source_sha256:sha256,
             artifacts:PublicArtifact[exactly4 distinct],
             synthetic_draft:true, filing_ready:false, human_review_required:true}
```

WarningCode is the closed set DRAFT_ONLY, CLAIMS_INCOMPLETE_ACKNOWLEDGED;
these are nonblocking notices only, never schema/review/package errors. Positive
validation is200 valid=true, records the current bound server receipt and returns
warnings (possibly empty). Negative package validation is422 VALIDATION_FAILED
ErrorDTO with ErrorIssueCode SCHEMA_INVALID, GROUNDING_INVALID, SOURCE_CHANGED or
PACKAGE_INVALID; validated=false, no receipt/export. Missing content/Claims
review is409 before validation executes, not a200 warning. Public issue pointers
are server-produced canonical JSON Pointers into safe DTOs, maximum256characters,
never arbitrary client keys/values or private authority fields.

All keys in a listed shape are required; absent optional content occurs only
inside the canonical JSON original values where absent/null must remain distinct.
`schema_version` is the literal `product-web/1.0.0`. Invalid enum/types/extra keys
fail closed. Binary success has no JSON envelope. No client-supplied actor,
context, owner, source digest, private manifest hash, configuration, original
records or arbitrary server path can replace server state.

### 5.2 Complete review, identifier/digest domains and edits (F-WEB-03/06)

`ReviewDTO={schema_version,document,revision,source_sha256,view,view_sha256,
mapping_version,records,authority_redactions,review_state,synthetic_draft:true,
filing_ready:false}`; mapping_version is `product-web-projection/1.0.0`.
Records are exactly7 C1 PROVENANCE_KEYS: source_envelope, structured_analysis,
reconstruction, specification, p2_003_generation_config, supported_claims,
p2_004_generation_config. Each is `{public_value:JSONValue,public_sha256:sha256}`;
review_state uses ReviewStateDTO. Preserve every non-authority business field,
evidence/locator/excerpt, warning/missing/conflict/Claims status, order and
null/absent distinction. No truncation for approval; no unclassified-field leak.

**Complete document alias inventory:** one independent public document alias is
substituted consistently at all7 pointer patterns below (`*` means every array
index). The advisory report says6 but enumerates7; execution of existing pure
P2 functions on the representative fixture confirms **7**, not6. Do not omit a
path to satisfy that arithmetic error.

| Original JSON Pointer within retained7records | Public handling |
|---|---|
| /source_envelope/document_metadata/document_id | Replace with current document's public alias |
| /structured_analysis/document_metadata/document_id | Same alias |
| /structured_analysis/evidence/*/document_id | Same alias for every evidence item |
| /reconstruction/document_metadata/document_id | Same alias |
| /reconstruction/review_package/evidence/*/document_id | Same alias for every evidence item |
| /specification/document_metadata/source_document/document_id | Same alias; previously missing |
| /supported_claims/source_identity/document_id | Same alias; previously missing |

Mapping acts on detached public copies only. Parent retains byte/canonical-value
identity of original records; clients never replace source IDs back into authority.
Record each mapping/redaction using only safe pointer+reason, never original value.
C1/A outer coordinator_instance_id, custody_id, owner, revision_token and its
hash, ProductSessionRef, callbacks, output_directory, private paths and private
snapshot/manifest authority are never serialized, including in errors/logs.
Unknown future identity/authority fields fail projection closed pending an
explicit mapping-version review; do not silently copy them.

| Digest / metadata domain | Meaning and handling |
|---|---|
| source_sha256 | Hash of admitted raw upload bytes captured/verified during intake, retained after deletion; safe source identifier, not a credential |
| originals_sha256[key] | Existing `sha256_canonical` of exact unaliased retained original; parent-only integrity baseline, never overwritten with a public-copy hash |
| public_sha256 | `sha256_canonical(public_value)` after the documented alias transform; same canonical JSON helper (sorted keys, compact separators, UTF8, ensure_ascii=false, no NaN) |
| view_sha256 | Hash of domain PRODUCT-WEB-PUBLIC-VIEW-1.0.0 plus mapping_version/document/public revision/source_sha256/records/redaction descriptors; excludes its own hash, random view selector and volatile review_state/expiry/CSRF fields |
| Private A/C1 snapshot and manifest digests | Existing authority binding over raw identity/revision/original digests; parent-only; public view selector maps to these exact values, is not a serialized hash/token |
| draft_id / p2_003_draft_id / claims_draft_id | Existing one-way P2 business provenance identifiers, not authentication or custody capability; permit read-only public metadata, including DRAFT ID printed by the current renderer |
| p2_002_identity / p2_003_content_sha256 | Existing business digest references to unaliased original reconstruction/specification; retain as provenance references, label their domain; do not recompute them over public copies or claim equality to public_sha256 |

The private snapshot excludes review-status flags in A/C1 source; the content
view binding remains stable through content/Claims/validation status changes
within one revision. Revisions change the view selector/content hashes and
invalidate every decision/validation/export. Display hash-domain labels explicitly.
All PDFs/DOCX metadata/relationships/text must be parsed/scanned for raw internal
IDs, private paths/capabilities/secrets; only the listed business identifiers and
safe source basename are admitted. Do not patch rendered bytes after manifest
hashing or modify P2 schema to hide a leak; block delivery and obtain scope if a
renderer fix is required. No general pseudonymity/cryptographic-identity claim.

UI must load the complete bounded view before enabling either decision. It
presents all7 records with safe pagination/expanders. Server binds the exact
snapshot; software does not prove a Human read every character. Source text is
inert; authority never comes from DOM text, URLs or stored client decisions.

**Narrow source-grounded edit policy:** only existing canonical pointers
`/title_candidates/<canonical-decimal-index>/title` and `/.../rationale`.
SOURCE_FACT titles are **read-only: reject EDIT_INVALID**; no silent relabeling
or keeping a SOURCE_FACT label on typed text. Only PARAPHRASE/INFERENCE entries
may be candidates. For this synthetic-only first increment, replacements must
also match a host-pinned, Human-admitted per-fixture/path/value/evidence-ID edit
variant. Unknown text is rejected rather than mechanically asserted as a faithful
paraphrase. Values/grounding are not an HTTP-provided allowlist. These admission
records are still PENDING D04/D05; no such fixture/variant is created here.

Preserve an admitted PARAPHRASE label/evidence IDs for a source-verified variant;
INFERENCE remains INFERENCE and keeps the released P2 exclusion/confirmation
behavior. Never upgrade a label or evidence/source reference. Do not weaken
P2's eligible-grounding rules to make an inference title render. W02 must use an
admitted PARAPHRASE title variant for which the existing generators actually put
the new title in all4 outputs. An INFERENCE edit may remain review-only; no claim
that all edited inference text appears in filing prose.

Server applies edits to its own retained analysis copy, validates full canonical
schema, exact source grounding and existing downstream prohibited-text rules,
then commits via approved public revision hooks. Title max500characters is the
canonical short_name limit; rationale has no canonical500-character limit but
keeps the proposed4096UTF8byte command cap. Tests must distinguish those cases,
uniqueItems/duplicate original objects, evidence preservation and filing-ready
phrases. No array/config/Claims/original/metadata replacement or pointer aliasing.
No-op (`REVISION_UNCHANGED`) and invalid edits produce422 EDIT_INVALID with no
state change. Successful edit rotates private authority, clears both reviews,
validation and manifest; stale two-tab operations409 and old artifacts404.

### 5.2a Deterministic state and review→validate sequencing (F-WEB-05)

| Current parent/C1 fact | DocumentDTO.state / allowed next step |
|---|---|
| Raw upload exists, no A ref, revision0 | UPLOADED; process or delete |
| Reserved live intake operation | PROCESSING; status/delete/logout, no review/export |
| C1 REVIEW_PENDING/current originals | READY; complete review view then explicit content decision |
| C1 CLAIMS_REVIEW_REQUIRED | CLAIMS_ACK_REQUIRED; content_reviewed=true, claims_acknowledged=false; only separate current-view Claims action can satisfy this gate |
| C1 REVIEW_RECORDED, required reviews complete, no current positive validation | REVIEWED; validate allowed |
| Same fact plus positive bound validation receipt | VALIDATED; render allowed, still revalidates everything |
| C1 RENDERED or DOWNLOADED with current valid manifest | RENDERED; authorized downloads or new validated edit |
| Failed intake operation with no usable custody | FAILED; safe status/delete/re-upload only; no retained authorization resurrected |
| Expired/revoked/missing/foreign authority | No actionable DTO; uniform401 for session,404 for resource and cleanup/revocation |

State is a server-derived summary, never an independent input or replacement
for actual flags/private revision. Validate requires content review AND separate
Claims acknowledgment if incomplete: missing content409 REVIEW_REQUIRED; missing
Claims409 CLAIMS_ACK_REQUIRED. Claims action before content or when not required
is409 INVALID_STATE. No-op duplicate decisions never call a second C1 transition;
return409 INVALID_STATE and refetch safe status. Positive200 has warnings only;
negative422 carries error issues only. Failed revalidation clears the old positive
receipt, so render cannot use it. Render/download still repeat all authority and
integrity checks; a ValidationDTO is not a browser capability.

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
|409 | STALE_REVISION, REVIEW_REQUIRED, CLAIMS_ACK_REQUIRED, VALIDATION_REQUIRED, OPERATION_BUSY, INVALID_STATE |
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
validator through the split-phase current-owner/revision/original checks and parent commit/fence;
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
each download, including missing/symlink/tampered peer files, retained source/envelope provenance and
all seven-original digests after intake (no raw-source rehash after deletion). No partial bundle advertised. On corruption revoke
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

Both admitted editable title variants must be source-verified PARAPHRASE (or
explicit review-only INFERENCE) with matching evidence references; no SOURCE_FACT
entry may be edited. This extends the proposed admission record, not its approval.

Existing controller.pdf/controller.docx variants of one source do not satisfy
two-content proof. Before fixture use, materialize candidate bytes only within
authorized scope, review provenance/rights/synthetic labels and final generators,
record exact name/MIME/size/hash and approve both identities. Constructor-pinned
allowlist only; request may not manufacture admission. Offline extraction runtime
must derive source-specific fixture analysis from the actual verified envelope,
check registered source hash and evidence IDs/locators, and refuse unknown bytes.
Never return the public fixed representative P2 sample for both documents.
The proposed app module `backend/app/services/product_synthetic_runtime.py`
implements SyntheticExtractionRuntime (`synthetic_only=True`) for the TWO admitted
identities. Constructor pins fixture identity, expected source units/locators,
canonical source-specific analysis and admitted edit variants; run_extraction
checks actual envelope/source digest and exact evidence/locator/excerpt links,
then runs existing canonical/grounding validators. Unknown/mutated source/locator/
content refuses. It returns the existing result.analysis surface without
importing tests/, providers, URLs or fixed demo output. This is an opt-in fixture
runtime implementation PROPOSED for B2, not a new general extraction pipeline,
not present today and not implemented by this PR.

Output-content assertions must distinguish controller markers from membrane
markers, preserve their source digest and show the approved edit in the new
revision. This remains synthetic test behavior, not arbitrary-paper AI extraction.

## 8. Implementation slices and exact hook proposal (D06)

All new paths below are PROPOSED, not created or implied to exist. Existing paths
are source evidence, not permission to patch runtime in this documentary PR.

| Slice | Existing/proposed module paths | Scope to approve before runtime |
|---|---|---|
| B0 admission | PR151/149/146 task/receipt records | Exact-SHA review/CI/provenance/disposition independently; no merge bundle or shared-history rewrite |
| B1 session/transport | Proposed backend/app/api/product_web.py, backend/app/services/product_web_sessions.py, product_web_host_control.py; opt-in backend/app/main.py; frontend/src/app/api/product-web/v1/[...segments]/route.ts | Versioned DTO/errors,8pending/2auth pairing, authenticated host IPC, Host/Origin/CSRF/owner and private proxy; default/public/Render modes unchanged |
| B2 custody hooks | Existing A product_synthetic_workflow.py/custody_review.py after admission; preapi_source_custody.py/document_parsing.py | Public prepare/complete/cancel intake/validate/render/revision hooks, pure parse helper; short ordered parent locks/tickets, original source cleanup/digest/state/manifest invariants preserved; never private `_get` from HTTP |
| B2 fixture runtime | Proposed backend/app/services/product_synthetic_runtime.py | Non-test SyntheticExtractionRuntime for both admitted sources and source-grounded edit variants; no tests/ imports/provider/fixed demo |
| B3 schemas/client | Proposed backend/app/schemas/product_web.py; existing frontend/src/lib/types/contracts.ts and frontend/src/lib/api/client.ts or adjacent productWeb.ts | Strict transport wrappers reuse canonical business validation, retain v1 contract; no duplicate P2 schema |
| B4 UI | Proposed frontend/src/app/product-web/page.tsx; reuse UploadPanel/WorkflowProgress/AnalysisView/EvidenceCard/GroundingBadge/ReviewItemsView/ResultWorkspace | Inert complete7-record review, admitted editor, separate explicit decisions, deterministic states/errors; no fixed sample output |
| B5 worker/native limits | Proposed backend/app/services/product_web_operations.py, product_web_worker.py; admitted hooks in A/C1/parser | Lightweight entry, bounded bytes/JSON IPC, pure existing parse/derive/render, Linux RLIMIT_AS/Windows Job Object, parent compare-and-commit/cancel/reap/staging cleanup; no coordinator object across spawn |
| B6 tests/fixtures | Proposed tests/backend/test_product_web_*.py, tests/e2e/product_web_backend.py harness, tests/fixtures/product-web/v1.0.0/manifest.json/admitted bytes; frontend/e2e/product-web.spec.ts | W01–W12/T01–T07; fixtures and app fixture runtime not implemented here |
| B6 HTTPS/test wiring | Proposed frontend/tools/product-web-local-https.mjs and a product-web project/global setup in frontend/playwright.config.ts | Actual testDir=./e2e; preserve existing v1 HTTP scope and add isolated real HTTPS project, no new skips or automatic mkcert download |

**Next streaming upload (F-WEB-07):** Node Route Handler must not call
request.formData/json/text/arrayBuffer for multipart. Forward request.body through
a backpressured byte-counting ReadableStream using `duplex:"half"`, cache:no-store,
redirect:manual and fixed upstream allowlist. AbortSignal binds client abort,
30s upload deadline and byte cap. Preserve multipart Content-Type/boundary; strip
sample-bypass/internal/forwarded/hop-by-hop headers, reject ambiguous lengths and
abort upstream on oversize/cancel. Content-Length alone is insufficient; cap
chunked streams as read. Backend independently enforces one-file/size/validator/
fixture identity and removes partial uploads. Actual buffer/peak-memory behavior
must be tested on pinned Next/Node, not inferred from fetch syntax.

TLS uses provisioned local material (§3.1); CI generation stays offline in an
owner-restricted temp directory, no committed private key or OS trust-store
change. Any self-signed test exception is limited to the product-web test project
and approved local origin, with network tripwire still enforced. Existing v1
project remains HTTP/127.0.0.1. Discovery uses frontend/e2e/, not frontend/tests/.
Native memory limits are not a general filesystem/network sandbox; fixture
admission, existing hardened parser and provider/network tripwire remain separate.

References: [Next Route Handlers](https://nextjs.org/docs/app/api-reference/file-conventions/route),
[Next custom server](https://nextjs.org/docs/app/guides/custom-server),
[Node/Undici streaming fetch](https://github.com/nodejs/undici#requestduplex).
No new package/service/business schema/Claims policy/renderer is granted.

## 9. Acceptance and test matrix — PLANNED / B RUNTIME NOT RUN

| B0.2 AC | Required proof and negative cases |
|---|---|
| W01 | Human admits two distinct actual source byte identities plus units/locators/analysis/edit-variant provenance; reject unknown/tampered hash/content/locator; no test-module runtime |
| W02 | Two real Chromium contexts use authenticated host IPC pairing; each upload→process→7-record review→admitted PARAPHRASE title edit→new content review→separate Claims ack if needed→validate→render→4downloads. Parse all8files for distinct controller/membrane markers, changed eligible title, source/revision/MIME/size/hash; no fixed sample |
| W03 | Complete7-pattern document alias inventory, unchanged raw originals, independently recomputable public hashes; preserve arrays/null/absence/locators and exclude classified outer authority; XSS/HTML/Markdown/URLs/prototypes inert; unclassified field blocks review |
| W04 | READY→content review→CLAIMS_ACK_REQUIRED if incomplete→separate ack→REVIEWED→validate→VALIDATED→render→RENDERED; missing/false/GET/refresh/Enter never approves; before-review validate409; failure422 vs success200 warnings only |
| W05 | Accepted edit cancels pending work, rotates revision and invalidates both reviews/validation/manifest/views; SOURCE_FACT edits denied, admitted PARAPHRASE/INFERENCE values keep evidence/no upgrade. Title501char, rationale501char vs4096UTF8bytes, canonical uniqueItems, prohibited filing-ready text and pointer attacks tested; invalid/no-op unchanged; stale tabs409 |
| W06 | Two separate owners; foreign document/view/artifact404; wrong cookies/internal/C1/AI-CONV capabilities cannot authenticate. Ordinary prelogin refresh/reuse does not prevent2sessions |
| W07 | POST bootstrap, GET/prefetch405/no allocation; repeat valid cookie reuses selector/CSRF/deadline; two-context/StrictMode/first-request race bounded;8pending/TTL/rate/2auth caps. Wrong Host/Origin/CSRF/Fetch Metadata/IPC key/peer/replay/TLS/backend proxy denied, default OFF |
| W08 | Revision0 raw source/registry deletion on abort/TTL; process success deletes them before usable A handle; revision>=1 uses retained provenance, no raw-file dependency. Failed cleanup revokes; login/C1 TTL/logout/restart/cancel prevent late commit and leave no live worker |
| W09 | Capture request/error/DOM/bundle/storage/logs and parsed PDF/DOCX text/metadata: no raw registry/custody/owner/ref/token/hash/private path/proxy key; explicit business derived-ID domains only. Safe no-store/disposition; no source payload logging |
| W10 | Tampered retained source hash/original digest, wrong revision/manifest/owner, changed/missing ANY4files, symlink/traversal/encodedpath fail closed; all4actual file digests and delivered bytes checked, no nonexistent source-file rehash |
| W11 | Supported Windows/Linux native limit readback and below/above512MiB worker and1536MiB aggregate probes with metric labels/peak RSS, kill/reap/parent death, usable locks during work, cancel/revise/abort races/late result fences. Upload/json/node/session/storage/rate/backpressure/partial cleanup/timeouts tested independently |
| W12 | Actual frontend/e2e discovery and local HTTPS project, real services/fixture runtime, provider/network tripwire allflows. Existing A/C1/P2/v1/security73+2/lint/typecheck/build/current+fixed-source browser/demo regressions retained. Independent Security AND Quality on same runtime final SHA and required main-target PR CI/artifact; no manual→PR CI substitution |

T01–T07 proposals are detailed in the [seven-finding reconciliation](PRODUCT-001B-WEB-001-review-remediation.md).
Executed existing pure-function inventory/regressions support source reasoning,
not B worker/OS/transport/E2E acceptance. Failures/skips stay separate; original
advisory REQUEST CHANGES is preserved. No new review/test PASS is inferred.

## 10. D01–D07 and explicit BF/BP4 gates

| Decision | v0.1.1 proposal needing actual Human acceptance |
|---|---|
| D01 | Offline local HTTPS wrapper/provisioned certificate, POST idempotent bootstrap8pending/2auth, OS-account protected IPC pairing and same real E2E path, private proxy/default OFF |
| D02 | Session/owner/CSRF/Host/Origin, all7alias patterns, public/original/private digest domains and derived metadata allowlist; exact authority-redaction inventory |
| D03 |128MiB retained-payload accounting,512MiB worker/1536MiB dedicated-host native memory budgets with Linux RLIMIT_AS+cgroupv2/Windows nested Job Object metrics/readback, supported-host probes, parent tickets/short commits/kill-reap and actual two-phase source lifecycle; no unlimited fallback |
| D04 | DTO/error/state machine, review-before-validate/warning-error split, SOURCE_FACT read-only plus admitted PARAPHRASE/INFERENCE edit variants; additive split-phase validation/render hooks without private access |
| D05 | Authorize candidate materialization THEN admit actual PDF-A/DOCX-B names/MIME/sizes/hashes and source-specific unit/analysis/edit variants. DOCX-B bytes/hash and both B admission decisions PENDING |
| D06 | Explicit A/C1/parser prepare/complete/cancel hooks, non-test synthetic runtime, worker/native limits, host IPC, Next streaming/HTTPS and frontend/e2e scope; accepted dependencies or reviewed integration disposition, no implicit146/149merge |
| D07 | Actual selected-default exact-SHA design review, then Human freeze of exact v0.1.1-or-successor commit and Phase4 scope reference; current spec DRAFT/not approved |

| Pre-freeze blocker | Status / closure evidence |
|---|---|
| BF-01 | SPEC REMEDIATION PROPOSED for F-WEB-01..07; independent final-SHA re-review must confirm; implementer edits are not finding closure |
| BF-02 / GOV-MODEL-01 | OPEN: prior actual reported model Gemini4 Argon High is advisory only; no retroactive selection. Human directs Gemini3.8 Flash High for fresh review; actual model/profile/session/reuse/independence evidence still required |
| BF-03 | OPEN: Human D01–D04/D07 decisions absent; documentary improvements do not activate security/transport/resource policy |
| BF-04 | OPEN: foundation151bc991c7 exact-SHA independent review/acceptance; old00f3833 PASS/manual152CI is not its gate |
| BF-05 | OPEN: DOCX-B bytes/hash/materialization/admission and PDF-A B approval absent; complete fixture/variant freeze needs real provenance/identity/Human evidence |

| Pre-Phase4 blocker | Status / closure evidence |
|---|---|
| BP4-01 | BLOCKED until BF-01..05 close with real evidence, frozen exact spec and Phase4 authorization |
| BP4-02 | BLOCKED: A149cf9097fd unaccepted/Draft/conflict/failed CI/provenance gap. Authorized normal integration+fresh review/CI or explicit Human-reviewed dependent plan; no force/rebase bypass |
| BP4-03 | BLOCKED: C214629daeb20 specification-only/no browser/fixture permission; D06 must delimit B/C2 contract without silent amendment |
| BP4-04 | BLOCKED: legitimate151acceptance/merge, normal integration/retarget and required main-target pull_request CI SUCCESS/security artifact; manual branch validation is separate |
| BP4-05 | CONTINUING STOP BOUNDARY: provider/API0, synthetic-only/tripwire, DRAFT/no filing/patentability/semantic acceptance/deploy; later actual independent Security AND Quality on same implementation SHA |

First obtain actual bc991c7 foundation review without moving its target merely
for status. Normal FF push only for this documentary patch; later normal main
integration/retarget preserves shared history/150/other-agent work. No manual
SUCCESS or advisory documentary PASS is promoted to freeze/merge approval.

Resume: **RESUME-PRODUCT-001B-WEB-001**. Read this spec, current checkpoint and
Draft handoff; refresh main/151/149/146; keep unapproved runtime work blocked.

Task ID: PRODUCT-001B-WEB-001
Agent: Codex — authorized verification/contract planner; future implementer conditional
Reviewer: Gemini3.8 Flash High / Antigravity STRICT READ-ONLY; actual new model/profile/session/reuse/verdict PENDING
Status: v0.1.1 documentary remediation proposed; advisory REQUEST CHANGES retained; selected-default re-review/decisions/fixture admission PENDING, runtime BLOCKED
Version: 0.1.1
Work completed: Verified original advisory review and proposed all7documentary fixes, updated parent/worker/lifecycle/projection/pairing/state/runtime/streaming contracts and acceptance matrices
Files affected: This spec, safe QA receipt and documentary README/checkpoint/review handoff only
Evidence checked: AGENTS0.6.2, context/system spec, B0.2.0/web decision, exact151/149/146 sources, live refs/checks/artifact and existing validators/services/UI
Findings: Foundation exact-SHA review absent; A/bound-review extension unmerged; independent validate method absent; C2 scope not browser/fixture approval
Decisions: Human phase4 gates preserved; all new security/fixture/runtime choices proposed, no policy activation
Issues: BF-01..05/BP4-01..05, D01–D07, accepted dependencies/fixture identities and exact-SHA selected-default review/main-target PR CI
Security impact: Documentation only; no runtime/auth/provider/deploy changes or sensitive evidence publication
Recommended next action: Independent design review plus concrete Human decisions; implement only admitted slice after gate evidence

0.1.0 created 2026-11-05 by Codex. Breaking change: No runtime change;
proposed new transport/security policy requires explicit approval before code.


0.1.0→0.1.1,2026-11-06,Codex under Human REVIEW REMEDIATION: address advisory
F-WEB-01..07 without runtime changes, correct pointer count to7 from source
execution; v0.1.0 remains at22d070c64ef7328ca893b06ad40044ac4f5ae722.
Original report unchanged local; model mismatch/advisory REQUEST CHANGES retained.
Breaking change: No deployed/runtime change; proposed DTO/policy corrections still
need Human review/freeze/implementation authority, never retroactive approval.
