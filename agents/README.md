# Workflow V2 Agent Role Contracts

Version: 0.1.0
Phase: GOV-AGENT-001-C
Status: IMPLEMENTED FOR REVIEW — NOT ACTIVATED

This package defines the four standing Workflow V2 role contracts requested by
`GOV-AGENT-001`: Planner, Implementer, Security Reviewer, and Quality Reviewer.
The contracts are client/model independent. A compatible client or model may
execute a role only when the surrounding governance and assignment state authorize
that role for the task.

Installing or merging this package does not activate Workflow V2, enroll a task,
assign a role, freeze a specification, authorize implementation, or grant merge
permission. Phase D skills are intentionally absent.

## Role separation

| Role | Primary responsibility | Tracked implementation writes | Independent verdict |
|---|---|---:|---:|
| Planner | Analyze and author/fix the task specification and acceptance criteria | No | No |
| Implementer | Execute the authorized frozen specification in the task branch/worktree | Yes, within authorized scope | No |
| Security Reviewer | Independently review security/privacy risk on the exact implementation SHA | No | Security only |
| Quality Reviewer | Independently review correctness/spec/regression quality on the exact implementation SHA | No | Quality only |

Independence is mandatory:

- Planner rationale is planning context, not proof that implementation is correct.
- Implementer self-review is diagnostic evidence only and cannot become an
  independent Security or Quality PASS.
- Security and Quality reviews are separately authored and attributed.
- Required reviewers target the same immutable final implementation SHA.
- Reviewers do not modify tracked implementation while acting as reviewers.
- A new implementation SHA makes prior applicable review PASS evidence stale.

## Evidence semantics

`RECORDED != VERIFIED`.

`RECORDED` means an authorized workflow actor stored evidence and a provenance
reference. It does not mean the designated authoritative source has verified that
evidence. Multiple agents agreeing cannot promote recorded evidence to verified
evidence.

`provisional_ready != authoritative_merge_eligible`.

`provisional_ready` may show that internally consistent recorded evidence exists.
It is not merge authorization. The Phase B3 implementation deliberately fails
closed: `authoritative_merge_eligible` remains false while approved authoritative
source adapters and the required fresh pre-merge checks are unavailable.

## Existing MCP capability references

These role contracts reference capabilities already delivered by GOV-AGENT-001
Phases B1/B2/B3. They do not add, wrap, or activate new MCP behavior.

- **B1 — V2 data foundation:** additive V2 workflow/assignment/specification,
  implementation, review, CI, and append-only evidence-verification storage.
  Schema availability is not workflow activation.
- **B2 — V2 tools/state:** `project.assign_role`, `project.get_assignments`,
  `project.submit_spec`, `project.freeze_spec`, `project.get_spec`,
  `project.start_implementation`, `project.record_implementation`,
  `project.record_ci`, `review.start`, `review.submit`, `review.get_status`, plus
  additive V2 state in `project.get_state` and role-aware checkpoint metadata.
- **B3 — merge evidence:** `project.get_merge_gate` and the merge-gate snapshot in
  `project.get_state`, including exact-SHA applicability, stale-evidence handling,
  provisional readiness, and fail-closed authoritative eligibility.

The current MCP implementation does not independently authenticate Human/agent
identity or prove Git/CI/review provenance. The role contracts therefore treat MCP
state as operational evidence under the verification level recorded for it.

## Review artefacts

Use `review-templates/security-review.md` and
`review-templates/quality-review.md` to produce durable task-scoped review
artefacts. Each review must identify the exact spec SHA, base SHA, implementation
SHA, evidence inspected, findings, blocking findings, verdict, attribution, and
whether tracked implementation files were modified.

The canonical durable location defined by the GOV-AGENT-001 specification is:

```text
docs/reviews/<TASK-ID>/
├── security-review.md
└── quality-review.md
```

The MCP review row is an operational index/state for that artefact; it does not
replace the durable Git evidence.

## Scope boundary

This Phase C package contains role contracts and review templates only. It does not:

- implement Phase D P0 skills;
- activate Workflow V2;
- change budget/quota behavior;
- add provider/API/network integrations;
- change application, backend, or frontend behavior;
- grant merge authority outside existing governance.

Activation remains a later Human-authorized governance phase.
