# UIUX-001 — Incremental Implementation & Verification Plan (Future Approval Only)

| Field | Value |
| --- | --- |
| Version | 0.1.0 |
| Date / baseline | 2026-10-10 / `a821716e63d0f3b3c87f594f42071bf937d590c9` |
| Task status | **Specification only**; implementation NOT AUTHORIZED |
| Design authority | [UIUX-001-specification.md](UIUX-001-specification.md) |
| Existing-state evidence | [UIUX-001-audit.md](UIUX-001-audit.md) |
| Workflow | V1 unless a separate future Human instruction explicitly enrolls task in V2 |

## 1. Goals, non-goals, and entry gate

Plan an additive UI adaptation of the existing Next.js / React / TypeScript frontend in five separately reviewable future work packages. Keep the currently deployed synthetic demo honest. No new backend/API, model/provider, paid spend, auth/storage/retention, real paper, Claims, schema, P2-006 public export, production deployment or changed legal/validation semantics. Existing official logo must remain unmodified. This document **does not implement or approve** any package.

**Future entry gate:** Human issues a new task ID, scope, acceptance criteria and authorization reference for implementation. Codex checks fresh main, active workflow governance, branch/lease, review/CI requirements, then opens implementation work. If the specification PR is reviewed and later merged, use its accepted merge SHA, not the present baseline, as the technical starting point.

## 2. Five sequential implementation packages and exit gates

| Phase / priority | Files and proposed component responsibilities | Concrete implementation steps | Minimum measurable exit gate |
| --- | --- | --- | --- |
| **1. Foundation — P0** | `app/layout.tsx`, `globals.css`, proposed `ThemeController`, `LocaleProvider`/typed `dictionaries`, `ProductHeader` | Preserve logo; semantic token layer; Light/Dark/System; preference restore and OS observer; prepaint approach compatible with static build; VI/EN dictionary, initial VI; screen-reader-selectable header controls; safe error message catalog. Keep controllers above workflow state without keying children. | 3 theme choices × 2 locales; saved preferences restored; no wrong-theme frame/hydration warning; no file/edit/revision reset; color contrast/focus pass in both resolved modes; existing static demo boot works; no missing keys. |
| **2. Home/upload/decor — P0** | `app/page.tsx`, `WorkflowProgress.tsx`, `UploadPanel.tsx`; proposed `CapabilityNotice`, `DecorativeMargins`, `ConfirmResetDialog` | Shorten hero; demo caveat beside CTA; distinguish select/upload/process; preserve 10 MiB/PDF/DOCX contract; safe remove/replace; original Science-left/Patent-right CSS/SVG behind outer margins; unreachable step explanations. | All upload states and exact synthetic-vs-arbitrary distinction; 390 px no overflow; decoration hit-test zero, both motifs wide desktop and hidden mobile; keyboard reset confirmation; no provider call for arbitrary public-demo selection. |
| **3. Review editor — P0** | `ResultWorkspace.tsx`, `PatentDraftView.tsx`, `EvidenceCard.tsx`, `GroundingBadge.tsx`, `ReviewItemsView.tsx`, `AnalysisView.tsx`, `lib/draftRevisions.ts`; proposed `SectionRail`, `EvidenceInspector`, `UnsavedChangesGuard` | Reuse existing session revision/validation functions; 3-area layout with drawers; section selection and evidence lookup by IDs; edit/save/cancel and dirty guard; preserve Human statuses/unverified edited prose warnings. Do not add new document field editing or persistence. | Keyboard-only edit → save revision → review; inspector shows exact linked quote; warning on unsaved destructive action; 390/768 layouts preserve editor and context; no current-revision/review/validation loss on theme/locale change. |
| **4. Validation/export UX — P0** | `ResultWorkspace.tsx`, `lib/api/client.ts` mapping presentation only; proposed `ValidationIssueList`, `ExportCapabilityPanel` | Convert safe server JSON paths to navigable section issues; preserve actual server response, revision ID/digest and gating; show v1 DOCX and inactive informational P2-006 formats; progress/success/error/retry with Human review disclaimer. | No validation or export bypass; exact revision match and digest preserved; failed export produces no download and retains validated revision; no enabled B2 PDF/application format; no false filing-ready language. |
| **5. Regression/a11y/polish — P0 quality gate, P1 details** | `e2e/integration.spec.ts`, `e2e-demo/demo-staging.spec.ts`, new focused theme/locale/a11y specs if authorized; CSS modular cleanup | Exhaustive deterministic P0 matrix below; assistive-technology and contrast checks; screenshots at 5 widths; cleanup repeated CSS rules only after matching snapshots; review dependency licenses if proposed. | Required scripts/build and Playwright suites PASS on final SHA; fixed-SHA independent review PASS; no Critical/High open findings; staging/public demo contracts unchanged. |

Do not add state libraries, i18n routers, CSS framework, icon packages or external illustration dependencies by default. React Context + hook + typed key dictionary and existing CSS custom properties suffice for this scale. Any new dependency must have need, package/version, license, maintenance risk and explicit approval documented before introduction.

### Component ownership and integration boundaries

- `page.tsx` owns the currently authoritative document/result/error and workflow navigation. It should pass stable callbacks to new presentation components, not duplicate workflow state inside theme/i18n providers.
- `WorkflowProgress.tsx` receives derived reachable/complete/attention state. It renders labels from dictionary and must not mutate review/validation permission.
- `UploadPanel.tsx` continues local selection validation and upload actions. In demo staging, an arbitrary local file stays UI-only; the synthetic sample is an explicitly separate action.
- `ResultWorkspace.tsx` keeps `createDraftSession`/`selectedRevision`/`saveDraftRevision`/`setReviewStatus`/`setRevisionValidation` semantics. New rail/inspector state is **view state**, not a legal review state.
- `PatentDraftView.tsx` retains schema-provided headings, missing markers, unverified edited prose and limited textareas. Do not introduce general Claims editing.
- `EvidenceCard.tsx`/`GroundingBadge.tsx` remain data display components. New inspector looks up evidence by immutable IDs/locators, marks unknown/empty links explicitly.
- `client.ts` remains sole backend transport adapter with `/backend` routing and existing safe exception normalization. An i18n presentation mapper consumes stable error codes; no translation of raw unknown messages or unredacted paths.
- `globals.css` can be split into logically scoped imports after snapshot comparison; migrate existing selectors incrementally to avoid cascade regression.

## 3. Verification matrix and expected artifacts

### 3.1 Primary orthogonal matrix

Cross **3 preferences (Light/Dark/System) × 2 locales (vi/en) × 5 widths (390/768/1280/1440/1920) = 30 base combinations**. For System run both OS light and dark (10 additional resolved combinations), plus mid-session OS change test. For each combination assert document `lang`, header selections, first-stage CTA, capability banner, focus outline, no missing keys, no horizontal page overflow and margin motif policy. Capture named before/after screenshots and trace where rendering fails. Use deterministic synthetic fixtures; never real papers.

Run **16 canonical screen scenarios** from [spec §9](UIUX-001-specification.md) in primary desktop/default locale/theme and in mobile/dark/en representative coverage. Add high-risk state/theme/locale cross checks below. Avoid claiming 30×16 permutations are tested if selected pairing is used; document actual cases and omissions. Visual snapshots require Human inspection, not automated pixel difference as the only pass criterion.

### 3.2 High-risk E2E test cases (future)

| Test ID | Setup and action | Required assertion |
| --- | --- | --- |
| Q01 | Fresh storage, OS dark; open page | Preference System, dark resolved tokens before first visible paint, no hydration warning |
| Q02 | Save Light, reload with OS dark; change to System, then OS light | Saved Light persists; System subsequently follows OS immediately |
| Q03 | Enter synthetic review, begin editing text, switch theme three times | Buffer text, revision selection, section status and validation context remain unchanged |
| Q04 | Select local PDF in public demo; switch vi → en → vi | File remains local UI selection; no backend process request; no accidental file upload |
| Q05 | Review a saved revision with one issue; switch locale during issue/error state | Selected revision, issue paths and recovery route unchanged; every UI notice translated safely |
| Q06 | Force translation key coverage check / unknown safe backend error code | No missing VI/EN dictionary keys; generic localized message, no raw paths/stack/provider leak |
| Q07 | Complete keyboard-only synthetic flow, including tabs, section rail, evidence inspector, modal, review statuses, validation, export | Logical focus order, no hidden-focus leaks; modal Escape/cancel/focus return; accessible labels |
| Q08 | Enter dirty editor, initiate destructive new-paper/removal/replace | Warning presents lost-state scope; Cancel preserves edit; Confirm clears exactly once |
| Q09 | Save edited revision-2 and select revision-1 | Review/validation belong to each revision; new revision initially unreviewed/unvalidated |
| Q10 | Attempt direct validation/export by stage nav before eligible; spoof visual state in UI if feasible | Server and UI guards remain; no premature request/export |
| Q11 | Backend invalidation after process failure; click recovery | Requires new upload; no stale document process retry |
| Q12 | API returns validation path on paragraph field; click issue link | Focus correct field; unmapped path gets safe fallback, ID preserved |
| Q13 | API returns revision mismatch / `valid=false` | No validation success state or enabled export |
| Q14 | Make DOCX export fail, then retry on validated revision | No file download on failure; selected validated revision and digest preserved |
| Q15 | Synthetic demo full PDF and DOCX fixtures | Legacy v1 DOCX filename/output and deterministic content still match existing tests |
| Q16 | Attempt B2 PDF/application output in public UI | No enabled unsupported format; explanatory “not available here” text |
| Q17 | At 390 px, long filenames/technical IDs/evidence quotes, zoom 200% | No body overflow, truncated core controls or obstructed editor |
| Q18 | At 1440/1920 hover/click near motifs and tab through UI; at 390 open bottom sheet | Graphics do not intercept hit tests/focus; motifs absent on mobile; drawer focus restore |
| Q19 | Test text/border/status/focus contrast in light and dark and System resolved both ways | WCAG 2.2 AA target thresholds; zero critical audit violations with manual checks |
| Q20 | Intercept all outgoing requests during theme/locale changes/local demo arbitrary file selection | No unexpected provider/AI/data/remote-asset requests; only authorized synthetic sample and backend calls |

Browser tests already in baseline: `frontend/e2e/integration.spec.ts` checks stage reachability, selection removal/reselect, revisions, validation, export, errors, keyboard; `frontend/e2e-demo/demo-staging.spec.ts` checks demo local selection, controlled samples, responsive width; `frontend/e2e/performance.spec.ts` checks synthetic local flow. Reuse these as regression sources. Copy-based locators must become locale-aware without weakening test semantics.

### 3.3 Accessibility and security checks

Use manual keyboard walkthrough in **both** locales and all theme modes plus automated axe or equivalent **only if already available / separately approved**. Focus and status are text+color, ratios normal text ≥4.5:1, large text and graphic/focus contrast ≥3:1; compare composited token combinations including opaque overlay dialogs, error surfaces and disabled states. Check screen-reader announcement of stage, picker, file state, revision, validation and destructive modal; no evidence quotes spoken as label noise when navigating section rail. Respect `prefers-reduced-motion`, zoom 400%, textarea resize and long translated strings. Security check detects third-party requests, leaked sample/real text in console/log, new persistence of document contents, provider calls, changed API contracts or schema. These are **future tests**, not results from this specification task.

## 4. Review, CI and completion gates

1. **Before future code:** explicit Human implementation authorization + frozen reviewed UIUX-001 specification + fresh main and correct V1/V2 selection. Technical decisions about actual saved locale SSR effects must preserve static export compatibility.
2. **Per phase:** narrow deterministic frontend unit/browser checks, TypeScript/lint/build as applicable, snapshots and a11y/manual checks; stop on API, document, security, provider, legal, Claims or real-data scope violations.
3. **Before integration merge:** exact final implementation SHA, successful required PR CI, independent applicable reviewer PASS on same SHA with model/profile, no unresolved blocking findings/threads, no unauthorized changes, and GitHub platform eligibility.
4. **After any authorized implementation merge:** verify actual main SHA and CI, publish evidence and update README status/governance and MCP only when supported. Do not infer production release.
5. **Current UIUX-001 doc PR:** check three files, exactly 28 explicit AC definitions in master spec, internal relative links, fixed main baseline, zero frontend/backend changes, repository diff scope and whitespace. Post PR comment with independent Gemini handoff. Stop **before merge**.

Suggested future review evidence per phase: diff/changed file inventory, selected screenshots at five widths and both resolved schemes, CI run URL, Playwright trace IDs, a11y/contrast report, external fixed-SHA review and remaining limitations. Report observed PASS only when the actual tool produced it.

## 5. Risks and resolutions for future scope decision

| Risk | Proposed mitigation / decision boundary |
| --- | --- |
| Theme initial flash/hydration on static build | Deterministic SSR markup, CSS media fallback and prepaint root attribute; test browser reload in saved and System modes. |
| Locale preference and static SSR initially differ | Hydrate with deterministic VI, apply persisted EN after hydration; measure visible swap; separate technical approval if server cookie or dynamic rendering is proposed. |
| Review three-column cannot fit at browser zoom or compact desktop | Use container-fit fallback to drawer layout, max text measure and min center width; no forced horizontal scrolling. |
| Edit buffer lost on internal navigation | Transition guard and confirm dialog; beforeunload best-effort; **no autosave promise**. |
| Old CSS cascade collision | Phased semantic aliases and screenshot diffs before moving rules; retain current blue-brand values. |
| Localizations introduce misleading legal/AI promises | Two-language review against safety glossary and explicit public demo capability matrix. |
| Evidence links imply newly substantiated edited claims | Keep evidence locator unchanged, mark altered prose semantic support unverified, never reclassify grounding. |
| P2-006 offline B2 renderer confused with public export | Current v1 DOCX only; advanced formats presented as unavailable until separately authorized API/frontend integration. |
| Art looks like an actual licensed drawing | Abstract original primitives, no patent source images or external assets, no technical labels suggesting source support. |
| New dependencies or state rewrite broaden scope | Prefer existing React/CSS/Playwright stack, dependency and change justification with Human authorization if material. |

This plan is review material only. **No implementation, production artifacts, merged PR, provider calls, real-paper work or public deployment are authorized or performed in UIUX-001.**
