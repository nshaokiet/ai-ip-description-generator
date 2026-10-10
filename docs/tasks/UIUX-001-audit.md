# UIUX-001 — Verified Frontend Audit

| Field | Value |
| --- | --- |
| Task / document | UIUX-001 / Audit v0.1.0 |
| Baseline | `a821716e63d0f3b3c87f594f42071bf937d590c9` (GitHub `main`, verified 2026-10-10) |
| Authorization | Human UIUX-001 specification-only instruction, 2026-10-10 |
| Workflow / owner | V1; Codex specification owner |
| Review target | Gemini 3.1 Pro High / Antigravity, STRICT READ-ONLY, fixed specification SHA |
| Evidence type | Static source inspection on exact GitHub baseline; no live visual or accessibility audit executed |
| Status | Proposed findings for independent specification review; frontend unchanged |

## 1. Scope and evidence hierarchy

The audit treats the source at the exact baseline commit as the observed state; recommended UX is separately labelled **proposal**. Source of truth: `AGENTS.md` §§8, 11, 19, 24; `PROJECT_CONTEXT.md`; `docs/system-specification.md`; `README.md`; `docs/tasks/P1-006-ux-polish.md`; `docs/tasks/P2-000-product-webapp-simplification.md`; `docs/tasks/P2-005-uspto-v2-draft-assembly.md`; `docs/tasks/P2-006-uspto-b2-pdf-docx-rendering.md`; and the paths below. P2-006 was merged in PR #101 and has an **internal offline** B2 reference/application renderer; this does not introduce a public frontend v2 export endpoint. Review its final closeout and `docs/tasks/P2-006-reference-qa.md` before future integration decisions.

Inspected frontend sources: `frontend/src/app/page.tsx`, `layout.tsx`, `globals.css`; `frontend/src/components/WorkflowProgress.tsx`, `UploadPanel.tsx`, `ResultWorkspace.tsx`, `AnalysisView.tsx`, `PatentDraftView.tsx`, `ReviewItemsView.tsx`, `EvidenceCard.tsx`, `GroundingBadge.tsx`; `frontend/src/lib/api/client.ts`, `draftRevisions.ts`; browser suites `frontend/e2e/integration.spec.ts`, `frontend/e2e-demo/demo-staging.spec.ts` and `frontend/e2e/performance.spec.ts`. These tests are **inspected**, not rerun or claimed passing here.

## 2. Actual screen, state and contract inventory

| Screen / owner | Confirmed present | Constraint / important boundary |
| --- | --- | --- |
| Shell / `page.tsx` + `layout.tsx` | Official PNG at `/brand/vnuhcm-innovation-hub-logo.png`, product name, hero, footer, five-stage stepper and Back | Header has no theme/locale controls; root `html` is `lang="en"` (`layout.tsx:12`). |
| Upload / `UploadPanel.tsx` | Drag/drop, picker, preflight .pdf/.docx, 10 MiB upper bound, nonempty, selected-file removal, uploaded metadata, replace/remove, destructive reset warning | File selected and backend accepted are separate states; `demoStaging` prevents arbitrary paper submission and offers controlled samples. `UploadPanel.tsx:5-19, 91-199, 200-327`. |
| Extraction / `page.tsx` | Upload → process; busy/error handling; revisiting completed analyze does not reprocess | Backend can invalidate source after process failure, requiring new upload (`page.tsx:151-172`). |
| Navigation / `WorkflowProgress.tsx` | `upload/analyze/review/validate/export`, reachable phase gating, aria-current, disabled future steps | “Complete” status currently depends on position/reachability; distinguish true completion, available and needs-attention in redesign. `WorkflowProgress.tsx:3-55`. |
| Review / `ResultWorkspace.tsx` | Draft / Review Items / Analysis tabs; session revision selector; edit/save/cancel; human per-section statuses; validation eligibility; technical details | Tab switching hides evidence while editing; not a persistent 3-area research workspace. `ResultWorkspace.tsx:45-105, 370-430`. |
| Draft / `PatentDraftView.tsx` | Title, abstract, patent sections/subsections, edit prose textareas, grounding indicators, missing markers, evidence appendix, per-section review controls | Certain prose fields are editable; do not promise free editing of every schema field, title, Claims or underlying evidence. `PatentDraftView.tsx:28-75, 97-204`. |
| Evidence / `EvidenceCard.tsx` + `GroundingBadge.tsx` | Evidence excerpt, locator page/section/paragraph/chunk/table/figure, usage references, grounding label | Long appendix / analysis cards require context switching to correlate evidence with draft paragraph. `EvidenceCard.tsx:3-48`. |
| Validation / `ResultWorkspace.tsx` | Exact saved revision request, server validation, digest, success, error paths and edit recovery | `valid` and matching `revision_id` required. Review-complete prerequisite preserved. `ResultWorkspace.tsx:128-157, 238-301`. |
| Export / `ResultWorkspace.tsx` + `client.ts` | Existing `POST /backend/api/exports/docx`; browser downloads `patent-description-draft.docx` after eligible review and validation | This is v1 frontend DOCX export; P2-006 B2 PDF/DOCX and USPTO application output are separate offline internal artifacts. `client.ts:8-9, 156-166`; `ResultWorkspace.tsx:303-348`. |
| Demo / `page.tsx` + `client.ts` | `NEXT_PUBLIC_DEMO_STAGING=1`; controlled samples at `/api/demo/samples/{id}`; disclosure that arbitrary uploads are UI-only | No evidence of paid production provider or real-paper conversion. `page.tsx:26`, `UploadPanel.tsx:234-277`, `README.md` “Public Demo”. |

Existing accessibility and safety protections to retain: `:focus-visible`, alert/focus recovery, progress live region, tab roving focus, keyboard tests, rate-limit/error sanitization, per-revision review/validation locks and warnings that output requires Human/IP specialist review. The review statuses `REVIEWED` do not mean source-proven or legally approved. `draftRevisions.ts` holds revisions **in browser component state only**; it does not persist after reload.

## 3. Evidence-backed UX findings

Severity expresses user impact relative to the authorized proposed design; it is **not** an assertion that existing tests fail. AC IDs refer to `UIUX-001-specification.md`.

| ID / severity | Verified current behavior (source) | User impact | Proposed improvement / measurable criterion | Regression / compatibility risk |
| --- | --- | --- | --- | --- |
| F01 **High** | Header has logo/name only (`page.tsx:231-249`), English-only copy (`WorkflowProgress.tsx:3-9`); `layout.tsx:12` fixes English root lang. | Vietnamese users cannot choose consistent UI language. | Typed VI/EN dictionary, first visit VI, selection persistence and correct document `lang`; AC-16/17. | Avoid reloading document and translating user/source text. |
| F02 **High** | `globals.css:1-22` defines single palette; no current color-mode control in header. | No dark or OS theme experience. | Light/Dark/System tokens, default System, no flash, responsive to OS, state-preserving; AC-14/15. | SSR hydration, contrast, editor input surfaces. |
| F03 **High** | Review is tabs `draft/review/analysis` (`ResultWorkspace.tsx:94-105, 386-430`); evidence appendix below draft (`PatentDraftView.tsx`). | Reviewer loses simultaneous draft/evidence context and must scroll or switch views. | Desktop section rail + draft + evidence/validation inspector, responsive drawer; AC-06/25. | Existing tab and per-section review semantics must survive. |
| F04 **High** | Hero describes paper upload/extraction generically (`page.tsx:252-259`); demo limitation appears below file selector (`UploadPanel.tsx:234-277`). | Initial promise may be interpreted as real arbitrary-paper conversion before seeing demo notice. | Place concise capability banner adjacent to primary CTA and exact action status; AC-02/23. | Never activate provider/API or overstate v2 export. |
| F05 **Medium** | A single stage stepper presents `current/complete/reachable/upcoming` (`WorkflowProgress.tsx`); review/validation need separate gates (`page.tsx:56-76`). | “Completed” and “available” are visually easy to conflate. | Explicit states and action required, maintain reachability invariant; AC-04. | Do not permit bypass or reprocessing. |
| F06 **Medium** | Replacement/reset confirmation is an inline `role="alert"` block (`UploadPanel.tsx:152-175`); new-paper has similar block (`ResultWorkspace.tsx:178-190`). | Focus and destructive impact are less structured than a modal pattern. | Consistent labelled confirmation dialog/focus return for downstream reset; AC-05/10. | Preserve user choice, especially during edit. |
| F07 **High** | Editing has `editBuffer`/dirty comparison, save new revision, cancel (`ResultWorkspace.tsx:56-61, 114-128`), but there is no evidence of navigation/reload unsaved loss interception. | Accidental state loss can discard in-progress prose. | Unsaved-change guard for destructive navigation, reload warning where technically supported; AC-06/07. | Do not invent autosave, server persistence, or bypass browser restrictions. |
| F08 **Medium** | Server validation errors show code, message and JSON-like field paths with a general “Edit this revision” action (`ResultWorkspace.tsx:275-300`). | User must locate a field manually. | Map safe server paths to section labels and focusable targets with fallback; AC-07/25. | Preserve exact server rule/paths and correlation ID, never mask blocker. |
| F09 **Medium** | `EvidenceCard` shows locator/quote and `GroundingBadge` marks label; draft links show IDs without inspect-in-context action (`PatentDraftView.tsx:66-70, 123-126`). | Evidence provenance is difficult to compare against a paragraph. | Contextual inspector with locator/quote and “back to field”; AC-06/24. | No relabeling inference as supported fact. |
| F10 **Medium** | 2,219-line `globals.css` contains repeated selectors such as `.site-header`, `.hero`, `.workflow-progress` and media queries at 900/620/980/700/420 px. | Design additions could be brittle due to cascade collisions. | Organize tokens/foundations/components/responsive layers without a framework migration; AC-09/26. | Visual regressions across existing breakpoints. |
| F11 **Medium** | Export UI prominently offers “Download editable DOCX” after exact revision validation (`ResultWorkspace.tsx:303-348`). | Users may mistake v1 DOCX for P2-006 B2 reference PDF/DOCX or filing-ready output. | Explicit format/runtime/provenance labels; unavailable advanced formats disabled/informational; AC-08/23/24. | Do not alter export contract or promise real-figure support. |
| F12 **Medium** | Layout is largely centered and uses card/tab sequences; `globals.css` defines 1200 px content cap and responsive breakpoints; no original side patterns in shell source. | Wide margins are empty on 1440/1920 px. | Two original margin-only motifs, science left/patent right; AC-19–22. | Decorative layering must not cover clickable content. |
| F13 **Low** | English copy includes an isolated Vietnamese step subtitle and footer while no dictionary exists (`WorkflowProgress.tsx:5`; `page.tsx:359-362`). | Mixed-language affordances impede a consistent chosen locale. | Central copy/glossary and completeness checks; AC-17. | Preserve original scientific/evidence strings. |
| F14 **Medium** | The active stage and per-tab views are not a complete enumerated 16-state design contract, though functional branches exist (`page.tsx`, `ResultWorkspace.tsx`, browser tests). | Implementation choices are difficult to verify against one shared storyboard. | State inventory, wireframes, events, guard conditions and QA scenarios; AC-13/25. | Do not replace the existing state machine speculatively. |

## 4. Priorities, preservation and limits

**P0 proposals:** F01–F04, F07, F11; then evidence-centric F09, accessibility-safe F06/F08. **P1 polish:** refined step statuses, decorative variants and CSS restructuring, subject to the mandatory ACs. No demonstrated security vulnerability is claimed by this source-only audit. Accessibility compliance, contrast, actual browser screenshots and UX effectiveness remain **unverified until implementation QA**.

Keep existing `.pdf/.docx` and 10 MiB frontend preflight, backend as authoritative validator, `/backend` API endpoints, synthetic sample allowlist and no arbitrary-paper AI conversion, revision IDs and exact validation digest, review eligibility, grounding/evidence labels, anti-duplicate request controls, safe error normalization, visible draft warnings, the official VIH logo asset and current authorized DOCX download. Preserve all existing Playwright regression contracts while adapting copy-based selectors to the selected locale.

Do not treat an apparent “need” for login, paid provider integration, confidential paper handling, new storage, patent Claims editing, P2-006 export integration or USPTO filing semantics as authorized. Those are separate Human governance decisions. This audit makes **no claim that code, runtime tests, visual renders, or API contracts were changed**.

See [master specification](UIUX-001-specification.md) and [implementation/test plan](UIUX-001-implementation-plan.md).
