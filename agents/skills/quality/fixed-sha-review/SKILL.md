# Fixed Sha Review

- name: `fixed-sha-review`
- version: `1.0.0`
- role_scope: `QUALITY`

Governance takes precedence over this skill. A task specification may narrow its behavior but may not expand authority.

## Purpose

Perform an immutable independent review tied to one exact implementation SHA.

## Applies when

Quality review of a completed implementation candidate.

## Required inputs

- task/spec identity
- base SHA
- implementation SHA
- diff/files
- tests/CI/evidence

## Allowed actions

- inspect exact diff and relevant repository evidence
- record findings/blockers
- submit QUALITY verdict

## Forbidden actions

- modify tracked implementation
- review a moving/unverified target as final
- reuse PASS from another SHA
- treat reviewer agreement as authoritative source verification

## Procedure

1. Verify exact task/spec/base/implementation identities and reviewer independence.
2. Inspect full authorized diff and relevant evidence.
3. Evaluate correctness, regression, failure handling, maintainability, and scope discipline.
4. Record immutable findings and QUALITY verdict for that SHA only.

## Required checks

- target SHA remains exact/current for the attempt
- reviewer did not modify tracked implementation
- blocking findings and evidence are explicit
- stale reviews remain historical only

## Output contract

Independent Quality review artefact with exact SHA identities, findings, blockers, evidence, and verdict.

## Failure conditions

- implementation SHA moved or cannot be verified
- reviewer independence is violated
- required evidence is missing

## Handoff

Return REQUEST_CHANGES/BLOCKED to Implementer; any remediation SHA requires a new review attempt.
