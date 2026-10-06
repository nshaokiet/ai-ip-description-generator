# GOV-AGENT-001 — Four-Agent Governance & Orchestration Migration

## 1. Metadata

| Field | Value |
|---|---|
| Task ID | `GOV-AGENT-001` |
| Version | `0.2.0` |
| Status | **READY FOR INDEPENDENT SPECIFICATION RE-REVIEW** |
| Phase | **SPECIFICATION REMEDIATION — FULL WORKFLOW V2** |
| Owner | Human / Product Owner |
| Authoring role | Planner / Architecture & Governance Specification Agent |
| Authorization reference | Human task instruction for `GOV-AGENT-001`, 2026-10-06; no separate canonical authorization ID was supplied |
| Repository baseline SHA | `009e1320405a8d956510c4a11a73f6626acec281` |
| Prior reviewed specification SHA | `6ed80f65a96c128a95d167c2d32ef91166618b6b` |
| Prior independent review disposition | **REQUEST CHANGES** — F-01…F-06 remediated by this version; no PASS is claimed |
| Breaking change | **No for this specification-only task.** Future Workflow V2 governance activation is a breaking governance change and requires separate authorization/review. |
| Confidentiality | Internal; research inputs remain Confidential by default under current governance |
| Intended activation boundary | Future `WORKFLOW_V2_ACTIVATION_COMMIT`; **not defined or activated by this task** |
| Preferred execution profile | GPT-5.6 Sol High may be used as an execution policy; role identity remains client/model independent |

Evidence baseline: `AGENTS.md`, `PROJECT_CONTEXT.md`, `docs/system-specification.md`, `docs/workflow.md`, `docs/operations/01_PROJECT_CONTROL_CENTER.md`, `docs/operations/02_GEMINI_REVIEW_LOG.md`, `docs/operations/AUTONOMOUS_AGENT_PROTOCOL.md`, P2 task/ADR records, and `tools/project-orchestrator-mcp/` source/tests at the repository baseline above. GitHub `main` was independently observed at the same SHA before authoring.

### 1.1 Revision history

| Version | Date | Disposition | Material change |
|---|---|---|---|
| `0.1.0` | 2026-10-06 | Independent review: **REQUEST CHANGES** | Initial four-agent Workflow V2 architecture. |
| `0.2.0` | 2026-10-06 | **READY FOR INDEPENDENT SPECIFICATION RE-REVIEW** | Retains Full Workflow V2 by explicit Product Owner decision; separates recorded/provisional evidence from authoritative merge eligibility; resolves spec-freeze authority; removes quota redesign from scope; phases risk-routing activation; narrows P0 skills; expands non-destructive schema/migration/PR/rollback contracts. |

### 1.2 Product Owner architecture decision

**FULL WORKFLOW V2 IS AN INTENTIONAL PRODUCT OWNER DECISION.** The project is expected to continue through many AI-CONV and other backend/frontend/security/deployment tasks. The four roles are intended as standing development roles, and reusable structured task/spec/review/CI evidence plus fixed-SHA merge gating are desired as project infrastructure. This remediation therefore preserves the Full Workflow V2 target architecture and makes its implementation incremental; it does not reduce the target to a temporary V1.5 workflow.

### 1.3 Independent review remediation map

| Finding | Severity | v0.2.0 disposition |
|---|---|---|
| F-01 | HIGH | **RESOLVED IN SPEC:** verification levels plus `provisional_ready` and fail-closed `authoritative_merge_eligible`; trust-only MCP metadata cannot authorize merge. |
| F-02 | HIGH | **PRODUCT OWNER OVERRIDE / REMEDIATED:** Full V2 intentionally retained; target architecture separated from bounded implementation phases/PRs. |
| F-03 | MEDIUM | **RESOLVED IN SPEC:** concrete five-condition Human-authorized spec-freeze rule and supersession/reconciliation semantics. |
| F-04 | MEDIUM | **REMOVED FROM SCOPE:** quota/budget redesign deferred to `GOV-RESOURCE-001`; current behavior unchanged. |
| F-05 | MEDIUM | **RESOLVED IN SPEC:** R0–R4 retained with DESIGNED/IMPLEMENTED/ACTIVATED rollout states and mandatory dual-review pilot option. |
| F-06 | LOW | **RESOLVED IN SPEC:** skill architecture retained with an exact minimal P0 set; all additional narrow skills are P1/FUTURE. |

These are authoring dispositions, not an independent re-review PASS.

## 2. Executive Summary

The current project workflow is a Human-governed, Codex-centered implementation lifecycle with one aggregate independent read-only reviewer role and Project Orchestrator MCP as a coordination/state layer. It already has strong fixed-SHA review, evidence-backed merge eligibility, task leases, checkpoints, and durable Git governance records. It does not have first-class Planner, Implementer, Security Reviewer, and Quality Reviewer assignments, frozen specification records, two independent review streams, CI evidence records, or a computed merge gate with explicit evidence-verification levels.

Workflow V2 is therefore an **additive, prospective governance migration**. Full V2 is intentionally retained by Product Owner decision. The target architecture keeps the compact task-level lifecycle, adds separate spec/assignment/implementation/review/CI records, distinguishes recorded evidence from provisional readiness and authoritative merge eligibility, preserves Git as durable technical evidence, and keeps Human authority above the orchestration layer. Implementation is split into bounded phases/PRs so the larger target does not imply one giant implementation change.

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
5. Current MCP records Human refs, SHAs, CI references, reviewer identity, and PR/merge facts as trust-based inputs; without an authoritative verifier it cannot safely convert those records into an authoritative `ready=true` decision.

The migration must close these gaps without duplicating Git as a competing source of truth or retroactively rewriting historical evidence.

## 6. Goals

- Define four stable roles with explicit authority boundaries.
- Preserve **Full Workflow V2** as the intentional long-lived target architecture while implementing it incrementally.
- Preserve Human governance and stop conditions.
- Preserve fixed-SHA review semantics and improve review independence.
- Add a frozen-spec contract before implementation.
- Define additive MCP V2 records for assignments, specs, implementation evidence, reviews, and CI.
- Define evidence verification levels and compute both provisional readiness and authoritative merge eligibility deterministically.
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
- redesign, deprecation, reinterpretation, or changed blocking semantics for the current quota/budget subsystem. Resource/quota modernization is deferred to future task `GOV-RESOURCE-001 — Resource / Quota Policy Modernization`.

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

`EVALUATION_REVIEWER` is reserved as a **future optional role** for separately authorized evaluation work. It is not part of the initial four-role activation contract and must not be synthesized into current assignments.

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

The R0–R4 scale is retained as part of the **Full Workflow V2 target architecture**. Risk routing has three distinct rollout states:

- **DESIGNED:** classes/rules exist in this specification only.
- **IMPLEMENTED:** MCP/agent code can represent and evaluate the rules, but the rules do not control active project workflow merely because code exists.
- **ACTIVATED:** Human-approved governance explicitly enables risk routing for enrolled V2 tasks.

The bounded pilot may require both Security and Quality review for every explicitly authorized pilot task regardless of R0–R4 classification. This validates review separation before automated risk routing controls production workflow. R0–R4 activation may occur only after pilot evidence and explicit Human activation.

| Risk | Typical scope | Planner | Implementer | CI | Quality | Security | Human gate |
|---|---|---|---|---|---|---|---|
| R0 | Docs/metadata/evidence-only | Planner-lite | Required for edits | CI-lite / applicable validation | Quality-lite independent check | Optional | Existing governance only |
| R1 | Low-risk isolated code/tooling | Required | Required | Required | Required | Optional unless threat surface changes | Existing governance only |
| R2 | Application functionality | Required | Required | Required | Required | Conditional: mandatory when auth/input/network/storage/security surface changes | Existing stop conditions |
| R3 | AI/conversion/patent pipeline | Required | Required | Required | **Mandatory** | **Mandatory** | Existing Human scope/provider/data/legal gates |
| R4 | Security, production, confidential data, auth, deployment boundary | Required | Required | Required | **Mandatory** | **Mandatory** | **Explicit Human exception/approval where current governance requires it** |

`Planner-lite`, `Quality-lite`, and `CI-lite` reduce depth, not independence or evidence integrity. Risk can only be raised automatically; lowering an initially assigned risk class requires Planner justification and any Human decision required by governance.

Risk-routing status for this specification: **DESIGNED, NOT IMPLEMENTED, NOT ACTIVATED**.

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
              -> REVIEW_PASS  [only when authoritative merge eligibility is satisfied]
              -> AWAITING_HUMAN_APPROVAL only when a Human gate is actually required
              -> MERGED
              -> COMPLETED

Any unrecoverable/current stop condition -> BLOCKED

SPEC SUB-STATE
DRAFT -> READY -> FROZEN -> SUPERSEDED (only by explicit newer version)

REVIEW SUB-STATE, per required review type and implementation SHA
NOT_STARTED -> IN_PROGRESS -> PASS | REQUEST_CHANGES | BLOCKED
```

Planning/spec readiness are represented in `task_specs` and assignments rather than proliferating top-level task states. `PROVISIONAL_READY` and `AUTHORITATIVE_MERGE_ELIGIBLE` are computed results, not manually writable task states.

### 16.1 Frozen-spec authority

A task specification is `FROZEN` only when **all** of the following are true:

1. the committed Git specification artefact exists;
2. its exact specification commit SHA is known;
3. its specification version is recorded;
4. explicit Human authorization references the task/specification or an unambiguous authorization record covering that exact version/SHA;
5. the orchestration layer records the frozen spec identity and the authorization evidence.

The Planner may author and submit a spec but **cannot self-authorize freeze**. MCP can record Human authorization evidence but **cannot create Human authorization**. If implementation has begun and the specification changes, the old spec becomes `SUPERSEDED`, the new version must satisfy the freeze rule, and implementation/review evidence must be reconciled against the new frozen spec. Existing evidence is retained as history and cannot silently migrate to the new spec.

## 17. MCP V2 Data Model

V2 is additive to the five current tables. Existing rows remain untouched and readable. The target model covers the legacy `tasks`, `dependencies`, `budget`, `progress`, and `checkpoints` tables plus new V2 records. No table installation implies workflow activation.

Common requirements for all V2 tables: foreign keys enabled; UTC epoch/integer timestamps consistent with the current store; migrations use `CREATE ... IF NOT EXISTS`; immutable evidence rows are append-oriented; updates that supersede/finalize records occur transactionally; historical rows are never deleted merely because they become stale.

### 17.0 Legacy tables retained

| Table | V2 treatment |
|---|---|
| `tasks` | Primary task identity/lifecycle remains readable. Existing IDs/states/history are preserved. V2 enrollment is externalized to `task_workflow`; no retroactive rewrite is required. |
| `dependencies` | Preserved unchanged unless a separately authorized compatibility change is required. |
| `budget` | Preserved with **current behavior unchanged** in GOV-AGENT-001. Resource-policy modernization is deferred to `GOV-RESOURCE-001`. |
| `progress` | Preserved; V2 may add role/assignment references only through additive compatible mechanisms if later authorized. |
| `checkpoints` | Preserved; historical checkpoints remain readable. V2 role-aware metadata must be additive/backward compatible. |

### 17.1 `task_workflow`

Purpose: opt a task into V2 prospectively.

- `task_id TEXT PRIMARY KEY REFERENCES tasks(id)`
- `workflow_version TEXT NOT NULL` (initial V2 value `2`)
- `risk_class TEXT NOT NULL CHECK IN ('R0','R1','R2','R3','R4')`
- `authorization_ref TEXT NOT NULL`
- `activation_commit TEXT NOT NULL`
- `created_at INTEGER NOT NULL`

- **Primary key:** `task_id`.
- **Foreign key:** `task_id -> tasks(id)`.
- **Uniqueness:** one V2 enrollment row per task.
- **Indexes:** index `(workflow_version, risk_class)` for routing/inspection if query plans justify it.
- **Immutable after enrollment:** `task_id`, initial `workflow_version`, initial `activation_commit`, original `authorization_ref`; later risk reclassification should be separately audited rather than overwriting history silently.
- **Mutable:** narrowly scoped current routing fields only if future implementation models audited reclassification.
- **Timestamps:** `created_at`; optional additive `updated_at` only if mutable routing fields are implemented.
- **Stale semantics:** enrollment itself does not become stale; activation may become disabled globally without deleting the row.
- **Backward compatibility:** no row means V1 behavior. Historical tasks receive no fake V2 row.

### 17.2 `task_assignments`

Purpose: represent standing-role assignment history without overloading the legacy single-owner task lease.

- `id INTEGER PRIMARY KEY AUTOINCREMENT`
- `task_id TEXT NOT NULL REFERENCES tasks(id)`
- `role TEXT NOT NULL CHECK IN ('PLANNER','IMPLEMENTER','SECURITY_REVIEWER','QUALITY_REVIEWER')`
- `agent_id TEXT NOT NULL`
- `status TEXT NOT NULL` (`ASSIGNED`,`ACTIVE`,`COMPLETED`,`BLOCKED`,`SUPERSEDED`)
- `assignment_version INTEGER NOT NULL`
- `assigned_at INTEGER NOT NULL`, `started_at`, `completed_at`
- `branch TEXT`, `worktree TEXT`, `lease_start`, `lease_expiry` only where the role needs a lease
- `UNIQUE(task_id, role, assignment_version)`
- partial unique index preventing more than one `ASSIGNED`/`ACTIVE` assignment for the same `(task_id, role)`

Implementer is the only role allowed to own the implementation branch/worktree lease. Planner/reviewer records may identify an authorized review/spec checkout but must not seize implementation ownership.

- **Primary key:** `id`; **FK:** `task_id -> tasks(id)`.
- **Uniqueness:** `(task_id, role, assignment_version)` plus one active assignment per `(task_id, role)`.
- **Indexes:** `(task_id, role, status)`, lease-expiry index for active Implementer assignment.
- **Immutable:** assignment identity, role, agent identity as originally recorded, assignment version, assigned timestamp.
- **Mutable:** status, lease timestamps, completion/block metadata under validated transitions.
- **Timestamps:** `assigned_at`, optional `started_at`, `completed_at`, and explicit transition time if implementation needs it.
- **Stale semantics:** replaced role assignments become `SUPERSEDED`; historical assignment evidence remains queryable.
- **Backward compatibility:** legacy `tasks.owner/branch/worktree` remain valid for V1. Any V2 projection/mirroring must be proven atomic and must not rewrite V1 history.

### 17.3 `task_specs`

Purpose: register versioned task specifications and make Human-authorized freeze/supersession auditable.

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

- **Primary key:** `id`; **FK:** `task_id -> tasks(id)`.
- **Uniqueness:** `(task_id, spec_version)`, `(task_id, spec_sha)`, at most one current `FROZEN` spec.
- **Indexes:** `(task_id,status)` and `(spec_sha)`.
- **Immutable once FROZEN:** task/spec identity, SHA, version, artefact path, freeze authorization reference, `frozen_at`.
- **Mutable before freeze:** draft/ready metadata; after freeze only the controlled `FROZEN -> SUPERSEDED` transition plus `superseded_at`.
- **Timestamps:** `created_at`, `frozen_at`, `superseded_at`.
- **Stale semantics:** `SUPERSEDED` specs remain durable history; all implementation/review/CI evidence tied to the superseded spec is non-satisfying for a newer frozen spec unless explicitly reconciled by a future authorized rule.
- **Backward compatibility:** V1 tasks do not require synthetic spec rows.

### 17.4 `implementation_evidence`

Purpose: preserve candidate/final implementation SHA history tied to a frozen specification and recorder assignment.

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

- **Primary key:** `id`; **FKs:** task and recorder assignment.
- **Uniqueness/indexes:** unique `(task_id, implementation_sha)`; indexes on `(task_id, created_at)` and `(spec_sha, implementation_sha)`.
- **Immutable:** all evidence identity fields after insert. Corrections append a new record; they do not mutate a reviewed SHA into another SHA.
- **Timestamps:** `created_at`.
- **Stale semantics:** any record whose implementation SHA or spec SHA differs from the currently selected final implementation/frozen spec remains historical and cannot satisfy current gates.
- **Backward compatibility:** no fake implementation records are created for V1 history.

### 17.5 `reviews`

Purpose: store immutable Security/Quality fixed-SHA verdict evidence as separate streams.

- `review_id INTEGER PRIMARY KEY AUTOINCREMENT`
- `task_id TEXT NOT NULL REFERENCES tasks(id)`
- `review_type TEXT NOT NULL CHECK IN ('SECURITY','QUALITY')`
- `reviewer_assignment_id INTEGER NOT NULL REFERENCES task_assignments(id)`
- `spec_sha TEXT NOT NULL`, `base_sha TEXT NOT NULL`, `implementation_sha TEXT NOT NULL`
- `attempt INTEGER NOT NULL`
- `verdict TEXT NOT NULL CHECK IN ('PASS','REQUEST_CHANGES','BLOCKED')`
- `findings_ref TEXT NOT NULL`, `blocking_findings INTEGER NOT NULL DEFAULT 0`, `evidence_ref TEXT NOT NULL`, `artifact_path TEXT NOT NULL`
- `reviewer TEXT NOT NULL`, `model_profile TEXT`, `created_at INTEGER NOT NULL`
- `tracked_files_modified INTEGER NOT NULL CHECK IN (0,1)`
- `UNIQUE(task_id, review_type, implementation_sha, attempt)`

Review types are `SECURITY`, `QUALITY`; future `EVALUATION` may be added by separately authorized compatible migration. Verdicts are `PASS`, `REQUEST_CHANGES`, `BLOCKED`. Old PASS rows are retained. They become **stale by computation** when `implementation_sha != current final implementation SHA`, `spec_sha != current frozen spec SHA`, or the reviewer assignment is no longer valid for the attempt; they are not deleted or rewritten.

- **Primary key:** `review_id`; **FKs:** task and reviewer assignment.
- **Indexes:** `(task_id,review_type,implementation_sha,verdict)`, `(spec_sha,implementation_sha)`.
- **Immutable:** submitted review content, reviewer/model attribution, target SHAs, verdict, evidence refs, timestamps. Correction/re-review creates a new attempt.
- **Timestamps:** `created_at`; optional start timestamp may live in a separate in-progress record/tool state but cannot overwrite submitted evidence.
- **Backward compatibility:** historical Antigravity review records remain in their existing artefacts and are never reclassified/backfilled as SECURITY/QUALITY rows.

### 17.6 `ci_evidence`

Purpose: record CI observations and their verification level without converting trust-based references into authoritative facts.

- `id INTEGER PRIMARY KEY AUTOINCREMENT`
- `task_id TEXT NOT NULL REFERENCES tasks(id)`
- `implementation_sha TEXT NOT NULL`
- `status TEXT NOT NULL CHECK IN ('PENDING','SUCCESS','FAILURE','CANCELLED','UNKNOWN')`
- `reference TEXT NOT NULL`
- `source TEXT NOT NULL`
- `verification_status TEXT NOT NULL CHECK IN ('UNVERIFIED','RECORDED','VERIFIED')`
- `verified_by TEXT`, `verified_at INTEGER`, `verification_ref TEXT`
- `created_at INTEGER NOT NULL`
- `UNIQUE(task_id, reference)`

MCP stores supplied evidence. A recorder cannot promote its own trust-based reference to authoritative truth unless it is also an approved authoritative verifier for that evidence source.

- **Primary key:** `id`; **FK:** task.
- **Indexes:** `(task_id,implementation_sha,status)`, `(verification_status)`.
- **Immutable:** CI source/reference/SHA/result as originally recorded; verification metadata may only transition forward under a defined verifier policy and is audit-preserving.
- **Timestamps:** `created_at`, `verified_at` when applicable.
- **Stale semantics:** a CI row is stale for merge gating when its implementation SHA differs from current final SHA, even if VERIFIED.
- **Backward compatibility:** V1 CI references remain external/historical and are not fabricated into V2 rows.

### 17.7 Evidence verification envelope

Evidence-bearing V2 records must expose verification metadata either directly or through a normalized evidence envelope with at least: `source`, `recorded_by`, `verification_status`, `verified_by`, `verified_at`, and `verification_ref` where applicable. Verification levels mean:

- `UNVERIFIED`: supplied claim/reference with no accepted provenance check.
- `RECORDED`: accepted into operational state with source/recorder attribution, but not authoritatively proven.
- `VERIFIED`: checked by a source-specific authoritative verifier defined by governance/integration and linked to verifiable evidence.

`RECORDED` is useful for orchestration and provisional readiness but cannot by itself satisfy a gate that requires authoritative verification.

### 17.8 Transaction/concurrency requirements

Assignment activation, spec freeze/supersession, implementation finalization, and review submission use `BEGIN IMMEDIATE` transactions and retain the existing `busy_timeout`/WAL approach. Multi-row transitions must commit atomically. Merge-gate reads execute from one consistent transaction/snapshot. Concurrent incompatible role assignment or duplicate freeze attempts fail deterministically.

## 18. MCP V2 Tool Contracts

These are **proposed contracts only**.

| Tool | Purpose / caller | Inputs | Outputs | State / idempotency / validation / failure |
|---|---|---|---|---|
| `project.get_state` | Read combined task/sub-state; any authorized role/Human client | `task_id?` | Task + workflow/risk + assignments + frozen spec + final SHA + review/CI summaries + merge gate | Read-only, idempotent. V1 task returns legacy shape plus `workflow_version=1`; unknown task remains explicit error. |
| `project.assign_role` | Assign one V2 role; Human/admin/orchestrator authority | `task_id, role, agent_id, authorization_ref, lease metadata?` | Assignment record | No task lifecycle transition. Reject V1 task without explicit V2 enrollment, incompatible active assignment, invalid role, missing authorization. Retry with same unique assignment request returns existing record. |
| `project.get_assignments` | Inspect role ownership; authorized roles/Human | `task_id` | Assignment history/current assignments | Read-only, idempotent. |
| `project.submit_spec` | Register versioned draft/ready spec; Planner | `task_id, spec_version, spec_sha, artifact_path, authorization_ref` | Spec record | No implementation start. Idempotent on same `(task,version,sha)`; reject version collision with different SHA, missing Planner assignment, malformed SHA/reference. |
| `project.freeze_spec` | Record a freeze after Human authorization is evidenced; Human/admin path or explicitly delegated governance actor only | `task_id, spec_version, spec_sha, approval_ref, approval_verification` | Frozen spec record + verification status | `READY -> FROZEN` only when §16.1 is satisfied. Planner cannot invoke this as self-authorization. MCP records but cannot manufacture Human approval. Atomic; same freeze is idempotent. Reject SHA/version mismatch, unverified/missing required authorization, already different frozen spec, or invalid authority. |
| `project.get_spec` | Read current/history; all authorized roles | `task_id, version?` | Spec record(s) | Read-only. |
| `project.start_implementation` | Start implementation against frozen spec; Implementer | `task_id, implementer_assignment_id, spec_sha, branch, worktree, lease_minutes?` | Active implementation assignment/lease | Task `APPROVED/CLAIMED -> IN_PROGRESS` as compatible with existing flow. Reject non-frozen spec, wrong role, lease collision, stop condition, invalid branch/worktree. Same active lease request is idempotent. |
| `project.record_implementation` | Record candidate/final immutable SHA; Implementer | `task_id, spec_sha, base_sha, implementation_sha, evidence_ref` | Implementation evidence + stale-gate summary | Task may become `IMPLEMENTED`. New SHA makes prior mismatched CI/review PASS stale by computation. Reject wrong role/spec mismatch/malformed SHA. Same SHA is idempotent. |
| `project.record_ci` | Record external CI evidence; Implementer/automation/admin according to policy | `task_id, implementation_sha, status, reference, source, verification metadata?` | CI record + current match/verification flags | Recording does not fabricate verification. `RECORDED SUCCESS` can contribute to provisional readiness only. Only source-authoritative verification can produce `VERIFIED`. Duplicate reference with identical payload is idempotent; conflicting reuse fails. SHA mismatch remains stored but cannot satisfy either merge gate. |
| `review.start` | Start independent review; assigned Security or Quality Reviewer | `task_id, review_type, assignment_id, spec_sha, base_sha, implementation_sha` | Review attempt token/record | `NOT_STARTED -> IN_PROGRESS`; no task-level PASS. Reject role/type mismatch, implementation SHA mismatch, reviewer=Implementer assignment, missing required artefacts. Same active attempt idempotent. |
| `review.submit` | Submit verdict/evidence; assigned reviewer only | `review_id, verdict, findings_ref, blocking_findings, evidence_ref, artifact_path, model_profile?, tracked_files_modified` | Immutable review result + gate summary | `IN_PROGRESS -> PASS/REQUEST_CHANGES/BLOCKED`. Reject reviewer/type mismatch, changed implementation SHA, missing artefact/evidence, `tracked_files_modified=1` for reviewer role. Submitted review immutable; correction requires new attempt. Review authenticity remains `RECORDED` unless a configured verifier establishes `VERIFIED`. |
| `review.get_status` | Read per-type current/stale history; any authorized role | `task_id, implementation_sha?` | Security/Quality statuses and stale flags | Read-only. |
| `project.get_merge_gate` | Compute merge evidence; Implementer/Human/authorized coordinator | `task_id` | `provisional_ready`, `authoritative_merge_eligible`, required/observed gates, verification levels, exact SHAs, stale evidence, blockers, Human gates | Pure computation/read; idempotent. Must never collapse recorded metadata into an authoritative `ready=true`. If authoritative verification is unavailable, `authoritative_merge_eligible=false` with explicit external-verification blockers. |
| `checkpoint.create` | Preserve resumable evidence; assigned active role | Existing checkpoint fields + `role/assignment_id` in V2 | Checkpoint record | Keep legacy behavior; quota must not block checkpoint. Role must match assignment when V2. |
| `checkpoint.get_latest` | Resume state; authorized role | `task_id, role?` | Latest compatible checkpoint | Read-only; legacy checkpoints remain readable. |

Authorization assumptions: MCP trusts authenticated/authorized caller context only to the extent future implementation actually provides it. Until identity/authentication is implemented, `agent_id`, role, Human authorization refs, Git SHAs, CI refs, and review artefacts are **trust-based recorded claims** subject to repository/Git verification by workflow policy.

### 18.1 Evidence verification responsibility

| Evidence type | Typical source | Recorder | Authoritative verifier | Recorded evidence can satisfy provisional readiness? | Required for authoritative merge eligibility? |
|---|---|---|---|---:|---:|
| Human task/spec authorization | Human governance instruction / durable decision artefact | Planner/admin/orchestrator | Human-authority channel or approved governance verifier | Yes, if explicit and internally consistent | **Yes — VERIFIED** |
| Specification SHA/version | Git committed spec artefact | Planner/admin | Git repository verification + freeze authorization reconciliation | Yes | **Yes — VERIFIED** |
| Implementation SHA/base | Git branch/PR commit | Implementer | Git repository/PR verifier | Yes | **Yes — VERIFIED** |
| CI result | CI provider/run reference | automation/Implementer/admin | CI provider integration or equivalent authoritative external check | Yes, if matching SHA and recorded SUCCESS | **Yes — VERIFIED SUCCESS on final SHA** |
| Security review | Durable review artefact + reviewer assignment | Security Reviewer | Review artefact/assignment verifier defined by governance; initial pilot may require external reconciliation | Yes, if required and exact-SHA PASS is recorded | **Yes when required; exact-SHA PASS must be authoritatively accepted** |
| Quality review | Durable review artefact + reviewer assignment | Quality Reviewer | Review artefact/assignment verifier defined by governance; initial pilot may require external reconciliation | Yes, if required and exact-SHA PASS is recorded | **Yes when required; exact-SHA PASS must be authoritatively accepted** |
| Branch/PR pre-merge state | GitHub/Git host | coordinator/automation | GitHub/Git provider | May be shown as recorded | **Yes — VERIFIED immediately before merge** |
| Merge result | GitHub/Git host | coordinator/automation | GitHub/Git provider + final main reconciliation | No pre-merge gate; historical record only | Post-merge **VERIFIED** evidence required for closeout |

The initial V2 implementation is allowed to remain partially trust-based. In that case MCP can compute `provisional_ready`, while authoritative merge eligibility stays false until the required Git/CI/Human/PR/review evidence is verified through an accepted authoritative path. This prevents the orchestration database from overstating trust it does not possess.

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
- For remediation `A -> B`, Security PASS(A), Quality PASS(A), and CI(A) are retained but stale for B. B requires its own applicable CI(B), Security(B), and Quality(B).

## 20. Merge Gate

Workflow V2 has two deliberately different merge concepts. Neither is an agent-declared task state.

### 20.1 Provisional merge readiness

`provisional_ready=true` means the orchestration layer has a complete, internally consistent set of **recorded** evidence for the current frozen spec/final implementation SHA and no recorded blocker. It is useful for deciding that the task is ready for authoritative pre-merge checks. It is **not permission to merge**.

For a typical R3/R4 task:

```text
provisional_ready =
  workflow_v2_active_for_task
  AND human_task_authorization_recorded
  AND frozen_spec_present
  AND final_implementation_sha_present
  AND recorded_ci_success_sha == final_implementation_sha
  AND recorded_security_pass_sha == final_implementation_sha
  AND recorded_quality_pass_sha == final_implementation_sha
  AND no_blocking_findings
  AND no_unresolved_stop_condition
  AND no_scope_violation
  AND no_known_secret_or_confidential_data_exposure
  AND all_required_human_exception_refs_recorded
```

### 20.2 Authoritative merge eligibility

`authoritative_merge_eligible=true` means provisional readiness is true **and** every evidence class that governance requires to be authoritative has been verified by an accepted source-specific verifier immediately enough to support merge.

```text
authoritative_merge_eligible =
  provisional_ready
  AND human_authorization_verification == VERIFIED
  AND frozen_spec_git_identity == VERIFIED
  AND final_implementation_git_identity == VERIFIED
  AND required_ci == VERIFIED_SUCCESS_ON_FINAL_SHA
  AND each_required_review == AUTHORITATIVELY_ACCEPTED_PASS_ON_FINAL_SHA
  AND branch_pr_premerge_state == VERIFIED_VALID
  AND required_human_exception_gates == VERIFIED
  AND no_authoritative_stop_condition
```

For R0–R2, the active routing policy determines which review streams are required. During the bounded pilot, governance may require both Security and Quality for all pilot tasks even before automated routing is activated. MCP must expose every gate as required/satisfied/stale/missing and `UNVERIFIED`/`RECORDED`/`VERIFIED` as applicable.

### 20.3 Fail-closed rule

MCP metadata alone cannot prove Git SHA existence, GitHub PR state, CI success, Human authorization, merge status, or review truth unless the implementation has an approved authoritative verification path for that evidence. Therefore:

- a recorded-only CI PASS never by itself satisfies authoritative merge eligibility;
- a recorded Human authorization reference never becomes `VERIFIED` merely because it is present in SQLite;
- a plain `ready=true` authoritative response is forbidden when required verification capability is absent;
- missing verifier capability is reported as an explicit blocker, not silently treated as PASS;
- actual merge remains subject to the repository's current governance, platform controls, and immediate pre-merge verification.

## 21. Agent Role Package

The following is the **target structure** for Full Workflow V2. Phase C/D activation content is intentionally smaller: only the four role contracts and the P0 skills in §22 are required initially; additional helpers/skills remain P1/FUTURE.

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

**Planner:** `task-specification`, `architecture-analysis`.

**Implementer:** `specification-execution`, `safe-code-change`.

**Security:** `threat-modeling`, `ai-security`.

**Quality:** `fixed-sha-review`, `spec-compliance`, `patent-conversion-review`.

These named skills are the complete P0 activation set. Repository analysis, risk classification, implementation handoff, regression review, web/API/file-upload checklists, dependency review, and other narrow procedures may be embedded as procedures/checklists in the P0 skills initially or introduced later as **P1/FUTURE** skills. Manifest/versioning remains part of the target architecture, but the initial implementation should be minimal: identify role, required P0 skill, and compatible version without building a general-purpose package manager.

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

## 26. Quota/Budget Boundary

Quota/budget redesign is **removed from GOV-AGENT-001 implementation scope** by Product Owner decision.

- The current `budget` table, APIs, threshold semantics, and blocking behavior remain unchanged by this task and by the GOV-AGENT-001 implementation phases unless a later Human decision explicitly amends scope.
- Workflow V2 may read/report legacy budget/resource metadata for observability, but it must not reinterpret, bypass, deprecate, or silently change the current enforcement behavior.
- No quota/resource-policy migration is an acceptance criterion for GOV-AGENT-001.
- Future modernization is tracked conceptually as `GOV-RESOURCE-001 — Resource / Quota Policy Modernization`, which requires its own authorization, specification, review, implementation, and activation decisions.

This boundary preserves existing behavior and removes quota redesign from the critical path for Full Workflow V2.

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

Initial V2 may therefore use procedural/trust-based agent identity with explicit verification limits. Stronger authenticated identity is a future concern tentatively named `GOV-IDENTITY-001 — Authenticated Agent Identity`, requiring separate authorization/specification; it is not a hidden dependency of GOV-AGENT-001 activation unless Human governance later makes it one.

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

Future Phase B1 migration must be forward-only and non-destructive:

1. Open the existing DB using current safety pragmas.
2. Create V2 tables/indexes with `CREATE TABLE/INDEX IF NOT EXISTS` inside one controlled migration transaction.
3. Record schema migration version separately; do not infer Workflow V2 activation merely from table existence.
4. Do **not** backfill fake assignments/specs/reviews for historical tasks.
5. Only explicitly authorized/enrolled V2 tasks receive `task_workflow` rows; no historical task is enrolled because it happens to exist in `tasks`.
6. Keep existing `tasks.owner` behavior for V1; V2 implementation ownership is projected from the active Implementer assignment while compatibility fields may be mirrored only if implementation proves this is safe and atomic.
7. Migration tests must open a real-format legacy fixture, migrate it, restart, and verify every old record remains readable.
8. On migration failure, roll back the transaction and continue on the prior schema; never reset the DB.
9. Preserve existing owner/lease rows, checkpoints, progress, dependencies, budget history, task history, P0/P1/P2 records, Review Log artefacts, and historical Codex/Antigravity attribution exactly as evidence; no synthetic V2 backfill is permitted.
10. Current budget/quota schema and enforcement semantics remain unchanged; GOV-AGENT-001 adds no resource-policy migration.

Schema availability and workflow activation are separate concerns. A database can contain V2 tables while `WORKFLOW_V2_ENABLED=false` and all tasks continue under V1.

## 30. Repository Change Plan

### 30.1 This task

```text
MODIFY  docs/tasks/GOV-AGENT-001_FOUR_AGENT_GOVERNANCE_ORCHESTRATION_SPEC.md
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

- **PR A — GOV-AGENT-001-SPEC:** specification remediation only (this task).
- **PR B — GOV-AGENT-001-MCP-DB:** additive MCP V2 database foundation/migration only.
- **PR C — GOV-AGENT-001-MCP-TOOLS:** role/spec/implementation/review/CI state and tool contracts, preserving legacy behavior.
- **PR D — GOV-AGENT-001-MERGE-EVIDENCE:** evidence verification levels plus provisional/authoritative merge-gate logic.
- **PR E — GOV-AGENT-001-AGENTS:** four role contracts, minimal P0 skills, manifest/templates; **no activation**.
- **PR F — GOV-AGENT-001-ACTIVATION:** Human-approved governance cutover/configuration and activation marker.
- **PR G — GOV-AGENT-001-PILOT-CLOSEOUT:** bounded pilot evidence, findings/remediation, and adoption recommendation/status reconciliation.

No giant implementation PR is authorized by this specification. Each PR must have its own bounded scope, tests, exact-SHA independent review, CI, and merge eligibility under the governance active at that time. Installation of schema/tools/agents does not imply activation.

## 31. Implementation Phases

Full Workflow V2 is the target architecture, but delivery is intentionally incremental. Every future phase requires its own authorization/scope and does not inherit implementation authorization from this specification.

### Phase A — Specification remediation (current)

- **Objective:** resolve independent review findings F-01…F-06 while retaining Full Workflow V2.
- **Files/modules:** this specification only.
- **Dependencies:** Product Owner Full V2 decision and prior review of SHA `6ed80f65...`.
- **Tests/checks:** changed-file gate, structural/AC checks, `git diff --check`, no implementation diff.
- **Review:** independent specification re-review on exact remediation SHA.
- **Rollback:** revert only this specification commit if rejected; no runtime state exists to roll back.
- **Exit:** v0.2.0 committed/pushed; re-review pending; no Workflow V2 implementation or activation.

### Phase B1 — MCP schema migration only

- **Objective:** install additive V2 tables/indexes/schema-version metadata without changing active workflow behavior.
- **Files/modules:** primarily MCP store/migration code and migration tests/fixtures; no agent/governance activation files.
- **Dependencies:** accepted specification; separately authorized implementation task.
- **Tests:** legacy-format DB migration, restart persistence, foreign keys/indexes/uniqueness, failed-migration rollback, byte/record-level preservation where practical, no fake backfill.
- **Review:** independent fixed-SHA implementation review + required CI.
- **Rollback:** disable/uninstall use of new schema while preserving created tables/rows; never reset/delete legacy or V2 evidence.
- **Exit:** schema available, legacy behavior unchanged, V2 still inactive.

### Phase B2 — MCP role/spec/review/CI tools and state logic

- **Objective:** implement V2 enrollment, assignments, spec submission/freeze/supersession, implementation evidence, reviews, CI evidence, and compatible checkpoint/state views.
- **Files/modules:** MCP server/store/admin/contracts/tests; no governance activation.
- **Dependencies:** B1 schema foundation.
- **Tests:** role permissions, assignment concurrency, freeze authority checks, supersession, exact-SHA staleness, review independence, immutable evidence, V1 compatibility.
- **Review:** independent fixed-SHA review + CI; security review if implementation changes a relevant security boundary.
- **Rollback:** stop using V2 tools; preserve all rows; V1 paths remain usable for V1 tasks.
- **Exit:** tools/state logic implemented but no project task is automatically activated/enrolled.

### Phase B3 — Provisional / authoritative merge evidence logic

- **Objective:** implement evidence verification levels and fail-closed `provisional_ready` / `authoritative_merge_eligible` computation.
- **Files/modules:** MCP gate/evidence modules, verifier adapters if separately authorized, tests/docs.
- **Dependencies:** B1+B2; clear verifier policy for each authoritative evidence class.
- **Tests:** recorded-only CI cannot authorize merge; missing verifier capability blocks authoritative eligibility; exact-SHA mismatch/stale evidence fails; Human/PR/CI/review verification semantics; consistent snapshot reads.
- **Review:** independent fixed-SHA Quality and Security review of gate logic + CI.
- **Rollback:** disable V2 gate consumption and return to current external/manual merge verification; preserve evidence records.
- **Exit:** gate reports both concepts correctly and never emits authoritative readiness from trust-only metadata.

### Phase C — Four agent role contracts

- **Objective:** create the standing Planner, Implementer, Security Reviewer, and Quality Reviewer packages with authority boundaries and client/model-independent contracts.
- **Files/modules:** `agents/README.md`, `agents/manifest.yaml`, `agents/roles/*.md`, review templates as needed.
- **Dependencies:** accepted architecture; B2/B3 contracts stable enough to reference.
- **Tests:** schema/lint/manifest validation, forbidden-action checks, role/assignment compatibility fixtures.
- **Review:** independent fixed-SHA review of role contracts; no role may self-approve its own authority expansion.
- **Rollback:** remove/disable package use while preserving Git history; no workflow change because activation has not occurred.
- **Exit:** roles installed and reviewable, still **NOT ACTIVATED**.

### Phase D — Minimum P0 skill package

- **Objective:** implement only the P0 skills listed in §22 with minimal manifest/version plumbing.
- **Files/modules:** `agents/skills/{shared,planner,implementer,security,quality}/` plus manifest references.
- **Dependencies:** Phase C role contracts.
- **Tests:** required-input/output contracts, forbidden-action behavior, governance precedence, missing/incompatible skill failure behavior.
- **Review:** independent exact-SHA review + applicable CI.
- **Rollback:** disable/remove skill loading for future assignments; preserve installed artefacts/history.
- **Exit:** P0 skills available; P1/FUTURE skills remain out of scope; no activation.

### Phase E — Governance activation

- **Objective:** explicitly activate Workflow V2 for eligible, specifically enrolled tasks under Human approval.
- **Files/modules:** `AGENTS.md`, Autonomous Agent Protocol, activation config/marker and necessary operational docs; no unrelated product implementation.
- **Dependencies:** B1–D accepted/merged; authoritative evidence strategy tested; explicit Human activation approval.
- **Tests:** activation-off retains V1; activation-on enrolls only authorized V2 tasks; rollback/disable behavior; governance precedence and stop conditions.
- **Review:** independent governance review + required CI; Human approval is mandatory for activation.
- **Rollback:** stop new V2 enrollment, disable activation flag/routing, preserve all DB/Git/review evidence; do not translate in-progress V2 tasks silently.
- **Exit:** immutable `WORKFLOW_V2_ACTIVATION_COMMIT` recorded. Only then is V2 **ACTIVATED** for explicitly enrolled tasks.

### Phase F — Bounded pilot

- **Objective:** demonstrate end-to-end role separation, frozen spec, exact-SHA CI/reviews, provisional/authoritative gates, rollback, and auditability on a specifically authorized non-production task.
- **Files/modules:** only the authorized pilot task scope plus its governance/review evidence.
- **Dependencies:** Phase E activation; pilot authorization.
- **Tests:** task-specific tests plus forced stale-SHA/re-review and rollback drills where safe. Both Security and Quality review are mandatory for the pilot regardless of automatic R0–R4 routing.
- **Review:** both independent review streams on final SHA; authoritative pre-merge verification.
- **Rollback:** checkpoint pilot, stop new V2 enrollment, preserve evidence, route later tasks to V1 only by Human-approved governance decision.
- **Exit:** pilot closeout records findings/resolutions and a Human-reviewed adoption decision; automated risk routing remains inactive unless separately activated.

### Phase G — Full project adoption

- **Objective:** make V2 the normal workflow for future explicitly authorized project tasks and optionally activate validated R0–R4 routing.
- **Files/modules:** governance/config/state reconciliation only as separately authorized; no automatic rewrite of historical V1 tasks.
- **Dependencies:** successful Phase F and explicit Human adoption approval.
- **Tests:** mixed V1/V2 history, routing, review requirements, authoritative gates, operational recovery.
- **Review:** governance/security/quality review appropriate to adoption change + CI.
- **Rollback:** stop new V2 enrollment and revert future routing to the approved V1 process without deleting V2 evidence.
- **Exit:** adoption decision and activation/routing status are durable and auditable.

### Phase H — AI-CONV tasks

- **Objective:** use the established V2 workflow for separately authorized AI-CONV work while preserving current AI-IP/patent contracts.
- **Files/modules:** only each authorized AI-CONV task plus required evidence; no automatic provider/data/production expansion.
- **Dependencies:** Phase G or an explicit bounded exception; `ai-ip-domain` and `patent-conversion-review` P0 skills validated.
- **Tests:** task-specific offline/synthetic AI-IP validation, evidence/source fidelity, unsupported-inference controls, existing contract compatibility.
- **Review:** R3 treatment requires both Security and Quality reviews on exact final SHA unless Human governance explicitly defines a stricter rule.
- **Rollback:** task-specific rollback/checkpoint under V2; preserve all evidence and current production/provider/data boundaries.
- **Exit:** each AI-CONV task closes independently under its own authorization. Provider/API, real/confidential data, legal filing, and production remain separately gated.

Phases B1–H are future work and are **not authorized** by this specification-remediation task.

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
- current budget/quota behavior remains unchanged by GOV-AGENT-001 changes;
- recorded-only external evidence can produce at most provisional readiness;
- authoritative eligibility stays false when required verifier capability/evidence is absent;
- spec freeze fails without committed SHA/version + Human authorization + orchestration record;
- concurrency prevents incompatible claims/assignments;
- restart preserves V2 state;
- rollback/disable mode preserves all records.

Future governance/agent tests should validate forbidden actions, role/skill routing, R0–R4 routing, fixed-SHA review contracts, reviewer read-only behavior, and review-template completeness. R3 fixtures must remain synthetic/offline unless a separate authorization permits real data.

## 33. Rollback Strategy

The activation boundary is the concrete governance concept `WORKFLOW_V2_ACTIVATION_COMMIT`.

- **Before** that Human-approved commit: Workflow V1 remains authoritative for project execution.
- Installing V2 SQLite schema does **not** activate V2.
- Installing MCP V2 tools or agent/skill packages does **not** activate V2.
- **After** the activation commit: only tasks explicitly authorized/enrolled for V2 use Workflow V2; historical V1 tasks remain V1 evidence unless separately migrated by Human decision.

Preferred runtime control is an explicit repository/governance configuration equivalent to `WORKFLOW_V2_ENABLED=false/true`, with the activation commit recorded separately from schema/tool installation.

Rollback behavior:

- stop assigning new tasks to V2;
- keep all V2 tables/rows/review artefacts/specs readable;
- allow already merged historical V2 evidence to remain immutable history;
- route newly authorized tasks back to the approved V1 workflow if Human governance permits;
- retain legacy MCP tables and clients;
- do not restore a database backup destructively and do not delete V2 rows.
- never silently translate a partially completed V2 task, frozen spec, review, or CI record into V1 semantics.

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
| Legacy quota/budget behavior interacts awkwardly with future V2 work | Workflow interruption | Preserve current behavior in GOV-AGENT-001; address only under separately authorized `GOV-RESOURCE-001` |
| Agent skills conflict with governance | Authority inversion | Governance precedence; blocked/handoff on conflict |
| Review artefacts expose secrets/confidential IP | Data leak | least-privilege evidence, no secrets/full research content, security checklist |

## 35. Open Questions

The following must be resolved before or during the specifically authorized future phase; none blocks independent review of this architecture unless the reviewer identifies it as critical:

1. Whether agent identity remains trust-based for initial V2 pilot or requires authenticated client identity before activation.
2. Whether GitHub/CI fact verification is added inside MCP or remains an external merge-time check in the initial implementation.
3. Exact repository config location/name for `WORKFLOW_V2_ENABLED` and the activation commit marker.
4. Whether V2 compatibility should mirror active Implementer ownership into legacy `tasks.owner/branch/worktree` or expose it only through the new assignment view.
5. Whether R2 security review becomes mandatory for all file-upload/parser changes rather than threat-surface conditional after pilot evidence exists.
6. Whether review artefacts are always committed before merge or can be referenced from an immutable external review system with a later governance reconciliation commit.

Spec-freeze authority is **resolved** by §16.1 and is not an open question. Quota/resource modernization is **out of scope** and deferred to `GOV-RESOURCE-001`, not an open GOV-AGENT-001 migration question.

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
| AC-12 | Merge gate explicit/deterministic | Addressed — §§18,20 |
| AC-13 | Risk classes R0–R4 or alternatives defined | Addressed — §15 |
| AC-14 | Agent role package architecture specified | Addressed — §21 |
| AC-15 | Skill contract format specified | Addressed — §22 |
| AC-16 | Minimum shared/role-specific skills identified | Addressed — §§22–23 |
| AC-17 | Historical review evidence preserved | Addressed — §§24,28 |
| AC-18 | Old tasks not retroactively rewritten | Addressed — §§3,28–29 |
| AC-19 | Current quota/budget behavior explicitly unchanged; modernization deferred to GOV-RESOURCE-001 | Addressed — §§7,17,26,29 |
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
| AC-31 | Full Workflow V2 retention is an explicit Product Owner architecture decision | Addressed — §§1.2,2,6,31 |
| AC-32 | Recorded/provisional evidence is distinguished from authoritative merge eligibility | Addressed — §§17.7,18.1,20 |
| AC-33 | Recorded-only CI PASS cannot satisfy authoritative merge eligibility | Addressed — §§18,20.3 |
| AC-34 | Evidence verification levels and source/recorder/verifier responsibilities are defined | Addressed — §§17.7,18.1 |
| AC-35 | Spec freeze requires committed artefact, exact SHA/version, explicit Human authorization, and orchestration record | Addressed — §16.1 |
| AC-36 | Planner cannot self-authorize spec freeze and MCP cannot create Human authorization | Addressed — §§16.1,18 |
| AC-37 | Spec change after implementation begins supersedes prior spec and requires evidence reconciliation | Addressed — §§16.1,17.3,19 |
| AC-38 | Risk routing distinguishes DESIGNED, IMPLEMENTED, and ACTIVATED | Addressed — §15 |
| AC-39 | Pilot may require mandatory Security + Quality before automated R0–R4 routing activation | Addressed — §§15,31 Phase F |
| AC-40 | P0 skill activation set is minimal and exact; other skills are P1/FUTURE | Addressed — §22 |
| AC-41 | V2 schema model defines purpose/keys/uniqueness/indexes/mutability/timestamps/staleness/backward compatibility | Addressed — §17 |
| AC-42 | V1 tasks/history/owners/leases/checkpoints/budget/reviews are preserved without fake V2 backfill | Addressed — §§17,24,28–29 |
| AC-43 | Schema/tool/agent installation is separate from Workflow V2 activation | Addressed — §§29–33 |
| AC-44 | Activation requires explicit Human approval and `WORKFLOW_V2_ACTIVATION_COMMIT` | Addressed — §§31 Phase E,33 |
| AC-45 | Rollback preserves V2 DB/Git/review evidence and never requires SQLite reset | Addressed — §§29,31,33 |
| AC-46 | Implementation is split into bounded PRs/phases; no giant implementation PR is authorized | Addressed — §§30–31 |
| AC-47 | Four standing roles remain client/model independent and role != skill != task spec | Addressed — §§21–25 |
| AC-48 | Agent identity limitations remain explicit; future authenticated identity is separately scoped | Addressed — §27 |
| AC-49 | Remediation A->B stales Security(A), Quality(A), and CI(A) for B while preserving history | Addressed — §§14,17,19 |
| AC-50 | Reviews include reviewer/model/spec/base/implementation/verdict/findings/blockers/evidence and exact-SHA semantics | Addressed — §§17.5,24 |
| AC-51 | Branch/PR state and merge result require authoritative external verification for eligibility/closeout | Addressed — §§18.1,20 |
| AC-52 | No implementation, activation, provider/API, real/confidential data, or downstream task is performed by this remediation | Addressed — §§7,31,38; verify changed-file gate before commit |

## 37. Implementation Handoff

```text
Task ID: GOV-AGENT-001
Agent: Planner / Architecture & Governance Specification Agent
Reviewer: Independent specification reviewer — pending
Status: READY FOR INDEPENDENT SPECIFICATION RE-REVIEW
Version: 0.2.0
Work completed: Remediated F-01…F-06 while intentionally retaining Full Workflow V2; defined evidence verification levels and provisional/authoritative merge gates; resolved spec-freeze authority; removed quota redesign from scope; phased risk routing; narrowed P0 skills; expanded schema, migration, implementation PR, activation, pilot, adoption, and rollback contracts.
Files affected: This specification artefact only, subject to pre-commit verification.
Evidence checked: Governance docs, workflow/protocol docs, control center/review log, P2 task/ADR boundaries, MCP source/tests/package behavior, Git/GitHub baseline.
Findings: Prior v0.1.0 review returned REQUEST CHANGES; this version addresses the trust/merge-gate, Full V2 scope, freeze authority, quota boundary, risk-routing rollout, and P0 skill findings without claiming re-review PASS.
Decisions: Full Workflow V2 intentionally retained; additive V2 sub-state model; two independent fixed-SHA review streams; recorded/provisional vs authoritative merge evidence; Git durable evidence + MCP operational index; quota unchanged; explicit cutover and reversible activation.
Issues: Open questions in §35; independent specification review pending.
Security impact: Specification only; no runtime/security boundary changed.
Recommended next action: Independent fixed-SHA re-review of this specification remediation commit. Do not implement Phase B1–H before separate authorization/review gates.
```

Downstream implementers must treat this document as architecture proposal until the required independent specification review and Human governance disposition are recorded. A PASS on this specification would authorize nothing beyond what the Human separately authorizes.

## 38. Explicit Non-Implementation Statement

This task changed no Project Orchestrator MCP TypeScript, SQLite schema/database, backend/frontend/application/AI runtime, prompt, JSON schema, DOCX renderer/template, CI behavior, provider/model runtime, production/deployment configuration, current governance activation file, or historical review record. It used no real/confidential research data and made no provider/API call. It does not change P2-001/P2-002/P2-003/P2-004 technical semantics or start downstream AI-CONV work.

**GOV-AGENT-001 FULL WORKFLOW V2 SPECIFICATION REMEDIATION COMPLETE —**
**FULL V2 INTENTIONALLY RETAINED —**
**NO WORKFLOW V2 IMPLEMENTATION OR ACTIVATION PERFORMED.**
