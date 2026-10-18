# GOV-MCP-001 — V1 Task Registration Specification

| Field | Value |
| --- | --- |
| Document ID / version | GOV-MCP-001 specification / **0.1.0** |
| Date / status | 2026-10-18 / **Proposed — frozen-ready; independent review and Human freeze pending** |
| Workflow / owner | V1 / Codex |
| Reviewer | Gemini 3.8 Flash High / Antigravity STRICT READ-ONLY, independent fixed-SHA specification review pending |
| Issue / authorization | [Issue #126](https://github.com/nshaokiet/ai-ip-description-generator/issues/126) / [Human specification-only authorization](https://github.com/nshaokiet/ai-ip-description-generator/issues/126#issuecomment-6247423831) (`HUMAN-GOV-MCP-001-SPEC-PREPARATION-2026-10-18`) |
| Source baseline | Verified `main` `6809355c089364d72ecdf30ff6fb70aba20fe8ca`; [investigation receipt](https://github.com/nshaokiet/ai-ip-description-generator/issues/126#issuecomment-6247401301) |
| Implementation authority | **NOT GRANTED**. This document does not authorize code, schema, database, deployment, V2, or historical-state changes. |

## 1. Problem and source-grounded baseline

`project.get_state({task_id:"AI-CONV-004-IMPL"})` reported `Unknown task`. The independent source reconciliation in Issue #126 and a Codex-attributed disposable-SQLite/stdio reproduction support a missing registration route, not a verified diagnosis of the user's live database or client version. The static `SEED` in [`store.ts`](../../tools/project-orchestrator-mcp/src/store.ts) (lines 33–49) contains P0/P1/DEPLOY IDs, not AI-CONV IDs; bootstrap uses `INSERT OR IGNORE` (69–74). Exact `tasks.id` lookup throws for absence (87–90). `addTask` (150–158) is a direct, non-idempotent insert without provenance. [`admin.ts`](../../tools/project-orchestrator-mcp/src/admin.ts) (5–19) has no register command; [`server.ts`](../../tools/project-orchestrator-mcp/src/server.ts) (30–33) exposes lookup, not registration. [`migrations.ts`](../../tools/project-orchestrator-mcp/src/migrations.ts) is at schema v3 and uses `BEGIN IMMEDIATE`/rollback (340–409). V2 enrollment requires a pre-existing task ([`v2-store.ts`](../../tools/project-orchestrator-mcp/src/v2-store.ts), 61–74).

The source of authority is the actual Human decision under [`AGENTS.md`](../../AGENTS.md) §§3–10, 16–20 and 24–25, not a row in MCP. Existing project [context](../../PROJECT_CONTEXT.md), [system specification](../system-specification.md), [Control Center](../operations/01_PROJECT_CONTROL_CENTER.md) and [Review Log](../operations/02_GEMINI_REVIEW_LOG.md) keep Git/governance completion distinct from MCP operational state. Issue #123 remains CLOSED/COMPLETED; this work must not recreate its historical approval, owner, lease, review, transition or completion.

## 2. Scope, architecture and trust boundary

The future implementation adds one **local administrative CLI** command, `npm run admin -- register-task /absolute/path/to/manifest.json`, backed by a Store registration method and additive SQLite provenance. It registers one previously absent, prospective **Workflow V1** task as `PLANNED`. It must not call `approveTask`, `claim`, `transition`, `checkpoint`, `enroll-v2`, or any other lifecycle method. It must not expose `register-task` through MCP, auto-discover GitHub issues, sync a catalog at startup, or create tasks merely because an ID is queried. The existing seed catalog and legacy state remain intact.

Registration is an operator action after **external Human-authorization preflight**. The command validates the shape of a receipt reference and records it; it cannot prove the author, decision meaning, approval scope, or the operator's identity. A reference is procedural provenance, **not cryptographic authentication or approval**. The operator must inspect the actual Human decision, exact task ID, scope, dependencies and prospective status before invoking the command. A `PLANNED` task still needs the existing separate administrative approval decision before a claim. This spec does not authorize running the command against any active database.

Threats include a forged/misleading receipt URL, arbitrary local file input, duplicate/concurrent operators, malformed or cyclic dependency graphs, a partial SQLite write, an unsafe migration or rollback, and legacy data overwritten by a retry. The controls below prevent silent state mutation and malformed registry entries but do **not** authenticate a Human or make an untrusted local operator safe. OS/database access control and manual receipt verification remain external governance gates.

## 3. Manifest and CLI contract

The UTF-8 JSON file is a single task object with exactly these fields; unknown fields fail closed. Version `1` is the only accepted manifest version. Example values are **synthetic and not an instruction to register them**:

```json
{
  "manifest_version": 1,
  "task_id": "SYNTH-REG-001",
  "title": "Synthetic registration fixture",
  "priority": 5,
  "dependencies": [],
  "authorization_ref": "https://github.com/nshaokiet/ai-ip-description-generator/issues/126#issuecomment-6247423831",
  "frozen_until_epoch_ms": null
}
```

The example URL illustrates *syntax only*: the linked comment authorizes this specification, **not** registration of the synthetic fixture or any implementation task. Tests must use synthetic fixture receipts and must never treat this URL as real task approval.

| Field | Proposed validation / meaning |
| --- | --- |
| `manifest_version` | JSON integer exactly `1`; no coercion. |
| `task_id` | Exact case-sensitive ASCII ID matching `^[A-Z0-9-]{3,50}$`; no implicit mapping, uppercasing or aliasing. |
| `title` | Nonempty UTF-8 string after trimming; 1–200 Unicode code points; reject leading/trailing whitespace and control characters. No implicit normalization. |
| `priority` | JSON safe integer `0..100`; priority affects scheduling only, never authorization. |
| `dependencies` | Array of 0–50 distinct exact valid task IDs; each must already exist and not equal `task_id`; stored/compared as a set in sorted ID order. No implicit task creation. |
| `authorization_ref` | Nonempty, <=2048-character exact HTTPS URL to a specific comment on an issue or PR in this repository (`#issuecomment-N` or `#discussion_rN`); no credentials, query string, fragmentless issue URL or arbitrary host. Syntax is checked locally; source/authority is checked **manually**, not by CLI. |
| `frozen_until_epoch_ms` | Required key with `null` or nonnegative safe integer Unix milliseconds. A freeze delays eligibility only; it is not approval. |

CLI accepts exactly one absolute manifest path and no positional overrides. It reads a regular file of at most 64 KiB, rejects parse failure/duplicate JSON keys/unknown keys, and never prints manifest contents, credentials or the full receipt URL on errors. The URL parser must require host `github.com`, no userinfo or nondefault port, the exact repository/issue-or-PR path and one permitted comment fragment; encoded path/host tricks fail closed. Output is a minimal outcome (`CREATED` or `ALREADY_REGISTERED`) with task ID and status only; failures use a nonzero exit code and a stable sanitized error category. No partial success is reported. The implementation must use parameterized SQL and must not follow an untrusted manifest path from an MCP request. CLI/package path conventions remain those in the [MCP README](../../tools/project-orchestrator-mcp/README.md).

## 4. Identity, idempotency and dependency invariants

`tasks.id` remains the unique registry key. Define the **canonical manifest** as the validated values above, with `dependencies` sorted lexically; `registered_at` and an optional operator label are audit metadata and excluded from equality. A retry is idempotent only when the existing task has an immutable registration record with **exactly equal canonical manifest bytes** and its current title, priority, freeze value and dependency-edge set still match that record. It returns `ALREADY_REGISTERED` without changing any task column, dependency, provenance, lease, checkpoint or timestamp—even if the task subsequently left `PLANNED`. Drift in those static fields is a corruption/conflict error, not an occasion to repair history. Approval, status and lease fields may legitimately have changed and are not part of manifest equality. Any same-ID mismatch, or an existing legacy/seed task with no registration record, returns `REGISTRATION_CONFLICT` without mutation. No retroactive provenance is inferred. No overwrite/upsert/`INSERT OR IGNORE` is allowed in this path.

For a new ID, every dependency must exist at commit time. Reject self-reference, duplicates and any cycle reachable from the proposed task; if the reachable existing graph is already cyclic or otherwise corrupt, fail closed rather than adding an edge. No dependency may be a newly auto-created task. The final graph check and insertion must use the same write transaction so another writer cannot invalidate the preflight. Registration makes no claim that a dependency is authorized or completed; existing claim eligibility checks still decide that later. A registration manifest may not select V2 or reuse an ID already enrolled in V2.

## 5. Persistence, migration, concurrency and recovery

Propose **additive schema v4**: a `task_registrations` table keyed by `task_id` (foreign key to `tasks.id`) holding manifest version, canonical manifest JSON, receipt reference and creation time; database constraints and update/delete-rejection triggers make the provenance row immutable through supported operations. Existing v1–v3 `tasks`, `dependencies`, `progress`, `checkpoints`, V2 evidence and budget structures are not rewritten. Existing seeded and historical tasks have **no** registration row; this is legitimate legacy-nullable provenance, not missing data to synthesize. Migration must validate expected columns/objects, reject future or malformed schemas, and be idempotent. It must not rewrite `approval_ref`, status or any history.

Within one `BEGIN IMMEDIATE` transaction: validate the existing row/registration conflict or idempotent retry; validate dependency presence and reachable graph; insert the `PLANNED` task with null owner/branch/worktree/lease/blockers/approval; insert sorted dependency edges; insert immutable provenance; commit. Any validation, constraint or busy failure rolls back everything. A second process contending for the same ID waits under the existing bounded SQLite `busy_timeout`, then observes the committed record: same manifest returns `ALREADY_REGISTERED`, different manifest returns `REGISTRATION_CONFLICT`; timeout returns a retryable, non-mutating error. Never claim two `CREATED` outcomes. A concurrent database migration or schema-version mismatch must fail closed.

Before any future active-DB rollout, an authorized operator must stop all MCP/CLI writers, identify the exact `PROJECT_ORCH_DB` path (the README documents the home-directory default), make a **consistent SQLite backup** using a verified SQLite backup API or clean shutdown/checkpoint procedure, record backup location/hash/schema version, and test restoration on a disposable copy. Dry-run migration from representative v3 and fresh databases in isolated paths; compare pre/post row counts, legacy task/status/approval/lease/checkpoint/budget values and foreign-key/integrity checks. Only after separate implementation/rollout approval may a supervised active migration occur. If migration fails, preserve the original and logs, stop writers and restore the verified backup offline; do not drop v4 tables or run an older binary against a v4 database (the current future-version guard should reject it). Prefer a reviewed forward fix if active writes have occurred since backup. Backup/restore is a planned procedure, **not performed by this specification task**.

## 6. Lifecycle and failure behavior

- A newly registered task is visible by exact-ID lookup as `PLANNED`; an unknown ID still returns the existing explicit `Unknown task: <id>` without creating a row.
- Registration leaves `approval_ref`, owner, branch, worktree, lease, progress, checkpoint and V2 workflow records absent/null. Only the existing separately authorized `approveTask` may set `APPROVED`; it currently checks for a nonempty reference, not authenticated Human identity ([`store.ts`](../../tools/project-orchestrator-mcp/src/store.ts), 160–169).
- `claim`, `active`, `checkpoint`, `stopAndHandoff` and transitions retain their current owner/lease/status/evidence protections ([`store.ts`](../../tools/project-orchestrator-mcp/src/store.ts), 172–315). Registration must not call or bypass them. It does not fix unrelated MCP completion limitations.
- A lookup on active V1 state may recover expired leases before returning ([`store.ts`](../../tools/project-orchestrator-mcp/src/store.ts), 121–126). Future registration diagnostics should use a disposable database or a genuinely read-only inspection route; do not label `get_state` a pure read against active data.

## 7. Acceptance criteria and planned tests (future implementation only)

| AC | Measurable requirement | Planned test / file |
| --- | --- | --- |
| AC-01 | Valid new V1 manifest creates exactly one `PLANNED` row; exact `project.get_state` resolves it, with null approval/owner/lease. | `test/store.test.ts` temp DB plus `test/mcp.test.ts` stdio lookup. |
| AC-02 | Genuinely unknown exact ID returns explicit `Unknown task` and changes no row or provenance. | `test/store.test.ts` and stdio negative lookup. |
| AC-03 | Same canonical manifest, including dependency-order permutation, can be retried after lifecycle movement/restart and returns `ALREADY_REGISTERED` with no changed records/timestamps. | `test/store.test.ts` snapshot comparison. |
| AC-04 | Same ID with different title, priority, dependency, freeze or receipt, and existing seed/legacy ID without provenance, returns conflict with zero mutation. | `test/store.test.ts` conflict matrix. |
| AC-05 | Registered task, dependency edges and provenance survive Store/server restart; schema migration is restart-idempotent. | `test/store.test.ts`, `test/schema-v2.test.ts` or new `test/registration-schema.test.ts`, stdio test. |
| AC-06 | Bad JSON/keys/types/path, missing/duplicate/self/cyclic dependencies and constraint failure are rejected atomically; no partial task/dependency/provenance. | New `test/registration-admin.test.ts` plus Store and migration tests on temp DB. |
| AC-07 | Registration alone cannot approve, claim, transition, checkpoint or complete; receipt string is not asserted as authenticated authority. | `test/store.test.ts` negative lifecycle tests; admin output assertion. |
| AC-08 | Existing wrong-owner, expired-lease, branch/worktree and checkpoint/handoff guards remain enforced for registered tasks. | `test/store.test.ts` lease/owner regression matrix. |
| AC-09 | Two independent processes on one temp DB produce one `CREATED` and one idempotent or conflict outcome; lock timeout leaves valid state. | New registration worker/process test following `test/claim-worker.ts`/`test/migration-worker.ts` patterns. |
| AC-10 | v3 and fresh DB migration preserves all legacy records; malicious receipt/path/SQL-like strings fail safely; MCP tool list gains no registration tool, V2 records/activation unchanged. | Migration fixture/integrity snapshots, admin negative tests, `test/mcp.test.ts` tool-list comparison, V2 regression suite. |

All planned tests use synthetic records and disposable databases; no active database, real research document or paid provider is needed. AC passage must be established by an independently reviewed implementation and actual CI, not this specification.

## 8. Future authorized implementation scope and review gate

Expected implementation changes, **only after separate Human freeze and implementation authorization**: `tools/project-orchestrator-mcp/src/store.ts` (atomic registration), `src/admin.ts` (CLI), `src/migrations.ts` (additive v4 and validation), possibly a small manifest parser/type module, focused `test/store.test.ts`, `test/mcp.test.ts`, migration/admin/concurrency tests or workers, and the MCP `README.md` (operator/backup runbook). No `server.ts` registration tool, product code, `AGENTS.md`, Render configuration, V2 activation or historical backfill is in scope. If review identifies a security/governance change beyond this contract, return to Human rather than silently expanding implementation.

Recommended sequence: (1) independent fixed-SHA review of this spec; (2) Human decision to freeze/accept and separately authorize implementation; (3) isolated branch and disposable-DB migration/registration implementation; (4) AC-01–AC-10 plus full MCP regression suite; (5) exact-SHA independent read-only implementation review, CI and ordinary V1 gates; (6) separately authorized rollout/backup/active migration if ever needed. This specification PR is **Draft and must not be merged under the present authorization**.

Reviewer handoff: Gemini 3.8 Flash High / Antigravity STRICT READ-ONLY should inspect this document at one exact final HEAD and the full `main...HEAD` diff; report actual model/profile, session identity and reuse disclosure, `PASS`/`REQUEST CHANGES`/`BLOCKED`, findings by severity, and AC-01–AC-10 coverage. Focus on recorded-vs-verified authorization, equality semantics after lifecycle changes, immutable provenance, reachable-cycle handling, SQLite writer races, legacy-nullable migration, backup/rollback and the absence of an MCP registration surface. A review invitation is not a review result.

## 9. Open risks and freeze decision

1. Procedural receipt verification can be mistaken for authenticated Human approval. Manual review and explicit CLI wording are required; stronger identity verification is outside this task.
2. An existing corrupt dependency graph or interrupted/out-of-date local SQLite deployment may make registration fail closed; the live installation has not been inspected. Implementation tests must cover this without altering active state.
3. Future active migration requires an operator-approved backup/restore window; no data-loss-free downgrade is promised after new writes.
4. This spec does not settle legacy/historical task reconciliation or the separate post-finish MCP completion limitation. Issue #123 stays closed; Issue #126 stays open until an authorized remedy is implemented, reviewed and verified.

**Freeze gate:** version 0.1.0 is proposed and frozen-ready, **not frozen or approved for implementation**. Record the independent report, exact reviewed SHA, CI and a separate Human freeze/implementation authorization before any code or database work. Any material post-review spec edit requires a new version and fixed-SHA re-review.

