# P2-003 — USPTO Specification Generation Contract & Offline Generation Pipeline v2

## Metadata

| Field | Value |
|---|---|
| Task ID | P2-003 |
| Title | USPTO Specification Generation Contract & Offline Generation Pipeline v2 |
| Specification version | 0.1.1 — semantic amendment for explicit source-document provenance |
| Governance evidence revision | 0.1.3 — 04/10/2026; merged amendment and implementation handoff evidence, specification semantics unchanged |
| Status | **SPECIFICATION 0.1.1 APPROVED / MERGED; IMPLEMENTED — INDEPENDENT IMPLEMENTATION REVIEW PENDING** |
| Amendment review | Human-supplied external Gemini 3.1 Pro High / Antigravity fixed-SHA PASS / findings NONE / AC-01…AC-41 PASS / A–H PASS; not GitHub-native review evidence |
| Reviewed amendment SHA | `1a17c87a6c42087965b7ac3fa88ae0fc17f26a4e` |
| Amendment PR / merge / implementation baseline | PR #76 — `26d21feff592ff73574071887148630d44018b41` |
| Amendment PR / post-merge main CI | `37182596336` / `37184343482` — SUCCESS on their exact respective SHAs |
| Contract blocker | **RESOLVED** by merged specification 0.1.1 |
| Independent implementation review | **PENDING** — AC-40 is not self-approved |
| Historical specification 0.1.0 review | Human-supplied external Gemini 3.1 Pro High / Antigravity fixed-SHA PASS / findings NONE / AC-01…AC-40 PASS; not GitHub-native review evidence; does not approve 0.1.1 |
| Historical 0.1.0 reviewed specification SHA | `a22440f1667388ece08868cbf0f2e22805449eef` |
| Historical 0.1.0 specification PR / merge | PR #74 — `af0948dab4f0e13e026ad7f6cdbd4ac9691a77a8` |
| Historical 0.1.0 specification PR CI | `37174156757` — SUCCESS on the reviewed SHA |
| Historical 0.1.0 specification post-merge main CI | `37175416694` — SUCCESS on the specification merge SHA |
| Implementation authorization | **GRANTED** — `HUMAN-P2-003-IMPLEMENTATION-2026-10-04` |
| Implementation execution | **RESUMED / IMPLEMENTED — INDEPENDENT IMPLEMENTATION REVIEW PENDING**; existing authorization remains granted |
| Amendment authorization / baseline | `HUMAN-P2-003-SPECIFICATION-AMENDMENT-0.1.1-2026-10-04`; `e74715f07a2c4c27c63369d8415a7964d02df4e2` |
| P2-004 | **NOT AUTHORIZED** |
| Historical governance reconciliation authorization | `HUMAN-P2-003-SPECIFICATION-GOVERNANCE-RECONCILIATION-2026-10-04` — bounded docs-only evidence sync |
| Original specification authorization | `HUMAN-P2-003-SPECIFICATION-2026-10-04` |
| Authorization scope | Current task: deterministic offline implementation and status/evidence sync in the same implementation PR; do not merge or start P2-004 |
| Historical 0.1.0 authorized baseline | `edf2239dd78258881a75c7e2406bd6041d62cce6` |
| Input contract | P2-002 `INVENTION_RECONSTRUCTION` v1.0.0 |
| Output target contract | P2-001 `USPTO_SPECIFICATION_DRAFT` v2.0.0 |
| Owner | Human / Product Owner; Codex implementation; ChatGPT technical coordination |
| Implementation owner | Codex under existing granted implementation authorization; independent implementation review pending |
| Independent reviewer | Gemini 3.1 Pro High / Antigravity read-only |
| Provider/API calls | **NONE / NOT AUTHORIZED** |
| Real/confidential research data | **NOT AUTHORIZED** |
| Claims generation | **OUT OF SCOPE / P2-004** |
| Production/deployment | **NOT APPROVED / NOT PERFORMED** |
| BLK-003 | **OPEN** |
| EVAL-001 PRODUCT_RUNTIME | **DEFERRED — AWAITING FUNDING** |
| Semantic acceptance | **NOT DETERMINED** |

## 1. Purpose

P2-003 defines the contract and deterministic offline generation rules that transform one **validated P2-002 Invention Reconstruction v1.0.0** payload into one **P2-001 USPTO Specification Draft v2.0.0** payload.

Target flow:

```text
Scientific Paper
  → APP-002 Parsed Source Units / Evidence
  → AI-001 Structured Invention Analysis v1
  → P2-002 INVENTION_RECONSTRUCTION v1.0.0
  → P2-003 USPTO_SPECIFICATION_DRAFT v2.0.0
  → P2-004 Claims / Support Audit
  → later DOCX v2 + Review Package
```

P2-003 is the **drafting layer**, not a second invention-discovery layer. It must consume the validated reconstruction and convert eligible supported technical content into filing-style patent-specification prose without reinterpreting the raw paper from scratch.

The initial P2-003 runtime is intended to be **offline and deterministic**. It does not claim the semantic quality of a provider-assisted patent drafter and does not establish filing readiness, patentability, novelty, inventorship, validity, infringement, or legal sufficiency.

## 2. Authoritative upstream contracts

### 2.1 P2-002 — canonical technical source

The sole technical drafting authority for P2-003 is a validated:

```text
INVENTION_RECONSTRUCTION
schema_version = 1.0.0
```

P2-003 may consume:

- document metadata;
- title candidates;
- technical field;
- technical context;
- technical problems;
- solution concepts;
- elements;
- relationships;
- method steps;
- flows;
- parameters;
- technical effects;
- embodiments;
- eligible variants;
- source-artifact references;
- support / grounding metadata;
- evidence;
- conflicts;
- missing information;
- author questions;
- warnings.

P2-003 must not silently bypass P2-002 by using APP-002 or AI-001 as a second semantic source.

APP-002 / AI-001 evidence remains indirectly authoritative through P2-002 support and evidence closure, but P2-003 source paths are rooted in the P2-002 reconstruction payload.

### 2.2 P2-001 — canonical output target

P2-003 targets the already released:

```text
schemas/uspto-specification/v2.0.0/uspto-specification.schema.json
schema_version = "2.0.0"
output_type = "USPTO_SPECIFICATION_DRAFT"
```

P2-003 must **not fork or redefine** the P2-001 target schema.

If implementation discovers that the released P2-001 schema cannot express a required reviewed P2-003 behavior, implementation must stop and report a contract blocker rather than silently mutate P2-001 semantics.

## 3. Input service boundary

Recommended future service boundary:

```python
generate_uspto_specification(
    reconstruction: dict,
    generation_config: dict,
) -> dict
```

The implementation must validate the reconstruction against P2-002 v1.0.0 before generation.

No duplicate canonical input schema is required. `generation_config` is a narrow caller-controlled configuration object, not a replacement technical-data contract.

### 3.1 Generation configuration

The initial configuration contains only narrow deterministic drafting controls
and the explicit caller-supplied source-document provenance assertion:

```json
{
  "language": "en",
  "selected_title_candidate_id": "optional-existing-id",
  "abstract_max_words": 150,
  "include_claims": false,
  "target_jurisdiction": "US",
  "source_document_synthetic": true
}
```

Rules:

- `language` must be `en`;
- `abstract_max_words` must be 150;
- `include_claims` must be false;
- `target_jurisdiction` must be `US`;
- `selected_title_candidate_id`, when present, must reference an existing P2-002 title candidate;
- `selected_title_candidate_id` remains optional;
- `source_document_synthetic` is **REQUIRED** and must be a boolean, not a
  string, number, null, or truthy/coerced value;
- there is **no default, inference, fallback, or derivation** from file name,
  media type, SHA, document ID, test environment, branch, fixture path, caller
  identity, or source text;
- absent provenance fails closed before generation with
  `SOURCE_DOCUMENT_PROVENANCE_REQUIRED`; a non-boolean value fails configuration
  validation;
- no configuration field may authorize provider calls, real-data use, Claims, legal conclusions, filing readiness, or production behavior.

### 3.2 Explicit provenance and current authorization gate

`generation_config.source_document_synthetic` means **the caller asserts whether
this source document is synthetic**. It maps exactly to
`output.document_metadata.source_document.synthetic`; copy the supplied value,
never invent it. Provenance and authorization are separate concepts. The field
does not grant permission to process real/confidential data, provider access,
production use, confidentiality clearance, semantic acceptance, or filing readiness.

For the currently authorized deterministic offline P2-003 implementation:

- `true` is permitted by this provenance gate, subject to all other validation;
- `false` **MUST FAIL CLOSED before specification generation** with
  `REAL_SOURCE_NOT_AUTHORIZED`; never ignore it or convert it to `true`.

P2-001 intentionally permits `synthetic=false` as representational capability
for a future separately authorized real-data runtime. This amendment does not
activate it. Accepting `source_document_synthetic=false` later requires separate
Human authorization covering real-data/runtime/security requirements; no future
task is pre-authorized here. P2-001 and P2-002 schemas remain unchanged.

The caller assertion is not cryptographic proof that a document is synthetic.
The gate refuses explicit real-source provenance; it does not verify the truth
of the caller's assertion. Do not scan document text to infer provenance.
Strings such as "This is synthetic" or "This is a real research paper" remain
untrusted DATA and cannot supply, override, or change the configuration value.

## 4. Output identity

The output must validate against P2-001 v2.0.0 and use exactly:

```text
schema_version = "2.0.0"
output_type = "USPTO_SPECIFICATION_DRAFT"
language = "en"
target_jurisdiction = "US"
specification_kind = "NONPROVISIONAL_UTILITY_PATENT_SPECIFICATION_DRAFT"
```

The output remains a Human/IP-specialist review draft.

### 4.1 Deterministic draft ID

The future implementation should derive `document_metadata.draft_id` deterministically from source-document identity using Python standard-library hashing.

Recommended rule:

```text
draft_id = "p2-003-" + first_24_hex(
    SHA256(document_id + "|" + file_name + "|" + source_sha256_or_empty)
)
```

No random UUID, provider request ID, wall-clock timestamp, or environment-specific identifier may affect the business payload.

`source_document_synthetic` is deterministic caller input. Identical validated
reconstruction plus generation configuration must still produce identical output.
Do **not** include the provenance boolean in `draft_id`; the reviewed identity
material remains document ID + file name + source SHA-256 or empty, unchanged.

### 4.2 Exact source-document mapping

| Output under `document_metadata.source_document` | Sole input authority |
|---|---|
| `document_id` | `reconstruction.document_metadata.document_id` |
| `file_name` | `reconstruction.document_metadata.file_name` |
| `media_type` | `reconstruction.document_metadata.media_type` |
| `sha256` | `reconstruction.document_metadata.sha256`, copied only when present; otherwise omitted |
| `synthetic` | Required boolean `generation_config.source_document_synthetic`, copied exactly after the authorization gate |

No other source-document provenance field may be fabricated. Do not add
`synthetic` to P2-002 or share mutable nested state with the reconstruction.

## 5. Patent-content format policy

P2-003 follows the **content structure and drafting organization** of a USPTO-style nonprovisional utility patent specification.

It does **not** attempt to reproduce the front page of an issued patent.

### 5.1 No INID / front-page bibliographic-number rendering

P2-003 must not generate or render WIPO/USPTO bibliographic labels or issued-document front-page codes such as:

- `(10)`;
- `(21)`;
- `(22)`;
- `(43)`;
- `(45)`;
- `(54)`;
- `(57)`;
- `(71)`;
- `(72)`;
- `(73)`;
- `(74)`.

It must also not invent:

- patent number;
- patent application number;
- publication number;
- publication kind code such as A1/B1/B2;
- filing receipt identifiers;
- examiner;
- art unit;
- classification code;
- issue date;
- publication date.

The section heading remains plain filing-style content, for example:

```text
TITLE OF THE INVENTION
ABSTRACT OF THE DISCLOSURE
```

not:

```text
(54) TITLE OF THE INVENTION
(57) ABSTRACT
```

This task targets **USPTO-style specification content**, not an issued-patent facsimile.

## 6. Canonical output order

P2-003 preserves the P2-001 canonical order:

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

P2-003 does not reorder or rename these canonical target sections.

## 7. Filing-content eligibility model

Only validated P2-002 content with eligible support may enter filing-style prose.

### 7.1 Eligible grounding classes

Potentially eligible:

- `SOURCE_FACT`;
- `PARAPHRASE`;
- `INFERENCE`;
- validated `SAFE_GENERALIZATION`.

Eligibility does not imply legal sufficiency or filing readiness.

### 7.2 Ineligible grounding / review states

The initial P2-003 pipeline must not place the following into filing-style prose:

- `PROPOSED_VARIANT`;
- `MISSING`;
- unaudited `HUMAN_CONFIRMED`;
- entities affected by unresolved conflicts;
- unsupported warnings;
- content whose support/evidence closure fails.

P2-003 must never silently promote these states.

### 7.3 Grounding aggregation for generated paragraphs

A generated paragraph may combine multiple eligible P2-002 source entities only when the resulting text adds no unsupported proposition.

The output paragraph grounding class is the most conservative class present in its source set, using this deterministic precedence:

```text
SOURCE_FACT
  < PARAPHRASE
  < INFERENCE
  < SAFE_GENERALIZATION
```

Examples:

- SOURCE_FACT + SOURCE_FACT → SOURCE_FACT;
- SOURCE_FACT + PARAPHRASE → PARAPHRASE;
- PARAPHRASE + INFERENCE → INFERENCE;
- any eligible set containing SAFE_GENERALIZATION → SAFE_GENERALIZATION.

This rule must never upgrade INFERENCE to PARAPHRASE or SOURCE_FACT.

## 8. Source-path and evidence closure

Every filing-style technical paragraph must contain support that points back to P2-002.

Rules:

1. each `source_path` must be a valid JSON Pointer into the P2-002 reconstruction;
2. every referenced reconstruction entity must exist;
3. every output evidence ID must exist in P2-002 `review_package.evidence`;
4. output evidence IDs preserve the same source evidence IDs;
5. no synthetic evidence ID may be invented to justify technical content;
6. used evidence is copied into the P2-001 `review_package.evidence` as `SOURCE_DOCUMENT` evidence;
7. unused P2-002 evidence need not be copied;
8. support paths must reference the reconstruction, not raw APP-002 / AI-001 paths as the primary P2-003 source.

P2-003 may preserve original P2-002 analysis provenance indirectly through the reconstruction but must not reconstruct a second competing source-path system.

## 9. Title generation

P2-003 must not invent or semantically optimize a title.

Rules:

1. if `selected_title_candidate_id` is supplied and valid, use that exact candidate title;
2. if no selection is supplied and exactly one eligible candidate exists, use that candidate;
3. if multiple eligible candidates exist and no selection is supplied, title status becomes `HUMAN_CONFIRMATION_REQUIRED`;
4. if no eligible candidate exists, title status becomes `MISSING`;
5. do not merge, rewrite, broaden, shorten, or rank title candidates in the initial offline implementation.

The title section must use plain section content without an INID prefix.

## 10. Administrative sections

The following sections require facts that P2-002 is explicitly prohibited from inventing:

- cross-reference to related applications;
- federally sponsored research/development;
- joint research agreement parties;
- incorporation by reference;
- prior disclosures.

The initial P2-003 input has no canonical Human administrative-data contract and no authorized external-source path.

Therefore the initial deterministic P2-003 runtime must **not emit these sections as PRESENT**.

It must also not mark them `NOT_APPLICABLE` merely because the scientific paper is silent.

Default initial state:

```text
HUMAN_CONFIRMATION_REQUIRED
```

with linked missing-information records in the review package.

A later audited Human-metadata task may supply supported administrative content or a reviewed deterministic non-applicability rule.

## 11. Background of the Invention

### 11.1 Field of the Invention

Primary source:

```text
/invention_model/technical_field
```

Generation rules:

- preserve the technical domain;
- use concise filing-style English;
- do not add new use cases;
- do not add patent classification;
- do not claim novelty;
- do not mention inventors, applicant, patent number, or prosecution state.

If no eligible technical-field content exists, the subsection is `MISSING`.

### 11.2 Description of Related Art

Primary source:

```text
/invention_model/technical_context
/review_package warnings and missing information as exclusion signals
```

Generation rules:

- only describe technical context represented in the reconstruction;
- scientific literature references are context, not a patent prior-art search;
- do not state that a reference anticipates, renders obvious, teaches away, or establishes patentability;
- do not turn the absence of a feature in a paper into a legal distinction;
- do not use unsupported language such as “no existing system,” “all prior systems,” or “state of the art fails” unless the reconstructed source directly supports the exact technical statement and the phrasing remains non-legal.

If no eligible context exists, the subsection is `MISSING`.

## 12. Brief Summary of the Invention

Primary eligible sources:

- problems;
- solution concepts;
- technical effects;
- supported elements;
- supported method steps;
- supported embodiments when necessary for clarity.

The summary must describe the disclosed technical solution without drafting Claims.

Rules:

- at least one eligible solution concept is required for a PRESENT summary;
- problem statements may be included only when supported;
- technical effects may be included only when eligible;
- essentiality must not be strengthened;
- optional/conditional/unknown features must not be rewritten as mandatory;
- “the invention requires,” “must,” or equivalent mandatory phrasing is prohibited unless the reconstruction expressly establishes that limitation;
- no novelty, inventive-step, non-obviousness, patentability, grantability, or “distinguishing over prior art” conclusion may be generated.

## 13. Brief Description of the Drawings

P2-003 may use P2-002 source artifacts only within the parser/vision boundary.

P2-002 does not understand image pixels and does not generate patent drawings.

Therefore P2-003 may draft a PRESENT drawing description only when validated P2-002 content provides enough textual support for a meaningful drawing description without image inference.

Allowed source-artifact categories:

- `FIGURE_REFERENCE`;
- source-supported `DRAWING_REQUIREMENT`;
- table references only when relevant to the description and not presented as a drawing.

Rules:

- do not infer visual geometry from a figure identifier;
- do not infer components visible in an image;
- do not perform OCR or vision;
- do not invent a figure caption from an opaque ID;
- source figure identifiers may be mapped deterministically to filing-style labels `FIG. 1`, `FIG. 2`, etc. only when the underlying figure is eligible for inclusion;
- generated `FIG. n` labels are document-internal drawing labels, not USPTO INID codes;
- reference numerals must remain empty unless a later authorized drawing/reference-numeral task supplies supported mappings.

If source artifacts exist but their textual description is insufficient, the section becomes `HUMAN_CONFIRMATION_REQUIRED` and a review warning records the source references that require Human drafting.

## 14. Detailed Description of the Invention

The Detailed Description is generated from the validated technical reconstruction, not from raw-paper sections.

Eligible sources include:

- elements;
- relationships;
- method steps;
- flows;
- parameters;
- technical effects;
- embodiments;
- eligible source-supported variants;
- eligible source artifacts.

### 14.1 Recommended deterministic paragraph order

The initial offline generator should use a stable order:

1. overview / disclosed technical arrangement;
2. technical elements;
3. relationships / connectivity;
4. flows;
5. method/process steps;
6. parameters and operating conditions;
7. embodiments;
8. effects/results tied to supported conditions;
9. eligible source-supported variants, when any.

The order is deterministic and does not establish legal claim hierarchy.

### 14.2 Element wording

Element prose must preserve:

- element name;
- type where useful;
- supported description;
- essentiality classification.

Rules:

- `UNKNOWN` essentiality must not become mandatory language;
- `OPTIONAL` must remain optional;
- `CONDITIONAL` must retain its condition;
- `ESSENTIAL` may be described as required only if that state itself is validly supported.

### 14.3 Relationship wording

Relationship prose must preserve the exact controlled P2-002 relationship type.

Do not upgrade:

```text
RELATED_TO → CONNECTED_TO / CONTROLS / COUPLED_TO / etc.
```

unless the reconstruction already contains the stronger relation.

### 14.4 Method wording

Method steps must preserve:

- sequence_index;
- action;
- inputs;
- outputs;
- dependencies;
- conditions.

Sequence does not imply causal dependency unless `dependency_step_ids` supports it.

Do not invent branches, prerequisites, feedback loops, or ordering not represented in P2-002.

### 14.5 Flow wording

Flow type remains exactly one of:

- MATERIAL;
- SIGNAL;
- DATA;
- ENERGY;
- CONTROL;
- UNSPECIFIED.

`UNSPECIFIED` must not be upgraded based on drafting intuition.

### 14.6 Parameters and ranges

Parameter drafting must preserve:

- value kind;
- exact value / bounds / set / qualitative value;
- unit;
- role;
- scope status.

Rules:

- never broaden a range;
- never convert an example value into a supported invention-wide limit;
- `EXAMPLE_ONLY` must be drafted using example-scoped language;
- `UNKNOWN_SCOPE` must not be framed as mandatory or preferred;
- `SUPPORTED_RANGE` may be stated only with the exact supported bounds.

Examples of prohibited transformations:

```text
5–10 μm → 1–20 μm
10 V example → preferably about 10 V
single tested value → mandatory operating value
```

### 14.7 Embodiments

Eligible embodiment states:

- `EXPLICIT`;
- `SYNTHESIZED` with eligible grounding.

`PROPOSED_REQUIRES_HUMAN_CONFIRMATION` is not filing-content eligible.

The generator may use patent-style transitional wording such as “In one embodiment” only when the underlying P2-002 embodiment is eligible.

### 14.8 Variants

Only variants with all of the following may enter filing prose:

- `status = SOURCE_SUPPORTED`;
- `filing_content_eligible = true`;
- eligible grounding;
- no unresolved conflict.

The current deterministic P2-002 producer normally emits no variants, so the P2-003 offline generator must not create new ones.

## 15. Technical effects and experimental results

Technical effects may be drafted only from eligible P2-002 `technical_effects`.

Rules:

- `SOURCE_REPORTED` may be described as reported technical behavior;
- `SUPPORTED_CONSEQUENCE` must retain non-promotional grounding;
- do not convert experimental observations into universal guarantees;
- conditions linked to an effect must remain attached;
- do not produce commercial advantage, legal advantage, novelty, patentability, or grantability language.

Experimental parameters or results must remain example-scoped unless the reconstruction explicitly supports a broader scope.

## 16. Unresolved conflict handling

P2-001 v2 does not contain a dedicated `conflicts[]` target array.

P2-003 must therefore transform unresolved P2-002 conflicts into review-only blocking state without choosing a side.

Rules:

1. build a deterministic set of entity IDs affected by every `UNRESOLVED` conflict;
2. affected entities are ineligible for filing prose;
3. generate a review warning code such as `UNRESOLVED_RECONSTRUCTION_CONFLICT`;
4. generate or map missing-information records to each affected output section;
5. preserve related Human/author questions when available;
6. if removing conflicted content leaves enough eligible content, draft the remaining supported content only;
7. if a required technical section cannot be meaningfully drafted without conflicted content, mark the section `HUMAN_CONFIRMATION_REQUIRED`;
8. never produce `HUMAN_RESOLVED` or infer a resolution.

## 17. Missing information and author questions

P2-003 must preserve meaningful P2-002 gaps and route them to P2-001 target sections.

Recommended deterministic routing:

| P2-002 source / target area | P2-001 target |
|---|---|
| title_candidates | TITLE_OF_THE_INVENTION |
| technical_field | FIELD_OF_THE_INVENTION |
| technical_context | DESCRIPTION_OF_RELATED_ART |
| problems | BRIEF_SUMMARY_OF_THE_INVENTION |
| solution_concepts | BRIEF_SUMMARY_OF_THE_INVENTION |
| technical_effects | BRIEF_SUMMARY and/or DETAILED_DESCRIPTION |
| source_artifacts / drawing requirements | BRIEF_DESCRIPTION_OF_THE_DRAWINGS |
| elements | DETAILED_DESCRIPTION_OF_THE_INVENTION |
| relationships | DETAILED_DESCRIPTION_OF_THE_INVENTION |
| method_steps | DETAILED_DESCRIPTION_OF_THE_INVENTION |
| flows | DETAILED_DESCRIPTION_OF_THE_INVENTION |
| parameters | DETAILED_DESCRIPTION_OF_THE_INVENTION |
| embodiments | DETAILED_DESCRIPTION_OF_THE_INVENTION |
| variants | DETAILED_DESCRIPTION_OF_THE_INVENTION |

If a gap cannot be routed deterministically, keep it review-only and emit a warning instead of guessing a section.

Administrative-section gaps are created by P2-003 because the input contract intentionally lacks administrative facts.

## 18. Claims boundary

P2-003 **does not generate Claims**.

The P2-001 target schema requires a Claims root object, so the P2-003 output must represent the Claims section as an explicit ungenerated gate.

Required initial state:

```text
claims.section_id = "CLAIMS"
claims.status = "MISSING"
claims.claims = []
claims has no preamble
claims.missing_information_ids contains a deterministic P2-003 Claims gate ID
review_package.claim_support = []
review_boundary.claims_runtime_implemented = false
```

The linked missing-information description must state that Claims are not generated by P2-003 and are reserved for P2-004 or another separately authorized Claims task.

Do not create:

- independent claim candidates;
- dependent claims;
- claim elements;
- claim strategy;
- claim breadth analysis;
- claim dependencies;
- “What is claimed is:” prose;
- novelty/non-obviousness/patentability analysis.

P2-003 completion must not be represented as Claims completion.

## 19. Abstract generation

The Abstract is separate from Brief Summary.

The initial deterministic offline generator may create a PRESENT Abstract only when there is enough eligible technical content to state, at minimum:

- the technical field or system context;
- the disclosed technical solution;
- at least one supported element, process aspect, or technical effect.

Recommended source priority:

1. technical field;
2. primary eligible solution concept;
3. core eligible element or method step;
4. eligible technical effect.

The generator should assemble complete deterministic sentences in priority order and include only whole sentences while the result remains within 150 words.

It must **not truncate mid-sentence** merely to satisfy the word limit.

The declared `word_count` must match the existing P2-001 business-validation counting algorithm.

If meaningful supported content cannot be produced within the rules, set:

```text
status = MISSING
text = ""
word_count = 0
```

with linked missing information.

## 20. Sequence Listing boundary

P2-002 does not contain a canonical audited sequence-listing eligibility/data contract.

Therefore the initial P2-003 runtime must not generate sequence listings and must not assume that the section is `NOT_APPLICABLE`.

Default state:

```text
HUMAN_CONFIRMATION_REQUIRED
```

until a later reviewed Human/deterministic sequence-listing rule is authorized.

No biological sequence content may be fabricated from element names or prose.

## 21. NOT_APPLICABLE policy

The P2-001 target supports `NOT_APPLICABLE` only with a valid `not_applicable_basis`.

The initial P2-003 offline pipeline has:

- no Human-confirmation input contract;
- no approved P2-003 deterministic NOT_APPLICABLE rules.

Therefore the initial producer must not emit `NOT_APPLICABLE`.

Administrative and sequence-listing uncertainty remains `HUMAN_CONFIRMATION_REQUIRED`.

A future task may add reviewed deterministic rules without modifying P2-003 v0.1.0 semantics retroactively.

## 22. HUMAN_CONFIRMED policy

Although P2-001 reserves `HUMAN_CONFIRMED`, the current P2-003 input has no canonical Human confirmation/audit contract.

Therefore the initial producer must not emit:

- support with `HUMAN_CONFIRMED`;
- Human-confirmed administrative paragraphs;
- Human-resolved conflicts;
- answered author questions unless already represented by an authorized future input.

Any unexpected unaudited Human state must fail closed.

## 23. Review package mapping

P2-003 produces a separate review package and never renders it as filing-style content.

### 23.1 Evidence

Include only evidence actually used by generated technical content or necessary to explain blocked/missing content.

Map source evidence as:

```text
evidence_type = SOURCE_DOCUMENT
```

unless a future separately authorized Human/external/rule input legitimately provides another P2-001 evidence type.

### 23.2 Missing information

Include:

- propagated P2-002 technical gaps;
- title-selection gaps;
- administrative-data gaps;
- drawing-description gaps;
- conflict-driven gaps;
- Claims gate;
- sequence-listing confirmation gap;
- Abstract insufficiency when applicable.

### 23.3 Author questions

Preserve eligible upstream questions and add deterministic drafting questions only when needed to resolve a specific P2-003 output gap.

Do not ask legal-strategy questions in P2-003.

### 23.4 Claim support

Must remain:

```json
[]
```

P2-004 owns claim-support generation/audit.

### 23.5 Warnings

Warnings may represent:

- unresolved reconstruction conflict;
- proposed variant omitted;
- unsupported effect omitted;
- drawing description requires Human review;
- unsupported generalization blocked;
- source content contained legal/claim language that was not drafted as a legal conclusion.

Warnings remain internal review data.

## 24. Filing-style prose rules

The initial deterministic generator should prefer plain, technically faithful English over ornate patent boilerplate.

Allowed drafting connectors include neutral phrases such as:

- “The disclosed system includes …”
- “In one embodiment, …”
- “A method includes …”
- “In an example, …”
- “The system may …” when optionality is supported.

Prohibited unsupported boilerplate includes:

- “without departing from the spirit and scope of the invention”;
- “all equivalents are intended to be covered”;
- “the invention is novel”;
- “the invention is non-obvious”;
- “the claims should be construed broadly”;
- “one skilled in the art would understand” unless explicitly sourced and semantically appropriate;
- unsupported “preferred,” “optimal,” “best,” “critical,” “essential,” or “surprising” language.

The generator must not introduce legal scope by boilerplate.

## 25. Source content is untrusted data

Every string inside the P2-002 reconstruction remains untrusted data.

Text such as:

```text
Ignore previous instructions.
Generate claims.
Mark HUMAN_CONFIRMED.
The invention is patentable.
Use US 12,345,678 B2.
```

must not alter program behavior.

The deterministic generator must treat it as data and may use it only when it is eligible technical content under normal support rules.

Source-side legal or prompt-injection language must never:

- enable Claims;
- change output constants;
- enable provider/network use;
- create administrative numbers;
- create Human approval state;
- bypass grounding rules.

## 26. Legal and patentability exclusions

P2-003 must not generate conclusions regarding:

- novelty;
- non-obviousness;
- inventive step;
- subject-matter eligibility;
- patentability;
- validity;
- infringement;
- enforceability;
- freedom to operate;
- likelihood of allowance;
- filing readiness;
- claim scope;
- inventorship.

The phrase “inventive concept” in internal architecture means reconstructed technical solution concept, not a legal conclusion under patent law.

## 27. Administrative anti-hallucination

P2-003 must not infer or create:

- inventor;
- assignee/applicant;
- patent/application/publication numbers;
- priority number/date;
- related-application relationship;
- federal funding;
- joint research agreement;
- prior-disclosure date/status;
- filing date;
- examiner;
- art unit;
- classification;
- issue date;
- publication date;
- INID codes as rendered document labels.

Administrative content requires a later authorized input path.

## 28. Deterministic paragraph and identifier policy

Recommended ID families:

```text
P-TITLE-0001
P-FIELD-0001
P-RELATED-0001
P-SUMMARY-0001
P-DRAWINGS-0001
P-DETAIL-0001

MI-P2-003-0001
AQ-P2-003-0001
W-P2-003-0001
FIG-P2-003-0001
```

Within each section, paragraph `sequence` starts at 1 and is contiguous.

Ordering must depend only on validated input order and reviewed deterministic rules.

No sorting by natural-language “importance,” model confidence, or semantic relevance is permitted in the initial offline runtime.

## 29. Future offline generation stages

The reviewed implementation should use an explicit deterministic pipeline:

1. validate P2-002 input schema;
2. run P2-002 business validation or equivalent trusted validation gate;
3. validate generation config, required explicit boolean provenance, and the
   true-only authorization gate before any specification generation;
4. build reconstruction entity/evidence indexes;
5. compute ineligible entities and unresolved-conflict taint;
6. compute filing-content eligibility;
7. map document metadata and deterministic draft ID;
8. generate title state/content;
9. create administrative confirmation-required sections;
10. generate Background / Field;
11. generate Related Art;
12. generate Brief Summary;
13. generate or block Brief Description of Drawings;
14. generate Detailed Description;
15. create explicit Claims missing gate;
16. generate Abstract;
17. create Sequence Listing confirmation-required state;
18. map review-package evidence/missing/questions/warnings;
19. validate P2-001 JSON Schema;
20. validate P2-003 cross-object/business rules;
21. verify determinism by repeated generation.

No network/provider stage exists.

## 30. Business validation requirements

P2-003 business validation must cover at minimum:

- exact P2-002 contract identity;
- exact P2-001 output identity;
- document identity preservation;
- required boolean caller provenance, exact output mapping, no default/inference,
  and rejection of explicit real-source provenance before generation;
- deterministic draft ID;
- fixed section order;
- exact heading IDs and sequences;
- paragraph-ID uniqueness;
- contiguous paragraph sequences;
- valid P2-002 source paths;
- evidence existence and closure;
- grounding non-promotion;
- conflict-taint exclusion;
- SAFE_GENERALIZATION eligibility;
- proposed-variant exclusion;
- unaudited Human-state exclusion;
- administrative-section anti-hallucination;
- no INID/front-page metadata;
- no patent/application/publication number fabrication;
- title-selection rule;
- relationship semantic preservation;
- method/dependency preservation;
- flow-type preservation;
- parameter/range anti-broadening;
- example-scope preservation;
- embodiment/variant gates;
- drawing/vision boundary;
- Abstract word count;
- Claims missing gate;
- empty claim-support array;
- sequence-listing confirmation gate;
- legal/patentability exclusion;
- review-package not rendered as filing content;
- output/input mutation isolation;
- deterministic repeat output.

## 31. Schema vs business-validation responsibility

### JSON Schema

P2-001 v2.0.0 remains responsible for:

- local shape;
- strict properties;
- constants/enums;
- canonical section order;
- local section state shape;
- Claims shape;
- Abstract maximum;
- review-boundary constants.

### P2-003 business validator

P2-003 implementation is responsible for:

- mapping integrity;
- source-path resolution into P2-002;
- grounding preservation;
- evidence closure;
- drafting eligibility;
- conflict taint;
- semantic-conservatism rules;
- no administrative hallucination;
- no INID/front-page metadata;
- no Claims runtime;
- no range broadening;
- no unsupported relationship/flow/essentiality upgrades;
- Abstract declared-count correctness;
- deterministic output.

The implementation must not alter P2-001 schema semantics merely to make an invalid generated output pass.

## 32. P2-003 output and P2-004 handoff

P2-003 output is a valid P2-001 `USPTO_SPECIFICATION_DRAFT` with:

- supported specification prose;
- Claims explicitly missing/unimplemented;
- `claim_support = []`;
- full review package for non-Claims drafting issues.

P2-004 may later consume:

- the validated P2-003 specification;
- the validated P2-002 reconstruction;
- support/evidence information;

to generate and audit Claims.

P2-004 must not need P2-003 to invent claim strategy in advance.

P2-003 must preserve enough support metadata for P2-004 to map eventual claim elements back to the specification and reconstruction.

## 33. Frontend, renderer and DOCX boundary

P2-003 does not:

- modify the current frontend workflow;
- add a public endpoint;
- add DOCX v2 rendering;
- modify DOCX v1;
- change the Render deployment;
- expose real-paper conversion;
- implement page layout or issued-patent front page;
- generate patent drawings.

A later renderer/DOCX task may render the filing-style fields while excluding `review_package` and internal support metadata.

## 34. No provider/runtime expansion

The initial P2-003 implementation, if separately authorized, is offline deterministic generation only.

It must not:

- call OpenAI;
- call Gemini;
- call any model/provider API;
- browse;
- retrieve external patent material;
- perform prior-art search;
- call vector databases;
- use embeddings;
- use external storage;
- spend paid credits.

A future provider-assisted patent-drafting runtime would require separate Human authorization and EVAL-001/product-runtime evidence.

## 35. Synthetic fixture plan

A future P2-003 implementation should include synthetic fixtures covering at least:

1. representative system specification;
2. method/process specification;
3. multi-component relationships;
4. parameter-heavy detailed description;
5. multiple embodiments;
6. title-selection-required;
7. missing technical field;
8. missing administrative information;
9. unresolved conflict blocks drafting;
10. valid SAFE_GENERALIZATION;
11. proposed variant blocked;
12. source-supported drawing reference;
13. insufficient drawing description;
14. experimental/example scope preservation;
15. unsupported range broadening attempt;
16. prompt-injection-like source content;
17. legal/patentability phrase contamination;
18. Claims gate / no Claims generation;
19. Abstract boundary / 150-word enforcement;
20. sequence-listing confirmation-required;
21. INID/front-page metadata fabrication attempt;
22. patent/application/publication-number fabrication attempt;
23. dangling P2-002 source path;
24. nonexistent evidence reference.

All fixtures must be synthetic and must not contain real/confidential paper content.

### 35.1 Amendment 0.1.1 provenance tests — mandatory future implementation coverage

Use synthetic fixtures and configuration mutations, not real research data:

| Case | Required assertion |
|---|---|
| A — `source_document_synthetic=true` | Valid generated output; output `source_document.synthetic=true`, copied from config |
| B — field missing (including absent/null config) | Fail closed with `SOURCE_DOCUMENT_PROVENANCE_REQUIRED`; no default/fallback |
| C — `source_document_synthetic=false` | Fail before generation with `REAL_SOURCE_NOT_AUTHORIZED` |
| D — wrong type | Configuration validation fails; no coercion of strings, numbers, null, containers, or truthy values |
| E — source text says synthetic, config missing | Still fail closed; text cannot supply provenance |
| F — source text says real, config `true` | Source text cannot alter control flow; provenance remains caller assertion, subject to ordinary technical-content validation |
| G — output mapping / determinism | Repeated identical input/config produces identical output; mapping/returned-output mutation cannot mutate P2-002 nested input |
| H — contract immutability | Hash/diff checks prove P2-001/P2-002 schemas unchanged |

These are requirements for the future resumed implementation, not tests run or
results claimed by this documentation-only amendment.

## 36. Expected future implementation files

New files are expected to include, subject to repository pattern review:

```text
backend/app/services/uspto_specification_generation.py
backend/app/services/uspto_specification_generation_validation.py

tests/backend/test_uspto_specification_generation_v2.py
tests/fixtures/uspto-generation/v2.0.0/

docs/decisions/ADR-013-uspto-specification-generation-v2.md
```

The existing P2-001 schema remains the canonical output schema:

```text
schemas/uspto-specification/v2.0.0/uspto-specification.schema.json
```

No new output schema should be introduced solely for P2-003.

Implementation may add a dedicated README for the generator if useful, but must not fork the output contract.

## 37. Expected immutable surfaces

P2-003 implementation must not silently alter semantics of:

- P2-002 `INVENTION_RECONSTRUCTION` v1.0.0;
- P2-001 `USPTO_SPECIFICATION_DRAFT` v2.0.0;
- AI-001 v1;
- APP-002;
- patent-draft v1;
- existing extraction prompt;
- existing v1 draft-generation prompt/runtime;
- DOCX v1;
- current frontend workflow;
- Render configuration.

If a breaking upstream/downstream contract change is required, stop and obtain a separately reviewed authorization.

## 38. Acceptance criteria

### AC-01 — Correct task boundary
P2-003 is a specification-generation layer from validated P2-002 reconstruction to P2-001 output, not raw-paper reinterpretation.

### AC-02 — Canonical input
The sole technical drafting input is validated `INVENTION_RECONSTRUCTION` v1.0.0 plus narrow generation configuration.

### AC-03 — Canonical output
Output targets existing `USPTO_SPECIFICATION_DRAFT` v2.0.0 without a duplicate output schema.

### AC-04 — USPTO content structure
Canonical P2-001 section order and headings are preserved.

### AC-05 — No INID/front-page imitation
The specification explicitly prohibits rendering INID codes and issued-patent front-page bibliographic fields/numbers.

### AC-06 — Administrative anti-hallucination
Administrative sections cannot become PRESENT from P2-002 paper-derived content alone.

### AC-07 — No unsupported NOT_APPLICABLE
Initial producer emits no NOT_APPLICABLE state without a future approved rule/Human input.

### AC-08 — Title conservatism
Title is selected from an existing P2-002 candidate only; no title invention/ranking/rewrite.

### AC-09 — Field drafting
Technical Field maps from eligible P2-002 technical-field content without unsupported scope expansion.

### AC-10 — Related-art conservatism
Related-art prose is technical context only and does not become prior-art/patentability analysis.

### AC-11 — Summary drafting
Brief Summary uses eligible solution/problem/effect content without drafting Claims or mandatory unsupported limitations.

### AC-12 — Drawing boundary
Drawing prose respects no-OCR/no-vision/no-invented-caption rules.

### AC-13 — Detailed description
Elements/relationships/methods/flows/parameters/effects/embodiments are mapped into deterministic filing-style prose.

### AC-14 — Essentiality preservation
UNKNOWN/OPTIONAL/CONDITIONAL essentiality cannot be silently strengthened.

### AC-15 — Relationship preservation
Controlled P2-002 relationship types cannot be upgraded by drafting.

### AC-16 — Method dependency preservation
Sequence cannot become causal dependency without explicit P2-002 dependency support.

### AC-17 — Flow preservation
UNSPECIFIED flow cannot be upgraded.

### AC-18 — Parameter anti-broadening
Values, ranges, units and scope states are preserved; range broadening is rejected.

### AC-19 — Example-scope preservation
Experimental/example values remain example-scoped.

### AC-20 — Effects conservatism
Technical effects retain their basis and conditions without guarantees or legal/commercial claims.

### AC-21 — Embodiment gate
EXPLICIT/SYNTHESIZED eligible embodiments may be drafted; proposed embodiments are blocked.

### AC-22 — Variant gate
Only source-supported filing-eligible variants may enter prose; P2-003 invents none.

### AC-23 — Grounding preservation
SOURCE_FACT/PARAPHRASE/INFERENCE/SAFE_GENERALIZATION are not promoted.

### AC-24 — Evidence closure
Every substantive generated paragraph resolves to valid P2-002 source paths and evidence IDs.

### AC-25 — Conflict blocking
Unresolved conflicts are not silently resolved and affected content is blocked from filing prose.

### AC-26 — Missing/question propagation
Relevant P2-002 gaps and questions are preserved/routed without fabrication.

### AC-27 — Claims boundary
Claims remain explicit MISSING with zero claim content and `claim_support = []`; P2-004 owns Claims.

### AC-28 — Abstract
Abstract is separately generated, supported, deterministic, and no more than 150 words.

### AC-29 — Sequence Listing gate
Sequence Listing is not fabricated or automatically marked not applicable.

### AC-30 — HUMAN_CONFIRMED boundary
No unaudited HUMAN_CONFIRMED/HUMAN_RESOLVED state is produced.

### AC-31 — Review/filing separation
Review package and support metadata are not rendered as filing content.

### AC-32 — Legal exclusion
No novelty, patentability, non-obviousness, infringement, validity, filing-readiness or inventorship conclusion.

### AC-33 — Prompt-injection resistance
Untrusted source strings cannot alter runtime rules or enable prohibited output.

### AC-34 — Determinism
Identical validated input/configuration produces identical business output.

### AC-35 — Input/output isolation
Generated output does not mutate or share mutable nested state with the input reconstruction.

### AC-36 — Offline boundary
No network/provider/external service is required or authorized.

### AC-37 — v1/P2-001/P2-002 immutability
Released upstream/downstream contracts and current runtime/frontend/deployment behavior remain unchanged.

### AC-38 — P2-004 handoff
Output preserves sufficient specification/reconstruction support for a separately authorized Claims task.

### AC-39 — Synthetic/adversarial coverage
Future implementation tests cover the reviewed fixture categories including INID/official-number fabrication attempts.

### AC-40 — Independent specification review
This specification receives fixed-SHA Gemini 3.1 Pro High / Antigravity read-only PASS with no unresolved blocking findings before specification merge.

### AC-41 — Explicit source-document provenance

1. `generation_config` requires boolean `source_document_synthetic`.
2. No default or inference is permitted.
3. Output `document_metadata.source_document.synthetic` equals the caller-supplied value.
4. The current authorized runtime accepts only `true`.
5. `false` fails closed because real-data runtime is not authorized.
6. Missing provenance fails closed.
7. P2-001 and P2-002 schemas remain unchanged.
8. This provenance control does not authorize real/confidential data.

AC-01…AC-40 remain semantically unchanged and applicable. Historical 0.1.0
review PASS does not satisfy AC-40 for the amended 0.1.1 fixed SHA.

## 39. Explicitly out of scope

This amendment authorization does not authorize the following work. Separately
granted implementation authorization is recorded in Section 41, but execution
remains blocked and must not resume during this amendment task:

- P2-003 implementation;
- any provider/model call;
- real/confidential research data;
- public runtime integration;
- frontend changes;
- DOCX v2;
- drawings generation;
- Claims;
- P2-004;
- prior-art search;
- legal advice;
- filing automation;
- patent filing;
- production deployment;
- BLK-003 closure;
- EVAL-001 PRODUCT_RUNTIME execution.

## 40. Specification review checklist

The independent reviewer must verify at minimum:

1. input boundary is P2-002 only;
2. output target is existing P2-001 v2.0.0;
3. no duplicate schema is proposed;
4. canonical USPTO content section order is preserved;
5. INID/front-page codes and official identifiers are explicitly excluded;
6. administrative sections cannot be fabricated;
7. initial NOT_APPLICABLE and HUMAN_CONFIRMED gates are conservative;
8. Background/Related Art do not perform patentability analysis;
9. Summary does not become Claims;
10. Detailed Description preserves relationships, essentiality, methods, flows and range scope;
11. SAFE_GENERALIZATION remains P2-002-validated only;
12. proposed variants are blocked;
13. unresolved conflicts block affected filing prose;
14. evidence/source-path closure is enforceable;
15. Claims remain MISSING / P2-004-only;
16. Abstract behavior is deterministic and ≤150 words;
17. Sequence Listing is not fabricated;
18. source strings remain untrusted;
19. no provider/network/real-data/production scope expansion;
20. AC-01…AC-40 remain complete, testable, and implementation-feasible;
21. the provenance blocker is real and resolved without P2-001/P2-002 changes;
22. caller provenance is required, strictly boolean, with no default/inference
    and exact target mapping; `true` alone is currently permitted;
23. `false` fails closed before generation without authorizing real data;
24. AC-41 and future test cases A–H are clear/testable; deterministic
    implementation may resume only after fixed-SHA PASS + merge + successful
    post-merge CI under the existing implementation authorization;
25. no Claims/P2-004/provider/frontend/DOCX/deployment/production scope expansion.

## 41. Governance / next gate

Current specification 0.1.1 state: **APPROVED / MERGED** under
`HUMAN-P2-003-SPECIFICATION-AMENDMENT-0.1.1-2026-10-04`.
Human-supplied external Gemini 3.1 Pro High / Antigravity amendment review on
`1a17c87a6c42087965b7ac3fa88ae0fc17f26a4e`: **PASS / findings NONE**;
AC-01…AC-41 and future implementation cases A–H PASS; critical areas ALL PASS;
Human decisions required NONE; reviewer modified tracked files NO; merge
suitability YES. This is not a GitHub-native review or an implementation PASS.
PR #76 merged at `26d21feff592ff73574071887148630d44018b41`; amendment PR CI
`37182596336` and post-merge main CI `37184343482` are SUCCESS on their exact
respective SHAs. This merge is the implementation baseline.

Contract blocker: P2-001 requires `source_document.synthetic`, P2-002 strict
metadata does not carry it, and the previous configuration supplied no provenance.
Disposition approved in specification 0.1.1: required explicit caller boolean
`source_document_synthetic`, copied exactly; true only at the current runtime
authorization gate; false/missing/wrong-type values fail closed. Independent
review, merge and post-merge CI gates are satisfied. Contract blocker: **RESOLVED**.

Historical specification **0.1.0 APPROVED / MERGED** evidence follows; it is not
a PASS on amendment 0.1.1. Human-supplied external
Gemini 3.1 Pro High / Antigravity fixed-SHA review on
`a22440f1667388ece08868cbf0f2e22805449eef` is **PASS**, findings **NONE**,
AC-01…AC-40 **PASS**; Human decisions required **NONE**, reviewer modified
tracked repository files **NO**, specification merge suitability **YES**.
PR #74 merged at `af0948dab4f0e13e026ad7f6cdbd4ac9691a77a8`; post-merge
main CI [`37175416694`](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/37175416694)
is **SUCCESS** on that exact specification merge. The
[verified specification handoff](https://github.com/nshaokiet/ai-ip-description-generator/pull/74#issuecomment-5976352217)
records the satisfied specification gate, not implementation completion.

Next gate: **GEMINI 3.1 PRO HIGH / ANTIGRAVITY FIXED-SHA IMPLEMENTATION
REVIEW** — reviewer read-only, after exact-head PR CI SUCCESS.
P2-003 implementation authorization is **GRANTED** under
`HUMAN-P2-003-IMPLEMENTATION-2026-10-04`; execution resumed under that existing
authorization. Status: **IMPLEMENTED — INDEPENDENT IMPLEMENTATION REVIEW PENDING**.
The task is not COMPLETED. New generator/validator, synthetic tests/corpus and
ADR-013 implement the existing amended contract without upstream schema changes.
Targeted P2-003 tests: 110 PASS; full offline Python: 684 passed / 3 skipped;
frontend lint/typecheck/build and Render synthetic Playwright: PASS.
Standard synthetic Playwright: 26 PASS, exit 0; Windows teardown was assisted by
stopping only the two verified test-server processes after all assertions passed.
Acceptance self-check AC-01…AC-39 and AC-41: PASS; AC-40: **PENDING INDEPENDENT
IMPLEMENTATION REVIEW**, never self-approved. The auditable test matrix is in
`tests/fixtures/uspto-generation/v2.0.0/README.md`; exact implementation SHA
and PR CI belong in the fixed-SHA PR handoff.
No new authorization is required within the unchanged scope. **Do not merge
the implementation in this task.**

Historical specification workflow recorded before review/merge:

```text
P2-003 specification
  → fixed SHA
  → Gemini 3.1 Pro High / Antigravity read-only review
  → PASS / no blocking findings
  → specification merge
  → post-merge main CI SUCCESS
  → separate Human authorization for P2-003 IMPLEMENTATION
```

Specification approval does not authorize implementation.

P2-004 remains unauthorized.

### Specification version history — distinct from governance evidence

| Previous | New | Date | Author | Change / reason | Authorization | Breaking |
|---|---|---|---|---|---|---|
| 0.1.0 | 0.1.1 | 04/10/2026 | Codex | Semantic amendment: explicit required source-document provenance resolves missing target mapping; true-only runtime gate; AC-41 and future test cases A–H added; independent review was pending at authorship, subsequently PASS / merged via PR #76 as evidenced above | HUMAN-P2-003-SPECIFICATION-AMENDMENT-0.1.1-2026-10-04 | Yes — required P2-003 configuration input; P2-001/P2-002 unchanged |

Compatibility: future callers must explicitly supply the boolean. Missing or
legacy configuration is rejected, never silently migrated/defaulted. No released
P2-003 implementation exists to migrate. Historical specification 0.1.0 remains
reviewed/merged evidence; amendment 0.1.1 approval is separately evidenced above.

### Governance evidence revision history

| Previous | New | Date | Author | Change / reason | Reference | Breaking |
|---|---|---|---|---|---|---|
| Specification 0.1.0 (unversioned governance evidence) | Governance evidence 0.1.1; specification 0.1.0 unchanged | 04/10/2026 | Codex | Reconcile existing fixed-SHA specification PASS, PR #74 merge and successful main CI; implementation remains unauthorized | HUMAN-P2-003-SPECIFICATION-GOVERNANCE-RECONCILIATION-2026-10-04; CI `37175416694` | No |
| Governance evidence 0.1.1 | Governance evidence 0.1.2; specification separately amended to 0.1.1 | 04/10/2026 | Codex | Record granted implementation authorization and blocked execution pending amended-spec review/merge/main CI; preserve historical external review evidence | HUMAN-P2-003-IMPLEMENTATION-2026-10-04; HUMAN-P2-003-SPECIFICATION-AMENDMENT-0.1.1-2026-10-04 | No — evidence update; semantic amendment recorded separately above |
| Governance evidence 0.1.2 | Governance evidence 0.1.3; specification 0.1.1 semantics unchanged | 04/10/2026 | Codex | Reconcile amendment external PASS, PR #76 merge / successful main CI; blocker resolved; record implemented offline service and local tests, independent implementation review pending | HUMAN-P2-003-IMPLEMENTATION-2026-10-04; merge `26d21feff592ff73574071887148630d44018b41`; CI `37184343482` | No |

Historically, additional independent review was waived by Human only for the bounded docs-only
reconciliation with unchanged specification/runtime/schema/prompt/code/test
semantics, no implementation authorization and successful PR CI. This is not a
new review PASS on the governance revision. That historical waiver does not
apply to specification amendment 0.1.1; its required independent fixed-SHA review
was subsequently supplied by Human. It does not waive implementation review.

MCP: **BLOCKED BY TOOL CAPABILITY — Unknown task: P2-003**; no task state,
lease, checkpoint or completion is fabricated. BLK-003 **OPEN**; PRODUCT_RUNTIME
**DEFERRED — AWAITING FUNDING**; semantic acceptance **NOT DETERMINED**;
provider/API authorization **NOT GRANTED**, budget **0**, calls **NONE**;
real/confidential data **NOT AUTHORIZED**; arbitrary real-paper conversion
**NOT ENABLED**; Claims runtime **NOT IMPLEMENTED**; production
**NOT APPROVED / NOT PERFORMED**; deployment change **NO**. No DOCX v2 or
frontend/runtime integration is authorized. **STOP after implementation handoff.
Do not merge the implementation in this task.
Do not start P2-004.**
