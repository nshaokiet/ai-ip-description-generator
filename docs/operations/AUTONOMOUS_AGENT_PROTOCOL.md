# Autonomous Agent Protocol — Project Orchestrator MCP

Version: 0.2.0 | Status: conditional Phase E governance; not active on branch | Date: 07/10/2026
Scope: local task coordination only. APP-003 was historically deferred until
26/09/2026 and has since been implemented/merged; this protocol does not
authorize production operation or change task authority.

Historical version 0.1.1 was a factual P0-008 correction only. Version 0.2.0
adds Human E-01–E-06 V1/V2 coexistence and external/manual verification, effective
only after reviewed Phase E merge/verification on main. This pre-1.0 minor is a
breaking governance change; V1 history, leases, product policy and quota remain.

## Authority and preflight

Read AGENTS.md, PROJECT_CONTEXT.md, docs/system-specification.md and the
relevant approved task specification. Check the current branch, worktree,
worktree cleanliness, upstream main and pending edits. Do not overwrite Human
files or another agent's branch. The orchestrator records metadata but does
not create, check out, clean or merge Git worktrees.

For each task: consult budget.should_continue and project.next_task. Obtain
Human approval for PLANNED work; approval is recorded through the local admin
command with a real decision reference. Create a separate non-main branch and
worktree for the V1 task, then atomically call project.claim_task with owner,
branch and worktree. If another agent owns the task, do not edit it. Periodically
renew the lease or report progress. A lease is coordination rather than
operating-system file locking: agents must honor it.

## Task states and evidence

PLANNED -> APPROVED (recorded Human decision)
APPROVED -> CLAIMED (atomic owner lease)
CLAIMED -> IN_PROGRESS (first report)
CLAIMED/IN_PROGRESS -> IMPLEMENTED (commit SHA and test evidence)
IMPLEMENTED -> AWAITING_REVIEW -> REVIEW_PASS or REVIEW_CHANGES_REQUIRED
REVIEW_PASS -> AWAITING_HUMAN_APPROVAL -> MERGED -> COMPLETED

These preserved legacy MCP state names do not require repeated permission for
operations already covered by AGENTS.md standing delegation. Actual authority,
merge eligibility and exceptions come from governance/real evidence, not MCP.
Use the role-aware flow below for explicitly enrolled V2 tasks.

A reviewer finding may lead to REVIEW_CHANGES_REQUIRED; Human approval returns
it to APPROVED for correction. BLOCKED records a stopped handoff and must be
reviewed before Human reapproval. A lease expiry or explicit release moves
uncompleted work back to APPROVED, preserving progress and checkpoint records.
These are legacy admin transitions, not new approval requirements for remediation
already within recorded Human scope/standing delegation. Exceptions still require
Human decision; never invent an admin transition if the tool cannot record it.
MERGED is a recorded status, never an action performed by this server. A task
is eligible as a dependency only once COMPLETED, not when IMPLEMENTED,
REVIEW_PASS or MERGED.

## Quota and checkpoint procedure

Initial Human record: Codex 14% remaining, stop threshold 8%, source manual.
Remaining >8: CONTINUE. Remaining <=8: STOP_AND_CHECKPOINT.
Reject values outside 0-100. When stopped, do not call claim, report or finish.
Create a checkpoint/handoff that records task, branch, last safe commit,
completed work, tests, remaining work, blockers, reason and exact next action.
Manual update from 8 to 100 changes the decision to CONTINUE. Weekly
26/09, banked #1, weekly 03/10 and banked #2 are separate potential cycles;
a Human enters the actual available percentage and cycle. Never add cycles
or activate a reset automatically. The server never scrapes an IDE quota UI.

## Required escalation

STOP and ask for Human decision before architecture changes, scope expansion,
security/privacy choices, provider/model changes, paid APIs, confidential
research inputs, canonical schema/prompt changes, merge without satisfied
AGENTS.md §8.2/§24 gates, destructive Git
actions or quota reset activation. The historical APP-003 deferral before
26/09/2026 Vietnam time no longer applies; do not infer authority for new
implementation tasks from its expiration. Do not run P0 seed tasks during
orchestrator development.

Never force push, reset --hard, rewrite shared history, bypass merge gates, git add .,
delete Human files/branches, or use unapproved paid services. No MCP tool
performs these operations. Verify real Git SHA, diff, tests and changed files
before recording progress; metadata entered by an agent is not automatic
verification or Human approval.

## Shared IDE setup and limitations

Install and build tools/project-orchestrator-mcp, then configure each IDE with
an absolute path to dist/src/server.js. VS Code uses workspace .vscode/mcp.json
with servers and a stdio entry; Antigravity IDE uses its raw mcp_config.json
with mcpServers and a command/args entry. Both spawn distinct stdio processes
sharing a user-local SQLite database. The database has atomic immediate
transactions and a busy timeout for concurrent claims. Details and examples:
tools/project-orchestrator-mcp/README.md.

The service trusts local clients: agent identities, Human decision references,
branches, test reports and SHAs are user-supplied. It does not inspect Git,
read confidential papers, provide authentication, or bind a TCP port. A Human or
delegated integration owner under current governance checks those facts and
controls gates outside MCP. Identity remains PROCEDURAL_TRUST_BASED.

## Conditional V2 activation and selection

The single marker is [WORKFLOW_V2_ACTIVATION.yaml](WORKFLOW_V2_ACTIVATION.yaml).
enabled=true on a branch does not activate V2. Only the reviewed Phase E PR merge
commit on main, accepted after Human approval, independent governance PASS and
required CI, becomes WORKFLOW_V2_ACTIVATION_COMMIT. Verify merge/main/ancestry and
post-merge CI; record the immutable merge SHA in durable closeout. The implementation
SHA is not the activation commit. No schema/tool/agent installation activates V2.

Before each admission/action, externally check current main's marker and accepted
activation record. OFF/unmerged/unverified means V1 for new/unenrolled tasks. ON
plus explicit Human task authorization, V2 enrollment referencing that exact merge,
and required role/spec/evidence state permits the V2 action. No automatic enrollment
or historical V1 migration. Existing V2 history with invalid/disabled prerequisites
requires checkpoint/Human disposition, not silent fallback.

## V2 enrollment, roles and current candidate

An authorized Human/operator may use the existing command only after external
preflight under [WORKFLOW_V2_MANUAL_VERIFICATION.md](WORKFLOW_V2_MANUAL_VERIFICATION.md):

```text
npm run admin -- enroll-v2 /absolute/path/to/enrollment.json
```

Require a separately authorized prospective task and exact activation_commit.
The command validates recorded input; it does not authenticate Human identity,
verify an activation merge or automatically enforce this marker. Phase E executes
no enrollment or runtime change. MCP's hardcoded NOT ACTIVATED diagnostic is not
canonical global activation evidence; report that limitation honestly.

Human task authorization → explicit enrollment → PLANNER assignment → versioned
spec → Human-authorized freeze → IMPLEMENTER assignment/lease → implementation →
exact-SHA CI → required independent SECURITY_REVIEWER and/or QUALITY_REVIEWER →
external verification → merge → post-merge verification/closeout.

Planner cannot own implementation/self-freeze; Implementer cannot self-approve;
reviewers are read-only and verdicts stay stream-specific. Use the
[agents role contracts](../../agents/README.md). F comes only from the persisted
same-task current pointer, not a latest-row guess. New spec/head stales prior
CI/review/verification and requires applicable fresh evidence.

## External/manual merge verification and routing

Follow the linked source-by-source runbook immediately before merge: actual Human
scope/exceptions, frozen committed spec/freeze authority, Git base/final SHA, actual
exact-head CI, canonical independent read-only required PASS reports, fresh correct
OPEN/mergeable PR/head, confidentiality/scope, stop conditions and platform controls.
Record provenance/results. Unavailable/failed required evidence blocks merge.
After merge verify actual main/ancestry and exact main CI. Delegated normal merge
requires all AGENTS.md gates and is not automatic or an MCP operation.

B3 authoritative_merge_eligible remains false; verifier adapters remain unavailable.
provisional_ready is not merge permission. RECORDED != VERIFIED; MCP state/model
metadata are not authenticated external truth/identity. No adapter override or
platform-denial bypass. Quota and Human exception authority remain unchanged.

Automatic R0–R4 routing is NOT ACTIVATED. The separately authorized Phase F pilot
requires BOTH Security and Quality on the same final SHA. Other V2 tasks before
Phase G need explicit Human/task-spec required streams; unclear policy blocks.
Phase F is NOT STARTED. No pilot/adoption/provider authority is created here.

## V2 rollback / disable

A separately reviewed Human governance change disables the marker on verified main
and stops new enrollment. Preserve all V2 database/Git/spec/assignment/review/CI/
verification evidence: no deletion/reset/backfill. Checkpoint in-progress V2 tasks;
Human chooses finish-under-V2 or explicit stop/reauthorize/restart-under-V1. Never
silently translate active V2 work. Unenrolled/new tasks use approved V1 if authorized.
Preserve safe reads/checkpoints/handoffs, immutable activation history and quota.

## Version history

| Old | New | Date | Author | Change / reason | Breaking change |
|---|---|---|---|---|---|
| 0.1.0 | 0.1.1 | 28/09/2026 | Codex | P0-008 factual status correction | No |
| 0.1.1 | 0.2.0 | 07/10/2026 | Codex | Human E-01–E-06; conditional selection/manual authority; reconcile obsolete blanket merge prohibition with AGENTS delegation | Yes — governance; no runtime/API change |
