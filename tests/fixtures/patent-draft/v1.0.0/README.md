# Patent Draft Contract v1.0.0 fixtures

All fixtures are synthetic and contain no real research data, PII, credentials, or provider output.

## Behavior cases

- `cases/representative.json`: complete technical mapping with all six draft sections present.
- `cases/missing-information.json`: no supported content; required headings and confirmation markers remain.
- `cases/conflicting-evidence.json`: two contradictory synthetic values remain unresolved and link an author question.
- `cases/prompt-injection.json`: hostile source text is treated as untrusted data and excluded from drafted content.

Each behavior case contains the documented input envelope and a deterministic expected output. Expected outputs are offline oracles only; they are not evidence that a live model follows the prompt.

## Invalid outputs

- `invalid/unsupported-claims-field.json`: otherwise schema-valid root with unexpected `claims`; expected validator is `additionalProperties` at the root.
- `invalid/missing-evidence.json`: otherwise schema-valid draft with an empty paragraph grounding list; expected validator is `minItems` at `draft_sections/0/paragraphs/0/grounding/evidence_ids`.
- `invalid/invalid-cross-reference.json`: contains source analysis plus a schema-valid draft whose selected title references a missing title ID; expected business error path is `/selected_title/source_title_candidate_id` and missing target is `title-does-not-exist`.

JSON Schema validates local structure. Logical-ID uniqueness, source paths, cross-references, Abstract word count, evidence closure, and reverse usage are downstream business rules.
