# P2-006 reference measurement and reproducible QA evidence

| Field | Value |
|---|---|
| Version / date | 1.0.0 / 2026-10-10 GMT+7 |
| Authority | HUMAN-P2-006-IMPLEMENTATION-2026-10-10; Human remediation instruction, attachment 884240cb-cbb0-47e2-a3d7-64a92b9717cd/Pasted text.txt |
| Workflow / frozen specification | V1 / v0.2.0 at 5ac9b7bcd31e8ade7f4b0861b6e7a9c14e531953; unchanged |
| Reconciliation finding | [PR #101 mandatory AC-02 / LibreOffice gates](https://github.com/nshaokiet/ai-ip-description-generator/pull/101#issuecomment-6095563219) |
| Status | Implementation self-check; new exact-SHA CI and independent re-review required; no merge in this execution |
| Change history | New -> 1.0.0: Codex records actual measurements and QA installation pins; no contract/rendering change; Breaking change: No |

Both public PDFs were fetched from the exact Human-supplied URLs and visually inspected at the required cover/body pages. The images and source PDFs remain temporary QA inputs, never application inputs or committed assets. Generated drafts contain none of their prose, claims, identifiers or drawings. Comparison montages are explicitly labeled public reference QA, separate from the four generated draft files.

| Public source | Original URL | SHA-256 of downloaded bytes | Measured PDF pages |
|---|---|---|---|
| US11367264B2 | https://patentimages.storage.googleapis.com/91/f6/9b/18dc2af29220c8/US11367264.pdf | 6f30294a48e11e22f28e8fbfd5eb3c6f3dbe28c391bac54f1f763e565d0170bf | 1 cover; 20 first two-column body; 2 drawing observation only (33 pages total) |
| US11044591B2 | https://patentimages.storage.googleapis.com/42/19/af/1c5089854ab9d4/US11044591.pdf | 712a1eca1b98d49bd2ef7482412f496fc1e612044484b5c0b2f1a3e3bb7642c7 | 1 cover; 10 first two-column body; 3 drawing observation only (19 pages total) |

## Method and reproducibility

`tests/backend/measure_p2_006_references.py` verifies each source hash/page count/MediaBox/rotation/image transform before measuring. The sole visible image is 2560 x 3300 pixels, placed with PDF matrix `[614.4 0 0 792 -1.2 0]`. Coordinates below are **points, top-left origin**: `x = pixel_x * 0.24 - 1.2`; `y = pixel_y * 0.24`; 72 pt = 1 inch. Standard bottom-left PDF y is `792 - top_y`. The scan extends 1.2 pt beyond each horizontal page edge; treating 2560 pixels as exactly 612 pt would miscalibrate it.

Fixed region windows, luminance threshold `<128`, and visible-ink bounding boxes are serialized in [measurement JSON](P2-006-reference-measurements.json). Row runs shorter than three scan pixels are excluded from rhythm measurements. Bounds are exclusive at right/bottom. Reported precision is 0.01 pt for audit reproducibility, **not metrological accuracy**; practical endpoint uncertainty is approximately +/-0.48 pt due to sampling/scan quality. Ink extents describe the selected occupied region, not a hidden nominal typesetting frame. Paragraph/number rhythm uses row-center spacing; glyph case/descenders mean this is not an exact font-baseline measurement.

The PDFs contain an invisible `/Courier` OCR layer (`Tr=3`). Its font names/sizes cannot identify the visible serif typography. Visible font family and nominal point size are **NOT MEASURABLE** from these files; no OCR font is presented as the patent's design font. Actual visible glyph-height and row-spacing observations are reported instead. No numerical resemblance/similarity score or pixel identity is claimed.

Reproduce with the existing pinned Python/pypdf/Pillow dependencies; no new runtime dependency:

```text
python tests/backend/measure_p2_006_references.py SOURCE_DIR --verify docs/tasks/P2-006-reference-measurements.json
```

`SOURCE_DIR` must contain the two exact downloaded filenames `US11367264.pdf` and `US11044591.pdf`. Any hash/transform/result mismatch fails closed. CI adds `--compare SYNTHETIC_QA_DIR` after successful pinned LibreOffice QA, rasterizes reference pages with pinned Poppler at 300 dpi, and generates clearly separated side-by-side cover/body montages against **both native-PDF and converted editable-DOCX outputs, for both profiles**. `synthetic-structure.json` records occupied synthetic column bounds in calibrated screenshots. These temporary source screenshots/JSON/montages are archived as `p2-006-public-reference-calibration`; no original patent PDF is archived or committed.

## Measured reference table

Each `(x0,y0,x1,y1)` box uses top-left points. Complete windows, individual row runs and page matrices are in the JSON above. Cover regions exclude the lower representative figure and the official masthead/barcode. Text-field proportions are observed region widths, not artwork similarity percentages.

| Metric | US11367264B2 | US11044591B2 |
|---|---|---|
| MediaBox at cover/body/drawing sample | (0,0,612,792), 8.5 x 11 in | Same |
| Cover left-field ink box; width | (77.76,120.24,292.80,486.72); 215.04 pt | (77.76,120.96,293.04,515.76); 215.28 pt |
| Cover right-field ink box; width | (310.56,120.24,527.28,486.48); 216.72 pt | (310.56,120.24,526.32,516.00); 215.76 pt |
| Cover width split (left:right) / gutter | 215.04:216.72; 17.76 pt (0.247 in) | 215.28:215.76; 17.52 pt (0.243 in) |
| Cover horizontal rule | x=77.28..526.32, y=105.12..105.60; 449.04 pt wide | Same |
| Cover (54) title occupied box / line count | (101.52,120.48,276.24,156.48); 4 lines | (101.28,121.20,252.48,148.08); 3 lines |
| Cover title uppercase ink height / row pitch | 6.00 pt / 9.84..10.08 pt | 6.00 pt / 10.32..10.56 pt |
| Cover (57) Abstract observed prose box | (310.80,319.68,527.28,467.52); 15 rows in selected band | (310.80,359.04,526.32,495.12); 14 rows in selected band |
| First body left column ink box / width | (77.28,84.72,293.04,751.20); 215.76 pt (2.997 in) | (77.28,84.72,293.04,749.28); 215.76 pt |
| First body right column ink box / width | (310.80,84.48,527.28,751.20); 216.48 pt (3.007 in) | (310.80,84.48,526.56,751.20); 215.76 pt |
| Body outer margins L/R/T/B (ink, excluding running header) | 77.28 / 84.72 / 84.48 / 40.80 pt = 1.073 / 1.177 / 1.173 / 0.567 in | 77.28 / 85.44 / 84.48 / 40.80 pt = 1.073 / 1.187 / 1.173 / 0.567 in |
| Body ink-to-ink gutter | 17.76 pt (0.247 in) | Same |
| Marginal number ink x / height / median five-line spacing | x=298.32..305.04; 4.56 pt; 49.92 pt (0.693 in) | Same |
| Body title uppercase ink height / occupied rows | 6.00 pt / 4 | 6.00 pt / 3 |
| Sample main heading uppercase ink height / placement | 6.00 pt; centered in left column, sampled y=354.00..360.00 | 6.00 pt; centered in left column, sampled y=126.48..132.48 |
| Sample prose ink heights / median row-center pitch | 6.00..8.16 pt / 10.32 pt | 5.28..8.16 pt / 10.32 pt |
| Visible font family / nominal point size | **NOT MEASURABLE**: scanned appearance; hidden OCR is not visible typography | Same |
| Drawing sample ink box and W:H, observation only | p.2: (210.00,216.72,390.96,614.16); 180.96 x 397.44 pt; 0.4553 | p.3: (85.20,126.00,516.24,704.88); 431.04 x 578.88 pt; 0.7446 |

Structural observations checked against screenshots: bilateral aligned fields under a shared black rule; title in the left cover region, Abstract in the right; serif uppercase headings centered over justified two-column body, marginal five-line numbering in the gutter. The issued masthead/identifier/header is reference-only. Drawing ratios describe one occupied drawing sample including its caption, not all sheets or a newly authorized image pipeline.

## Comparison with unchanged synthetic rendering

| Element | Both measured references | P2-006 native B2 PDF / editable B2 DOCX | Application PDF / DOCX |
|---|---|---|---|
| Page / identity | Letter; issued identifiers present in sources | Letter; explicit draft banner, neutral ID; issued fields omitted | Letter; draft banner; no B2 front page |
| Cover fields | Approximately equal 215..217 pt occupied widths; many genuine bibliographic fields; lower source figure | Two 255 pt table cells with 9 pt left/right padding in native PDF; only verified (54) title and (57) Abstract; empty lower area because no entitled figure/admin data | Title starts the single-column disclosure; cover comparison intentionally differs |
| Body frames / width | Occupied widths ~216 pt; x=77..293 and 311..527 | Native frames x=50..305 and 322..565, content x=54..300 and 326..560 (246/234 pt usable widths). Editable DOCX uses 0.66 in side margins, equal ~237.48 pt columns | Native frame x=72..558 (486 pt); DOCX L/R=1.00/0.75 in; single column |
| Gutter | 17.76 pt occupied gap | Native frame gap 17 pt; padded content gap 26 pt. DOCX **840 twips = 42 pt**, retained to prevent line-number collision | No intercolumn gutter |
| Body scale / hierarchy | Visible uppercase ink ~6 pt; prose row pitch ~10.32 pt; font point size unknown | Licensed Crimson Text: PDF 9.4 pt body / 11.6 pt leading, main 11 pt and secondary 9.6 pt. DOCX 9.4 pt / 1.12 line spacing. Larger/bolder hierarchy and missing-status blocks differ visibly | 12 pt body / 18 pt native leading; 1.5 DOCX line spacing |
| Line numbers | Gutter x=298.32..305.04, ~49.92 pt five-line rhythm | Native right-aligned at x=47/318, 6.5 pt, 58 pt five-line rhythm; DOCX actual OOXML countBy=5. Separate placement keeps body text clear | No marginal line numbering |
| Drawings | Real source sheets and cover figure; measured only as reference observations | Zero source drawings or representative figure; synthetic geometry QA separate from draft files | Same entitlement boundary |
| Claims / Abstract | Published invention content; not copied or used as renderer input | Authentic synthetic chain has incomplete Claims marker, no invented preamble; one verified Abstract reused on cover/body | Same semantic substance; Claims and Abstract on new pages |

These are honest deviations preserved under the instruction to retain current rendering behavior. Measurements close the missing-reference-evidence gate, not every possible typographic difference. No assertion of identical fonts, page counts, granted-patent status or filing compliance. CI's `synthetic-structure.json` gives actual occupied output boxes alongside the nominal frame settings; native versus LibreOffice pagination is recorded separately in `synthetic-qa-evidence.json`. Microsoft Word is unavailable here; Word pagination remains **NOT VERIFIED**.

## Pinned QA environment

Source-controlled definition: `tests/backend/p2_006_qa_environment.json` v1.0.0. Installation: `tests/backend/install_p2_006_qa.sh`. Runtime/package verifier: `tests/backend/verify_p2_006_qa_environment.py`, also called by the conversion script before rendering.

- Ubuntu 24.04 / amd64; signed archive snapshot **20261009T000000Z**. Isolated sources and index directory exclude live runner repositories/PPAs; only noble, noble-updates and noble-security main/universe at that fixed snapshot resolve newly installed dependencies.
- LibreOffice writer/core/common/base-core: exact Debian revision **4:24.2.7-0ubuntu0.24.04.7**; expected runtime **24.2.7.2**. `dpkg-query` verifies complete revisions, while `soffice --version` verifies the runtime and records the full build string. A different Ubuntu patch revision with the same upstream version fails the package check.
- Poppler utilities and libpoppler134: exact revision **24.02.0-1ubuntu9.10**, expected `pdftoppm` **24.02.0**. Poppler also affects glyph rasterization/measurement evidence, so it is locked alongside LibreOffice.
- Availability and SHA-256 were independently read from snapshot noble-updates amd64 indexes before selection: writer `5d46bde2995b99fe06202b8e8cdad625fba37ddf9e8cfbdae009c82346a730b8`, core `5b7dd970e81f3690aceb07587cf17ba746fc5cd86a4c0b1ea5499fcc4b59859a`, common `374910adaeabb3415aa6c020388796f2761043c4cc0f53c0ace8bb3381a1da18`, base-core `a3174b36ea75f0b99d4d7207fcee0e60bf37a8920169f17dad1b01c6276a874b`, poppler-utils `19ce4557ad89350506a0f1c33ad4c5a6aa7469e48c78aacae351a59b43ee20c6`, libpoppler134 `2974536ea4ce7d75e54923b1bab0f251f407d1c291427ddc7c53da65e1c505b7`. APT verifies signed archive metadata and package hashes; TLS alone is not treated as package authentication.
- Historical metadata expiry is disabled only for isolated snapshot indexes (`Acquire::Check-Valid-Until=false`); signature and checksum verification remain enabled. Exact install/unavailable archive/version mismatch errors terminate CI; no dynamic revision selection, live-apt fallback or QA skip.
- Fonts are the existing Git-tracked Crimson Text/OFL assets copied into the QA user's font directory. Production Python pins remain unchanged. LibreOffice is MPL-2.0 with component notices; Poppler is GPL-2.0-or-later with component notices; existing Crimson Text is SIL OFL-1.1. Package-specific copyright files remain installed under `/usr/share/doc/*/copyright`. No new runtime service or redistribution of QA binaries in this repository.
- This locks the two rendering tools and snapshot package resolution, **not the entire evolving GitHub-hosted runner image** or every preinstalled support library. OS baseline, actual installed-package versions, font assets and full tool output are part of the QA evidence; byte-identical PDF/DOCX output is not promised. Local Windows has no installed Linux LibreOffice/Poppler runtime; actual pinned conversion is verified by the exact-head Ubuntu CI, not a fabricated local result.

Primary provenance: [Canonical snapshot procedure](https://snapshot.ubuntu.com/), [Ubuntu LibreOffice package](https://packages.ubuntu.com/noble-updates/libreoffice-writer), [Ubuntu Poppler package](https://packages.ubuntu.com/noble-updates/poppler-utils), [LibreOffice licenses](https://www.libreoffice.org/about-us/licenses/), [Poppler project](https://poppler.freedesktop.org/). Snapshot URLs, not the moving package catalog, are the installation source of truth.

Update procedure: change snapshot and exact revisions together in a scoped PR after verifying signed indexes/package availability and license/security notices; update runtime expectations; rerun all four outputs, semantic/Claims/Abstract checks, all-page 300-dpi captures, reference hash/metric verification and full regression. Inspect rendering drift, obtain fresh fixed-SHA independent review and required CI. Do not auto-select a new package or waive a failed pin. If Canonical stops retaining this snapshot, CI remains blocked until a separately validated source-controlled update (Canonical's documented retention is at least two years, not perpetual).
