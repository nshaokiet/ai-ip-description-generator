# Governance

- name: `governance`
- version: `1.0.0`
- role_scope: `SHARED`

Governance takes precedence over this skill. A task specification may narrow its behavior but may not expand authority.

## Purpose

Apply project authority, stop-condition, evidence, and merge rules consistently.

## Applies when

Any role action that changes artefacts, records evidence, reviews work, or evaluates readiness.

## Required inputs

- authorized task/spec
- current AGENTS.md/governance decisions
- role assignment
- relevant evidence and verification levels

## Allowed actions

- apply existing authority matrix and stop conditions
- classify evidence as UNVERIFIED/RECORDED/VERIFIED when the governing contract supports it
- block or hand off actions that exceed authority

## Forbidden actions

- create Human approval
- promote RECORDED evidence to VERIFIED by repetition or consensus
- treat provisional_ready as merge permission
- waive required review/CI/security/data/provider gates

## Procedure

1. Identify the actor, authorized scope, and action being considered.
2. Evaluate stop conditions and required Human decisions.
3. Preserve RECORDED != VERIFIED and provisional_ready != authoritative_merge_eligible.
4. Allow only actions inside the role and task authority; block the rest with evidence.

## Required checks

- no self-authorization or authority expansion
- all required stop conditions evaluated
- evidence level and provenance are stated

## Output contract

A governance decision for the proposed role action: ALLOW, BLOCKED, or HANDOFF, with governing evidence.

## Failure conditions

- governance sources conflict materially
- required Human decision is absent
- authoritative evidence required by policy cannot be verified

## Handoff

Record the blocker and route only the affected decision to Human/authorized governance authority.
