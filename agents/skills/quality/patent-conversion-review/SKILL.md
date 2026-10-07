# Patent Conversion Review

- name: `patent-conversion-review`
- version: `1.0.0`
- role_scope: `QUALITY`

Governance takes precedence over this skill. A task specification may narrow its behavior but may not expand authority.

## Purpose

Review scientific-paper-to-patent conversion quality while preserving evidence and invention boundaries.

## Applies when

R3 AI-IP/conversion work producing invention reconstruction, specification drafting, or supported draft claims.

## Required inputs

- applicable P2-002/P2-003/P2-004 contracts
- source/evidence traceability
- implementation/output under review
- exact review SHA when reviewing code

## Allowed actions

- review source fidelity and traceability
- check invention/prior-art separation and unsupported inference
- review missing-information behavior and terminology consistency

## Forbidden actions

- invent disclosure or patentability conclusions
- promote unsupported inference to source fact
- expand Claims/provider/runtime authority
- treat draft output as legal filing advice

## Procedure

1. Identify the versioned AI-IP contracts governing the stage.
2. Trace material technical content through source evidence and reconstruction.
3. Check invention boundary, unsupported inference, terminology, conflicts, and missing-information handling.
4. Record quality findings without rewriting source truth.

## Required checks

- Scientific Paper -> Evidence -> Invention Reconstruction -> Patent Draft chain remains intact
- SOURCE_FACT/PARAPHRASE/INFERENCE/MISSING distinctions preserved
- P2-002/P2-003/P2-004 boundaries preserved
- Human/legal review status explicit

## Output contract

Patent-conversion Quality findings/verdict with source-fidelity and boundary evidence.

## Failure conditions

- traceability is broken
- unsupported disclosure is promoted
- required Human/author confirmation is missing for critical content

## Handoff

Block affected content/criterion and route evidence/content remediation through the authorized Implementer/Human path.
