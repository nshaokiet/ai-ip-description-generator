# UIUX-001 — Complete Patent Drafting Workspace Design Specification

| Attribute | Decision |
| --- | --- |
| Document / version | UIUX-001 master specification v0.1.0 |
| Date / source baseline | 2026-10-10 / `a821716e63d0f3b3c87f594f42071bf937d590c9` |
| Authorization | Human UIUX-001 specification-only directive, 2026-10-10 |
| Workflow / status | V1; proposed, independent fixed-SHA review pending |
| Owner / reviewer | Codex specification owner / Gemini 3.1 Pro High, Antigravity STRICT READ-ONLY |
| Target audience | Universities, research teams, technology-transfer and intellectual-property reviewers |
| Product visual thesis | **Modern, Minimal, Professional Scientific Research & Patent Drafting Workspace** |
| Defaults | Theme = **System**; UI language = **Vietnamese (vi)** |
| Decoration recommendation | **Hybrid A — Science left / Patent right**; alternative B documented below |
| Source of truth | This document for proposed UI; [audit](UIUX-001-audit.md) for observed baseline; [plan](UIUX-001-implementation-plan.md) for proposed implementation |
| Implementation authority | **NOT GRANTED** by UIUX-001; no product code, exports, provider or deployment changes |

## 1. Design contract and non-goals

Transform the existing five-stage flow into a restrained enterprise research workspace: **Source Upload → AI Extraction → Review & Refine → Validation → Export**. Emphasize editing the draft and comparing its source evidence. Present one dominant action per state; organize secondary diagnostics behind disclosure. Preserve official VNUHCM Innovation Hub logo bytes, recognizable blue palette and current backend semantics.

A visual/state redesign must preserve local PDF/DOCX limit and authoritative backend validation, deterministic synthetic-demo constraints, section-review gates, immutable session revisions, revision-bound validation, safe errors and present v1 DOCX export. The user should be told that **real-paper AI conversion is unavailable in the public synthetic demo**, and that the document is an editable **draft requiring Human/IP specialist review**, never a grant, issued patent, filing-ready package or legal opinion. UI locale affects the shell only.

**Out of scope:** adding provider/API spend, real or confidential papers, storage or retention, auth/collaboration, backend endpoints or schema changes, Claims generation/editing or change of provenance semantics, production deployment, P2-006 public B2 PDF/application export, real figures, translated paper/evidence/document output, final production visual assets. Future component names are suggestions; they create no technical authorization.

## 2. Product information architecture

One-page workflow with persistent compact header, status bar, guarded progress navigator, stage content and footer. Keep stepper semantics derived from existing `WorkflowPhase`/`WorkflowState` rather than a second independent process engine. When returning to a completed reachable stage, show cached session data rather than re-trigger extraction.

```text
HEADER [official VIH logo + AI IP Description Generator]     [VI | EN] [System ▾]
HOME (only before result): "Từ nghiên cứu đến bản dự thảo sáng chế"
  [Public demo notice: only controlled synthetic samples use processing]
  [One primary task action: Chọn tài liệu / Select document]
STEPS  [1 Tải nguồn] — [2 Trích xuất] — [3 Rà soát] — [4 Xác thực] — [5 Xuất]
STAGE  upload / extraction / document-centered review / validation / export
FOOTER [Draft / Human review and data-safety notices]
```

Header: 64–72 px desktop, 60 px narrow; unmodified logo source `/brand/vnuhcm-innovation-hub-logo.png`, descriptive `alt`, 36–44 px logo visual height without forcing distortion. Product name to right of logo. Two segmented/small menu controls with accessible names “Ngôn ngữ giao diện / Interface language” and “Giao diện màu / Color theme”; indicate selection in text and `aria-pressed` or native select state, avoid icon-only ambiguity. Do not invent login, billing or cloud actions. Header may wrap one row on narrow widths; minimum targets 44 × 44 px.

Home hero: max content copy width 720 px, heading 32–44 px responsive, one-sentence subline. The actionable source/upload surface must be visible near first viewport; keep empty white space controlled. A capability banner directly above it says the demo allows local file selection while only deterministic synthetic samples can be processed. Non-demo environments must derive availability from existing authorized runtime configuration and responses, never assume arbitrary papers work.

Stage navigation statuses: `CURRENT`, `COMPLETE` (the specific milestone truly finished), `AVAILABLE` (reachable without rerunning), `UNAVAILABLE` (prerequisite missing), `PROCESSING`, `ERROR` and `ATTENTION`. Use text + icon + hue, never color alone. The navigation guard is authoritative: `upload` always; `analyze` only after accepted upload; `review` after a successful process result; `validate` only after all selected-revision section statuses are `REVIEWED`; `export` only after valid exact-revision server validation and review-complete. Existing logic must still enforce the final gate regardless of appearance. Buttons for unreachable steps disabled and described; Back selects nearest reachable prior stage without wiping session. A saved edit creates a new revision and invalidates that new revision's review/validation; selecting an older revision uses its own recorded review and validation only.

## 3. Review & Edit — primary workspace

At ≥1280 px, build one reading surface with **left section navigation**, **center editable patent draft**, **right evidence/grounding/validation inspector**. The content is user-oriented: section names, completeness, review statuses, draft prose and evidence, with IDs behind “Chi tiết kỹ thuật / Technical details.”

```text
┌───────────────────────────────────────── HEADER / GLOBAL CONTROLS ──────────────────────────────────────────┐
│ 1 Source Upload  ✓  2 AI Extraction  ✓  3 Review & Refine [CURRENT]  4 Validation [LOCKED]  5 Export [LOCKED] │
├────────────────┬──────────────────────────────────────────────────┬───────────────────────────────┤
│ SECTIONS       │ DRAFT / revision-2 [choose]   [Edit] [Continue]  │ SOURCE & VALIDATION           │
│ Abstract       │ PATENT DESCRIPTION DRAFT • HUMAN REVIEW          │ Evidence: source / locator    │
│ Tech. field    │ Title / Abstract / Background ...               │ Grounding: SOURCE FACT etc.   │
│ Background     │ [prose textarea when editing]                   │ Exact quote (read-only)       │
│ Summary        │ [Missing information; review status]            │ Missing/validation issue     │
│ Description    │ [Save new revision] [Cancel]                     │ [Back to selected field]     │
│ Claims*        │ [draft content only, not editable Claims]        │ Source/evidence status       │
├────────────────┴──────────────────────────────────────────────────┴───────────────────────────────┤
│ Persistent note: Draft, not issued; technical validation ≠ legal/Human approval                              │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
* Only if present in the authorized existing draft contract; no v2 Claims UI invention.
```

Left rail ~220–240 px: source-schema section order, anchors with stable IDs, section-level `UNREVIEWED/REVIEWED/NEEDS_CHANGES`, missing/issue count. Clicking scrolls/focuses the draft heading without changing revision. Section currently viewed is announced. Center min 520 px: document masthead and revision selection; editor toolbar; title, abstract and existing editable prose fields only; visible `[AUTHOR CONFIRMATION REQUIRED]` blocks. Review control remains mapped to the exact section ID. Right inspector ~300–320 px: pinned selected evidence locator, evidence excerpt and grounding label, unresolved conflict / issue; clicking a paragraph’s “Xem chứng cứ / Inspect evidence” supplies the related IDs to inspector; for no link say “Chưa có chứng cứ liên kết / No linked evidence” without inventing one. Keep read-only evidence and unverified-edit warning adjacent to modified prose. Existing Analysis and Review Items remain accessible as alternate view/panels without losing editor context.

Edit transaction: `View → Edit (copy selected revision) → Dirty/clean → Save new revision` (only if changed) or `Cancel` (restore exact selected revision). While editing, disallow or guard switching revision or leaving to stage/tab that would unmount buffer. Explicit modal before discarding **dirty** draft or resetting source; Cancel in that modal restores editor and focus. Save creates immutable `revision-N` using existing `saveDraftRevision`, resets new review to UNREVIEWED and its validation to null; retain previous revisions. Never claim autosave/persistence: show “Chỉ lưu trong phiên hiện tại; tải lại trang có thể mất chỉnh sửa / Stored in this session; reload may discard edits”. `beforeunload` may warn on dirty edit but cannot promise browser always shows custom text. Theme and language changes must be pure presentation updates and preserve `session`, `editBuffer`, `active section`, `selectedId`, review counts, errors, validation and file selection. Avoid keying workflow subtree by theme or locale.

Validation inspector must associate each server `paths[]` entry with existing JSON-pointer-to-field map; one “Đi đến trường / Go to field” focuses the offending editor field; unmapped paths remain visible in a safe generic issue list with correlation ID. Errors and warnings carry text priority and guidance. Preserve exact `revision_id` match and validated digest; no client-simulated PASS.

## 4. Responsive layout contract

| Viewport | Content / columns | Header + stages + rail/inspector | Decoration |
| --- | --- | --- | --- |
| **390 px** mobile | 100% width minus 16 px side gutters; single draft column, editable controls full width; long words wrap, horizontal code scroll confined | Header two rows if necessary; stepper a labelled compact “Step 3 of 5” + accessible stage list; section navigator bottom-sheet/drawer; evidence/validation drawer with open/close and focus restore; sticky action bar only if it does not obscure text/keyboard | Hidden, both sides |
| **768 px** tablet | 24 px gutters; draft full width, optional 200 px section rail only if draft ≥480 px; otherwise drawers | Stage list condensed; inspector below draft / side sheet; upload card centered and full usable width | Reduced, clipped to outer margin; hide if conflict |
| **1280 px** desktop | Main max 1160 px; left 210, center min 520, right 290, 20 px gaps | Full stepper; inspector persistent | Both faint, scaled to available ~60 px outer strips |
| **1440 px** desktop | Main max 1200 px; left 220, center ≥600, right 300, 20 px gaps | Full toolbar and side columns | Both visible, ≤110 px each outside text content |
| **1920 px** wide | Main max 1480 px; left 240, center flexible up to ~840, right 320, 24 px gaps | Max text measure 75–85 characters within center; long evidence scroll inside panel | Both visible, up to 180 px per side |

Breakpoints proposed: `≤699` mobile, `700–1199` tablet/compact, `≥1200` desktop tri-column (actual fit checked at 1200–1279), `≥1600` wide. Use layout container-query safeguards for embedded/narrow windows; never cause page horizontal overflow at 390 px or clip field labels/controls. On small screens, preserve source inspection, draft editing, review, validation and export functionality, not miniature three-column layout. Touch targets ≥24×24 CSS px or equivalent spacing under WCAG 2.2 AA (prefer 44×44). Keep scroll/focus positions predictable when sheets close.

## 5. System tokens (proposed, implementation not performed)

Use the existing `globals.css` variable vocabulary and additive semantic aliases; no new UI framework. Colors are initial candidate values; verify 4.5:1 normal text, 3:1 large text and nontext/focus components on **actual composited surfaces** before approval.

| Semantic token | Light | Dark |
| --- | --- | --- |
| `--color-bg` / page | `#F6F8FC` | `#0B1320` |
| `--color-surface` / cards | `#FFFFFF` | `#121E30` |
| `--color-surface-alt` / editor/rail | `#F0F4F9` | `#1B2B40` |
| `--color-elevated` / dialog/popover | `#FFFFFF` | `#24344B` |
| `--color-text` / primary | `#102A43` | `#F0F6FC` |
| `--color-text-secondary` | `#38546C` | `#CAD9E9` |
| `--color-text-muted` | `#50677E` | `#A8BED3` |
| `--color-border` | `#CBD6E2` | `#4B6078` |
| `--color-primary-700` (legacy/action) | `#0D5AAE` | `#86C2F9` |
| `--color-primary-600` | `#166CC2` | `#A3D4FF` |
| `--color-primary-500` | `#1E88D8` | `#75B8F4` |
| `--color-primary-on` | `#FFFFFF` | `#081321` |
| `--color-link` | `#0D5AAE` | `#A3D4FF` |
| `--color-success` / status text | `#17653B` | `#90E5B5` |
| `--color-warning` / status text | `#805600` | `#FFDA86` |
| `--color-error` / status text | `#B42318` | `#FF9A94` |
| `--color-info` | `#165DAD` | `#A3D4FF` |
| `--color-focus` / visible outline | `#0D5AAE` | `#FFD166` |
| `--color-disabled-bg` | `#E5EBF2` | `#2B394D` |
| `--color-disabled-text` | `#596B7C` | `#ADBDD0` |
| `--color-overlay` | `rgba(9,24,42,.52)` | `rgba(0,0,0,.72)` |
| `--color-selection` | `#D8EDFF` | `#2F5274` |
| `--color-error-surface` | `#FFF0EE` | `#392527` |
| `--color-warning-surface` | `#FFF7E6` | `#352D1B` |
| `--color-success-surface` | `#ECF8F0` | `#1C382C` |
| `--color-decor-line` | `rgba(13,90,174,.11)` | `rgba(163,212,255,.10)` |

Focus rings: 3 px solid `--color-focus`, offset 3 px; if same-color or low-contrast adjacent areas, add 1 px counterstroke and validate 3:1. Selected state: accent border + selected icon/text and `aria-current/aria-selected`. Error is icon + label + safe description; warning not conveyed by color alone. Status badges fill only with corresponding surface token, text from status token after contrast verification. Inputs use surface-alt, 1 px border, 2 px focus indicator; readonly inputs visually distinguished. Table headers use surface-alt, row divider border, keyboard-visible focus for interactive cells. Primary button blue, secondary outlined, tertiary text-only, destructive red only after confirmation. On dark mode, primary button background maps to bright blue with dark label; never use white-on-bright-blue.

Type: `Inter` if already locally available, otherwise system UI (`-apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif`); body 16/24, compact 14/20, captions 12/18, H1 36/44 desktop 28/36 mobile, H2 26/34, H3 20/28, section labels 13/18 weight 600; body weight 400, headings 600/700. Document text 16/26, max reading width 80ch; use serif only if approved as a document-preview styling option, never imply it is exported filing typography. Monospace for small evidence IDs only, wrap/break long IDs. Spacing scale `4,8,12,16,20,24,32,40,48,64` px; grid gutters 16/24/32; radii `6,10,14` px; cards 1px border + shadow `0 1px 3px rgba(16,42,67,.07)` light, `0 8px 24px rgba(0,0,0,.22)` dark; dialogs 16 px radius. Animation ≤150 ms opacity/transform, no workflow-slowing transitions, zero/reduced under `prefers-reduced-motion: reduce`. Icons original geometric or plain SVG lines, paired with text, size 16–20 px. Skeletons approximate eventual layout with “Đang…” live status and no pulsing if reduced motion.

**CSS organization proposal:** immutable brand base, semantic light tokens, dark overrides, reset/typography, components by section (shell/stepper/upload/review/forms/dialog/status), then responsive overrides. Current `globals.css` is 2,219 lines with repeated selectors; split only as necessary after visual comparison, retain CSS variable compatibility and existing styles throughout phased migration.

## 6. Theme architecture — P0

Theme preference `"light" | "dark" | "system"` stored only as a harmless local key `aiip.theme`. Default **system**. Resolved theme follows `matchMedia("(prefers-color-scheme: dark)")` whenever system is selected; listen to OS changes and clean up listeners. One top-level theme controller updates an attribute on `document.documentElement` and does **not** remount workflow subtree. CSS can use `[data-theme="light"]` and `[data-theme="dark"]` overrides, and media-query system fallback. Apply user choice with a tiny local pre-paint initializer in the Next root layout, avoiding network calls. With JavaScript disabled, CSS media queries still supply usable system colors. Initial server markup must use deterministic defaults and avoid reading `window` or `localStorage` in the server-rendered component. If the pre-paint initializer changes the root attribute before hydration, reconcile the attribute with `suppressHydrationWarning` on the root only; never silence mismatches in the app tree. Verify all SSR/hydration approaches against actual static public build constraints before implementation.

Theme coverage: header, hero, workflow and disabled steps, upload drop zone, cards, editor textareas, evidence quotes, section rail, result tabs, forms, tables, dialogs/overlay, error/success/warning alerts, code snippets, skeletons, focus and document preview. **The exported patent DOCX/PDF payload and typography must not change with UI theme.** Show selected preference + resolved scheme in tests. Guard storage read exceptions and corrupted preference by falling back to system. Performance tests must establish no visible incorrect-color frame on reload with saved light/dark and no React hydration warning; tested at each specified viewport.

## 7. Locale architecture — P0

Locales: typed keys `vi` and `en`; first visit **vi**. Store `aiip.locale` locally. Application-owned UI copy, aria text, notices, labels, validation errors, and confirmation dialogs all use typed `t(key, params)` over one centralized dictionary; keep identical key sets and a missing-key check that fails development/CI. Unknown locale → `vi`; missing translation during development → emit safe visible fallback to English/key with diagnostic, but production builds must fail completeness check so raw keys never reach users. Untrusted server error codes map to an **allowlisted localized error catalog**; never interpolate unsanitized raw backend messages or technical paths into prose. Safe correlation ID may remain an identifier; show a generic localized fallback for unknown errors. Translate user-facing labels for source locator types without altering locator values.

SSR/static compatibility: server and initial React render deterministic Vietnamese copy; restore stored locale in an effect after hydration, ensuring React trees match. If a persisted EN setting causes a brief VI→EN content change on a static page, quantify it during future QA and optimize with a compliant bootstrapping strategy only after feasibility review; **do not** use client-only initial state that mismatches SSR. Set actual document `lang` to selected UI locale post-hydration, announce language change politely without reading the whole draft; provide language-appropriate font fallbacks. Do not remount document/edit session. Distinguish UI text from **unchanged** uploaded paper, patent body, Claims, technical source wording, evidence quotes, identifiers, backend JSON, citations, and exported DOCX/PDF. Automatic document translation requires separate approval.

### 7.1 Bilingual terminology glossary

| Vietnamese UI | English UI | Meaning / boundary |
| --- | --- | --- |
| Tài liệu nguồn | Source document | Input PDF/DOCX |
| Trích xuất nội dung | Content extraction | Stage label; not assurance of real-provider capability |
| Bản dự thảo mô tả sáng chế | Patent specification draft | Editable draft; not issued or filed |
| Rà soát và hoàn thiện | Review & Refine | Human review activity |
| Chứng cứ nguồn | Source evidence | Citation/locator, not legal proof |
| Liên kết nguồn | Grounding | Origin/evidence classification |
| Suy luận | Inference | Must remain separate from SOURCE_FACT |
| Thiếu thông tin | Missing information | Requires author confirmation when applicable |
| Xung đột chưa giải quyết | Unresolved conflict | Visible review blocker |
| Phiên bản dự thảo | Draft revision | Immutable in-session snapshot |
| Xác thực cấu trúc | Structural validation | Server validation, not legal approval |
| Xuất tài liệu | Export document | Only currently implemented format/endpoint |
| Yêu cầu tác giả xác nhận | Author confirmation required | Missing evidence/action; no invented facts |
| Yêu cầu chuyên gia SHTT rà soát | IP specialist review required | Disclaimer |

### 7.2 Typed-dictionary sample — copy, not code

| Key | vi | en |
| --- | --- | --- |
| `workflow.upload` | Tải tài liệu nguồn | Source Upload |
| `workflow.extract` | Trích xuất nội dung | AI Extraction |
| `workflow.review` | Rà soát và hoàn thiện | Review & Refine |
| `workflow.validate` | Xác thực cấu trúc | Validation |
| `workflow.export` | Xuất bản nháp | Export draft |
| `action.selectFile` | Chọn tài liệu | Select document |
| `action.saveRevision` | Lưu thành phiên bản mới | Save as new revision |
| `action.cancel` | Hủy | Cancel |
| `action.inspectEvidence` | Xem chứng cứ nguồn | Inspect source evidence |
| `action.retry` | Thử lại | Retry |
| `status.localSelection` | Đã chọn trên thiết bị; chưa tải lên | Selected locally; not uploaded |
| `status.uploaded` | Đã tải lên và được hệ thống chấp nhận | Uploaded and accepted by service |
| `status.processing` | Đang xử lý tài liệu… | Processing document… |
| `error.unsupportedFile` | Chỉ chấp nhận một tệp PDF hoặc DOCX. | Choose one PDF or DOCX file. |
| `error.tooLarge` | Tệp vượt quá giới hạn 10 MiB. | File exceeds the 10 MiB limit. |
| `error.emptyFile` | Tệp được chọn không có dữ liệu. | The selected file is empty. |
| `error.backendUnavailable` | Không thể kết nối dịch vụ. Hãy thử lại hoặc liên hệ bộ phận hỗ trợ. | Service unavailable. Retry or contact support. |
| `error.validationFailed` | Phiên bản này chưa đạt xác thực; xem mục có lỗi để sửa. | This revision failed validation; inspect the affected fields. |
| `notice.demo` | Bản demo chỉ xử lý mẫu tổng hợp có sẵn. Tệp riêng chỉ được chọn trong giao diện; chưa chuyển đổi bằng AI. | This demo processes controlled synthetic samples only. Your own file can be selected in the UI but is not AI-converted. |
| `notice.unsaved` | Chỉnh sửa chưa được lưu. Rời khỏi sẽ mất thay đổi. | Changes are unsaved. Leaving will discard them. |
| `notice.draftLegal` | Đây là bản dự thảo, không phải bằng sáng chế đã cấp hoặc hồ sơ sẵn sàng nộp. Cần chuyên gia kỹ thuật và sở hữu trí tuệ rà soát. | This is a draft, not an issued patent or filing-ready submission. Technical and IP specialist review is required. |
| `notice.technical` | Xác thực kỹ thuật không đồng nghĩa phê duyệt của con người hoặc kết luận pháp lý. | Technical validation is not Human approval or a legal determination. |
| `notice.noClaims` | Không tạo hoặc xác nhận yêu cầu bảo hộ khi thiếu nguồn hỗ trợ. | No patent Claims are created or approved without supporting source evidence. |
| `export.unavailable` | Định dạng này chưa khả dụng trong giao diện hiện tại. | This format is not available in the current interface. |

Interpolate only explicit safe variable types: filename as plain text, count as integer, revision as validated ID, code in code element; React escapes text by default. Internationalize plural counts and aria descriptions. Equivalent warnings must retain **the same** safety meaning in both locales. No localized provider error leaking underlying internals.

## 8. Original science/patent decoration — mandatory both sides

**Recommended variant A: HYBRID — SCIENCE LEFT / PATENT RIGHT.** Create original, static, abstract and generic inline SVG/CSS primitives in a later authorized implementation. The left margin contains 6–9 blue outlined nodes, short bonds and a faint 20–28 px technical grid fading toward outer edge; the right margin contains 2–3 concentric technical arcs/rectangles, dashed axis, 2–3 leader lines and anonymous abstract reference-number callouts (e.g., 01/02, not a claimed figure). This communicates research → draft and avoids real drawing claims. Light line token `rgba(13,90,174,.11)`, dark `rgba(163,212,255,.10)`; initial opacity/effective emphasis **5–12%**, verified against layout and contrast rather than treated as an invariant.

```text
[LEFT OUTER MARGIN]       [CLEAR CENTER CONTENT SURFACE]       [RIGHT OUTER MARGIN]
 o───o  ·  grid          Header, hero, upload/editor          ┌─┐  - - (01)
  ╲ /   ·               no graphic below text               └─┘──  (02)
   o──o                  clickable workflow fully clear       ─ ─ axis/arc
```

**Alternative B: Research network / patent section index.** Left: vertical abstract node cluster with sparse short chart bars; right: parallel typographic-independent technical rules and numbered boxes suggesting a drawing index. Variant B is more geometric but risks appearing as actual patent figures; choose A for clearer visual distinction and less visual noise. Both must be original and source-neutral.

Placement: decoration container outside main interactive surface; CSS `position:absolute` in page-wide presentation layer with `overflow:hidden` and isolated stacking context; each motif max visual width 180 px at 1920, scaling to available outer margin. `pointer-events:none` on container **and descendants**, `aria-hidden="true"`, `focusable="false"`, no focusable SVG content, no semantics that enter accessibility tree; stacking below content, no bleed behind text, inputs, quotes or alerts. Avoid `position:fixed` over scrolling content. At 768 reduce to 1–2 primitive groups each if actually isolated from content; hide below 700 or earlier on collision. No animation; respect reduced motion. Do not copy issued patent illustrations, diagrams, symbols from external products, logos or sensitive research sources. No remote fetch/stock art or final production assets in UIUX-001.

## 9. Sixteen screen-state specifications and transitions

States below describe future UI presentation. All actions must call only existing authorized endpoints/state operations, and availability is conditional on runtime mode.

| # | Screen/state and visible hierarchy | Primary action → next / recovery | Guard, microcopy and test anchor |
| --- | --- | --- | --- |
| 01 | **Home / empty upload**: hero, demo banner, dropzone, five-stage map | Select file → 02 | “Chọn một PDF hoặc DOCX”; max 10 MiB; no implied real conversion |
| 02 | **File selected locally**: filename/size/status, Remove, upload availability | Local supported runtime: Upload → 03/04; public demo: choose synthetic sample separately | “Đã chọn trên thiết bị”; button disabled for arbitrary demo upload; invalid/zero/oversize errors inline |
| 03 | **Upload successful**: accepted file metadata, continue, replace/remove | Continue → 04 | Distinguish backend accepted from processed; no automatic invented analysis |
| 04 | **Processing**: progress/aria-busy, safe explanation, busy lock | Success → 06; failure → 05 | Duplicate clicks blocked; timing unspecified, no fabricated percentage |
| 05 | **Processing failure**: alert, correlation ID, safe error copy | Choose new paper / return as supported → 01/03 | If backend source invalidated, demand re-upload; never retry expired ID |
| 06 | **Review default**: tri-area document, revision selection, review status | Edit → 07; inspect → 08; finish review → 10 | Draft and not-issued notice; no legal PASS |
| 07 | **Section editing**: textareas, Save new revision, Cancel, dirty badge | Save → 06 with new revision; Cancel → 06; dirty exit → 15 | Only supported prose fields; unsaved alert; review/validation reset for new revision |
| 08 | **Evidence inspection**: right panel quote, locator, grounding, back-to-field | Back → 06/07 | Quote is read-only, no translate/relabel; absence explicitly signaled |
| 09 | **Validation issues**: issue summary, section links, selected revision | Edit field → 07; revalidate after review → 10 | No false PASS; sanitized paths; keep prior revision selection |
| 10 | **Validation success**: exact revision ID, server digest status, warning | Continue → 11/12 based on eligibility | “Chỉ xác thực cấu trúc”; not filing/legal approval |
| 11 | **Export unavailable**: format/permission explanation, no enabled advanced export | Return to Review/Validation | Public demo or unavailable P2-006 format labelled accurately |
| 12 | **Export in progress**: validated revision/format, spinner, live status | Success → 13; failure → 14 | Lock duplicate requests; existing v1 DOCX only |
| 13 | **Export success**: downloaded DOCX, draft warning, next action | Back → review/validation | Browser download success criterion; no issued/filing-ready text |
| 14 | **Export failure/recovery**: safe cause, correlation ID if supplied | Retry current exact validated revision → 12 or return → 06/10 | No download on failure; keep revision and validation |
| 15 | **Remove/replace confirmation**: modal, lost-data summary, keep/reset | Keep → prior state; confirm → 01/02 | Dialog focus trap, Escape cancel, focus return; only destructive action clears session |
| 16 | **Mobile collapsed workspace**: draft content first, section/evidence bottom sheets | Open rail/evidence → same state; close restores focus | 390 px, no horizontal overflow, editing and validation accessible |

Overlay states (invalid format, uploading, validation pending, network error, changing preferences) are modifiers to the 16 scenarios; avoid inventing a parallel state engine. Each test asserts visible status, main CTA, disabled gates and preservation of session invariants after Back, theme and locale changes. Screen-specific aria-live should avoid repeated announcements.

## 10. Export capability and provenance matrix

| Capability | Current frontend surface (source-confirmed) | Redesign presentation rule |
| --- | --- | --- |
| Arbitrary local PDF/DOCX selection | Yes, browser UI | Show “Selected locally” until backend upload succeeds |
| Public synthetic samples | Yes, controlled PDF/DOCX from `fetchDemoSample`; demo staging | Label as synthetic samples and explicitly separate from arbitrary real-paper processing |
| Real arbitrary-paper AI processing in public demo | **Not enabled** (README/demo notice) | No success promise or active converting CTA |
| v1 backend DOCX export | Implemented `POST /backend/api/exports/docx` with review/validation gates | Show exact “Editable DOCX draft (v1)” when endpoint/runtime supports it |
| P2-006 B2 reference PDF + editable DOCX | **Internal offline synthetic renderer**, closed task | No enabled public UI buttons without separately authorized integration |
| P2-006 application profile PDF/DOCX | Internal offline technical output | Informational “Not available here” only; no simulated download |
| Authentic supported Claims full-chain / real source figures | Unverified or unauthorized | Show unresolved status; never present as finalized |
| USPTO filing-ready output | Not established | Never claim filing compliance, patent issuance or legal validity |

Do not use a frontend “success” toast if browser download failed. Preserve validated digest, exact revision and present backend error sanitization.

## 11. Accessibility and safety quality contract

Target **WCAG 2.2 AA** in authorized future implementation: landmarks (header/nav/main/footer), one H1, heading order, labelled native controls, descriptive error messages tied via `aria-describedby`, live statuses only for actual async progress, dialog `role="dialog" aria-modal` with initial safe focus/Escape/focus return, keyboard stage/rail/editor/evidence/export complete, visible focus ≥3:1, text contrast ≥4.5:1 (large ≥3:1), distinguish state with icons/text beyond hue, scroll and zoom at 200%/400%, no keyboard trap aside from purposeful focus containment within an open modal, target 24×24 min with spacing (prefer 44×44), reduced motion, no decorations in hit-testing or accessibility tree. Tab switching and inspector focus must not unexpectedly destroy an edit buffer. Hidden data must be absent from focus sequence. Check all 3 theme preferences × 2 locales × 5 widths, system OS light and dark.

Preserve grounding categories `SOURCE_FACT`, `PARAPHRASE`, `INFERENCE` and missing evidence/status without reclassification; quotes immutable. Editing prose keeps source links but does **not** certify that changed text is supported; clear visible warning. Keep backend validation and review gate authoritative. No protected input data sent to outside providers, analytics or remote assets by redesign; no new PII, storage, retention or logged full document content.

## 12. Measurable acceptance ledger (28 criteria)

**Gate key:** `SPEC` = completeness/testability required to accept **this specification**; `IMPL` = proposed checks only for separately authorized future implementation (not claimed passing now). Each row gives observable expected result, a verification method and document/evidence anchor. **P0/P1** refer to future implementation priority; all 28 rows are mandatory to specify.

| AC | Priority; gate | Expected observable result / test | Evidence / design reference |
| --- | --- | --- | --- |
| AC-UIUX-01 | P0; SPEC | Baseline 40-char main SHA, ≥12 named source/test files and severity findings with verified/proposed separation; reviewer compares cited lines. | [audit](UIUX-001-audit.md) §§1–3 |
| AC-UIUX-02 | P0; SPEC+IMPL | Five named stages, CTA and truthful demo banner; 01→02→03→04→06 normal synthetic path. | §§2, 9; `page.tsx` |
| AC-UIUX-03 | P0; SPEC+IMPL | ≥390/768/1280/1440/1920 px design variants; no 390 px overflow in browser. | §4; [plan](UIUX-001-implementation-plan.md) |
| AC-UIUX-04 | P0; SPEC+IMPL | Seven progress statuses and stage reachability defined; browser cannot jump to validation/export before gates. | §2; `WorkflowProgress.tsx` |
| AC-UIUX-05 | P0; SPEC+IMPL | Upload, remove, replace, invalid/empty/oversize and destructive confirmation states; no stale processed result after reset. | §§2, 9 (01–05,15); `UploadPanel.tsx` |
| AC-UIUX-06 | P0; SPEC+IMPL | 3-area desktop review, accessible mobile drawers, revision/section/grounding and edit/save/cancel with dirty guard; test preserves edits. | §§3–4,9 (06–08,16) |
| AC-UIUX-07 | P0; SPEC+IMPL | Upload/process/validate/export busy, error, retry/recovery with safe text and same selected revision; test 4 failure paths. | §§3, 9 (04–05,09,12,14) |
| AC-UIUX-08 | P0; SPEC+IMPL | Export stages distinguish existing v1 DOCX and unavailable P2-006; no enabled unsupported format. | §§9–10 |
| AC-UIUX-09 | P0; SPEC+IMPL | Explicit light/dark token values + type/space/radii/forms/tables/modal/status; visual snapshot coverage. | §5 |
| AC-UIUX-10 | P0; SPEC+IMPL | Keyboard end-to-end, focus, role/labels, alerts, contrast 4.5:1/3:1, dialogs and target size tests. | §11 |
| AC-UIUX-11 | P0; SPEC+IMPL | Five widths with functional editor, upload, stepper, inspector and long text; overflow assertion. | §4 |
| AC-UIUX-12 | P0; SPEC+IMPL | Explicit legal/provider/data/API non-goals, no schema/validation/Claims changes; diff and network audit. | §§1,10–11 |
| AC-UIUX-13 | P0; SPEC | Current components mapped to screens; 16 numbered screen-state scenarios, guards and recovery. | [audit](UIUX-001-audit.md) §2; §9 |
| AC-UIUX-14 | P0; SPEC+IMPL | Light/Dark/System; default System; preference persists; OS change under System; no incorrect paint/hydration warnings; no state resets. | §§5–6 |
| AC-UIUX-15 | P0; SPEC+IMPL | All major surfaces, focus, dialogs, badges, inputs, charts/decor, both resolved schemes; color/contrast regression screenshots. | §§5–6,11 |
| AC-UIUX-16 | P0; SPEC+IMPL | VI/EN; first VI; persisted override; in-place switch retains file/edit/revision/validation/error; test no remount. | §7 |
| AC-UIUX-17 | P0; SPEC+IMPL | Typed complete dictionary, glossary, safe localized errors and equivalent legal notices; no source/Claims/evidence/doc translation; no missing keys. | §§7.1–7.2 |
| AC-UIUX-18 | P0; SPEC | Repeatable theme×locale×viewport×state, failure/recovery, Playwright and a11y matrix with owner/exit gates. | [plan](UIUX-001-implementation-plan.md) §3 |
| AC-UIUX-19 | P0; SPEC+IMPL | Original left science/right patent static concepts + two variants, chosen A; reviewer checks both outer margins. | §8 |
| AC-UIUX-20 | P0; SPEC+IMPL | Graphics only in margin, 5–12% emphasis initial target, dark/light legibility, no text obscured/blocked clicks. | §§4,8,11 |
| AC-UIUX-21 | P0; SPEC+IMPL | Both motifs on wide desktop, reduced tablet, hidden 390 px, no horizontal overflow. | §§4,8 |
| AC-UIUX-22 | P0; SPEC+IMPL | Original local primitives; no source patent art, remote art or trademark copy; aria-hidden/pointer-events:none. | §8 |
| AC-UIUX-23 | P0; SPEC+IMPL | Public demo and format limitations accurate; no live-provider/unsupported Claims/filing-ready claim; copy audit. | §§1–2,7,10 |
| AC-UIUX-24 | P0; SPEC+IMPL | Evidence/grounding, revision digest, server validation, Claims boundaries remain unchanged; semantic regression. | §§3,10–11 |
| AC-UIUX-25 | P0; SPEC | All 16 state wireframes/rules and concrete 3-column/mobile layouts plus CTA/error outcomes; reviewer can implement directly. | §§2–4,9 |
| AC-UIUX-26 | P0; SPEC | Component/refactor plan reuses Next/React/TS/CSS and endpoints; any dependency proposed has necessity/license review. | §5; [plan](UIUX-001-implementation-plan.md) §2 |
| AC-UIUX-27 | P0; SPEC | Five future phases with measurable quality/review/CI exit gates and explicit Human implementation authorization. | [plan](UIUX-001-implementation-plan.md) §§2–4 |
| AC-UIUX-28 | P0; SPEC | Exactly 3 task docs in scoped PR; links, AC IDs, diff, base/head SHA and review handoff verified at final SHA. | [audit](UIUX-001-audit.md), this file, [plan](UIUX-001-implementation-plan.md), PR metadata |

**Self-check classification:** all 28 are defined with testable behavior and references. Actual implementation behavior, WCAG compliance and visual QA are **NOT TESTED** in this documentation-only phase. Independent spec PASS is pending; AC-28 requires final GitHub post-write evidence, recorded in PR handoff.

## 13. Assumptions, risks and review gate

- Existing frontend API contract is v1, document-scoped and non-provider-public-demo. Do not interpret closed offline P2-006 as integrated UI export.
- Existing revisions are in-memory; theme/locale preferences may persist locally, but **paper/draft/validation and raw errors must not** be silently saved to localStorage. A separately approved persistence design is required for that capability.
- The 3-column center can fit at desktop widths only after real content/zoom testing; use tablet fallback when center <520 px.
- Color values are candidate tokens pending automated contrast verification in both themes and human visual QA; a proposal is not WCAG certification.
- “System” preference can be implemented without a new framework; static-site compatibility takes precedence over server-only cookies.
- Desktop motifs may need opacity reductions or hide at unusually narrow content containers; function and legibility are absolute constraints.
- Translated UI error catalog needs complete mapping of actual current backend error codes; unknown codes use safe generic localized fallback. Preserve opaque IDs and correlation codes.
- The frozen specification will require Gemini independent fixed-SHA review. Any changes to this documentation after review require a new exact-SHA review. UI implementation requires a **new, explicit Human authorization**, not this PR's merge.

**Required review verdict:** Gemini 3.1 Pro High / Antigravity STRICT READ-ONLY checks all 28 ACs, source grounding, practical theme/locale hydration, responsive/editor safety, copyright, accessibility, P2-006 distinction and contract scope. Report `PASS` or `REQUEST CHANGES` against the **exact final commit SHA**. This task ends with an open specification PR and verified handoff; **do not merge**.

