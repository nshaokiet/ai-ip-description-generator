# P2-000 — Product Webapp Simplification & Research Paper Entry

## Metadata

| Field | Value |
| --- | --- |
| Task ID | P2-000 |
| Status | **AUTHORIZED — SPECIFICATION / IMPLEMENTATION HANDOFF PREPARATION** |
| Authorization | `HUMAN-P2-000-WEBAPP-SIMPLIFICATION-2026-10-02` |
| Authorization evidence | Human directive on 02/10/2026: “tiếp tục dự án đi”, following the previously agreed next-step roadmap after P2-001 |
| Baseline main | `461d9b33b07bb39aad11aa47b84f678e232d80a8` |
| Specification branch | `docs/p2-000-product-webapp-simplification-spec` |
| Primary implementation owner | Codex under AGENTS.md |
| Independent reviewer | Gemini 3.1 Pro High / Antigravity read-only |
| Classification | Frontend UX/presentation task only |
| Provider/API calls | **NOT AUTHORIZED / NOT REQUIRED** |
| Real/confidential research data | **NOT AUTHORIZED** |
| Production | **NOT APPROVED / NOT PERFORMED** |
| BLK-003 | **OPEN** |

## Purpose

Simplify the product-facing web experience so a researcher can understand the primary workflow immediately:

```text
Upload research paper
→ Generate draft
→ Review / edit
→ Export editable DOCX
```

The current frontend exposes implementation detail such as a five-step technical workflow, correlation/document identifiers, validation state, revision mechanics, analysis-first result navigation and verbose demo/staging copy. P2-000 reduces that cognitive load while preserving the existing runtime contracts, safety controls, accessibility behavior and synthetic-demo restrictions.

P2-000 does **not** claim that the current v1 runtime already produces the P2-001 USPTO v2 target. Until later P2 runtime/renderer work is implemented, the UI must continue to describe the output as a **patent draft** or **editable draft DOCX**, not a filing-ready USPTO specification.

## Product principles

1. **One obvious primary action.** The page should make upload/generation the dominant workflow.
2. **Patent draft first.** After processing, the user should land on the draft rather than the analysis/debug view.
3. **Progressive disclosure.** Technical metadata remains available but is collapsed or visually secondary.
4. **Four user-facing stages.** Upload, Generate, Review, Export. Backend validation remains an implementation/quality gate rather than a top-level product step.
5. **No false capability claims.** Do not label current v1 output as a completed USPTO v2 specification or Claims-enabled output.
6. **Synthetic demo safety remains strict.** Public staging must continue to expose controlled samples only and must not gain an arbitrary file input.
7. **Accessibility is a regression gate.** Existing keyboard/focus/error semantics must remain intact.

## Current frontend observations

Baseline files reviewed on `main`:

- `frontend/src/app/page.tsx`
- `frontend/src/components/UploadPanel.tsx`
- `frontend/src/components/ResultWorkspace.tsx`
- `frontend/src/components/WorkflowProgress.tsx`
- `frontend/src/app/globals.css`
- `frontend/e2e/integration.spec.ts`
- `frontend/e2e-demo/demo-staging.spec.ts`

Current UX characteristics:

- five top-level steps: Upload → Analyze → Review/Edit → Validate → Export;
- large hero and separate notice compete with the upload action;
- validated-document screen exposes MIME type, size, page count and document ID prominently;
- primary generation CTA is labeled “Analyze & Generate Draft”;
- results default to the **Analysis** tab;
- correlation ID and revision internals are prominently visible;
- validation is represented as a first-class user workflow step;
- public demo correctly removes arbitrary upload and offers controlled synthetic PDF/DOCX samples.

## Authorized implementation scope

### A. Header and hero simplification

The implementation may:

- reduce header/hero vertical footprint;
- keep the official VNUHCM Innovation Hub logo and product identity;
- retain the environment badge, but make it visually secondary;
- use concise product copy centered on research-paper → patent-draft workflow;
- preserve the Human/IP-specialist review disclaimer.

Suggested non-demo heading:

> **Turn a research paper into a reviewable patent draft**

Suggested demo heading:

> **Explore the patent drafting workflow**

The exact wording may be adjusted during implementation if it remains accurate and concise.

### B. Four-step user-facing workflow

Replace the five visible product steps with:

1. **Upload** — Choose research paper
2. **Generate** — Build patent draft
3. **Review** — Inspect and revise
4. **Export** — Download editable DOCX

Existing internal `WorkflowPhase` values may remain unchanged. In particular, `validate` may be mapped into the **Review** stage rather than changing backend/frontend API contracts solely for presentation.

### C. Research-paper entry

In normal/local product mode:

- primary heading should clearly say **Upload a research paper**;
- keep one text-based PDF or DOCX, 10 MiB maximum;
- preserve client-side convenience validation and backend source-of-truth validation;
- retain drag/drop and keyboard file chooser behavior.

In public demo/staging:

- preserve controlled synthetic sample buttons;
- preserve **no arbitrary file input**;
- preserve the “do not upload real/confidential/unpublished/sensitive research” boundary;
- preserve provider-free language.

### D. Validated-document state

After upload:

- show filename and validated state prominently;
- move document ID, MIME type, byte size and similar implementation metadata into a collapsed **Technical details** disclosure or equivalent secondary surface;
- retain page count where useful but do not make technical metadata dominate the page;
- rename primary action from **Analyze & Generate Draft** to a simpler truthful label such as **Generate draft**.

### E. Results workspace

After processing:

- default result view must be **Patent Draft**;
- recommended tab order: **Patent Draft → Review Items → Analysis**;
- heading should prioritize the patent draft rather than “Grounded draft workspace”;
- **New paper** or equivalent reset/navigation action must remain available;
- correlation ID and low-level metadata should move into a secondary/collapsible technical area;
- editing/revision behavior and immutable revision semantics must remain unchanged;
- analysis/evidence must remain accessible, only visually secondary.

### F. Validation and export

Validation remains required by the existing backend/export contract.

P2-000 may simplify its presentation, but must not bypass or weaken validation.

The user-facing workflow may treat validation as part of **Review**. Export remains disabled until the selected revision has valid server-side validation.

Until P2-003/P2-006 are implemented:

- export wording must remain **draft DOCX** / **editable DOCX**;
- do not claim that the exported file is filing-ready;
- do not rename the current v1 DOCX to a completed USPTO Specification unless the underlying runtime/renderer contract has actually changed in a separately authorized task.

### G. Responsive and accessibility behavior

Preserve:

- keyboard upload/file chooser;
- tab roving focus;
- visible focus styles;
- error-heading focus;
- `aria-current` workflow semantics;
- live-region status announcements;
- reduced-motion support;
- mobile/narrow-screen behavior.

## Expected implementation files

Implementation should normally be limited to:

- `frontend/src/app/page.tsx`
- `frontend/src/components/UploadPanel.tsx`
- `frontend/src/components/ResultWorkspace.tsx`
- `frontend/src/components/WorkflowProgress.tsx`
- `frontend/src/app/globals.css`
- `frontend/e2e/integration.spec.ts`
- `frontend/e2e-demo/demo-staging.spec.ts`

A small additional frontend file may be changed only when necessary to satisfy the acceptance criteria and must be explained in the handoff.

## Explicitly out of scope

Do **not** modify in P2-000:

- backend API behavior;
- current extraction/drafting prompts;
- v1 schema semantics;
- P2-001 v2 schema semantics;
- Claims generation/runtime;
- DOCX renderer semantics;
- provider/model selection;
- provider/API authorization;
- Render resource topology;
- authentication/storage/retention;
- BLK-003;
- real/confidential-data policy;
- P2-002+ runtime implementation.

## Acceptance criteria

### AC-01 — Primary workflow clarity
A first-time user can identify the main product flow as Upload → Generate → Review → Export without reading technical implementation detail.

### AC-02 — Four visible workflow stages
The top-level workflow component renders exactly four user-facing stages. Backend validation is not presented as a separate top-level product stage.

### AC-03 — Normal-mode research paper entry
Normal/local mode exposes one PDF/DOCX research-paper input with the existing size/type constraints and keyboard/drag-drop behavior.

### AC-04 — Public demo isolation
When `NEXT_PUBLIC_DEMO_STAGING=1`, no arbitrary file input is rendered. Controlled synthetic PDF/DOCX choices and current safety copy remain enforced.

### AC-05 — Concise header/hero
Header and hero consume materially less vertical space while retaining brand identity, environment labeling and Human-review disclaimer.

### AC-06 — Validated document simplification
Filename/validated state and the generation CTA are primary. Document ID/MIME/low-level metadata are visually secondary or collapsed.

### AC-07 — Draft-first results
After processing, the selected/default result view is Patent Draft rather than Analysis.

### AC-08 — Result information hierarchy
Patent draft is primary; Review Items and Analysis/Evidence remain reachable without removing any current review/grounding information.

### AC-09 — New-paper navigation
The result workspace includes an obvious reset action labeled **New paper** or semantically equivalent and preserves existing reset behavior.

### AC-10 — Validation preserved
Server-side revision validation remains mandatory for export. P2-000 must not bypass, fake or weaken validation.

### AC-11 — Truthful export semantics
Current output remains described as an editable/reviewable **draft DOCX**. No filing-ready, Claims-enabled or completed USPTO-v2 claim is introduced.

### AC-12 — No runtime semantic change
No backend, prompt, schema, provider/model, DOCX-renderer or orchestration semantic change is introduced.

### AC-13 — Existing accessibility preserved
Keyboard navigation, focus behavior, error focus, ARIA semantics and reduced-motion behavior continue to pass deterministic tests.

### AC-14 — Responsive presentation
Desktop and narrow/mobile layouts remain usable without clipped primary actions or horizontal overflow in the main workflow.

### AC-15 — Regression coverage
Update/add deterministic Playwright coverage for at least:

- exactly four visible workflow stages;
- normal-mode upload remains available;
- demo mode has no arbitrary file input;
- Patent Draft is default after processing;
- New paper resets to upload state;
- validation still gates export.

### AC-16 — Required quality gates
Before independent implementation review:

- full backend regression PASS;
- `pip check` PASS;
- frontend lint PASS;
- frontend typecheck PASS;
- frontend build PASS;
- standard Playwright PASS;
- Render synthetic-demo Playwright PASS;
- live provider flags remain 0/0;
- provider/API calls remain NONE.

### AC-17 — Independent fixed-SHA review
Gemini 3.1 Pro High / Antigravity must review the exact final implementation SHA in read-only mode and return PASS with no unresolved blocking finding before merge.

## Verification boundaries

Use only synthetic/offline fixtures for implementation verification.

Do not:

- upload a real/unpublished/confidential research paper;
- call OpenAI or another model provider;
- enable live-provider test flags;
- alter Render production/staging resources;
- claim semantic quality or patentability.

## Implementation handoff

After this specification is approved, Codex should:

1. create `feat/p2-000-product-webapp-simplification` from the then-current `main`;
2. modify only the authorized frontend/test scope;
3. run the full required quality gates;
4. push the branch and open a PR;
5. return the final exact SHA and CI run for Gemini 3.1 Pro High fixed-SHA review;
6. not merge until the independent PASS and required CI are both verified.

Because Codex quota is currently unavailable, this specification and review preparation can proceed now; implementation waits for Codex capacity unless the Human explicitly changes the role/implementation authority in `AGENTS.md`.

## Next tasks after P2-000

P2-000 does not implement the P2-001 target contract. It prepares the product surface for subsequent semantic work:

1. **P2-002 — Invention Reconstruction**
2. **P2-003 — USPTO Specification Generation v2**
3. **P2-004 — Claims**
4. **P2-005 — Figures/reference numerals**
5. **P2-006 — USPTO DOCX v2**
6. **P2-007 — Grounding/QA**
7. **P2-008 — paper↔patent benchmark**
8. **P2-009 — live product runtime**
9. **P2-010 — end-to-end product acceptance**
