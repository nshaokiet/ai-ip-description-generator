# P2-006 offline renderer implementation notes

Current remediation evidence (2026-10-10): [measured source table, deviations and pinned QA provenance](P2-006-reference-qa.md), [reproducible geometry JSON](P2-006-reference-measurements.json). Earlier preparatory CI/review wording below remains historical; the new implementation/QA commit requires fresh exact-head CI and Gemini 3.1 Pro High / Antigravity STRICT READ-ONLY independent re-review. No merge during this remediation.

- Scope: additive internal Python service only. No public API or v1 export change.
- Authority: Human-provided `HUMAN-P2-006-IMPLEMENTATION-2026-10-10`; frozen spec v0.2.0 at `5ac9b7bcd31e8ade7f4b0861b6e7a9c14e531953`. Workflow V1. This is not GitHub-native or cryptographic approval.
- Input trust: released public `validate_uspto_document_package` takes P2-005 package and **all seven** original inputs, called before any staging/output. Output directory is an existing absolute local path; each successful run atomically renames one freshly rendered four-file directory. Unsafe symlink roots and output collisions fail closed.
- Exact required deliverables: `B2_REFERENCE_PREVIEW.pdf`, `B2_REFERENCE_PREVIEW.docx`, `USPTO_APPLICATION_DRAFT.pdf`, `USPTO_APPLICATION_DRAFT.docx`. Filing view is the only textual source. Review metadata and evidence stay out of the pages.
- Font: Crimson Text Regular/Bold from `google/fonts/ofl/crimsontext`, SIL Open Font License 1.1 (bundled `assets/fonts/OFL.txt`). Source: `https://github.com/google/fonts/tree/main/ofl/crimsontext`. Font embedding/redistribution permitted under OFL; use without implying any USPTO affiliation. DOCX asks for Crimson Text; viewer substitutions can affect pagination.
- Dependencies: ReportLab **4.4.4** (open-source BSD license; `https://docs.reportlab.com/developerfaqs/`); Pillow **12.3.0** (HPND license, transitive ReportLab); charset-normalizer **3.5.2** (MIT license, transitive ReportLab). Pins in `backend/requirements.txt`. Existing python-docx **1.2.0** (MIT) unchanged. Check deployed platform/wheel availability independently before any production proposal.
- Figures: P2-005 supplies metadata without rights-cleared image bytes or attestation, so this implementation emits **zero drawing sheets**. It neither ingests images nor grants an asset pipeline. Synthetic figure layout QA remains a separate branch of testing until a defined rights contract exists.
- Claims: authentic seven-input APP-002 synthetic chain yields `HUMAN_CONFIRMATION_REQUIRED`. The P2-004 positive standalone component projection is deliberately rejected by this renderer and must not be represented as proven full-chain supported Claims.
- Accessibility/fidelity boundaries: selectable PDF text and editable DOCX, not exact byte identity. The PDF is visually authoritative for B2; Word may repaginate. Application is explicitly UNREVIEWED and requires specialist filing review. No release/filing assertion.
- Optional local visual inspection utility: `tests/backend/inspect_p2_006_pages.py` using `pypdfium2==4.30.0` (BSD/Apache PDFium; QA only). Neither this QA utility nor any generated PNG is a renderer runtime dependency.
- Required final governance: fixed-SHA independent review by Gemini 3.1 Pro High / Antigravity in STRICT READ-ONLY mode, exact-head CI, and separate later merge eligibility. This note does not claim any independent implementation PASS.


## AC-01–AC-20 evidence ledger — implementation review candidate

Status here is an implementation self-check. **Independent fixed-SHA Antigravity review is not yet performed.** Results are bound to the commit and CI referenced in the PR handoff; until those are known this ledger is preparatory.

| AC | Implementation evidence and residual gate |
|---|---|
| 01 | Human-provided spec, architecture and implementation approvals recorded; Workflow V1 with no enrollment; final reviewed SHA pending. |
| 02 | Both exact source PDFs now hash-verified and measured: cover/body pp.1/20 and pp.1/10; actual PDF image matrices, visible-ink bounds, margins/columns/gutter/line rhythm, title/heading scale and drawing observations in `P2-006-reference-measurements.json` and `P2-006-reference-qa.md`. Hidden OCR fonts explicitly NOT MEASURABLE as visible font identity. CI reproduces the table and separate side-by-side source/synthetic comparisons; fresh exact-SHA result/re-review required. |
| 03 | `FILES` has exactly two profiles × PDF/editable DOCX. `test_four_mandatory_formats_order_status_and_filing_boundary` checks four atomic outputs. |
| 04 | `_build_model` traverses validated `section_order`: exactly 13 IDs (11 ordinary sections plus separate Claims/Abstract), including status markers and sequence-listing disposition. Source order assertions in tests. |
| 05 | B2 US Letter PDF uses (54) title/(57) abstract on black/white cover; same source fields in editable DOCX table. Local rasterized PDF cover inspected. |
| 06 | No issued patent grant number, barcode, actual inventor/assignee claim, official B2 identity or patent figure. Every page has an explicit draft banner. |
| 07 | ReportLab B2 flow has two serif columns and five-line marginal number marks; DOCX uses actual OOXML `w:cols` and `w:lnNumType`. Local p02 inspected; LibreOffice rendering and pagination drift check in CI. |
| 08 | No user figure bytes or drawing sheets. Separately generated synthetic geometric `SYNTHETIC_DRAWING_LAYOUT_QA.pdf/png` demonstrates rights-cleared layout-only artwork; rights/FIG association must be separately authorized. |
| 09 | Missing authentic Claims visibly retain non-numbered `CLAIMS_INCOMPLETE`, without preamble or invented claims. Standalone positive Claims fixture is rejected at seven-input trust boundary; positive full-chain Claims E2E remains **UNVERIFIED / upstream gap**. |
| 10 | Single validated abstract string used for (57) and body; regression asserts source equality and <=150 words on synthetic fixture. |
| 11 | Non-PRESENT sections retain explicit validated missing/not-applicable markers, without inferred administrative or technical facts. |
| 12 | Renderer reads copied `filing_view` only; tests exclude `review_package`, source IDs and evidence metadata from all four outputs. Draft/filing boundary disclosed. |
| 13 | Tests verify Unicode, escaped angle/ampersand text, PDFs with embedded fonts and selectable text, editable OOXML DOCX and stable core semantics; exact Word vs LibreOffice pagination not guaranteed. CI LibreOffice independent-engine smoke check pending. |
| 14 | Single-column US Letter application flow with 12 pt/1.5 leading; separate Claims and Abstract pages. PDF and DOCX section/page breaks tested. Application is **UNREVIEWED** and not filing-ready. |
| 15 | Released public `validate_uspto_document_package` called with all seven upstream originals before output/staging. Mutation/absent sidecar/collision/positive-component rejection tests. |
| 16 | Targeted synthetic layout tests cover missing Claims, component-only positive case, mutations, multiple pages, Unicode/XML escaping, DOCX structure, external links and macro absence. Synthetic snapshots are visual aid; CI LibreOffice QA pending. |
| 17 | Implementation self-check and local PDF preview only; independent exact-SHA Gemini 3.1 Pro High / Antigravity STRICT READ-ONLY review is **PENDING**. |
| 18 | Renderer adds no route, modifies no P2-001–P2-005 contract and leaves existing v1 export untouched. Full backend regression locally 898 passed/3 skipped before final test addition; exact-head CI frontend/browser still pending. |
| 19 | All rendering is offline against public synthetic fixtures. No provider/API, real/confidential paper, production endpoint, P2-007 or unapproved actual drawings. Licenses and exact pins documented above. |
| 20 | `PATENT SPECIFICATION DRAFT — NOT ISSUED` placed on each PDF page and DOCX running header. Visible `UNREVIEWED` filing profile label is in report/documentation; output is subject to Human/IP specialist review, with no filing approval implied. |

## QA observations / known restrictions

- Visual inspection of native PDF: B2 cover and populated two-column body, Claims/status continuation, plus application first/Claims/Abstract pages were sampled. All inspected samples readable and without observed overlaps/clipping. This is not a blanket visual guarantee; run the CI-provided LibreOffice/Poppler QA and inspect archived PNGs for layout artifacts.
- Chromium/Word/LibreOffice engines may substitute fonts or repaginate editable DOCX. B2 **reference preview** is a synthetic approximation, not issued USPTO formatting certification. Application output is **UNREVIEWED**.
- Authentic APP-002 → P2-002 synthetic pipeline cannot produce eligible supported Claims end-to-end. `P2-003 claims_runtime_implemented=false` remains unchanged; standalone P2-004 positive Claims test supports component projection only.
- Outputs contain no genuine figures because P2-005 does not expose an authorized image-byte/right-attestation input. Real figure processing requires separate Human decision.
- P2-005 bundle validator remains the only public trust boundary; no new endpoint, external service, provider cost or real-paper permission.

- Independent offline DOCX pagination inspection caught B2 column-two line numbers overlapping column-one text with a 320-twip gutter. Increased OOXML two-column space to **840 twips**; manually re-rendered all three B2 pages and verified the gutter is clear, with application mode five-page visual check unchanged. Regression asserts the safe gutter. This remediation requires a new implementation SHA/CI and fixed-SHA review.

## Mandatory-gate remediation addendum (2026-10-10)

- Version: addendum 1.0.0; original unversioned implementation notes preserved, no released contract or renderer change; Breaking change: No.
- Accepted findings: AC-02 lacked measured source evidence; unpinned apt installation did not satisfy the frozen specification's pinned LibreOffice requirement. No exception/waiver claimed.
- AC-16 / spec Sections 8–9: CI now installs **LibreOffice 4:24.2.7-0ubuntu0.24.04.7 (runtime 24.2.7.2)** and **Poppler 24.02.0-1ubuntu9.10 (runtime 24.02.0)** from isolated signed Ubuntu snapshot `20261009T000000Z`. Exact revision/runtime mismatch blocks conversion. Snapshot index provenance, license notes, assumptions and update process are documented in the linked reference QA record.
- AC-07/13/14: unchanged renderer and 840-twip DOCX gutter. QA captures every native/converted page at 300 dpi, verifies all filing-model text fragments across native/converted outputs, records page counts and hashes, checks missing Claims/absence of preamble and application Claims/Abstract sheet ordering. Four actual draft files remain synthetic-only; source patents are used solely by separate reference measurement QA.
- Local remediation verification: 12 renderer tests PASS; full pre-addition Windows backend 899 PASS / 3 SKIP / one existing Starlette deprecation warning; 4 new pin success/mismatch tests PASS; pip check clean; frozen specification and released contracts/renderer unchanged. Actual pinned Ubuntu conversion, full frontend/browser regression and source-versus-output QA are required in the new exact-head CI, with final results/artifact IDs in the external fixed-SHA handoff.
- Old external review on `2a8c7d664606ed586715a4373a41d636a6335c89` remains historical. New QA/evidence/CI code is not independently reviewed by that PASS. Current MCP read returns `Unknown task: P2-006`; operational state/lease remains BLOCKED BY TOOL CAPABILITY, never fabricated.
- Completion boundary for this execution: after new exact-head CI SUCCESS and artifact verification, **REMEDIATION COMPLETE / READY FOR INDEPENDENT FIXED-SHA RE-REVIEW**; not task Completed, PR merged, production-ready or filing-ready. New independent review remains pending.
