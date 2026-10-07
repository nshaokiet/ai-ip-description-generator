# Task Specification

- name: `task-specification`
- version: `1.0.0`
- role_scope: `PLANNER`

Governance takes precedence over this skill. A task specification may narrow its behavior but may not expand authority.

## Purpose

Author or repair a versioned, implementable task specification inside Human-authorized scope.

## Applies when

Planner assignments that require scope, acceptance criteria, gates, or implementation handoff.

## Required inputs

- Human task authorization
- project context and governance
- repository constraints
- known dependencies/risks

## Allowed actions

- define scope/non-goals and acceptance criteria
- define required tests/reviews/migration/rollback
- version and submit specification artefacts

## Forbidden actions

- self-authorize a specification freeze
- implement the specified product/MCP change
- expand provider/data/budget/production authority

## Procedure

1. Translate Human authorization into explicit scope and non-goals.
2. Define measurable acceptance criteria and required evidence/gates.
3. Identify dependencies, risks, rollback, security/testing requirements.
4. Version the specification and prepare implementation handoff.

## Required checks

- every requirement is traceable to authorization or approved architecture
- acceptance criteria are testable
- stop conditions and Human gates are explicit

## Output contract

Versioned specification + implementation handoff with scope, ACs, dependencies, tests, risks, rollback, and non-goals.

## Failure conditions

- authorization is insufficient for requested scope
- critical requirement remains contradictory or untestable
- required architectural decision needs Human approval

## Handoff

Keep the spec unfrozen/blocked and route the specific decision to Human authority.
