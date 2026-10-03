# ADR-012 — Invention Reconstruction Boundary

## Metadata

| Field | Value |
|---|---|
| ADR ID | ADR-012 |
| Status | Records approved specification architecture — implementation review pending |
| Date | 03/10/2026 |
| Decision owner | Human / Product Owner |
| Implementation owner | Codex |
| Independent reviewer | Gemini 3.1 Pro High / Antigravity read-only |
| Related task | P2-002 |
| Authorization | `HUMAN-P2-002-IMPLEMENTATION-2026-10-03` |
| Reviewed specification | `9c3f5e67f3c3af73807aab3f3ba84300fcd99c07` |
| Implementation baseline | `e87b51987c42edb1432a9612a4e05bc7c0d9b113` |

## Context

The current v1 pipeline can transform structured analysis directly into a claim-free Patent Description Draft. P2-001 establishes a broader USPTO-style target for later P2 work. Direct raw-paper-to-patent-prose generation is rejected because it collapses evidence authority, technical reconstruction, filing-style drafting, and review gates into one semantic step. That design would make unsupported components, mechanisms, ranges, relationships, effects, embodiments, and administrative facts difficult to detect deterministically.

## Decision

This ADR records the architecture already approved in specification PR #70 and
the cited Human implementation authorization. It introduces no new architecture
decision; implementation evidence still requires independent fixed-SHA review.

Introduce the strict `INVENTION_RECONSTRUCTION` v1.0.0 contract and an offline deterministic adapter with this boundary:

```text
APP-002 ExtractionInputEnvelope
        +
AI-001 STRUCTURED_INVENTION_ANALYSIS v1
        → P2-002 INVENTION_RECONSTRUCTION v1.0.0
        → future P2-003 USPTO Specification Generation
```

Both upstream inputs are required:

- APP-002 is the canonical source-evidence authority for document identity, evidence IDs, types, locators, and verbatim normalized content.
- AI-001 is the canonical structured semantic-analysis authority for problems, solutions, components, process steps, effects, embodiments, experiments, missing information, questions, and evidence usage.

P2-002 validates and adapts those contracts. It does not redefine them.

## Evidence-authority boundary

Where both upstream contracts represent document identity, values must match exactly. Every used AI-001 evidence record must resolve to APP-002 and match evidence ID, supported current type, locator, and a contiguous verbatim excerpt. A mismatch fails closed.

Grounding is non-promotional. AI-001 `SOURCE_FACT`, `PARAPHRASE`, and `INFERENCE` map exactly. Limited supported synthesis remains `INFERENCE`; it cannot add unsupported mechanisms, components, relations, parameters, effects, embodiments, or use cases.

The only approved SAFE_GENERALIZATION rule is `SG-01_EXPLICIT_SOURCE_CATEGORY`, and the initial adapter does not generate it. The validator requires the category and member terms to occur in cited evidence and prohibits numerical broadening or unsupported technical additions.

## Offline deterministic boundary

Identical validated inputs produce identical business output. IDs use ordered `IR-*`, `MI-IR-*`, `AQ-IR-*`, and `W-IR-*` families. Business output contains no random UUID, wall-clock timestamp, provider request ID, or model result.

The initial adapter uses conservative defaults: element type `OTHER`, essentiality `UNKNOWN`, untyped component relations as `RELATED_TO`, input/output flow type `UNSPECIFIED`, experimental scope `EXAMPLE_ONLY`, and no generated variants or Human-confirmed states.

## Versioning and immutability

The new schema is additive at `schemas/invention-reconstruction/v1.0.0/`. Released APP-002, AI-001, patent-draft v1, USPTO specification v2, prompt, runtime, DOCX, frontend, and deployment semantics remain unchanged. Any later breaking reconstruction change requires a new version and approved compatibility plan.

## Claims, provider, and production boundaries

P2-002 does not implement Claims, Draft Claims, claim strategy, patentability, novelty, obviousness, infringement, validity, final USPTO prose, P2-003, provider-assisted reconstruction, public endpoints, frontend integration, deployment, or production behavior.

Provider authorization remains not granted, budget remains zero, paid calls remain prohibited, real/confidential research data remains unauthorized, EVAL-001 PRODUCT_RUNTIME remains deferred awaiting funding, and BLK-003 remains open.

## Consequences

Positive consequences:

- P2-003 can consume a validated technical model instead of reinterpreting raw paper content from scratch.
- Source/evidence failures, dangling references, unsupported ranges, review-only variants, and prohibited legal/Claims content can be blocked deterministically.
- P2-001 filing-style output stays separated from internal review evidence.

Trade-offs:

- The initial offline adapter deliberately leaves element type, essentiality, flow type, dependency, variants, and unsupported semantic relationships conservative or empty.
- Deep invention discovery and semantic quality remain unvalidated without a separately authorized provider/runtime evaluation.
- Human confirmation and conflict resolution require a future audited input contract.

## Alternatives rejected

1. **Raw paper directly to USPTO prose** — rejected because evidence authority and technical reconstruction cannot be independently validated.
2. **AI-001 only** — rejected because AI-001 evidence excerpts must still be verified against canonical APP-002 source units.
3. **APP-002 only** — rejected because deterministic parsing does not provide the structured semantic analysis already defined by AI-001.
4. **Duplicate combined input schema** — rejected because it would fork released upstream semantics and create drift.
5. **Provider-assisted reconstruction in P2-002** — rejected because provider authorization/budget and PRODUCT_RUNTIME evaluation are absent.
