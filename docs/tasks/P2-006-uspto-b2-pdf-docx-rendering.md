# P2-006 — USPTO B2-Reference PDF + Editable DOCX Rendering Specification

## 1. Status, authority, and dependencies

| Field | Value |
|---|---|
| Task | P2-006 |
| Version | 0.1.0 — PROPOSED / SPECIFICATION ONLY |
| Date | 2026-10-09 (GMT+7) |
| User objective | Produce a technical patent-specification draft with titles, typographic hierarchy, page composition, figures and claims as visually close as feasible to two supplied USPTO B2 references, as high-quality PDF plus editable DOCX |
| References | [US11367264B2 PDF](https://patentimages.storage.googleapis.com/91/f6/9b/18dc2af29220c8/US11367264.pdf) (33 pages); [US11044591B2 PDF](https://patentimages.storage.googleapis.com/42/19/af/1c5089854ab9d4/US11044591.pdf) (19 pages) |
| Technical references | P2-001 target/schema, P2-002 reconstruction, P2-003 v2 disclosure, P2-004 supported Claims, P2-005 proposed `USPTO_DOCUMENT_PACKAGE` |
| Base branch | `main` at `155ed888510380c2d8d7cba2e7e1aa0e81b54ed4` |
| P2-005 | PR #96, separate proposed specification on `docs/p2-005-uspto-assembly-specification`, head `b0f71abdeb37f7474b2b197fdfbe2edf90ee2dea`; **not merged or approved** at drafting |
| Intended implementer | Codex, only after independent spec review and explicit separate Human implementation authorization |
| Independent reviewer | Gemini 3.1 Pro High / Antigravity read-only (Security and Quality separately if subsequently explicitly enrolled in Workflow V2) |
| Current state | DRAFT — no code, render, output, tests, API spend or production authorization claimed |

This document is a **specification proposal**, not authorization to write P2-006 implementation code, run paid providers, process real/confidential papers, activate P2-007, amend P2-001…P2-004, merge the PR, or claim USPTO filing readiness. Follow AGENTS.md conditional Workflow V2; enrollment is explicit-only, external/manual review checks remain mandatory.

## 2. Reference observations — what fidelity means

The two **issued** U.S. B2 PDFs share these visually observable conventions:
- Portrait monochrome pages; large, formal serif type and black rules on the front page.
- A two-area **published-patent first page** with patent title (54), available bibliographic fields, Abstract (57), and a representative technical figure; issued-only fields include grant number/date and actual prosecution metadata.
- Separate patent drawing sheets with black/white diagram line art, `FIG. n` references and figure-sheet headers.
- Compact two-column patent **published-body** typography, running header/page numbers, formal uppercase centered section headings, justification and marginal line numbers at approximately five-line intervals.
- Technical narrative expressed under Background, Summary, Drawings, Detailed Description and numbered Claims; formats differ in optional headings, never require copying either patent's actual technical text.

**Target:** emulate the references' visual grammar, not a byte-for-byte replica of an issued patent, a counterfeit USPTO grant or a reproduction of either patent's scientific text/figures. Exact fonts and page proportions must be checked against rendered reference screenshots, not guessed to be pixel-identical.

**Crucial legal/format distinction:** The official nonprovisional utility **application** is normally a single-column, 1.5- or double-spaced specification on US Letter/A4; Claims and Abstract start on separate sheets (37 CFR 1.52(b)(2), 1.72, 1.77). The two-column B2 issued-patent look therefore must be labelled a **reference-style publication preview**, never "filing-compliant".

## 3. Deliverables and modes (proposed)

### Primary: `B2_REFERENCE_PREVIEW` (priority 1)

- `patent-b2-reference-draft.pdf`: canonical print-quality, selectable/searchable PDF with an issued-patent-inspired cover, drawing sheets if authorized source artwork exists, and two-column specification body.
- `patent-b2-reference-draft.docx`: editable Word document with closely matching headings, two-column sections and editable claim text; fidelity priorities in Section 8 apply to Word/LibreOffice differences.
- `patent-review-package.json` and/or separate optional `patent-review-report.pdf` **only if separately approved**: evidence/grounding/missing questions; this sidecar is NEVER mixed into filing-style text.
- Clear on-document identifier: `PATENT SPECIFICATION DRAFT — NOT ISSUED` on the cover and unambiguous draft marker in running headers. Never reproduce an actual USPTO-issued grant number, grant date, barcode or official status.

### Secondary: `USPTO_APPLICATION_DRAFT` (priority 2)

- `patent-application-draft.docx` and PDF export generated from the same validated semantic content, in **single column, 1.5-spaced, approximately 12pt nonscript font**, with suitable margins, consecutive page numbers and **Claims/Abstract on new pages**.
- Intended as an editable Human/IP-specialist review copy, **not** a promise of complete submission compliance; filing requirements and data/ADS/claims must be separately reviewed.
- Secondary mode **may be delivered after primary mode** but is an explicit acceptance target of P2-006; it cannot be used to justify lowering the reference-preview visual QA requirement.

Both modes must render identical validated technical substance, claim ordering/dependencies, Abstract, and missing-content status. Different styles never add technical facts or legal assertions.

## 4. Canonical output content and headings

The complete filing-style semantic outline follows P2-001 and P2-005; preserve exact supported text without model rewriting in renderer:

1. `TITLE OF THE INVENTION`
2. `CROSS-REFERENCE TO RELATED APPLICATIONS`
3. `STATEMENT REGARDING FEDERALLY SPONSORED RESEARCH OR DEVELOPMENT`
4. `NAMES OF PARTIES TO A JOINT RESEARCH AGREEMENT`
5. `INCORPORATION BY REFERENCE`
6. `STATEMENT REGARDING PRIOR DISCLOSURES`
7. `BACKGROUND OF THE INVENTION`, including `FIELD OF THE INVENTION` and `DESCRIPTION OF RELATED ART` where supported
8. `BRIEF SUMMARY OF THE INVENTION`
9. `BRIEF DESCRIPTION OF THE DRAWINGS`
10. `DETAILED DESCRIPTION OF THE INVENTION`
11. `CLAIMS`
12. `ABSTRACT OF THE DISCLOSURE`
13. `SEQUENCE LISTING`, only if applicable/supported

Headings visually echo B2 publications: serif uppercase, centered, controlled space above/below and keep-with-next; distinguish main/secondary headings, avoid orphaned headings. The cover uses an independently rendered **(54) invention title** and **(57) Abstract** drawn from the same canonical data; this visual duplication never creates a second semantic Abstract source. Brief Summary and Abstract are distinct. Abstract stays <=150 words under the released validation rule.

No title, applicant, inventor, assignee, filing/priority date, grant information, classification, examiner, cited prior art or government funding may be invented. When unsupported: omit unconfirmed front-page metadata, keep section visibility/status policy from P2-005, and put targeted author questions in separate review data; never turn missing status into "Not Applicable" without authorized basis.

The two reference patents' original invention titles and figures are **style examples only**, never generated content for another paper.

## 5. Page composition and visual profile

**Page size:** US Letter portrait (8.5 x 11 in), black on white; minimum stable print margins and no clipping. B2 preview style is a **published-patent look**, not 37 CFR filing-form mode.

**Front page**:
- Upper typographic system: prominent neutral `PATENT SPECIFICATION DRAFT — NOT ISSUED`, unobtrusive draft identifier/version, strong horizontal rule, formal black serif headings.
- Approximate bilateral cover layout: left column `(54) TITLE OF THE INVENTION` and verified optional source/admin descriptors; right column `(57) ABSTRACT` and nonfabricated supported technical overview.
- No `(12) United States Patent`, no `(10) Patent No.`, no `(45) Date of Patent`, no actual official USPTO logo/seal/barcode or copied real-patent IDs.
- Title uppercase/bold and wrapped without distortion. Abstract justified and readable. If supported: show actual emitted Claim count and actual approved drawing-sheet count; never reference 21 Claims / 18 Drawings or other reference counts.
- Lower figure space contains **only** a permission-cleared, source-supported representative figure. With no such figure, do not fabricate, borrow from the B2 patents, or synthesize an ungrounded "technical" figure. Reflow cover if empty; report drawing gap in review sidecar.

**Drawings**:
- Dedicated single-column sheets, vector/high-resolution black-line art when source-verified and rights-cleared; centered `FIG. 1`, `FIG. 2` labels and sequential sheet index; source figure ↔ disclosure ↔ claims reference numerals checked.
- Preserve figure aspect ratio, captions, visibility and text contrast; no blurred scaling. Do not create false source-evidence drawings or redraw complex figures automatically.
- Current P2-002/P2-003 are not a pixel-level drawing extraction/approval pipeline. **Drawing ingestion/reuse is an explicit dependent capability**, not silently granted by this renderer spec. For unapproved figures, render zero drawing pages and show the missing figure requirement separately.

**Body**:
- Two balanced, justified text columns, compact serif font visually calibrated from the two originals; consistent intercolumn gutter, baseline rhythm, hyphenation strategy and page numbering.
- Optional marginal line numbers at 5, 10, 15… and visible column-page numbering, but never by colliding with body text. Repeated draft running header must remain clearly non-issued.
- Heading hierarchy centered/uppercase; body paragraph indentation and spacing coherent, supported FIG references anchored to actual figures only.
- Avoid split figures, rows, claim numbers, heading or citation path; no crowding/cut-off at column breaks, headers, footers, page transitions.
- Claims numbered 1, 2, 3... with indentation and exact independent/dependent relationships, no orphaned claim numbers, no fabricated preamble when Claims are absent; visibly mark an incomplete Claims status as requiring Human/IP review rather than pretending legal completeness.
- No legal readiness seal, attorney approval, examiner language, counterfeit patent number, invented filing status or garbled glyphs.

**Application mode**:
- Use USPTO application-oriented single-column layout, 1.5/double spacing and at least the prescribed margins; centered consecutive page numbers; new sheet for Claims and Abstract; Title as first heading.
- Prefer clean editable 12pt text. Render missing/not-applicable states conservatively and keep review notes outside filing-facing sections. This mode is still UNREVIEWED.

## 6. Data contracts and rendering architecture

- Renderer consumes only a **validated**, already assembled `USPTO_DOCUMENT_PACKAGE` (future P2-005), with explicit version and content identity; rejects arbitrary JSON, mismatched hashes, stale Claims, manipulated numbering or unsupported source assets.
- Use **one canonical semantic filing view** and deterministic template-driven presentation profiles. Renderers do not call any model, invent claims, paraphrase source, calculate patentability or merge conflicting source facts.
- Keep full P2-002/003/004 provenance in an immutable review-sidecar link. Filing-style body must not leak raw evidence IDs, JSON pointers, metadata/audit notes or provider logs.
- New modules, templates and output paths are **additive and versioned**. Preserve `PatentDocxRenderer`, v1 `/api/exports/docx`, old schema/contracts, existing frontend and deployment unchanged unless separately authorized.
- Define deterministic font fallbacks with embeddable, non-restricted fonts; check PDF font embedding/searchable text and consistent Unicode typography.
- PDF and DOCX must come from the same canonical content and be verified for **text-equivalence**; DOCX is editable, but precise pagination may vary with installed fonts/Word rendering. PDF is authoritative for pixel-level B2 style.
- Establish explicit file-cleanup/temporary retention rules for eventual API integration; this spec does **not** authorize a new public export endpoint.

## 7. Visual QA corpus and repeatable verification

Official reference baselines:
- US11367264B2 page 1: two-zone granted-patent cover; 18 drawing sheets; first body page (PDF page 20) two-column paragraph/section style.
- US11044591B2 page 1: similar cover; 7 drawing sheets; first body page (PDF page 10) two-column Background/Summary style.

Required QA:
1. Inspect reference PDFs directly; record page anatomy and geometries in non-copyright-substitutive **layout metrics** (paper size, cover zones, heading alignments, type scale, column widths/gutter, line numbering, drawing proportions).
2. Produce synthetic A/B fixtures with enough supported content to span multiple body pages, Claims and at least one **explicitly authorized synthetic** representative drawing. Test no-figure/no-Claims/missing-metadata variants separately.
3. Render each output PDF at >=200 dpi (prefer 300 for print QA); inspect front page, first drawing page, first content page, a column-break page, Claims page and final page. Spot-check every page for overflow/fragmentation and text completeness.
4. Perform side-by-side screenshot review against **both** B2 references on layout (not on replicated patent content). Fix defects and rerender. Reviewer records matched/unmatched structural characteristics without claiming unsupported numeric "visual similarity %" scores.
5. DOCX -> PDF render in a reproducible office engine; compare typography/sections/content/figures against canonical PDF, disclose expected page-drift limitations; manual Microsoft Word visual check when available.
6. Print-oriented PDF preflight: valid page size, selectable/searchable text, embedded fonts or safe fallback, high-contrast figures, correct reading order, no unintended rasterized full-text pages, corrupted PDF, missing pages, text clipping, overlapping margins, broken diacritics/symbols or blank figure shells.
7. Source-content QA: no source text copied from either reference patent, no unsupported real-patent identifiers, no review-package leak, no unapproved drawing. Verify identical ordered claims/abstract in PDF+DOCX.
8. Security & compatibility QA: synthetic only, no provider calls, real paper, browser retrieval, network/personal data processing, v1 regression break or production deploy. Record tests with exact code SHA.

## 8. Priorities and acceptance criteria

**Priority P0**: correct supported technical content, source grounding, safety/non-issued status; stable PDF with **two-column B2-like** profile; clean cover, section headings, actual supported Claims/Abstract, readable diagram policy, no provenance leakage; DOCX text editable and export parity.

**Priority P1**: polish line numbering/pagination/hyphenation, richer vetted figures and reference numerals, high fidelity Word layout parity, single-column USPTO application-draft export.

**Priority P2**: optional additional print-archive compliance, document-accessibility enhancements and reference-style variants, only if separately approved.

| AC | Required verification |
|---|---|
| AC-01 | Scope/spec-only, explicit implementation gate and exact provenance respected |
| AC-02 | Both actual B2 reference PDFs visually inspected; structural metrics/limits documented |
| AC-03 | Two unambiguously distinct `B2_REFERENCE_PREVIEW` and `USPTO_APPLICATION_DRAFT` profiles |
| AC-04 | Canonical P2-001 headings/subsections, Claims/Abstract/sequence listing as applicable |
| AC-05 | Black-and-white US Letter B2 cover with two areas and supported (54)/(57) data |
| AC-06 | No fake B2 patent metadata, grant logo/barcode/status/identifier or copied patent wording |
| AC-07 | Correct serif two-column bodies, uppercase headings, margins, page/line numbering; no overflow |
| AC-08 | Drawing-sheet/source-rights/FIG-reference policy is fail-closed and testable |
| AC-09 | Claims numbering/independent-dependents/prelude faithful to validated package, no filler |
| AC-10 | Abstract <=150 words; cover excerpt and canonical body source remain identical |
| AC-11 | Missing metadata/Claims/drawings are not guessed, suppressed or marked applicable without basis |
| AC-12 | Filing-view is separate from review JSON and not mislabeled ready-for-filing |
| AC-13 | Both PDF and **editable** DOCX export; text parity; PDF is visually authoritative |
| AC-14 | Official application-draft variant is single column, 1.5/double-spaced with separate Claims/Abstract pages |
| AC-15 | Offline synthetic positive/negative/regression tests include mutation, renderer escape and malformed source |
| AC-16 | PDF render preflight and screenshot QA on all layout classes and multiple-page samples |
| AC-17 | Independent fixed-SHA reviewer scores visible layout/heading consistency against both references |
| AC-18 | Old DOCX v1 path and released P2-001/002/003/004 contracts untouched |
| AC-19 | No paid API, no real/confidential paper, no production or new public endpoint in task |
| AC-20 | Human/IP-review warning, non-issued status and legally conservative presentation always visible |

If a font/renderer combination cannot satisfy B2 two-column body/line numbering reliably, record a blocking finding and propose an explicit alternative architecture rather than silently shipping a lower-fidelity artifact.

## 9. Handoff and task order

1. P2-005 is still proposed in PR #96. Freeze/review/approve its assembly contract and implement through **separately authorized** Codex work, fixed-SHA review, required CI and merge before P2-006 renderer implementation.
2. For P2-006, first independently review this **spec-only** PR with exact SHA, attach Human decisions and approved frozen version. No implementation or auto-merge solely from this draft.
3. After approval: implement deterministic PDF + editable DOCX templates, QA/reference fixtures, test/report evidence. Review Security and Quality independently if V2 admitted per canonical adoption policy; exact-head CI; guarded merge; postmerge closeout.
4. P2-007 (separately scoped): connect real-paper upload/extraction/provider to P2-002/003/004/005/006 only after funding/provider rights, BLK-003 authentication/storage/retention, real-data permission and semantic acceptance gates. Until then **offline synthetic only**.
5. If approved illustrations are unavailable, deliver a text-only patent draft with drawing requirements reported explicitly, not a fabricated full visual patent.

## 10. Review stop conditions

- STOP if this requires modifying P2-001 v2.0.0 `claims_runtime_implemented=false`, P2-003 exact generation, P2-004 support rules, v1 endpoint/export or real-data/provider boundaries.
- STOP if P2-005 output type/missing state/figure entitlement are insufficient to implement this contract without unsupported assumptions; request precise P2-005 spec reconciliation/re-review.
- STOP if a file would misleadingly appear to be a granted B2 patent or a validated submission.
- STOP before merging this specification PR and before implementing P2-006. Human authorization is a separate recorded decision.

**This spec locks the desired appearance and deliverable plan, not the current implementation state.**
