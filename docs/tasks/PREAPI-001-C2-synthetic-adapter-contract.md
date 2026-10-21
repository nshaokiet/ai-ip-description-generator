# PREAPI-C2 — Synthetic product adapter and review flow

| Field | Value |
|---|---|
| Version | 0.1.0, architecture review candidate |
| Status | SPECIFICATION_DRAFT; no frozen C2 contract, implementation acceptance or merge |
| Task / authority | PREAPI-C2; Human zero-cost development instruction, 21/10/2026 |
| Base | `d7516d4322f828c5802ec6d9e5ef5f8dffa5721d` |
| Prerequisite | Human-frozen C1 v0.1.1, [implementation Draft PR #139](https://github.com/nshaokiet/ai-ip-description-generator/pull/139) still unmerged and independently unreviewed |

## Intended boundary and user journey

This specification proposes a **local, same-process, synthetic-only** adapter.
Its input is a newly registered PDF/DOCX document ID from APP-001 and a trusted
process-local owner context. It calls C1 `commit_upload` with an explicit
synthetic extraction runtime. The adapter cannot accept a caller-authored
`ExtractionInputEnvelope`, analysis, seven-original bundle, package, manifest
or `draft_digest` as custody proof. C1 retains and validates the actual APP-002
envelope before upload cleanup, then derives P2-002 reconstruction, P2-003
specification and P2-004 supported-Claims result from the same source. The
reviewer sees a current revision, source/evidence index, unsupported or
missing elements and draft status; the trusted caller records explicit content
acknowledgment. If Claims are incomplete, a separate affirmative incomplete
Claims acknowledgment is required. Only then may C1 call P2-005 and P2-006
to publish four verified PDF/DOCX **synthetic draft** artifacts. Every output
remains `filing_ready=false`.

This is a proposed internal interface, not an HTTP route, browser UI, public
API, tenant/auth model or deployment authorization. Future frontend transport
requires a separate Human security decision. The existing v1 routes and
Candidate A `local_synthetic_v2.py` remain unchanged and unmounted; its bearer
capability must not be passed to a browser.

## Source-to-target contract

| Existing source | Proposed C2 use | Gate / authority |
|---|---|---|
| `backend/app/api/routes/documents.py`, `document_storage.py`, `document_registry.py` | Accept synthetic PDF/DOCX, return opaque registered ID | APP-001 owns bytes, size/type and initial SHA-256 |
| `document_parsing.py` and C1 `commit_upload` in PR #139 | Build canonical APP-002 envelope from leased stored bytes | C1 rehashes actual bytes, validates grounding and retains envelope before cleanup |
| `preapi_source_custody.py` in PR #139 | Proposed `start/status/revise/review/render/download/abort` delegation | Owner, custody ID, opaque revision token, idle/absolute expiry and per-record lock |
| `invention_reconstruction.py`, `uspto_specification_generation.py`, `supported_draft_claims_generation.py` | C1 derives and retains P2-002/003/004 originals | No client replacement or unsupported Claims promotion |
| `uspto_document_package.py`, `uspto_document_package_validation.py` | C1 assembles/revalidates seven originals | Package digest alone confers no authority |
| `uspto_offline_renderer.py` | C1 renders four fixed files | Manifest binds owner, custody, revision, MIME, size, SHA-256 |
| `uspto_offline_orchestration.py` | Reuse only compatible internal validation semantics | Its session alone is not upload custody or authentication |
| `local_synthetic_v2.py`, `backend/app/main.py` | Reference isolation boundary only | No new mounted route or browser bearer exposure |

The adapter may expose only an internal `C2SessionView` containing opaque
custody/revision references, safe state, evidence locators, Claims status and
artifact metadata. Raw source excerpts, private filesystem paths and bearer
tokens do not belong in logs or broad status listings. A trusted caller may
hold the C1 revision token in memory; it is not an authentication substitute.

## State and error semantics

| State or operation | Required condition | Failure result |
|---|---|---|
| Start | New APP-001 ID, synthetic runtime, trusted owner, validated configs | Reject missing/hash-mismatched/foreign source; clean upload |
| Review pending | C1 receipt at current revision; seven originals retained | No render or download |
| Revised | C1 recomputes dependent originals and rotates token | Prior review, manifest and token invalid |
| Content reviewed | Explicit trusted Human authorizer callback for exact revision | Deny absent/forged callback |
| Claims incomplete | Explicit second acknowledgment | Zero available exports until affirmative decision |
| Rendered | C1 validates package and four-file manifest before publication | Incomplete render cleans/revokes staged output |
| Download | Same owner and current token, one of four fixed names, live TTL and verified entire manifest | No path-selected arbitrary file or stale output |
| Abort/expiry | Revoke lookup/token/manifest before owned-path cleanup | Cleanup failure remains sanitized and never restores access |

The adapter should map C1 error codes to stable, source-safe internal results,
without echoing file content, exception messages or credential data. It must
not retry a state transition after uncertain failure by adopting a
caller-supplied package. Thirty-minute idle and two-hour absolute TTL use the
C1 monotonic clock. A process restart loses custody; recovery cannot recreate
it from a v1 `PipelineResult` or a client analysis object.

## Threat and acceptance matrix

| Threat / test | Expected synthetic outcome |
|---|---|
| Foreign analysis, envelope or self-consistent draft splice | Reject before custody commit; V2-03/04 plus C2 negative test |
| Changed stored source bytes or forged evidence ID/locator | Reject at intake; no published record or artifact |
| Wrong owner, stale revision or expired record | Deny status, review, render and download |
| Missing Human content or incomplete-Claims acknowledgment | Four-artifact count remains zero |
| Missing one of seven originals, altered config or package-only render | Fail closed; no export authority |
| Manifest corruption, symlink, traversal or foreign output directory | Deny all artifact retrieval; revoke if integrity fails |
| Interrupted renderer or cleanup failure | Revoke first, expose only sanitized cleanup marker |
| Provider client construction or outbound provider egress | Test tripwire blocks attempt; normal synthetic path reports zero unexpected attempts |
| Public route/browser capability | Main app route inventory unchanged; Candidate A remains unmounted |

Positive C2 acceptance needs both synthetic PDF and DOCX paths, a fresh
source-bound revision, seven original inputs, explicit review decisions and
exactly four verified outputs. Tests must inspect source digest and manifest
integrity without preserving raw paper text in reports. Existing C1 V2-01…10
cover many primitives; C2 tests should target integration gaps, not mirror
those tests merely to increase count. Released v1 behavior must remain intact.

## Decisions required before implementation acceptance

1. Freeze the C2 internal adapter interface and define which trusted process
   component supplies owner and Human review authorization. C1's test callback
   does not establish a production reviewer identity.
2. Decide whether a browser-facing review UI is in scope. If so, approve a
   separate transport/auth/session/retention policy and threat model before
   any route, capability or frontend code is written.
3. Accept C1 implementation only after its own exact-SHA independent review,
   CI and guarded merge/postmerge checks; a stacked C2 candidate cannot be
   merged ahead of C1.

Rollback of a future internal adapter is disabling its default-off entry
point and allowing current in-memory sessions to expire or abort. It must
not rewrite C1 custody records, accepted gold or released v1 outputs. No paid
provider call, real/confidential paper, production Claims or Render change
belongs to this task.
