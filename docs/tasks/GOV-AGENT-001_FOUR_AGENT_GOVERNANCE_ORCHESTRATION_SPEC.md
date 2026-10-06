# GOV-AGENT-001 — Four-Agent Governance & Orchestration Migration

## 1. Metadata

| Field | Value |
|---|---|
| Task ID | `GOV-AGENT-001` |
| Version | `0.1.0` |
| Status | **READY FOR INDEPENDENT SPECIFICATION REVIEW** |
| Phase | **SPECIFICATION ONLY** |
| Owner | Human / Product Owner |
| Authoring role | Planner / Architecture & Governance Specification Agent |
| Authorization reference | Human task instruction for `GOV-AGENT-001`, 2026-10-06; no separate canonical authorization ID was supplied |
| Repository baseline SHA | `009e1320405a8d956510c4a11a73f6626acec281` |
| Breaking change | **No for this specification-only task.** Future Workflow V2 governance activation is a breaking governance change and requires separate authorization/review. |
| Confidentiality | Internal; research inputs remain Confidential by default under current governance |
| Intended activation boundary | Future `WORKFLOW_V2_ACTIVATION_COMMIT`; **not defined or activated by this task** |
| Preferred execution profile | GPT-5.6 Sol High may be used as an execution policy; role identity remains client/model independent |

Evidence baseline: `AGENTS.md`, `PROJECT_CONTEXT.md`, `docs/system-specification.md`, `docs/workflow.md`, `docs/operations/01_PROJECT_CONTROL_CENTER.md`, `docs/operations/02_GEMINI_REVIEW_LOG.md`, `docs/operations/AUTONOMOUS_AGENT_PROTOCOL.md`, P2 task/ADR records, and `tools/project-orchestrator-mcp/` source/tests at the repository baseline above. GitHub `main` was independently observed at the same SHA before authoring.

## 2. Executive Summary

The current project workflow is a Human-governed, Codex-centered implementation lifecycle with one aggregate independent read-only reviewer role and Project Orchestrator MCP as a coordination/state layer. It already has strong fixed-SHA review, evidence-backed merge eligibility, task leases, checkpoints, and durable Git governance records. It does not have first-class Planner, Implementer, Security Reviewer, and Quality Reviewer assignments, frozen specification records, two independent review streams, CI evidence records, or a computed merge gate.

Workflow V2 should therefore be an **additive, prospective governance migration**, not a rewrite of the product or a destructive MCP replacement. The recommended design keeps the compact task-level lifecycle, adds separate spec/assignment/implementation/review/CI records, computes merge readiness from evidence, preserves Git as durable technical evidence, and keeps Human authority above the orchestration layer.

This document defines the future architecture only. It does not implement MCP V2, agents, skills, runtime behavior, database changes, CI changes, or governance activation.

## 3. Current Workflow V1

### 3.1 Evidence-grounded operating model

| Capability | Current classification | Evidence / interpretation |
|---|---|---|
| Human / Product Owner governance and exception authority | **EXISTS / MUST BE PRESERVED** | `AGENTS.md` §§3–5, 8, 19 |
| ChatGPT technical coordination / architecture advisory | **EXISTS / MUST BE PRESERVED** | `AGENTS.md` §5 |
| Codex primary implementation/integration ownership | **EXISTS / MUST BE PRESERVED until V2 cutover** | `AGENTS.md` §§5, 8, 10–11 |
| Antigravity independent read-only review role | **EXISTS / LEGACY ROLE MODEL** | `AGENTS.md` §§6, 11–12 |
| Project Orchestrator MCP coordination/state role | **EXISTS / MUST BE PRESERVED** | `AGENTS.md` §7; MCP README/source |
| Standing delegation for an explicitly authorized task | **EXISTS / MUST BE PRESERVED** | `AGENTS.md` §8.1 |
| Evidence-backed merge eligibility | **EXISTS / MUST BE PRESERVED** | `AGENTS.md` §8.2 |
| Independent fixed-SHA review | **EXISTS / MUST BE PRESERVED** | `AGENTS.md` §§6, 8.2, 11 |
| Separate Security and Quality reviewer streams | **DOES NOT EXIST** | Current governance has one aggregate independent reviewer role |
| First-class frozen spec state in MCP | **DOES NOT EXIST** | No spec table/tool in current MCP |
| Role-based multi-agent assignment model | **DOES NOT EXIST** | Current ownership is a single `tasks.owner` lease |
| CI evidence as first-class MCP record | **DOES NOT EXIST** | CI is external evidence recorded in governance/task text |
| Deterministic computed merge gate | **DOES NOT EXIST** | Current merge eligibility is governance-defined and manually evidenced |
| Historical Review Log | **EXISTS / LEGACY / MUST BE PRESERVED** | `docs/operations/02_GEMINI_REVIEW_LOG.md` |

### 3.2 Current lifecycle

Current governance is effectively:

```text
Human authorization/delegation
  -> Codex claim / implement / test / PR
  -> Antigravity independent fixed-SHA review
  -> Codex remediation + re-review if needed
  -> review PASS + required CI + merge eligibility
  -> Codex merge under standing delegation
  -> post-merge verification / governance closeout
```

The Human remains the authority for new task scope, exceptions, breaking changes, provider/model policy, production, security/data-policy boundaries, paid services, real/confidential research data, and other stop conditions in `AGENTS.md` §19.

### 3.3 Active-work protection and historical status

The baseline SHA `009e1320405a8d956510c4a11a73f6626acec281` is the GitHub `main` merge commit for PR #82 (P2-004 implementation). GOV-AGENT-001 does not modify or reinterpret P2-001/P2-002/P2-003/P2-004 technical contracts, review evidence, task records, or historical approvals. Any stale status sentence contained inside an older artefact remains historical evidence rather than a reason to rewrite that artefact in this specification task.

Workflow V2 is prospective. Every task whose governing authorization/review history predates `WORKFLOW_V2_ACTIVATION_COMMIT` remains a Workflow V1 historical record unless the Human explicitly authorizes a bounded migration of that task.

## 4. Current MCP Architecture

The current `tools/project-orchestrator-mcp` package is version `0.1.0` and uses SQLite as an operational coordination store.

### 4.1 Current task states

The source defines 12 states in `src/store.ts`:

`PLANNED`, `APPROVED`, `CLAIMED`, `IN_PROGRESS`, `IMPLEMENTED`, `AWAITING_REVIEW`, `REVIEW_CHANGES_REQUIRED`, `REVIEW_PASS`, `AWAITING_HUMAN_APPROVAL`, `MERGED`, `COMPLETED`, `BLOCKED`.

### 4.2 Current tables

Exactly five tables are created by current store initialization:

1. `tasks`
2. `dependencies`
3. `budget`
4. `progress`
5. `checkpoints`

Initialization is non-destructive (`CREATE TABLE IF NOT EXISTS`, seed behavior using `INSERT OR IGNORE`). Foreign keys are enabled. Transactions use `BEGIN IMMEDIATE`; the database configures `busy_timeout=5000` and WAL mode.

### 4.3 Ownership, lease, concurrency

Current assignment is single-owner: `tasks.owner` plus one `branch` and one `worktree`. Claim leases default to 60 minutes and accept 1–1440 minutes. Expired `CLAIMED`/`IN_PROGRESS` leases are atomically returned to `APPROVED`. Concurrent branch/worktree collisions are rejected. Existing tests verify that only one claimant succeeds across concurrent processes. The lease coordinates agents; it is not an operating-system lock or an identity proof.

### 4.4 Current MCP tools

The stdio server exposes 13 tools:

`project.get_state`, `project.next_task`, `project.claim_task`, `project.renew_lease`, `project.release_task`, `project.report_progress`, `project.finish_task`, `budget.get`, `budget.set_remaining`, `budget.should_continue`, `checkpoint.create`, `checkpoint.get_latest`, `project.stop_and_handoff`.

Administrative approval/evidence-backed transitions exist in local admin code, not as general MCP tools.

### 4.5 Budget guard

The current singleton budget row is seeded manually at remaining `14`, threshold `8`. `remaining > 8` yields `CONTINUE`; `remaining <= 8` yields `STOP_AND_CHECKPOINT`. The guard blocks claim/progress/finish while still permitting checkpoint/handoff. Current tests verify the strict threshold and persistence.

### 4.6 Current limitations

Current MCP has no role assignment model, spec freeze model, separate Security/Quality review model, CI evidence table, computed merge gate, Git fact verification, authentication, cryptographic identity, or provider integration. Human refs, SHAs, branches, test reports, and status evidence are trust-based inputs. MCP does not itself merge Git, call providers, or prove that a supplied SHA/CI/review reference is genuine.

Current seeded task catalog is also incomplete for later P2 tasks; historical governance records correctly preserve observed `Unknown task: P2-00x` as `BLOCKED BY TOOL CAPABILITY` rather than fabricating MCP state.

## 5. Problems / Gaps

The V1 model has five material gaps for the requested architecture:

1. A single owner field conflates implementation ownership with role assignment and cannot represent independent Planner/Security/Quality work cleanly.
2. Specification approval/freeze is represented in Git/governance prose but not as first-class operational state.
3. One aggregate reviewer cannot encode two independent verdict streams or their exact-SHA staleness separately.
4. CI and merge-readiness evidence are manually reconciled rather than computed from structured evidence.
5. Weekly quota/budget logic is currently coupled to task execution and can block future work even when quota is no longer a workflow constraint.

The migration must close these gaps without duplicating Git as a competing source of truth or retroactively rewriting historical evidence.

## 6. Goals

- Define four stable roles with explicit authority boundaries.
- Preserve Human governance and stop conditions.
- Preserve fixed-SHA review semantics and improve review independence.
- Add a frozen-spec contract before implementation.
- Define additive MCP V2 records for assignments, specs, implementation evidence, reviews, and CI.
- Compute merge readiness deterministically from required evidence.
- Route review effort by task risk R0–R4.
- Define a minimal agent/skill package that can run across clients/models.
- Preserve current SQLite data, Git history, Review Log, checkpoints, and task evidence.
- Define reversible phased activation and a non-production pilot before AI-CONV adoption.

## 7. Non-Goals

This specification does not implement or authorize:

- MCP TypeScript or SQLite changes;
- agent runtimes, manifests, skills, prompts, or tool implementations;
- backend/frontend/application/AI runtime changes;
- prompt/schema/DOCX/CI changes;
- provider/API calls or provider/model policy changes;
- real/confidential research-data use;
- production/public release changes;
- P2 contract changes or Claims runtime integration;
- Workflow V2 activation in `AGENTS.md` or `AUTONOMOUS_AGENT_PROTOCOL.md`;
- AI-CONV or any downstream implementation task.

## 8. Design Principles

1. **Human authority remains supreme.** MCP and agent roles record/enforce authorized workflow but do not create authorization.
2. **Git is durable technical evidence.** Specifications, implementation commits, review artefacts, and governance decisions remain reviewable in repository history.
3. **MCP is operational state/index.** It accelerates coordination but is not the sole permanent evidence store.
4. **Additive migration first.** Existing tables/fields remain readable; no reset or destructive history rewrite.
5. **Task state stays compact.** Spec, assignment, review, and CI details live in sub-state records to avoid state explosion.
6. **Review is exact-SHA and independent.** A new implementation SHA stales prior applicable PASS evidence.
7. **Role != skill != task spec.** Stable authority, reusable procedure, and task-specific requirements remain separate.
8. **Client/model independence.** Model/profile is execution metadata, not agent identity.
9. **Least privilege.** Planner/reviewers do not edit tracked implementation in their role.
10. **Reversibility.** Activation and rollback do not require deleting V2 data.

## 9. Target Four-Agent Architecture

| Role | Primary responsibility | Tracked implementation write authority | Independent verdict authority |
|---|---|---:|---:|
| Planner Agent | Analyze repository, classify risk, author/fix task spec and acceptance criteria | No | No |
| Implementer Agent | Execute frozen authorized spec, code/tests/remediation/handoff | Yes, authorized task branch/worktree only | No |
| Security Reviewer Agent | Independent security/privacy/threat review on fixed SHA | No | Security verdict only |
| Quality Reviewer Agent | Independent correctness/spec/regression/domain review on fixed SHA | No | Quality verdict only |

The Human authorizes scope/exceptions and approves any gate explicitly reserved to Human authority. The orchestration layer coordinates roles and evidence. No role gains powers beyond current repository governance merely because it exists in Workflow V2.

## 10. Planner Agent Contract

**Responsibilities:** repository/architecture analysis, task decomposition, specification authoring, acceptance criteria, risk classification, security/test/migration/rollback requirements.

**May read:** repository, Git history, tests, governance, MCP operational state, authorized evidence.

**May write:** only authorized specification/governance artefacts for the planning task.

**Must produce:** versioned spec, risk class, required gates, required skills, dependencies, explicit non-goals, rollback/test strategy, and implementation handoff.

**Forbidden:** application/MCP implementation, implementation self-approval, independent implementation verdict, or merging implementation because it authored the spec.

**Freeze rule:** Planner may submit revisions until the authorized spec is frozen. A frozen spec can only be superseded through an explicit versioned re-planning path; it is not edited in place.

## 11. Implementer Agent Contract

**Responsibilities:** execute the authorized frozen spec, own the task worktree/branch, code, tests, debugging, evidence capture, and remediation.

**May read:** full repository and frozen task evidence.

**May write:** files allowed by the frozen specification in the authorized branch/worktree.

**Must preserve:** scope, current source-of-truth contracts, test evidence, review SHA identity, and unrelated worktrees/files.

**Forbidden:** silently changing frozen requirements; recording Security/Quality PASS for its own implementation; using self-review as independent approval; bypassing CI/review gates; broadening scope without authorization.

If the frozen spec is contradictory, incomplete, infeasible, or requires an unauthorized exception, implementation enters `SPEC_BLOCKED` sub-state and hands back to Planner/Human. `SPEC_BLOCKED` is a spec/assignment condition, not a new top-level task state.

## 12. Security Reviewer Contract

Security Reviewer performs independent read-only review of the exact final implementation SHA. Applicable domains include file upload and malformed PDF/DOCX/package abuse, path traversal, parser/resource exhaustion, prompt injection, instruction/data boundary, model/provider security, confidential IP handling, secret leakage, logging/filesystem controls, auth/authz, IDOR, CSRF, CORS, XSS, SSRF, rate limiting, dependencies, and runtime hardening.

It may create only its authorized review artefact and/or submit review state through orchestration. It must not remediate tracked implementation. Findings must cite concrete diff/file/test/evidence. Its verdict is `PASS`, `REQUEST_CHANGES`, or `BLOCKED`; severity is recorded separately.

## 13. Quality Reviewer Contract

Quality Reviewer independently reviews the exact final implementation SHA for specification compliance, correctness, architecture, regression, compatibility, test adequacy, API/schema behavior, failure handling, maintainability, and scope discipline.

For R3 AI/conversion work, review also covers source fidelity, evidence preservation, invention-boundary correctness, prior-art vs inventor-contribution separation, unsupported inference, technical relationships, terminology, missing-information behavior, and end-to-end traceability from paper to evidence to invention reconstruction to patent draft.

It is read-only for tracked implementation, may create only its authorized review artefact and/or submit review state, and must not remediate code directly.

## 14. Agent Independence Model

Security and Quality reviews are separate evidence streams. Both reviewers receive the frozen spec, base SHA, final implementation SHA, diff/files, and relevant test/CI evidence. Neither reviewer must wait for or consume the other's verdict before forming its own conclusion.

Minimum independence rules:

- Implementer self-review is diagnostic evidence only, never independent approval.
- Planner rationale is context, never proof that implementation satisfies the spec.
- Security and Quality verdicts are independently authored and attributed.
- Both required reviews target the same immutable final implementation SHA.
- Reviewers do not modify tracked implementation in reviewer role.
- A remediation commit creates a new final SHA and stales all applicable prior review PASS records and prior mismatched CI evidence.
- Re-review is mandatory for each required review type after implementation SHA changes.
- The same underlying model family may be used across roles if operationally necessary, but role/session separation and independent verdict formation remain required; stronger provider/model diversity can be added later as policy, not architecture identity.

## 15. Risk Classification & Routing

The proposed R0–R4 scale fits this repository because its historical tasks range from documentation reconciliation to application/UI work, AI/patent transformation contracts, and deployment/confidential-data boundaries.

| Risk | Typical scope | Planner | Implementer | CI | Quality | Security | Human gate |
|---|---|---|---|---|---|---|---|
| R0 | Docs/metadata/evidence-only | Planner-lite | Required for edits | CI-lite / applicable validation | Quality-lite independent check | Optional | Existing governance only |
| R1 | Low-risk isolated code/tooling | Required | Required | Required | Required | Optional unless threat surface changes | Existing governance only |
| R2 | Application functionality | Required | Required | Required | Required | Conditional: mandatory when auth/input/network/storage/security surface changes | Existing stop conditions |
| R3 | AI/conversion/patent pipeline | Required | Required | Required | **Mandatory** | **Mandatory** | Existing Human scope/provider/data/legal gates |
| R4 | Security, production, confidential data, auth, deployment boundary | Required | Required | Required | **Mandatory** | **Mandatory** | **Explicit Human exception/approval where current governance requires it** |

`Planner-lite`, `Quality-lite`, and `CI-lite` reduce depth, not independence or evidence integrity. Risk can only be raised automatically; lowering an initially assigned risk class requires Planner justification and any Human decision required by governance.

## 16. Workflow V2 State Model

Recommendation: **keep a compact task-level lifecycle and add separate spec/assignment/review/CI sub-state.** Do not replace the existing task state enum wholesale and do not encode every reviewer combination as a task state.

```text
TASK LEVEL (compatible with V1)

PLANNED
  -> APPROVED
  -> CLAIMED / IN_PROGRESS
  -> IMPLEMENTED
  -> AWAITING_REVIEW
       |-- any required review REQUEST_CHANGES --> REVIEW_CHANGES_REQUIRED
       |                                             |
       |                                             +-> APPROVED/IN_PROGRESS
       |                                                   -> NEW SHA -> CI/reviews again
       |
       +-- all required reviews PASS + CI PASS + all gates true
              -> REVIEW_PASS  [merge gate reports READY_TO_MERGE=true]
              -> AWAITING_HUMAN_APPROVAL only when a Human gate is actually required
              -> MERGED
              -> COMPLETED

Any unrecoverable/current stop condition -> BLOCKED

SPEC SUB-STATE
DRAFT -> READY -> FROZEN -> SUPERSEDED (only by explicit newer version)

REVIEW SUB-STATE, per required review type and implementation SHA
NOT_STARTED -> IN_PROGRESS -> PASS | REQUEST_CHANGES | BLOCKED
```

Planning/spec readiness are represented in `task_specs` and assignments rather than proliferating top-level task states. `READY_TO_MERGE` is a computed result, not a manually writable task state.

## 17. MCP V2 Data Model

V2 is additive to the five current tables. Existing rows remain untouched and readable.

### 17.1 `task_workflow`

Purpose: opt a task into V2 prospectively.

- `task_id TEXT PRIMARY KEY REFERENCES tasks(id)`
- `workflow_version TEXT NOT NULL` (initial V2 value `2`)
- `risk_class TEXT NOT NULL CHECK IN ('R0','R1','R2','R3','R4')`
- `authorization_ref TEXT NOT NULL`
- `activation_commit TEXT NOT NULL`
- `created_at INTEGER NOT NULL`

No row means legacy/V1 behavior. This avoids rewriting old task rows.

### 17.2 `task_assignments`

- `id INTEGER PRIMARY KEY AUTOINCREMENT`
- `task_id TEXT NOT NULL REFERENCES tasks(id)`
- `role TEXT NOT NULL CHECK IN ('PLANNER','IMPLEMENTER','SECURITY_REVIEWER','QUALITY_REVIEWER')`
- `agent_id TEXT NOT NULL`
- `status TEXT NOT NULL` (`ASSIGNED`,`ACTIVE`,`COMPLETED`,`RELEASED`,`BLOCKED`)
- `assignment_version INTEGER NOT NULL`
- `assigned_at INTEGER NOT NULL`, `started_at`, `completed_at`
- `branch TEXT`, `worktree TEXT`, `lease_start`, `lease_expiry` only where the role needs a lease
- `UNIQUE(task_id, role, assignment_version)`
- partial unique index preventing more than one `ASSIGNED`/`ACTIVE` assignment for the same `(task_id, role)`

Implementer is the only role allowed to own the implementation branch/worktree lease. Planner/reviewer records may identify an authorized review/spec checkout but must not seize implementation ownership.

### 17.3 `task_specs`

- `id INTEGER PRIMARY KEY AUTOINCREMENT`
- `task_id TEXT NOT NULL REFERENCES tasks(id)`
- `spec_version TEXT NOT NULL`
- `spec_sha TEXT NOT NULL`
- `status TEXT NOT NULL CHECK IN ('DRAFT','READY','FROZEN','SUPERSEDED')`
- `authorization_ref TEXT NOT NULL`
- `artifact_path TEXT NOT NULL`
- `created_at INTEGER NOT NULL`, `frozen_at`, `superseded_at`
- `UNIQUE(task_id, spec_version)` and `UNIQUE(task_id, spec_sha)`
- partial unique index allowing at most one current `FROZEN` spec per task

A frozen row is immutable. A requirement change creates a new version and marks the prior frozen row `SUPERSEDED` in one transaction after proper authorization.

### 17.4 `implementation_evidence`

- `id INTEGER PRIMARY KEY AUTOINCREMENT`
- `task_id TEXT NOT NULL REFERENCES tasks(id)`
- `spec_sha TEXT NOT NULL`
- `base_sha TEXT NOT NULL`
- `implementation_sha TEXT NOT NULL`
- `evidence_ref TEXT`
- `recorded_by_assignment_id INTEGER REFERENCES task_assignments(id)`
- `created_at INTEGER NOT NULL`
- `UNIQUE(task_id, implementation_sha)`

This table preserves remediation history rather than overwriting one commit field.

### 17.5 `reviews`

- `id INTEGER PRIMARY KEY AUTOINCREMENT`
- `task_id TEXT NOT NULL REFERENCES tasks(id)`
- `review_type TEXT NOT NULL CHECK IN ('SECURITY','QUALITY')`
- `reviewer_assignment_id INTEGER NOT NULL REFERENCES task_assignments(id)`
- `spec_sha TEXT NOT NULL`, `base_sha TEXT NOT NULL`, `reviewed_sha TEXT NOT NULL`
- `attempt INTEGER NOT NULL`
- `verdict TEXT NOT NULL CHECK IN ('PASS','REQUEST_CHANGES','BLOCKED')`
- `findings_ref TEXT NOT NULL`, `artifact_path TEXT NOT NULL`
- `model_profile TEXT`, `created_at INTEGER NOT NULL`
- `tracked_files_modified INTEGER NOT NULL CHECK IN (0,1)`
- `UNIQUE(task_id, review_type, reviewed_sha, attempt)`

Old PASS rows are retained. They become **stale by computation** when `reviewed_sha != current final implementation SHA`; they are not deleted or rewritten.

### 17.6 `ci_evidence`

- `id INTEGER PRIMARY KEY AUTOINCREMENT`
- `task_id TEXT NOT NULL REFERENCES tasks(id)`
- `implementation_sha TEXT NOT NULL`
- `status TEXT NOT NULL CHECK IN ('PENDING','SUCCESS','FAILURE','CANCELLED','UNKNOWN')`
- `reference TEXT NOT NULL`
- `source TEXT NOT NULL`
- `created_at INTEGER NOT NULL`
- `UNIQUE(task_id, reference)`

MCP stores supplied evidence. Until a separately authorized Git/CI verification capability exists, the trust model must label external references as recorded rather than independently verified.

### 17.7 Transaction/concurrency requirements

Assignment activation, spec freeze/supersession, implementation finalization, and review submission use `BEGIN IMMEDIATE` transactions and retain the existing `busy_timeout`/WAL approach. Multi-row transitions must commit atomically. Merge-gate reads execute from one consistent transaction/snapshot. Concurrent incompatible role assignment or duplicate freeze attempts fail deterministically.

## 18. MCP V2 Tool Contracts

These are **proposed contracts only**.

| Tool | Purpose / caller | Inputs | Outputs | State / idempotency / validation / failure |
|---|---|---|---|---|
| `project.get_state` | Read combined task/sub-state; any authorized role/Human client | `task_id?` | Task + workflow/risk + assignments + frozen spec + final SHA + review/CI summaries + merge gate | Read-only, idempotent. V1 task returns legacy shape plus `workflow_version=1`; unknown task remains explicit error. |
| `project.assign_role` | Assign one V2 role; Human/admin/orchestrator authority | `task_id, role, agent_id, authorization_ref, lease metadata?` | Assignment record | No task lifecycle transition. Reject V1 task without explicit V2 enrollment, incompatible active assignment, invalid role, missing authorization. Retry with same unique assignment request returns existing record. |
| `project.get_assignments` | Inspect role ownership; authorized roles/Human | `task_id` | Assignment history/current assignments | Read-only, idempotent. |
| `project.submit_spec` | Register versioned draft/ready spec; Planner | `task_id, spec_version, spec_sha, artifact_path, authorization_ref` | Spec record | No implementation start. Idempotent on same `(task,version,sha)`; reject version collision with different SHA, missing Planner assignment, malformed SHA/reference. |
| `project.freeze_spec` | Freeze authorized spec; Human/admin path or delegated governance actor only | `task_id, spec_version, spec_sha, approval_ref` | Frozen spec record | `READY -> FROZEN`. Atomic; same freeze is idempotent. Reject SHA/version mismatch, already different frozen spec, missing approval authority. |
| `project.get_spec` | Read current/history; all authorized roles | `task_id, version?` | Spec record(s) | Read-only. |
| `project.start_implementation` | Start implementation against frozen spec; Implementer | `task_id, implementer_assignment_id, spec_sha, branch, worktree, lease_minutes?` | Active implementation assignment/lease | Task `APPROVED/CLAIMED -> IN_PROGRESS` as compatible with existing flow. Reject non-frozen spec, wrong role, lease collision, stop condition, invalid branch/worktree. Same active lease request is idempotent. |
| `project.record_implementation` | Record candidate/final immutable SHA; Implementer | `task_id, spec_sha, base_sha, implementation_sha, evidence_ref` | Implementation evidence + stale-gate summary | Task may become `IMPLEMENTED`. New SHA makes prior mismatched CI/review PASS stale by computation. Reject wrong role/spec mismatch/malformed SHA. Same SHA is idempotent. |
| `project.record_ci` | Record external CI evidence; Implementer/automation/admin according to policy | `task_id, implementation_sha, status, reference, source` | CI record + current match flag | Does not fabricate verification. Duplicate reference with identical payload is idempotent; conflicting reuse fails. SHA mismatch remains stored but cannot satisfy gate. |
| `review.start` | Start independent review; assigned Security or Quality Reviewer | `task_id, review_type, assignment_id, spec_sha, base_sha, reviewed_sha` | Review attempt token/record | `NOT_STARTED -> IN_PROGRESS`; no task-level PASS. Reject role/type mismatch, implementation SHA mismatch, reviewer=Implementer assignment, missing required artefacts. Same active attempt idempotent. |
| `review.submit` | Submit verdict/evidence; assigned reviewer only | `review_id, verdict, findings_ref, artifact_path, model_profile?, tracked_files_modified` | Immutable review result + gate summary | `IN_PROGRESS -> PASS/REQUEST_CHANGES/BLOCKED`. Reject reviewer/type mismatch, changed reviewed SHA, missing artefact/evidence, `tracked_files_modified=1` for reviewer role. Submitted review immutable; correction requires new attempt. |
| `review.get_status` | Read per-type current/stale history; any authorized role | `task_id, reviewed_sha?` | Security/Quality statuses and stale flags | Read-only. |
| `project.get_merge_gate` | Compute readiness; Implementer/Human/authorized coordinator | `task_id` | `ready`, required/observed gates, exact SHAs, blockers, Human gates | Pure computation/read; idempotent. Must never write `READY_TO_MERGE` manually. |
| `checkpoint.create` | Preserve resumable evidence; assigned active role | Existing checkpoint fields + `role/assignment_id` in V2 | Checkpoint record | Keep legacy behavior; quota must not block checkpoint. Role must match assignment when V2. |
| `checkpoint.get_latest` | Resume state; authorized role | `task_id, role?` | Latest compatible checkpoint | Read-only; legacy checkpoints remain readable. |

Authorization assumptions: MCP trusts authenticated/authorized caller context only to the extent future implementation actually provides it. Until identity/authentication is implemented, `agent_id`, role, Human authorization refs, Git SHAs, CI refs, and review artefacts are **trust-based recorded claims** subject to repository/Git verification by workflow policy.

## 19. Fixed-SHA & Review Invariants

For every task, let `F` be the current final implementation SHA, `C` the SHA referenced by satisfying CI, `S` the satisfying Security review SHA when required, and `Q` the satisfying Quality review SHA when required.

For R3/R4:

```text
C == S == Q == F
```

For lower risk classes, omit review types that routing explicitly marks non-required; every required evidence item still equals `F`.

Additional invariants:

- `F` must reference the frozen `spec_sha` recorded for the implementation attempt.
- A new implementation SHA never inherits PASS from an older SHA.
- A CI PASS on a different SHA is visible history but cannot satisfy the gate.
- Review artefacts are immutable evidence; re-review creates a new attempt.
- A spec change after implementation start requires a new frozen spec version and reimplementation/revalidation decision; it cannot silently retarget existing PASS evidence.
- Governance exceptions must be explicit, Human-authorized, bounded, and durable; absence of a required review is never inferred as waived.

## 20. Merge Gate

`READY_TO_MERGE` is a computed condition returned by `project.get_merge_gate`, not an agent-declared status.

For a typical R3/R4 task:

```text
merge_ready =
  workflow_v2_active_for_task
  AND human_task_authorization_present
  AND frozen_spec_present
  AND final_implementation_sha_present
  AND ci_success_sha == final_implementation_sha
  AND security_required_and_pass_sha == final_implementation_sha
  AND quality_required_and_pass_sha == final_implementation_sha
  AND no_blocking_findings
  AND no_unresolved_stop_condition
  AND no_scope_violation
  AND no_known_secret_or_confidential_data_exposure
  AND branch_pr_premerge_state_validated_by_required_external/process evidence
  AND all_required_human_exception_gates_satisfied
```

For R0–R2, the routing matrix determines whether Security is required. Quality remains required at an appropriate depth. MCP must expose which gates are required, satisfied, stale, missing, or externally unverified.

MCP metadata alone cannot prove Git SHA existence, GitHub PR state, CI success, Human authorization, merge status, or review truth unless separately authorized verification integrations are later implemented.

## 21. Agent Role Package

Future repository layout:

```text
agents/
├── README.md                         # CREATE in Phase C
├── manifest.yaml                     # CREATE in Phase C
├── roles/
│   ├── planner.md                    # CREATE in Phase C
│   ├── implementer.md                # CREATE in Phase C
│   ├── security-reviewer.md          # CREATE in Phase C
│   └── quality-reviewer.md           # CREATE in Phase C
├── skills/
│   ├── shared/                       # CREATE in Phase C
│   ├── planner/                      # CREATE in Phase C
│   ├── implementer/                  # CREATE in Phase C
│   ├── security/                     # CREATE in Phase C
│   └── quality/                      # CREATE in Phase C
└── review-templates/                 # CREATE in Phase C
```

`ROLE` defines stable responsibility/authority. `SKILL` defines a reusable procedure. `TASK SPEC` defines one authorized task's requirements and acceptance criteria. Role files reference skills; they do not duplicate all project governance into giant prompts.

## 22. Skill Architecture

### 22.1 Standard contract

Every skill package must define at least:

`name`, `version`, `purpose`, `applies_when`, `required_inputs`, `allowed_actions`, `forbidden_actions`, `procedure`, `required_checks`, `output_contract`, `failure_conditions`, `handoff`.

Skills use explicit semantic versions. A role manifest pins a compatible major version/range. A frozen task spec may pin an exact skill version when deterministic procedure identity matters.

Resolution rules:

- Missing required skill -> assignment is `BLOCKED`; hand off, do not silently substitute.
- Incompatible versions -> `BLOCKED` until Planner/Human resolves the contract.
- Unavailable required skill -> task cannot claim completion for that gate.
- Skill/governance conflict -> governance wins; record the conflict and handoff.
- Task spec may narrow a skill's allowed behavior but may not expand authority beyond governance.

### 22.2 P0 shared skills for activation

- `project-context`
- `governance`
- `git-safety`
- `testing-policy`
- `ai-ip-domain`

### 22.3 Role-specific P0 inventory

**Planner:** `repository-analysis`, `task-specification`, `risk-classification`. Architecture/migration planning is initially part of `task-specification` to avoid skill sprawl.

**Implementer:** `specification-execution`, `safe-code-change`, `implementation-handoff` (including regression protection/testing routing).

**Security:** `threat-modeling`, `security-review-core`. File-upload, web/API, AI/prompt, confidential-IP, and dependency checks are modules/checklists under the core skill initially.

**Quality:** `fixed-sha-review`, `spec-compliance`, `regression-review`; `patent-conversion-review` is P0 for R3 AI-IP tasks.

Additional narrow skills are **FUTURE / OPTIONAL** until repeated use demonstrates a need.

## 23. AI-IP Shared Domain Skill

`ai-ip-domain` is a shared P0 skill for Planner, Implementer, Security Reviewer, and Quality Reviewer when work touches scientific-paper-to-patent conversion.

It must preserve current project principles and terminology:

- Scientific paper != patent.
- Prior art != inventor contribution.
- Experimental result != automatically an inventive feature.
- `INFERENCE` != `SOURCE_FACT`.
- Unsupported technical content must not silently become patent disclosure.
- Critical chain: **Scientific Paper -> Evidence -> Invention Reconstruction -> Patent Draft**.
- P2-002 structured reconstruction/evidence authority, P2-003 draft-specification boundaries, and P2-004 supported-draft-claims boundaries remain versioned contracts; a workflow skill does not rewrite them.
- Human review/legal disclaimers and missing-information behavior remain explicit.

The skill may teach how to inspect and preserve these contracts. It must not invent a parallel ontology or grant broader Claims/provider/runtime authority.

## 24. Review Artefact Model

Historical `docs/operations/02_GEMINI_REVIEW_LOG.md` remains preserved and append-oriented for V1 history. Workflow V2 should use task-scoped durable artefacts:

```text
docs/reviews/<TASK-ID>/
├── security-review.md
└── quality-review.md
```

Each review records: task ID, review type, reviewer role/agent, model/profile where relevant, spec SHA, base SHA, implementation SHA, files/diff reviewed, tests/evidence inspected, findings with severity/evidence, blocking findings, verdict, timestamp/reference, and whether tracked implementation files were modified.

The Git review artefact is canonical durable evidence. The MCP `reviews` row is its operational index/state. Historical Antigravity reviews are never retroactively relabeled as Security or Quality reviews and never fabricated into missing streams.

## 25. Client / Model Independence

The architecture names roles, contracts, evidence, and permissions rather than products. Any compatible client/session can execute a role:

```text
client/session A -> Planner
client/session B -> Implementer
client/session C -> Security Reviewer
client/session D -> Quality Reviewer
```

`agent_id` identifies an execution actor/session according to available identity mechanisms. `model_profile` is metadata on assignments/reviews/checkpoints. The preferred current profile `GPT-5.6 Sol High` may be recorded there, but no state transition, permission, table, or skill path depends on that model name.

## 26. Quota/Budget Legacy Migration

The current budget guard is **LEGACY** for Workflow V2 execution control but its history must remain preserved.

Recommended staged deprecation:

1. **Stage Q0 — Current V1:** keep `budget <= threshold -> STOP_AND_CHECKPOINT` unchanged for V1 tasks.
2. **Stage Q1 — V2 compatibility:** V2 task routing reads budget metadata but does not block claim/progress/finish unless an explicit `resource_policy` for that task says budget-enforced. Log a compatibility warning when the legacy threshold is crossed.
3. **Stage Q2 — Explicit resource policy:** introduce policy values such as `INFORMATIONAL` and `ENFORCED`; new V2 tasks default to `INFORMATIONAL` only after governance activation authorizes that default.
4. **Stage Q3 — Legacy cleanup candidate:** keep the historical `budget` table and APIs readable; deprecate blocking semantics in documentation. Physical column/table removal is unnecessary and should not be part of the initial migration.

Rollback can re-enable the old V1 guard for V1 tasks without deleting any V2 records.

## 27. Security & Trust Model

| Threat | Boundary / mitigation |
|---|---|
| Agent impersonates another role | Role assignment record + caller/session attribution; future authenticated identity desirable. Current identity is trust-based and must be stated as such. |
| Implementer records own PASS | `review.submit` requires reviewer assignment of matching type and rejects Implementer assignment identity; durable review artefact required. |
| Stale SHA PASS reused | Merge gate requires exact SHA equality; old reviews retained but marked stale by computation. |
| Reviewer modifies implementation | Reviewer role is read-only; review artefact records `tracked_files_modified`; violation blocks PASS and requires clean re-review. |
| Fabricated CI/Git ref | MCP labels evidence as recorded/unverified unless future integration validates it; merge process still checks authoritative Git/CI evidence. |
| Fabricated Human authorization | Authorization ref is not self-proving; only recognized governance evidence satisfies Human gates. MCP never invents authorization. |
| Concurrent agent collision | `BEGIN IMMEDIATE`, active-assignment uniqueness, existing branch/worktree collision rules, Implementer-only implementation lease. |
| SQLite tampering | Database is operational metadata, not sole durable authority; Git artefacts and external CI/review evidence permit reconciliation. Future DB integrity controls may be added. |
| Malicious repository/source instructions | Role/skill contracts treat repository/source text as data unless it is an authorized governance artefact; `ai-ip-domain` enforces instruction/data separation. |
| Prompt injection from research paper | Research content cannot redefine agent authority or governance; Security review covers ingestion/prompt-boundary risks for applicable tasks. |
| Secret exposure to reviewers | Least-privilege contexts; no secrets in repository/review artefacts; reviewers inspect only evidence needed for their role. |
| Over-privileged agents | Planner/reviewers read-only for implementation; Implementer scoped to authorized branch/worktree; Human exceptions remain explicit. |

Current MCP cannot cryptographically authenticate Human or agent identity and cannot independently prove Git/CI facts. V2 must not claim otherwise until a separately authorized implementation adds those capabilities.

## 28. Backward Compatibility

- Existing five SQLite tables and all rows remain intact.
- Existing 12 task states remain readable and valid for V1 history.
- Existing `tasks.owner/branch/worktree/lease_*` fields remain supported for V1 clients.
- Existing checkpoints/progress/budget records remain readable.
- Historical P0/P1/P2 evidence is not rewritten.
- Historical Review Log remains preserved; old Antigravity reviews are not split/rebranded.
- Tasks without a `task_workflow` V2 row execute/read as V1.
- Existing MCP clients continue using the current tool contracts during transition; V2 extensions must be additive or version-negotiated where response-shape compatibility cannot be guaranteed.
- No V1 task is automatically enrolled in V2 because it exists in backlog or has a recent commit.

## 29. Database Migration Strategy

Future Phase B migration must be forward-only and non-destructive:

1. Open the existing DB using current safety pragmas.
2. Create V2 tables/indexes with `CREATE TABLE/INDEX IF NOT EXISTS` inside one controlled migration transaction.
3. Record schema migration version separately; do not infer Workflow V2 activation merely from table existence.
4. Do **not** backfill fake assignments/specs/reviews for historical tasks.
5. Only tasks explicitly enrolled after activation receive `task_workflow` rows.
6. Keep existing `tasks.owner` behavior for V1; V2 implementation ownership is projected from the active Implementer assignment while compatibility fields may be mirrored only if implementation proves this is safe and atomic.
7. Migration tests must open a real-format legacy fixture, migrate it, restart, and verify every old record remains readable.
8. On migration failure, roll back the transaction and continue on the prior schema; never reset the DB.

Schema availability and workflow activation are separate concerns. A database can contain V2 tables while `WORKFLOW_V2_ENABLED=false` and all tasks continue under V1.

## 30. Repository Change Plan

### 30.1 This task

```text
CREATE  docs/tasks/GOV-AGENT-001_FOUR_AGENT_GOVERNANCE_ORCHESTRATION_SPEC.md
```

No other file is required for this specification phase.

### 30.2 Proposed future changes

```text
MODIFY DURING IMPLEMENTATION  tools/project-orchestrator-mcp/src/store.ts
MODIFY DURING IMPLEMENTATION  tools/project-orchestrator-mcp/src/server.ts
MODIFY DURING IMPLEMENTATION  tools/project-orchestrator-mcp/src/admin.ts
MODIFY DURING IMPLEMENTATION  tools/project-orchestrator-mcp/test/*.test.ts
MODIFY DURING IMPLEMENTATION  tools/project-orchestrator-mcp/README.md
CREATE                       agents/...
CREATE                       docs/reviews/<TASK-ID>/...
MODIFY DURING ACTIVATION      AGENTS.md
MODIFY DURING ACTIVATION      docs/operations/AUTONOMOUS_AGENT_PROTOCOL.md
HISTORICAL — DO NOT MODIFY    docs/operations/02_GEMINI_REVIEW_LOG.md historical entries
HISTORICAL — DO NOT MODIFY    completed P0/P1/P2 task/review evidence except separately authorized factual reconciliation
OPTIONAL / FUTURE             Git/CI identity-verification integration
OPTIONAL / FUTURE             cryptographic/authenticated agent identity
```

No ADR is created in this phase because this document is sufficient to present the architecture for independent specification review. A future accepted architecture may create an ADR if the reviewer/Human requires one before implementation.

Downstream PR split recommendation:

- **PR A — GOV-AGENT-001-SPEC:** this specification only.
- **PR B — GOV-AGENT-001-MCP:** additive MCP V2 schema/state/tools/compatibility.
- **PR C — GOV-AGENT-001-AGENTS:** role package, skills, manifests, review templates; **no activation**.
- **PR D — GOV-AGENT-001-ACTIVATION:** governance cutover, activation marker/config, `AGENTS.md` and Autonomous Agent Protocol changes.

Separating PR C and PR D keeps package installation reviewable without implicitly activating a new governance model.

## 31. Implementation Phases

### Phase A — Specification (current)

Exit: this document committed; only authorized spec artefact changed; independent specification review pending. No activation.

### Phase B — MCP V2 additive implementation

Exit: non-destructive DB migration/tests pass; V1 clients/tasks remain readable; V2 assignment/spec/review/CI/merge-gate contracts implemented; quota compatibility behavior tested; independent implementation review PASS on exact SHA; still disabled for production workflow unless activation is separately authorized.

### Phase C — Agent package + skills/templates

Exit: four role contracts, minimal P0 skills, manifest, review templates, validation tests, and versioning rules implemented/reviewed; package exists but does not alter active project governance.

### Phase D — Governance activation

Exit: Human explicitly approves activation; `AGENTS.md`/Autonomous Agent Protocol updated; an immutable `WORKFLOW_V2_ACTIVATION_COMMIT` and activation config are recorded; legacy cutover semantics documented; CI/review PASS.

### Phase E — Bounded non-production pilot

Exit: one explicitly authorized low/medium-risk task completes end-to-end under V2; role separation, exact-SHA review, rollback, auditability, and merge-gate behavior are demonstrated; findings resolved before wider adoption.

### Phase F — AI-CONV adoption

Exit: Human separately authorizes AI-CONV task(s); R3 routing mandates both reviews; AI-IP domain skill is validated against current contracts; no provider/real-data/production boundary is crossed without its own authorization.

Phases B–F are future work and are not authorized by this specification task.

## 32. Test Strategy

Future MCP tests must cover at minimum:

- legacy DB opens successfully;
- migration is non-destructive;
- all four roles can be represented;
- duplicate/incompatible active assignments are rejected;
- frozen spec is immutable and supersession is versioned;
- reviewer cannot overwrite implementation ownership;
- Security and Quality verdicts remain independent;
- PASS is tied to exact implementation SHA;
- new SHA makes old PASS stale;
- CI SHA mismatch blocks merge readiness;
- one required review FAIL/REQUEST_CHANGES blocks merge;
- both required PASS + matching CI allow readiness when all other gates pass;
- missing Human authorization/required exception blocks readiness;
- V1 tasks remain readable and retain legacy behavior;
- V2 informational quota mode does not accidentally block work;
- concurrency prevents incompatible claims/assignments;
- restart preserves V2 state;
- rollback/disable mode preserves all records.

Future governance/agent tests should validate forbidden actions, role/skill routing, R0–R4 routing, fixed-SHA review contracts, reviewer read-only behavior, and review-template completeness. R3 fixtures must remain synthetic/offline unless a separate authorization permits real data.

## 33. Rollback Strategy

Preferred control: an explicit repository/governance configuration equivalent to `WORKFLOW_V2_ENABLED=false`, with activation commit recorded separately from schema installation.

Rollback behavior:

- stop assigning new tasks to V2;
- keep all V2 tables/rows/review artefacts/specs readable;
- allow already merged historical V2 evidence to remain immutable history;
- route newly authorized tasks back to the approved V1 workflow if Human governance permits;
- retain legacy MCP tables and clients;
- do not restore a database backup destructively and do not delete V2 rows.

If a pilot task is in progress during rollback, Human/Planner decides whether to finish it under V2 or checkpoint and restart under V1; the system must not silently translate review evidence between workflows.

## 34. Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Governance framework becomes larger than product work | Process overhead | Minimal P0 skills, compact task state, risk-based routing, phased rollout |
| Duplicate source of truth between Git and MCP | Conflicting status | Git artefacts durable/canonical; MCP operational index only |
| Role labels imply stronger identity than exists | False assurance | Explicit trust-based identity limitation until authenticated identity exists |
| Reviewer collusion/confirmation bias | Weak assurance | Independent submissions, same fixed SHA, no dependency on peer verdict |
| V2 migration breaks legacy tasks | Lost coordination/history | Additive tables, no backfill, legacy tests, activation separate from migration |
| Stale CI/review evidence satisfies gate | Unsafe merge | Exact-SHA equality and stale computation |
| Risk routing under-classifies AI/security work | Missing review | R3/R4 mandatory dual review; risk can be raised conservatively |
| Quota guard blocks V2 unexpectedly | Workflow interruption | staged deprecation and explicit resource policy |
| Agent skills conflict with governance | Authority inversion | Governance precedence; blocked/handoff on conflict |
| Review artefacts expose secrets/confidential IP | Data leak | least-privilege evidence, no secrets/full research content, security checklist |

## 35. Open Questions

The following must be resolved before or during the specifically authorized future phase; none blocks independent review of this architecture unless the reviewer identifies it as critical:

1. Whether agent identity remains trust-based for initial V2 pilot or requires authenticated client identity before activation.
2. Whether GitHub/CI fact verification is added inside MCP or remains an external merge-time check in the initial implementation.
3. Exact repository config location/name for `WORKFLOW_V2_ENABLED` and the activation commit marker.
4. Whether V2 compatibility should mirror active Implementer ownership into legacy `tasks.owner/branch/worktree` or expose it only through the new assignment view.
5. Exact Human/admin mechanism that freezes specs and records explicit exception gates.
6. Whether R2 security review becomes mandatory for all file-upload/parser changes rather than threat-surface conditional.
7. Whether review artefacts are always committed before merge or can be referenced from an immutable external review system with a later governance reconciliation commit.

## 36. Acceptance Criteria

Status values below mean **addressed by this specification draft; independent specification review is still required**. They are not self-issued review PASS evidence.

| AC | Requirement | Draft status / evidence |
|---|---|---|
| AC-01 | Current Workflow V1 accurately documented from repository evidence | Addressed — §§3–4 |
| AC-02 | Four roles and authority boundaries explicit | Addressed — §§9–13 |
| AC-03 | Planner/reviewers cannot modify application implementation in role | Addressed — §§10,12,13 |
| AC-04 | Only Implementer owns implementation modification responsibility | Addressed — §§9,11,17 |
| AC-05 | Security and Quality reviews independent | Addressed — §14 |
| AC-06 | Fixed-SHA semantics unambiguous | Addressed — §19 |
| AC-07 | Changed implementation SHA invalidates applicable old review PASS | Addressed — §§14,17,19 |
| AC-08 | Proposed MCP V2 data model defined | Addressed — §17 |
| AC-09 | Backward-compatible SQLite migration strategy defined | Addressed — §§28–29 |
| AC-10 | No destructive reset required | Addressed — §§17,29,33 |
| AC-11 | Proposed MCP tool contracts specified | Addressed — §18 |
| AC-12 | Merge gate explicit/deterministic | Addressed — §20 |
| AC-13 | Risk classes R0–R4 or alternatives defined | Addressed — §15 |
| AC-14 | Agent role package architecture specified | Addressed — §21 |
| AC-15 | Skill contract format specified | Addressed — §22 |
| AC-16 | Minimum shared/role-specific skills identified | Addressed — §§22–23 |
| AC-17 | Historical review evidence preserved | Addressed — §§24,28 |
| AC-18 | Old tasks not retroactively rewritten | Addressed — §§3,28–29 |
| AC-19 | Quota/budget deprecation strategy specified | Addressed — §26 |
| AC-20 | Client/model independence preserved | Addressed — §25 |
| AC-21 | GPT-5.6 Sol High may be recorded without binding role identity | Addressed — §§1,25 |
| AC-22 | Security/trust threats analyzed | Addressed — §27 |
| AC-23 | Implementation migration incremental | Addressed — §31 |
| AC-24 | Rollback defined | Addressed — §33 |
| AC-25 | Future implementation test plan detailed | Addressed — §32 |
| AC-26 | Current application behavior untouched | Addressed by task scope; verify changed-file gate before commit |
| AC-27 | Current AI/patent contracts untouched | Addressed by §§3,7,23; verify changed-file gate before commit |
| AC-28 | No provider/API calls performed | Addressed by task scope; verify handoff statement |
| AC-29 | No real/confidential research data used | Addressed by task scope; verify handoff statement |
| AC-30 | No four-agent workflow activated by this task | Addressed — §§7,30,31,38 |

## 37. Implementation Handoff

```text
Task ID: GOV-AGENT-001
Agent: Planner / Architecture & Governance Specification Agent
Reviewer: Independent specification reviewer — pending
Status: READY FOR INDEPENDENT SPECIFICATION REVIEW
Version: 0.1.0
Work completed: Current V1/MCP analysis; target four-role contracts; independence/risk/state/data/tool/merge-gate design; skill/review/trust/backward-compatibility/migration/test/rollback plan.
Files affected: This specification artefact only, subject to pre-commit verification.
Evidence checked: Governance docs, workflow/protocol docs, control center/review log, P2 task/ADR boundaries, MCP source/tests/package behavior, Git/GitHub baseline.
Findings: V1 has strong fixed-SHA/standing-delegation foundations but lacks role/spec/dual-review/CI/merge-gate first-class structures.
Decisions: Proposed additive V2 sub-state model; two independent fixed-SHA review streams; computed merge gate; Git durable evidence + MCP operational index; staged quota deprecation; explicit cutover and reversible activation.
Issues: Open questions in §35; independent specification review pending.
Security impact: Specification only; no runtime/security boundary changed.
Recommended next action: Independent fixed-SHA review of this specification commit. Do not implement Phase B–F before separate authorization/review gates.
```

Downstream implementers must treat this document as architecture proposal until the required independent specification review and Human governance disposition are recorded. A PASS on this specification would authorize nothing beyond what the Human separately authorizes.

## 38. Explicit Non-Implementation Statement

This task changed no Project Orchestrator MCP TypeScript, SQLite schema/database, backend/frontend/application/AI runtime, prompt, JSON schema, DOCX renderer/template, CI behavior, provider/model runtime, production/deployment configuration, current governance activation file, or historical review record. It used no real/confidential research data and made no provider/API call. It does not change P2-001/P2-002/P2-003/P2-004 technical semantics or start downstream AI-CONV work.

**GOV-AGENT-001 SPECIFICATION COMPLETE — FOUR-AGENT WORKFLOW NOT IMPLEMENTED OR ACTIVATED.**
