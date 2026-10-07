# Safe Code Change

- name: `safe-code-change`
- version: `1.0.0`
- role_scope: `IMPLEMENTER`

Governance takes precedence over this skill. A task specification may narrow its behavior but may not expand authority.

## Purpose

Make a minimal, secure, reversible repository change while preserving unrelated work.

## Applies when

Implementer edits to code, tests, configuration, or authorized technical documentation.

## Required inputs

- authorized file scope
- current diff/status
- applicable coding/security contracts
- test strategy

## Allowed actions

- edit only authorized files
- add focused tests needed to verify behavior
- refactor only when required for the authorized change

## Forbidden actions

- opportunistic unrelated cleanup
- commit secrets/confidential research data
- add provider/network/dependency changes outside authorization
- force-push shared history

## Procedure

1. Inspect existing implementation and neighboring tests before editing.
2. Make the smallest coherent change preserving existing contracts.
3. Run targeted validation and diff/secret/scope checks.
4. Commit only authorized files with a precise message.

## Required checks

- no unrelated file drift
- failure handling and security boundaries preserved
- tests meaningfully verify changed behavior
- git diff --check/secret review clean

## Output contract

A scoped commit/diff with validation evidence and material risk/limitation notes.

## Failure conditions

- safe isolated edit is not possible
- change requires unauthorized dependency/service/policy
- tests reveal unresolved regression

## Handoff

Stop affected implementation and hand back the precise blocker; preserve the worktree and evidence.
