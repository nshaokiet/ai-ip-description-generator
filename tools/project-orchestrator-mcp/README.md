# Project Orchestrator MCP (local tooling)

A local MCP server for the AI IP Description Generator task queue. Version 0.3.0.
This tool does not invoke the application pipeline, AI providers, Git commands or paid APIs.

## Requirements and install

- Node.js 24 or later (uses the built-in node:sqlite module).
- From tools/project-orchestrator-mcp run: npm install
- Run: npm run typecheck
- Run: npm test
- Run: npm run build
- Start a local stdio instance: npm start

The server writes JSON-RPC to stdout; diagnostic output must use stderr.
It creates its SQLite database in the user's home directory at
.ai-ip-description-generator/project-orchestrator.sqlite, unless PROJECT_ORCH_DB
names a different absolute local path. VS Code and Antigravity processes on the
same machine and user account share the same database and task leases. Use the
same PROJECT_ORCH_DB for both if overriding the default. The database, including
journal files, is local and must not be committed.

## Workflow V2 data foundation (Phase B1)

Phase B1 installed SQLite schema version `2`, recorded in `schema_migrations`. Schema
availability is separate from workflow activation: **Workflow V2 is NOT
activated by this package version**. Package `0.3.0` preserves all 13 Workflow V1
tools and 11 Phase B2 tools, and adds one Phase B3 read (25 total).

Schema version 2 additively installs `task_workflow`, `task_assignments`,
`task_specs`, `implementation_evidence`, `reviews`, `ci_evidence`, and the
normalized append-only `evidence_verifications` table. Existing V1 tables and
rows remain unchanged. Historical tasks are not backfilled with synthetic V2
workflow, assignment, specification, review, CI, or verification records.

For F-07, `task_workflow.current_implementation_evidence_id` is the sole
persisted current-candidate selector and is protected by a same-task composite
foreign key. `implementation_evidence` keeps immutable candidate history and
does not use insertion order or a latest-row rule to select the current
candidate. Phase B2 implements expected-current compare-and-swap pointer updates
through `project.record_implementation`, including idempotent winner retries.

For F-08, verification state exists only in `evidence_verifications`. Internal
subjects use typed, same-task foreign keys; Security/Quality review subjects are
checked against the stored review type; versions form an append-only linear
supersession chain; `REVOKE` is `UNVERIFIED`; and a `VERIFIED` attestation
requires verifier provenance fields. Phase B2 records these claims through a
narrow admin path and canonicalizes external subject keys. Source verification
and merge-gate computation are described under Phase B3 below. No source verifier
adapter is installed.

Migration runs inside `BEGIN IMMEDIATE`, is restart-safe and idempotent, and
keeps `foreign_keys=ON`, WAL, and the 5000 ms busy timeout model. A failed or
incompatible migration is rolled back and never resets or deletes the existing
database. Budget/quota tables and enforcement semantics are unchanged.

## Workflow V2 tools/state (Phase B2)

Schema version `3` additively installs `review_attempts` for durable in-progress
review state (§17.5) and `checkpoint_assignments` for role metadata (§18), retaining
all B1 tables, evidence constraints, migration entries and legacy checkpoints.
No task is enrolled or governance activated by installing either schema version.

New tools: `project.assign_role`, `project.get_assignments`, `project.submit_spec`,
`project.freeze_spec`, `project.get_spec`, `project.start_implementation`,
`project.record_implementation`, `project.record_ci`, `review.start`,
`review.submit`, `review.get_status`. Existing `project.get_state` exposes additive
V2 sub-state or a V1 version marker. Checkpoint tools accept optional role/assignment
metadata; V2 callers must supply the matching active assignment. Implementer
checkpoint/handoff remains usable at the quota threshold.

Explicit enrollment and verification recording stay in the local Human/admin CLI:

```text
npm run admin -- enroll-v2 /absolute/path/to/enrollment.json
npm run admin -- record-verification /absolute/path/to/attestation.json
```

Payloads are validated by [v2-contracts.ts](src/v2-contracts.ts). Enrollment requires
task ID, risk class, authorization reference and exact activation commit; it is
prospective and refuses historical V1 execution. This records per-task capability
metadata only; it does not enable project governance or create an activation commit.

Freeze requires a current recorded Human authorization attestation covering the
exact committed spec artifact/version/SHA, its source/reference, and Human/admin
caller attribution. Planner identities cannot self-authorize. These are procedural
recorded claims: the package does not authenticate identity, inspect Git, or prove
that the committed artifact/Human decision exists. `VERIFIED` recording validates
supplied provenance fields; state views explicitly report `authority_validated=false`.
The B3 gate evaluates these fields without trusting their claimed authority.
**WORKFLOW V2 NOT ACTIVATED.** No source verifier or automatic merge permission
is implemented.

See [B2 implementation and test evidence](B2_IMPLEMENTATION.md) for the baseline,
record semantics, known limitations and exact added test inventory.

## Workflow V2 merge evidence (Phase B3)

`project.get_merge_gate` takes `task_id`. V2 `project.get_state` includes the same
snapshot result under `merge_gate`. F comes only from the persisted
`task_workflow.current_implementation_evidence_id`, never the newest history row.
Both V2 reads are idempotent and leave task/assignment leases and evidence untouched,
including expired leases. Recovery remains on `project.next_task` and execution
paths. Legacy V1 read recovery, budget/quota and task behavior remain compatible.
V1 `get_merge_gate` returns `NOT_APPLICABLE`; unknown tasks remain errors.

The gate validates complete typed verification chains, resolves their unique
terminal attestation/revocation, derives superseded history and checks applicability
against current spec/candidate/review assignments and expected PR identity. Invalid
chains, cross-task subjects, revocation and SHA mismatches fail closed. It retains
historical rows. `MERGE_RESULT` is visible history, not a pre-merge requirement.

`provisional_ready` means complete consistent recorded evidence, including current
Human task/freeze authorization, frozen spec, candidate, successful CI and required
independent read-only reviews. All observed CI records for F must be SUCCESS;
conflicting/pending records are not hidden by selecting one passing row. Review
attempt ordering is considered only within the exact F and stream; an in-progress
re-review cannot reuse earlier PASS. A recorded policy must explicitly resolve
scope, confidentiality, stop conditions and required Human exceptions. R3/R4 always
require Security and Quality; lower-risk Security requires an explicit recorded
boolean. `NOT_REQUIRED` never pretends a stream passed.

This narrow context lives in the **existing** task-authorization attestation's
`metadata_json.merge_policy`, recorded using the existing admin verification path.
There is no schema change, new activation/enrollment path or trusted identity:

```json
{
  "merge_policy": {
    "security_required": true,
    "required_human_exception_refs": [],
    "stop_conditions": [],
    "scope_violation": false,
    "secret_or_confidential_exposure": false,
    "repository": "synthetic/repo",
    "pr_number": 42
  }
}
```

The example is synthetic, not task authorization. Missing/invalid context is
`MERGE_POLICY_UNRESOLVED`. An explicit empty exception list records that no additional
Human exception is required; it does not waive existing governance. `repository`
and `pr_number` identify expected PR context; absence blocks authoritative eligibility
but does not block provisional readiness. Append policy changes/revocations through
the same immutable chain; do not edit past attestations.

`authoritative_merge_eligible` is **always false in this release**: no approved
Human/Git/CI/review/PR verifier or fresh pre-merge check adapter exists. The §18.1
source matrix is reported per subject, and claimed VERIFIED provenance cannot opt
into a trusted source by naming it. The output reports
`AUTHORITATIVE_VERIFIER_UNAVAILABLE`, `AUTHORITATIVE_SOURCE_POLICY_UNACCEPTED` for
unsupported VERIFIED claims, and `FRESH_PREMERGE_CHECK_UNAVAILABLE` for PR freshness.
This explicitly preserves `RECORDED != VERIFIED` and
`provisional_ready != authoritative_merge_eligible`. Actual source adapters require
separate authorization; B3 performs no Git, GitHub or external network operation.

Full required/observed gates, effective verification IDs/levels, applicability,
missing/stale/revoked evidence, exact SHA mismatch history, Human gates and separate
provisional/authoritative blockers are returned for diagnostics. Computation runs
inside one SQLite snapshot and persists no computed gate/status table. Schema stays
`3`; dependency versions and quota semantics stay unchanged.

See [B3 implementation and handoff evidence](B3_IMPLEMENTATION.md). Workflow V2
governance **NOT ACTIVATED**; Phase C **NOT STARTED**.

Stdio is chosen for client-spawned local servers. It opens no network listener;
127.0.0.1 binding is therefore inapplicable. An HTTP endpoint would require
separate local authentication and origin validation before exposure.

## VS Code setup

Official VS Code workspace MCP configuration uses .vscode/mcp.json with the
top-level servers object. This repository ignores .vscode/, so create this file
locally. Replace the path below with the full absolute path on your computer
and use forward slashes in JSON paths on Windows:

    {
      "servers": {
        "project-orchestrator": {
          "type": "stdio",
          "command": "node",
          "args": ["C:/path/to/ai-ip-description-generator/tools/project-orchestrator-mcp/dist/src/server.js"]
        }
      }
    }

Build the package before connecting. In VS Code open the Command Palette and
run MCP: List Servers to start the server and inspect its output. Source:
https://code.visualstudio.com/docs/agents/reference/mcp-configuration

## Antigravity IDE setup

In the agent panel, open the options menu, then MCP Servers > Manage MCP
Servers > View raw config. Add this entry under the existing mcpServers object
of the configuration opened by the IDE (global ~/.gemini/config/mcp_config.json
or workspace .agents/mcp_config.json). The example uses an absolute path;
do not replace other installed servers:

    {
      "mcpServers": {
        "project-orchestrator": {
          "command": "node",
          "args": ["C:/path/to/ai-ip-description-generator/tools/project-orchestrator-mcp/dist/src/server.js"]
        }
      }
    }

The official Antigravity IDE configuration format uses mcpServers for local
stdio commands. Refresh servers in the IDE after saving. Source:
https://antigravity.google/docs/mcp

A machine-specific path is deliberately not committed. Both IDE configurations
point to the same build and the same user-local SQLite database.

## Tools

- project.get_state: tasks in progress or a named task, worktree/branch, owner,
  blockers, most recent checkpoint, next action, budget and next eligible task.
- project.next_task: highest priority APPROVED task whose freeze date has
  passed, dependencies are COMPLETED, and blockers are clear.
- project.claim_task: atomic single-owner lease, non-main unique branch and
  worktree; default 60 minutes, configurable 1 to 1440.
- project.renew_lease: extend a live lease for the same owner.
- project.release_task: release a live lease back to APPROVED.
- project.report_progress: evidence and remaining work; renews lease 60 minutes.
- project.finish_task: marks IMPLEMENTED only; requires test evidence and SHA.
- budget.get, budget.set_remaining, budget.should_continue: manual budget
  updates, 0-100; >8 CONTINUE, <=8 STOP_AND_CHECKPOINT.
- checkpoint.create and checkpoint.get_latest: persisted restart-safe handoff.
- project.stop_and_handoff: atomic checkpoint then BLOCKED with lease released,
  including task, branch, safe commit, completed work, tests, remaining work,
  blockers, stop reason and exact next action.

The server seeds P0-001 through P0-008, the zero-cost Post-MVP roadmap
P1-001 through P1-006, and DEPLOY-001 as PLANNED only. The P1 tasks are, in priority order:
Frontend accessibility and type-safety hardening; Offline adversarial regression
expansion; Local security hardening; Developer experience and one-command local
run; Offline performance baseline; and UX polish, responsive behavior and error
recovery. DEPLOY-001 is a separate planned zero-cost demo/staging deployment task
for a synthetic/demo-only public URL; it has no seeded dependency and does not
select a hosting platform or authorize implementation. Priority is not a technical
dependency: P1 tasks and DEPLOY-001 require separate Human authorization before claim.
Seeding is not authorization; PLANNED does not mean approved. In the current
local project state P1-001 is COMPLETED while P1-002 through P1-006 remain PLANNED;
DEPLOY-001 is newly registered as PLANNED and is added to an existing database on restart.
An existing database may therefore already have P1-001 as COMPLETED. Seed
insertion uses INSERT OR IGNORE: restarting with a new build adds missing task
IDs without overwriting existing task state, owner, approval evidence,
branch/worktree or budget/quota. P0-001 is frozen until 26/09/2026 00:00 in
Vietnam; the entire queue requires recorded Human approval before claim. A
dependent task waits for its predecessor to reach COMPLETED. Quota cycles are
labels for Human records, not additional balances. The two weekly and two banked
cycles are never combined or activated automatically.

## Human gates and lifecycle

After pulling and building a version with new seed tasks, restart the MCP
server so the existing local SQLite database receives any missing task IDs.

An authorized Human records approval using the local administrator CLI only,
after reviewing a task and its scope. The placeholder below is illustrative
only; it is not an approval for any task:

    npm run admin -- approve TASK_ID HUMAN-DECISION-REFERENCE

It refuses approval of P0-001 before its freeze ends. Evidence-backed lifecycle
transitions are administrative and never run Git operations:

    npm run admin -- transition TASK_ID AWAITING_REVIEW REVIEW-REFERENCE

States are distinct: PLANNED, APPROVED, CLAIMED, IN_PROGRESS, IMPLEMENTED,
AWAITING_REVIEW, REVIEW_CHANGES_REQUIRED, REVIEW_PASS,
AWAITING_HUMAN_APPROVAL, MERGED, COMPLETED, BLOCKED.
The MERGED status only records evidence of a Git merge after applicable review
and CI gates; the software never merges a branch or touches Git history.

At <=8%, stop implementation and use checkpoint.create or
project.stop_and_handoff. A Human can manually update 8 to 100 with
budget.set_remaining and a new cycle label, but no reset is activated by MCP.
Lease expiry returns a CLAIMED/IN_PROGRESS task to APPROVED so a new agent can
claim it atomically; an agent should checkpoint before the lease expires.
A handoff BLOCKED task requires a Human review and fresh approval to resume.

## Boundaries

The service does not scrape quota, manipulate Git/worktrees, start APP-003,
approve its own tasks, authorize review/merge, inspect research data, or
authenticate a purported Human calling the local administrative CLI. The
implementing agent must create a separate branch/worktree before editing, check
the actual Git state, and record true commit/test evidence. Calls from trusted
local IDE agents can change the manually recorded budget; treat IDE access as
trusted.
For rules and escalation, see docs/operations/AUTONOMOUS_AGENT_PROTOCOL.md.
