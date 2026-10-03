# P2-000 — Enterprise SaaS Webapp Redesign & Research Paper Workflow

## Metadata

| Field | Value |
| --- | --- |
| Task ID | P2-000 |
| Status | **CLOSED / COMPLETED — MERGED** |
| Authorization | `HUMAN-P2-000-WEBAPP-SIMPLIFICATION-2026-10-02` |
| P2-000-R2 authorization | `HUMAN-P2-000-R2-README-UPLOAD-UX-LOGO-2026-10-02` |
| P2-000-R3 authorization | `HUMAN-P2-000-R3-HUMAN-REVIEW-VALIDATION-DOCX-2026-10-03` |
| P2-000-R3 reconciled baseline | `8e38df7ef1427828fdff0a5fc7792bfa5bf03f9a` — Human-approved after verified README-only intervening commit |
| P2-000-R3 status | **IMPLEMENTATION MERGED — GOVERNANCE CLOSEOUT REVIEW PENDING** |
| P2-000-R3 reviewed SHA | `5569354e7003511d2e761236395ab6a604076530` — Gemini 3.1 Pro High / Antigravity PASS, findings NONE, 15/15 requirements PASS |
| P2-000-R3 implementation merge | PR #67 — `62a25a9ae136461924bc8047c5a6ad0f3550c68c` |
| P2-000-R3 CI | Exact-head `37080649206` SUCCESS; post-merge main `37109553040` SUCCESS |
| Latest Human design decision | 02/10/2026 — approve the reviewed Enterprise SaaS layout, preserve existing VNUHCM Innovation Hub logo/color system, add backward/forward step navigation and wrong-paper removal |
| Specification baseline | `461d9b33b07bb39aad11aa47b84f678e232d80a8` |
| Specification reviewed SHA | `5c57c47d562fa3d003850faf5820ffd17a3be385` — PASS / findings NONE |
| Specification PR / merge | `#59` / `3a11d358ba65bb5a83345a96f1e3f464a1a3abc0` |
| Implementation baseline | `3a11d358ba65bb5a83345a96f1e3f464a1a3abc0` |
| Implementation reviewed SHA | `8d63f19ebb755dafef1eafdb47874553be1fcdd3` — PASS / findings NONE |
| Implementation PR / merge | `#60` / `d0ffd09e0fe29e8a46c04e14b392e3c4aea22731` |
| Post-merge main CI | `36982485345` — **SUCCESS** |
| P2-000-R2 reviewed SHA | `05fc2d3dff6929ada7a4a974428cc26f5256c4fe` — PASS / findings NONE / all 10 review requirements PASS |
| P2-000-R2 PR / merge | `#65` / `a394a98b0a86b1ce686fac4871f7e5b0c0c3c44f` |
| P2-000-R2 post-merge main CI | `37012025003` — **SUCCESS** |
| Specification branch | `docs/p2-000-product-webapp-simplification-spec` |
| Primary implementation owner | Codex under AGENTS.md |
| Independent reviewer | Gemini 3.1 Pro High / Antigravity read-only |
| Classification | Frontend UX/presentation/navigation task only |
| Provider/API calls | **NOT AUTHORIZED / NOT REQUIRED** |
| Real/confidential research data | **NOT AUTHORIZED** |
| Production | **NOT APPROVED / NOT PERFORMED** |
| BLK-003 | **OPEN** |

---

## 1. Purpose

Redesign the current webapp home/upload and result workflow into a modern, minimal **Enterprise SaaS** experience inspired by products such as Linear/Vercel in information density and interaction clarity, while **preserving the project's existing visual identity**.

The product-facing workflow is:

```text
1. Source Upload
      ↓
2. AI Extraction
      ↓
3. Review & Refine
      ↓
4. Validation
      ↓
5. DOCX Export
```

The redesign must feel like one coherent workflow rather than a developer/debug dashboard.

P2-000 is a **presentation and navigation task**. It must not change backend semantics, AI behavior, schema contracts, Claims runtime, DOCX generation semantics, provider authorization, deployment topology, or security/data policy.

The current v1 runtime still produces a reviewable patent-description draft. P2-000 must not imply that P2-001 USPTO v2 runtime/Claims/DOCX-v2 functionality is already implemented.

---

## 2. Approved visual direction

### 2.1 Design language

Use a modern Enterprise SaaS visual language:

- white / very light neutral surfaces;
- high whitespace;
- restrained borders and shadows;
- centered hero;
- clear typographic hierarchy;
- single dominant CTA per state;
- compact secondary actions;
- minimal visual noise;
- progressive disclosure for technical information;
- desktop-first composition with complete responsive behavior.

Do **not** copy another product's branding, icons, typography assets, or proprietary UI. The reference is interaction density and visual restraint only.

### 2.2 Preserve existing project colors

Do not introduce a new brand palette. Reuse the existing frontend design tokens:

```css
--color-primary-700: #0d5aae;
--color-primary-600: #166cc2;
--color-primary-500: #1e88d8;
--color-secondary:   #27a3e3;
--color-accent:      #f47a2a;
--color-bg:          #f7f9fc;
--color-surface:     #ffffff;
--color-surface-alt: #f1f5f9;
--color-border:      #d9e2ec;
--color-text:        #102a43;
--color-text-secondary: #486581;
--color-text-muted:  #7b8794;
--color-success:     #2f9e44;
--color-warning:     #f08c00;
--color-error:       #d64545;
```

Use the blue family for primary interaction/state. Orange is an accent only and must not dominate the page.

### 2.3 Preserve official logo

Continue using the existing official asset:

`frontend/public/brand/vnuhcm-innovation-hub-logo.png`

Do not redraw, alter, recolor, crop, or replace the official logo.

---

## 3. Approved home/upload layout

### 3.1 Header

Desktop structure:

```text
[VNUHCM Innovation Hub logo] | AI IP Description Generator        About   Documentation
```

Requirements:

- keep logo at the left;
- keep product name immediately beside it;
- retain a thin divider if useful;
- no large environment/status badge in the header;
- header height must be materially smaller than the current hero-heavy composition;
- optional About / Documentation links may be shown only if they point to valid project destinations;
- do not add non-functional navigation.

### 3.2 Hero

Centered layout.

Approved title:

> **From Scientific Research Paper to USPTO-Style Patent Specification**

Approved supporting copy:

> Upload one scientific research paper in PDF or DOCX format to extract invention-relevant content, review and refine the generated patent specification draft, validate required sections, and export an editable DOCX for further expert review.

Requirements:

- hero centered;
- no right-side warning card;
- no large orange warning panel;
- no oversized marketing copy;
- title should fit approximately two lines on desktop;
- supporting copy limited to a readable centered width;
- preserve accurate draft/review semantics.

### 3.3 Global back action

Add a **Go back** action at the upper-left of the main workflow area.

Desktop example:

```text
← Go back
```

Rules:

- hidden or disabled on the initial Source Upload state where there is no prior reachable step;
- on later steps, returns to the nearest previous reachable workflow state;
- must not trigger a new API call merely to navigate backward;
- must preserve safe in-session data already generated unless the user explicitly removes/resets it;
- keyboard accessible;
- visible focus style required;
- browser Back is not a substitute for this product-level action.

---

## 4. Five-step interactive workflow stepper

Render exactly these five visible stages:

1. **Source Upload**  
   `Upload PDF or DOCX`

2. **AI Extraction**  
   `Extract key content`

3. **Review & Refine**  
   `Rà soát & hoàn thiện`

4. **Validation**  
   `Check required sections`

5. **DOCX Export**  
   `Download editable file`

### 4.1 Visual states

Each step must support:

- upcoming;
- current;
- completed;
- reachable.

Current step:

- blue filled marker;
- strongest label emphasis.

Completed step:

- success or approved completed treatment using the existing palette;
- may display a check mark.

Upcoming step:

- neutral border/text.

### 4.2 Step navigation

The user must be able to move backward and forward between **already reached** steps.

Rules:

- clicking a completed/reachable step navigates to it;
- keyboard activation with Enter/Space required;
- do not allow skipping into a step whose prerequisite has never been completed;
- returning backward must not automatically discard downstream state;
- navigating forward to a previously completed step must reuse current in-session state rather than re-run extraction/validation automatically;
- destructive reset/removal is a separate explicit action;
- current step must expose `aria-current="step"`.

### 4.3 State mapping to existing runtime

P2-000 should reuse the existing application/runtime state rather than requiring backend changes.

Expected mapping:

| UI stage | Existing behavior |
| --- | --- |
| Source Upload | file selection/upload/validation |
| AI Extraction | existing process call that analyzes source and generates current patent draft |
| Review & Refine | existing draft/revision/review workspace |
| Validation | existing server-side revision validation |
| DOCX Export | existing validated revision DOCX export |

Do not split the current process API solely to simulate new frontend stages.

---

## 5. Source Upload state

### 5.1 Upload card

Centered Enterprise SaaS upload card with a light dashed border.

Desktop content hierarchy:

```text
[document icon]

Drag & drop your research paper here
or

[ Select file ]

PDF or DOCX · Max 10 MB
```

Requirements:

- one text-based PDF or DOCX;
- maximum 10 MiB;
- preserve drag/drop;
- preserve keyboard file chooser;
- preserve backend validation as the source of truth;
- scanned PDF/OCR remains unsupported unless separately implemented later;
- selected/drag-active/focus states must use existing blue palette;
- no decorative animation that harms accessibility.

### 5.2 Sample paper links

Below the main upload area show two subtle sample actions:

```text
Thử nhanh bài báo mẫu:
Sample PDF (.pdf)  |  Sample DOCX (.docx)
```

Requirements:

- visually secondary to real upload in authorized local/internal mode;
- each action must have a clear accessible name;
- existing exact sample endpoints/assets may be reused;
- no paid/provider call is permitted by using a sample;
- do not introduce external sample sources.

### 5.3 Public environment safety

P2-000 does not authorize real/confidential upload to the existing public Render environment.

Therefore:

- the backend upload guard must remain unchanged;
- the public environment must not silently accept arbitrary real papers;
- if the current environment contract permits only approved sample documents, the UI must preserve that functional restriction;
- visible wording may be concise and product-oriented, but must not falsely imply that arbitrary real/confidential files are accepted publicly;
- no security/data authorization is inferred from the new visual design.

This requirement overrides purely cosmetic parity where necessary.

### 5.4 Session/privacy note

Use one subtle lock-icon note instead of a large warning panel.

Preferred local/session copy:

> **Tài liệu được xử lý trong phạm vi phiên làm việc.**

A stronger claim such as “bảo mật tuyệt đối”, “encrypted/private storage”, or equivalent must not be shown unless separately evidenced and approved.

For any public environment where only sample documents are allowed, use concise wording that accurately communicates the sample-only restriction without large warning panels.

---

## 6. Uploaded-paper state

After successful upload/validation, keep the same card footprint and transform it into a success state.

Approved hierarchy:

```text
[document icon]

Paper uploaded successfully

[PDF icon]  paper-name.pdf
            PDF · 2.4 MB                        [trash icon]

[ Continue to AI Extraction → ]

or

[ Select a different file ]

PDF or DOCX · Max 10 MB
```

### 6.1 Wrong-paper removal

Add an explicit delete/remove action on the uploaded file row.

Behavior before extraction begins:

- trash icon/button removes the currently uploaded paper from the active frontend workflow;
- resets the UI to Source Upload;
- clears current document reference and upload-derived state;
- invokes an existing supported backend cleanup/delete action only if one already exists and is correct for the lifecycle;
- do not invent a new backend deletion API in P2-000.

If no backend delete endpoint is available:

- clearing the frontend/session reference is allowed;
- existing backend cleanup policy remains authoritative;
- UI copy must not falsely claim remote deletion occurred.

### 6.2 Select a different file

Provide a secondary **Select a different file** action.

Rules:

- before extraction, selecting another paper replaces the current active paper in the workflow;
- previous in-session document reference must no longer drive extraction;
- backend cleanup remains governed by existing lifecycle behavior.

### 6.3 Removal after downstream work exists

If the user navigates back after extraction/review data already exists:

- do not silently remove the paper;
- use an explicit reset/new-paper confirmation before discarding generated downstream state;
- confirmation should explain that current analysis/draft/revisions/validation will be cleared from the frontend session;
- no modal is required if a compact accessible confirmation pattern is simpler.

---

## 7. AI Extraction state

When the user selects **Continue to AI Extraction**:

- set stage 2 current;
- use the existing process endpoint;
- display a clean progress state inside the main workflow card;
- copy should describe extraction/generation professionally and concisely.

Suggested:

> **Extracting invention-relevant content**

Supporting line:

> Identifying technical concepts and preparing a grounded draft for review.

Do not show internal provider/runtime debugging information.

On success:

- mark AI Extraction complete;
- navigate automatically to Review & Refine;
- default the result content to Patent Draft.

On failure:

- preserve existing normalized/safe error handling;
- focus the error heading;
- provide a recovery path to Source Upload where required by existing source cleanup behavior.

---

## 8. Review & Refine state

### 8.1 Default result view

The primary result view after extraction must be:

> **Patent Draft**

Do not default to Analysis.

Recommended result view order:

```text
Patent Draft | Review Items | Analysis
```

### 8.2 Main heading

Prefer:

> **Review & Refine**

with a concise contextual line such as:

> Review the generated patent draft, refine prose, and inspect supporting evidence before validation.

### 8.3 Navigation actions

Provide:

- **Go back** → AI Extraction or previous reachable state;
- stepper navigation among reached steps;
- **New paper** / reset action;
- next primary action toward Validation.

### 8.4 Revision semantics

Preserve existing:

- immutable in-session revisions;
- edit/cancel/save behavior;
- review statuses;
- evidence links;
- unverified edited-prose warning;
- session-only behavior.

UI may simplify presentation but must not weaken semantics.

### 8.5 Technical information

Correlation ID, internal IDs, detailed revision diagnostics, and similar implementation metadata should be secondary.

Use a `Technical details` disclosure or similarly low-emphasis region.

Do not remove evidence/analysis/review capability.

---

## 9. Validation state

Validation remains a visible first-class workflow stage in the approved five-step design.

Requirements:

- selected revision must be validated using the existing backend endpoint;
- validation result must remain tied to the exact selected revision/digest;
- no fake client-side PASS;
- validation failure returns a clear correction path to Review & Refine;
- Go back must return to Review & Refine without losing the saved revision;
- successful validation unlocks/reaches DOCX Export;
- stepper navigation may return to Review & Refine after validation;
- editing a validated revision via a new saved revision must require validation of the new selected revision before export.

Suggested success treatment:

```text
Validation complete
✓ Structure and required fields passed server validation.

[ Continue to DOCX Export → ]
```

Do not imply legal approval, patentability, filing readiness, or specialist approval.

---

## 10. DOCX Export state

Primary action:

> **Download editable DOCX**

or

> **Export draft DOCX**

Requirements:

- export only the exact validated selected revision;
- preserve backend revalidation/digest behavior;
- preserve single-in-flight export protection;
- keep filename behavior unless changed by a separately authorized DOCX task;
- current v1 output must remain clearly a draft.

Do not label current output:

- filing-ready;
- granted-patent format;
- Claims-complete;
- final USPTO filing;
- completed P2-001 v2 specification runtime.

Those capabilities belong to later P2 tasks.

---

## 11. Footer

Use a compact one-row or responsive two-line footer.

Suggested copy:

> © 2026 VNUHCM Innovation Hub. All rights reserved.

and:

> Kết quả cần được chuyên gia kỹ thuật và sở hữu trí tuệ rà soát trước khi sử dụng chính thức.

Do not use a large disclaimer panel.

---

## 12. Text/content cleanup

### 12.1 Product-facing language

Prefer professional workflow labels:

- Source Upload
- AI Extraction
- Review & Refine
- Validation
- DOCX Export
- Patent Draft
- Review Items
- Analysis
- Go back
- New paper
- Select file
- Select a different file
- Remove paper
- Download editable DOCX

### 12.2 Reduce internal-environment jargon

Do not make technical environment labels a dominant part of the product UI.

Avoid prominent copy such as:

- Synthetic Demo / Staging
- controlled sample
- no live AI
- internal runtime/provider explanations

However, P2-000 must still communicate any **functional restriction** necessary to avoid misleading users, especially on the public sample-only environment.

Safety/truthfulness has priority over cosmetic text removal.

---

## 13. Responsive requirements

### Desktop

- centered content;
- max content width aligned with existing `--content-width`;
- stepper rendered horizontally;
- upload card centered below stepper;
- hero compact enough that upload interaction is visible without excessive scrolling on typical laptop displays.

### Tablet

- preserve horizontal stepper where readable;
- otherwise allow compact labels/wrapping without horizontal page overflow.

### Mobile

- header remains compact;
- logo remains legible;
- stepper may become compact horizontal scroll or accessible stacked form;
- all primary/secondary actions remain reachable;
- upload card uses full available width;
- uploaded-file row may stack metadata/actions;
- Go back remains easy to activate;
- no clipped filenames/buttons;
- no horizontal page overflow.

---

## 14. Accessibility requirements

Preserve or improve all existing accessibility behavior:

- visible `:focus-visible`;
- keyboard file selection;
- keyboard step activation;
- current step `aria-current="step"`;
- status updates via appropriate live regions;
- error heading receives focus after global operation failure;
- result tabs retain correct roving tabindex / arrow / Home / End behavior;
- destructive remove/reset has accessible label and sufficient target size;
- icon-only trash action requires an accessible name such as `Remove paper`;
- reduced-motion support preserved;
- color must not be the only state indicator.

---

## 15. State/navigation invariants

The implementation must enforce these invariants:

1. Source Upload is always reachable.
2. AI Extraction becomes reachable only after a valid uploaded/sample document exists.
3. Review & Refine becomes reachable only after process success.
4. Validation becomes reachable only when a saved revision exists.
5. DOCX Export becomes reachable only after exact-revision validation PASS.
6. Backward navigation never re-runs network operations automatically.
7. Forward navigation to an already reached step does not re-run operations automatically.
8. A new edited revision invalidates prior validation eligibility for that new revision.
9. Remove/replace paper before extraction clears the active document selection.
10. New paper/reset after extraction clears downstream frontend session state explicitly.
11. The UI must not expose stale analysis/draft from a previous paper as if it belonged to the new one.
12. Stepper state must derive from application state, not visual-only local flags that can contradict runtime state.

---

## 16. Existing runtime/security boundaries

P2-000 must not change:

- backend API semantics;
- APP-003 cleanup rules;
- source storage lifecycle;
- extraction prompt;
- draft prompt;
- v1 schemas;
- P2-001 v2 schemas;
- Claims runtime;
- DOCX renderer semantics;
- OpenAI/provider/model selection;
- API-key policy;
- Render resource topology;
- authentication/tenant/storage/retention policies;
- BLK-003 state;
- EVAL-001 PRODUCT_RUNTIME state.

Provider/API spend remains **NOT AUTHORIZED**.

Real/confidential research data remains **NOT AUTHORIZED** for the public environment.

Production remains **NOT APPROVED / NOT PERFORMED**.

---

## 17. Expected implementation files

Primary expected files:

- `frontend/src/app/page.tsx`
- `frontend/src/app/globals.css`
- `frontend/src/components/UploadPanel.tsx`
- `frontend/src/components/WorkflowProgress.tsx`
- `frontend/src/components/ResultWorkspace.tsx`
- `frontend/e2e/integration.spec.ts`
- `frontend/e2e-demo/demo-staging.spec.ts`

Additional frontend-only files/components are permitted when needed for maintainable implementation, for example:

- reusable workflow navigation;
- technical-details disclosure;
- uploaded-file row;
- confirmation component.

Any additional file must remain inside authorized frontend/test scope and be listed in the handoff.

No backend file should change without a new Human decision.

---

## 18. Acceptance criteria

### AC-01 — Approved Enterprise SaaS layout
Home/upload visually follows the approved centered Enterprise SaaS composition: compact header, centered hero, five-step workflow, centered upload card, subtle sample actions and compact footer.

### AC-02 — Existing brand identity preserved
Official VNUHCM Innovation Hub logo and existing project color tokens are preserved. No replacement brand palette or altered logo is introduced.

### AC-03 — Header simplification
Header contains logo/product identity without the current large green environment badge. No non-functional nav link is introduced.

### AC-04 — Hero simplification
Hero is centered, uses the approved title/copy or a semantically equivalent Human-approved wording, and has no right-side orange warning card.

### AC-05 — Exactly five visible stages
The workflow displays exactly:
Source Upload → AI Extraction → Review & Refine → Validation → DOCX Export.

### AC-06 — Interactive reached-step navigation
User can move backward and forward among already reached steps through the stepper without automatically re-running API operations.

### AC-07 — Go back action
A visible/accessible Go back control appears where a previous step exists and returns to the appropriate reachable prior state.

### AC-08 — Upload behavior
Normal/local authorized mode retains one-file drag/drop + keyboard file selection for PDF/DOCX ≤10 MiB, with backend validation authoritative.

### AC-09 — Sample actions
Sample PDF and Sample DOCX actions are available as visually secondary quick-start options and use existing internal sample resources only.

### AC-10 — Public sample-only boundary preserved
Existing public environment restrictions remain functionally enforced; P2-000 does not authorize arbitrary real/confidential public uploads.

### AC-11 — Uploaded-paper success state
Successful upload transforms the card into a clear file summary with filename, type/size where available, primary Continue to AI Extraction action, replace-file action and remove-paper action.

### AC-12 — Wrong-paper removal
Before extraction, Remove paper safely clears the active document from the frontend workflow and returns to Source Upload without inventing unsupported backend deletion claims.

### AC-13 — Downstream reset protection
If downstream results already exist, changing/removing the paper requires explicit reset semantics so stale analysis/draft/revisions cannot remain associated with a new source.

### AC-14 — AI Extraction state
Existing process API is reused. UI presents a professional progress state and advances to Review & Refine only after successful processing.

### AC-15 — Draft-first review
After processing, Patent Draft is the default view. Recommended tab order is Patent Draft → Review Items → Analysis.

### AC-16 — Review/revision behavior preserved
Existing edit/save/cancel/revision/review/evidence semantics remain functionally intact.

### AC-17 — Validation remains exact
Existing server-side validation remains mandatory and tied to the exact selected revision. No client-only fake validation is introduced.

### AC-18 — Export remains gated
DOCX Export is reachable/enabled only when the selected revision satisfies the existing validation/export contract.

### AC-19 — Truthful output naming
Current output remains a reviewable/editable draft DOCX. No filing-ready, Claims-complete or implemented-USPTO-v2 claim is introduced.

### AC-20 — Technical metadata de-emphasized
Document ID, correlation ID and comparable implementation metadata remain available where useful but are secondary/collapsed rather than dominating the main product surface.

### AC-21 — Disclaimer cleanup
Large warning cards are removed from the main composition; specialist-review and session/data boundaries are communicated through compact truthful notes/footer copy.

### AC-22 — Accessibility regression protection
Keyboard upload, step navigation, result-tab roving focus, focus-visible, global-error focus, ARIA workflow semantics and reduced motion all remain correct.

### AC-23 — Responsive layout
Desktop/tablet/mobile layouts remain usable without clipped primary actions, unreadable workflow steps, or horizontal page overflow.

### AC-24 — Deterministic navigation regression tests
Playwright coverage verifies:
- five step labels/order;
- Go back behavior;
- reached-step backward/forward navigation;
- inaccessible future-step prevention;
- upload success state;
- remove wrong paper before extraction;
- replace paper;
- Patent Draft default after process;
- validation step;
- export gated until validation;
- New paper/reset clears downstream state.

### AC-25 — Existing public sample flow regression
Public sample flow still supports the authorized sample path through extraction/review/validation/export and does not expose unauthorized arbitrary real-paper processing.

### AC-26 — No backend/runtime semantic change
No backend, prompt, schema, provider/model, DOCX renderer, cleanup, deployment or security/data-policy semantic change occurs.

### AC-27 — Required quality gates
Before independent implementation review:

- full offline backend regression PASS;
- `python -m pip check` PASS;
- frontend lint PASS;
- frontend typecheck PASS;
- frontend build PASS;
- standard Playwright PASS;
- public sample-flow Playwright PASS;
- live provider flags remain 0/0;
- provider/API calls remain NONE;
- `git diff --check` PASS.

### AC-28 — Fixed-SHA independent implementation review
Gemini 3.1 Pro High / Antigravity reviews the exact final implementation SHA in read-only mode and returns PASS with no unresolved blocking finding before merge.

---

## 19. Required implementation test scenarios

At minimum add/update deterministic browser tests for the following.

### T-01 Initial home state
Verify compact header, approved hero, five workflow stages, Source Upload current and no large side warning/environment badge.

### T-02 Normal local upload
Keyboard/file-input upload of a supported paper fixture remains possible and upload constraints are visible.

### T-03 Uploaded paper state
After upload, verify:
- success heading;
- filename;
- Continue to AI Extraction;
- Select a different file;
- accessible Remove paper control.

### T-04 Remove wrong paper
Upload fixture → remove paper → confirm workflow returns to initial Source Upload and old document is not processable.

### T-05 Replace wrong paper
Upload paper A → select paper B → verify B is current source and A does not drive process.

### T-06 Step gating
Before upload, future stages cannot be activated. After each successful prerequisite, newly reached stage becomes navigable.

### T-07 Step backward/forward
Reach Review & Refine → navigate to earlier reached step → navigate forward again → ensure current results are reused and no duplicate process call occurs.

### T-08 AI Extraction
Process request remains single-flight and loading UI maps to stage 2.

### T-09 Draft-first results
After process success, Patent Draft is active by default.

### T-10 Review & Refine
Editing/saving a new revision remains functional and makes that new revision require validation.

### T-11 Validation
Validation request remains single-flight and successful validation advances/reaches stage 5.

### T-12 Export gate
DOCX Export cannot execute before exact revision validation and succeeds afterward.

### T-13 New paper after generated results
Explicit reset/new-paper action clears current result/revision state and returns to Source Upload.

### T-14 Public sample restriction
Public build exposes only currently authorized sample processing behavior and does not enable arbitrary real/confidential document processing.

### T-15 Narrow viewport
Critical actions and five-step navigation remain usable at narrow mobile width.

---

## 20. Implementation handoff to Codex

After this specification PR is independently reviewed and merged, Codex may start implementation under the existing Human authorization.

Implementation branch:

`feat/p2-000-enterprise-saas-webapp`

Baseline:

the then-current verified `main` after P2-000 specification merge.

Codex instructions:

1. read `AGENTS.md`, `PROJECT_CONTEXT.md`, this P2-000 task specification, and current frontend/E2E files;
2. claim/work only inside P2-000 authorized scope;
3. preserve existing logo asset and color tokens;
4. implement the approved layout and workflow navigation;
5. do not change backend/runtime semantics to make the UI easier;
6. extend deterministic Playwright coverage for AC-24/T-01…T-15;
7. run all AC-27 quality gates;
8. commit/push implementation;
9. open implementation PR;
10. return exact implementation SHA, changed-file list, test evidence and CI run;
11. hand off to Gemini 3.1 Pro High / Antigravity for fixed-SHA read-only review;
12. do not merge until required review/CI gates pass.

---

## 21. Subsequent P2 tasks

P2-000 changes the product surface only. It does not implement the semantic patent-generation target.

After P2-000:

1. **P2-002 — Invention Reconstruction**
2. **P2-003 — USPTO Specification Generation v2**
3. **P2-004 — Claims**
4. **P2-005 — Figures/reference numerals**
5. **P2-006 — USPTO DOCX v2**
6. **P2-007 — Grounding/QA**
7. **P2-008 — paper↔patent benchmark**
8. **P2-009 — live product runtime**
9. **P2-010 — end-to-end product acceptance**


---

## 22. Post-merge closeout evidence

P2-000 specification was independently reviewed by **Gemini 3.1 Pro High / Antigravity** on exact SHA `5c57c47d562fa3d003850faf5820ffd17a3be385` with **PASS**, findings **NONE**. PR #59 merged at `3a11d358ba65bb5a83345a96f1e3f464a1a3abc0`.

P2-000 implementation was independently reviewed by **Gemini 3.1 Pro High / Antigravity** on exact SHA `8d63f19ebb755dafef1eafdb47874553be1fcdd3` with **PASS**, findings **NONE**. Implementation CI `36980893272` was **SUCCESS**.

Human / Product Owner then explicitly authorized ChatGPT to merge PR #60, verify post-merge main CI, and perform the P2-000 governance closeout as a **one-time exception** to the current AGENTS.md ChatGPT merge-role restriction.

PR #60 merged at `d0ffd09e0fe29e8a46c04e14b392e3c4aea22731`.

Post-merge main CI `36982485345` completed **SUCCESS** on the exact merge SHA with:

- backend: **467 passed / 2 skipped**;
- Python dependency consistency: **PASS**;
- frontend lint: **PASS**;
- frontend typecheck: **PASS**;
- frontend production build: **PASS**;
- standard Playwright: **24 passed**;
- public sample/demo Playwright: **3 passed**;
- `RUN_OPENAI_LIVE_TESTS=0`;
- `RUN_OPENAI_DRAFT_LIVE_TESTS=0`;
- provider/API calls: **NONE**.

Implementation scope remained exactly the reviewed eight frontend/test files. No backend/runtime semantics, Claims runtime, P2-001 schema, DOCX renderer semantics, production/deployment configuration, provider authorization, or real/confidential-data authorization changed.

BLK-003 remains **OPEN**. EVAL-001 PRODUCT_RUNTIME remains **DEFERRED — AWAITING FUNDING**. Production remains **NOT APPROVED / NOT PERFORMED**.

The original P2-000 governance closeout was independently reviewed on `ddd96548c939bffe71f395011c0b98147cb2f797` with **PASS**, findings **NONE**, and merged through PR #61 at `1bc4f56444451f8fd42f3cc8b8e741b3d0045fa5`. P2-000-R1 was independently reviewed on `cdb5e5bd2cc8f0ef5464bbc11550ad0c34673851` with **PASS**, findings **NONE**, and merged through PR #63 at `fe1b0d52ea4c90fd87ba3ec6139d63e1fa359cd1`.

P2-000-R2 was independently reviewed by **Gemini 3.1 Pro High** on exact SHA `05fc2d3dff6929ada7a4a974428cc26f5256c4fe` with **PASS**, findings **NONE**, and all 10 review requirements **PASS**. Exact-head CI `37008786531` was **SUCCESS**. PR #65 remained at the reviewed three-commit head, was marked ready, and merged normally at `a394a98b0a86b1ce686fac4871f7e5b0c0c3c44f`. Push/main CI `37012025003` completed **SUCCESS** on that exact merge SHA; dependency consistency, backend regression, frontend lint/typecheck/build, standard browser E2E, static-demo build, provider-secret marker scan, and demo browser E2E all passed.

P2-000-R2 changed README/frontend/test presentation behavior only. BLK-003 remains **OPEN**. EVAL-001 PRODUCT_RUNTIME remains **DEFERRED — AWAITING FUNDING**. Provider/API spend remains **NONE / NOT AUTHORIZED**. Real/confidential-data use remains **NOT AUTHORIZED**. Claims runtime remains **NOT IMPLEMENTED**. Production remains **NOT APPROVED / NOT PERFORMED**.

---

## 23. P2-000-R3 — Human Review Gate + Validation/DOCX Workflow Correction

Human / Product Owner authorized P2-000-R3 under `HUMAN-P2-000-R3-HUMAN-REVIEW-VALIDATION-DOCX-2026-10-03`. The implementation baseline was reconciled to `8e38df7ef1427828fdff0a5fc7792bfa5bf03f9a` after the Human verified that the only intervening change from the original authorized baseline was a README-only one-line wording change. That README change is preserved.

The bounded correction requires selected-revision Human review to be complete only when at least one tracked section exists and every tracked section is `REVIEWED (not approved)`. Any `UNREVIEWED` or `NEEDS_CHANGES` section blocks Validation and DOCX Export. Review status changes update eligibility immediately; a review-only change may preserve exact-revision technical validation internally, but export remains blocked until review is complete again. A newly saved revision continues to reset every section to `UNREVIEWED` and clears validation.

The required forward workflow is explicit: Review & Refine navigates to Validation without making the validation request; successful validation remains on Validation and exposes `Continue to DOCX Export`; successful or failed export remains on DOCX Export. Review & Refine must not expose a DOCX download shortcut. Existing single-flight, normalized-error, exact-revision, accessibility, keyboard, responsive, and controlled synthetic PDF/DOCX behavior remains required.

Gemini 3.1 Pro High / Antigravity independently reviewed exact implementation SHA `5569354e7003511d2e761236395ab6a604076530` and returned **PASS**, findings **NONE**, with **15 of 15 requirements PASS**; the reviewer modified no repository files and reported merge suitability **YES**. Exact-head CI `37080649206` succeeded. PR #67 merged normally at `62a25a9ae136461924bc8047c5a6ad0f3550c68c`, and push/main CI `37109553040` succeeded on that exact merge SHA.

The exact-main browser coverage confirms that incomplete Human review cannot reach Validation or DOCX Export; all tracked sections must be `REVIEWED (not approved)` before `Continue to Validation` is enabled; validation PASS remains on Validation; DOCX Export requires the explicit forward action; download remains on DOCX Export; and Review exposes no direct DOCX download shortcut. Render also reports the backend deploy `dep-db0bot5g1s2s738ibku0` and frontend deploy `dep-db0bot5g1s2s738ibl20` **live** on the exact implementation merge SHA. This is evidence for the public synthetic demo only and is not a production approval.

P2-000-R3 implementation is merged. Final task closure remains pending fixed-SHA independent review and merge of the documentation-only governance closeout; no frontend implementation changes belong in that closeout.

Runtime boundaries remain unchanged: BLK-003 is **OPEN**; EVAL-001 PRODUCT_RUNTIME is **DEFERRED — AWAITING FUNDING**; provider/API spend is **NONE / NOT AUTHORIZED**; real/confidential-data use is **NOT AUTHORIZED**; Claims runtime is **NOT IMPLEMENTED**; production is **NOT APPROVED / NOT PERFORMED**.
