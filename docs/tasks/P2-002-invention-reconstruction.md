# P2-002 — Invention Reconstruction Contract & Offline Reconstruction Pipeline

## Metadata

| Field | Value |
|---|---|
| Task ID | P2-002 |
| Title | Invention Reconstruction Contract & Offline Reconstruction Pipeline |
| Specification version | 0.1.0 |
| Status | **SPECIFICATION READY FOR FIXED-SHA INDEPENDENT REVIEW — IMPLEMENTATION NOT AUTHORIZED** |
| Human authorization | `HUMAN-P2-002-INVENTION-RECONSTRUCTION-2026-10-03` |
| Authorized baseline | `054410f937eaaecf7b462855b7dce921e40e8924` |
| Owner | ChatGPT/Codex under AGENTS.md role separation |
| Independent reviewer | Gemini 3.1 Pro High / Antigravity read-only |
| Provider/API calls | **NONE / NOT AUTHORIZED** |
| Real/confidential research data | **NOT AUTHORIZED** |
| Claims runtime | **NOT IMPLEMENTED / OUT OF SCOPE** |
| Production | **NOT APPROVED / NOT PERFORMED** |
| BLK-003 | **OPEN** |
| EVAL-001 PRODUCT_RUNTIME | **DEFERRED — AWAITING FUNDING** |

## 1. Purpose

P2-002 defines and later implements a strict intermediate **Invention Reconstruction** contract between the current parsed/evidence + structured-analysis layers and future USPTO specification generation.

Target flow:

```text
Scientific Paper
  → APP-002 Parsed Source Units / Evidence
  → AI-001 Structured Invention Analysis v1
  → P2-002 INVENTION RECONSTRUCTION
  → P2-003 USPTO Specification Generation v2
  → P2-004 Claims / Support Audit
  → DOCX v2 + Review Package
```

P2-002 does **not** generate final patent prose, Claims, filing-ready content, patentability conclusions, prior-art conclusions, or legal advice.

The central product requirement is to reconstruct the technical invention from grounded scientific evidence rather than directly reformatting paper sections into patent sections.

## 2. Current architecture audit and upstream contracts

### 2.1 APP-002 — canonical parsed evidence

APP-002 currently produces a strict `ExtractionInputEnvelope` containing:

- `document_metadata`;
- ordered `source_units[]`;
- caller-assigned deterministic `evidence_id`;
- `evidence_type` currently emitted by APP-002 as `TEXT` or `TABLE`;
- source locator fields;
- verbatim normalized `content`.

APP-002 does not perform OCR, image understanding, semantic summarization, or provider/model invocation.

### 2.2 AI-001 — canonical structured invention analysis

AI-001 `STRUCTURED_INVENTION_ANALYSIS` v1 already models:

- title candidates;
- technical field;
- background;
- technical problems;
- technical solutions;
- components;
- process steps;
- potential distinguishing features;
- technical effects;
- embodiments;
- experimental data;
- drawing requirements;
- missing information;
- author questions;
- evidence.

AI-001 v1 grounding classes are exactly:

- `SOURCE_FACT`;
- `PARAPHRASE`;
- `INFERENCE`.

Missing/ambiguous/conflicting information is represented separately and must not be silently fabricated.

### 2.3 P2-001 — target USPTO v2 contract

P2-001 reserves these v2 grounding classes:

- `SOURCE_FACT`;
- `PARAPHRASE`;
- `INFERENCE`;
- `SAFE_GENERALIZATION`;
- `PROPOSED_VARIANT`;
- `MISSING`;
- `HUMAN_CONFIRMED`.

P2-001 intentionally does not define runtime semantics for `SAFE_GENERALIZATION` and `PROPOSED_VARIANT`. P2-002 owns those reconstruction-level semantics.

## 3. Architecture decision — P2-002 input boundary

P2-002 consumes **both** current canonical upstream artefacts:

1. APP-002 `ExtractionInputEnvelope`;
2. AI-001 `STRUCTURED_INVENTION_ANALYSIS` v1.

The implementation must not duplicate either input schema into a third copy.

Recommended service boundary:

```python
reconstruct(
    source_envelope: ExtractionInputEnvelope,
    structured_analysis: dict,
) -> InventionReconstruction
```

The source envelope remains the canonical evidence authority; AI-001 remains the canonical structured semantic analysis.

### 3.1 Input coherence validation

Before reconstruction, the implementation must verify document identity coherence.

Where present in both contracts, the following values must match exactly:

- `document_id`;
- `file_name`;
- `media_type`;
- `sha256`.

Every AI-001 evidence ID used by a reconstruction assertion must correspond to a source evidence record that can be traced to the input evidence envelope.

For mapped evidence, the implementation must verify, where represented by the current upstream contracts:

- evidence ID integrity;
- evidence type integrity;
- locator integrity;
- evidence excerpt is a contiguous verbatim substring of the canonical source-unit content.

A mismatch fails closed.

## 4. Output contract identity

Canonical new artefact:

```text
schemas/invention-reconstruction/v1.0.0/
  invention-reconstruction.schema.json
  README.md
```

Contract identity:

```text
schema_version = "1.0.0"
output_type    = "INVENTION_RECONSTRUCTION"
JSON Schema    = Draft 2020-12
```

All strict objects use `additionalProperties: false` unless a later reviewed requirement explicitly justifies otherwise.

Released v1 schemas remain immutable.

## 5. Root reconstruction shape

The target output is conceptually:

```text
INVENTION_RECONSTRUCTION
├── schema_version
├── output_type
├── output_notice
├── document_metadata
├── provenance
├── invention_model
│   ├── title_candidates
│   ├── technical_field
│   ├── technical_context
│   ├── problems
│   ├── solution_concepts
│   ├── elements
│   ├── relationships
│   ├── method_steps
│   ├── flows
│   ├── parameters
│   ├── technical_effects
│   ├── embodiments
│   ├── variants
│   └── source_artifacts
└── review_package
    ├── evidence
    ├── conflicts
    ├── missing_information
    ├── author_questions
    └── warnings
```

P2-002 output is a technical reconstruction model, not final patent prose.

## 6. Output notice

The reconstruction contract must mechanically preserve these boundaries:

```text
status = DRAFT
human_review_required = true
is_legal_advice = false
filing_ready = false
includes_patentability_assessment = false
includes_claims = false
```

## 7. Provenance

The output must identify its canonical upstream contracts and reconstruction mode.

At minimum:

- source evidence contract: APP-002 / `ExtractionInputEnvelope`;
- structured analysis contract: AI-001 / `STRUCTURED_INVENTION_ANALYSIS` v1;
- reconstruction mode for the initial implementation: `OFFLINE_DETERMINISTIC`.

The initial offline implementation must not imply provider-assisted semantic reconstruction or PRODUCT_RUNTIME validation.

## 8. Technical problem model

Each reconstructed problem contains:

- stable `problem_id`;
- statement;
- support.

P2-002 must not convert source wording such as “novel”, “new”, “state of the art”, or citation comparisons into patentability conclusions.

Literature statements may be represented only as grounded technical context.

## 9. Technical solution / inventive concept model

Each solution concept contains at least:

- stable `solution_id`;
- statement;
- `addresses_problem_ids[]`;
- related technical element IDs;
- related method-step IDs;
- support.

The model must preserve distinctions among:

- core technical solution concept;
- supporting mechanism;
- optional/conditional feature;
- experimental implementation detail;
- observed result.

The contract must not equate an experimental detail with an essential invention limitation without support.

## 10. Technical elements

The reconstruction layer normalizes AI-001 components into technical elements.

Initial controlled element types:

- `DEVICE`;
- `MODULE`;
- `STRUCTURE`;
- `MATERIAL`;
- `SOFTWARE_COMPONENT`;
- `DATA_STRUCTURE`;
- `PROCESSING_BLOCK`;
- `CHEMICAL_ELEMENT`;
- `BIOLOGICAL_ELEMENT`;
- `OTHER`.

Each element contains:

- stable `element_id`;
- name;
- optional description;
- `element_type`;
- `essentiality`;
- support.

### 10.1 Essentiality

Allowed states:

- `ESSENTIAL`;
- `OPTIONAL`;
- `CONDITIONAL`;
- `UNKNOWN`.

Initial offline reconstruction must be conservative. If upstream evidence does not establish essentiality, the value is `UNKNOWN`.

Frequency of mention, section placement, or experimental use alone must not cause automatic `ESSENTIAL` classification.

## 11. Relationships

The reconstruction model uses explicit typed relationships instead of AI-001's untyped `related_component_ids`.

Initial controlled vocabulary:

- `RELATED_TO`;
- `PART_OF`;
- `CONTAINS`;
- `CONNECTED_TO`;
- `COUPLED_TO`;
- `COMMUNICATES_WITH`;
- `RECEIVES_FROM`;
- `OUTPUTS_TO`;
- `CONTROLS`;
- `TRANSFORMS`;
- `MEASURES`;
- `STORES`;
- `EXECUTES`;
- `INPUT_TO_STEP`;
- `OUTPUT_FROM_STEP`;
- `DEPENDS_ON`.

Each relationship contains:

- `relationship_id`;
- `subject_id`;
- `relation_type`;
- `object_id`;
- support.

### 11.1 Conservative mapping rule

AI-001 `related_component_ids` may deterministically map to `RELATED_TO`.

It must not be promoted to a more specific relation such as `CONNECTED_TO`, `CONTROLS`, or `COUPLED_TO` unless upstream evidence directly supports that relation.

## 12. Method/process reconstruction

Each method step contains:

- `step_id`;
- `sequence_index`;
- action;
- `input_element_ids[]`;
- `output_element_ids[]`;
- `dependency_step_ids[]`;
- conditions;
- support.

Sequence order does not automatically imply causal dependency.

The implementation must not invent process ordering, prerequisites, or branching semantics absent from the current evidence/analysis.

## 13. Input/output/data/material flow model

Supported flow types:

- `MATERIAL`;
- `SIGNAL`;
- `DATA`;
- `ENERGY`;
- `CONTROL`;
- `UNSPECIFIED`.

Each flow contains:

- `flow_id`;
- `flow_type`;
- source reference;
- target reference;
- description;
- support.

If upstream evidence establishes input/output relationships but not the nature of the flow, the reconstruction uses `UNSPECIFIED`.

## 14. Parameters, conditions, values and ranges

Each reconstructed parameter contains:

- `parameter_id`;
- name;
- role;
- `value_kind`;
- value/range representation;
- unit where applicable;
- `scope_status`;
- related reconstruction IDs;
- support.

Initial `value_kind` values:

- `EXACT`;
- `RANGE`;
- `SET`;
- `QUALITATIVE`.

Initial roles:

- `OPERATING_CONDITION`;
- `EXPERIMENTAL_CONDITION`;
- `EXPERIMENTAL_RESULT`;
- `THRESHOLD`;
- `DIMENSION`;
- `OTHER`.

Initial scope states:

- `EXAMPLE_ONLY`;
- `SUPPORTED_RANGE`;
- `UNKNOWN_SCOPE`.

An experimental condition does not become a mandatory invention limitation by default.

A source value or range must never be numerically broadened without explicit support.

## 15. Technical effects

Each effect contains:

- `effect_id`;
- statement;
- related solution IDs;
- related element IDs;
- conditions;
- `effect_basis`;
- support.

Allowed effect bases:

- `SOURCE_REPORTED`;
- `SUPPORTED_CONSEQUENCE`.

Unsupported extrapolation does not enter the supported invention model. It is recorded as a warning or missing-information/review issue.

No commercial, legal, novelty, grantability, or patentability effect may be inferred.

## 16. Embodiments

Each embodiment contains:

- `embodiment_id`;
- name;
- description;
- element IDs;
- method-step IDs;
- parameter IDs;
- `disclosure_status`;
- support.

Allowed disclosure states:

- `EXPLICIT`;
- `SYNTHESIZED`;
- `PROPOSED_REQUIRES_HUMAN_CONFIRMATION`.

Source-grounded or faithful paraphrased embodiments may be `EXPLICIT`. Limited synthesis may be `SYNTHESIZED`. Unsupported proposed embodiments must not be silently treated as source-supported embodiments.

## 17. Variants

Variants are modeled separately from embodiments.

Each variant contains:

- `variant_id`;
- description;
- base entity IDs;
- status;
- support.

Allowed status:

- `SOURCE_SUPPORTED`;
- `PROPOSED_REQUIRES_HUMAN_CONFIRMATION`;
- `HUMAN_CONFIRMED`.

The initial deterministic offline pipeline must not invent new variants. If there is no supported variant evidence, `variants` is empty.

## 18. Grounding model

P2-002 adopts the P2-001 grounding vocabulary:

- `SOURCE_FACT`;
- `PARAPHRASE`;
- `INFERENCE`;
- `SAFE_GENERALIZATION`;
- `PROPOSED_VARIANT`;
- `MISSING`;
- `HUMAN_CONFIRMED`.

A material reconstruction assertion stores support metadata containing, as applicable:

- `grounding_class`;
- `evidence_ids[]`;
- `analysis_paths[]`;
- generalization metadata when `SAFE_GENERALIZATION` is used.

### 18.1 AI-001 mapping

Initial mapping is exact and non-promotional:

```text
AI-001 SOURCE_FACT → SOURCE_FACT
AI-001 PARAPHRASE  → PARAPHRASE
AI-001 INFERENCE   → INFERENCE
```

No `INFERENCE → SOURCE_FACT` promotion is allowed.

## 19. Supported synthesis

P2-002 does not add a separate `SUPPORTED_SYNTHESIS` enum.

Limited synthesis already maps to `INFERENCE`, with explicit evidence IDs and AI-001 analysis paths.

An inference must not introduce a new unsupported mechanism, component, causal relation, parameter, technical effect, embodiment, or use case.

## 20. SAFE_GENERALIZATION

P2-002 defines deterministic runtime semantics for `SAFE_GENERALIZATION`.

Initial implementation supports exactly one approved rule:

```text
SG-01_EXPLICIT_SOURCE_CATEGORY
```

The rule allows use of a more general category only when that category is itself explicitly present in cited source evidence and the cited member terms are also source-supported.

Example of a potentially valid pattern:

```text
source: "sensors such as photodiodes and phototransistors"
generalized term: "sensor"
members: "photodiode", "phototransistor"
```

The source evidence must actually contain the general category and members.

### 20.1 Required metadata

A `SAFE_GENERALIZATION` assertion must carry:

- `rule_id`;
- `generalized_term`;
- `member_terms[]`;
- `evidence_ids[]`.

### 20.2 Validator requirements

The validator must confirm:

1. the rule is an approved deterministic rule;
2. generalized term exists in cited source evidence;
3. cited member terms exist in cited evidence;
4. evidence IDs exist;
5. no numerical range broadening;
6. no new component;
7. no new mechanism;
8. no new causal relation;
9. no new technical effect;
10. no new domain/use case.

### 20.3 Prohibited examples

The following are not safe generalization unless explicit source evidence provides the broader category:

```text
"copper electrode" → "conductive material"
```

The following is always prohibited without explicit source support:

```text
"5–10 μm" → "1–20 μm"
```

### 20.4 Initial offline generation rule

The initial deterministic adapter must **not automatically synthesize new SAFE_GENERALIZATION assertions from AI-001**.

It supports the contract and validation semantics but does not fabricate such assertions.

## 21. PROPOSED_VARIANT

`PROPOSED_VARIANT` is review-only candidate content.

It is not a source fact and always requires Human confirmation.

P2-003 must not automatically treat `PROPOSED_VARIANT` content as filing-style patent content.

A future Human-confirmation workflow may promote eligible content only with explicit audit evidence.

## 22. HUMAN_CONFIRMED

P2-002 reserves `HUMAN_CONFIRMED` for a future authorized Human-evidence path.

The initial implementation has no canonical Human-confirmation input contract and therefore must not generate `HUMAN_CONFIRMED`.

## 23. Missing information

Missing-information reason vocabulary:

- `NOT_FOUND`;
- `AMBIGUOUS`;
- `CONFLICTING`;
- `INSUFFICIENT_DETAIL`;
- `UNSUPPORTED_GENERALIZATION`;
- `HUMAN_CONFIRMATION_REQUIRED`.

Each record contains:

- `missing_id`;
- `target_path`;
- description;
- reason;
- impact;
- owner;
- source/analysis record references where available.

Gaps are never filled by fabrication.

## 24. Contradictions

The reconstruction contract supports explicit contradiction records.

A conflict contains:

- `conflict_id`;
- topic;
- affected reconstruction entity IDs;
- two or more supported alternatives when available;
- status;
- resolution metadata if later resolved.

Each alternative contains:

- statement;
- evidence IDs;
- analysis paths.

Initial status values:

- `UNRESOLVED`;
- `HUMAN_RESOLVED`.

An unresolved conflict must not be silently resolved by selecting one side.

Where AI-001 only reports `missing_information.reason = CONFLICTING` but lacks enough data to reconstruct both alternatives, P2-002 propagates the conflict as missing/review information and must not fabricate the missing side.

## 25. Figures, tables and source artifacts

P2-002 preserves supported source-artifact references.

Initial source-artifact handling supports:

- table evidence;
- figure references already represented by upstream contracts;
- drawing requirements already represented by AI-001.

APP-002 currently emits only `TEXT` and `TABLE` source units and does not perform image/vision extraction.

Therefore the initial P2-002 implementation:

- must not claim pixel/image understanding;
- must not infer figure content not represented upstream;
- may preserve figure identifiers/references if they already exist in validated upstream data;
- does not generate formal patent drawings.

## 26. Administrative information boundary

P2-002 must never infer as fact:

- inventor identity;
- assignee;
- application/priority number;
- related-application relationship;
- government funding;
- joint research agreement;
- prior-disclosure date/status;
- filing date;
- examiner;
- patent number;
- issue date;
- patent classification.

These are outside the invention model and require Human-supplied or separately authorized evidence in later work.

## 27. Claims boundary

P2-002 has no Claims-generation responsibility.

The reconstruction output must not create root-level claim drafting structures such as:

- claims;
- independent claim;
- dependent claim;
- claim text;
- claim breadth;
- claim dependency;
- claim strategy.

P2-002 also must not perform:

- novelty determination;
- non-obviousness determination;
- patentability assessment;
- infringement analysis;
- validity analysis.

P2-004 or another explicitly authorized Claims task owns those functions.

## 28. P2-003 handoff

P2-003 consumes the **validated P2-002 reconstruction output**.

P2-003 should not need to reinterpret the raw paper from scratch as its primary semantic source.

P2-003 may use:

- `invention_model`;
- grounding/support metadata;
- review-package evidence;
- missing/conflict states;

to generate supported content for the P2-001 USPTO v2 target, including later:

- Technical Field;
- Background;
- Brief Summary;
- Brief Description of Drawings;
- Detailed Description;
- Abstract.

### 28.1 Filing-content eligibility

Potentially eligible after validation:

- `SOURCE_FACT`;
- `PARAPHRASE`;
- `INFERENCE`;
- valid `SAFE_GENERALIZATION`.

Not automatically eligible:

- `PROPOSED_VARIANT`;
- `MISSING`;
- unresolved conflict;
- `HUMAN_CONFIRMED` without an authorized Human-evidence path.

P2-002 itself does not generate final USPTO specification prose.

## 29. Offline reconstruction pipeline

Initial implementation architecture:

```text
ExtractionInputEnvelope
        +
Structured Invention Analysis v1
        ↓
[1] Upstream contract validation
        ↓
[2] Document identity coherence validation
        ↓
[3] Canonical evidence index construction
        ↓
[4] AI-001 evidence ↔ APP-002 evidence integrity validation
        ↓
[5] Problem / solution normalization
        ↓
[6] Component → element reconstruction
        ↓
[7] Relationship graph construction
        ↓
[8] Method-step reconstruction
        ↓
[9] Flow normalization
        ↓
[10] Parameter / experiment reconstruction
        ↓
[11] Technical-effect reconstruction
        ↓
[12] Embodiment mapping
        ↓
[13] Missing/conflict propagation
        ↓
[14] Review-package construction
        ↓
[15] JSON Schema validation
        ↓
[16] Cross-object business validation
        ↓
INVENTION_RECONSTRUCTION
```

## 30. Offline capability boundary

### 30.1 Deterministic behavior authorized for initial implementation

- upstream validation;
- evidence preservation/integrity checking;
- deterministic ID generation;
- problem/solution normalization;
- component → element mapping;
- conservative relationship mapping;
- process-step mapping;
- input/output flow normalization;
- experiment/parameter mapping;
- effect linking;
- embodiment mapping;
- missing-information propagation;
- contradiction-state propagation where enough source structure exists;
- cross-reference validation;
- SAFE_GENERALIZATION validation;
- strict output validation.

### 30.2 Not validated by this offline task

P2-002 must not falsely claim offline validation of:

- deep semantic invention discovery from arbitrary raw prose;
- provider-level hidden relationship inference;
- automatic discovery of undisclosed embodiments;
- automatic broad technical abstraction;
- generation of new variants;
- semantic contradiction discovery where upstream structure is insufficient;
- PRODUCT_RUNTIME semantic quality.

Provider-assisted reconstruction and PRODUCT_RUNTIME evidence remain separate future work.

## 31. Determinism

For identical validated inputs, the initial reconstruction implementation must produce identical business output after canonical serialization.

Business payloads must not depend on:

- random UUIDs;
- wall-clock timestamps;
- provider request IDs;
- model output.

Recommended deterministic identifier families:

```text
IR-ELEM-0001
IR-REL-0001
IR-STEP-0001
IR-FLOW-0001
IR-PARAM-0001
IR-EFFECT-0001
IR-EMB-0001
IR-VAR-0001
IR-CONFLICT-0001
MI-IR-0001
AQ-IR-0001
W-IR-0001
```

## 32. JSON Schema validation vs business validation

JSON Schema owns local structural validation, including:

- types;
- required fields;
- enums;
- identifier format;
- strict objects;
- basic cardinalities;
- local state combinations.

Business validation owns cross-object and source-integrity rules, including:

- unique logical IDs;
- dangling references;
- evidence existence;
- analysis-path existence;
- document identity coherence;
- evidence locator/excerpt integrity;
- relationship target validity;
- method dependencies;
- embodiment references;
- SAFE_GENERALIZATION semantics;
- PROPOSED_VARIANT filing gate;
- rejection of unauthorized `HUMAN_CONFIRMED`;
- conflict eligibility;
- parameter/range broadening guards;
- Claims-structure exclusion.

The implementation must not force all cross-object semantics into JSON Schema.

## 33. Synthetic fixture corpus

Minimum synthetic fixture coverage:

1. representative system invention;
2. multi-component system;
3. method/process invention;
4. parameter/range-heavy invention;
5. multiple embodiments;
6. table evidence;
7. missing information;
8. conflicting information;
9. valid SAFE_GENERALIZATION;
10. invalid SAFE_GENERALIZATION;
11. proposed variant requiring Human confirmation;
12. prompt-injection-like source content;
13. dangling/cross-reference failure;
14. unsupported range broadening;
15. administrative-data fabrication attempt;
16. Claims leakage attempt.

All fixtures must be synthetic and non-confidential.

## 34. Negative/adversarial requirements

The implementation must fail closed or explicitly block/review at least:

- invented component;
- invented mechanism;
- invented typed relationship;
- unsupported technical effect;
- unsupported parameter/range broadening;
- nonexistent evidence ID;
- mismatched evidence locator;
- non-verbatim/mismatched evidence excerpt;
- dangling element reference;
- dangling method-step reference;
- invalid embodiment reference;
- silently resolved contradiction;
- unauthorized SAFE_GENERALIZATION;
- PROPOSED_VARIANT treated as supported filing content;
- fake HUMAN_CONFIRMED;
- fabricated administrative information;
- Claims content inserted into reconstruction;
- legal/patentability conclusion structure;
- source prompt injection treated as instruction.

## 35. Expected implementation artefacts

Expected new paths:

```text
schemas/invention-reconstruction/v1.0.0/
  invention-reconstruction.schema.json
  README.md

backend/app/services/
  invention_reconstruction.py
  invention_reconstruction_validation.py

tests/fixtures/invention-reconstruction/v1.0.0/
  ...

tests/schema/
  test_invention_reconstruction_v1.py

tests/backend/
  test_invention_reconstruction.py

docs/tasks/
  P2-002-invention-reconstruction.md

docs/decisions/
  ADR-012-invention-reconstruction-boundary.md
```

The implementation may update repository index/workflow/governance documents only when required by existing project conventions.

## 36. Immutable/current artefacts

P2-002 must not overwrite or silently alter semantics of:

- `schemas/invention-output/v1.0.0/*`;
- `schemas/patent-draft/v1.0.0/*`;
- `schemas/uspto-specification/v2.0.0/*`;
- `prompts/extraction/v1.0.0/*`;
- existing draft-generation prompt/runtime;
- existing DOCX v1;
- current frontend workflow;
- `render.yaml`;
- provider/model policy.

P2-002 is additive.

## 37. Runtime, security and data boundaries

Remain unchanged:

- BLK-003: **OPEN**;
- EVAL-001 PRODUCT_RUNTIME: **DEFERRED — AWAITING FUNDING**;
- provider/API authorization: **NOT GRANTED**;
- provider/API budget: **0**;
- paid calls: **PROHIBITED**;
- real/confidential research papers: **NOT AUTHORIZED**;
- Claims runtime: **NOT IMPLEMENTED**;
- production: **NOT APPROVED / NOT PERFORMED**.

No:

- new secrets;
- provider credentials;
- network dependency;
- external database/service;
- browser/retrieval/prior-art search;
- public deployment change.

## 38. Acceptance criteria

| AC | Requirement |
|---|---|
| AC-01 | Versioned strict `INVENTION_RECONSTRUCTION` contract exists |
| AC-02 | P2-002 consumes APP-002 + AI-001 as canonical upstream inputs |
| AC-03 | No duplicated/redefined upstream input semantics |
| AC-04 | Exact document-identity coherence validation |
| AC-05 | Source-evidence integrity validation |
| AC-06 | Technical-problem representation |
| AC-07 | Technical-solution/inventive-concept representation |
| AC-08 | Technical element/component model |
| AC-09 | Essentiality is modeled conservatively |
| AC-10 | Controlled typed relationship model |
| AC-11 | Method/process model |
| AC-12 | Input/output/material/data/signal flow model |
| AC-13 | Parameter/condition/range model |
| AC-14 | Experimental values remain example-scoped unless stronger support exists |
| AC-15 | Technical-effect representation |
| AC-16 | Embodiment reconstruction |
| AC-17 | Variant representation is separate from embodiments |
| AC-18 | Figure/table/source-artifact handling respects current parser limits |
| AC-19 | Material assertions retain evidence-level grounding |
| AC-20 | AI-001 grounding classes are preserved without promotion |
| AC-21 | Deterministic SAFE_GENERALIZATION rule and validation |
| AC-22 | PROPOSED_VARIANT is blocked from automatic filing handoff |
| AC-23 | Initial implementation cannot fabricate HUMAN_CONFIRMED |
| AC-24 | Contradictions are represented or conservatively propagated without silent resolution |
| AC-25 | Missing information and author questions are structured |
| AC-26 | Administrative anti-hallucination boundary is preserved |
| AC-27 | Claims generation and patentability analysis are excluded |
| AC-28 | Explicit P2-003 handoff contract |
| AC-29 | Strict JSON Schema Draft 2020-12 validation |
| AC-30 | Cross-object/source-integrity business validation |
| AC-31 | Repeated identical inputs produce deterministic business output |
| AC-32 | Synthetic and adversarial offline fixture coverage |
| AC-33 | Existing v1/P2-001/runtime/frontend/deployment semantics remain unchanged |
| AC-34 | Zero-provider, zero-real-data, zero-production boundary |

## 39. Implementation verification plan

When implementation is separately authorized, verification must include:

- dedicated P2-002 schema tests;
- dedicated P2-002 business-validator tests;
- dedicated reconstruction service tests;
- current schema regression tests;
- current backend regression tests;
- `python -m pip check`;
- `git diff --check`;
- frontend lint/typecheck/build and existing synthetic browser suites when required by repository CI;
- live-provider flags remain disabled;
- no provider/API calls;
- no real/confidential data.

Final implementation SHA requires independent fixed-SHA review before merge.

## 40. Definition of Done — implementation phase

P2-002 implementation may be marked completed only after all of the following are evidenced:

1. AC-01…AC-34 verified;
2. strict schema and business validation pass;
3. synthetic/adversarial fixtures pass;
4. existing regression suites pass;
5. provider/API calls remain zero;
6. real/confidential data usage remains zero;
7. Claims runtime remains absent;
8. diff remains inside authorized scope;
9. independent Gemini 3.1 Pro High / Antigravity review returns PASS on the exact final implementation SHA;
10. required CI succeeds;
11. merge and post-merge governance closeout complete under AGENTS.md.

## 41. Specification review checklist

The independent reviewer must verify:

- P2-001 compatibility;
- APP-002 / AI-001 input boundary correctness;
- no duplicated upstream contract;
- grounding rigor;
- evidence integrity rules;
- no inference promotion;
- SAFE_GENERALIZATION semantics are deterministic and narrow;
- proposed-variant/Human-confirmation gating;
- conservative contradiction handling;
- conservative essentiality handling;
- parameter/range anti-broadening;
- Claims exclusion;
- P2-003 handoff sufficiency;
- implementation feasibility;
- offline determinism;
- synthetic testability;
- v1 immutability;
- provider/data/security/production boundaries;
- AC-01…AC-34 completeness.

## 42. Specification gate

This specification does **not** authorize implementation.

Required next gate:

```text
Fixed specification SHA
→ Gemini 3.1 Pro High / Antigravity read-only review
→ PASS / no blocking findings
→ Human authorization for P2-002 implementation
→ Codex implementation
```

No implementation file may be created solely because this specification exists.
