# Ai Ip Domain

- name: `ai-ip-domain`
- version: `1.0.1`
- role_scope: `SHARED`

Governance takes precedence over this skill. A task specification may narrow its behavior but may not expand authority.

## Purpose

Preserve AI-IP evidence, invention-boundary, and patent-drafting semantics.

## Applies when

Work touching scientific-paper ingestion, invention reconstruction, patent drafting, claims, or related review.

## Required inputs

- authorized source/evidence artefacts
- [P2-002 reconstruction contract](../../../../docs/tasks/P2-002-invention-reconstruction.md)
- [P2-003 draft specification contract](../../../../docs/tasks/P2-003-uspto-specification-generation-v2.md)
- [P2-004 supported draft claims contract](../../../../docs/tasks/P2-004-supported-draft-claims.md)
- task-specific source facts and Human confirmations

## Allowed actions

- trace source evidence through reconstruction to draft output
- preserve SOURCE_FACT/PARAPHRASE/INFERENCE/MISSING distinctions
- flag missing author/Human confirmation

## Forbidden actions

- treat a scientific paper as a patent
- promote prior art or experimental results automatically into inventor contribution
- convert INFERENCE into SOURCE_FACT
- invent unsupported disclosure, claims, provider/runtime authority, or legal conclusions

## Procedure

1. Identify the applicable versioned AI-IP contracts.
2. Trace each material draft/review statement to permitted evidence.
3. Preserve unsupported or conflicting content as MISSING/confirmation-required.
4. Maintain the chain Scientific Paper -> Evidence -> Invention Reconstruction -> Patent Draft.

Preserve these distinctions explicitly:

- Scientific paper != patent.
- Prior art != inventor contribution.
- Experimental result != automatically an inventive feature.
- INFERENCE != SOURCE_FACT.
- Unsupported technical content must not silently become patent disclosure.

Apply [P2-002](../../../../docs/tasks/P2-002-invention-reconstruction.md),
[P2-003](../../../../docs/tasks/P2-003-uspto-specification-generation-v2.md) and
[P2-004](../../../../docs/tasks/P2-004-supported-draft-claims.md) with their existing
versioned schemas; do not invent a parallel ontology. Preserve missing information
and author questions, Human review and legal disclaimers. Output remains a draft,
not legal advice, patentability or filing approval. Skills do not authorize Claims
runtime, provider calls or real/confidential research data.

## Required checks

- prior art and inventor contribution remain separated
- unsupported inference is not promoted
- Human/legal review status remains explicit
- claims/provider/runtime boundaries are preserved

## Output contract

Evidence-grounded AI-IP reasoning/review output with labels, traceability, and unresolved confirmations.

## Failure conditions

- required evidence is missing or contradictory
- task asks the skill to exceed Claims/provider/runtime/legal authority
- source provenance cannot be preserved

## Handoff

Block the affected content and request the required Human/author/source confirmation without inventing facts.
