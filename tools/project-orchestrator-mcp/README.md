# Project Orchestrator MCP (local tooling)

A local MCP server for the AI IP Description Generator task queue. Version 0.1.0.
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

The server seeds P0-001 through P0-008 as PLANNED only. P0-001 is frozen until
26/09/2026 00:00 in Vietnam; the entire queue still requires recorded Human
approval before any task can be claimed. A dependent task waits for the
predecessor to reach COMPLETED. The database is initialized once; restarts
never overwrite task or budget state. Quota cycles are labels for Human records,
not additional balances. The two weekly and two banked cycles are never
combined or activated automatically.

## Human gates and lifecycle

An authorized Human records approval using the local administrator CLI only,
after reviewing a task and its scope:

    npm run admin -- approve P0-001 HUMAN-DECISION-REFERENCE

It refuses approval of P0-001 before its freeze ends. Evidence-backed lifecycle
transitions are administrative and never run Git operations:

    npm run admin -- transition P0-001 AWAITING_REVIEW REVIEW-REFERENCE

States are distinct: PLANNED, APPROVED, CLAIMED, IN_PROGRESS, IMPLEMENTED,
AWAITING_REVIEW, REVIEW_CHANGES_REQUIRED, REVIEW_PASS,
AWAITING_HUMAN_APPROVAL, MERGED, COMPLETED, BLOCKED.
The MERGED status only records independent Human-provided evidence; the
software never merges a branch or touches Git history.

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
Human must create a separate branch/worktree before editing, check the actual
Git state, and record true commit/test evidence. Calls from trusted local IDE
agents can change the manually recorded budget; treat IDE access as trusted.
For rules and escalation, see docs/operations/AUTONOMOUS_AGENT_PROTOCOL.md.
