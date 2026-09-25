# Autonomous Agent Protocol — Project Orchestrator MCP

Version: 0.1.0 | Status: tooling instructions | Date: 25/09/2026
Scope: local task coordination only; production APP-003 remains frozen until
26/09/2026 and is not implemented by this tooling task.

## Authority and preflight

Read AGENTS.md, PROJECT_CONTEXT.md, docs/system-specification.md and the
relevant approved task specification. Check the current branch, worktree,
worktree cleanliness, upstream main and pending edits. Do not overwrite Human
files or another agent's branch. The orchestrator records metadata but does
not create, check out, clean or merge Git worktrees.

For each task: consult budget.should_continue and project.next_task. Obtain
Human approval for PLANNED work; approval is recorded through the local admin
command with a real decision reference. Create a separate non-main branch and
worktree for the task, then atomically call project.claim_task with owner,
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

A reviewer finding may lead to REVIEW_CHANGES_REQUIRED; Human approval returns
it to APPROVED for correction. BLOCKED records a stopped handoff and must be
reviewed before Human reapproval. A lease expiry or explicit release moves
uncompleted work back to APPROVED, preserving progress and checkpoint records.
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
research inputs, canonical schema/prompt changes, main merge, destructive Git
actions or quota reset activation. Keep APP-003 unmodified before 26/09/2026
Vietnam time. Do not run the P0 seed tasks during orchestrator development.

Never force push, reset --hard, rewrite shared history, merge main, git add .,
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
read confidential papers, provide authentication, or bind a TCP port. A Human
checks those facts and controls workflow gates outside MCP.
