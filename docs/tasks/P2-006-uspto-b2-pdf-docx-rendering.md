# P2-006 — USPTO B2-Reference PDF + Editable DOCX Rendering Specification

## 1. Status, authority, and dependencies

| Field | Value |
|---|---|
| Task | P2-006 |
| Version | 0.2.0 — RECONCILED SPECIFICATION / INDEPENDENT REVIEW PENDING (supersedes 0.1.0) |
| Date | 2026-10-09 (GMT+7) |
| User objective | Produce a technical patent-specification draft with titles, typographic hierarchy, page composition, figures and claims as visually close as feasible to two supplied USPTO B2 references, as high-quality PDF plus editable DOCX |
| References | [US11367264B2 PDF](https://patentimages.storage.googleapis.com/91/f6/9b/18dc2af29220c8/US11367264.pdf) (33 pages); [US11044591B2 PDF](https://patentimages.storage.googleapis.com/42/19/af/1c5089854ab9d4/US11044591.pdf) (19 pages) |
| Technical references | P2-001 target/schema, P2-002 reconstruction, P2-003 v2 disclosure, P2-004 supported Claims, P2-005 released `USPTO_DOCUMENT_PACKAGE v1.0.0` |
| Base branch | `main` at `1d1ad1ad3721d641346c3df359661fa5524602a4` (non-destructively integrated into existing PR #97 branch) |
| P2-005 | **CLOSED / COMPLETED — MERGED**; P2-005 spec PR #96, implementation PR #98, governance PR #99, final PR #100; terminal main `1d1ad1ad3721d641346c3df359661fa5524602a4` and [verified receipt](https://github.com/nshaokiet/ai-ip-description-generator/pull/100#issuecomment-6076674154). Old unapproved status is retained in PR history, not current. |
| Intended implementer | Codex, only after independent spec review and explicit separate Human implementation authorization |
| Independent reviewer | Gemini 3.1 Pro High / Antigravity read-only (Security and Quality separately if subsequently explicitly enrolled in Workflow V2) |
| Authorization (Human-provided) | `HUMAN-P2-006-SPEC-RECONCILIATION-2026-10-09` — specification reconciliation **only**; no external approval URL claimed |
| Current state | **UPDATED SPECIFICATION / READY FOR INDEPENDENT FIXED-SHA REVIEW** once committed and checked; no implementation or Human specification freeze approval |

This document is a **Human-authorized specification reconciliation**, not authorization to write P2-006 implementation code, run paid providers, process real/confidential papers, activate P2-007, amend P2-001…P2-004, merge the PR, or claim USPTO filing readiness. Follow AGENTS.md: **Workflow V1** unless separately explicitly enrolled in V2. No V2 enrollment or independent review PASS is inferred.

## 2. Reference observations — what fidelity means

The two **issued** U.S. B2 PDFs have been visually inspected at **cover page and first two-column body page** in both sources (US11367264B2 PDF pp.1/20; US11044591B2 PDF pp.1/10). These are qualitative observations, **not measured design parameters or P2-006 output QA**:
- Portrait monochrome pages; large, formal serif type and black rules on the front page.
- A two-area **published-patent first page** with patent title (54), available bibliographic fields, Abstract (57), and a representative technical figure; issued-only fields include grant number/date and actual prosecution metadata.
- Separate patent drawing sheets with black/white diagram line art, `FIG. n` references and figure-sheet headers.
- Compact two-column patent **published-body** typography, centered running identifier, page/column numbering, serif headings, justified paragraphs and marginal line numbers at approximately five-line intervals. Exact dimensions/font names require actual measurement during later QA.
- Technical narrative expressed under Background, Summary, Drawings, Detailed Description and numbered Claims; formats differ in optional headings, never require copying either patent's actual technical text.

**Reference evidence:** US11367264B2 has 33 PDF pages, 18 drawing sheets and body at PDF p.20; US11044591B2 has 19 PDF pages, a references continuation at p.2, 7 drawing sheets and body at PDF p.10. **Target:** emulate visual grammar, not a byte-for-byte replica of an issued patent, a counterfeit grant or reproduction of either patent's text/figures. Exact fonts and page proportions must be checked against rendered reference screenshots, not guessed to be pixel-identical.

**Crucial legal/format distinction:** The official nonprovisional utility **application** is normally a single-column, 1.5- or double-spaced specification on US Letter/A4; Claims and Abstract start on separate sheets (37 CFR 1.52(b)(2), 1.72, 1.77). The two-column B2 issued-patent look therefore must be labelled a **reference-style publication preview**, never "filing-compliant".

## 3. Deliverables and modes (proposed)

### Primary: `B2_REFERENCE_PREVIEW` (priority 1)

- `patent-b2-reference-draft.pdf`: canonical print-quality, selectable/searchable PDF with an issued-patent-inspired cover, drawing sheets if authorized source artwork exists, and two-column specification body.
- `patent-b2-reference-draft.docx`: editable Word document with closely matching headings, two-column sections and editable claim text; fidelity priorities in Section 8 apply to Word/LibreOffice differences.
- Internal isolated review/QA view may consume validated P2-005 `review_package`. Any **distributed** `patent-review-package.json` or separate review PDF requires separate Human approval; NEVER mix evidence, grounding, warnings, author questions or raw source with filing-style prose.
- Clear on-document identifier: `PATENT SPECIFICATION DRAFT — NOT ISSUED` on the cover and unambiguous draft marker in running headers. Never reproduce an actual USPTO-issued grant number, grant date, barcode or official status.

### Secondary: `USPTO_APPLICATION_DRAFT` (priority 2)

- `patent-application-draft.docx` and PDF export generated from the same validated semantic content, in **single column, 1.5-spaced, approximately 12pt nonscript font**, with suitable margins, consecutive page numbers and **Claims/Abstract on new pages**.
- Intended as an editable Human/IP-specialist review copy, **not** a promise of complete submission compliance; filing requirements and data/ADS/claims must be separately reviewed.
- B2-first and application-second are **implementation order only**. **Both profiles, each in PDF and editable DOCX, are P0 mandatory final acceptance gates**. A primary-only intermediate milestone is NOT P2-006 completed; scope reduction requires a separate Human decision.

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
- Released P2-005 provides **figure metadata only**, no approved image bytes, rights, MIME or figure-asset attestations. Drawing ingestion is separately permission-gated; without verified rights-cleared binary assets render **zero drawing pages**, no fabricated figure. Put missing-asset details only in isolated review data; synthetic approved test art is for offline QA, not real-source entitlement.

**Body**:
- Two balanced, justified text columns, compact serif font visually calibrated from the two originals; consistent intercolumn gutter, baseline rhythm, hyphenation strategy and page numbering.
- Optional marginal line numbers at 5, 10, 15… and visible column-page numbering, but never by colliding with body text. Repeated draft running header must remain clearly non-issued.
- Heading hierarchy centered/uppercase; body paragraph indentation and spacing coherent, supported FIG references anchored to actual figures only.
- Avoid split figures, rows, claim numbers, heading or citation path; no crowding/cut-off at column breaks, headers, footers, page transitions.
- For validated `PRESENT` Claims, preserve exact ordinals, texts, dependencies and preamble. For `HUMAN_CONFIRMATION_REQUIRED`, keep the CLAIMS heading but print a non-numbered visible draft-state marker, e.g. `[CLAIMS INCOMPLETE — HUMAN CONFIRMATION REQUIRED; NO CLAIM TEXT SUPPLIED]` **outside legal claim prose**, with no Claim 1 or fabricated preamble. Keep detailed issues in review-only data.
- No legal readiness seal, attorney approval, examiner language, counterfeit patent number, invented filing status or garbled glyphs.

**Application mode**:
- Use application-oriented single-column layout, 1.5/double spacing, margins checked against applicable 37 CFR, centered consecutive page numbers, new sheet for Claims and Abstract, Title first. This is UNREVIEWED and NOT a certified filing-compliant output.
- Prefer clean editable 12pt text. Render missing/not-applicable states conservatively and keep review notes outside filing-facing sections. This mode is still UNREVIEWED.

## 6. Released P2-005 schema and mandatory renderer trust boundary

### 6.1 Actual source contract (verified on terminal main)

- Released sources: `schemas/uspto-document-package/v1.0.0/uspto-document-package.schema.json` (JSON Schema Draft 2020-12), `backend/app/services/uspto_document_package.py` and `backend/app/services/uspto_document_package_validation.py`. No public v2 renderer/export endpoint exists.
- Required top-level fields (strict additionalProperties): `schema_version` = `1.0.0`, `output_type` = `USPTO_DOCUMENT_PACKAGE`, `package_id`, `source_identity`, `input_digests`, `generation_config`, `filing_view`, `review_package`, `review_boundary`.
- `input_digests` carries five canonical SHA256 digest fields: `source_envelope`, `structured_analysis`, `reconstruction`, `specification`, `supported_claims`. `package_id` has form `p2-005-<24 lower-hex>`. Neither ID nor self-asserted digests constitute authenticated provenance, signatures or a complete upstream proof.
- `filing_view` = `document_metadata`, `section_order` (fixed 13 canonical entries), `sections` (11 ordered sections excluding separate Claims and Abstract), `claims`, `abstract`. Render sections by the **schema's order**, not by guessing section array offsets. Released `document_metadata.language=en`: engine Unicode capability does not authorize translation or arbitrary multilingual upstream records.
- Each `sections[*]` includes validated `section_id`, `sequence`, `heading`, `status`, `paragraphs`, `subsections`, `figures` and `missing_information_ids`; `paragraph.text` is filing prose, while `support`, evidence IDs, JSON paths, `not_applicable_basis` and missing-information identifiers are **not** filing prose.
- `filing_view.claims` has `section_id=CLAIMS` and `sequence=11`: if `status=PRESENT`, it includes validated consecutively numbered `claims[]` (`claim_number`, `claim_type`, `independent_or_dependent`, `depends_on`, `claim_text`, `claim_elements`), zero missing IDs and exact `preamble="What is claimed is:"`; if `status=HUMAN_CONFIRMATION_REQUIRED`, it has `claims=[]`, nonempty `missing_information_ids` and no preamble.
- `filing_view.abstract` is separate, with `section_id=ABSTRACT_OF_THE_DISCLOSURE`, `status`, `text`, `word_count<=150`, `support` and `missing_information_ids`; non-PRESENT means no source Abstract text may be fabricated.
- `review_package`: `original_p2_003`, `original_p2_004`, `projected_claim_support`, `assembly_missing_information`. `review_boundary` fixes `status=DRAFT`, `review_status=UNREVIEWED`, `human_ip_review_required=true`, `filing_ready=false`, `source_document_synthetic=true`, `render_review_metadata_as_filing_content=false`, `p2_003_claims_runtime_implemented=false` and nonlegal/nonpatentability flags.

### 6.2 Non-negotiable public validation before rendering

1. A **trusted internal offline caller** passes the package and **all seven original upstream inputs**: `source_envelope`, `structured_analysis`, `reconstruction`, `specification`, `p2_003_generation_config`, `supported_claims`, `p2_004_generation_config`. Do not accept a standalone uploaded JSON package as validated output.
2. Immediately call `validate_uspto_document_package(package, **original_inputs)` from the **public** released P2-005 validator **before any template rendering, file creation, asset decoding or network**. It checks APP-002/AI-001→P2-002 reproduction, P2-003/P2-004 source/config/Claims validity, strict schema and full exact-value reprojection. Its stable `USPTODocumentPackageValidationError.code` and safe `paths` are the only allowable surfaced failure diagnostics; never echo paper contents or unknown raw keys.
3. Upon success, deep-copy the allowed `filing_view` into a typed **internal immutable-in-use render model** with fixed profile settings. Separately retain isolated `review_package` for internal Human review, **never** for filing text. Fail closed with **no output artifact** on invalid version, package/Claim/data mutation, missing sidecar, mismatched original input, malformed structure, unsafe figure, path traversal or injected markup.
4. **Reject** unsigned receipts, caller Boolean `validated=true`, content hash/ID alone, cache assertion, claimed cryptographic origin or a caller-supplied `source_document_synthetic` as proof. P2-003 original `claims_runtime_implemented=false` remains unchanged. Never use private `_assemble_verified` to bypass the validator or relabel a P2-005 package as P2-001 runtime-true.
5. Alternative not authorized: an authenticated signed validator receipt / brokered validated render job. P2-005 contains **no released issuer/trust-root/signature/receipt schema**. Such a path requires **separate Human architecture/security approval and independently reviewed, versioned interface**. Until then use the seven-input in-process validation path.

### 6.3 Semantic rendering and incomplete content

- One ordered semantic model drives both profiles and both file formats; render only verified `paragraph.text`, subsection headings, the validated Title and Abstract, and `claims[*].claim_text` with exact numbering/`depends_on`. Do not paraphrase, change technical case/numbers, introduce claim limitations, recalculate support or infer administrative metadata. Claim elements and source paths are audit data, **not a license to recompute claims**.
- Distinguish present vs missing status in every mode. `PRESENT` renders supported text. `MISSING`/`HUMAN_CONFIRMATION_REQUIRED` keeps the section heading and a **clearly styled draft-status marker**, not substantive filing prose; `NOT_APPLICABLE` only if already validated with its original required basis. Never infer Not Applicable or invent contents. Keep issue IDs/warnings/questions separate.
- For missing Claims, show `CLAIMS` plus **[CLAIMS INCOMPLETE — HUMAN CONFIRMATION REQUIRED; NO CLAIM TEXT SUPPLIED]** in a visually distinct non-numbered status block. No Claim text/preamble, no claim number, no false filing completeness. For valid positive Claims, use **exact** source numbering, text, single-parent dependency structure; keep opening number with first line and prevent column or page orphaning.
- If Abstract is present, the cover (57) and body Abstract draw from the **same** verified `abstract.text`, not separate generated excerpts. If absent, both show an explicitly labeled incomplete status only. Never fabricate inventor/assignee/filing/grant/priority data, examiner identity, prior-art determination or government support.

## 7. Figures, rights, FIG references and missing assets

The **released** `filing_view.sections[*].figures` holds descriptive `figure_id`, `figure_label`, `title`, `description`, `source_figure_ids` and `reference_numerals`, but **no image binary, approved asset digest, source licensing or consent**. Presence of `FIG. 1` metadata is not permission to reproduce a drawing.

- Default **fail closed**: no independently approved, rights-cleared binary asset ⇒ **zero drawing sheets and no representative cover image**. Do not fetch any URL, copy either B2 reference's images, auto-synthesize an illustration or pretend metadata is a rendered drawing. Retain source/asset gap in review data only.
- Future production entitlement would require a **separately Human-authorized and validated** versioned asset manifest: `figure_id` / `figure_label` ↔ verified source ID ↔ image digest/bytes/MIME/dimensions ↔ explicit rights/synthetic authorization ↔ representative selection/reference numerals, with size/sanitization/retention constraints. P2-005 supplies **no** such contract; this specification does not authorize implementation of one.
- Offline synthetic fixture art (explicitly rights-cleared and synthetic) may test draw-sheet positioning, captions, FIG ordering, cover representative-figure branch and aspect ratio **without** claiming the authentic/public approved drawing pipeline exists.
- Reject invalid/missing manifest, duplicate/unsupported FIG labels/references, mismatched source mapping/asset digest, unlicensed/confidential art, external SVG/scripts/OLE, remote images, zip-bombs and traversal. Absent validated entitlement, still render the **text-only** draft and record missing graphics externally; do not silently insert a blank FIG page.

## 8. Technical rendering feasibility and deterministic limits

**Proposed architecture, pending separately approved implementation dependencies:** validated P2-005 package + seven original inputs → typed filing IR → profile-specific offline PDF and editable DOCX renderers + isolated review view. All new renderers/templates are **additive/versioned**; preserve `PatentDocxRenderer`, `POST /api/exports/docx`, frontend/deployment and released P2-001…P2-005.

| Area | Implementation proposal and objective verification |
|---|---|
| PDF compositor | **ReportLab** PageTemplate/Frame-based US Letter cover, independent B2 two-column body, Claims and optional approved drawing sheets. Pin engine/version; dependency and architecture choice require explicit Human implementation approval. |
| Editable DOCX | **python-docx** plus controlled OOXML `w:cols`/section breaks; typed styles, genuine editable text and claim-number paragraphs. Use pinned headless LibreOffice to QA the output, NOT as a hidden PDF-authority substitute. |
| Fonts | Local licensed and embeddable serif with pinned fallback manifest; verify font embedding and searchable/selectable PDF text. Add offline Unicode/Vietnamese diacritic **rendering-robustness tests**, without treating the English-only P2-005 schema as translation authorization. Never disclose/distribute restricted font files. |
| Page geometry | US Letter **612×792 pt**. Proposal tokens for future calibration (not claimed measurements of reference): printable margins ≥0.6 in, body font 9–11 pt, two-column gutter 0.18–0.30 in. Record reference screenshots, measured areas/heading hierarchy and justified layout before freezing. |
| Pagination | Print-authoritative PDF needs bounded flowing columns/pages, repeatable page/column numbers, visible draft running header and marginal **5-line numbering without overlap**. No clipped titles, broken paragraphs, orphan Claims, split figures or colliding numerals. |
| Word compatibility | DOCX supports editable two-column text and distinct section/page breaks; **Microsoft Word and LibreOffice may repaginate differently**. Record drift; do NOT claim pixel-identical pagination or identical page counts across engines. Must still meet semantic fidelity and reasonable visual QA. |
| Application profile | Single-column 1.5/double-spacing, verified applicable 37 CFR margin rules, separate Claims and Abstract pages; not an assertion of filing-ready compliance. Required for completion despite secondary implementation order. |
| Security & temp files | Offline only; XML/OOXML escaping, macro/OLE/external-relationship rejection, no unsafe URL/active graphics, bounded memory/file sizes, private random per-render temp directory, traversal/symlink checks, cleanup even after failure and atomic release of approved artifacts. Never log raw research prose or retain source files in Git. |
| Determinism | Same input/profile/engine version yields deterministic **ordered semantic text and calibrated layout** in controlled environment. Container metadata/timestamps, font availability and Word layout may vary: no unconditional byte-identical PDF/DOCX claim; compare canonical normalized extracted text and fixed layout metrics. |
| Stop/escalate | If two-column/line-number layout or DOCX editability cannot meet ACs with this architecture, produce reproducible failing samples and alternative engine/tradeoff for **Human technical/dependency decision**, not reduced requirements or fake QA PASS. |

**PDF is the visually authoritative B2 preview; DOCX is editable and semantically authoritative.** Both must match the same validated source content. All four format/profile deliverables remain mandatory, independent of implementation order.

## 9. Reference calibration, fixtures and repeatable QA (future implementation)

Observed reference anchors: [US11367264B2](https://patentimages.storage.googleapis.com/91/f6/9b/18dc2af29220c8/US11367264.pdf) PDF p.1 cover, pp.2–19 drawings (18 sheets), p.20 first two-column body; [US11044591B2](https://patentimages.storage.googleapis.com/42/19/af/1c5089854ab9d4/US11044591.pdf) p.1 cover, p.2 additional references, pp.3–9 drawings (7 sheets), p.10 first two-column body. Both p.1/body pages were **inspected as references**, **NOT as successful P2-006 generated QA**. Future implementation must measure page boxes, cover column splits, margin/gutter, serif scale, heading/paragraph styles, line-number positions and drawing proportions with repeatable screenshot evidence; never invent a numerical similarity percentage.

**Offline synthetic test matrix:** authentic APP-002→P2-002→P2-003→P2-004→P2-005 input set with **no eligible Claims**; curated P2-004 positive Claims fixture as **component projection only, not source-provenance-valid public positive E2E**; package/wrong config/digest/source mutation, tampered Claims, absent upstream sidecar, bad figure rights, rejected external file/markup, missing abstract/admin/title, long/multi-page text, valid synthetic authorized figure layout, UTF-8/unicode/fonts, missing Claims marker, no output on validation error, no network/provider, and v1 regression.

**Future visual test evidence:** screenshot-render both generated PDFs at ≥200 dpi (prefer 300) for cover, drawing (if eligible), first/last text, column breaks, Claims and Abstract; side-by-side structural review against BOTH reference patents. Check page breaks, orphan prevention, PDF selectable/extractable text, font embedding, no clipping and non-issued banners. Extract normalized semantic output from all four files; compare content, numerical values, exact Claims numbering/dependencies and Abstract against the same verified input while excluding only tagged layout/draft status markers. Re-render DOCX via pinned LibreOffice; inspect Microsoft Word when available and report pagination drift. No generated output or QA PASS is claimed in this spec task.

## 10. AC-01…AC-20 — mandatory gates, not aspirational priority reductions

**P0 completion gate:** BOTH `B2_REFERENCE_PREVIEW` and `USPTO_APPLICATION_DRAFT`, EACH as **PDF + editable DOCX**, full source-validation/privacy/status/visual QA and old-v1 nonregression. Sequence: B2 first, application second; partial delivery remains IN PROGRESS. **P1** is optional further typographic polish, not waiver of required two columns, margins, line numbering or editability. **P2** future archive/accessibility enhancements require separate Human decision.

| AC | Required future implementation proof / fixed-SHA spec-review challenge |
|---|---|
| AC-01 | Correct Human-supplied spec authorization and workflow V1; separate Human approval/freeze & implementation authorization; no P2-006 implementation now |
| AC-02 | Both reference PDFs visually measured with recorded page IDs/layout metrics; no copied technical data, unauthorized font claims or fake similarity score |
| AC-03 | Separate named modes; BOTH are mandatory final gates with PDF and editable DOCX |
| AC-04 | Exactly 13 canonical `section_order` keys; 11 `sections` plus separate Claims and Abstract, including statuses/conditional sequence listing |
| AC-05 | B2 black/white US Letter cover with verifiable (54) Title and (57) Abstract source; clean reflow |
| AC-06 | No invented/copied official B2 patent metadata/numbers/barcodes/legal statuses, patent wording or source figures |
| AC-07 | B2 two-column serif body, centered headings, controlled margins/numbering and no collisions; 5-line marginal numbering; meaningful visual verification |
| AC-08 | Fail-closed drawing rights/assets/FIG mapping, zero drawing sheets without entitlement, synthetic-only authorized positive layout fixture |
| AC-09 | Positive Claims exactly validated text/numbers/dependencies; missing Claims has visible **non-numbered** status-only marker and NO preamble/filler |
| AC-10 | Abstract text from one verified source, <=150 words, cover/body parity and no mutation of technical content |
| AC-11 | Missing administrative/Claims/figures/sections never guessed; NOT_APPLICABLE only with validated basis |
| AC-12 | Filing/technical prose strictly separate from P2-005 review_package/metadata/raw evidence and no false filing readiness |
| AC-13 | Searchable/embedded-font PDFs and genuinely editable DOCX; text/order parity across all four outputs, Word/LibreOffice drift explicitly noted |
| AC-14 | Application mode mandatory P0: single column, verified margins/spacing, Claims/Abstract new sheets, UNREVIEWED and non-filing guarantee |
| AC-15 | Seven original upstream inputs and exact released `validate_uspto_document_package` before any output; mutate/reject package-only attestations/invalid inputs |
| AC-16 | Offline negative/positive-component/missing-Claims/figure and multi-page tests with screenshot/preflight and no fake public positive Claims E2E |
| AC-17 | Independent fixed-SHA specification review then separately authorized implementation, independent output QA and real CI/test evidence |
| AC-18 | Released P2-001 through P2-005 and v1 DOCX/export/frontend/deployment unchanged, regression-proved |
| AC-19 | No paid/provider, real/confidential input, production, new public endpoint, unapproved external dependency or P2-007 work |
| AC-20 | Unmistakable PATENT SPECIFICATION DRAFT — NOT ISSUED marker on cover and every page, Human/IP review required, no legal/filing acceptance claim |

The proposed engines and third-party dependencies are architecture **recommendations, not approvals**. Failure to meet two-column layout/line numbering or editable DOCX is a blocking technical issue to be escalated with concrete alternatives. No AC is implicitly waived.

## 11. Specification review handoff and unresolved decisions

1. **P2-005 CLOSED / COMPLETED — MERGED:** PR #96 spec, #98 implementation, #99 governance and #100 terminal, with verified main SHA `1d1ad1ad3721d641346c3df359661fa5524602a4`. Released `USPTO_DOCUMENT_PACKAGE v1.0.0` remains synthetic-only, with `review_boundary.filing_ready=false` and original P2-003 `claims_runtime_implemented=false`.
2. **P2-006 now:** Human-provided `HUMAN-P2-006-SPEC-RECONCILIATION-2026-10-09` authorizes specification reconciliation, safe branch synchronization, static checks and GitHub PR #97 review handoff **only**. Request **Gemini 3.1 Pro High / Antigravity STRICT READ-ONLY independent fixed-SHA specification review** with scope, AC-01…20, actual package validator, Claims/figures, two profiles, QA feasibility and findings; old review SHA is invalid after updates.
3. **After separate Human approval/freeze:** choose renderer engines and dependency/asset authorization, give separate P2-006 implementation authorization, perform offline fixture/render/test/visual QA, independent implementation review and guarded later merge. No automatic implementation or PR #97 merge today.
4. **Open Human decisions (not approved):** choose final renderer dependency/architecture based on feasibility; separately authorize any figure asset manifest/pipeline, distributed review output, public API, requirement reduction or completion-by-stage. Authentic positive APP-002→P2-002→P2-004 Claims full-chain remains unsupported and requires separately authorized remediation. Provider budget/BLK-003/real-data/production and P2-007 are out of scope.

## 12. Stop conditions

- No bypass of P2-005 exact package+seven-input provenance validation; no unsigned receipt/mismatched config trust; no modification to P2-001…P2-005, `PatentDocxRenderer` or v1 export; no illegal/unsupported figure or claim creation.
- No accepting primary-only delivery as full completion or silent removal of application-style layout/positive/missing Claims QA. Report substantial architecture/legal/security/data/rights gaps as **separate Human decision**, not unapproved code.
- Stop at **P2-006 — UPDATED SPECIFICATION / READY FOR INDEPENDENT FIXED-SHA REVIEW**. The specification is not yet approved/frozen; no renderer, paid provider, confidential-paper processing, production, PR merge or P2-007 authorization.
