# P0-006 — Frontend/Backend Integration Specification and Current-State Audit

## 1. Metadata

| Field | Value |
|---|---|
| Task ID | P0-006 |
| Specification version | 0.2.0 |
| Status | Specification — Human Decisions Resolved; Awaiting Targeted Independent Re-review |
| Implementation status | NOT STARTED; targeted re-review and separate Human implementation approval pending |
| Owner / author | Human / Product Owner; Codex draft |
| v0.1.0 independent reviewer | Gemini 3.8 Flash High — `PASS WITH HUMAN DECISIONS REQUIRED`; findings `NONE` |
| Human decision gate | RESOLVED — HD-P0-006-01 through HD-P0-006-07 approved by Human / Product Owner |
| v0.2.0 reviewer | Targeted independent re-review pending; exact reviewer model/profile to be recorded |
| Date | 27/09/2026 |
| Source of truth | This Git file; audit baseline `ec4db79af8d0511a2888e176d45defefdc3828dc` |
| Related tasks | P0-005, APP-003, P0-003, P0-004, DOC-001 |
| P0-005 accepted implementation | `43907213f14c8c55294f55af34afcc0cbcc9dc66` |
| P0-005 closeout | `ec4db79af8d0511a2888e176d45defefdc3828dc` |

### Change history

| From | To | Date | Author | Change | Reason | Related decision/finding | Breaking change |
|---|---|---|---|---|---|---|---|
| None | 0.1.0 | 27/09/2026 | Codex | Initial current-state audit and proposed integration contract | Define the actual remaining P0-006 work before implementation | P0-005 closeout; governance issue GOV-P0-006-01 | No production contract changed |
| 0.1.0 | 0.2.0 | 27/09/2026 | Codex | Incorporate seven approved Human decisions after v0.1.0 independent review | Resolve the specification's decision gate before targeted re-review | HD-P0-006-01…07; Gemini 3.8 Flash High `PASS WITH HUMAN DECISIONS REQUIRED`, findings `NONE` | No production contract changed |

The seven decisions in section 22 are approved specification requirements. v0.1.0 received independent `PASS WITH HUMAN DECISIONS REQUIRED` with no findings; v0.2.0 awaits targeted independent re-review. This is not approval to start implementation or release.

## 2. Objective

Complete the local, single-tenant, synthetic-data Human review path after P0-005's read-only results: edit eligible draft prose, keep distinct review revisions and section decisions, validate the selected edited revision, and export that exact revision as an editable DOCX. Reuse the existing upload, process, result transport, and export boundaries. The generated content remains a draft requiring Human review and is neither legal advice nor filing-ready.

## 3. Current-state evidence

| Capability | Verified implementation evidence | Present boundary |
|---|---|---|
| Upload | `backend/app/api/routes/documents.py:upload_document`; `frontend/src/components/UploadPanel.tsx`; `frontend/src/lib/api/client.ts:uploadDocument` | One PDF/DOCX, 10 MiB client check; backend validates and returns safe metadata. Client check is not authoritative. |
| Metadata retrieval | `backend/app/api/routes/local_orchestration.py:get_document`; `frontend/src/lib/api/client.ts:getDocument` | `GET /api/documents/{id}` exists when local orchestration is enabled; frontend helper exists but page does not call it. Registry metadata can disappear after source cleanup. |
| Process | `local_orchestration.py:process_document`; `backend/app/services/core_pipeline.py:run_pipeline`; `frontend/src/app/page.tsx:handleProcess` | `POST /api/documents/{id}/process` synchronously runs preparation, extraction, drafting; source cleanup runs in `finally`. |
| Analysis and draft transport | `local_orchestration.py:ProcessDocumentResponse`; `frontend/src/lib/types/contracts.ts:ProcessResult`; `frontend/src/components/ResultWorkspace.tsx` | One response includes canonical `analysis`, `draft`, and minimal metadata; views are read-only. |
| TypeScript contract coverage | `frontend/src/lib/types/contracts.ts:PatentDraft`; `schemas/patent-draft/v1.0.0/patent-draft.schema.json` | The frontend type omits canonical `output_notice` and `drawings`; returned JSON still carries them. Editing must preserve the full payload. |
| DOCX export | `local_orchestration.py:export_docx`; `backend/app/services/patent_docx_renderer.py:render`; `frontend/src/lib/api/client.ts:exportDocx`; `frontend/src/app/page.tsx:handleExport` | `POST /api/exports/docx` accepts `{draft}`, returns DOCX and removes temporary output. Renderer applies canonical JSON Schema, but the route does not re-run source-analysis business/grounding validation or verify Human review state. |
| Same-origin proxy | `frontend/next.config.ts`; `frontend/README.md` | Browser requests `/backend/*`; Next.js rewrites to server-side `BACKEND_URL` (default `127.0.0.1:8000`). |
| Safe errors | `backend/app/main.py` handlers; `local_orchestration.py:_pipeline_status`; `frontend/src/lib/api/client.ts:toApiError` | Structured safe error and correlation ID; proxy/non-JSON fallback and network fallback. |
| Local enablement | `backend/app/core/config.py:Settings.from_environment`; `backend/app/main.py:create_app` | `AI_IP_ENABLE_LOCAL_ORCHESTRATION_API=1` opts in to metadata/process/export routes; flag is not authentication. |
| Existing tests | `tests/backend/test_document_upload.py`, `test_core_pipeline.py`, `test_core_pipeline_e2e_offline.py`, `test_patent_docx_renderer.py`, `test_pipeline_docx_integration.py`, `test_local_orchestration_api.py` | Backend offline upload, pipeline, renderer, and HTTP behavior covered. No tracked frontend component or browser E2E test is present in this baseline. |

`backend/app/services/pipeline_docx.py:CorePipelineDocxService` already composes pipeline and DOCX internally for P0-003; the P0-004 HTTP export route uses the renderer directly. Neither should be reimplemented as P0-006.

### APP-003 provenance and governance reconciliation

- `3e7c2910695eed9e5ef1d7d0ff11f8f0e3ac6c38` introduced `core_pipeline.py` and its two offline test modules as APP-003.
- `b5a47f6030441b438e7e1745b75b05d8b345d6c0` merged APP-003 into `main`; its repository merge message records 32/32 acceptance criteria and independent Antigravity `PASS`. The merge was made under the Human repository account. This is evidence of implementation acceptance for the local merged code, though the exact reviewer model/profile is not in the merge message.
- `e891c38cedf4d7b18d190d082993d0e8d5aa2c6b` introduced `patent_docx_renderer.py` and `pipeline_docx.py` for P0-003; merge `5cfb1b5d0377fcb4538a2bba0bbb48232001b123` records independent `PASS` and no findings.
- `0f5799baad63f4516556d6c984f7fc31a1956699` introduced `local_orchestration.py` and the opt-in HTTP wiring for P0-004; merge `43737a79fcdb634a12a92752c767df9fbf98d1f3` records independent `PASS` and no findings.
- P0-005 `d5804df944ad85c53f0c5d90f0174b39e78b24b5` introduced the frontend; final accepted implementation is `43907213f14c8c55294f55af34afcc0cbcc9dc66`, closed by `ec4db79af8d0511a2888e176d45defefdc3828dc`.
- **GOV-P0-006-01 (open governance issue):** `docs/operations/01_PROJECT_CONTROL_CENTER.md`, `PROJECT_CONTEXT.md`, and `docs/tasks/APP-003-core-pipeline-orchestration.md` still say APP-003 implementation `NOT STARTED`, although the later implementation and merge commits above exist. These are stale statements, not evidence that the code is absent. This task records the discrepancy and does not change APP-003 status. Human should commission a separate APP-003 governance reconciliation, including the exact review record/profile if available.

The merged APP-003 implementation may be used as the technical dependency for this draft specification. A separate new APP-003 implementation or review is not proposed.

## 4. Problem statement

P0-005 displays canonical results and exports the returned draft unchanged. `frontend/README.md` defers draft editing and versioned Human approval to P0-006; HD-P0-006-02 now narrows that wording to local session review state, not formal audited approval. The current `PatentDraftView` renders text and provenance without edit controls; `ResultWorkspace` exports `result.draft`. No edit revision, section decision, actor attribution, or review audit state is present. The AI-003 canonical schema intentionally excludes Human approval state. The current export endpoint validates schema only, so a schema-valid edited draft could bypass the source-linked business rules enforced during generation. Also, `page.tsx:handleProcess` sends no `selected_title_candidate_id`; the synchronous process creates analysis and draft together, before the UI can show title candidates. Under `draft_business_validation.py`, absent selection requires a `MISSING` title marker. A post-analysis title-selection workflow would require a separately approved contract.

## 5. Scope — In

1. Finish the existing local frontend/backend contract for edited-draft validation and export, including complete frontend types for the canonical payload, without duplicating upload, process, result transport, or rendering.
2. Edit only prose in an existing `PRESENT` abstract or `PRESENT` draft paragraph. The UI must not silently edit logical/section/subsection/paragraph IDs, section/subsection order, evidence IDs, source paths/JSON Pointers, grounding labels, missing/conflict markers, author-question relationships, or canonical metadata/notices. Text editing creates no new evidence or stronger grounding.
3. Track immutable draft revisions and separate `UNREVIEWED` / `REVIEWED` / `NEEDS_CHANGES` section review records in active browser memory. These records are local session state, not formal audited approval; show selected revision, unsaved changes, validation result, review state, and export target.
4. Validate the exact selected edited revision against canonical schema and business/grounding rules using its original analysis, then revalidate server-side immediately before DOCX rendering. Recompute abstract word count and enforce at most 150 words.
5. Provide failure/recovery UI, offline backend integration tests, and offline Playwright browser E2E/responsive/interaction tests using only the approved `@playwright/test` development dependency.
6. Preserve an explicitly `MISSING` generated title and its confirmation marker when no candidate was selected. Post-analysis title selection and arbitrary title editing are outside P0-006.

## 6. Scope — Out

No replacement of existing upload/process/export pipeline; no changes to canonical AI-001/AI-003 schema, prompts, model/provider policy, DOCX template, or approved section order. No post-analysis title-selection provider workflow or arbitrary title edit. No production authentication or multi-tenant system; no localStorage, IndexedDB, database, filesystem revision store, or server-side durable review store. No Claims, prior-art search, OCR, analytics, deployment, background queue, WebSockets, collaboration, comments, or unrelated redesign.

## 7. Dependencies

| Dependency | Evidence | Required role |
|---|---|---|
| P0-005 CLOSED | Accepted `4390721`; closeout `ec4db79` | Existing frontend baseline |
| APP-003 implementation accepted | `3e7c291` merged by `b5a47f6`, 32/32 AC and independent PASS in merge message | Validated analysis/draft generation and source cleanup |
| DOC-001 renderer and P0-003 composition | DOC-001 PR #7 evidence in `docs/system-specification.md`; P0-003 `e891c38` merged by `5cfb1b5` | Canonical DOCX output |
| P0-004 local HTTP boundary | `0f5799b` merged by `43737a7` | Existing opt-in upload/metadata/process/export contract |
| P0-006 specification review and Human decisions | v0.1.0: Gemini 3.8 Flash High `PASS WITH HUMAN DECISIONS REQUIRED`, findings `NONE`; HD-P0-006-01…07 now approved | v0.2.0 targeted re-review remains before separate Human implementation approval |

## 8. Blockers

- P0-006 implementation remains NOT STARTED until targeted independent re-review of v0.2.0 and separate Human implementation approval. The seven Human decision questions in v0.1.0 are RESOLVED.
- Local review state is not formal section approval or authenticated actor attribution. Any future audited approval/persistence policy requires a separate task and Human decision.
- BLK-003 (production auth/private storage/retention) blocks real or unpublished research data and production use, but does not block synthetic-only local specification review.
- GOV-P0-006-01 requires governance reconciliation; merged APP-003 technical acceptance is established by `b5a47f6`, so the stale document text alone does not require reimplementation.

## 9. Architecture boundary

```text
Browser (local session: canonical analysis + draft, edit revisions, review UI)
  -> Next.js same-origin /backend/* rewrite
  -> FastAPI opt-in local HTTP boundary
  -> existing APP-003 process and P0-003/DOC-001 renderer
```

Human review metadata must be a separate session record, never an AI-generated field in the canonical draft. Keep the original generated analysis/draft immutable in browser memory; revisions derive from a copy. Any backend validation must fail closed. Client-side hints are not authority for schema, grounding, or export eligibility, and P0-006 does not establish authenticated reviewer identity.

## 10. API / frontend contracts

| Operation | Current contract | Approved P0-006 requirement |
|---|---|---|
| Upload | `POST /api/documents`, multipart `file` | Reuse without change. |
| Metadata | `GET /api/documents/{id}` while source registry exists | Reuse only for pre-process lookup/recovery; do not promise retrieval after cleanup. |
| Process | `POST /api/documents/{id}/process`, optional `selected_title_candidate_id`; returns `analysis`, `draft`, `metadata` | Reuse; retain the returned canonical analysis in local session for validation. No repeat process call to edit. |
| Edited-draft validation | No public endpoint | Add opt-in local `POST /api/drafts/validate`. Request carries original analysis, exact edited draft/revision identifier, and `selected_title_candidate_id` when applicable. Backend applies canonical schema, existing business/grounding rules, and recomputed abstract word count (at most 150); return safe validation result/field paths and correlation ID. No model/provider call. |
| DOCX export | `POST /api/exports/docx` with `{draft}` | Preserve route and reuse existing renderer/template. Submit the exact selected revision plus original analysis/selection context needed for authoritative server-side revalidation immediately before rendering; reject invalid revision without creating DOCX. The backend must not trust a prior client-side validation claim. `UNREVIEWED` does not block technically valid export; review state remains visible and outside canonical draft. |
| Errors | `{error:{code,message,correlation_id}}` | Preserve safe messages and correlation ID; provide field paths without leaking payloads. Distinguish invalid edit, stale revision, unavailable backend, render failure, and uncertain synchronous process outcome. |

Client-supplied original analysis can support local internal-consistency checks but cannot authenticate a reviewer or prove provider provenance. This is a single-tenant local integrity boundary, not a production identity/audit boundary. No server-side durable review store is authorized.

## 11. State model

Local UI revision states: `READY_GENERATED -> EDITING -> DIRTY -> VALIDATING -> VALIDATED`, with `INVALID` and `EXPORTING/EXPORT_ERROR` branches. Section review status is a separate enum: `UNREVIEWED`, `REVIEWED`, `NEEDS_CHANGES`; it is not a `REVIEWED` validation state. Saving text creates a new immutable revision with fresh `UNREVIEWED` section statuses and no inherited validation. Earlier revisions remain historical within the active session; their validation/review cannot be displayed as applying to the new revision. Review-status changes do not themselves change draft prose or silently alter a technical validation result. Export identifies one exact revision that passed backend validation and has not since been edited; `UNREVIEWED` is not an export blocker, and `NEEDS_CHANGES` is never displayed as approval. Reload/reset/session loss may discard all in-memory revisions, validation and review state.

## 12. Human review/editing behavior

Show generated text alongside grounding/evidence and outstanding missing/conflict/inference items while editing. Preserve all unsupported-content warnings; do not promote `INFERENCE` to `SOURCE_FACT` or resolve missing/conflict items merely because text changed. Provide explicit save/cancel, revision selection, and visible section decision controls using only `UNREVIEWED`, `REVIEWED`, `NEEDS_CHANGES`. A session-local review record may bind exact revision ID, section ID, status and timestamp; it must not claim an authenticated actor or use audited `HUMAN_CONFIRMED`. Review state stays outside canonical AI-003 JSON. Export with `UNREVIEWED` sections is allowed when the selected revision passes backend validation and has no later edit. Show all outstanding statuses, keep the Human-review disclaimer, never render `NEEDS_CHANGES` as approved, and never change status as a side effect of export. DOCX download is not legal/formal approval or filing readiness.

## 13. Validation rules

- At `POST /api/drafts/validate` and again before DOCX render, apply canonical Patent Draft v1.0.0 JSON Schema and `validate_draft_business_rules(draft, analysis, selected_title_candidate_id=...)` to the exact submitted revision. Backend validation is authoritative; no provider call.
- Preserve required 11-part order, six technical sections and required subsections, logical IDs, source JSON Pointers, evidence closure/reverse usage, missing/conflict/author-question links, and draft notice.
- Recompute abstract `word_count` on text change; enforce the existing 150-word rule. Do not accept blank required prose, prohibited legal/Claims assertions, malformed pointers, or altered source metadata.
- Text edits do not automatically create new technical facts, evidence IDs, source paths, stronger grounding, or Human confirmation. If preserved support no longer justifies edited prose, backend validation must fail or the content must remain explicitly flagged; it must never silently pass as grounded. A flagged unsupported revision is not treated as validated grounded content.
- Validation success belongs to one exact revision ID/content. A subsequent text edit or source-analysis mismatch invalidates export eligibility; a review-status change alone does not. Server-side export revalidation closes the gap between an earlier validation response and the submitted DOCX payload. Review status is not a substitute for technical validation.

## 14. Error handling

Show safe field-level validation feedback and correlation ID; keep the unsent revision available in the current session after 422/5xx/network errors. On process failure, follow P0-005's reupload requirement because source cleanup may have occurred. On export failure, preserve the chosen revision and allow retry without repeating provider calls. Never present a timed-out or interrupted request as a successful process/export; avoid fabricated progress or approval state.

## 15. Security/privacy boundary

Local single-tenant synthetic/authorized fixtures only while BLK-003 remains open. The enablement flag and same-origin rewrite are not auth. Do not expose provider keys in browser, log full paper/analysis/draft/review payloads, or commit research data. Errors must not disclose local paths or raw source. Canonical output and DOCX keep Human-review/legal disclaimers. No provider call is needed to validate or export edits.

## 16. Data lifecycle / persistence boundary

Current frontend state is memory-only and reset clears it (`frontend/src/app/page.tsx`); upload source is deleted after pipeline, with TTL fallback; temporary export is removed after response. P0-006 revision/history, validation state and section review state must remain in memory for the active browser session only. Reload, reset or session loss may discard all of them; UI and documentation must state this plainly. No localStorage, IndexedDB, database, filesystem revision store or server-side durable review store is authorized. This is not durable approval evidence. Do not extend source upload retention to support editing.

## 17. Accessibility/responsive expectations

Keep keyboard-operable edit/review controls, visible focus, labels tied to fields, screen-reader announcements for save/validation/error states, and logical focus after failures. Preserve the P0-005 narrow layout and avoid hiding provenance or warning labels on small screens. Do not rely on color alone for review status.

## 18. Test strategy

- Offline backend contract tests: valid/invalid edited drafts, source mismatch, pointer/evidence closure, abstract count, export rejection without partial file, safe error/correlation ID, disabled flag route absence.
- Frontend interaction checks: edit/save/cancel, immutable memory-only revisions, stale validation/review invalidation, all three review statuses, selected-revision export, errors/recovery and keyboard labels. `@playwright/test` is the only newly approved frontend development dependency; do not add Jest, Vitest, React Testing Library, Cypress or another framework without separate Human approval.
- Playwright browser E2E with synthetic PDF and DOCX plus fake/offline runtimes: upload -> process -> inspect -> edit -> validate -> review -> export; test `UNREVIEWED` export, `NEEDS_CHANGES` display, rejected edit/export, reload loss and narrow viewport. No provider API calls.
- Run existing targeted backend tests (`test_document_upload.py`, `test_core_pipeline.py`, `test_core_pipeline_e2e_offline.py`, `test_patent_docx_renderer.py`, `test_pipeline_docx_integration.py`, `test_local_orchestration_api.py`) and existing frontend lint/build during implementation review. No implementation test is claimed in this specification-only task.

## 19. Acceptance Criteria

The following objective implementation gates incorporate all seven approved Human decisions. Implementation remains NOT STARTED pending targeted specification re-review and separate Human approval.

| ID | Objective test |
|---|---|
| AC-01 | Existing upload, metadata, process and DOCX routes still pass their current offline contract tests with the local flag on; flag off does not expose local routes. |
| AC-02 | Existing P0-005 same-origin `/backend/*` rewrite and safe error display work with the approved backend, without browser-visible provider secret or backend URL configuration. |
| AC-03 | A synthetic PDF and a synthetic DOCX can each reach read-only analysis/draft results through the existing process response without fixture data embedded in production UI. |
| AC-04 | UI edits only existing `PRESENT` abstract prose and `PRESENT` paragraph prose; logical/section/subsection/paragraph IDs, section/subsection order, evidence IDs, source paths, grounding labels, missing/conflict markers, author-question relationships and canonical metadata/notices remain unchanged. |
| AC-05 | Save creates a distinct immutable revision in active browser memory; generated revision remains unchanged and selectable; cancel leaves the prior revision unchanged. Reload/reset/session loss discards session history as documented. |
| AC-06 | A new text revision has no inherited validation and starts with `UNREVIEWED` section records; prior revision validation/review cannot appear current. Review-status changes do not edit canonical draft text or fabricate technical validation. |
| AC-07 | Each editable paragraph and abstract retains visible grounding, evidence IDs, source paths and outstanding review warnings while edited. |
| AC-08 | Opt-in `POST /api/drafts/validate` validates exact edited revision against original analysis using canonical schema, existing business/grounding rules and recomputed abstract word count at most 150; invalid or explicitly unsupported content does not silently pass as grounded; no provider call occurs. |
| AC-09 | DOCX export revalidates the exact submitted revision server-side before rendering; a stale, invalid, different (including older) or unsaved draft cannot be substituted for the selected revision. A technically valid revision may export with `UNREVIEWED` sections while outstanding statuses and disclaimer remain visible; export never changes review status or implies approval. Rejected export creates no DOCX; failure preserves session revision for retry. |
| AC-10 | Each local review record is outside AI-003 JSON and binds exact revision ID, section ID, `UNREVIEWED` / `REVIEWED` / `NEEDS_CHANGES`, and session timestamp; no authenticated actor, audited `HUMAN_CONFIRMED` or formal approval is claimed, and `NEEDS_CHANGES` is never displayed as approved. |
| AC-11 | Source cleanup after process, temporary DOCX cleanup and synthetic-only boundary continue to pass existing tests; editing does not keep uploaded source bytes. |
| AC-12 | Network/proxy/non-JSON/422/5xx failures display safe messages and correlation ID when available; no false success or leaked payload/path. |
| AC-13 | Offline Playwright keyboard and narrow-viewport tests complete edit, validation, review and export with visible status/warnings. |
| AC-14 | Offline backend integration and Playwright browser E2E cover edited export, `UNREVIEWED` export, rejected edit/export, all review statuses and session reload loss without provider API calls; only approved `@playwright/test` is added as a frontend development dependency. |
| AC-15 | UI/documentation state that edits, revisions, validation and local review may disappear on reload/reset/session loss; no durable storage or production/real-data readiness is claimed. |
| AC-16 | Frontend types preserve all canonical draft fields including `output_notice` and `drawings`; edit/export round trip does not discard unseen fields. |
| AC-17 | A process result without selected title stays visibly `MISSING` with its confirmation marker; no post-analysis title-selection workflow or arbitrary title edit is added, and UI does not invent or silently approve a title. |

## 20. Definition of Done

Specification v0.2.0 is ready for targeted independent re-review when all seven approved decisions are traceable through sections 5–19 and 22, v0.1.0 review history is preserved, and the documentation-only diff passes checks. Implementation may begin only after that gate and separate Human approval. Implementation DoD then requires AC-01…AC-17 with evidence, independent review of a fixed branch/SHA with exact reviewer model/profile, version/API documentation aligned with code, no secret or confidential fixture committed, and separate Human merge/release approval.

## 21. Explicit non-goals

No new AI generation capability, post-analysis title-selection provider flow, arbitrary title editing, prompt/schema/template revision, content invention, Claims, patentability/legal conclusion, formal audited approval, durable revision storage, real-data readiness, public deployment, new auth system, or generalized document repository. This task does not reopen P0-005 review or APP-003 implementation.

## 22. Approved Human decisions

v0.1.0 received Gemini 3.8 Flash High independent `PASS WITH HUMAN DECISIONS REQUIRED`, findings `NONE`. Human / Product Owner subsequently approved every decision below; the decision gate is **RESOLVED**. This records scope approval, not implementation approval.

| ID | Status | Approved requirement |
|---|---|---|
| HD-P0-006-01 | APPROVED | Edit only existing `PRESENT` abstract/paragraph prose; preserve all canonical IDs, order, evidence, pointers, labels, markers, question links, metadata and notices. Unsupported edited prose must fail backend validation or remain explicitly flagged, never silently gain grounding. |
| HD-P0-006-02 | APPROVED | Session-only `UNREVIEWED`, `REVIEWED`, `NEEDS_CHANGES` records outside canonical draft, bound to revision/section/status/timestamp; no authenticated actor, audited `HUMAN_CONFIRMED` or formal approval claim. |
| HD-P0-006-03 | APPROVED | Export requires authoritative validation of exact selected revision and no later edit; `UNREVIEWED` does not automatically block. Show outstanding review state and disclaimer; `NEEDS_CHANGES` never means approved and export never changes status. |
| HD-P0-006-04 | APPROVED | Revisions/history, validation and review state in active browser memory only; reload/reset/session loss may discard them. No localStorage, IndexedDB, database, filesystem revision store or server-side durable review store; source cleanup unchanged. |
| HD-P0-006-05 | APPROVED | Add opt-in local `POST /api/drafts/validate` with original analysis, exact edited draft and selected title ID when applicable; backend applies schema, business/grounding and abstract count without provider call. DOCX export authoritatively revalidates exact submitted revision before using existing renderer/template. Client analysis is not authenticated provenance. |
| HD-P0-006-06 | APPROVED | `@playwright/test` may be added only as a development dependency for offline browser E2E/responsive/interaction tests; no other frontend test framework without separate evidenced blocker and Human approval. |
| HD-P0-006-07 | APPROVED | Post-analysis title selection and arbitrary title edit are out of scope. Preserve truthful canonical `MISSING` title/confirmation marker when no candidate was selected; future workflow needs separate scope and Human approval. |

## 23. Proposed implementation branch name

`feat/p0-006-frontend-backend-integration`, created only after targeted specification re-review and separate Human implementation approval, from an approved base containing the accepted P0-005, APP-003, P0-003 and P0-004 commits.

## 24. Proposed independent-review gate

v0.1.0 was independently reviewed by Gemini 3.8 Flash High: `PASS WITH HUMAN DECISIONS REQUIRED`, findings `NONE`; Human has resolved HD-P0-006-01…07. Targeted independent re-review of this v0.2.0 fixed commit must verify faithful incorporation, AC consistency, and unchanged technical/security boundaries; record exact reviewer model/profile, evidence and findings. Only after that and separate Human implementation approval may code work start. Later, independently review a fixed implementation SHA for all ACs, synthetic offline integration and Playwright E2E, security/privacy, versioned edits, source-grounding validation and regression. Reviewer `PASS` does not substitute for Human merge/release approval.
