# DEP-001-SR-20261024 — Minimal frontend security remediation

| Field | Value |
|---|---|
| Version / date / author | 1.0.0 / 24/10/2026 Asia/Saigon / Codex |
| Parent / task | AIIP-PR146-RECOVERY-20261024 / DEP-001-SR-20261024 |
| Status | LOCAL FIX VERIFIED; Draft PR / independent review / required CI pending |
| Workflow / reviewer | V1 / Gemini 3.8 Flash High, Antigravity STRICT READ-ONLY |
| Base | 53c253be874236c6f38a5333a6f7f3390de9f51e |
| Branch | security/dep-001-audit-remediation-20261024 |
| Authority | Actual Human attachment 36124a99-71b0-4dc9-ab03-07ada1f7c37d/Pasted text.txt |
| Authorization SHA-256 | 199b5e35ad72cd180c433205460e9cb33e8837a5173048f1eb2a676b3a658dd6 |
| Scope | Necessary manifests/lockfile, dependency-specific tests if needed, narrowly related docs; separate Draft PR |
| Budget / implementation boundary | USD 0; no C1/C2 application implementation, C2 fixture approval or deployment |

Human expressly authorizes diagnosis and compatible remediation through
`DEP-001-SR-20261024`, without repeated routine confirmations. The actual
instruction says “Do NOT include dependency fixes in PR #146” and “Do not merge
until all governance gates are satisfied.” This record is provenance for that
received instruction, not a proposed approval, authenticated signature or
independent reviewer verdict.

None → **1.0.0**, 24/10/2026, Codex: record minimal compatible security patch and
observed regression evidence. Breaking change: **No**; same Next major,
unchanged application/API/schema, lint contract and deployment policy.

## Confirmed findings

Raw before/after reports and command outcomes are in
[security evidence](../qa/dep-001-sr-20261024.json). Node **24.18.0**, npm
**11.16.0**, npm lockfile v3 and `install-links=true` match the current CI policy.

Baseline full audit exits **1**: two package entries, maximum severities one
CRITICAL and one HIGH. These aggregate **four underlying advisories**, not two
distinct exploits. Production audit exits **1**, contains Next only.

| Installed / relation | Advisory / CVE | Severity | Affected / minimum fixed |
|---|---|---|---|
| next 16.3.8, direct production | [GHSA-2464-fhr4-w9xw](https://github.com/vercel/next.js/security/advisories/GHSA-2464-fhr4-w9xw); advisory has no assigned CVE, references upstream CVE-2026-96889 | CRITICAL | Next16 >=16.0.0 <=16.4.0 / 16.4.1 |
| next 16.3.8, direct production | [GHSA-p3m5-59mp-jv5r](https://github.com/advisories/GHSA-p3m5-59mp-jv5r), CVE-2026-94482 | HIGH | Next16 >=16.0.0 <=16.4.0 / 16.4.1 |
| next 16.3.8, direct production | [GHSA-673q-mjm6-r5xr](https://github.com/vercel/next.js/security/advisories/GHSA-673q-mjm6-r5xr); no assigned CVE shown | CRITICAL | Next16 >=16.0.0 <=16.4.0 / 16.4.1 |
| zod 4.6.5, transitive development | [GHSA-mrhx-c7xc-m3w5](https://github.com/advisories/GHSA-mrhx-c7xc-m3w5), CVE-2023-54404 | HIGH | <4.6.6 / 4.6.6 |

Zod path: root dev `eslint-config-next16.3.8` →
`eslint-plugin-react-hooks7.1.1` → `zod`; `zod-validation-error4.0.2` also
uses it as a peer. `npm explain zod` and the installed graph confirm the path.

**CONFIRMED:** package versions, graph placement, audit membership, published
ranges and patched releases. **NOT_VERIFIED:** complete production reachability
or exploitability. Source uses `next/image`; static export has
`images.unoptimized=true`, and existing sharp0.35.5 matches the upstream image
workaround. No `use server`, `use cache` or cacheComponents setting was found in
the inspected app/config. These observations are not an exemption or proof of
non-exploitability. Zod exposure is development/lint-time by graph placement.

## Minimal decision and exact change

[Next16.4.1 release](https://github.com/vercel/next.js/releases/tag/v16.4.1)
publishes fixes for the three Next advisories. npm metadata confirms its Node/
React peer requirements accept the existing runtime and React19.3.0.

| Option | Result |
|---|---|
| Compatible direct upgrade | **Selected:** next16.3.8 → exact16.4.1, minimum published fixed release |
| Compatible transitive update | **Selected:** zod4.6.5 → exact4.6.6 in lock; satisfies existing ^3.25.0 or ^4.0.0 |
| New override or resolution | Unnecessary; no new override, suppression or replacement package |
| Major migration / force audit fix | Unnecessary and not authorized; not used |
| Hold without a patch | Appropriate only if compatibility or required gates fail; no risk acceptance |

Only runtime `next` changes in package.json. Its matching env/eight platform SWC
packages follow in the lockfile; Zod's existing entry uses the actual npm4.6.6
tarball/integrity. Exactly **11 existing package versions** change, with no package
identity additions/removals or unrelated version churn.

`eslint-config-next` and its plugin deliberately stay16.3.8: neither is an
affected entry, metadata has no peer constraint tying them to the runtime Next
minor, and updating them would change the previously captured lint adapter
contract. The valid installed tree and all **73 unchanged security/equivalence
tests** verify that choice. React/DOM, TypeScript, ESLint, Playwright, sharp,
source-map-js and existing scoped local-glob override remain unchanged.

Install/update commands use `--ignore-scripts`; the only lock package declaring
an install script is unrs-resolver, and it was not executed. Registry integrity
and optional prebuilt packages were installed normally. No global npm/security
policy, audit gate, lint rule, test assertion or workflow is changed.

## Actual validation

| Check | Result |
|---|---|
| npm ci --ignore-scripts | Exit0; authoritative candidate lockfile accepted |
| Full npm audit --json | Exit0; **0 vulnerabilities** |
| Production npm audit --omit=dev --json | Exit0; **0 vulnerabilities** |
| npm ls --all / npm explain zod | Exit0 / exit0; valid dependency graph |
| Repeated clean-install reproducibility | Exit0; lock SHA-256 unchanged, complete installed graph equal |
| npm run test:lint-security | **73 PASS / 0 FAIL / 0 SKIP**, exit0 |
| npm run lint / typecheck | Exit0 / exit0 |
| npm run build | Exit0, Next16.4.1 normal production build |
| Existing full browser suite | **78 PASS / 0 FAIL / 0 SKIP / 0 FLAKY**, exit0 |
| Render static build / selected secret-marker scan | Exit0 / exit0; expected index/logo present |
| Existing static demo E2E | **8 PASS**, exit0, task-owned TEMP/TMP |
| New C2 integration/fixture tests | **NOT RUN / NOT AUTHORIZED** |
| Local full Python suite / fixed-source UIUX compatibility | **NOT RUN**; no backend/source change; hosted existing gates remain mandatory |
| Required exact-head hosted CI / independent Gemini | **PENDING**, no success claimed in advance |

The first browser attempt was aborted after evidence showed the build's default
8000 proxy target differed from the isolated18146 backend. Rebuilding with
`BACKEND_URL=http://127.0.0.1:18146` yielded the completed78-case pass without
source/assertion changes. First demo attempt was **6 PASS / 2 FAIL** due to shared
temp upload `PermissionError`; a task-owned TEMP/TMP produced8PASS. Both initial
logs and corrected results remain in the external checkpoint. No ACL change,
test weakening or out-of-scope product fix was made. Server cleanup targeted
only verified task-owned processes.

## CI, review and deployment gates

PR146 remains OPEN/DRAFT, unchanged `29daeb208f7736a448297f699e674192c124c7da`
with exactly eight specification/governance paths. Its new actual fixed-SHA Gemini
report is **PENDING**; advisory standalone PASS is not substituted. Its own
CI40078806412 remains FAILURE. This separate patch does not clear its existing
checks or authorize moving its protected review head.

PR144's upload-tail proposal is still unmerged. Main still requires security
audit/evidence and downstream functional checks. Storage remains independently
blocked: the latest PR146 run reports quota and empty artifacts after the prior
successful cleanup. Account/billing-period usage is not exposed by the available
connector; recovery is NOT_VERIFIED. No cleanup, billing change, workflow edit or
speculative rerun is performed.

Render live settings are **NOT_VERIFIED**: the connected tool has no selected
workspace and explicitly requires Human confirmation before selecting one.
Historical OFF settings and repository YAML do not replace a fresh live check.
No Render configuration or deployment is performed. This remains a merge gate.

The security PR needs its own genuine independent Gemini3.8FlashHigh /
Antigravity STRICT READ-ONLY PASS on exact final SHA, actual required CI SUCCESS,
resolved blockers, fresh branch/head/base/scope/platform checks, confirmed safe
Render settings, expected-head protected ordinary merge and verified main CI/
ancestry/tree before closeout. No merge, completion or next-task approval is
inferred from these local passes. MCP returned Unknown task for this task; no
registration, lease or state is fabricated.

Rollback requires an ordinary reviewed revert of an eventual accepted merge,
preserving history; it would restore the vulnerable audited graph and cannot be
treated as a security-success state.

## Handoff

```text
Task ID: DEP-001-SR-20261024 / AIIP-PR146-RECOVERY-20261024
Agent: Codex — security remediation implementation/integration owner
Reviewer: Gemini 3.8 Flash High / Antigravity STRICT READ-ONLY — final-SHA review pending
Status: LOCAL FIX VERIFIED — Draft PR candidate; required hosted CI/review and merge pending
Version: 1.0.0; Next16.4.1/Zod4.6.6
Work completed: Identified four advisories, compared compatible options, applied two-package security fix with matching Next platform packages, verified audits/tree/73 security/78 browser/8 demo and builds
Files affected: frontend/package.json; frontend/package-lock.json; this task record; docs/qa/dep-001-sr-20261024.json; scoped README Project status row
Evidence checked: Actual Human attachment hash; fresh PR146/main/PR144; raw npm reports and metadata; installed dependency path; actual commands/exits; source/lock diff
Findings: Local security graph now zero vulnerabilities; hosted storage and independent reviews remain external blockers; initial test environment failures preserved
Decisions: Compatible minimum patched releases, no major migration or added override; preserve PR146 and all application/CI/C2 boundaries
Issues: Required hosted CI and Gemini pending; Render workspace not selected; MCP Unknown task / BLOCKED BY TOOL CAPABILITY
Security impact: Vulnerable dependency versions updated; no audit suppression or product/security-policy weakening; no paid provider, research data or deployment
Recommended next action: Review the published exact final security SHA, inspect its required hosted CI, preserve all gates and resume from external checkpoint RESUME-AIIP-146
```
