# DEP-001-SR-20261024 — Proposed frontend security continuation

Version: 0.1.0. Date: 05/11/2026, Asia/Saigon. Planner: Codex.
Status: PROPOSED CONTINUATION OF EXISTING TASK; NOT IMPLEMENTATION APPROVED/FROZEN.
Existing task: [PR147 task record](https://github.com/nshaokiet/ai-ip-description-generator/blob/c50be576b39acd2eac9da096efd11060545463d1/docs/tasks/DEP-001-SR-20261024-security-remediation.md).
Registry/lease: UNVERIFIED (MCP unavailable). Proposed owner: Codex.
Foundation authorization covers this planning only. Breaking change: No runtime change here.

## Problem and result

PR147 head `c50be576b39acd2eac9da096efd11060545463d1`, base
`53c253be874236c6f38a5333a6f7f3390de9f51e`, fixes earlier Next/Zod findings.
The 05/11 fresh locked graph audit reports **8 MODERATE/full exit1; production0**.
Current CI executes plain full `npm audit` under fail-closed shell; therefore
these findings still block that step. Old zero-audit PASS is dated evidence only.

Result sought: a compatible reproducible frontend graph that passes the unchanged
full and production audit gates and preserves the existing lint adapter and web
behavior. Continue the existing PR/task rather than create a competing security PR.

## Scope, dependencies and authority

- Inspect current PR147 and the existing local Next16.4.5 candidate
  `efa1856ed50244eea0370e8112fced428ab152f6` first; it is not merged/reviewed by
  this foundation. A higher Next alone is not evidence of fixing nested minimatch.
- Proposed files: `frontend/package.json`, `frontend/package-lock.json`, existing
  security-task/audit evidence and README status. Map every changed package/node,
  range, advisory and compatibility constraint before selecting minimum fixes.
- Current chain: eslint-config-next → typescript-eslint → typescript-estree →
  nested minimatch10.2.6, affected globparts range `>=7.0.0 <11.0.1`,
  [GHSA-g3hv-75wg-m249](https://github.com/advisories/GHSA-g3hv-75wg-m249).
  Eight affected package nodes are not eight independently proven exploits.
  [Current evidence](../qa/resume-foundation-001-20261105.json) records every path.
- Legacy scope allowed a bounded set of changes; any expanded dependency/adapter
  or major-version migration needs explicit Human scope disposition before code.
  Do not add a new external package/service or upgrade tech stack by assumption.
- No PRODUCT/C1/C2 runtime changes, MCP dependency edits, CI weakening, auth,
  active DB rollout, deploy/settings, billing, provider or research data. MCP
  remediation is a separate dependency-security change with separate review.
- No dependency on A's external review to prepare this patch. Final hosted full
  acceptance may also depend on CI144 integration/QA snapshot availability;
  report that blocker rather than broaden this PR to installer/workflow changes.

## Measurable acceptance / validation

| AC | Requirement |
|---|---|
| S01 | Actual chosen base/head/tree and complete package changes recorded; unrelated local/root lockfile edits preserved. Refresh PR before continuation. |
| S02 | Clean isolated `npm ci` succeeds; lock bytes unchanged by repeated clean install, `npm ls --all` has no invalid graph; actual npm/node versions and package paths retained. |
| S03 | Fresh full and production audits on installed exact graph both exit0 with zero vulnerabilities under unchanged commands; save raw reports and SHA256. Lock-only planning audits cannot replace this check. |
| S04 | Existing lint-security suite73/73, lint, typecheck and normal build pass; scoped adapter retains integrity/equivalence checks. No suppressions, audit thresholds, `audit fix --force` or `continue-on-error`. |
| S05 | Existing browser suite (historical78), compatibility suite (historical77), applicable static export/provider-marker and demo tests actually run/pass under isolated test temp and backend config. Record actual counts, skips and prior failures; no number copied as fresh evidence. |
| S06 | Application behavior/source contracts unchanged; source review distinguishes dev tool glob path, installed affected range and runtime reachability. Severity retained independently of mitigation. |
| S07 | Fresh independent Gemini/Antigravity strict-read-only security/quality review on exact final SHA with actual model/profile/session/reuse, no unresolved blocker; required PR CI SUCCESS including mandatory artifacts, then authorized normal merge and exact-main verification. Old c50be PASS does not cover new head. |

Before a code change, resolve Human authorization for this continuation's exact
scope and any graph/compatibility plan. After code changes, test final graph once,
re-review final SHA, preserve all failed/skipped evidence. Revert by ordinary
reviewed revert if later accepted; do not force/reset shared history.

First action on resumption: read this spec and [PR147](https://github.com/nshaokiet/ai-ip-description-generator/pull/147),
refresh refs/dirty state, compare local efa1856 with c50be, and map the nested
minimatch chain against supported existing adapter constraints. This document
does not claim that scope extension or implementation is already approved.
