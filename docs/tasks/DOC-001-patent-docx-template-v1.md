# DOC-001 — Patent DOCX Template v1.0.0

## Metadata

| Field | Value |
|---|---|
| Task ID | DOC-001 |
| Status | Gemini Review Passed — Awaiting Human Merge Approval |
| Owner | ChatGPT/Codex |
| Reviewer | Gemini 3.1 Pro High + Human / Product Owner |
| Version | 1.0.0 |
| Date | 20/09/2026 |
| Decision record | `docs/decisions/ADR-009-patent-docx-template-v1.md` |

## Objective

Create the canonical English Patent DOCX Template v1.0.0 and a deterministic offline renderer for payloads valid against Patent Draft Generation Contract v1.0.0.

The output is an AI-generated technical draft requiring Human review. It is not legal advice, a patentability assessment, a filing-ready application, or a complete patent filing.

## In scope

- Versioned DOCX template, manifest, mapping, renderer, synthetic fixtures, automated tests, and supporting documentation.
- Exact eleven-part document order and seven canonical subsections.
- A4, 2.54 cm margins, approved Times New Roman styles, header/footer, PAGE/NUMPAGES fields.
- Schema validation before rendering, safe escaping, missing/conflict/inference preservation, author questions, and evidence appendix.
- One ignored representative output for Human visual QA.

## Out of scope

- Claims or Draft Claims.
- Legal advice, novelty/inventive-step conclusions, patentability assessment, or filing-ready representation.
- PDF export, technical image generation, backend/frontend/API/database/provider integration, live-model calls, deployment, and real research data.
- Changes to AI-001, AI-002, or AI-003 technical contracts.

## Acceptance criteria

- [x] Canonical template, manifest, mapping, renderer, fixtures, tests, ADR, and documentation exist at the approved paths.
- [x] Renderer accepts an input JSON path and output DOCX path, validates the canonical schema first, and returns nonzero on invalid input.
- [x] Renderer uses the canonical template through `docxtpl`, enables automatic escaping, makes no network/model call, and writes only under the approved generated-output root.
- [x] Template package is a valid macro-free DOCX with no embedded active content, remote image, or unapproved external relationship.
- [x] Page setup, typography, line/paragraph spacing, header, footer, PAGE, and NUMPAGES match the approved contract.
- [x] Exact section/subsection order is preserved and Claims/Draft Claims are absent.
- [x] Abstract is retained, limited by the validated contract to 150 words, and renders the exact marker when missing.
- [x] Missing sections retain headings and `[AUTHOR CONFIRMATION REQUIRED]`.
- [x] Conflicts remain unresolved; INFERENCE remains explicit; absent drawings are labeled proposed/not supplied; author questions and used evidence are rendered.
- [x] Special characters and Jinja-like input render as escaped data with no unresolved template markers.
- [x] All fixtures are synthetic and contain no secret, PII, or real research data.
- [x] AI-001, AI-002, and AI-003 regressions pass.
- [x] DOC-001 automated tests pass and `git diff --check` succeeds.
- [x] Human visual QA in Microsoft Word is complete: page fields/layout, pagination/typography, header/footer, section order, evidence appendix, placeholder/overflow, and claims exclusion all `PASS`; no findings.
- [x] Gemini 3.1 Pro High independent review is complete with verdict `PASS`, no findings, no required changes, and recommendation `APPROVE`; DOC-001 remains pending Human merge approval.

## Manual visual QA

Open `generated/patent-docx/v1.0.0/representative-patent-draft.docx` in Microsoft Word. Check A4 layout, margins, font hierarchy, header/footer, page fields, section order, lists, evidence appendix, clipping, broken placeholders, and absence of Claims. If required, press `Ctrl+A`, then `F9` to refresh PAGE/NUMPAGES.

Human Visual QA and Gemini independent review are recorded as `PASS`; 85/85 tests passed. Implementation commit, Pull Request, and merge commit have not been created. Do not mark DOC-001 `Completed` until the subsequent Human merge decision is recorded.
