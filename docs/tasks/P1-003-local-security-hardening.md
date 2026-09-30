# P1-003 — Local Security Hardening

| Field | Value |
|---|---|
| Version | 0.2.1 |
| Status | **COMPLETED WITH MCP TOOL LIMITATION** |
| Owner | Codex |
| Baseline | `cbe0e9520ff3e0162e8917052c153cfe58829c4a` |
| Human authorization | `HUMAN-P1-003-LOCAL-SECURITY-HARDENING-2026-09-29` |
| Branch | `feat/p1-003-local-security-hardening` |
| Independent reviewer | Gemini 3.1 Pro High |

Version 0.2.1 (30/09/2026): close the Git/governance lifecycle after Gemini 3.1 Pro High PASS/findings NONE on exact closeout SHA `4ccb9ba5cb4f088f3568f182fe5eb03b381d4a05`, PR #43 merge, and successful final main CI; preserve MCP `IMPLEMENTED` and the explicit `BLOCKED BY TOOL CAPABILITY` limitation.

Version 0.2.0 (30/09/2026): record exact-SHA independent implementation review, PR #42 merge, successful push/main CI, and documentation-only governance closeout handoff. The implementation is merged; final governance review/merge and MCP completion remain pending.

Version 0.1.1 (30/09/2026): record the bounded remediations, seven deterministic security regression tests, and final green local verification matrix; merge and completion remain blocked on exact-SHA PR CI, fixed-SHA independent review, merge, main CI, and governance closeout.

Version 0.1.0 (30/09/2026): register the authorized local/synthetic scope, pre-implementation attack-surface review, evidence-backed findings matrix, and verification plan.

## Scope and boundaries

Harden the local/synthetic application at existing upload, archive, path, temporary-storage, error, HTTP, and frontend boundaries. This task does not authorize production authentication, tenant isolation, production/private storage, a production retention policy, deployment, provider calls, paid services, prompt/schema/model/runtime changes, real or confidential data, or Claims.

Project classification remains **MVP COMPLETE — LOCAL/SYNTHETIC**. EVAL-001 PRODUCT_RUNTIME remains **DEFERRED — AWAITING FUNDING** and BLK-003 remains **OPEN**.

## Threat areas reviewed

- Extension, MIME, signature, size, page-count, corruption, encryption, macro, embedded-object, external-relationship, and archive-expansion controls.
- Filename normalization across traversal, absolute-path-like, separator, Windows, control-character, and Unicode cases.
- Opaque local storage IDs, exclusive file creation, restrictive-permission assumptions, leases, expiry sweeps, and export cleanup.
- API exception mapping, log content, multipart parsing, request validation, and client-visible path/trace leakage.
- Frontend rendering of filenames and backend error text, download naming, and local response headers.

## Pre-implementation findings matrix

| ID | Area | Risk | Evidence | Severity | Current protection | Required remediation | Test needed |
|---|---|---|---|---|---|---|---|
| SEC-P1-003-01 | DOCX archive validation | A ZIP may contain duplicate or case-colliding member names, making the OOXML part selected by a reader ambiguous. | `_validate_zip_limits` checks count, paths, sizes, expansion and compression ratio but does not reject duplicate normalized member names; required parts are later read by name. | MEDIUM | Traversal, macro, embedded object, external relationship, DTD/entity and compression controls already reject known unsafe packages. | Reject duplicate normalized member names, including case-insensitive collisions, before any required OOXML part is parsed. | Upload packages with exact duplicate and case-colliding required parts; require a safe `unsafe_docx_package` response and no retained file. |
| SEC-P1-003-02 | Temporary upload cleanup | The TTL sweep may delete an unrelated expired regular file merely because its name has 32 characters. | `sweep_expired` accepts any regular file whose name length is 32; `path_for` applies the stricter lowercase-hex identifier rule only outside the sweep. | LOW | Storage root is dedicated, local, resolved, mode-restricted where supported; generated IDs are opaque UUID4 hex and active leases block deletion. | Apply the same opaque-ID validation in cleanup and skip symlinks/non-files. | Prove an expired 32-character non-ID sentinel and symlink are preserved while a valid expired opaque file is removed. |
| SEC-P1-003-03 | Local HTTP responses | Local pages/API responses can be cached, MIME-sniffed, framed, or send referrer data without explicit defensive policy. | FastAPI only emits `X-Correlation-ID`; Next config only declares a backend rewrite. | LOW | React escapes displayed values; API errors are normalized; exports use a constant attachment filename. | Add narrow local `no-store`, `nosniff`, `no-referrer`, frame-deny and capability-deny headers without HSTS or production claims. | Assert headers on normal and rejected backend responses and on the local frontend document response. |
| SEC-P1-003-04 | Filename/path handling | Platform-style absolute paths, mixed separators and unusual Unicode could regress into storage-path control or unsafe display metadata. | Current sanitizer uses normalized basename plus an ASCII allowlist, and storage always writes to an opaque ID, but coverage only proves `../../` traversal. | LOW | Filename is display metadata only; destination is generated with exclusive creation under the resolved root. | Preserve current behavior; add distinct boundary regressions rather than broaden normalization speculatively. | Prove Windows/UNC/mixed-separator and Unicode names normalize safely and never determine the stored path. |
| SEC-P1-003-05 | Multipart/error boundary | Malformed multipart input could expose parser details, paths or a traceback if exception mapping regresses. | Route catches Starlette HTTP parsing errors and global handlers return generic envelopes, but no malformed-multipart regression exists. | LOW | Generic HTTP/API/unexpected error handlers and correlation IDs; logs omit payload and filename. | Preserve current mapping; add deterministic malformed-boundary coverage. | Send malformed multipart bytes and assert a bounded generic error with no trace/path/payload reflection. |
| SEC-P1-003-06 | Frontend untrusted text rendering | A backend-controlled error string could become script/HTML if rendering changes away from React text nodes. | Current components interpolate error messages and filenames through JSX; no `dangerouslySetInnerHTML` or direct DOM HTML assignment is present. | NOTE | React text escaping and generic fallback for non-JSON errors. | No product-code change; lock the property with a browser regression. | Inject an HTML-shaped API error, assert literal text is shown, and assert no injected element/script executes. |
| SEC-P1-003-07 | Production controls | Local controls do not provide production authentication, tenant isolation, private storage, or a production retention/deletion policy. | These controls remain explicitly absent from the approved local architecture and current project status. | NOTE | Local-only/synthetic classification; no production authorization. | **OUT OF P1-003 SCOPE / BLK-003-related.** Do not implement or claim production readiness. | None in this task. |

## Verification gates

- Targeted deterministic security regressions for every applicable finding.
- Full offline pytest suite and `pip check`.
- Frontend lint, typecheck, production build, and synthetic Playwright suite.
- Live flags remain `RUN_OPENAI_LIVE_TESTS=0` and `RUN_OPENAI_DRAFT_LIVE_TESTS=0`; provider/API calls remain **NONE**.
- Draft PR CI succeeds on the exact implementation SHA before the fixed-SHA Gemini 3.1 Pro High review package is handed off.

## Implemented remediations

- `SEC-P1-003-01`: DOCX validation now rejects exact duplicate and case-colliding normalized ZIP member names before parsing required OOXML parts.
- `SEC-P1-003-02`: expiry cleanup now uses the canonical lowercase-hex opaque-ID rule and skips symlinks and non-files; path construction no longer resolves a final symlink component.
- `SEC-P1-003-03`: FastAPI responses and local Next.js pages now emit `Cache-Control: no-store`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: no-referrer`, `X-Frame-Options: DENY`, and a narrow `Permissions-Policy`.
- `SEC-P1-003-04` through `SEC-P1-003-06`: existing safe filename, multipart/error-envelope, and React text-rendering behavior is preserved and locked by distinct regressions.
- `SEC-P1-003-07`: production authentication, tenant isolation, private production storage, and production retention/deletion policy remain **OUT OF P1-003 SCOPE / BLK-003-related** and unimplemented.

## Local implementation evidence

- Security regression test methods added: **7** — duplicate/case-colliding DOCX members; Windows/UNC/mixed-separator and Unicode filenames; cleanup isolation; malformed multipart; backend headers; frontend headers; frontend untrusted-error text rendering.
- Targeted affected backend suites: **51 passed / 1 skipped / 1 warning**.
- Full offline backend: **418 passed / 3 skipped / 1 warning**.
- Python dependency consistency: `pip check` **PASS**.
- Frontend lint: **PASS**.
- Frontend typecheck: **PASS**.
- Frontend production build: **PASS**.
- Synthetic Playwright: **17 passed**. The known Windows server-teardown wait ended after stopping only the two identified test-owned listeners; the runner then exited successfully.
- Stability/cleanup oracle: PDF **3/3** and DOCX **3/3**, with zero source/export files after every run.
- Live flags: `RUN_OPENAI_LIVE_TESTS=0`, `RUN_OPENAI_DRAFT_LIVE_TESTS=0`.
- Provider/API calls: **NONE**; paid services: **NONE**; real/confidential data: **NONE**.
- At the implementation handoff, README P1-003 remained **Incomplete — Planned**; this is historical local evidence. The post-merge governance branch updates the canonical status summary.

## Implementation merge and main CI evidence

- Authorization: `HUMAN-P1-003-LOCAL-SECURITY-HARDENING-2026-09-29`.
- Implementation PR [#42](https://github.com/nshaokiet/ai-ip-description-generator/pull/42) reviewed head: `44ee7dcc2d459d97446a52f86bbc839c4036caf5`; baseline: `cbe0e9520ff3e0162e8917052c153cfe58829c4a`. No later implementation-changing commit was present at merge gate.
- Human-supplied independent reviewer/result: **Gemini 3.1 Pro High — PASS**, findings **NONE**, on that exact reviewed SHA. The separate reviewer report/date was not supplied with this closeout instruction; this record does not claim a new review.
- PR CI [`36658496058`](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/36658496058): **SUCCESS** on the reviewed SHA. PR #42 merged normally at `3fa1519ee31f6d2b3d6ffc7dbdc39ff56462e966`; resulting `main` is that exact SHA.
- Push/main CI [`36659558740`](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/36659558740): **SUCCESS** on `3fa1519ee31f6d2b3d6ffc7dbdc39ff56462e966`. Linux backend **419 passed / 2 skipped** (no warning summary displayed); `pip check` **PASS**; frontend lint, typecheck and build **PASS**; synthetic Playwright **17 passed**.
- Live flags: `RUN_OPENAI_LIVE_TESTS=0`, `RUN_OPENAI_DRAFT_LIVE_TESTS=0`; provider/API calls **NONE**. No paid service or real/confidential data was used.
- The implementation resolves the bounded local findings `SEC-P1-003-01` through `SEC-P1-003-06`; `SEC-P1-003-07` remains an out-of-scope production boundary. BLK-003 **OPEN**. Production authentication, tenant isolation, private production storage, and production retention/deletion policy remain unimplemented; production deployment is **NOT APPROVED**.
- Governance closeout PR [#43](https://github.com/nshaokiet/ai-ip-description-generator/pull/43) received Human-supplied **Gemini 3.1 Pro High — PASS**, findings **NONE**, on exact reviewed SHA `4ccb9ba5cb4f088f3568f182fe5eb03b381d4a05`; exact-SHA PR CI `36679703167` was **SUCCESS**. PR #43 merged normally at `8bd677475c5791f1947319f9e084fe455d19b421`; final push/main CI [`36681005158`](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/36681005158) was **SUCCESS** on that exact SHA: backend **419 passed / 2 skipped** with no warning summary, `pip check` **PASS**, frontend lint/typecheck/build **PASS**, synthetic Playwright **17 passed**, live flags **0/0**, provider/API calls **NONE**.
- MCP checkpoint/transition remains **BLOCKED BY TOOL CAPABILITY** — MCP reports `IMPLEMENTED`, its checkpoint tool requires an active lease after `finish_task` removed that lease, and it offers no Codex-facing post-merge transition. Git evidence establishes P1-003 **COMPLETED WITH MCP TOOL LIMITATION**; no false MCP `COMPLETED` claim is made. BLK-003 remains **OPEN**, production remains **NOT APPROVED**, and P1-004 is **PLANNED / NOT AUTHORIZED**.
