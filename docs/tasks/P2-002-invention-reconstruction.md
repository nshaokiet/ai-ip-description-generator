# P2-002 — Invention Reconstruction Contract & Offline Reconstruction Pipeline

## Metadata

| Field | Value |
|---|---|
| Task ID | P2-002 |
| Title | Invention Reconstruction Contract & Offline Reconstruction Pipeline |
| Specification version | 0.1.0 (reviewed semantics unchanged) |
| Implementation evidence revision | 0.2.0 |
| Governance evidence revision | 0.2.2 — 04/10/2026 |
| Status | **CLOSED / COMPLETED — MERGED** |
| Governance closeout gate | **CLOSED** — Human-supplied Gemini 3.1 Pro High / Antigravity fixed-SHA PASS, findings NONE, 25/25 checklist PASS; reviewer modified tracked files NO |
| Reviewed closeout SHA | `5ec0157cb5c60674421dc75b4ae90c88659524e2` |
| Governance closeout merge | PR #72 — `ba8062f1c7db1506af10fdd2193ed193d31cd72d` |
| Final closeout main CI | `37168633773` — SUCCESS on the closeout merge SHA |
| Human authorization | `HUMAN-P2-002-INVENTION-RECONSTRUCTION-2026-10-03` |
| Human implementation authorization | `HUMAN-P2-002-IMPLEMENTATION-2026-10-03` |
| Authorized baseline | `054410f937eaaecf7b462855b7dce921e40e8924` |
| Implementation baseline | `e87b51987c42edb1432a9612a4e05bc7c0d9b113` |
| Reviewed specification SHA | `9c3f5e67f3c3af73807aab3f3ba84300fcd99c07` — PASS, findings NONE, 34/34 requirements PASS |
| Specification merge | PR #70 — `e87b51987c42edb1432a9612a4e05bc7c0d9b113` |
| Reviewed implementation SHA | `62a43da07fc4ccd60c9dab0da188388f6cab88e2` — Human-supplied Gemini 3.1 Pro High / Antigravity PASS, findings NONE, AC-01…AC-34 PASS; reviewer modified tracked files NO; merge suitability YES |
| Implementation merge | PR #71 — `7d295165379dfa3aa16cd305eb73e7ee739f5f03` |
| Implementation PR CI | `37133351078` — SUCCESS |
| Post-merge push/main CI | `37135175570` — SUCCESS on the implementation merge SHA |
| Implementation branch | `feat/p2-002-invention-reconstruction` |
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

The specification gate was satisfied by reviewed specification SHA `9c3f5e67f3c3af73807aab3f3ba84300fcd99c07` and Human implementation authorization `HUMAN-P2-002-IMPLEMENTATION-2026-10-03`. The reviewed specification semantics remain unchanged.

## 43. Implementation evidence — 03/10/2026

Implemented additive artefacts:

- `schemas/invention-reconstruction/v1.0.0/invention-reconstruction.schema.json`;
- `schemas/invention-reconstruction/v1.0.0/README.md`;
- `backend/app/services/invention_reconstruction.py`;
- `backend/app/services/invention_reconstruction_validation.py`;
- `tests/schema/test_invention_reconstruction_v1.py`;
- `tests/backend/test_invention_reconstruction.py`;
- 16 synthetic fixture categories under `tests/fixtures/invention-reconstruction/v1.0.0/`;
- `docs/decisions/ADR-012-invention-reconstruction-boundary.md`.

The service consumes the existing APP-002 `ExtractionInputEnvelope` model plus a canonical-schema/business-validated AI-001 payload. It performs exact document/evidence coherence checks before deterministic reconstruction and then applies separate Draft 2020-12 schema and cross-object/source-integrity validation.

Initial adapter behavior is deliberately conservative: element type `OTHER`; essentiality `UNKNOWN`; AI-001 related components map only to `RELATED_TO`; method sequence creates no dependency; process input/output flow is `UNSPECIFIED`; experimental values remain `EXAMPLE_ONLY`; variants remain empty; `HUMAN_CONFIRMED` and `HUMAN_RESOLVED` are rejected without a future audited input path.

### Recovery and remediation

Resumed the existing `feat/p2-002-invention-reconstruction` worktree without
reset, restore, cleanup of implementation files or history rewrite. Starting
HEAD and fetched `origin/main` were both
`e87b51987c42edb1432a9612a4e05bc7c0d9b113`; no earlier implementation commits
existed. Recovery found 4 tracked modified files and 23 new P2-002 files, plus a
generated frontend TypeScript incremental cache (excluded and later removed).
Unrelated files in the main worktree were preserved and not staged.

Remediation closed incomplete fixture execution and validation gaps: full
projection comparison (including scalar types, units, scope, descriptions and
precise upstream references), revalidation of constructed envelope instances,
deep-copy isolation of evidence, safe pointer parsing and iterative dependency
cycle detection, drawing/figure traceability and grounded candidate warnings.
SG-01 permits only explicit source-category substitution, not structural,
numerical or semantic additions. Supplied proposed variants can be validated
only in explicit review-candidate mode and are mechanically filing-ineligible;
the adapter still generates none. Semantic entailment is not claimed.

### Local verification (Python 3.12.10, offline)

| Check | Evidence / outcome |
|---|---|
| Targeted P2-002 schema | 23 passed |
| Targeted P2-002 backend | 85 passed |
| Combined targeted run | 108 passed, exit 0 |
| Full schema regression | 57 passed, exit 0 |
| Full backend regression | 396 passed, 2 skipped, exit 0 |
| Entire Python test suite | 574 passed, 3 skipped, exit 0 |
| pip check | No broken requirements found, exit 0 |
| git diff --check | PASS; staged diff checked again before commit |
| Frontend lint / typecheck | PASS / PASS, exit 0; existing completed evidence retained because no frontend files changed |
| Frontend production build | PASS, exit 0 (standard and Render/static builds) |
| Standard synthetic Playwright | Controlled external-server run: 26 passed, runner exit 0 |
| Render/demo synthetic Playwright | 5 passed, exit 0; existing completed evidence retained because no frontend/static code changed |

The full-suite skips are two gated live-provider tests (flags 0/0) and one
Windows-specific upload permission test. Backend-only skips are one gated
draft-provider test and that Windows permission test. One existing
Starlette/AnyIO deprecation warning remains. No skipped case is a P2-002 failure.

The interrupted standard browser command printed 26 successful cases but was
stopped during Windows server teardown, so it was **not** treated as clean final
verification. Recovery found no remaining task server process. The first
external-server retry failed 4 DOCX inspection cases because the worktree's
default Python path did not exist; setting `PLAYWRIGHT_PYTHON` to the existing
project Python 3.12 environment resolved that environment error. The final run
used `P1_005_EXTERNAL_SERVERS=1`, achieved 26/26 and exit 0, and its two explicitly
owned server sessions were stopped afterward. A process/port check confirmed no
task servers or listeners on 8000/3106/8001/3107 remained. No product configuration
or test source was changed to work around Windows teardown.

### AC traceability — historical implementation self-check before independent review

`S` denotes `tests/schema/test_invention_reconstruction_v1.py`; `B` denotes
`tests/backend/test_invention_reconstruction.py`. These are local self-checks,
not an independent reviewer decision or task closeout.

| AC | Evidence | Self-check |
|---|---|---|
| AC-01 | Versioned strict schema; S canonical path/root identity tests | VERIFIED |
| AC-02 | Existing APP-002 model + canonical AI-001 validation in producer | VERIFIED |
| AC-03 | No replacement upstream contract; S upstream-not-redefined test | VERIFIED |
| AC-04 | B four identity mismatch cases and optional-SHA test | VERIFIED |
| AC-05 | B ID/type/locator/excerpt integrity rejection cases | VERIFIED |
| AC-06 | B conservative problem mapping | VERIFIED |
| AC-07 | B solution/problem references and invented-mechanism rejection | VERIFIED |
| AC-08 | B deterministic two-element model; executable multi-component fixture | VERIFIED |
| AC-09 | UNKNOWN default and changed-essentiality rejection | VERIFIED |
| AC-10 | RELATED_TO/input/output-only mapping and typed-relation rejection | VERIFIED |
| AC-11 | Two-step fixture; sequence preservation; dangling/cyclic dependencies | VERIFIED |
| AC-12 | UNSPECIFIED flows; exact source/target/description projection | VERIFIED |
| AC-13 | Exclusive EXACT/RANGE/SET/QUALITATIVE schema; parameter-heavy fixture | VERIFIED |
| AC-14 | EXAMPLE_ONLY; changed scalar/unit/role/scope and broad-range rejection | VERIFIED |
| AC-15 | SOURCE_REPORTED vs INFERENCE consequence tests; effect rejection | VERIFIED |
| AC-16 | Explicit/inferred separate embodiments; invalid refs/description rejected | VERIFIED |
| AC-17 | Separate variant collection; producer emits none; contract fixture | VERIFIED |
| AC-18 | TABLE fixture; text figure test; drawing ID/kind/status/path preservation | VERIFIED |
| AC-19 | Per-assertion evidence/paths, including conditions and candidate warnings | VERIFIED |
| AC-20 | Non-promotion test; INFERENCE effect/embodiment preservation | VERIFIED |
| AC-21 | Executed valid literal-category and invalid-category SG-01 fixtures | VERIFIED |
| AC-22 | Proposed fixture requires confirmation and filing_content_eligible=false | VERIFIED |
| AC-23 | Fake HUMAN_CONFIRMED rejected; no audit input or generated confirmation | VERIFIED |
| AC-24 | CONFLICTING fixture propagated as gap; unaudited resolution rejected | VERIFIED |
| AC-25 | Missing/question linkage fixture and exact-content projection tests | VERIFIED |
| AC-26 | Administrative schema rejection cases and strict all-object test | VERIFIED |
| AC-27 | Claims/schema/legal-phrase rejection; root notice constants | VERIFIED |
| AC-28 | Contract README future P2-003 handoff and filing/review eligibility | VERIFIED |
| AC-29 | Draft 2020-12 self-validation, strict objects, constants/local states | VERIFIED |
| AC-30 | Source/support/ref/unique-ID validation and complete projection guard | VERIFIED |
| AC-31 | Determinism/input-isolation tests and repeat generation in every fixture | VERIFIED |
| AC-32 | All 16 JSON cases executed; adversarial safe failure codes asserted | VERIFIED |
| AC-33 | Baseline diff leaves released schema/prompt/runtime/DOCX/frontend/deployment unchanged; regressions PASS | VERIFIED |
| AC-34 | Offline socket-disabled test, synthetic fixtures, flags 0/0, no endpoints/providers/deployment | VERIFIED |

### Version/change record

| Previous | New | Date | Author | Change / reason | Reference | Breaking |
|---|---|---|---|---|---|---|
| Specification 0.1.0 | Specification 0.1.0 + implementation evidence 0.2.0 | 03/10/2026 | Codex | Implement reviewed additive reconstruction contract and record resume/test evidence | HUMAN-P2-002-IMPLEMENTATION-2026-10-03 | No — reviewed semantics and released contracts unchanged |
| Implementation evidence 0.2.0 | Governance evidence 0.2.1; specification 0.1.0 and contract 1.0.0 unchanged | 04/10/2026 | Codex | Reconcile Human-supplied independent PASS, specification/implementation merges and verified CI; propose final task status with closeout review/merge still pending | Human P2-002 governance closeout instruction; PR #70/#71; main CI `37135175570` | No |
| Governance evidence 0.2.1 | Governance evidence 0.2.2; specification 0.1.0 and contract 1.0.0 unchanged | 04/10/2026 | Codex | Finalize stale proposed/pending closeout status from existing PASS, PR #72 merge and successful final main CI | HUMAN-P2-002-FINAL-GOVERNANCE-STATUS-RECONCILIATION-2026-10-04; CI `37168633773` | No |

### Historical fixed-SHA implementation handoff gate — satisfied

At the implementation handoff, review and merge were pending. Human subsequently
supplied Gemini 3.1 Pro High / Antigravity independent **PASS**, findings **NONE**,
AC-01…AC-34 **PASS** on exact final SHA
`62a43da07fc4ccd60c9dab0da188388f6cab88e2`; reviewer modified tracked files **NO**,
merge suitability **YES**. This is external review evidence supplied by Human,
not a GitHub API approval or a Codex self-review. The historical self-checks
above remain self-checks; they are not rewritten as reviewer findings.

PR [#71](https://github.com/nshaokiet/ai-ip-description-generator/pull/71) merged
at `7d295165379dfa3aa16cd305eb73e7ee739f5f03` after PR CI
[`37133351078`](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/37133351078)
**SUCCESS** on the reviewed SHA. Post-merge push/main CI
[`37135175570`](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/37135175570)
is **SUCCESS** on that merge. All 29 implementation files exist on main; the
merge tree equals the reviewed implementation tree. The merge handoff is
[recorded on PR #71](https://github.com/nshaokiet/ai-ip-description-generator/pull/71#issuecomment-5970905119).

Project Orchestrator returned `Unknown task: P2-002`; claim/progress lifecycle state is therefore **BLOCKED BY TOOL CAPABILITY**. Git/task/test evidence remains authoritative and no MCP approval, lease, or state is fabricated.

Provider/API calls: **NONE**. Real/confidential data: **NONE**. Claims implementation: **NO**. Production/deployment change: **NO**. BLK-003 remains **OPEN** and EVAL-001 PRODUCT_RUNTIME remains **DEFERRED — AWAITING FUNDING**.

## 44. Final governance closeout evidence — 04/10/2026

P2-002 is **CLOSED / COMPLETED — MERGED**. Human supplied Gemini 3.1 Pro High /
Antigravity closeout review **PASS**, findings **NONE**, checklist **25/25 PASS**
on `5ec0157cb5c60674421dc75b4ae90c88659524e2`; reviewer modified tracked files
**NO**. Closeout PR CI `37163143518` **SUCCESS**. PR #72 merged at
`ba8062f1c7db1506af10fdd2193ed193d31cd72d`; final closeout push/main CI
[`37168633773`](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/37168633773)
**SUCCESS** on that exact merge. The earlier pending proposal state is historical
and superseded by this final evidence and the
[PR #72 handoff](https://github.com/nshaokiet/ai-ip-description-generator/pull/72#issuecomment-5975495162).

Specification authorization: `HUMAN-P2-002-INVENTION-RECONSTRUCTION-2026-10-03`.
Implementation authorization: `HUMAN-P2-002-IMPLEMENTATION-2026-10-03`.
Human supplied specification review **PASS / NONE / 34 of 34 PASS** on
`9c3f5e67f3c3af73807aab3f3ba84300fcd99c07`; PR #70 merged at
`e87b51987c42edb1432a9612a4e05bc7c0d9b113`.

The original closeout branch started from exact implementation merge
`7d295165379dfa3aa16cd305eb73e7ee739f5f03`. At that handoff, divergent root local
main (ahead 2 / behind 46) and existing untracked files were preserved without
reset, cleanup or history rewrite. Only documentation/status evidence was reconciled.
`docs/workflow.md` was inspected and left unchanged: its P2-002 section describes
the offline boundary without stale P2-002 review-pending wording.

**MCP TOOL LIMITATION:** Project Orchestrator returns `Unknown task: P2-002`;
lifecycle/lease/checkpoint is **BLOCKED BY TOOL CAPABILITY**, not a fabricated
MCP task state. Git review/merge/CI evidence records completion without inventing
MCP completion.

Preserved boundaries: BLK-003 **OPEN**; PRODUCT_RUNTIME **DEFERRED — AWAITING
FUNDING**; semantic acceptance **NOT DETERMINED**; provider authorization
**NOT GRANTED**, budget **0**, calls **NONE**; real/confidential data **NONE /
NOT AUTHORIZED**; arbitrary real-paper AI conversion **NOT ENABLED**; Claims
runtime **NOT IMPLEMENTED**; production **NOT APPROVED / NOT PERFORMED**;
deployment change **NO**. P2-003 and P2-004 are **NOT AUTHORIZED BY THIS CLOSEOUT**.

Human authorization
`HUMAN-P2-002-FINAL-GOVERNANCE-STATUS-RECONCILIATION-2026-10-04` permits only
this final documentation evidence sync. Additional independent review is waived
only for this bounded status reconciliation if evidence/scope remain correct
and PR CI passes; no technical/policy change or future task is authorized.
**STOP. Do not start P2-003 or P2-004.**
