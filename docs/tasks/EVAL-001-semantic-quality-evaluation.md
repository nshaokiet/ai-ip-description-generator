# EVAL-001 — Semantic Quality Evaluation Specification

## Metadata

| Field | Value |
|---|---|
| Task ID | EVAL-001 |
| Specification version | 0.1.0 |
| Status | READY FOR INDEPENDENT SPECIFICATION REVIEW — implementation not approved |
| Owner / final decision authority | Human / Product Owner |
| Author | ChatGPT |
| Intended implementation agent | GPT-6 Sol |
| Independent specification reviewer | Gemini 3.1 Pro High |
| Independent implementation reviewer | Gemini 3.1 Pro High |
| Date | 28/09/2026 |
| Fixed baseline | `main` at `37d42fc8b07003aa2a67f2d1d32e64e69eb0ddb5` |
| Branch | `docs/eval-001-semantic-quality-evaluation-spec` |
| Confidentiality | Public/open-access or synthetic evaluation inputs only; real/confidential research data is prohibited while BLK-003 remains OPEN |

## 1. Purpose

EVAL-001 measures whether the current, already-merged MVP converts research papers into source-grounded structured invention analysis and patent-description drafts with acceptable semantic fidelity, coverage, missing-information behavior, and hallucination resistance.

This task is an **evaluation task, not a product-feature task**. It must evaluate a fixed system baseline before any prompt, schema, model, runtime, application, or test-expectation remediation is attempted.

A successful EVAL-001 result establishes only a bounded semantic-quality evidence set for the evaluated corpus and exact runtime configuration. It does **not** establish production readiness, patentability, filing readiness, legal correctness, confidential-data safety, universal model quality, or performance on papers outside the evaluated population.

## 2. Fixed baseline and frozen system under evaluation

The evaluation baseline is:

`37d42fc8b07003aa2a67f2d1d32e64e69eb0ddb5`

The system under evaluation includes the canonical merged versions of:

- Output Schema v1.0.0.
- Extraction Prompt v1.0.0.
- Patent Draft Generation Contract / Draft Prompt v1.0.0.
- Current parsing, evidence-unit, grounding-validation, draft-generation and DOCX pipeline.
- Current provider runtime configuration when a Human-authorized live evaluation run is performed.
- Current frontend/backend behavior only insofar as it is needed to obtain or verify the evaluated outputs.

During EVAL-001 measurement, the following are frozen unless a separate Human-approved remediation task is created:

- model/provider selection;
- reasoning level;
- extraction and draft prompts;
- JSON schema;
- validation rules;
- source-unit construction;
- draft contract;
- application code;
- test expectations;
- DOCX template.

The purpose is to measure the current system, not optimize while measuring it.

## 3. Existing boundary inherited from the project

The current project classification remains:

**MVP HANDOVER READY — LOCAL/SYNTHETIC**

P0-009 CI is active and validates deterministic/local-synthetic regression, but CI success does not establish semantic quality on real research papers.

The following remain unchanged:

- BLK-003: **OPEN**.
- Live-provider smoke: **UNVALIDATED / DEFERRED** until separately authorized and actually executed.
- Production readiness: **NO**.
- Public deployment: **NOT PERFORMED**.
- Real/confidential research-data authorization: **NO**.
- Claims generation: outside the MVP.
- Patentability, novelty, inventive step, FTO and legal advice: outside scope.

EVAL-001 may use only public/open-access papers with documented provenance/licensing or synthetic research-style inputs. No unpublished, customer, internal, personal, or otherwise confidential research data may be used.

## 4. Evaluation questions

EVAL-001 must answer, with evidence:

1. Are emitted technical assertions supported by the cited source evidence?
2. Are numbers, units, experimental results, components, process steps and technical effects preserved without invention?
3. Are `SOURCE_FACT`, `PARAPHRASE` and `INFERENCE` labels semantically appropriate?
4. Does the extraction capture the important technical content that a Human evaluator identifies in the source?
5. Does the system correctly identify material missing, ambiguous or conflicting information instead of guessing?
6. Are author questions relevant and actionable for the identified gaps?
7. Does the generated patent-description draft remain faithful to the structured analysis and source evidence?
8. Does the draft avoid unsupported legal/patentability conclusions and Claims?
9. Is the Abstract compliant with the current <=150-word contract?
10. How variable are the results across documents and, if repeated runs are authorized, across repeated runs of the same document?

## 5. Non-goals

EVAL-001 must not:

- modify prompts, schemas, runtime model configuration or application behavior in order to improve the measured result;
- perform prior-art search or patentability assessment;
- evaluate legal sufficiency or likelihood of patent grant;
- create Claims;
- fine-tune a model;
- introduce a vector database, RAG architecture, multi-agent runtime or new provider abstraction;
- implement production authentication, storage, retention or deployment;
- use confidential research material;
- silently substitute ChatGPT web/UI output, Gemini output, or another model for the product runtime and call it product-quality evidence;
- convert local/synthetic CI results into semantic-quality evidence.

If evaluation exposes a product defect, record it as an evaluation finding and create a separate remediation task after Human approval.

## 6. Corpus design

### 6.1 Minimum corpus

The proposed minimum evaluation corpus is **6 research papers**:

- at least 2 distinct technical domains;
- at least 4 English-language papers;
- at least 1 Vietnamese-language paper;
- at least 1 paper with substantial experimental results/tables;
- at least 1 paper whose technical disclosure is incomplete or ambiguous enough to exercise missing-information behavior;
- each paper must satisfy the current MVP input limits: text-based PDF or DOCX, <=10 MiB, PDF <=50 pages, no OCR requirement.

If a license-compatible Vietnamese paper cannot be sourced, implementation must stop at corpus approval and request a Human decision; it must not silently remove the language-coverage requirement.

### 6.2 Provenance and licensing

For every corpus item, record:

- case ID;
- title;
- authors;
- publication/source;
- public source URL or repository identifier;
- language;
- technical domain;
- document format;
- page count where known;
- SHA-256 of the exact evaluated file;
- access/license status;
- local acquisition date.

Do not commit a full source document unless redistribution is clearly permitted. The repository should normally commit a manifest and evaluation annotations, not copyrighted full-text papers. Local source files must remain outside tracked Git unless a specific license review permits inclusion.

### 6.3 No hidden benchmark substitution

The corpus must be selected before viewing the evaluated model outputs. Do not replace difficult cases after seeing poor model performance unless the original case is objectively unusable, and record any replacement with reason and Human approval.

## 7. Gold annotation model

Each case must have a Human-reviewed gold annotation package containing atomic evaluation items rather than one free-form “ideal answer.”

Minimum gold categories:

- technical field;
- technical problem(s);
- technical solution(s);
- components or system elements;
- process steps where applicable;
- distinguishing technical features supported by the source;
- technical effects;
- experimental conditions/results;
- embodiment/example facts where applicable;
- material missing/ambiguous/conflicting information;
- prohibited conclusions that must not appear.

Each gold item must contain:

- stable gold ID;
- category;
- normalized proposition;
- importance: `KEY` or `SECONDARY`;
- source locator(s);
- short supporting excerpt(s) only as needed;
- evaluator note;
- whether omission should count against coverage;
- whether the item is intentionally absent and therefore belongs in missing-information evaluation.

Gemini or another model may assist annotation, but **a model may not be the sole authority for the gold set**. A Human evaluator must review and accept the gold annotations before they are used for final scoring.

## 8. Evaluation unit and semantic labels

The evaluator must decompose system output into atomic substantive assertions. Pure headings, boilerplate warnings, IDs and formatting-only text are excluded from semantic assertion counts.

Each assertion is assigned one support judgment:

- `SUPPORTED_DIRECT` — explicitly stated by the cited source.
- `SUPPORTED_PARAPHRASE` — faithful paraphrase with no added technical meaning.
- `SUPPORTED_INFERENCE` — reasonable limited synthesis supported by cited evidence but not directly stated.
- `UNSUPPORTED` — not supported by the cited evidence or source.
- `CONTRADICTED` — conflicts with the source.
- `NOT_APPLICABLE` — non-substantive boilerplate or excluded content.

For assertions carrying the system's own grounding label, separately score whether the system label is appropriate.

A **critical hallucination** is any unsupported or contradicted assertion involving at least one of:

- numeric result, parameter, unit or threshold;
- experimental outcome;
- component or material;
- process step;
- causal/technical effect;
- comparison or superiority claim;
- embodiment/variant;
- attribution to the source;
- legal/patentability conclusion.

## 9. Metrics

The implementation must produce both per-case and aggregate metrics.

### 9.1 Grounding support precision

`supported substantive assertions / all substantive assertions`

Report unsupported and contradicted assertions separately.

### 9.2 Critical hallucination count

Raw count and affected case IDs.

### 9.3 Key-fact coverage

`covered KEY gold items / all applicable KEY gold items`

Also report SECONDARY coverage separately so the score is not inflated by minor details.

### 9.4 Grounding-label accuracy

For assertions mapped to output grounding labels, compare the system label to Human semantic judgment.

### 9.5 Evidence fidelity

Measure whether cited evidence IDs exist and whether the cited evidence actually supports the assertion. Deterministic identifier/excerpt integrity may reuse existing validators, but semantic support must still be judged.

### 9.6 Missing-information quality

For Human-annotated material gaps:

- recall: gold gaps surfaced by the system / gold gaps;
- precision: relevant system gaps / all system gaps;
- conflict handling accuracy where applicable.

### 9.7 Author-question usefulness

Human rates each question:

- relevant to an identified gap;
- specific/actionable;
- answerable by the author;
- does not presuppose unsupported facts.

Report pass rate and common failure modes.

### 9.8 Draft faithfulness

Evaluate substantive assertions in the generated draft against the structured analysis and source evidence using the same support labels.

Report:

- supported draft assertion rate;
- unsupported/contradicted draft assertion rate;
- critical hallucinations in draft;
- whether unsupported content is introduced between extraction and drafting.

### 9.9 Contract safety

Record deterministic counts for:

- Claims or draft Claims appearing: must be 0;
- patentability/novelty/inventive-step/FTO/legal conclusion violations: must be 0;
- Abstract >150 words: must be 0;
- schema/business-rule failures: must be 0 for an accepted run.

## 10. Proposed acceptance thresholds

These thresholds are **proposed by this specification and are not implementation-approved until Human acceptance after independent specification review**.

For the approved corpus:

| Gate | Proposed threshold |
|---|---|
| Critical hallucinations | **0** |
| Contradicted substantive assertions | **0** |
| Grounding support precision | **>=98% aggregate** and **>=95% per case** |
| KEY gold-item coverage | **>=85% aggregate** and **>=75% per case** |
| Grounding-label accuracy | **>=90% aggregate** |
| Missing-information precision | **>=80% aggregate** |
| Missing-information recall | **>=80% aggregate** |
| Author-question usefulness | **>=80% pass rate** |
| Draft supported-assertion rate | **>=97% aggregate** and **>=93% per case** |
| Claims / prohibited legal conclusions | **0** |
| Abstract >150 words | **0** |
| Accepted-run schema/business-rule failures | **0** |

No weighted “overall score” may hide a failure of a zero-tolerance gate. Critical hallucination, contradiction, Claims/legal-boundary violation, or falsified evidence is individually blocking.

If independent specification review concludes a threshold is unjustified, the threshold must be revised before Human implementation approval rather than silently weakened during implementation.

## 11. Runtime/output acquisition

### 11.1 Product-runtime evidence

Final semantic-quality claims must be based on outputs produced by the **actual current product runtime** at the frozen baseline and recorded runtime configuration.

For every evaluated run record:

- source case ID and source SHA-256;
- repository baseline SHA;
- prompt/schema versions;
- model identifier;
- reasoning/configuration values that materially affect output;
- run timestamp;
- extraction output hash;
- draft output hash;
- whether the run was product runtime, local synthetic harness, or another source.

Only **product-runtime** rows count toward EVAL-001 semantic acceptance.

### 11.2 Provider-access gate

Current live-provider smoke is UNVALIDATED / DEFERRED. This specification does not authorize use of a paid API, provider credential, or budget.

If product-runtime evaluation requires an API key or paid usage, implementation must obtain explicit Human approval for:

- provider use;
- credential handling;
- budget ceiling;
- number of evaluation runs.

If no authorized provider access exists, the evaluation framework/gold set may be prepared, but EVAL-001 must remain **BLOCKED FOR PRODUCT-RUNTIME EVIDENCE** and must not be marked PASS/COMPLETED.

Outputs manually generated in ChatGPT, Gemini or another consumer UI may be used only as exploratory/non-product evidence and must be labeled as such.

## 12. Repeated-run stability

Repeated live runs are optional until Human approves their cost.

If authorized, run at least 3 repetitions on 2 representative cases and report:

- KEY-fact coverage range;
- support-precision range;
- critical hallucination count per repetition;
- missing-information variance;
- major structural differences.

Do not average away a critical failure.

## 13. Evaluation artefacts

Implementation should create a versioned evaluation package under a dedicated path, proposed:

`eval/semantic/v1/`

Expected artefacts:

- `README.md` — execution and interpretation guide;
- `manifest.json` — corpus metadata, provenance and hashes;
- `rubric.md` — frozen semantic rubric;
- `gold/` — Human-reviewed case annotations;
- `runs/` — metadata/output references for authorized evaluated runs;
- `reports/` — machine-readable metrics and Human-readable summary;
- evaluator scripts/tests needed to reproduce deterministic calculations.

Do not commit:

- provider credentials;
- confidential source documents;
- unrestricted local paths;
- full copyrighted papers without clear redistribution permission;
- raw logs containing sensitive material.

Generated evaluation reports must distinguish deterministic metrics, Human judgments and model-assisted judgments.

## 14. Reviewer independence and adjudication

The implementation agent may build the evaluator and calculate deterministic metrics but may not independently declare semantic PASS.

Gemini 3.1 Pro High may perform independent implementation review and may assist semantic cross-checking, but Human / Product Owner remains final acceptance authority.

For disputed semantic items:

1. preserve the original evaluator judgment;
2. record reviewer disagreement;
3. Human adjudicates the final label;
4. do not overwrite history to make the score cleaner.

## 15. Failure and remediation policy

EVAL-001 is measurement-first.

If a gate fails:

- record exact case, assertion/gold IDs and evidence;
- classify the failure;
- do not change prompts/schema/model/application inside EVAL-001 merely to improve the score;
- propose a separate remediation task with bounded scope;
- rerun only after Human approval and a new fixed baseline.

A failed evaluation is valid project evidence and must not be hidden.

## 16. Security, privacy and legal boundary

- Public/open-access or synthetic documents only.
- No real/confidential research data while BLK-003 is OPEN.
- No secrets in Git or reports.
- No provider key in evaluation artefacts.
- Keep evidence excerpts minimal.
- No legal/patentability claim is produced by the evaluator.
- Evaluation results describe observed technical behavior, not legal quality.
- No public deployment is required or authorized.

## 17. Acceptance criteria

| AC | Requirement | Evidence required |
|---|---|---|
| AC-01 | Evaluation runs from exact baseline `37d42fc8b07003aa2a67f2d1d32e64e69eb0ddb5` or a Human-approved successor created only after a separate remediation cycle | Git SHA recorded in manifest/report |
| AC-02 | Corpus has >=6 approved public/open-access cases satisfying the composition rules | Manifest + provenance/license review |
| AC-03 | No confidential/unpublished/customer research data is used | Corpus review + Git diff audit |
| AC-04 | Human-reviewed atomic gold annotations exist for every accepted case | Gold files + Human acceptance record |
| AC-05 | Rubric and metric formulas are frozen before final evaluated outputs are scored | Versioned rubric + commit history |
| AC-06 | Every substantive extraction assertion receives a semantic support judgment | Machine-readable assertion-level results |
| AC-07 | KEY-fact coverage is calculated per case and aggregate | Report |
| AC-08 | Missing-information precision/recall and author-question usefulness are evaluated | Report + annotation evidence |
| AC-09 | Draft substantive assertions are independently checked for source/analysis support | Draft assertion-level results |
| AC-10 | Critical hallucinations, contradictions and prohibited-output violations are reported as non-averagable gates | Report |
| AC-11 | Abstract length, schema and business-rule safety are checked deterministically | Script/test output |
| AC-12 | Product-runtime runs record exact model/config/prompt/schema/source/output hashes | Run metadata |
| AC-13 | Manual ChatGPT/Gemini UI outputs, if any, are excluded from product-runtime acceptance metrics | Report provenance |
| AC-14 | No provider call or spend occurs without separate Human approval | Approval/evidence or BLOCKED status |
| AC-15 | CI/local regression remains green after evaluator-only implementation; no application/test expectation weakening | Existing CI + implementation diff |
| AC-16 | Independent Gemini 3.1 Pro High implementation review occurs on a fixed SHA; reviewer modifies no artefacts | Review record |
| AC-17 | Human makes final semantic acceptance decision after reviewing metrics/findings | Human decision record |
| AC-18 | BLK-003 remains OPEN and EVAL-001 does not claim production/confidential-data/legal readiness | Final report/governance docs |

## 18. Required implementation boundaries

Unless separately approved, implementation may add evaluation-only artefacts, scripts and tests, plus minimal governance documentation.

It must not change:

- `backend/app/` product behavior;
- `frontend/src/` product behavior;
- canonical prompts;
- canonical schemas;
- model/provider selection;
- runtime token/time limits;
- production dependency manifests merely to support evaluation;
- existing test expectations;
- DOCX template.

If evaluation tooling requires a new dependency, prefer standard-library/existing dependencies. Any dependency-manifest change requires explicit justification and Human approval before implementation.

## 19. Human decisions required before implementation

Independent specification review must explicitly assess these proposed decisions. Human approval is required for:

1. corpus requirement: >=6 cases, including >=1 Vietnamese case and >=2 technical domains;
2. proposed semantic acceptance thresholds in Section 10;
3. Human gold-annotation/adjudication responsibility;
4. whether product-runtime provider access is authorized for EVAL-001;
5. if authorized: provider budget ceiling and maximum run count;
6. whether repeated-run stability testing is authorized;
7. whether full source papers may ever be committed when licensing permits, or manifest/local-only is mandatory.

No implementation agent may infer approval of these items merely because this specification exists.

## 20. Independent specification review checklist

Gemini 3.1 Pro High should verify:

- the evaluation measures semantic quality rather than structural validity already covered by CI;
- zero-tolerance hallucination/legal-boundary gates are appropriate;
- formulas are reproducible and not vulnerable to denominator gaming;
- gold annotation design separates KEY from SECONDARY facts;
- corpus selection avoids cherry-picking and confidential data;
- actual product-runtime evidence is distinguished from synthetic/manual UI evidence;
- provider-access/budget constraints are explicit;
- evaluation does not mutate the system under test;
- acceptance thresholds are defensible for a patent-drafting support MVP;
- failure/remediation workflow preserves negative evidence;
- copyright/licensing handling is adequate;
- no production-readiness implication is introduced.

## 21. Handoff

```text
Task ID: EVAL-001
Task: Semantic Quality Evaluation
Specification: v0.1.0
Baseline: 37d42fc8b07003aa2a67f2d1d32e64e69eb0ddb5
Status: READY FOR INDEPENDENT SPECIFICATION REVIEW
Author: ChatGPT
Intended implementation agent: GPT-6 Sol
Independent reviewer: Gemini 3.1 Pro High
Implementation approval: NOT GRANTED
Provider/API authorization: NOT GRANTED
BLK-003: OPEN
Live-provider smoke: UNVALIDATED / DEFERRED
Production readiness: NO
Next action: GEMINI 3.1 PRO HIGH — INDEPENDENT SPECIFICATION REVIEW
```

## 22. Post-specification decision and framework implementation evidence addendum

This addendum records later decisions and implementation evidence without changing the reviewed specification **v0.1.0** or rewriting its historical pre-review metadata/handoff above. Approved specification commit: `67c8d71f79712ede8780babf890a79fcbfd2769e` (documentation-only direct child of frozen product baseline `37d42fc8b07003aa2a67f2d1d32e64e69eb0ddb5`). Gemini 3.1 Pro High independent specification review: **PASS WITH HUMAN DECISIONS REQUIRED**, AC-01…AC-18 **PASS**, findings **NONE**. Exact review date was not supplied.

Human / Product Owner approved all seven Section 19 decisions: corpus >=6 with >=1 Vietnamese and >=2 domains; thresholds exactly Section 10; AI-assisted gold drafts permissible only with Human review/acceptance; no product-runtime provider access; live/provider budget **0** and no paid API calls; repeated live runs not authorized; source papers **manifest/local-only** with no full-paper Git commit. Implementation approval is **GRANTED FOR FRAMEWORK PHASE ONLY**.

Framework package: `eval/semantic/v1/`, with six public/open-access **candidate** PDFs recorded by provenance/hash in the manifest (five English, one Vietnamese, multiple domains) and locally ignored full sources. All six draft gold files remain `PENDING_HUMAN` and explicitly incomplete; candidate corpus Human acceptance: **PENDING**. The deterministic scorer and JSON/Markdown framework report return **BLOCKED FOR PRODUCT-RUNTIME EVIDENCE / SEMANTIC ACCEPTANCE NOT DETERMINED**. No product-runtime record, provider credential, provider API call or provider spend was created. Targeted synthetic evaluator tests: **26 passed**; full offline `python -m pytest tests -q -p no:cacheprovider` with live flags set to 0: **406 passed, 3 skipped, 1 warning**. Draft PR [#29](https://github.com/nshaokiet/ai-ip-description-generator/pull/29) CI run [`36404294487`](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/36404294487) on framework implementation `b8a7ede8f18ca50dedd669fcd47365dd8ed250bc` / checkout merge-ref `f9f1fbd891882d70dc26e644cca4d1dbb1728cc2` succeeded: Linux backend **407 passed, 2 skipped**, frontend lint/build **PASS**, Playwright synthetic E2E **11 passed**. These are implementation/regression evidence, not semantic product-quality evidence.

Current framework lifecycle: **READY FOR INDEPENDENT FRAMEWORK IMPLEMENTATION REVIEW** after successful Draft PR CI; Gemini 3.1 Pro High review remains pending. Overall EVAL-001 remains **BLOCKED FOR PRODUCT-RUNTIME EVIDENCE**; not PASS or Completed. BLK-003 remains **OPEN**; live-provider smoke **UNVALIDATED / DEFERRED**. Production/public deployment, legal quality and real/confidential-data use are not approved. Future product-runtime evaluation, corpus/gold acceptance and final semantic decision require their separate Human gates.

## 23. Gold completion phase evidence addendum (29/09/2026)

This later evidence does not rewrite specification v0.1.0 or the true earlier pending state above. Gemini 3.1 Pro High independently reviewed the final framework SHA `1c077bbb0d53304e44ad0ff7639ea3866b30fb5f`: **PASS**, findings **NONE**. Human / Product Owner accepted that review and the exact six manifest cases (`eval-en-002`, `eval-en-003`, `eval-en-004`, `eval-en-005`, `eval-en-007`, `eval-vi-001`), then authorized **gold annotation completion only**.

Each unchanged-hash, local-only PDF was verified for bytes, SHA-256, page limit and text extraction before annotation. The six candidate inventories now contain **154 atomic items** (102 KEY, 52 SECONDARY), with source locators, brief excerpts, material gap/conflict targets and evaluator prohibited-conclusion expectations; see `eval/semantic/v1/GOLD_REVIEW_GUIDE.md`. Inventory completion is **6/6**, but Human gold acceptance is **0/6**: all six remain `PENDING_HUMAN` with null reviewer/date. No full paper is committed.

Provider access remains **NOT AUTHORIZED**, budget **0**, provider calls **NONE**, product-runtime evidence **NONE**, semantic acceptance **NOT DETERMINED** and EVAL-001 **NOT COMPLETED**. BLK-003 stays **OPEN**; no live-provider, production, legal-readiness or confidential-data claim. Next gate: Gemini 3.1 Pro High targeted gold-completion review followed by Human item/package adjudication. Draft PR #29 remains open; no merge is authorized.
