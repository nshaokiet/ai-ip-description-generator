# PRODUCT-001B — Trusted Local Review Presenter

Version: 0.1.0. Date: 2026-11-05 (Asia/Saigon). Author: Codex.
Status: PROPOSED IMPLEMENTATION SCOPE — planning only; not frozen or implemented.
Authorization: Human requested product continuation planning following PRODUCT-001A
reconciliation. USD 0; no provider call, merge, deployment or production release.
Breaking change: No proposed product/API/schema/template change.

## Product outcome and dependency

A local operator can inspect the complete, revision-consistent seven-document
review snapshot from PRODUCT-001A, make explicit content and separate incomplete-
Claims acknowledgments, and obtain the existing four validated draft artifacts.
The first increment is a **terminal presenter in the same trusted process**.
This keeps the already approved local single-principal trust boundary and requires
no new browser/session/authentication policy. Browser integration is a later,
separately reviewed scope.

A dependency is [PR #149](https://github.com/nshaokiet/ai-ip-description-generator/pull/149),
implementation `cf9097fda4688db08fd505e21fcbf3c0e53a9d5c`,
tree `b75cf5d35bef555933dae6c42037b544525092e0`.
It is OPEN/DRAFT, reviewer-reported Technical PASS, provenance NOT VERIFIED,
hosted CI FAILED; it is not an accepted merged baseline.
See [reconciliation](PRODUCT-001A-review-reconciliation.md). This scope can be
reviewed provisionally while original-report archival remains pending. Do not
silently treat reconciliation as completed or A as merged.
A future implementation may be stacked on the exact authorized A candidate with
its dependency explicitly disclosed; it must not claim A is on main. Prefer
accepted A as the eventual merge base. No merge authorization follows here.

## Reuse and ownership boundary

| Concern | Existing owner to reuse | B responsibility |
| --- | --- | --- |
| Upload validation/registration | Existing document storage/registry/intake services | Invoke trusted intake with host-pinned synthetic fixture policy; do not build another parser/custody store |
| Source custody/extraction/reconstruction/Claims/assembly | A OfflineSyntheticWorkflow plus existing C1 and USPTO services | Construct/inject once in trusted host; no parallel extraction pipeline or caller-selected provider |
| Complete review data | A review + custody_review.review_documents | Present all seven originals and provenance without flattening, truncation or mutating them |
| Acknowledgments | A acknowledge, with snapshot-bound C1 target | Explicit interactive decisions, actor/context from trusted host, separate incomplete-Claims invocation |
| Rendering/download integrity | A render/download and existing four-file manifest validation | Show safe artifact metadata and write only downloaded verified bytes to a host-controlled destination |
| Revision, expiry, abort | A revise/abort and C1 invalidation/cleanup | Discard stale presentation state; show safe errors; require fresh display and decisions |

No app import from test modules. Reuse the existing synthetic runtime interface via
trusted host injection; if an executable bootstrap needs a concrete runtime, define
its source/factory in the implementation spec without creating a second semantic
extractor. Fixture admission stays byte-pinned and explicit; existing test files
are not automatically Human-approved pilot papers.

## Proposed behavior and acceptance criteria

1. Default OFF, local/synthetic only, one configured principal, existing four-session
   capacity. Host owns runtime, authorization callbacks, fixtures and output root.
   Request/terminal data cannot replace callbacks or construct arbitrary authority.
2. Convert A's immutable snapshot to a detached complete JSON tree; verify the
   expected seven originals/digests and snapshot identity. Display all fields,
   source/evidence locators, warnings, missing information, support information,
   absent-versus-null distinctions and array order. Paging is navigation only;
   it must never produce a truncated acknowledgment snapshot.
3. Render source strings inertly: escape terminal control/ANSI sequences and
   dangerous bidi/control characters for display, preserve original data/digests
   unchanged, and prevent source text from creating prompts, commands or links
   with executable behavior. No automatic browser launch or shell command.
4. Mark every screen/output as synthetic, draft, Human-review-required and
   filing_ready=false. Acknowledgment does not change SOURCE_FACT/INFERENCE,
   establish semantic acceptance or confer filing/legal readiness.
5. Never acknowledge on load, EOF, Enter-default, source instruction, parse error
   or generic confirmation. Require deliberate affirmative content review for
   the exact fully presented snapshot; incomplete Claims need a distinct subsequent
   affirmative decision. Negative/interrupt leaves approval unset.
6. Before each decision/render/download, obtain current A authority/state and
   snapshot binding. Revision, expiry, restart, cross-session mix or authorization
   revocation invalidates presentation/decision state and old exports. Reads do
   not extend the existing 1800-second idle / 7200-second absolute limits.
7. Keep ProductSessionRef, coordinator/custody internals, owner handles, revision
   tokens and token hashes private to the host. Do not dump dataclasses, exception
   reprs or debug state. Show only explicitly selected safe status/revision/digest/
   artifact fields. No token in terminal logs, URL, browser storage or JSON DTO.
8. Render/download through A only. Show four fixed filenames/MIME/size/hash values
   and synthetic disclaimers. Verify manifest/current revision through A again
   before saving; refuse stale/tampered bytes, symlink/path escapes and overwrite
   of unrelated files. No caller-provided output pathname enters custody internals.
9. On abort, expiry, denial or errors, revoke UI action state and surface sanitized
   errors. Delegate custody/source/export cleanup to A; do not add persistent
   source/projection/decision caches or a second cleanup policy.

## Focused validation for an implementation PR

- PDF and DOCX happy paths reuse A end-to-end behavior and parse all four outputs;
  provider/network tripwires remain active.
- Complete seven-original presentation and unchanged snapshot/digests, including
  nested arrays, explicit nulls, absent optional fields, long content and limits.
- Terminal control/prompt injection remains inert without changing source data.
- No affirmative input, EOF/interruption, incomplete display and separate Claims
  gates; no automatic acknowledgment.
- Changed snapshot, stale revision, mixed sessions, revoked principal and expiry
  between display/ack/render/download all fail closed.
- Captured stdout/stderr/error/log/output metadata contain no private token,
  token hash or host handle. No HTTP route, browser bundle export or adapter
  serialization is introduced.
- Invalid artifact metadata/hash and destination traversal/symlink/overwrite
  cases fail safely; abort/expiry cleanup uses existing A behavior.
- Run focused B and relevant A/C1 regression checks once on final candidate;
  exact-SHA independent review and required CI remain separate gates.

## Proposed file scope and exclusions

Expected changes: one terminal presenter module/entry point, focused presenter
tests, task/runbook documentation and README status. Prefer standard library;
no new external dependency/service, schema, renderer, extraction, Claims semantics
or provider configuration. Small A integration fixes, if actually required, must
be justified and reviewed on the new SHA rather than concealed as presentation.
Do not import other implementation branches or reproduce custody logic.

No HTTP/browser adapter exposure. A later browser version needs an approved
server-owned authorization/owner/session/CSRF/CORS/retention design and an explicit
safe DTO boundary; localhost alone does not provide those controls. Internal
custody tokens, revision secrets and the trusted same-process adapter must never
be sent directly to browsers.

## Recommended next product PR

**PRODUCT-001B: add trusted local review presenter over PRODUCT-001A**.
Review/freeze its concrete implementation spec and dependent base first. Keep CI
snapshot resilience and dependency remediation in separate PRs. Leave PR #149
OPEN/DRAFT; do not merge/deploy or fabricate full CI success. Full C2 admission,
provider/real-paper semantic extraction and production readiness remain separate.

Task ID: PRODUCT-001B
Agent: Codex — planner
Reviewer: Scope review pending; no new independent verdict
Status: Proposed scope only; implementation not started
Version: 0.1.0
Work completed: Reuse map, terminal-first trust boundary, acceptance and validation scope
Files affected: Planning document and factual status references
Evidence checked: A fixed-SHA adapter/projection/tests, C1 policy, actual PR/CI
Findings: A acceptance and provenance/report archival remain unresolved
Decisions: Reuse A end to end; preserve private authority in trusted process
Issues: Concrete implementation authorization/freeze and dependency disposition pending
Security impact: No new transport or browser exposure; explicit inert presentation controls proposed
Recommended next action: Review scope, archive A report, resolve required CI/security gates separately
