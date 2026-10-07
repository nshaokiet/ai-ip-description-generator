# Phase D P0 Skill Package

Version: 1.0.1
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

P0 skills use major `1`: shared `governance` and `ai-ip-domain` are `1.0.1`;
the other 12 remain `1.0.0`. Role contracts require compatible major `^1.0`.

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

The static validator checks exact inventory, nonempty contract fields, manifest
targets, strict SemVer, exact role mappings, declared role authority, governance
precedence and AI-IP/P2 safeguards. It is read-only and performs no runtime loading.

Run `python -m unittest discover -s tests -p test_agent_package.py -v` for actual
temporary-copy negative fixtures, including missing/unavailable skills, incompatible
major, governance conflicts, malformed metadata and authority/activation drift.
The existing pytest CI step collects these tests and exercises the committed CLI.

The manifest retains its bounded indented YAML subset. Unsupported YAML constructs
are rejected; no new dependency or general-purpose package manager is introduced.
Static declaration checks do not authenticate provenance or prove prose safe.

Version 1.0.0 -> 1.0.1, 2026-10-07, Codex: authorized PR #89 reconciliation,
document actual validation and additive contract safeguards. Breaking change: No.

`RECORDED != VERIFIED`.
`provisional_ready != authoritative_merge_eligible`.
Workflow V2 remains **NOT ACTIVATED**.
