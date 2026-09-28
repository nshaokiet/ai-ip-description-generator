# EVAL-001 semantic rubric v1.0.0

This freezes the arithmetic for the framework phase against specification v0.1.0, Section 10. Human semantic judgments, corpus acceptance, product-runtime authorization and final acceptance are separate gates. The evaluator does not assign semantic labels by keyword or act as an independent reviewer.

## Unit and labels

Split extraction and draft output into atomic substantive assertions. Exclude headings, IDs and boilerplate as `NOT_APPLICABLE`; every remaining assertion must receive exactly one of `SUPPORTED_DIRECT`, `SUPPORTED_PARAPHRASE`, `SUPPORTED_INFERENCE`, `UNSUPPORTED`, `CONTRADICTED`. The first three count as supported. An assertion carrying `SOURCE_FACT`, `PARAPHRASE` or `INFERENCE` is also judged for grounding-label correctness; an unsupported/contradicted assertion cannot have a correct support label. Evidence-ID existence and whether evidence semantically supports the assertion are distinct Human-reviewed fields.

A Human marks `critical_categories` only for an `UNSUPPORTED` or `CONTRADICTED` assertion involving numeric results/units/parameters, experimental outcome, component/material, process step, technical effect, comparison/superiority, embodiment, source attribution, or legal/patentability conclusion. The engine counts these IDs; it never infers a hallucination from keywords. Preserve every original assertion ID and disagreement for Human adjudication, without editing history to improve a score.

## Deterministic formulas

Every rate is a numerator/denominator pair; a zero denominator is `NOT_APPLICABLE` with JSON `rate: null`, never 100% and never threshold PASS. Aggregate rates divide summed numerators by summed denominators, not the mean of case percentages.

| Metric | Numerator / denominator |
|---|---|
| Extraction grounding support precision | Supported substantive extraction assertions / all substantive extraction assertions |
| Draft supported-assertion rate | Supported substantive draft assertions / all substantive draft assertions |
| KEY or SECONDARY coverage | Covered applicable gold items of that importance / all applicable items of that importance |
| Grounding-label accuracy | Correct system labels / extraction assertions carrying system labels |
| Missing-information precision | Relevant system gaps / all system gaps |
| Missing-information recall | Distinct gold gap IDs surfaced by relevant system gaps / all Human gold gap targets |
| Author-question usefulness | Questions passing all four Human checks / all author questions |

The four question checks are relevance to a gap, specificity/actionability, answerability by an author, and no unsupported presupposition. `gold_coverage` must enumerate every applicable gold item exactly once. KEY omissions cannot be hidden by high precision. Draft assertions are judged independently of extraction assertions. Unsupported/contradicted IDs, critical IDs, evidence-ID failures, semantic-evidence failures and missed KEY/gap IDs remain visible in per-case reports.

Contract safety records raw counts of Claims, prohibited legal conclusions, Abstracts over 150 words (`abstract_word_count > 150`), and schema/business-rule failures. Critical hallucinations, contradictions, falsified evidence IDs, Claims/legal violations, Abstract length violations and schema/business-rule failures are non-averagable.

## Human-approved thresholds

| Gate | Threshold |
|---|---|
| Critical hallucinations; contradicted substantive assertions | 0 each |
| Extraction support | >=98% aggregate; >=95% every case |
| KEY coverage | >=85% aggregate; >=75% every case |
| Grounding-label accuracy | >=90% aggregate |
| Missing-information precision and recall | >=80% aggregate each |
| Author-question usefulness | >=80% aggregate |
| Draft support | >=97% aggregate; >=93% every case |
| Claims; prohibited legal conclusions; Abstract >150 words; accepted-run schema/business-rule failures | 0 each |

No weighted overall score exists. A threshold failure is evidence, not a reason to change this rubric or the frozen product. Threshold arithmetic is deterministic, but semantic labels and gold completeness require Human review.

## Provenance and blocking

Only `PRODUCT_RUNTIME` output at baseline `37d42fc8b07003aa2a67f2d1d32e64e69eb0ddb5`, with explicit provider authorization and verified local output hashes, may contribute to semantic acceptance. `SYNTHETIC_HARNESS` and `MANUAL_UI` are validated as provenance but excluded. Product-runtime case coverage, Human-accepted corpus and gold, Human-accepted complete assertion inventory, and threshold results are separate checks. Even when all checks pass, the engine returns `READY_FOR_HUMAN_SEMANTIC_DECISION`, never an autonomous semantic PASS.

For this implementation phase, provider authorization is **not granted**, budget is **0**, and repeated runs are **not authorized**. With no product-runtime output the result is **BLOCKED FOR PRODUCT-RUNTIME EVIDENCE / SEMANTIC ACCEPTANCE NOT DETERMINED**. BLK-003 remains OPEN; no production, public-deployment, legal or confidential-data readiness is implied.
