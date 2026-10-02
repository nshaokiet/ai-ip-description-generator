# USPTO Patent Specification Target Schema v2.0.0

## Status and boundary

This directory defines the machine-readable **target contract** for a USPTO-style nonprovisional utility patent specification draft. It is a specification artifact for P2-001 only.

It does not implement generation, Claims runtime, rendering, filing, legal review, patentability analysis, provider access, or production behavior. Every output remains a draft requiring Human/IP-specialist review.

## Files

- `uspto-specification.schema.json` — JSON Schema Draft 2020-12 contract.
- `README.md` — semantic rules, validation boundary, and v1 compatibility record.

Synthetic examples are under `tests/fixtures/uspto-specification/v2.0.0/`.
All P2-001 fixtures set `document_metadata.source_document.synthetic` to `true`.
The field is an explicit provenance boolean rather than a hard-coded product
restriction, so a later authorized real-data runtime could set it to `false`.

## Root model

The root object is strict (`additionalProperties: false`) and contains:

- `schema_version` — fixed to `2.0.0`;
- `output_type` — fixed to `USPTO_SPECIFICATION_DRAFT`;
- `document_metadata` — draft/source identity without fabricated filing metadata;
- `section_order` — the complete canonical filing order;
- `sections` — filing-style content other than Claims and Abstract;
- `claims` — a separately modeled target Claims section;
- `abstract` — a separately modeled Abstract section;
- `review_boundary` — constants that keep draft content and internal review data distinct; and
- `review_package` — evidence, missing information, author questions, claim support, and warnings that must not be rendered as filing content.

## Canonical section order

The schema fixes this order:

1. `TITLE_OF_THE_INVENTION`
2. `CROSS_REFERENCE_TO_RELATED_APPLICATIONS`
3. `STATEMENT_REGARDING_FEDERALLY_SPONSORED_RESEARCH_OR_DEVELOPMENT`
4. `NAMES_OF_PARTIES_TO_JOINT_RESEARCH_AGREEMENT`
5. `INCORPORATION_BY_REFERENCE`
6. `STATEMENT_REGARDING_PRIOR_DISCLOSURES`
7. `BACKGROUND_OF_THE_INVENTION`
   - `FIELD_OF_THE_INVENTION`
   - `DESCRIPTION_OF_RELATED_ART`
8. `BRIEF_SUMMARY_OF_THE_INVENTION`
9. `BRIEF_DESCRIPTION_OF_THE_DRAWINGS`
10. `DETAILED_DESCRIPTION_OF_THE_INVENTION`
11. `CLAIMS`
12. `ABSTRACT_OF_THE_DISCLOSURE`
13. `SEQUENCE_LISTING`

`claims` and `abstract` are root objects because each has rules different from ordinary prose sections. `sections` stores positions 1–10 and 13. The fixed `section_order` field and prefix-constrained section objects define their rendered order.

## Section states

Ordinary sections and Background subsections use:

- `PRESENT` — filing-style content exists;
- `MISSING` — the required content is known to be absent;
- `HUMAN_CONFIRMATION_REQUIRED` — the system cannot safely determine the content without Human input; or
- `NOT_APPLICABLE` — permitted only with `not_applicable_basis`.

`NOT_APPLICABLE` requires a rule identifier, rationale, evidence IDs, and either:

- `HUMAN_CONFIRMED`; or
- `APPROVED_DETERMINISTIC_RULE`.

The Claims and Abstract sections omit `NOT_APPLICABLE` because a nonprovisional utility specification target cannot silently discard them. They may remain `MISSING` or `HUMAN_CONFIRMATION_REQUIRED` until later authorized work supplies supported content.

Administrative statements must never be inferred from a scientific paper. Cross-object validation therefore requires a `PRESENT` administrative paragraph to be supported by `HUMAN_CONFIRMATION` or an `AUTHORIZED_EXTERNAL_SOURCE`. Missing administrative data remains explicit in `review_package.missing_information`.

## Grounding model

Every substantive paragraph stores review-only support metadata:

- `source_paths`;
- `evidence_ids`; and
- one `grounding_class` from `SOURCE_FACT`, `PARAPHRASE`, `INFERENCE`, `SAFE_GENERALIZATION`, `PROPOSED_VARIANT`, `MISSING`, or `HUMAN_CONFIRMED`.

These are v2-only values. They do not modify the released v1 enum.

`SAFE_GENERALIZATION` and `PROPOSED_VARIANT` are classification targets, not authorization to invent content. Runtime policy for either class belongs to a later approved task.

## Claims target contract

The Claims section models:

- `claim_number`;
- `claim_type`;
- `independent_or_dependent`;
- `depends_on`;
- `claim_text`; and
- decomposed `claim_elements`.

Each claim element can link to future evidence and specification support through `evidence_ids`, `specification_section_ids`, and `support_status` (`SUPPORTED`, `HUMAN_CONFIRMATION_REQUIRED`, or `UNSUPPORTED`).

Schema validation enforces the local shape and independent/dependent cardinality. Business validation in `tests/schema/test_uspto_specification_v2.py` checks unique/contiguous numbering, backward dependency references, evidence links, and unsupported elements. Nothing in this contract represents a conclusion on legal sufficiency, patentability, validity, infringement, grantability, or filing readiness.

## Drawings target contract

The Brief Description of the Drawings may carry a future drawing plan with:

- `figure_id`;
- `figure_label`;
- `title`;
- `description`;
- `source_figure_ids`; and
- `reference_numerals` such as `100` for a system and `110` for a component.

P2-001 creates no drawing images. The model only preserves the identifiers needed by later drawing and detailed-description tasks.

## Abstract rule

The Abstract is separate from Brief Summary. Its declared `word_count` is constrained to 150 or fewer, and the business validator recalculates the count from `text` to detect a stale or false declaration.

## Filing/review separation

Only `sections`, `claims`, and `abstract` are filing-style content fields. `review_package`, paragraph support metadata, missing-information IDs, warnings, and internal identifiers are review data and must not be rendered into the filing-style body.

The required `review_boundary` constants make this separation explicit and record that:

- Human review is required;
- the artifact is not filing-ready or legal advice;
- no patentability assessment is included; and
- Claims runtime is not implemented.

## Validation

From the repository root:

```powershell
python -m pytest tests/schema/test_uspto_specification_v2.py -q
```

The tests cover schema self-validation, a representative synthetic document, strict-property rejection, section order, the 150-word Abstract limit, claim dependencies, unsupported claim elements, administrative anti-hallucination, required Claims modeling, and v1 immutability.

## v1 immutability

P2-001 adds a new versioned schema and does not overwrite v1. The test suite pins these baseline SHA-256 values:

| Released v1 file | SHA-256 |
| --- | --- |
| `schemas/patent-draft/v1.0.0/patent-draft.schema.json` | `9f08aa2487b9bcacd3e40885899c6d7871f1df88b27cfc6d5ad85f01bbf3cb21` |
| `schemas/patent-draft/v1.0.0/README.md` | `8449b2e2975b2661184a8e616dc5972ca773e969105fe6eb87342f1c53b869cd` |

Current v1 prompts, validators, runtime code, and DOCX templates remain outside this change.

## Downstream ownership

- P2-002 may define an invention-reconstruction input feeding this target.
- P2-003 may define specification-generation behavior against this schema.
- P2-004 or a separately authorized Claims task may implement Claims behavior and support auditing.
- Later drawing and DOCX v2 tasks may consume the figure/reference-numeral and filing/review boundaries.

Those tasks are not authorized or implemented by P2-001.
