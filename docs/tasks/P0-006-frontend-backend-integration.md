# P0-006 — Frontend/Backend Integration Specification and Current-State Audit

## 1. Metadata

| Field | Value |
|---|---|
| Task ID | P0-006 |
| Specification version | 0.1.0 |
| Status | Specification — Draft for Independent Review |
| Implementation status | BLOCKED / NOT STARTED pending specification review, Human decisions, and task approval |
| Owner / author | Human / Product Owner; Codex draft |
| Reviewer | Independent reviewer to be assigned; exact model/profile not yet known |
| Date | 27/09/2026 |
| Source of truth | This Git file; audit baseline `ec4db79af8d0511a2888e176d45defefdc3828dc` |
| Related tasks | P0-005, APP-003, P0-003, P0-004, DOC-001 |
| P0-005 accepted implementation | `43907213f14c8c55294f55af34afcc0cbcc9dc66` |
| P0-005 closeout | `ec4db79af8d0511a2888e176d45defefdc3828dc` |

### Change history

| From | To | Date | Author | Change | Reason | Related decision/finding | Breaking change |
|---|---|---|---|---|---|---|---|
| None | 0.1.0 | 27/09/2026 | Codex | Initial current-state audit and proposed integration contract | Define the actual remaining P0-006 work before implementation | P0-005 closeout; governance issue GOV-P0-006-01 | No production contract changed |

This document is a proposal, not Human approval to implement, change data policy, or release.

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

P0-005 displays canonical results and exports the returned draft unchanged. `frontend/README.md` explicitly defers draft editing and versioned Human approval to P0-006. The current `PatentDraftView` renders text and provenance without edit controls; `ResultWorkspace` exports `result.draft`. No edit revision, section decision, actor attribution, or review audit state is present. The AI-003 canonical schema intentionally excludes Human approval state. The current export endpoint validates schema only, so a schema-valid edited draft could bypass the source-linked business rules enforced during generation. Also, `page.tsx:handleProcess` sends no `selected_title_candidate_id`; the synchronous process creates analysis and draft together, before the UI can show title candidates. Under `draft_business_validation.py`, absent selection requires a `MISSING` title marker. A post-analysis title-selection workflow would require a separately approved contract.

## 5. Scope — In

1. Finish the existing local frontend/backend contract for edited-draft validation and export, including complete frontend types for the canonical payload, without duplicating upload, process, result transport, or rendering.
2. Allow controlled edits to existing `PRESENT` abstract and technical paragraph text. Preserve IDs, section order, source paths, grounding labels, evidence IDs, missing markers, and unresolved conflicts. Title selection remains the existing pipeline choice; arbitrary title editing is excluded because `validate_draft_business_rules` requires exact selected-candidate identity.
3. Track immutable draft revisions and separate per-section Human review decisions in a local session. Show the selected revision, unsaved changes, validation result, and export target clearly.
4. Validate the exact selected edited revision against canonical schema and business/grounding rules using its original analysis before DOCX export. Recalculate the abstract word count and reject an abstract over 150 words.
5. Provide failure/recovery UI and offline integration/browser tests for edit, validation, review, and export.
6. Preserve an explicitly `MISSING` generated title when no candidate was selected; resolve any new title-selection workflow only through HD-P0-006-07.

## 6. Scope — Out

No replacement of existing upload/process/export pipeline; no changes to canonical AI-001/AI-003 schema, prompts, model/provider policy, DOCX template, or approved section order. No production authentication or multi-tenant system; no Supabase/PostgreSQL by default; no Claims, prior-art search, OCR, analytics, deployment, background queue, WebSockets, collaboration, comments, or unrelated redesign.

## 7. Dependencies

| Dependency | Evidence | Required role |
|---|---|---|
| P0-005 CLOSED | Accepted `4390721`; closeout `ec4db79` | Existing frontend baseline |
| APP-003 implementation accepted | `3e7c291` merged by `b5a47f6`, 32/32 AC and independent PASS in merge message | Validated analysis/draft generation and source cleanup |
| DOC-001 renderer and P0-003 composition | DOC-001 PR #7 evidence in `docs/system-specification.md`; P0-003 `e891c38` merged by `5cfb1b5` | Canonical DOCX output |
| P0-004 local HTTP boundary | `0f5799b` merged by `43737a7` | Existing opt-in upload/metadata/process/export contract |
| Independent P0-006 specification review and Human scope decision | Not yet recorded | Gate before implementation |

## 8. Blockers

- P0-006 **implementation** remains BLOCKED / NOT STARTED until independent specification review and Human approval of this task's scope.
- Human decisions in section 22 are required before implementing formal section approval, attribution, export gating, or any persistence policy. The specification does not treat an unauthenticated click as audited approval.
- BLK-003 (production auth/private storage/retention) blocks real or unpublished research data and production use, but does not block synthetic-only local specification review.
- GOV-P0-006-01 requires governance reconciliation; merged APP-003 technical acceptance is established by `b5a47f6`, so the stale document text alone does not require reimplementation.

## 9. Architecture boundary

```text
Browser (local session: canonical analysis + draft, edit revisions, review UI)
  -> Next.js same-origin /backend/* rewrite
  -> FastAPI opt-in local HTTP boundary
  -> existing APP-003 process and P0-003/DOC-001 renderer
```

Human review metadata must be a separate application-owned record, never an AI-generated field in the canonical draft. Keep the original generated analysis/draft immutable in the session; revisions derive from a copy. Any backend validation must fail closed. Client-side hints are not authority for schema, grounding, review identity, or export eligibility.

## 10. API / frontend contracts

| Operation | Current contract | P0-006 proposed delta |
|---|---|---|
| Upload | `POST /api/documents`, multipart `file` | Reuse without change. |
| Metadata | `GET /api/documents/{id}` while source registry exists | Reuse only for pre-process lookup/recovery; do not promise retrieval after cleanup. |
| Process | `POST /api/documents/{id}/process`, optional `selected_title_candidate_id`; returns `analysis`, `draft`, `metadata` | Reuse; retain the returned canonical analysis in local session for validation. No repeat process call to edit. |
| Edited-draft validation | No public endpoint | Proposed local, opt-in `POST /api/drafts/validate` with `{analysis, draft, selected_title_candidate_id}`; return safe `valid`/field-path errors and correlation ID. Exact path/shape requires Human API approval. It must apply canonical schema plus `validate_draft_business_rules`, with no provider call. |
| DOCX export | `POST /api/exports/docx` with `{draft}` | Preserve the route. Proposed extension submits the selected revision and source analysis/selection for server-side business validation before render; reject invalid payload without file creation. Exact request and review-gate fields require Human approval. Do not silently equate current schema-only validation with edited-draft validation. |
| Errors | `{error:{code,message,correlation_id}}` | Preserve safe messages and correlation ID; provide field paths without leaking payloads. Distinguish invalid edit, stale revision, unavailable backend, render failure, and uncertain synchronous process outcome. |

The stateless client-supplied analysis proposal verifies internal consistency but cannot authenticate a reviewer or prove that the analysis was the original provider result. Production-grade identity/audit would require separately approved server state and auth. Do not claim that the local contract provides such assurance.

## 11. State model

Proposed local UI states: `READY_GENERATED -> EDITING -> DIRTY -> VALIDATING -> VALIDATED -> REVIEWED` for each revision, plus `INVALID` and `EXPORTING/EXPORT_ERROR`. A text edit creates a new immutable revision after save and invalidates prior validation and review decisions for that revision. The original generated revision remains selectable. Export identifies a single validated revision; response errors do not silently change the selected revision. Server restart, page reload, or session reset has the data-loss behavior to be decided in section 22.

## 12. Human review/editing behavior

Show the generated text alongside grounding/evidence and outstanding missing/conflict/inference items while editing. Preserve all unsupported-content warnings; do not promote `INFERENCE` to `SOURCE_FACT` or mark missing/conflict items resolved merely because text changed. Provide explicit save/cancel, revision selection, and visible section decision controls. Separate review decisions from the canonical draft; record actor/time/revision only when an approved local attribution mechanism exists. Exact status vocabulary and whether all sections must be confirmed before export remain Human decisions. A downloaded editable DOCX remains a draft; downloading is not approval.

## 13. Validation rules

- Apply the canonical Patent Draft v1.0.0 JSON Schema, then `validate_draft_business_rules(draft, analysis, selected_title_candidate_id=...)` to the selected revision before export.
- Preserve required 11-part order, six technical sections and required subsections, logical IDs, source JSON Pointers, evidence closure/reverse usage, missing/conflict/author-question links, and draft notice.
- Recompute abstract `word_count` on text change; enforce the existing 150-word rule. Do not accept blank required prose, prohibited legal/Claims assertions, malformed pointers, or altered source metadata.
- Text edits do not automatically create new technical facts, evidence IDs, source paths, or Human confirmation. Any change that cannot keep the existing grounding truthful must remain flagged for Human/author review and must not be exported as validated evidence.
- Validation success belongs to one revision hash/version. A subsequent edit, source-analysis mismatch, or review-state change invalidates its export eligibility according to the approved gate.

## 14. Error handling

Show safe field-level validation feedback and correlation ID; keep the unsent revision available in the current session after 422/5xx/network errors. On process failure, follow P0-005's reupload requirement because source cleanup may have occurred. On export failure, preserve the chosen revision and allow retry without repeating provider calls. Never present a timed-out or interrupted request as a successful process/export; avoid fabricated progress or approval state.

## 15. Security/privacy boundary

Local single-tenant synthetic/authorized fixtures only while BLK-003 remains open. The enablement flag and same-origin rewrite are not auth. Do not expose provider keys in browser, log full paper/analysis/draft/review payloads, or commit research data. Errors must not disclose local paths or raw source. Canonical output and DOCX keep Human-review/legal disclaimers. No provider call is needed to validate or export edits.

## 16. Data lifecycle / persistence boundary

Current frontend state is memory-only and reset clears it (`frontend/src/app/page.tsx`); upload source is deleted after pipeline, with TTL fallback; temporary export is removed after response. P0-006 proposes in-memory revision history for the local session only as the minimal baseline. It is not durable approval evidence and must not be presented as such. No localStorage/IndexedDB, database, or new filesystem store is authorized by this draft. If durable revision/audit retention is required, Human must approve storage, access, deletion, and retention before implementation. Do not extend source upload retention to support editing.

## 17. Accessibility/responsive expectations

Keep keyboard-operable edit/review controls, visible focus, labels tied to fields, screen-reader announcements for save/validation/error states, and logical focus after failures. Preserve the P0-005 narrow layout and avoid hiding provenance or warning labels on small screens. Do not rely on color alone for review status.

## 18. Test strategy

- Offline backend contract tests: valid/invalid edited drafts, source mismatch, pointer/evidence closure, abstract count, export rejection without partial file, safe error/correlation ID, disabled flag route absence.
- Frontend component tests: edit/save/cancel, immutable revisions, review-decision invalidation, export of selected revision, errors and recovery, keyboard labels. Add only the smallest test tooling justified by the implementation plan; dependency changes require Human approval.
- Browser E2E with synthetic PDF and DOCX plus fake/offline runtimes: upload -> process -> inspect -> edit -> validate -> review -> export; negative flow and narrow viewport. Do not call live provider APIs.
- Run existing targeted backend tests (`test_document_upload.py`, `test_core_pipeline.py`, `test_core_pipeline_e2e_offline.py`, `test_patent_docx_renderer.py`, `test_pipeline_docx_integration.py`, `test_local_orchestration_api.py`) and existing frontend lint/build during implementation review. No implementation test is claimed in this specification-only task.

## 19. Acceptance Criteria

The following are proposed implementation gates; choices marked as Human decisions in section 22 must be resolved before implementation acceptance.

| ID | Objective test |
|---|---|
| AC-01 | Existing upload, metadata, process and DOCX routes still pass their current offline contract tests with the local flag on; flag off does not expose local routes. |
| AC-02 | Existing P0-005 same-origin `/backend/*` rewrite and safe error display work with the approved backend, without browser-visible provider secret or backend URL configuration. |
| AC-03 | A synthetic PDF and a synthetic DOCX can each reach read-only analysis/draft results through the existing process response without fixture data embedded in production UI. |
| AC-04 | An editor can change only approved prose fields; IDs, title candidate identity, evidence/source links, section order, notices and missing/conflict markers cannot be silently changed through the UI. |
| AC-05 | Saving an edit creates a distinct selectable revision; the generated revision is retained unchanged in the active session; cancel leaves the prior revision unchanged. |
| AC-06 | Any edit invalidates the edited revision's previous validation and review decision; the UI cannot present stale approval/validation as current. |
| AC-07 | Each editable paragraph and abstract retains visible grounding, evidence IDs, source paths and outstanding review warnings while edited. |
| AC-08 | Backend rejects schema-invalid or business/grounding-invalid edited drafts with a safe structured error and no DOCX file; abstract word count mismatch or more than 150 words is rejected. |
| AC-09 | The exact selected validated revision is rendered to DOCX; a prior or unsaved revision is not substituted; export failure keeps the revision available for retry. |
| AC-10 | Human review decisions are stored outside AI-003 payload and tied to an exact revision; status vocabulary, attribution and export gate follow recorded Human decisions rather than inferred defaults. |
| AC-11 | Source cleanup after process, temporary DOCX cleanup and synthetic-only boundary continue to pass existing tests; editing does not keep uploaded source bytes. |
| AC-12 | Network/proxy/non-JSON/422/5xx failures display safe messages and correlation ID when available; no false success or leaked payload/path. |
| AC-13 | Keyboard and narrow-viewport browser tests can complete edit, validation, review and export with visible status and warnings. |
| AC-14 | Offline integration and browser E2E tests cover a successful edited export and at least one rejected edit/export flow without provider API calls. |
| AC-15 | Documentation states session data-loss behavior and unresolved production controls; no production/real-data readiness claim is made. |
| AC-16 | Frontend types preserve all canonical draft fields including `output_notice` and `drawings`; edit/export round trip does not discard unseen fields. |
| AC-17 | A process result without selected title stays visibly `MISSING` with its confirmation marker; UI does not invent or silently approve a title. |

## 20. Definition of Done

After separate Human approval to implement: all resolved ACs pass with test evidence; independent review of fixed branch/SHA records exact reviewer model/profile and resolves blockers; version/change log and API docs match code; no secret or confidential fixture is committed; Human approves merge/release separately. This draft specification itself is ready for independent review when its evidence, open decisions and governance issue are visible and the documentation-only diff passes checks.

## 21. Explicit non-goals

No new AI generation capability, prompt/schema/template revision, arbitrary content invention, Claims, patentability/legal conclusion, real-data readiness, public deployment, new auth system, or generalized document repository. This task does not reopen P0-005 review or APP-003 implementation.

## 22. Open decisions requiring Human approval

| ID | Decision | Why it matters | Proposed default for review; not approved |
|---|---|---|---|
| HD-P0-006-01 | Exact editable fields and treatment of text whose existing evidence no longer supports it | Grounding integrity | Existing `PRESENT` abstract and paragraph prose only; unsupported changes fail validation/remain flagged. |
| HD-P0-006-02 | Section status vocabulary, actor attribution, and whether in-memory decisions count as formal approval | AGENTS.md requires audit evidence for `HUMAN_CONFIRMED` | Treat in-memory clicks as local review notes, not formal audited approval. |
| HD-P0-006-03 | Whether every section must be approved before export or an explicitly marked unapproved draft may export | `docs/system-specification.md:UC-005` leaves this unresolved | No silent approval; retain draft notice and require an explicit decision before any gate is coded. |
| HD-P0-006-04 | Revision retention and recovery after reload/restart, plus deletion SLA | Current P0-005 session memory is non-durable; BLK-003 remains open | No durable persistence until approved. |
| HD-P0-006-05 | Exact public validation/export request contract and handling of client-supplied analysis | Existing export is schema-only and stateless | Local opt-in validation with original analysis, with explicit limits on provenance assurance. |
| HD-P0-006-06 | Any new frontend test dependency | Project rules require approval for dependencies | Prefer existing tools; approve a narrowly justified browser test tool only if needed. |
| HD-P0-006-07 | Whether selecting a title after analysis belongs to P0-006 | Current one-call process drafts before the user sees candidates; arbitrary title edits violate selected-candidate identity | Keep the truthful `MISSING` title in this scope unless Human approves a distinct analysis-to-draft contract and its provider/cost effects. |

## 23. Proposed implementation branch name

`feat/p0-006-frontend-backend-integration`, created only after specification review and Human implementation approval, from an approved base containing the accepted P0-005, APP-003, P0-003 and P0-004 commits.

## 24. Proposed independent-review gate

Review this specification at a fixed commit first. Record exact Antigravity reviewer model/profile, evidence and findings; Human decides the open scope/API/data questions. After implementation is authorized, independently review a fixed implementation SHA for all ACs, synthetic offline integration and browser E2E, security/privacy, versioned edits, source-grounding validation and regression. Reviewer `PASS` does not substitute for Human merge/release approval.
