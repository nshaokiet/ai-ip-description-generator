# Git Safety

- name: `git-safety`
- version: `1.0.0`
- role_scope: `SHARED`

Governance takes precedence over this skill. A task specification may narrow its behavior but may not expand authority.

## Purpose

Keep Git changes isolated, reviewable, reversible, and scoped.

## Applies when

Any role action that reads diffs or modifies tracked repository artefacts.

## Required inputs

- authorized base SHA
- task branch/worktree
- allowed file scope
- current Git status/diff

## Allowed actions

- use an isolated branch/worktree
- inspect history/diff/status
- commit and push authorized changes when role/task allows

## Forbidden actions

- rewrite shared history without explicit Human authorization
- discard unrelated Human/agent changes
- stage or commit files outside authorized scope
- use reviewer role to modify tracked implementation

## Procedure

1. Verify exact base and working tree status before changes.
2. Isolate task work and preserve unrelated files/worktrees.
3. Inspect changed-file allowlist, diff, whitespace, secrets, and task scope before commit.
4. Bind evidence/review to the final immutable implementation SHA.

## Required checks

- base SHA and branch/worktree identity verified
- changed-file set matches scope
- no unrelated or secret material staged
- review target SHA is exact

## Output contract

Git evidence: base SHA, branch/worktree, changed files, final SHA, and validation status.

## Failure conditions

- base mismatch or unresolved conflict
- unrelated tracked changes would be overwritten
- required exact-SHA identity cannot be established

## Handoff

Stop the conflicting Git operation and report the exact mismatch/conflict; preserve all unrelated work.
