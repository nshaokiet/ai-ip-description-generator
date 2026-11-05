# DEP-001-SR-20261024 — Scoped minimatch continuation

Version: 1.0.0. Date: 05/11/2026, Asia/Saigon. Implementer: Codex.
Status: LOCAL VALIDATION PASS; fixed-SHA independent review / required CI pending.
Workflow: V1. MCP registration/lease UNVERIFIED; tools unavailable, no state invented.
Base: PR147 `c50be576b39acd2eac9da096efd11060545463d1`, tree
`7dfcba0f5356c5eaf12aa0c3af6e9c650b0b5504`; main remains53c253be.
Authority: direct Human option1 approval and subsequent explicit three-resolve
probe-setup correction approval in RESUME-FOUNDATION-001-WEB,05/11/2026.
No merge/deploy/provider/gate waiver or broader runtime/migration authorization.

None→1.0.0,05/11/2026,Codex: record bounded dependency remediation and separately
attributed checks after Human scope disposition. Breaking change: No application,
API/schema/template or existing lint behavior change; the transitive major
override itself is explicitly Human-authorized and tested below.

## Problem, scope and exact change

PR147's original Next/Zod patches remain intact. A fresh baseline locked-graph
audit on c50be reports8MODERATE/full exit1, production0/exit0. Eight affected
package nodes share the nested minimatch advisory chain; they are not eight
demonstrated exploits. The [primary advisory](https://github.com/advisories/GHSA-g3hv-75wg-m249)
marks `>=7.0.0 <11.0.1` affected. The actual consumer, typescript-estree8.70.1,
requires `^10.2.2`, and even registry8.72.1 retains that range. A compatible
refresh within10.x cannot fix this advisory. Original scope excluded this major
expansion; Codex stopped that edit until the new explicit Human approval.

The added npm override is scoped only to
`@typescript-eslint/typescript-estree@8.70.1` → exact minimatch11.0.1.
The actual lock delta against c50be is exactly:

| Node | Before | After |
|---|---|---|
| eslint-config-next/node_modules/typescript-eslint/node_modules/minimatch | 10.2.6 | 11.0.1 |
| @isaacs/nonrecursive-glob-match | absent | 1.0.3 |

The minimatch manifest raises brace-expansion to`^5.0.12`; the installed locked
brace-expansion already satisfies it and does not change. No similarly named
unrelated package is added. npm resolves the required closure normally; no
hand-edited package bytes, generalized override, suppression or force audit fix.

Next16.4.1, React/DOM19.3.0, root ESLint9.39.5, root minimatch3.1.5, pinned Next
lint plugin16.3.8, typescript-eslint8.70.1, existing adapter/baseline/73 tests and
all application/runtime/CI sources are unchanged. Public new graph evidence is
[the scoped evidence record](../qa/dep-001-sr-20261105-minimatch.json). Original
October task/evidence/review stay historical; their old PASS is not this candidate.

## Compatibility, testing and failure chronology

Node24.18.0/npm11.16.0; existing Python3.12.10 supplies only synthetic test servers.
Task-owned temp/log locations and loopback-only test ports isolate other work.
Original log bytes are preserved privately; public records contain safe summaries,
hashes and commands, never personal paths or raw internal reviews.

- Clean `npm ci --ignore-scripts`, actual installed full/prod audits0/exit0,
  `npm ls --all` and `npm explain minimatch` exit0. Scope includes actual installed
  graph, not only a locked-graph planning audit. Second clean install/graph check
  verifies lock-byte and complete graph reproducibility.
- Existing security/equivalence suite73/73, lint/typecheck/normal build and current
  browser78/78 completed successfully. These outcomes retain their own scope.
- New `frontend/tools/dep-001-minimatch-compat.test.mjs` resolves the **actual
  estree consumer**, checks dot-aware/default-project allowlist matching and runs
  representative optimizationLevel2 preprocessing in a bounded child process.
  This bounded stress smoke is not proof against every malicious glob.
  The existing `test:lint-security` command runs the original73 first, then the
  new2 via fail-closed `&&`, so the unchanged required CI security entry executes
  both. No original assertion/config/baseline or workflow is weakened or replaced.
- Initial new-probe attempt failed before matcher assertions because Codex used
  a package.json subpath that eslint-config-next does not export. Codex stopped
  the trial and preserved failure logs. Human explicitly approved exactly three
  resolves to exported entry points, unchanged assertions, and remaining checks.
  Attempt2 passed2/2. The73/78 prior passes never substitute for this probe.
- Static build/demo and the existing fixed-source compatibility path are recorded
  independently in evidence. Fixed source102b7e9 is an isolated checkout with
  candidate manifest/lock/tools only, mirroring the current CI procedure. Do not
  add counts from different source SHAs into one claimed suite.
  Actual results: current browser78/current demo8; fixed-source browser77/demo5;
  zero unexpected/flaky/skipped browser cases. Both static builds and selected
  marker checks pass; repeat clean install has identical complete graph and lock.

Only necessary frontend graph/probe and related status/evidence files belong to
this PR. No backend suite rerun or live model/semantic/production acceptance is
claimed. Selected static marker scans are not a comprehensive security audit.

## Review and remaining gates

After all related checks pass, preserve the final commit/tree and full file list
in PR147's fixed-SHA handoff. A genuinely independent Gemini/Antigravity strict
read-only review must cover the full candidate, actual model/profile/session and
reuse disclosure, graph/override compatibility, unchanged73-case contract,
failure disposition and privacy. No tracked reviewer writes or self-PASS.
Required hosted CI must actually succeed with mandatory evidence; a failed gate
remains blocking regardless of local results. No merge or deployment in this task.

Foundation PR151 is preferred by the latest Human instruction; PR150 overlap is
documented there without closing or overwriting another agent's work. The product
remains the existing Next.js/FastAPI website and four USPTO v2 draft artifacts.
This dependency task adds no browser product feature, auth policy or pipeline.

Task ID: DEP-001-SR-20261024
Agent: Codex — scoped implementer, V1
Reviewer: Gemini/Antigravity independent strict read-only; actual new report PENDING
Status: Local validation PASS; fixed-SHA independent review / required CI pending
Version: 1.0.0
Work completed: Scoped minimatch override/closure, compatibility probes and related checks
Files affected: Frontend manifest/lock/new probe, this task record, public evidence and README task row
Evidence checked: Current PR147/base, primary advisory, npm graph/registry, actual local logs and fixed-source tests
Findings: Baseline8MODERATE; initial probe setup failure preserved separately
Decisions: Human authorized bounded major/transitives and exactly three setup resolves; no broader scope
Issues: Actual independent final-SHA review, required hosted CI and task acceptance remain pending
Security impact: Dev dependency graph only; no auth/data/provider/CI/deployment change
Recommended next action: Inspect final validation record, review exact final SHA, inspect hosted checks; do not merge/deploy
