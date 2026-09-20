# Patent Draft Generation Contract v1.0.0

Canonical schema: `schemas/patent-draft/v1.0.0/patent-draft.schema.json`

JSON Schema dialect: Draft 2020-12

Status: **Gemini Review Passed — Awaiting Human Merge Approval**

## Purpose and boundary

This contract represents an English patent-description draft generated from a validated Invention Output Schema v1.0.0 payload. It is the controlled boundary between structured invention analysis and the future DOCX template.

It is not legal advice, a patentability assessment, a filing-ready application, or a claims contract. Claims and Draft Claims are excluded completely. Human approval/audit state and live-model/provider integration are also outside v1.0.0.

## Canonical input

The prompt receives a strict documented envelope containing:

- `input_contract_version: "1.0.0"`;
- `task: "GENERATE_PATENT_DESCRIPTION_DRAFT"`;
- `source_analysis`, valid against `schemas/invention-output/v1.0.0/invention-output.schema.json`;
- approved `generation_config` constants.

There is no separate input-envelope schema file in v1.0.0. Automated tests validate the envelope and validate `source_analysis` against the canonical input schema.

The caller may provide `selected_title_candidate_id`. The prompt may select only that existing candidate and must copy its text exactly. If selection is absent or invalid, the title is `MISSING`; the prompt must not invent a title.

## Root fields

All fields are required and all objects are strict with `additionalProperties: false`.

| Field | Purpose |
|---|---|
| `schema_version` | Exact contract version `1.0.0` |
| `output_type` | Exact value `PATENT_DESCRIPTION_DRAFT` |
| `document_metadata` | Draft identity and exact source-contract/document traceability |
| `output_notice` | Machine-enforced draft, Human-review, legal, filing, patentability and claims flags |
| `section_order` | Exact 11-part order approved for the future DOCX |
| `selected_title` | Caller-selected source candidate or explicit missing state |
| `abstract` | Grounded English abstract or explicit missing state |
| `draft_sections` | Six ordered technical sections and seven canonical subsections |
| `drawings` | Source/proposed drawing state without generating drawings |
| `missing_information` | Source or controlled draft-validation gaps |
| `conflicts` | Unresolved contradictory evidence |
| `author_questions` | Questions tied to missing information and conflicts |
| `evidence_appendix` | Only evidence actually used by the draft |

No field has a default. Producers must emit every required value explicitly.

## Section model

`section_order` contains the exact eleven approved document parts. Technical prose is stored in six `draft_sections` at overall sequences 4–9:

1. `TECHNICAL_FIELD`
2. `BACKGROUND`
3. `SUMMARY_OF_TECHNICAL_DISCLOSURE`
4. `BRIEF_DESCRIPTION_OF_DRAWINGS`
5. `DETAILED_DESCRIPTION`
6. `EXPERIMENTAL_EXAMPLES_AND_RESULTS`

Summary has four ordered subsections: technical problems, technical solutions, potential distinguishing features, and technical effects. Detailed Description has three: components or system, process or method steps, and embodiments.

Status is only `PRESENT` or `MISSING`. Required content that is unavailable keeps its heading and uses the exact marker `[AUTHOR CONFIRMATION REQUIRED]`. v1.0.0 does not use `OMITTED`.

## Grounding and evidence

Every technical paragraph has:

- a globally unique `paragraph_id`;
- contiguous `sequence` within its content block;
- one or more JSON Pointer `source_paths` relative to `source_analysis`;
- `grounding.label`, one of `SOURCE_FACT`, `PARAPHRASE`, `INFERENCE`;
- one or more `grounding.evidence_ids`.

Every referenced evidence ID must exist in both the source analysis and `evidence_appendix`. Appendix metadata and excerpt must equal the source evidence. `usage_references` provide the reverse link to title, abstract, paragraph, drawing, or conflict. Unused evidence is not allowed in the appendix.

JSON Schema cannot prove logical-ID uniqueness, resolve JSON Pointers, confirm cross-reference existence, recalculate Abstract words, or establish semantic support. Those checks are downstream business validation implemented and tested in `tests/draft/test_patent_draft_contract_v1.py`.

## Abstract word count

For a present Abstract:

1. Normalize text with Unicode NFKC.
2. Count tokens with Unicode regular expression `\b\w+(?:[-'’]\w+)*\b`.
3. Require the calculated value to equal `word_count`.
4. Require no more than 150 words.

If supported content is insufficient, the Abstract remains structurally present as `status: "MISSING"` with the approved marker and linked missing-information IDs.

## Missing information and conflicts

Source gaps retain their source missing-information ID. Draft validation may create gaps only with these controlled rule IDs:

- `TITLE_SELECTION_REQUIRED`
- `ABSTRACT_SOURCE_INSUFFICIENT`
- `SECTION_SOURCE_INSUFFICIENT`
- `CONFLICT_REQUIRES_RESOLUTION`

Conflicts require at least two evidence IDs, remain `UNRESOLVED`, preserve both sides, and link at least one author question. The prompt must not choose a preferred value.

## Drawing rules

- `SOURCE_FIGURE` requires evidence.
- `PROPOSED_DRAWING` requires Human confirmation.
- `MISSING` requires Human confirmation.
- The contract records requirements only; it does not create images or unsupported figure details.

## Legal boundary

`output_notice.includes_claims`, `is_legal_advice`, `filing_ready`, and `includes_patentability_assessment` are all fixed to `false`. Strict objects reject an unexpected `claims` property. A downstream minimal phrase scanner checks generated narrative as defense in depth; it is not a complete legal classifier.

## Validation commands

```powershell
$env:PYTHONDONTWRITEBYTECODE="1"
.\.venv\Scripts\python.exe -m unittest discover -s tests/schema -p "test_*.py" -v
.\.venv\Scripts\python.exe -m unittest discover -s tests/prompt -p "test_*.py" -v
.\.venv\Scripts\python.exe -m unittest discover -s tests/draft -p "test_*.py" -v
```

Fixtures are synthetic offline oracles. Passing them does not demonstrate live-model compliance or provider integration.
