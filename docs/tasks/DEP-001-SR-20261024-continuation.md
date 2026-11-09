# DEP-001-SR-20261024 — Bounded frontend security continuation

Version: 0.1.1. Date: 05/11/2026, Asia/Saigon. Planner: Codex.
Status: LOCAL VALIDATION PASS; PR147 candidate4c30d37; independent review/required CI PENDING.
Existing task: [PR147 task record](https://github.com/nshaokiet/ai-ip-description-generator/blob/c50be576b39acd2eac9da096efd11060545463d1/docs/tasks/DEP-001-SR-20261024-security-remediation.md).
Registry/lease: UNVERIFIED (MCP unavailable). Proposed owner: Codex.
The original foundation instruction covers planning only. The later direct Human
reply approving option1 expressly authorizes the bounded trial below and its
checks/conditional PR147 update. No merge/deploy or broader migration approved.
Breaking change: No application/API/schema change approved by this document.

0.1.0→0.1.1,05/11/2026,Codex: refreshed audit/registry evidence and concrete
bounded remediation decision, followed by the explicit bounded Human approval
and isolated trial. Breaking change: No application/API/schema change.

## Current scope decision — bounded trial authorized

Human explicitly approved option1 in this resumption: a scoped override for the
typescript-estree8.70.1 branch to minimatch>=11.0.1 plus required transitives;
preserve Next/React, root ESLint, root minimatch3.1.5 and lint adapter behavior;
isolated worktree, graph/regression proof, all stated audit/build/browser checks,
stop on failure/out-of-scope breaking change, update147 only after relevant checks
pass, then actual final-SHA Gemini/Antigravity review. No merge/deploy/gate waiver.
Actual registry names are `brace-expansion`5.x and
`@isaacs/nonrecursive-glob-match`1.x; no unrelated similarly named package is added.
The initially pending-scope observation below remains chronological evidence;
the new explicit Human disposition resolves that specific authorization blocker.

Validation chronology: installed full/prod audits0, graph valid, unchanged security
73/73, lint/typecheck/build and browser78/78 passed. A new additional probe failed
at setup before matcher assertions (non-exported package.json subpath). Codex
paused and preserved logs. Human then expressly authorized exactly three resolve
changes to exported entry points, assertions unchanged, and continuation of the
remaining checks. Attempt2 passed2/2; this does not erase attempt1 or turn the
earlier73/78 results into probe evidence. Genuine dependency incompatibility or
out-of-scope change remains a stop condition. PR147 update waits for remaining
static/demo/reproducibility/fixed-source compatibility checks. These subsequently
passed: current browser78/demo8, fixed-source browser77/demo5, identical repeat
install graph/lock, all lint/typecheck/normal/static builds. The existing security
npm entry now executes unchanged73 first, new2 second under fail-closed&&, so
required CI also exercises the probe; workflow/thresholds unchanged.

After related checks passed, existing PR147 was normally fast-forwarded to
4c30d37d6ad73dede6ea8439fae897a86fffbdc0, treeb440f3021c39c9504cd49753dae63acfc1a3a0ed.
[Exact candidate evidence](https://github.com/nshaokiet/ai-ip-description-generator/blob/4c30d37d6ad73dede6ea8439fae897a86fffbdc0/docs/qa/dep-001-sr-20261105-minimatch.json)
and PR147 body provide the implementation handoff. Actual new independent review
and full hosted CI remain PENDING; no merge or deployment in this authorization.

At the 05/11 resumption, PR147 remains c50be576; a fresh pinned-lock audit confirms
eight MODERATE package nodes in one minimatch advisory chain, full exit1 and
production0/exit0. Installed baseline is minimatch10.2.6 under typescript-estree8.70.1,
whose manifest requires `^10.2.2`. Registry10.x versions end at10.2.6. Latest
typescript-estree8.72.1 still requires `^10.2.2`; merely refreshing compatible
parent versions cannot leave the affected range. No install or remediation PASS
is asserted by this metadata check.

The [primary advisory](https://github.com/advisories/GHSA-g3hv-75wg-m249) lists
affected `>=7.0.0 <11.0.1`, patched11.0.1. Registry11.0.1 requires
brace-expansion`^5.0.12` and **new transitive package**
`@isaacs/nonrecursive-glob-match` `^1.0.1`; Node24 satisfies its engine range.
These facts do not establish API/lint compatibility or installed-graph acceptance.

Initially, original DEP-001-SR scope permitted compatible manifests/lockfile remediation but
explicitly excludes a major migration; this continuation also reserves expanded
dependency/adapter scope for Human. AGENTS§19 therefore blocked the edit until the explicit disposition.
No override, package update, installation of the new dependency, or PR147 change
was performed before the disposition. The subsequent trial follows the new scope;
foundation documentation remains a separate PR.

**Bounded option expressly accepted by Human:** evaluate an exact scoped
override for `@typescript-eslint/typescript-estree@8.70.1` → minimatch11.x,
starting with minimum fixed11.0.1, and only its required transitive closure.
The proposed manifest addition is:

```json
{
  "overrides": {
    "@typescript-eslint/typescript-estree@8.70.1": { "minimatch": "11.0.1" }
  }
}
```

This fragment is additive to existing overrides; it is not a replacement manifest.
Keep root minimatch3.1.5, Next16.4.1, React, ESLint, pinned Next lint plugin16.3.8,
the local glob adapter, captured73-case lint contract, application/tests and CI
thresholds unchanged. No general override, suppression, `audit fix --force`,
MCP changes, adapter rewrite, provider or deployment. If the minimum fixed version
has another current finding, a later11.x patch may be evaluated within the same
explicitly authorized family; exact selected version/closure must be pinned and
recorded. Any required lint-contract change or other package/service expansion
stops this option and returns a separate decision.

Under the approval, evaluate in an isolated continuation checkout; require all S01–S07
below, including exact installed full/prod audits, unchanged73-case contract,
frontend/browser/demo/compatibility validation and new final-SHA independent review.
Retain failures and old c50be PASS as history. If the bounded trial is stopped,
leave PR147 unchanged/BLOCKED and continue authorized documentation only.

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
| S07 | Fresh independent Gemini/Antigravity strict-read-only security/quality review on exact final SHA with actual model/profile/session/reuse, no unresolved blocker; required PR CI SUCCESS including mandatory artifacts. Old c50be PASS does not cover new head. This trial stops at Draft PR/review/CI; no merge/deploy authority. |

The direct bounded Human approval above supplies this continuation's exact scope;
any further graph/compatibility expansion still needs disposition. Test the final graph,
re-review final SHA, preserve all failed/skipped evidence. Revert by ordinary
reviewed revert if later accepted; do not force/reset shared history.

First action on resumption: read this spec and [PR147](https://github.com/nshaokiet/ai-ip-description-generator/pull/147),
refresh refs/dirty state, compare local efa1856 with c50be, and map the nested
minimatch chain against supported existing adapter constraints. This document
does not approve scope beyond the explicit bounded trial above.
