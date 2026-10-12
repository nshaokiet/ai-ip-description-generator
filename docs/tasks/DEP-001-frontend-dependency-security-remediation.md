# DEP-001 — Frontend dependency security remediation

## Current DEP-001-A2 implementation checkpoint — ledger 1.1.0

2026-10-11, Codex, Workflow V1. **IMPLEMENTATION CANDIDATE / FRESH INDEPENDENT
SECURITY REVIEW PENDING**. Human explicitly approved “TASK: DEP-001-A2 — IMPLEMENT
CONTROLLED ESLINT SECURITY ADAPTER”; attachment SHA-256
`8059948bd2106830b6265ea39ecd292987422ff8c042cb9b1176ee665e0b0658`.
Approved research proposal 1.0.0 SHA-256
`986e71ab6422abe0b348513d6bac05d114a35eb5219a2c36d38804bc281ee6b4`.
These Human-provided local instruction references are not GitHub-native approvals.
Implementation starts at `9804e416beec2a975cc9ab51efba5e95c1719f4b`; main remains
`63d5a61235669ad7d32bb38d583789ea59ce5497`. Same branch and draft [PR #105](https://github.com/nshaokiet/ai-ip-description-generator/pull/105).

| Old | New | Date | Author | Reason | Breaking change |
| --- | --- | --- | --- | --- | --- |
| Ledger 1.0.0 | 1.1.0 | 2026-10-11 | Codex | Human-approved bounded local adapter, preserved lint configuration, complete security/regression evidence | Explicit tooling contract restriction; no product/API/schema change |

The private dev-only `@ai-ip/next-root-glob-adapter@1.0.0` replaces the module
slot consumed by the pinned Next lint plugin. Root devDependency **fast-glob**
resolves to `file:tools/next-root-glob-adapter`, with a version-scoped `$fast-glob`
override and `frontend/.npmrc` **install-links=true**. This small packaging
adjustment to the proposed private-name root key is necessary: the initial scoped
local-file link produced EUSAGE/ENOENT/dangling module resolution. The packed,
root-deduplicated adapter passed normal npm ci, actual CJS-to-ESM consumer loading,
full tree validation and a fresh source-copy installation. No install scripts or
manual installed-file patching. The lock transparently records the local identity;
do not mistake its module-directory name for official fast-glob.

Unchanged versions: Next/config/plugin 16.3.8, React/DOM 19.3.0, TypeScript 6.0.3,
ESLint 9.39.5, Playwright 1.63.0, sharp 0.35.5, source-map-js 1.2.2. Adapter uses
already present tinyglobby 0.2.17 → fdir 6.5.0 / picomatch 4.0.7; no unrelated
installed version changed. Actual braces, micromatch and fast-glob 3.3.1 code and
unused subgraph are absent. Next helper/rule hashes and the sole consumer are tested.

| Final local validation | Actual result |
| --- | --- |
| Full / production npm audit JSON | **0 vulnerabilities / 0 vulnerabilities**, exits 0/0; no suppression, filtering or risk exception |
| npm ci / npm ls --all | PASS; fresh source-copy lock unchanged and same contract tests pass |
| Adapter/lint-security | **73 PASS / 0 FAIL / 0 SKIP**; 25 original configs, 17 original negative fixtures, 22 relative + 21 absolute glob cases, 6 exact Next route-diagnostic cases and additional protections |
| Lint/typecheck/normal production builds | PASS for candidate and isolated UIUX-003 compatibility source |
| Original browser suite | **78 PASS / 0 FAIL / 0 SKIP / 0 FLAKY** |
| Isolated UIUX-003 source compatibility | **77 PASS**, comprising **52 UIUX-003 + 25 integration**; original source SHA `102b7e90dc3bfc1f79c197a20184f97b89070bf2` unchanged |
| Static exports / secret-marker checks | PASS for both candidate and compatibility copy |
| Synthetic static demo | **5 PASS + 5 PASS**, exits 0/0 |
| Offline Python | **903 PASS / 3 SKIP**, one existing Starlette deprecation warning, exit 0 |
| Development browser / native sharp synthetic SVG | PASS; HTTP 200, VI, two selects; sharp 0.35.5 / rsvg evidence recorded |
| Final exact-head Ubuntu CI | Must be independently verified after push; final SHA/run/artifacts in canonical PR handoff |
| Independent Gemini review | **PENDING** on entire new final SHA; no reused old PASS |

[Adapter contract and maintenance](../../frontend/tools/next-root-glob-adapter/README.md),
[immutable before inventory](../../frontend/tools/dep-001-lint-baseline.json),
[automated tests](../../frontend/tools/dep-001-lint-security.test.mjs).
The four existing evidence JSON files now have an **a2** section with raw audits,
installed graph, integrity/clean-install data and actual regressions; their original
fields remain historical evidence. Windows CRLF working bytes can differ from Git
LF blobs; reported local SHA-256 values explicitly refer to working bytes.

Glob limits are explicit: 4096 characters, depth 32, 64 operators, conservative
alternative product 256. Unsupported arrays/exclusions/options/ranges/nested
extglobs/escaped syntax fail clearly; Next itself handles root arrays and slash
normalization. Dynamic root order intentionally becomes deterministic. All path
values match captured fast-glob results; actual ordered Next diagnostics match
over literal, wildcard, recursive, brace and array roots. Independent review must
assess that difference. This is a bounded pinned-consumer adapter, not a full glob
API, universal regex-DoS guarantee or filesystem traversal resource guarantee.
Current application has no explicit next.rootDir. Official lint configuration,
all enabled/off rules, parser/globals/settings and ignore behavior are unchanged.

Initial failures are preserved in evidence: npm local-file resolution, one test
variable rejected by an existing lint rule, an aborted browser run with a harness
port mismatch, and initial demo 3 PASS/2 FAIL due to shared temporary-directory
permissions. Corrected only packaging/test execution context and the new test;
no product/backend edit, weakened assertion, ACL modification or security bypass.
Generated Next development agent files and temporary outputs are excluded.

First A2 CI [38135527214](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/38135527214)
at `e4d1af782b2f162236d017cfbaef66006ba84961` failed only at the private UIUX-003
source fetch (exit 128, could not read Username), because persist-credentials=false
correctly left no authentication for a later git fetch. Security/73 equivalence,
Python/pinned document QA and 78 browser gates had passed; compatibility/final demo
were not verified by that run. Remediation uses a separate exact-SHA official
checkout with the existing contents:read token and persist-credentials=false,
then verifies its HEAD. No credential persistence, permission expansion or source
change. Fresh complete CI is required for the new final candidate. Local source/
dependency/test code remains byte-identical, so no repeated local full suites are
needed for this CI-only correction.

CI now checks the literal PR head, full/prod audit/tree/73 lint-security tests,
existing Python/pinned document QA/browser/static/demo gates, and an isolated
fixed-source UIUX-003 compatibility archive. No PR #104 branch modification.
Fresh exact-SHA **Gemini 3.1 Pro High / Antigravity, STRICT READ-ONLY**, entire
candidate review is required. Human reports an external old partial PASS, but its
original report/session was not available here; no native approval is inferred.

Render YAML remains unchanged: both services declare checksPass; actual settings,
build Node and deployment event state remain unverified, a separate merge/deploy
blocker. ESLint 9 EOL is an existing maintenance limitation; a supported-major
migration is outside A2. MCP returns Unknown task: DEP-001-A2 — **BLOCKED BY TOOL
CAPABILITY**; no invented state/lease. Roll back with an ordinary A2 revert,
preserving earlier Next/sharp/source-map patches; this restores five HIGH entries
and BLOCKED status. No reset/force push, merge, deployment, closure, paid API,
real research, backend/API/Claims/product change, risk acceptance or next task.

Task ID: DEP-001-A2. Agent: Codex. Reviewer: Gemini 3.1 Pro High / Antigravity,
STRICT READ-ONLY, pending. Status: implementation candidate, independent review
pending. Version: ledger 1.1.0 / adapter 1.0.0. Work completed: controlled adapter,
tests, local security/regression evidence and CI gates. Files affected: precise
final inventory in PR handoff. Evidence checked: authorization, fixed baseline,
actual modules/audits/configs/tests/source hashes. Findings: bounded contract and
ordering for independent review; Render and ESLint maintenance limits. Decisions:
approved C2 implementation only. Issues: final CI verification and fresh external
review. Security impact: vulnerable npm graph removed, custom code still requires
independent assessment. Recommended next action: verify final CI and review one
fixed entire candidate; stop, keep both PRs unmerged.

## Historical partial-remediation checkpoint — original ledger 1.0.0 at 9804e416

The following original record is retained as history. Its five-HIGH/unresolved
wording describes the earlier candidate, not the current A2 dependency graph.

| Field | Evidence |
| --- | --- |
| Version / date | 1.0.0 / 2026-10-11 Asia/Saigon |
| Owner / implementer | Human Product Owner / Codex |
| Workflow | V1; no V2 enrollment |
| Authorization | Human attachment “TASK: DEP-001 — FRONTEND DEPENDENCY SECURITY REMEDIATION”, supplied in this conversation on 2026-10-11; OPTION A remediation before UIUX-003 merge |
| Baseline | `63d5a61235669ad7d32bb38d583789ea59ce5497`, freshly fetched main |
| Branch | `fix/dep-001-frontend-security-remediation` |
| Status | **BLOCKED — PARTIAL REMEDIATION; FULL SECURITY ACCEPTANCE NOT MET** |
| Independent reviewer | Gemini 3.1 Pro High / Antigravity — STRICT READ-ONLY; verdict PENDING |
| Immutable final SHA / PR / CI | Published and read back in the single DEP-001 PR handoff after commit; do not embed a future commit's own SHA in its tree |

Human authorizes existing dependency upgrades, manifest/lockfile, minimal frontend
compatibility fixes, synthetic testing, commit/push, one dedicated PR and independent
security-review handoff. **Merge, deployment, risk acceptance, new external service,
paid APIs, backend/Claims changes and unrelated refactoring are NOT authorized.**
PR #104 and its reviewed implementation `102b7e90dc3bfc1f79c197a20184f97b89070bf2`
remain untouched and unmerged.

| Old | New | Date | Author | Reason | Breaking change |
| --- | --- | --- | --- | --- | --- |
| None | 1.0.0 | 2026-10-11 | Codex | Authorized partial dependency remediation and explicit upstream blocker | No product/API/schema change; no major upgrade |

## Audit evidence and advisory reconciliation

Commands ran from this task worktree's `frontend`, Node **24.18.0**, npm **11.16.0**,
using the existing npm registry. Read-only audit/tree reports, exact exit codes and
capture times are preserved in [audit evidence](../qa/dep-001/audit-evidence.json),
[dependency tree and lockfile changes](../qa/dep-001/dependency-tree-evidence.json),
[current primary registry metadata](../qa/dep-001/registry-evidence.json) and
[local regression evidence](../qa/dep-001/local-regression-evidence.json).
These are actual outputs/summaries, not fabricated reviewer verdicts.

| Audit | Before | After | Exit before / after |
| --- | --- | --- | --- |
| `npm audit --json` | 8 HIGH package entries; 0 CRITICAL | **5 HIGH package entries; 0 CRITICAL** | 1 / 1 |
| `npm audit --omit=dev --json` | 3 HIGH package entries | **0 vulnerabilities** | 1 / 0 |
| Full audit remaining MODERATE / LOW entries | 0 / 0 (Next entry aggregates mixed severities) | 0 / 0 | See raw reports |
| Unique underlying advisories | **9 GHSA records: 4 HIGH / 4 MODERATE / 1 LOW** | **1 HIGH GHSA** | Count distinct object-valued `via[].url`, not propagated strings |
| Dependency tree | Valid, exit 0 | Valid, exit 0; actual patched overrides resolved | 0 / 0 |
| Clean install | Baseline `npm ci` succeeded, 348 installed | Regenerated lockfile `npm ci` succeeded, 348 installed | 0 / 0 |

Eight HIGH package entries were not eight distinct HIGH exploits. Six advisories
were grouped under Next (one HIGH, four MODERATE, one LOW), plus sharp, source-map-js
and braces. **Eight underlying advisory records are resolved by patched versions;
the braces advisory remains OPEN with five propagated HIGH package entries.**
A production-only clean audit does not satisfy the Human's full frontend audit target.

| Affected package / relationship | Before → after | Vulnerable range / patched release | Exposure and disposition |
| --- | --- | --- | --- |
| next, direct production dependency | 16.3.6 → **16.3.8** | Six GHSA rows below; all fixed for Next 16 at 16.3.8 | Server image/cache/metadata and dev MCP paths; patched, no exploitability exemption relied upon |
| sharp, optional transitive via next | 0.35.4 → **0.35.5** | <0.35.5 / 0.35.5 | Native image/SVG processing; exact patched override, upstream librsvg issue |
| source-map-js, transitive via next → postcss | 1.2.1 → **1.2.2** | >=1.0.0 <1.2.2 / 1.2.2 | Primarily build/source-map processing, included in production dependency graph; exact patched override |
| eslint-config-next, direct development dependency | 16.3.6 → **16.3.8** | Audit propagated range >=14.3.0-canary.0; no compatible release removing this chain identified | Aligned with Next patch; **HIGH unresolved** via plugin |
| @next/eslint-plugin-next, development transitive | 16.3.6 → **16.3.8** | Same propagated audit range; registry 16.3.8 and 16.4.0 both depend on fast-glob 3.3.1 | **HIGH unresolved**, development/lint globbing |
| fast-glob, development transitive | 3.3.1 → 3.3.1 | Audit propagated range *; latest 3.3.3 still uses micromatch ^4.0.8 | **HIGH unresolved** via micromatch; bumping it alone cannot resolve braces |
| micromatch, development transitive | 4.0.8 → 4.0.8 | Audit propagated range >=0.2.0; latest 4.0.8 requires braces ^3.0.3 | **HIGH unresolved** via braces |
| braces, development transitive | 3.0.3 → 3.0.3 | <=3.0.3 / **no patched release** | Recursive pattern parsing/compiling/expansion DoS; **HIGH OPEN** |

Runtime/development classifications describe actual dependency placement and
advisory paths, not full reachability certification. Glob/brace input is used by
the lint/tooling chain; no production-audit entry remains, but the development
security gate still applies.

### Underlying GHSA/CVE records

Primary advisory pages and registry metadata were read on 2026-10-11.

| GHSA / CVE | Baseline vulnerable range / severity | Patched version / current disposition |
| --- | --- | --- |
| [GHSA-3w37-wq28-93x7](https://github.com/advisories/GHSA-3w37-wq28-93x7), CVE-2026-94544 — Draft Mode cache leak | next >=16.3.0 <16.3.8 / MODERATE | 16.3.8 — resolved |
| [GHSA-4jqv-mc3x-m676](https://github.com/advisories/GHSA-4jqv-mc3x-m676), CVE-2026-94543 — self-hosted page cache poisoning | next >=16.0.0 <16.3.8 / MODERATE | 16.3.8 — resolved |
| [GHSA-39w2-rjm5-chcv](https://github.com/advisories/GHSA-39w2-rjm5-chcv), CVE-2026-94486 — dev MCP information disclosure | next >=16.0.0 <16.3.8 / LOW | 16.3.8 — resolved |
| [GHSA-f87g-xv8r-7p7x](https://github.com/advisories/GHSA-f87g-xv8r-7p7x), CVE-2026-94485 — metadata route information disclosure | next >=16.0.0 <16.3.8 / MODERATE | 16.3.8 — resolved |
| [GHSA-mcj8-r9mp-w47p](https://github.com/advisories/GHSA-mcj8-r9mp-w47p), CVE-2026-94484 — persistent page cache poisoning | next >=16.0.0 <16.3.8 / MODERATE | 16.3.8 — resolved |
| [GHSA-cjq9-62q9-8jv4](https://github.com/advisories/GHSA-cjq9-62q9-8jv4), CVE-2026-94483 — image optimization SSRF | next >=16.0.0 <16.3.8 / HIGH | 16.3.8 — resolved |
| [GHSA-wq5f-xc86-pv6w](https://github.com/advisories/GHSA-wq5f-xc86-pv6w), CVE-2026-96889 — librsvg memory vulnerability | sharp <0.35.5 / HIGH | 0.35.5 — resolved |
| [GHSA-68fv-2mgg-jv7q](https://github.com/advisories/GHSA-68fv-2mgg-jv7q), CVE-2026-93749 — indexed source-map DoS | source-map-js >=1.0.0 <1.2.2 / HIGH | 1.2.2 — resolved |
| [GHSA-vfj7-8cjw-p6xm](https://github.com/advisories/GHSA-vfj7-8cjw-p6xm), CVE-2026-93687 — nested brace pattern DoS | braces <=3.0.3 / HIGH | **None — OPEN / BLOCKING** |

## Minimal remediation and compatibility

- Patch-only Next / eslint-config-next 16.3.6→16.3.8; @next/env, plugin and
  platform SWC packages follow the matching patch.
- Pin existing transitive sharp 0.35.5 and source-map-js 1.2.2 through npm
  `overrides`. Both satisfy their existing upstream ^0.35.4 / ^1.2.1 ranges.
  This installs real patched releases; no audit entry is hidden or suppressed.
- Next 16.3.8 retains Node >=20.9 and React/React DOM ^19 support. Existing
  Node 24.18.0, React/React DOM 19.3.0, TypeScript 6.0.3, ESLint 9.39.5 and
  Playwright 1.63.0 remain pinned. No new package identity is added/removed;
  lockfile changes are existing package version/integrity metadata plus root pins.
- `npm ci` validates manifest/lock agreement and registry integrity. Lockfile
  SHA256: `6d24bbcb19920a0cf7320ec7701315409ff11bd02367de4204d2ea53354bd747`.
- Native Windows sharp smoke decoded a synthetic 16×16 SVG to a 107-byte PNG;
  loaded sharp reports **0.35.5 / librsvg 2.63.2**, matching upstream patched
  library guidance. Linux runtime security is not certified by this smoke.
- No frontend application code, test assertions, Next architecture, backend,
  Claims/schema/export contract or Render configuration changes.
- npm emits an existing ESLint 9.39.5 end-of-support warning and an existing
  unrs-resolver install-script approval warning. No global npm approval/security
  configuration was changed; no install-script bypass was used.

### Why the remaining chain is blocked

The primary braces advisory lists **no patched version**; registry latest is
still 3.0.3. Looking up 3.0.4 returned E404. Next ESLint plugin 16.4.0 still pins
fast-glob 3.3.1, so a Next minor upgrade would not solve it. npm proposes a major
eslint-config-next downgrade to 14.2.35 (`isSemVerMajor=true`), which is not an
authorized/validated safe compatible patch remediation. No force audit fix,
major downgrade, substitute glob package, removed lint guard, vendored fork or
audit suppression was applied.

**Security acceptance: NOT MET / BLOCKED**, under the Human target and AGENTS
§§8.2/11/19. No HIGH-risk exception is requested or accepted. Human may choose
to wait for an upstream patched release, or explicitly authorize a separately
specified and independently reviewed lint-chain replacement/vendor remediation
if it needs a new dependency or breaking compatibility change. Such work is not
started by this partial implementation. A future patched release can be selected
under authorized scope once real primary evidence exists.

## Functional regression evidence

The actual main baseline contains UIUX-002's System/Light/Dark implementation;
UIUX-003 fixed Light is still unmerged. This DEP-001 PR deliberately preserves
that baseline. To check the requested light-only future combination without
changing PR #104, a **test-only Git archive** of exact UIUX-003 SHA was extracted
under ignored `tmp/dep-001/uiux-003-compatibility/`, with only DEP-001's manifest
and lockfile copied into it. That source was built and tested separately. It is
not a merge, implementation commit, independent review or exact-head CI result.

| Check | Actual local result |
| --- | --- |
| Clean baseline and updated npm ci / target tree | PASS; audit failure statuses preserved separately |
| Lint / typecheck | PASS / PASS |
| Next 16.3.8 production build | PASS |
| Development compile/serve/browser smoke | PASS; HTTP 200, VI html language, title/logo/heading/native selects |
| Existing baseline browser suite | **78 PASS / 0 FAIL / 0 SKIP / 0 FLAKY**, runner exit 0 |
| UIUX-003 test-only combination production build | PASS |
| UIUX-003 compatibility suite | **52 PASS / 0 FAIL / 0 SKIP / 0 FLAKY**, runner exit 0 |
| Baseline static export + secret-marker scan | PASS; index/logo present; zero configured provider markers |
| Baseline static-demo suite | **5 PASS**, exit 0, 12.6s |
| UIUX-003 test-only combination static export / secret scan / demo | PASS / PASS / **5 PASS**, exit 0, 15.4s |
| Python regression | **903 PASS / 3 SKIP**, one existing upstream Starlette warning, 135.75s |
| Exact-head GitHub CI | Required; actual run/job/logs recorded in immutable PR handoff after push |

The 52 compatibility cases cover fixed-light first paint, saved legacy preferences,
OS changes, VI/EN at 390/768/1280/1440/1920, header/logo/SVG geometry, five steps,
storage failure, focus/contrast, review/edit/evidence, validation/export gating,
mobile and v1 DOCX. Baseline integration/demo cover real local HTTP PDF/DOCX
synthetic upload→process→review/edit→validate→export and retained safety restrictions.
These checks are regression evidence, not full visual/accessibility certification.

Windows config-managed server teardown stalled after all 78/52 case assertions
finished. Only task-owned loopback server PIDs/command lines were verified and
cleaned up; both runners subsequently emitted their final summaries and JSON
with **exit 0**, no flaky/skipped/failing tests. PowerShell Stop-Process initially
returned a null-reference runtime error; standard .NET cleanup succeeded after
fresh PID ownership checks. The unrelated IDE Playwright test-server was untouched.
No tool safety-status rejection occurred or was bypassed. Next dev generated
untracked agent/cache files in this isolated worktree; only those task-owned
generated files were removed. Logs and full browser JSON remain ignored locally.

### Reproduction

From task worktree/frontend, run:
```powershell
npm ci
npm audit --json
npm audit --omit=dev --json
npm ls next sharp source-map-js eslint-config-next @next/eslint-plugin-next fast-glob micromatch braces --all --json
npm run lint
npm run typecheck
npm run build
$env:PLAYWRIGHT_PYTHON='<repository>/.venv/Scripts/python.exe'
$env:PYTHONUTF8='1'
$env:PYTHONDONTWRITEBYTECODE='1'
npm run test:e2e
# After normal browser runner exits:
$env:RENDER_STATIC_EXPORT='1'
$env:NEXT_PUBLIC_DEMO_STAGING='1'
npm run build
npm run test:e2e:demo
# From repository root:
& '<repository>/.venv/Scripts/python.exe' -m pytest -q
```
Full audit currently returns 1 because the HIGH blocker is real. Do not convert
that exit status into a security PASS. Existing CI tests may succeed while this
separate mandatory audit gate remains unsatisfied. No CI checks were weakened.

## Deployment and governance boundaries

Both synthetic-demo services in unchanged `render.yaml` declare
`autoDeployTrigger: checksPass`. A successful future merge could therefore
trigger an unauthorized deployment. **Actual Render service settings are NOT
VERIFIED**, no Render service/configuration was changed, and no deployment was
performed. Repository YAML is not proof that live auto-deploy is disabled.
**Before any future merge, actual settings must be verified to prevent
unauthorized deployment; otherwise STOP.** This execution stops before merge.

MCP read: **Unknown task: DEP-001 — BLOCKED BY TOOL CAPABILITY**; no fabricated
registration/lease/state. Security reviewer must independently check advisories,
patched versions/overrides, lock integrity, compatibility/regressions, exact-head
CI, scope and this deployment gate. No reviewer PASS is fabricated or requested
despite the remaining HIGH advisory.

Draft-only outputs, authentic supported-Claims positive E2E unverified, real
figures/research unauthorized, Word pagination variation, full WCAG/assistive
technology/cross-browser certification unverified, paid provider and production
authorization absent remain unchanged. Do not merge DEP-001/UIUX-003, deploy or
start another task.
