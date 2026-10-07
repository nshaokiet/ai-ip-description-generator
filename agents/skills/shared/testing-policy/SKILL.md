# Testing Policy

- name: `testing-policy`
- version: `1.0.0`
- role_scope: `SHARED`

Governance takes precedence over this skill. A task specification may narrow its behavior but may not expand authority.

## Purpose

Select, run, and report proportionate validation without fabricating results.

## Applies when

Implementation and review tasks with acceptance criteria or regression risk.

## Required inputs

- task acceptance criteria
- changed-file/diff scope
- available test/lint/build/static checks
- known risk class

## Allowed actions

- choose focused checks tied to changed behavior
- run applicable repository checks
- record skipped/unavailable checks with reasons

## Forbidden actions

- claim PASS for a check that did not run
- substitute self-review for required independent review
- hide failing, pending, or contradictory CI/test evidence

## Procedure

1. Map acceptance criteria and risk to relevant checks.
2. Run focused checks first, then applicable repository regression checks.
3. Record command/check identity, result, and exact SHA where relevant.
4. Treat failure or unavailable required validation as a blocker.

## Required checks

- each material acceptance criterion has evidence
- required CI/review remains separate from local checks
- failed/pending results are preserved

## Output contract

A validation matrix of checks, results, evidence references, and unresolved gaps.

## Failure conditions

- required check fails
- required validation cannot run and no approved exception exists
- results cannot be tied to the intended artefact/SHA

## Handoff

Return failed/unavailable checks to Implementer or Human exception authority; do not claim completion.
