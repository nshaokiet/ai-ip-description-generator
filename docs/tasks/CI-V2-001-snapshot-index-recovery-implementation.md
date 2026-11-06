# CI-V2-001 — bounded pinned snapshot index recovery

Version 1.0.1 · 2026-11-06 · Status: **DRAFT IMPLEMENTATION — no merge approval**

## Authority and original failure

Human explicitly approved the bounded snapshot installer recovery on a **separate Draft PR** after the [planning-only baseline](CI-V2-001-document-layout-installer-recovery-plan.md). Base `main`: `417708d9154d86226504e69cc6587a3ca0a78c09`.

Exact-main [postmerge CI #42177917762](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/42177917762), attempts 1 and 2, both FAILED at signed pinned Ubuntu snapshot HTTP 502/503: layout installer exit 100, mandatory DEP-001 security archive absent. Backend 1160 PASS / 2 SKIP, MCP SUCCESS. No postmerge CI or security PASS was inferred. Further blind retries are prohibited.

## Implementation and preserved gates

- Retain Ubuntu **24.04/amd64**, immutable snapshot `20261009T000000Z`, `signed-by=/usr/share/keyrings/ubuntu-archive-keyring.gpg`, three Ubuntu suites and all **six exact package revisions** from `p2_006_qa_environment.json`. Keep LibreOffice/Poppler version verification, fonts and signed metadata checks.
- Only the pinned APT index update is retried. Helper `p2_006_snapshot_index.py` uses isolated `sources.list` and **fresh lists per attempt**, `APT::Update::Error-Mode=any`, `Acquire::Retries=0`, 30s per-acquisition timeouts and explicit nonempty InRelease checks on all three suites.
- At most **three attempts total**, delays **2s, 5s**; retry only known HTTP **502/503** failures of those specific pinned snapshot InRelease URLs. APT exit 0 accompanied by failed-fetch warnings is not a success. Exhaustion and any other cause fail closed before install.
- Signature/Hash/404/unknown APT errors, incomplete indexes, wrong OS/architecture and unavailable pinned versions must fail hard. No live mirror/PPA fallback, snapshot refresh, pin drift, insecure apt or optional security evidence.
- **No change** to `.github/workflows/ci.yml`, workflow permissions, application source, provider behavior or mandatory `dep-001-security` evidence. Existing conflicting PR #144 remains separate.

## Validation and honest boundaries

Deterministic local unit tests of mocked APT (no network/root/package install): **20 PASS**, covering first success, 502/503 recovery, mixed errors, exhausted retries, returncode0 with partial indexes, missing indexes, 404/signature/hash errors, invalid snapshot, script invariants. `bash -n` and Python compile PASS. Shellcheck unavailable locally; **NOT RUN**. These local tests do **not** demonstrate real signed Ubuntu package availability, layout QA, CI or security audit.

Required acceptance on final immutable candidate: current-main-target `pull_request` CI SUCCESS with real pinned Ubuntu install, document layout/reference validation, backend/MCP/browser gates and a present, independently verified mandatory DEP-001 ZIP and audit evidence. Follow with actual Gemini 3.8 Flash High / Antigravity STRICT READ-ONLY exact-SHA independent review, applicable governance gates and a separate Human merge decision. If upstream remains down, status **BLOCKED**, not PASS.

No authorization for PR #152 merge/spec freeze, D01–D07, DOCX-B admission, B/C2 runtime, deployment, or paid providers.

Resume: `RESUME-AIIP-CIV2-001-SNAPSHOT-RECOVERY`.

## Autonomous diagnosis and minimal guard correction — 2026-11-06

Human CI-V2-001 PR154 AUTONOMOUS DIAGNOSIS & REMEDIATION authorizes in-scope defects/tests and one required CI run for a justified new candidate; it does not authorize changing pins/allowed retries/workflow or main. Original d4df289 CI42182826367 actually completed FAILURE: metadata/index acquisition succeeded on attempt1, then apt-get install failed at a pinned transitive LibreOffice package HTTP500, exit100. The mandatory security producer was not reached; browser/audit/layout/reference skips are not PASS. This differs from historical main42177917762attempts1/2 (index HTTP502/503). No retry of packageHTTP500 was introduced, and no CI retry loop was run.

Separate from that external failure, a deterministic probe reproduced an implementation fail-closed defect: rc0 and existing nonempty InRelease paths allowed success despite an explicit E/W partial/stale-index summary with no eligible fetch details. Two new regression cases failed before the fix;23other helper cases passed. The minimal success guard now rejects that summary unconditionally; only the already recognized pinned InReleaseHTTP502/503 can follow existing bounded retry logic. Three additional cases proveHTTP500 or package-poolHTTP502/503 stay ineligible. All original20tests/assertions are unchanged.

Fresh local validation:25helpertests +4existing package/runtime-environment tests PASS/0FAIL/ERROR/SKIP;2existing mocked artifact-maintenance tests also PASS. Bashsyntax and targetPython3.12in-memory compile PASS. These deterministic/mocked results are not actual Ubuntu installation, signed metadata proof, layout/reference QA or audit acceptance. Raw before-fix failures and subsequent results remain private; safe evidence is in the QA receipt. Final head/tree/new hosted outcome belong in post-commit PR handoff, not a self-referenced tree.

All six pins/snapshot/Ubuntu24.04amd64/source signatures/strictAPT flags/fresh-lists/max3indexattempts/backoff2s5s remain unchanged. Installer script, pin definition, runtime verifier, workflow and mandatory evidence contracts are unchanged from d4df289. The full PR stays within five original paths; this patch changes helper/test plus the two existing evidence documents only. If real package acquisition remains unavailable, report BLOCKED_INFRASTRUCTURE rather than extending retry policy or claiming review readiness. Actual independent Gemini3.8FlashHigh review is requested only after all required final-SHA hosted gates pass.

1.0.0→1.0.1,2026-11-06,Codex: fix reproduced partial-index-summary fail-open, preserve original assertions and record separate external packageHTTP500. Breaking change:No; no scope/gate/pin change. Keep Draft; no merge/deploy/B-C2runtime/D01-D07/DOCX-B/paidAPI/realresearch.
