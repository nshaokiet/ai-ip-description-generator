# Spec Compliance

- name: `spec-compliance`
- version: `1.0.0`
- role_scope: `QUALITY`

Governance takes precedence over this skill. A task specification may narrow its behavior but may not expand authority.

## Purpose

Verify the implementation satisfies the frozen specification without scope drift.

## Applies when

Quality review with explicit acceptance criteria or compatibility requirements.

## Required inputs

- frozen spec/version/SHA
- implementation diff
- acceptance criteria
- tests/CI
- relevant contracts

## Allowed actions

- map each acceptance criterion to evidence
- identify missing behavior, regression, incompatibility, or unauthorized scope
- record QUALITY findings

## Forbidden actions

- invent new requirements
- waive failed acceptance criteria
- accept unrelated scope expansion because tests pass

## Procedure

1. Enumerate frozen acceptance criteria and explicit non-goals.
2. Map each criterion to implementation and validation evidence.
3. Check compatibility, error handling, regression, and scope discipline.
4. Report unsatisfied/unsupported criteria and verdict.

## Required checks

- every acceptance criterion has evidence or a finding
- non-goals remain untouched
- no requirement is silently reinterpreted

## Output contract

Spec-compliance matrix plus evidence-backed Quality findings/verdict.

## Failure conditions

- frozen spec identity is unavailable
- material criteria cannot be evaluated
- implementation includes unauthorized scope drift

## Handoff

Request changes or block with exact unmet criteria; Planner handles actual spec defects.
