# P2-001 — USPTO Reference Corpus v0.1.0

## Purpose

This reference corpus captures structural observations used to define the future USPTO-style specification target. It is not a legal template library, training dataset, prior-art opinion or patentability analysis.

Machine-readable structural maps:

- `docs/references/US11367264B2-section-map.json`
- `docs/references/US11044591B2-section-map.json`

The maps contain headings, presence/absence observations, figure-label summaries, claim-family/count metadata, and limitations only. They contain no copied substantive patent passage.

## Normative sources

### USPTO Nonprovisional Utility Patent Application Filing Guide

URL: https://www.uspto.gov/patents/basics/apply/utility-patent

Key target constraints used by P2-001:

- the specification provides the written description and concludes with Claims;
- Claims begin on a new page;
- a nonprovisional utility application contains at least one claim;
- Abstract begins on a separate page;
- Abstract should not exceed 150 words;
- Human/legal review remains necessary because patent applications are complex legal documents.

### MPEP § 608 / 37 CFR 1.77(b) preferred arrangement

URL: https://www.uspto.gov/web/offices/pac/mpep/s608.html

Preferred specification sections used by P2-001:

- TITLE OF THE INVENTION;
- CROSS-REFERENCE TO RELATED APPLICATIONS;
- STATEMENT REGARDING FEDERALLY SPONSORED RESEARCH OR DEVELOPMENT;
- NAMES OF PARTIES TO A JOINT RESEARCH AGREEMENT;
- INCORPORATION BY REFERENCE;
- STATEMENT REGARDING PRIOR DISCLOSURES;
- BACKGROUND OF THE INVENTION;
- BRIEF SUMMARY OF THE INVENTION;
- BRIEF DESCRIPTION OF THE DRAWINGS;
- DETAILED DESCRIPTION OF THE INVENTION;
- CLAIM OR CLAIMS;
- ABSTRACT OF THE DISCLOSURE;
- SEQUENCE LISTING when applicable.

This is a preferred arrangement; applicability depends on the invention/application.

---

## Reference A — US11367264B2

URL: https://patentimages.storage.googleapis.com/91/f6/9b/18dc2af29220c8/US11367264.pdf

Title: *Semantic Interior Mapology: A Tool Box for Indoor Scene Description from Architectural Floor Plans*

### Structural observations

| Feature | Observation | P2 implication |
| --- | --- | --- |
| Related application | Present | Cannot be inferred from paper; Human metadata required |
| Federally sponsored research | Present | Funding statements need explicit evidence |
| Background | Split into Field of the Invention and Description of Related Art | v2 Background should support both |
| Summary | Describes toolbox and implementation concepts | Requires invention reconstruction, not section renaming |
| Drawings | Many figure sheets and figure-linked description | Future drawing/reference-numeral pipeline required |
| Detailed description | Expands systems, processes and examples | P2-002/P2-003 must support embodiments and relationships |
| Claims | Numbered system claims and dependent limitations | P2-004 must model dependency/support |
| Issued-patent front matter | Patent number/date/classification/examiner information appears in grant | Must NOT be generated from paper |

### What this reference does not prove

- that the source research paper alone contains all administrative statements;
- that a generated claim set is legally sufficient;
- that a structurally similar output is patentable or filing-ready.

---

## Reference B — US11044591B2

URL: https://patentimages.storage.googleapis.com/42/19/af/1c5089854ab9d4/US11044591.pdf

Title: *Cloud Based Phone Services Accessible in the Cloud by a Remote Device*

### Structural observations

| Feature | Observation | P2 implication |
| --- | --- | --- |
| Background | Concise technical context/problem framing | Background should be selective, not a paper Introduction dump |
| Brief Summary | Expressed through multiple embodiments | Invention Reconstruction should derive supported embodiments |
| Drawings | Figures describe network/system/process structure | v2 must support drawing plan and detailed-description mapping |
| Detailed description | Expands architecture, virtual machines, remote devices and implementations | Paper methods need system/method/software reconstruction |
| Claims | Includes a computer-implemented method and additional computer-implemented forms | Claims strategy may use different families when technically supported |
| Variants | Multiple dependent embodiments narrow earlier concepts | Later Claims runtime needs structured dependencies |

### What this reference does not prove

- that every software invention needs method/system/CRM claims;
- that all embodiments may be invented beyond source support;
- that the wording should be copied.

---

## Reference comparison

| Dimension | US11367264B2 | US11044591B2 | Canonical P2-001 rule |
| --- | --- | --- | --- |
| Administrative sections | Explicit related-application and federal-funding statements | Not all such sections visibly emphasized | Model them, never fabricate them |
| Background | Field + related art | Compact Background | Support flexible content under canonical v2 headings |
| Summary | Toolbox/system concepts | Multiple enumerated embodiments | Reconstruct invention before drafting Summary |
| Drawings | Extensive | Multiple system/process figures | Plan figure mapping/reference numerals |
| Detailed description | System/process/examples | Architecture/method/software | Support multiple implementation perspectives |
| Claims | System/dependent claims | Method and other computer-implemented forms | Generate only technically supported claim families |
| Abstract | Issued-patent front matter contains abstract | Issued-patent front matter contains abstract | Future filing-style draft places Abstract per USPTO preferred specification order |

## Corpus policy

- Public patent references may be cited by identifier and structural observation.
- Do not copy long patent passages into prompts/fixtures.
- Do not treat patent wording as a gold answer for a different invention.
- Real scientific papers are not added to this task.
- Future paired paper↔patent benchmark data require separate source/licensing/privacy review.

## Handoff

This corpus is sufficient for P2-001 target-definition review. It is intentionally small. P2-008 will define a broader benchmark corpus and evaluation methodology.
