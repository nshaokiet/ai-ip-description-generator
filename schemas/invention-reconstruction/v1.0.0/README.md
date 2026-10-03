# Invention Reconstruction Contract v1.0.0

Canonical schema: `schemas/invention-reconstruction/v1.0.0/invention-reconstruction.schema.json`

Dialect: JSON Schema Draft 2020-12

Output identity: `INVENTION_RECONSTRUCTION` / `1.0.0`

## Purpose and boundary

This contract is the grounded intermediate model between APP-002 + AI-001 and future P2-003 USPTO specification generation. It is not final patent prose, a Claims contract, legal advice, patentability analysis, provider semantic validation, or filing-ready content.

The initial producer is deterministic and offline:

```text
APP-002 ExtractionInputEnvelope
        +
AI-001 STRUCTURED_INVENTION_ANALYSIS v1
        ↓
P2-002 offline reconstruction and validation
        ↓
INVENTION_RECONSTRUCTION v1.0.0
```

The source envelope remains evidence authority. AI-001 remains the structured semantic-analysis authority. Neither upstream contract is copied or replaced by this schema.

## Root contract

Every root field is required and every object is strict:

- `schema_version` — fixed `1.0.0`;
- `output_type` — fixed `INVENTION_RECONSTRUCTION`;
- `output_notice` — machine-enforced draft/legal/Claims boundaries;
- `document_metadata` — coherent source identity;
- `provenance` — APP-002, AI-001, and `OFFLINE_DETERMINISTIC` identity;
- `invention_model` — reconstructed technical model; and
- `review_package` — evidence, conflicts, missing information, author questions, and warnings.

## Invention model

The model contains title candidates, technical field/context, problems, solution concepts, elements, relationships, method steps, flows, parameters, technical effects, embodiments, variants, and source artifacts.

Initial deterministic adapter rules are intentionally conservative:

- AI-001 components become `OTHER` elements with `UNKNOWN` essentiality;
- `related_component_ids` becomes only `RELATED_TO`;
- process inputs/outputs become `INPUT_TO_STEP` / `OUTPUT_FROM_STEP` plus `UNSPECIFIED` flows;
- sequence does not create dependencies;
- experiment values become `EXACT`, `EXPERIMENTAL_CONDITION` or `EXPERIMENTAL_RESULT`, and `EXAMPLE_ONLY`;
- SOURCE_FACT/PARAPHRASE effects are `SOURCE_REPORTED`; INFERENCE effects are `SUPPORTED_CONSEQUENCE`;
- SOURCE_FACT/PARAPHRASE embodiments are `EXPLICIT`; INFERENCE embodiments are `SYNTHESIZED`;
- the adapter emits no variants and no `HUMAN_CONFIRMED` state.

Potential distinguishing features are retained as review warnings instead of being promoted into novelty or patentability conclusions.

## Grounding

The contract uses the P2-001 vocabulary:

- `SOURCE_FACT`
- `PARAPHRASE`
- `INFERENCE`
- `SAFE_GENERALIZATION`
- `PROPOSED_VARIANT`
- `MISSING`
- `HUMAN_CONFIRMED`

The initial adapter maps AI-001 labels exactly and never promotes `INFERENCE`. Every material assertion has evidence IDs and AI-001 JSON Pointer paths.

`SAFE_GENERALIZATION` supports only `SG-01_EXPLICIT_SOURCE_CATEGORY`. NFKC/case/whitespace-normalized category and member terms must occur as whole terms within individual cited APP-002 units (never joined across units). No synonym expansion or singularization is performed. A supplied assertion may only replace a literal member term with the explicit source category; all other content, structure, paths, evidence and numeric values must equal the deterministic projection. Upstream `INFERENCE` cannot be promoted to this class. The adapter does not generate this class.

`PROPOSED_VARIANT` is review-only. `HUMAN_CONFIRMED` and `HUMAN_RESOLVED` are reserved contract states but are rejected by the initial runtime because no authorized Human audit input exists.

The business validator defaults to producer mode: any variant absent from the
upstream projection is rejected. `allow_review_candidates=True` is an explicit
validator-only mode for supplied proposed-variant fixtures, not generation or
Human approval. Such candidates must have `PROPOSED_VARIANT` support,
`PROPOSED_REQUIRES_HUMAN_CONFIRMATION` status,
`human_confirmation_required=true`, and `filing_content_eligible=false`.

Opaque upstream scalar strings (including range-like text such as `5–10`) remain
`EXACT` strings; the adapter does not parse bounds, infer sets, or widen scope.
Each parameter links both its experiment grounding and the precise condition or
result path. Missing-information `target_path` retains the **AI-001 namespace**;
it may deliberately identify absent content and is not a reconstruction pointer.
All `analysis_paths` reference AI-001 records. Source artifacts preserve drawing
ID/kind/status and text-based figure/table references, without image interpretation.

## Validation layers

JSON Schema validates local structure, constants, enums, strictness, identifier form, and local state combinations.

`backend/app/services/invention_reconstruction_validation.py` validates:

- upstream/source/output identity coherence;
- exact evidence ID/type/locator and contiguous verbatim excerpt integrity;
- unique IDs and cross-object references;
- AI-001 analysis-path existence and non-promotional grounding;
- deterministic entity, relationship, flow, parameter, effect, embodiment, missing/question, and warning mappings;
- method dependency references and cycle rejection;
- SAFE_GENERALIZATION source-term rules;
- range anti-broadening;
- proposed-variant, Human-confirmation, and conflict gates;
- Claims, administrative fabrication, and legal/patentability exclusions.

The full deterministic projection is checked, not only IDs and primary text.
These checks validate integrity and faithful transformation; they do **not**
establish scientific truth or semantic entailment of arbitrary AI-001 prose.
Semantic acceptance remains `NOT_DETERMINED`. Legal phrase checks are conservative
guards, not a complete natural-language legal classifier. Source excerpts remain
untrusted data and cannot alter notice, grounding, review gates or output structure.

## Future P2-003 handoff (not implemented)

P2-003 must consume validated `invention_model`, preserving evidence/support and
conditions, and keep `review_package` as internal review data. Eligible technical
grounding is SOURCE_FACT/PARAPHRASE/INFERENCE/validated SAFE_GENERALIZATION; this
does not waive Human review. Proposed variants, MISSING records, unresolved
conflicts and unaudited Human states cannot be silently promoted into filing prose.
Warnings are candidate review content, not novelty or patentability conclusions.
Proposed drawing requirements are not existing drawings. The root notice remains
draft, claim-free and not filing-ready. No P2-003 generator or public route is added.

## Parser and runtime limits

APP-002 currently emits only `TEXT` and `TABLE`. P2-002 does no OCR, pixel inspection, vision, external retrieval, prior-art search, provider call, or public endpoint integration. Figure/drawing records are preserved only when represented by valid upstream data; no patent drawing is generated.

## Verification

```powershell
python -m pytest tests/schema/test_invention_reconstruction_v1.py -q
python -m pytest tests/backend/test_invention_reconstruction.py -q
```

All fixtures under `tests/fixtures/invention-reconstruction/v1.0.0/` are synthetic. The fixture corpus covers the 16 reviewed representative/adversarial categories without real or confidential research data.

## Version history

| Previous | New | Date | Author | Change / reason | Task | Breaking |
|---|---|---|---|---|---|---|
| None | 1.0.0 | 03/10/2026 | Codex | Initial additive contract, approved offline reconstruction boundary | P2-002 | No — existing contracts unchanged |
