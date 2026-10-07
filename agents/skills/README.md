# Phase D P0 Skill Package

Version: 1.0.0
Phase: GOV-AGENT-001-D
Status: IMPLEMENTED FOR REVIEW — NOT ACTIVATED

This directory contains the complete P0 skill inventory defined by
`GOV-AGENT-001` §22. Skills are reusable procedures. They do not create task
authorization, role assignment, evidence verification, merge permission, provider
authority, or Workflow V2 activation.

## Standard contract

Every `SKILL.md` defines `name`, `version`, purpose, applies-when conditions,
required inputs, allowed actions, forbidden actions, procedure, required checks,
output contract, failure conditions, and handoff.

All P0 skills are version `1.0.0`. Role contracts require compatible major
version `^1.0`.

## Resolution rules

- Missing required skill -> `BLOCKED`.
- Incompatible major version -> `BLOCKED`.
- Unavailable required skill -> `BLOCKED`.
- Skill/governance conflict -> `BLOCKED`; governance wins.
- A task specification may narrow allowed behavior, never expand authority.
- Silent substitution is forbidden.

These rules are package integrity and handoff rules only. Phase D does not add a
general-purpose package manager or activate runtime routing.

## P0 inventory

Shared: `project-context`, `governance`, `git-safety`, `testing-policy`,
`ai-ip-domain`.

Planner: `task-specification`, `architecture-analysis`.

Implementer: `specification-execution`, `safe-code-change`.

Security: `threat-modeling`, `ai-security`.

Quality: `fixed-sha-review`, `spec-compliance`,
`patent-conversion-review`.

## Validation

Run:

```text
python agents/validate_skills.py
```

The static validator checks exact P0 inventory, standard contract headings,
manifest references, role requirements, governance precedence, and fail-closed
fixtures for missing/incompatible skills.

`RECORDED != VERIFIED`.
`provisional_ready != authoritative_merge_eligible`.
Workflow V2 remains **NOT ACTIVATED**.
