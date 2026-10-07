# Specification Execution

- name: `specification-execution`
- version: `1.0.0`
- role_scope: `IMPLEMENTER`

Governance takes precedence over this skill. A task specification may narrow its behavior but may not expand authority.

## Purpose

Execute an authorized frozen specification exactly and produce reviewable evidence.

## Applies when

Implementer assignments with a frozen authorized task specification.

## Required inputs

- frozen spec identity/SHA
- Human authorization reference
- authorized branch/worktree
- acceptance criteria and allowed file scope

## Allowed actions

- implement scoped code/docs/tests
- record implementation/CI evidence
- remediate in-scope review findings

## Forbidden actions

- silently change frozen requirements
- implement outside allowed scope
- self-record Security/Quality PASS
- treat local success as merge authorization

## Procedure

1. Verify frozen spec, authorization, base, branch/worktree, and scope.
2. Implement the smallest complete change satisfying the acceptance criteria.
3. Run required focused and repository validation.
4. Capture final immutable SHA and hand off to independent review.

## Required checks

- diff matches scope and spec
- all acceptance criteria have evidence
- new SHA triggers fresh applicable review
- RECORDED evidence is not overstated

## Output contract

Implementation candidate with exact base/spec/final SHA, changed files, validation, and independent-review handoff.

## Failure conditions

- spec is contradictory/incomplete/infeasible
- required exception or scope expansion is unauthorized
- required validation fails

## Handoff

Enter SPEC_BLOCKED semantics for spec issues or return failures to the appropriate Planner/Human/reviewer path.
