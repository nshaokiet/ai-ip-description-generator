# CI-V2-001 — bounded pinned snapshot index recovery

Version 1.0.0 · 2026-11-06 · Status: **DRAFT IMPLEMENTATION — no merge approval**

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

Deterministic local unit tests of mocked APT (no network/root/package install): **19 PASS**, covering first success, 502/503 recovery, mixed errors, exhausted retries, returncode0 with partial indexes, missing indexes, 404/signature/hash errors, invalid snapshot, script invariants. `bash -n` and Python compile PASS. Shellcheck unavailable locally; **NOT RUN**. These local tests do **not** demonstrate real signed Ubuntu package availability, layout QA, CI or security audit.

Required acceptance on final immutable candidate: current-main-target `pull_request` CI SUCCESS with real pinned Ubuntu install, document layout/reference validation, backend/MCP/browser gates and a present, independently verified mandatory DEP-001 ZIP and audit evidence. Follow with actual Gemini 3.8 Flash High / Antigravity STRICT READ-ONLY exact-SHA independent review, applicable governance gates and a separate Human merge decision. If upstream remains down, status **BLOCKED**, not PASS.

No authorization for PR #152 merge/spec freeze, D01–D07, DOCX-B admission, B/C2 runtime, deployment, or paid providers.

Resume: `RESUME-AIIP-CIV2-001-SNAPSHOT-RECOVERY`.
