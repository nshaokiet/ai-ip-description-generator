# P1-005 — Offline Performance Baseline

## Metadata

| Field | Value |
| --- | --- |
| Task | P1-005 |
| Status | **CLOSED / COMPLETED — MERGED; MCP TOOL LIMITATION** |
| Authorization | `HUMAN-P1-005-OFFLINE-PERFORMANCE-BASELINE-2026-10-01` |
| Baseline main | `a44d26d895724a254cb5e598047baaed32f7087d` |
| Branch | `feat/p1-005-offline-performance-baseline` |
| Executable implementation SHA | `e4db6b231bf99b3227f6a3e331479356cbcd869e` |
| Pull request | #48 — merged at `3641c7ed91636d8480226d931b719cdcf28b17e0` |
| PR CI | `36807093817` — **SUCCESS** on executable implementation SHA; final review-head CI `36808292952` — **SUCCESS** |
| Scope | Deterministic offline measurement only; no product-semantic optimization |
| Data | Synthetic and reproducible only |
| Independent review | Gemini 3.1 Pro High — **PASS**, findings **NONE**, reviewed `2c3e03ed8faf7bb929cfe38e7131108c6f57426b` |
| MCP | `PLANNED` / **BLOCKED BY TOOL CAPABILITY** |

## Purpose and boundaries

This task establishes a repeatable performance baseline for the existing local/synthetic MVP. It does not set a production service-level objective, prove semantic quality, authorize a provider call, or change prompt/schema/model/runtime policy. The harness removes `OPENAI_API_KEY`, forces both live-test flags to `0`, and blocks non-loopback browser traffic.

Existing limits remain authoritative: upload size is 10 MiB, PDF page count is 50, and OCR is unsupported. BLK-003 remains OPEN; EVAL-001 PRODUCT_RUNTIME remains DEFERRED — AWAITING FUNDING; P1-006 is separately authorized under `HUMAN-P1-006-UX-POLISH-2026-10-01`; DEPLOY-001 remains NOT AUTHORIZED.

## Developer command

After installing the pinned Python/frontend dependencies and building the frontend, run the complete backend plus local-browser baseline from the repository root:

```powershell
python tools/offline_benchmark.py --profile baseline --warmups 1 --samples 5 --output artifacts/p1-005-offline-baseline.json
```

The command writes schema-versioned JSON and prints a compact median/p95 summary. `--skip-browser` is intentionally labeled incomplete and is intended only for targeted backend diagnosis. `--profile ci --warmups 0 --samples 1 --skip-browser` provides a fast correctness smoke test.

## Workload matrix

| Stage | Workloads | Recorded metadata |
| --- | --- | --- |
| Upload/document validation | 1-page small PDF; 10-page medium PDF; 50-page PDF; 9,438,743-byte PDF near the 10 MiB limit | bytes, SHA-256, page count, configured limit |
| PDF parsing | 1, 10 and 50 text-layer pages | bytes, pages, parsed characters, source units |
| DOCX parsing | 10, 250 and 2,000 deterministic paragraphs | bytes, paragraphs, parsed characters, source units |
| Structured validation | Canonical representative Patent Draft JSON and schema v1.0.0 | serialized input bytes, top-level field count |
| DOCX render/export | Canonical representative draft and approved template | section count, output bytes |
| Offline backend E2E | validation → PDF parsing → structured validation → DOCX export | pages, parsed characters, source units, output bytes |
| Local browser workflow | upload → process with offline fakes → validate revision → DOCX download | input bytes, completed downloads, outbound network blocked |

Fixtures are generated before timing. PDF and DOCX bytes are deterministic; DOCX ZIP timestamps and permissions are fixed. Timed operations use `time.perf_counter_ns`. Each baseline case has one warm-up and five measured samples. Median uses the standard median; p95 uses the documented nearest-rank method.

## Baseline evidence

Machine-readable evidence: [`docs/performance/p1-005-offline-baseline.json`](../performance/p1-005-offline-baseline.json).

Environment: CPython 3.12.10, Windows 11 build 26200, Intel64 Family 6 Model 140, 8 logical CPUs. These measurements describe this machine only.

| Case | Median (ms) | p95 (ms) | Samples |
| --- | ---: | ---: | ---: |
| Upload + validation — small PDF | 6.136 | 7.072 | 5 |
| PDF parse — small | 1.003 | 1.868 | 5 |
| DOCX parse — small | 0.294 | 0.349 | 5 |
| Upload + validation — medium PDF | 46.116 | 49.184 | 5 |
| PDF parse — medium | 8.136 | 9.191 | 5 |
| DOCX parse — medium | 3.022 | 4.203 | 5 |
| Upload + validation — 50-page PDF | 163.916 | 167.831 | 5 |
| PDF parse — 50 pages | 38.446 | 40.354 | 5 |
| DOCX parse — 2,000 paragraphs | 26.192 | 39.575 | 5 |
| Upload + validation — near 10 MiB | 42.100 | 64.431 | 5 |
| Structured draft validation | 89.869 | 121.734 | 5 |
| DOCX render/export | 137.193 | 138.940 | 5 |
| Representative offline backend E2E | 245.610 | 252.828 | 5 |
| Local browser workflow | 1,087.810 | 1,108.514 | 5 |

## Regression policy

CI verifies benchmark correctness rather than local speed: deterministic fixtures, case execution, result schema, warm-up/sample accounting, statistics, configuration errors, JSON serialization, optional threshold evaluation, provider isolation, and exit codes. CI does not enforce absolute timing thresholds.

Optional local thresholds may be supplied with `--thresholds`. They are explicit environment-specific absolute ceilings and cause exit code `2` on breach. A threshold must not be promoted to shared CI until repeated evidence on a controlled runner supports a broad, stable ceiling. Cross-machine results must be compared only after checking environment metadata and workload hashes.

## Verification evidence

Local Windows evidence:

- Targeted benchmark tests: **12 passed**.
- Full offline backend: **442 passed / 3 skipped / 1 third-party deprecation warning**.
- Actual complete baseline: **SUCCESS**, 14 measured cases.
- `pip check`: **PASS**.
- Frontend lint / typecheck / build: **PASS / PASS / PASS**.
- Synthetic Playwright: **18 passed**.

PR CI `36807093817` on executable implementation `e4db6b231bf99b3227f6a3e331479356cbcd869e`:

- Backend: **443 passed / 2 skipped**.
- `pip check`: **PASS**.
- Frontend lint / typecheck / build: **PASS / PASS / PASS**.
- Playwright: **18 passed**.
- Live flags: **0 / 0**.
- Provider/API calls: **NONE**.

The local and CI counts are separate environment-specific evidence; neither is substituted for the other.

Implementation review and merge evidence:

- Final reviewed SHA: `2c3e03ed8faf7bb929cfe38e7131108c6f57426b`.
- Reviewer: **Gemini 3.1 Pro High**.
- Decision: **PASS**; findings **NONE**.
- Final review-head CI `36808292952`: **SUCCESS** with backend **443 passed / 2 skipped**, `pip check` **PASS**, frontend lint/typecheck/build **PASS**, Playwright **18 passed**, live flags **0 / 0**, provider/API calls **NONE**.
- PR #48 merged at `3641c7ed91636d8480226d931b719cdcf28b17e0`.
- Push/main CI `36809603707`: **SUCCESS** on the exact merge SHA with backend **443 passed / 2 skipped**, `pip check` **PASS**, frontend lint/typecheck/build **PASS**, Playwright **18 passed**, live flags **0 / 0**, provider/API calls **NONE**.
- Governance closeout reviewed SHA `2765dde0eaa99e9d8d9f989876d1310b1843424e`: Gemini 3.1 Pro High **PASS**, findings **NONE**, reviewer modified tracked files **NO**.
- Closeout PR #49 merged at `90ead2c0f26f17c617cfa71e6d7b3d16808d46e1`.
- Final push/main CI `36811043597`: **SUCCESS** on the exact merge SHA; dependency consistency, backend offline regression, frontend lint/typecheck/build and synthetic browser E2E all completed successfully.
- Git/governance status: **CLOSED / COMPLETED — MERGED; MCP TOOL LIMITATION**.
- MCP remains `PLANNED` / **BLOCKED BY TOOL CAPABILITY**; no MCP `IMPLEMENTED` or `COMPLETED` state is fabricated.

## Safety and handoff

- Provider/API calls: **NONE**.
- Live flags: **0 / 0**.
- Production/deployment/auth/storage/retention changes: **NONE**.
- Real/confidential/unpublished data: **NONE**.
- Claims changes: **NONE**.
- P1-005 has no remaining Git/review/CI gate.
- P1-006 is a separate Human-authorized task and does not alter the P1-005 performance-baseline contract.
