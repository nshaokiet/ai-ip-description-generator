# Architecture Analysis

- name: `architecture-analysis`
- version: `1.0.0`
- role_scope: `PLANNER`

Governance takes precedence over this skill. A task specification may narrow its behavior but may not expand authority.

## Purpose

Analyze architecture, dependencies, risk, and compatibility without implementing changes.

## Applies when

Planner tasks that need technical decomposition or impact analysis.

## Required inputs

- repository architecture
- task specification/authorization
- relevant ADRs/contracts/tests
- current integration boundaries

## Allowed actions

- map components/data flows/trust boundaries
- identify dependencies and compatibility risks
- recommend bounded implementation slices

## Forbidden actions

- modify application/runtime implementation
- approve its own proposed architecture when Human approval is required
- hide material tradeoffs or migration impact

## Procedure

1. Map affected components, interfaces, evidence/data flow, and owners.
2. Identify compatibility, security, migration, rollback, and operational risks.
3. Separate required changes from optional/future work.
4. Produce a bounded architecture recommendation and task decomposition.

## Required checks

- no unauthorized dependency/service expansion
- backward compatibility considered
- security/data/provider boundaries identified

## Output contract

Architecture analysis with affected components, risks, decisions needed, and bounded implementation plan.

## Failure conditions

- architecture decision exceeds delegated authority
- source-of-truth contracts materially conflict
- required system evidence is unavailable

## Handoff

Escalate only the unresolved architecture/authority decision; keep independent analysis available.
