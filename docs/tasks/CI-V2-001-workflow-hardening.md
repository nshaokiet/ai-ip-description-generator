# CI-V2-001 — Workflow hardening

| Field | Value |
| --- | --- |
| Version / date / author | 1.0.0 / 2026-10-21 Asia/Saigon / Codex |
| Status | IMPLEMENTED CANDIDATE — DRAFT; independent review and complete CI pending |
| Authorization | Human attachment “TASK: AI-IP CI-V2 — GitHub Actions Optimization”, 2026-10-21; subsequent Human instruction requests handoff for external Gemini review |
| Workflow | V1, unenrolled; no V2 history created |
| Baseline | `7abc63e12e18a8027de1d4be4c71ad7aa182cb91` |
| Branch / PR | `ci/ci-v2-001-workflow-hardening` / [#144](https://github.com/nshaokiet/ai-ip-description-generator/pull/144) |
| Reviewer | Gemini 3.8 Flash High / Antigravity STRICT READ-ONLY; PENDING, no verdict claimed |
| Resume keyword | `RESUME-AIIP-CIV2-001-20261021` |

Version history: none → 1.0.0, 2026-10-21, Codex: record authorized minimal
upload hardening, regression guards and review handoff. Breaking change: **No**;
job names/status contracts, product, provider and governance authority unchanged.

## Failure and implementation

[C1 main run #39555439292 attempt 2](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/39555439292/attempts/2)
passed backend **1127/2 skipped** and MCP, then security artifact upload failed
with `Artifact storage quota has been hit`. Typecheck, build and browser steps
were skipped. A subsequent `failure()` condition also attempted optional QA upload.

All five archive steps now follow the final functional gate. A preceding
`always()` snapshot captures `job.status` before uploads. Optional archives use
that immutable failure output or the existing explicit manual QA input, with
`always()` so required security upload failure cannot suppress requested diagnostics.
An upload failure alone does not activate optional archives. A genuine earlier
functional/bootstrap failure can still select optional diagnostics.

Security evidence remains mandatory: `always()`, missing files error, unchanged
payload and two-day retention. Every upload failure remains blocking. All
functional commands, exact-head checkout, MCP isolation, provider-free flags,
permissions, triggers, fixed compatibility SHA and status names are preserved.
Normal successful runs select only security evidence; no new deletion or cleanup
policy is implemented. Cancellation is not success; the snapshot records only
failure, and the existing always-run security evidence requirement is retained.

## Verification and limitations

- Local Python 3.12.10: **25 passed**, comprising **23 hardening checks + 2 existing
  cleanup tests**. Covers archive ordering, retained gates, failure suppression,
  security evidence, optional selectors, exact-head/provider/status contracts,
  and actual snapshot Bash for success/failure/cancelled.
- Initial local invocation: **22 passed / 3 setup errors** due to existing shared
  pytest Temp directory ACL. A unique test-owned `--basetemp` resolved it; no ACL
  or production code change. Final command: `python -m pytest
  tests/test_ci_workflow_hardening.py tests/test_actions_artifact_prune.py -q
  -p no:cacheprovider --basetemp <unique-test-owned-directory>`.
- actionlint **1.7.12**, official Windows archive SHA256
  `6e7241b51e6817ea6a047693d8e6fed13b31819c9a0dd6c5a726e1592d22f6e9`:
  CI and unchanged cleanup YAML/expression validation **PASS**, exit 0;
  `-shellcheck= -pyflakes=` (those external analyzers unavailable).
- Existing js-yaml parsed comparison against baseline checks unchanged functional
  steps, upload payloads/retention, MCP job and non-step workflow configuration.
- [Predecessor run #39594108615](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/39594108615)
  on `d009db493fe47827656c5cc7474537c77220805c` **FAILED**: backend **1127 passed /
  2 skipped**, MCP SUCCESS; pinned Ubuntu snapshot returned HTTP **503**, followed
  by missing LibreOffice/Poppler packages (exit 100). Later functional steps were
  skipped due to that installation failure, before uploads. Security archive
  correctly failed for missing producer files; optional browser archive again
  reported quota exceeded. This is not fresh full-pipeline success or proof of
  quota recovery. No rerun requested. Final-head CI is tracked in the PR checkpoint.
- Source: [GitHub expression/status semantics](https://docs.github.com/en/actions/reference/workflows-and-actions/expressions).
  Static/shell checks do not simulate the hosted Actions runner or replace CI.
- MCP returned `Unknown task: CI-V2-001`: **BLOCKED BY TOOL CAPABILITY**;
  no registration, lease, approval or completion state invented.
- No available connected mechanism to invoke the specified Gemini environment
  was found. Human will obtain external review and return its original report.

## Acceptance evidence and review request

| AC | Candidate evidence / remaining gate |
| --- | --- |
| 01 | No archive before functional gates; ordering test PASS; hosted quota-failure execution still to verify |
| 02–03 | No suppression; required security upload/missing evidence still blocking |
| 04 | Four optional archives excluded by default after successful functional checks; bytes not freshly measured |
| 05–07 | Functional/security/MCP/provenance gates, provider flags and governance preserved; static comparison plus tests; full CI pending |
| 08 | Immutable final head published in PR checkpoint; fresh review must target that exact head |
| 09 | No paid AI, billing/deploy change, real/confidential research input or artifact deletion |
| 10 | Reviewed ordinary revert procedure below |

Gemini must inspect the **entire baseline-to-final-head diff**, run focused tests,
review `always()`/snapshot semantics for PR/push/manual/cancellation, verify no
upload-only diagnostic cascade or failure suppression, preserve security payload
and exact-SHA checks, and distinguish infrastructure blockers from acceptance.
Return original report with exact baseline/head, model/profile, actual session
identity/reuse, commands/results, AC verdicts, severity/findings, and confirmation
of no tracked writes/commit/push/merge. Review PASS alone does not permit merge.

## Rollback

If merged, create a dedicated revert branch from current main, revert the actual
CI-V2-001 merge using `git revert -m 1 <verified-merge-sha>`, inspect scope, run
validation and obtain required exact-head independent review/CI before normal
protected PR merge. Preserve history and all evidence. No reset/force push or
unreviewed pin changes. Revert restores the old upload ordering vulnerability;
record that limitation. Do not copy baseline over unrelated future changes.

## Handoff

```text
Task ID: CI-V2-001
Agent: Codex — IMPLEMENTER, Workflow V1
Reviewer: Gemini 3.8 Flash High / Antigravity STRICT READ-ONLY; PENDING
Status: IMPLEMENTED CANDIDATE / DRAFT; NOT MERGE ELIGIBLE
Version: 1.0.0; exact final Git SHA in PR #144 checkpoint
Work completed: Upload-tail hardening; regression tests; scoped status/task documentation.
Files affected: .github/workflows/ci.yml; tests/test_ci_workflow_hardening.py; docs/tasks/CI-V2-001-workflow-hardening.md; README.md; docs/operations/01_PROJECT_CONTROL_CENTER.md.
Evidence checked: Real main/PR/history/logs, local focused tests, actionlint and parsed workflow comparison.
Findings: Ubuntu snapshot HTTP 503 and artifact quota blocked predecessor full CI; final-head results external.
Decisions: Human-authorized CI-V2-001 implementation; CI-V2-002/003 planning kept on a separate branch; Human will return Gemini review.
Issues: Independent exact-head review, complete final-head CI and artifact quota recovery unverified; MCP task unknown.
Security impact: Mandatory security evidence and provider-free fail-closed gates preserved; no release/billing/data authority expanded.
Recommended next action: External Gemini exact-final-head review; inspect CI without retry loops; only then assess merge eligibility.
```
