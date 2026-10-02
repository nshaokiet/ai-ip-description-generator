# P2-001 — USPTO Patent Specification Target v2.0.0 & Reference Corpus

## Metadata

| Field | Value |
| --- | --- |
| Task ID | P2-001 |
| Status | **READY FOR INDEPENDENT FIXED-SHA REVIEW** |
| Authorization | `HUMAN-P2-001-USPTO-TARGET-2026-10-02` |
| Authorization evidence | Human directive on 02/10/2026: “bắt đầu p2 - 001”, following the agreed P2-001 scope in the same project conversation |
| Baseline main | `eab9cd8d9421cb5bc40dc18134716febc16ac7cd` |
| Branch | `docs/p2-001-uspto-target-spec-v2` |
| Owner | ChatGPT/Codex under AGENTS.md standing delegation |
| Independent reviewer | Gemini 3.1 Pro High / Antigravity read-only |
| Target version | `2.0.0` |
| Classification | Specification/contract implementation and reference-corpus task only |
| Paid API/provider calls | **NOT AUTHORIZED / NOT REQUIRED** |
| Real/confidential research data | **NOT AUTHORIZED** |
| Production | **NOT APPROVED / NOT PERFORMED** |
| BLK-003 | **OPEN** |

## Purpose

Define and implement the project-level target contract for transforming one scientific research paper into a **USPTO-style nonprovisional utility patent specification draft** suitable for Human/IP-specialist review.

P2-001 does **not** implement live generation, Claims runtime, production data handling, or filing automation. It provides the strict machine-readable contract, neutral Human-readable template, structural reference maps, synthetic fixtures, and offline validation that later P2 tasks may implement against.

The phrase “B2-style” in product discussion refers to structural inspiration from issued U.S. utility patents such as `US11367264B2` and `US11044591B2`; `B2` is a patent publication kind code, not a USPTO fill-in form. The product target is therefore a **USPTO-style specification draft**, not an issued-patent facsimile and not a filing-ready legal document.

## Authoritative references

Primary requirements sources:

1. [USPTO Nonprovisional (Utility) Patent Application Filing Guide](https://www.uspto.gov/patents/basics/apply/utility-patent)
2. [USPTO MPEP § 608 — Disclosure / preferred specification arrangement under 37 CFR 1.77(b)](https://www.uspto.gov/web/offices/pac/mpep/s608.html)

Reference examples supplied by the Human / Product Owner:

3. [`US11367264B2`](https://patentimages.storage.googleapis.com/91/f6/9b/18dc2af29220c8/US11367264.pdf)
4. [`US11044591B2`](https://patentimages.storage.googleapis.com/42/19/af/1c5089854ab9d4/US11044591.pdf)

The USPTO sources govern the target structure. Issued patents are examples of drafting patterns only and do not override current USPTO guidance.

## Product target

### Input

Exactly one supported scientific research document:

- text-based PDF; or
- DOCX.

The later product runtime will use parsed text, tables, figures, source locators and evidence units produced by the existing APP-001/APP-002 pipeline.

### Primary output

`USPTO_SPECIFICATION_DRAFT` in English, exportable to editable DOCX, using the preferred utility-specification structure below.

### Secondary review output

A separate `REVIEW_PACKAGE` containing grounding, missing information, author questions, claim-support mappings, inferences and warnings.

Review-only metadata must not be mixed into the filing-style specification body unless explicitly required by the USPTO structure.

## Canonical target section order

The v2 target contract models the following order:

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
13. `SEQUENCE_LISTING` when applicable.

Notes:

- The arrangement is the preferred USPTO utility-specification order, not a claim that every section applies to every invention.
- If an administrative section is not supported by source/Human evidence, the system must not guess.
- A section may be represented internally as `NOT_APPLICABLE` only when that state is supported by Human confirmation or a deterministic rule approved in a later task.
- Claims and Abstract must be renderable on separate pages.
- Abstract maximum: 150 words.
- Claims must be numbered and must support independent/dependent relationships.

## Target content model

### 1. Filing-style content

The v2 target schema can represent:

- technically accurate invention title;
- administrative statements requiring Human-supplied information;
- technical field;
- related art/background;
- technical problem;
- inventive concept;
- brief summary aligned with the claimed invention;
- drawing list;
- detailed embodiments;
- components and relationships;
- method/process steps;
- operating conditions;
- examples/experimental support where appropriate;
- alternatives/variants only under explicit support classification;
- claims;
- abstract.

### 2. Grounding/support model

Every substantive technical proposition should retain a support classification:

- `SOURCE_FACT`
- `PARAPHRASE`
- `INFERENCE`
- `SAFE_GENERALIZATION` — proposed for v2; deterministic definition required before runtime implementation
- `PROPOSED_VARIANT` — requires Human confirmation before being treated as supported invention content
- `MISSING`
- `HUMAN_CONFIRMED`

P2-001 reserves these v2 concepts but does not modify the released v1 schema or runtime.

### 3. Administrative-data policy

The system must never infer as fact:

- inventor identity;
- assignee;
- application/priority numbers;
- related-application relationships;
- federal funding;
- joint-research agreements;
- prior-disclosure dates/status;
- filing date;
- examiner;
- patent number;
- issue date;
- classifications.

Such information must come from Human-supplied metadata or an explicitly authorized external source in a later task.

### 4. Claims target

Claims are part of the v2 product target, but **Claims generation is not implemented by P2-001**.

The v2 Claims target contract supports:

- at least one independent claim candidate;
- dependent claims with valid dependency references;
- claim numbering;
- claim type/family metadata where useful (for example method/system/non-transitory computer-readable medium) without forcing every family for every invention;
- claim-element decomposition;
- support mapping from each material claim element to specification/evidence;
- unsupported-element blocking or explicit Human-confirmation state;
- no patentability, validity, infringement or grantability conclusion.

Implementation belongs to P2-004 or a separately authorized Claims task.

## Separation of product outputs

### A. USPTO-style specification draft

Contains filing-style sections only.

It must not include internal QA sections such as:

- Evidence Appendix;
- Missing Information and Author Questions;
- internal grounding labels;
- validation digests;
- correlation IDs;
- developer/runtime metadata.

### B. Review package

May contain:

- evidence matrix;
- source locators;
- inference/generalization labels;
- missing-information list;
- author questions;
- conflicts;
- claim-support matrix;
- unsupported-content warnings;
- revision/validation metadata.

This separation preserves reviewability without polluting the patent-style document.

## v1 → v2 compatibility direction

Released v1 artefacts remain immutable.

Current v1:

`Structured Invention Analysis v1 → Patent Description Draft v1 → DOCX v1`

Target v2:

`Parsed Paper/Evidence → Structured Analysis → Invention Reconstruction → USPTO Specification Draft v2 → Claims/Support Audit → DOCX v2 + Review Package`

P2-001 does not overwrite `schemas/patent-draft/v1.0.0`, current prompts, validators, runtimes or DOCX templates.

A later implementation task must introduce new versioned artefacts and a migration/adapter boundary rather than silently changing v1 semantics.

## Reference-corpus findings to preserve

### US11367264B2

Useful structural patterns:

- title;
- cross-reference to related application;
- federally sponsored research statement;
- Background split into Field of the Invention and Description of Related Art;
- Summary of the Invention;
- multiple drawing sheets;
- detailed description with figure/reference-numeral mapping;
- numbered claims.

This reference demonstrates that administrative sections can be materially present and therefore cannot be fabricated from a scientific paper.

### US11044591B2

Useful structural patterns:

- concise Background;
- Brief Summary expressed through multiple embodiments;
- Brief Description of the Drawings;
- detailed system/method/software discussion;
- multiple claim categories, including computer-implemented method and other computer-implemented forms;
- numbered claims.

This reference demonstrates that a scientific/technical disclosure may need to be reconstructed into multiple embodiments and claim perspectives, not merely reformatted section-by-section.

## In scope

- target definition for USPTO-style utility specification draft v2;
- section order and semantic responsibilities;
- separation between filing-style draft and review package;
- reference-corpus analysis for the two Human-supplied B2 examples;
- v1→v2 migration direction;
- Claims target requirements without implementing Claims generation;
- administrative-data missing/Human-confirmation policy;
- future drawing/reference-numeral requirements;
- acceptance criteria for downstream P2-002…P2-010.

## Explicitly out of scope

- modifying current application code;
- changing current v1 JSON Schemas;
- changing prompts or provider/runtime policy;
- generating Claims at runtime;
- paid API/provider calls;
- live-model evaluation;
- uploading or processing a real/confidential paper;
- prior-art search;
- patentability/novelty/non-obviousness conclusions;
- legal advice;
- inventorship determination;
- production deployment;
- authentication/storage/retention changes;
- filing to USPTO;
- representing output as an issued B2 patent.

## Deliverables

- `schemas/uspto-specification/v2.0.0/uspto-specification.schema.json`
- `schemas/uspto-specification/v2.0.0/README.md`
- `docs/templates/USPTO_SPECIFICATION_TEMPLATE_v2.md`
- `docs/references/US11367264B2-section-map.json`
- `docs/references/US11044591B2-section-map.json`
- `tests/fixtures/uspto-specification/v2.0.0/representative.json`
- `tests/fixtures/uspto-specification/v2.0.0/missing-administrative-information.json`
- `tests/fixtures/uspto-specification/v2.0.0/unsupported-claim-element.json`
- `tests/schema/test_uspto_specification_v2.py`
- `docs/tasks/P2-001-uspto-target-specification-v2.md`
- `docs/decisions/ADR-011-uspto-target-specification-v2.md`
- `docs/references/P2-001-uspto-reference-corpus.md`
- roadmap/status reconciliation required by project governance.

## Implementation and verification evidence

The v2 schema is JSON Schema Draft 2020-12 and uses strict objects. It fixes the canonical 13-section order, explicit state and non-applicability support, v2-only grounding classes, Claims and claim-element support links, drawing-plan metadata, deterministic Abstract word-count validation, and the filing-content/review-package boundary.

Local evidence on 02/10/2026, with `RUN_OPENAI_LIVE_TESTS=0` and `RUN_OPENAI_DRAFT_LIVE_TESTS=0`:

| Gate | Result |
| --- | --- |
| Dedicated v2 schema/fixture/reference-map tests | **PASS — 19 passed** |
| Full offline backend regression | **PASS — 466 passed, 3 skipped** |
| Python dependency consistency | **PASS — no broken requirements** |
| Frontend lint | **PASS** |
| Frontend typecheck | **PASS** |
| Frontend production build | **PASS** |
| Render static-demo export and provider-secret marker scan | **PASS** |
| Standard synthetic Playwright suite | **PASS — 19 passed** |
| Render synthetic-demo Playwright suite | **PASS — 3 passed** |
| `git diff --check` | **PASS** |

The released v1 schema files are pinned by SHA-256 in the new offline test. No current prompt, runtime, DOCX v1 renderer, frontend, backend, or `render.yaml` file is changed. Provider/API calls: **0**. Claims runtime introduced: **NO**. Real/confidential data used: **NO**. Production/deployment changed: **NO**.

Project Orchestrator evidence is unavailable for this identifier: the connected state tool returned `Unknown task: P2-001`. This is recorded as **BLOCKED BY TOOL CAPABILITY** and does not replace Git/task/CI evidence or fabricate lifecycle state.

## Acceptance criteria

### AC-01 — Correct target identity
The task defines the output as a USPTO-style nonprovisional utility patent specification **draft**, not a “B2 form,” issued patent, legal advice or filing-ready artefact.

### AC-02 — USPTO structure
The target section model covers the preferred utility-specification arrangement in MPEP § 608 / 37 CFR 1.77(b), including Claims and Abstract.

### AC-03 — Claims boundary
Claims are explicitly part of the future product target, but P2-001 performs no Claims generation and introduces no runtime Claims behavior.

### AC-04 — Administrative anti-hallucination
Related applications, funding, joint research, prior disclosure and similar administrative facts cannot be inferred from the paper.

### AC-05 — Background semantics
Background distinguishes technical field from related art/background and does not convert citations into patentability conclusions.

### AC-06 — Summary semantics
Brief Summary is distinct from Abstract and is directed to the invention/inventive concept.

### AC-07 — Drawings target
The target supports figure identifiers/reference numerals and later detailed-description mapping.

### AC-08 — Detailed-description target
The target supports components, relationships, methods, embodiments, conditions, examples and carefully classified variants.

### AC-09 — Abstract rule
Abstract is modeled as a separate-page section with a maximum of 150 words.

### AC-10 — Filing/review separation
Internal evidence/missing-information/QA data are separated from the filing-style specification body.

### AC-11 — v1 preservation
No released v1 schema/prompt/runtime/template is overwritten or semantically changed.

### AC-12 — Reference corpus
Both Human-supplied patents are documented as reference examples with structural observations and limitations.

### AC-13 — Zero-cost/offline task
No provider/API call, paid service, live model, real/confidential research paper or production mutation is required or authorized.

### AC-14 — Downstream handoff
The specification provides clear input/output boundaries for P2-002 Invention Reconstruction, P2-003 Patent Specification Generation, P2-004 Claims and later renderer/evaluation tasks.

### AC-15 — Independent review
Final documentation SHA receives Gemini 3.1 Pro High / Antigravity read-only review with PASS and no unresolved blocking findings before merge.

## Review checklist

Reviewer must verify:

- authoritative USPTO references are represented accurately;
- the two B2 references are used as examples, not as normative law or templates;
- no issued-patent metadata is proposed for AI fabrication;
- Claims are target scope only, not silently implemented;
- no v1 runtime/schema/template behavior changes;
- no provider/API/funding/production/data authorization expansion;
- BLK-003 remains OPEN;
- EVAL-001 PRODUCT_RUNTIME remains DEFERRED — AWAITING FUNDING.

## Next tasks enabled by P2-001

After P2-001 is approved and merged:

1. **P2-000** — Product Webapp Simplification & Research Paper Entry may align its result headings and UX language with the v2 target while preserving synthetic/public safety boundaries.
2. **P2-002** — Invention Reconstruction contract/runtime design.
3. **P2-003** — USPTO Specification Generation contract/runtime v2.
4. **P2-004** — Claims strategy/generation/support matrix.
5. Later P2 tasks for drawings, DOCX v2, QA, benchmark and live-product evaluation.

P2-001 approval does not automatically authorize those implementation tasks.
