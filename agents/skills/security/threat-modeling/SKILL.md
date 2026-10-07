# Threat Modeling

- name: `threat-modeling`
- version: `1.0.0`
- role_scope: `SECURITY`

Governance takes precedence over this skill. A task specification may narrow its behavior but may not expand authority.

## Purpose

Perform independent threat analysis on the exact review target without remediation.

## Applies when

Security review of a fixed implementation SHA or security-relevant specification.

## Required inputs

- task/spec identity
- base and implementation SHA
- diff/files
- architecture/data/trust-boundary evidence
- relevant tests/CI

## Allowed actions

- identify assets, actors, trust boundaries, abuse cases, attack paths, and mitigations
- classify findings/severity with evidence
- submit SECURITY verdict

## Forbidden actions

- modify tracked implementation
- substitute Quality verdict
- reuse stale-SHA PASS
- waive Human/security/data/provider gates

## Procedure

1. Confirm reviewer independence and exact SHA target.
2. Map assets, entry points, trust boundaries, attacker capabilities, and sensitive data.
3. Review diff/tests against plausible abuse paths and required controls.
4. Record evidence-backed findings, blockers, and SECURITY verdict.

## Required checks

- review target equals exact final SHA
- tracked implementation files were not modified
- material trust boundaries covered
- findings cite concrete evidence

## Output contract

Independent Security review artefact with findings, severity, blockers, verdict, attribution, and exact SHA identities.

## Failure conditions

- review target or evidence identity is ambiguous
- reviewer independence is violated
- required security evidence cannot be inspected

## Handoff

Submit BLOCKED/REQUEST_CHANGES with evidence; Implementer owns remediation and fresh-SHA re-review.
