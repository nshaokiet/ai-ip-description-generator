# PRODUCT-001A — fixed-SHA review reconciliation

Version: 0.1.0. Date: 2026-11-05 (Asia/Saigon). Author: Codex.
Status: evidence reconciliation recorded; original recovered report archival PENDING.
Authorization: Human task “PRODUCT-001A — Review Reconciliation and Product Continuation”
and follow-up confirming the external report. USD 0. No merge or deployment.
Breaking change: No — factual records and planning only.

## Reviewed candidate and verdict

- [PR #149](https://github.com/nshaokiet/ai-ip-description-generator/pull/149):
  OPEN / DRAFT, not merged; branch `feat/product-001a-offline-synthetic-20261104`.
- Reviewed implementation: `cf9097fda4688db08fd505e21fcbf3c0e53a9d5c`.
- Reviewed tree: `b75cf5d35bef555933dae6c42037b544525092e0`.
- Base: `53c253be874236c6f38a5333a6f7f3390de9f51e`.
- **Technical PASS — reviewer-reported external verdict, relayed/confirmed by Human.**
  Full hosted CI was reported BLOCKED; GitHub's actual run conclusion is FAILED.
  This record is implementer reconciliation, not another independent review.
- GitHub-native approvals: none observed. An external report does not require a
  PR comment to exist; absence of comments is not evidence against its existence.

## Original report and attribution — preserve separately from corrections

Human identifies the original upload as `Pasted text(20261104-151926).txt`,
previously provided to ChatGPT, and confirms recovery in Markdown.
Reported reviewer description: **"Independent Senior Application Security &
Systems QA Reviewer"**, **Strict Read-Only**, dated **2026-11-04**.
Human associates it with Gemini/Antigravity; the original report does not explicitly
identify an exact Gemini model/profile or session ID. Exact model/profile,
session identity, reuse disclosure and independently established provenance:
**NOT VERIFIED**. Do not substitute the standing reviewer default or infer a
verified identity.

The original full report bytes/body are not accessible in this execution.
Human states the recovered Markdown will be supplied locally. **Original-report
verbatim archival is PENDING**, not claimed complete. No report body, hash,
filename for the recovered Markdown, findings inventory or stronger identity is
fabricated. Preserve the recovered file verbatim, including inaccuracies, when
accessible; record its actual path and SHA-256 then. Preserve the original upload
too if available. This reconciliation and Human's summary are not replacements
for either original. Corrections below do not rewrite the reviewer text.

Local shell startup failed with `helper_unknown_error: setup refresh had errors`;
the Node file-access runtime also failed. GitHub connected tools supplied the
fixed-SHA source, PR and hosted CI evidence. Local worktree status, uncommitted
files and local attachments were not inspected or changed. MCP tools are unavailable:
**BLOCKED BY TOOL CAPABILITY**; no lease/state/approval transition is invented.

## Factual corrections and implementer dispositions

| Topic | Disposition | Evidence and corrected record |
| --- | --- | --- |
| C1 idle TTL reported as 900 seconds | ACCEPT factual correction | [C1 source at reviewed SHA](https://github.com/nshaokiet/ai-ip-description-generator/blob/cf9097fda4688db08fd505e21fcbf3c0e53a9d5c/backend/app/services/preapi_source_custody.py): `IDLE_SECONDS = 30 * 60`, therefore **1800 seconds**. Independent absolute lifetime is `2 * 60 * 60` = **7200 seconds**. Existing approved C1 policy also says 30 minutes / 2 hours. Reads do not refresh idle TTL. No runtime modification is needed to match incorrect review prose. |
| Dependency findings generalized to a lower severity | ACCEPT severity correction | Preserve each primary advisory's actual severity, affected range and dependency path. Reachability, a mitigation and inherited status are separate fields; none changes the advisory severity. See inventory below. |
| Technical PASS interpreted as merge/security/CI approval | REJECT that interpretation | Reviewer-reported functional verdict is separate from independently verified provenance, hosted CI and security acceptance. PR stays OPEN/DRAFT. No merge eligibility or completion asserted. |

## Hosted CI — actual GitHub evidence

[Run 41848393889, attempt 1](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/41848393889)
is `pull_request`, exact `head_sha=cf9097fda4688db08fd505e21fcbf3c0e53a9d5c`,
completed with **failure**. Run time: 2026-11-04 14:31:22–14:39:55 UTC.

| Check | Actual result |
| --- | --- |
| Backend regression, job 126637829943 | **1160 PASS / 2 SKIP**, 485.71 seconds; pip consistency PASS |
| MCP, job 126637829472 | **SUCCESS** |
| Install offline document layout QA tools | **FAILED**, exit 100 |
| Layout conversion and public reference measurements | **SKIPPED** |
| Frontend install/lint/typecheck/build | **SKIPPED** |
| Full/production dependency audit, tree and lint-security check | **SKIPPED** |
| Playwright/browser, isolated compatibility and static/demo checks | **SKIPPED** |
| Security evidence upload | **FAILED** because its producer never ran and the evidence directory was absent |
| Overall hosted CI | **FAILED**, not full CI success and not waived |

[Build job and logs](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/41848393889/job/126637829943)
show HTTP **503 Service Unavailable** from the signed snapshot
`https://snapshot.ubuntu.com/ubuntu/20261009T000000Z/` for `noble`,
`noble-updates` and `noble-security` InRelease files. APT treated missing indexes
as warnings, then installation could not locate the pinned LibreOffice/Poppler
packages. The log also contains an _apt permission warning; the observed repository
responses are still explicitly HTTP 503. Missing security upload output is a
downstream consequence, not a newly observed quota failure. Successful upload of
existing browser screenshots does not prove that skipped browser tests executed.

No new test run, manual dispatch or retry was performed for this reconciliation.
The existing local 33/22/19 test reports remain historical task evidence, not
newly executed results.

## Dependency advisory severity reconciliation

Source baseline is the reviewed SHA's
[package manifest](https://github.com/nshaokiet/ai-ip-description-generator/blob/cf9097fda4688db08fd505e21fcbf3c0e53a9d5c/frontend/package.json)
and
[lockfile](https://github.com/nshaokiet/ai-ip-description-generator/blob/cf9097fda4688db08fd505e21fcbf3c0e53a9d5c/frontend/package-lock.json).
Primary advisories were read 2026-11-05. This is a targeted source/range
reconciliation, **not a fresh npm audit or exhaustive vulnerability inventory**.
Earlier DEP-001 zero-audit reports are dated history and do not certify this SHA.

| Advisory | Primary severity | Reviewed graph / disposition |
| --- | --- | --- |
| [GHSA-673q-mjm6-r5xr](https://github.com/vercel/next.js/security/advisories/GHSA-673q-mjm6-r5xr), typed-array use-cache RCE | **CRITICAL** | next 16.3.8 is inside affected >=16.0.0 <=16.4.0. Runtime exploitability requires specified Cache Components/use-cache behavior; not demonstrated here. OPEN; no waiver. |
| [GHSA-p3m5-59mp-jv5r](https://github.com/vercel/next.js/security/advisories/GHSA-p3m5-59mp-jv5r), Server Actions DoS | **HIGH** | next 16.3.8 is in the affected range. Server Action reachability is separate and unverified. OPEN; no waiver. |
| [GHSA-2464-fhr4-w9xw](https://github.com/vercel/next.js/security/advisories/GHSA-2464-fhr4-w9xw), SVG image optimization RCE | **CRITICAL** | next range includes 16.3.8. The manifest/lock pin sharp 0.35.5, which meets the vendor's documented workaround. Preserve CRITICAL severity; mitigation is source-evidenced, actual installed graph/runtime not freshly checked. No blanket security acceptance. |
| [GHSA-g3hv-75wg-m249](https://github.com/advisories/GHSA-g3hv-75wg-m249), globparts amplification | **MODERATE** | nested eslint-config-next → typescript-eslint → minimatch 10.2.6 is inside >=7.0.0 <11.0.1. Development graph; optimization/input reachability unverified. OPEN. Root minimatch 3.1.5 is a different path. |

Older minimatch HIGH advisories retain HIGH in history:
[GHSA-7r86-cg39-jmmj](https://github.com/advisories/GHSA-7r86-cg39-jmmj),
[GHSA-23c5-xmqv-rm74](https://github.com/advisories/GHSA-23c5-xmqv-rm74),
[GHSA-3ppc-4f35-3m26](https://github.com/advisories/GHSA-3ppc-4f35-3m26).
The reviewed lock's minimatch 3.1.5/10.2.6 lie beyond those particular vulnerable
ranges. Do not reclassify those advisories as MODERATE or claim they are the
currently applicable globparts advisory. Any additional finding in the recovered
original must be mapped by ID/range/path; its exact severity is not guessed.
No dependency, audit threshold, suppression, risk acceptance or runtime was changed.

## Separate minimal CI infrastructure investigation

The narrow candidate targets only `tests/backend/install_p2_006_qa.sh`.
It is a **proposal, not an applied or tested fix**:

1. Add `-o Acquire::Retries=3` to the existing isolated APT options, so failed
   metadata and package downloads have a finite retry allowance.
2. Run update with `--error-on=any`, so incomplete snapshot indexes fail before
   package installation. Keep fail-closed shell behavior.
3. Keep the existing snapshot date, exact package revisions, archive signature/
   hash checks, isolated source list, postinstall version verifier and workflow
   check coverage. No live-mirror fallback, signature bypass or continue-on-error.
4. Validate separately: shell syntax; transient-503 recovery and persistent-503
   fail-closed behavior, including proof install is not invoked after failed
   update; existing package/runtime mismatch verifier; one real Ubuntu 24.04
   pinned install/QA validation when the service is available.
5. Only after a reviewed infrastructure candidate, use one deliberate hosted
   validation. Do not loop whole workflows or rerun unchanged product tests merely
   to investigate the endpoint. Persistent outage remains a blocker. A successful
   infrastructure test would not retroactively change run 41848393889 or skipped
   frontend/security/browser results.

Supported by Ubuntu's [APT retry documentation](https://manpages.ubuntu.com/manpages/noble/man5/apt.conf.5.html)
and [strict update error option](https://manpages.ubuntu.com/manpages/noble/man8/apt-get.8.html).
No workflow rewrite, runner/platform change, billing change or hosted retry is
performed. Infrastructure/security remediation belongs in separate reviewable
changes, not a runtime change solely to satisfy reviewer prose.

## Blockers and product continuation

No PRODUCT-001A runtime defect has been established by this factual
reconciliation. That is not a new independent functional/security PASS.
Accepted closeout remains blocked by FAILED required CI, unresolved inherited
security acceptance, NOT VERIFIED reviewer provenance and pending verbatim report
archival. Full C2 pilot/admitted fixture governance and arbitrary-paper semantic
extraction remain unimplemented boundaries, not newly discovered A runtime bugs.

[PRODUCT-001B proposed scope](PRODUCT-001B-trusted-local-review-presenter.md)
is preparatory planning. Initial recommendation is a **trusted same-process
terminal presenter**, avoiding a new browser authorization architecture. Reuse A's
custody/extraction/USPTO pipeline. Its implementation is not started or approved
by the existence of this proposal.

## Handoff

Task ID: PRODUCT-001A — review reconciliation / PRODUCT-001B planning
Agent: Codex — implementer reconciliation and planning
Reviewer: External Human-confirmed report; exact model/profile/session NOT VERIFIED
Status: Reconciliation checkpoint; original report archival pending; PR #149 OPEN/DRAFT
Version: 0.1.0
Work completed: Fixed-SHA source/CI reconciliation, severity mapping, narrow CI remedy proposal, provisional B scope
Files affected: Reconciliation note, B scope, README, Control Center and append-oriented Review Log
Evidence checked: Exact PR/head/tree, hosted run/jobs/logs, C1 code/policy, product adapter/tests, lockfile and primary advisories
Findings: 1800-second idle TTL; CRITICAL/HIGH severities retained; hosted CI FAILED; original body unavailable
Decisions: Preserve external attribution and original inaccuracies separately; no runtime change, retry, merge or deployment
Issues: Original Markdown archival and verified reviewer provenance pending; required CI/security gates unresolved
Security impact: No new transport; internal authority stays private; advisory severity is not suppressed
Recommended next action: Archive recovered original verbatim; separately validate narrow installer remedy; review B scope before implementation
