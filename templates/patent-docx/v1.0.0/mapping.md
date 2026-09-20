# Patent DOCX Template v1.0.0 Mapping

Input contract: `schemas/patent-draft/v1.0.0/patent-draft.schema.json`

Renderer: `tests/docx/render_patent_docx_v1.py`

## Canonical order

| Order | DOCX section | Contract source |
|---:|---|---|
| 1 | Cover and Draft Notice | `output_notice`, `document_metadata` |
| 2 | Title | `selected_title` |
| 3 | Abstract | `abstract` |
| 4 | Technical Field | `draft_sections[section_id=TECHNICAL_FIELD]` |
| 5 | Background | `draft_sections[section_id=BACKGROUND]` |
| 6 | Summary of Technical Disclosure | `draft_sections[section_id=SUMMARY_OF_TECHNICAL_DISCLOSURE]` |
| 6.1 | Technical Problems | `subsections[subsection_id=TECHNICAL_PROBLEMS]` |
| 6.2 | Technical Solutions | `subsections[subsection_id=TECHNICAL_SOLUTIONS]` |
| 6.3 | Potential Distinguishing Features | `subsections[subsection_id=POTENTIAL_DISTINGUISHING_FEATURES]` |
| 6.4 | Technical Effects | `subsections[subsection_id=TECHNICAL_EFFECTS]` |
| 7 | Brief Description of Drawings | `draft_sections[section_id=BRIEF_DESCRIPTION_OF_DRAWINGS]`, `drawings` |
| 8 | Detailed Description | `draft_sections[section_id=DETAILED_DESCRIPTION]` |
| 8.1 | Components or System | `subsections[subsection_id=COMPONENTS_OR_SYSTEM]` |
| 8.2 | Process or Method Steps | `subsections[subsection_id=PROCESS_OR_METHOD_STEPS]` |
| 8.3 | Embodiments | `subsections[subsection_id=EMBODIMENTS]` |
| 9 | Experimental Examples and Results | `draft_sections[section_id=EXPERIMENTAL_EXAMPLES_AND_RESULTS]` |
| 10 | Missing Information and Author Questions | `missing_information`, `conflicts`, `author_questions` |
| 11 | Evidence and Reference Appendix | `evidence_appendix` |

## Rendering rules

- `PRESENT` content is rendered in contract order without adding technical statements.
- `MISSING` title, Abstract, section, or subsection retains its heading and exact marker `[AUTHOR CONFIRMATION REQUIRED]`.
- Every rendered technical paragraph is followed by its grounding label, evidence IDs, and source paths.
- `INFERENCE` remains explicitly labeled `INFERENCE`.
- Conflicts retain `UNRESOLVED`, both evidence references, the exact marker, and linked author questions.
- Drawing records describe only the contract state. Proposed or missing drawings are labeled `not supplied`; the renderer creates no figure or figure number.
- The appendix renders only the evidence records supplied by `evidence_appendix` and preserves usage references.
- Claims and Draft Claims have no mapping and are rejected by the strict input schema.
- The renderer does not provide legal advice, novelty or inventive-step conclusions, patentability assessment, or filing-ready representation.
