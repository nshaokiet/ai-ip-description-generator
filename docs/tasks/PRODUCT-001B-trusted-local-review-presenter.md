# PRODUCT-001B — Browser review and synthetic export increment

Version: 0.2.0. Date: 05/11/2026, Asia/Saigon. Planner: Codex.
Status: PROPOSED WEB CONTRACT; NOT FROZEN / NOT IMPLEMENTATION APPROVED.
Registry/lease: UNVERIFIED. Proposed implementer: Codex.
Authority: RESUME-FOUNDATION-001 authorizes web-direction/spec planning only.
Review: independent Security AND Quality proposed on the same final SHA; actual review PENDING.
Breaking change: No runtime change here; proposed new transport/security boundary needs Human approval.

## Delta and user outcome

0.1.0 → 0.2.0, 05/11/2026, Codex: replace terminal-first product recommendation
with browser increment under [Human web direction](../decisions/RESUME-FOUNDATION-001-web-direction.md).
Keep [v0.1.0 byte-identical](history/PRODUCT-001B-trusted-local-review-presenter-v0.1.0.md)
and its [source commit ff511e5](https://github.com/nshaokiet/ai-ip-description-generator/commit/ff511e5b4e384268224d586a8abd3cea11313655).
The historical filename remains the task location; no second B task is created.

A local synthetic operator can upload an admitted PDF/DOCX, inspect complete
source-linked draft data, submit a validated edit, explicitly review the current
revision, validate, then download four artifacts derived from that selected
source. This is a Next.js + FastAPI web path over A/C1/P2, not the fixed-file
public demo. It does not provide arbitrary-paper AI extraction.

## Dependencies and proposed scope

- Accepted PRODUCT-001A/PR149 (or explicitly reviewed dependent integration), C1
  postmerge disposition, applicable C2/PR146 contract disposition, current security
  and required CI gates. Branch presence or a technical PASS is insufficient.
- Human approval/freeze of this browser session/auth/CSRF design and synthetic
  fixture policy before implementation. C2's same-process no-browser contract
  is not silently amended; record B as an explicit separate transport increment.
- Existing Next UI, FastAPI opt-in local factory/adapter, a server session/DTO
  boundary, A's workflow and C1/P2 are the proposed modules. Exact route names and
  request/response/error schemas must be pinned in the approved implementation
  spec before code; never expose Python dataclass/projection objects directly.
- Reuse upload validation/storage/registry, source parsing, extraction injection,
  reconstruction, specification/Claims checks, assembly and renderer. No parallel
  pipeline, test-module import, provider selection from requests, schema/template
  change, public deploy or new external service/package.

## Proposed security contract — not activated policy

The first increment is **single local operator, single process, volatile state**.
It has no multi-user production claim. Still test two independent browser login
sessions with distinct server owner scopes; one session cannot act on the other.
One A workflow instance per server principal/session preserves A's single-principal
authorization callback. Host callbacks must bind the exact current principal.

The trusted host authenticates the configured local operator and bootstraps a
short-lived browser login without using C1/AI-CONV capabilities as credentials.
Use a distinct random opaque session cookie, server lookup, HttpOnly and
SameSite=Strict; Secure in the approved HTTPS mode. Exact local development
transport/cookie setup and credential bootstrap must be approved and tested
before code (including any explicit loopback-HTTP exception). No secrets in URL,
query string, localStorage or logs. No external identity service is proposed.

Server owns original source, authenticated principal/owner, browser session,
ProductSessionRef, C1 custody/revision authority, seven originals, review decision
and manifest. Browser DTOs allow only app-level document selectors, safe source
digest/status/revision, complete inert review content/evidence, public artifact
metadata and an independent anti-CSRF token. Selector possession is never authority.
Keep internal custody handles/IDs, coordinator IDs, revision secrets/token hashes,
capabilities, private paths and callbacks out of DTOs/errors/HTML/JS/bundles/logs.
An app selector must not serialize the internal handle.

Use one explicitly configured browser origin and server-side proxy/API mapping;
check Host/Origin and synchronizer CSRF token for upload/mutations, deny missing
or foreign origins in the approved browser mutation path, deny permissive
credentialed CORS; GET cannot approve, edit revisions or initiate rendering.
Existing custody download bookkeeping/TTL behavior remains explicit. SameSite/CORS/unguessable URL
are supplementary controls, not authorization. All reads and downloads enforce
owner/session. Never register a public default route merely because localhost
or an opt-in environment flag is present. Existing static demo remains its
separate mode; deployment/Render changes are excluded.

Apply existing upload/resource limits, four A sessions per workflow and bounded
review projections; implementation spec must also bound global browser sessions,
request bodies, operation rate and aggregate RAM rather than multiply A limits
without a host cap. Reject unexpected content types/fields and sanitize errors.

## Revision, review, editing and lifecycle

1. Upload uses approved synthetic byte identities, not a request-generated
   allowlist. Source SHA256 is computed from actual registered bytes and verified
   by C1. Safe UI identifies the selected source and current public revision.
2. Present all seven originals, evidence/locators, warnings, missing/conflict and
   Claims status without truncation. Source content renders inertly; no raw HTML,
   executable Markdown/links or source-driven command/automatic approval. Preserve
   exact original JSON/digests; pagination must permit complete review.
3. An edit goes through a schema-bound server command compatible with A's current
   `revise` input (grounded structured analysis + existing fixed configs). Server
   validates and rederives; no arbitrary DOM text/package or seven-original
   replacement becomes authority. Invalid/unsupported edits are rejected safely.
4. A successful edit rotates private revision authority and invalidates content
   review, incomplete-Claims acknowledgment, validation result and export manifest.
   Invalidate UI action state immediately; old downloads/decisions must fail even
   under concurrent tabs. Re-present the complete new snapshot before decisions.
5. Content review and acknowledgment of **incomplete Claims are two independent
   explicit actions** on the exact current snapshot/revision. No checkbox default,
   page load, Enter, refresh or validation result records approval. Actor/context
   are server-derived; never accept them as trusted client assertions.
6. Validate/render/download re-check owner, expiry, revision/snapshot and all seven
   originals. C1 retains 1800-second idle and 7200-second absolute limits; passive
   reads do not extend TTL. Browser login expiry cannot outlive valid authority.
7. Refresh may recover safe display only from a still-valid server login and
   current in-memory source/revision; never restore decisions from client state.
   Logout/expiry/abort revoke UI and server access. Process restart loses volatile
   sessions and fails closed: no draft recovery promised; require new login/upload.
   Cleanup is limited to service-owned paths; do not adopt or serve orphaned files.
   Persistence/review history/author answers/retention are a separate later task.

## Exact export contract

Names derive from P2-006 `uspto_offline_renderer.FILES`; MIME and custody conditions
derive from C1 `preapi_source_custody.MIME/render/download` at main53c253be and
A `render/download` at cf9097fd. Those executable contracts prevail over old
descriptive P2-006 lowercase draft-name examples.

| Filename | Exact MIME | Meaning / condition |
|---|---|---|
| `B2_REFERENCE_PREVIEW.pdf` | `application/pdf` | Reference-style preview, not filing-ready. |
| `B2_REFERENCE_PREVIEW.docx` | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` | Editable reference-style preview. |
| `USPTO_APPLICATION_DRAFT.pdf` | `application/pdf` | Application-layout draft; no legal/filing acceptance. |
| `USPTO_APPLICATION_DRAFT.docx` | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` | Editable application-layout draft. |

All four require valid current source/custody/revision, full retained originals,
content review and separate incomplete-Claims acknowledgment when applicable,
validated assembled package, atomic complete render and verified signatures,
nonempty sizes and hashes. A binds manifest digest to the actual source/document/
revision/snapshot. Server retains the internal manifest; download uses an app
artifact key after full authorization and revalidation, never a filesystem path
or client-supplied custody/capability. No partial bundle is advertised. Send
correct MIME/disposition and Cache-Control:no-store; verify bytes before delivery.
Every UI/output remains synthetic_draft=true, filing_ready=false, Human-review-required.

## Measurable acceptance and test matrix — all proposed / NOT RUN

| AC | Browser/server case and required result |
|---|---|
| W01 | Two explicit admitted synthetic sources, one text PDF and one DOCX, with **different technical content** and distinct pinned bytes/hashes. Actual registry/C1 hashes match; approved names/hashes recorded before fixture use. A's existing PDF/DOCX variants of one controller do not alone satisfy two-content proof. |
| W02 | Both fixtures complete real browser upload → process → complete review → validated edit → re-review → validate → export. Parse both PDFs and both DOCX for each source; assert source-specific technical markers and current revision, plus matching MIME/size/hash/manifest. Never compare only filenames or serve fixed demo output. |
| W03 | All seven originals/locators/digests, nested arrays/null/absent fields and warnings survive inert presentation; XSS/HTML/Markdown injection cannot change actions/authority. No whole confidential projection logged. |
| W04 | Unreviewed export denied; content acknowledgment alone cannot bypass incomplete-Claims gate. Negative/no input/refresh never approves. |
| W05 | Edited/stale snapshot, two-tab races, old validation or old export fail; fresh review/export works only for the new revision. Server rejects unauthorized original replacement. |
| W06 | Cross-browser-session/owner document, snapshot, revision and download selectors denied; random/tampered selectors/hashes/metadata confer no access. No C1 or AI-CONV capability usable as browser auth. |
| W07 | Foreign/missing Origin/Host and CSRF, cross-site upload/review/edit/download attempts, invalid cookie/session, revoked login and default-off routes fail safely. Test exact approved cookie/transport mode. |
| W08 | Expiry between review/ack/render/download denies access; reads do not renew C1 TTL. Refresh preserves only valid server-owned state; process restart/logout cannot recover approvals or exports. Cleanup failure is visible and fail-closed. |
| W09 | Capture request/response/error/UI/bundle/storage/log output; no revision token, custody handle, internal capability, token hash or private path. Correct no-store and safe artifact MIME/disposition. |
| W10 | Forged bytes/manifest, wrong source/revision, symlink/path escape and missing/partial artifact bundle rejected. All four artifact digests rechecked before bytes are served. |
| W11 | Bounded request/projection/session/global resource behavior; cancellation/abort and cleanup use existing A/C1 policy; test precise approved caps without changing renderer/source contracts. |
| W12 | Provider/network tripwire active on both complete flows; relevant A/C1/v1 regressions, lint/typecheck/build and actual Chromium E2E pass. Independent Security AND Quality read-only on same final SHA plus all required CI; record real skipped/failed results and do not inherit PASS on new code. |

Implementation may begin only after contract/route schemas, auth/transport policy,
fixture admission and scope are explicitly accepted. Acceptance of this planning
document never activates live provider, real-data use, production Claims,
persistence, public deployment or semantic acceptance.
