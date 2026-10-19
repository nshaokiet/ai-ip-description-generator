# PREAPI-001-A/B — Postmerge governance receipt (candidate)

| Field | Value |
|---|---|
| Version | 0.1.0 — factual review candidate |
| Date | 19/10/2026 |
| Workflow | V1; separate docs PR review and merge pending |
| Baseline | `cdc879adedbb1c5d1945d2e5722d61df4959aebb` |
| Scope | Git/CI/Render facts only; no runtime authorization |

## PREAPI-001-A

The frozen specification [v0.1.3](../tasks/PREAPI-001-zero-cost-readiness.md) was merged by [PR #132](https://github.com/nshaokiet/ai-ip-description-generator/pull/132): reviewed head `898e7417316409bae23752bbc385ec7384f042bd`, merge `4e67243dd49058187e6376ff26ea7ee174387930`. The Human-attributed independent Gemini 3.8 Flash High / Antigravity STRICT READ-ONLY specification report was PASS (4 INFO, zero blockers), as recorded in the existing README row. Exact-main [CI #39196559718](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/39196559718) was reported SUCCESS: MCP 152/152, backend 1094 pass / 2 skip, Playwright 78 + 77 + 5 + 8 pass. These counts belong to that specification merge, **not** to PR #134.

The separate README synchronization [PR #134](https://github.com/nshaokiet/ai-ip-description-generator/pull/134) merged at `e4d0093fc1cffd07b2226cd8b6c673bab2a820f1`; Git parents are `4e67243dd49058187e6376ff26ea7ee174387930` and reviewed documentation head `d2e0e0d50960b9c71a64b9c03d54363b6332c586`; merge tree `d9bece867a35c844668c1a48edc528184d363971` matches the reviewed head tree. The Human supplied authenticated GitHub UI evidence for [postmerge CI #39210714722](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/39210714722): main/short SHA `e4d0093`, workflow SUCCESS, both `mcp-tests` and `build-and-test` SUCCESS, duration 16m 7s and two nonblocking annotations. This is **Human-provided UI evidence**, not a direct Actions API read. Per-job test counts and the annotations' details were not available in this audit. README on the merge tree still described A as governance review pending; this candidate corrects that historical status. Formal completion of this new factual sync depends on its own review/merge and current Render readback.

## PREAPI-001-B

[PR #135](https://github.com/nshaokiet/ai-ip-description-generator/pull/135) is in Git history as normal merge/main `cdc879adedbb1c5d1945d2e5722d61df4959aebb`, parents `e4d0093fc1cffd07b2226cd8b6c673bab2a820f1` and reviewed implementation `edcad55f156b89cc84ebc8b8f00b1330ed08e02d`, tree `f9da49322a492053c89841015646d95bd9b0d48e`. The reviewed implementation tree is `91ce82ab592b59edd07b55a3573ea01301f5191e`. The five-file test-only delta is `+404/-1`: `tests/e2e/provider_tripwire.py`, `tests/e2e/offline_backend.py`, `tests/backend/test_preapi_provider_tripwire.py`, `tests/backend/test_core_pipeline_e2e_offline.py`, `frontend/e2e/integration.spec.ts`. External Gemini 3.8 Flash High / Antigravity STRICT READ-ONLY review was Human-reported PASS with 3 INFO and zero blockers; [exact-head CI #39206503443](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/39206503443) was previously reported SUCCESS. Local premerge targeted pytest was 37 passed; full offline pytest was 1102 passed / 3 skipped, with UTF-8 subprocess mode on Windows. Frontend lint/typecheck/build passed in that candidate. None of those counts are asserted as the new postmerge run's counts.

The [postmerge CI #39215886819](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/39215886819) is linked to the B merge in the Human checkpoint. Its last supplied observation was `mcp-tests` SUCCESS and `build-and-test` IN_PROGRESS. The private Actions run and [Issue #133](https://github.com/nshaokiet/ai-ip-description-generator/issues/133) were not readable through the GitHub connector in this audit (`Unknown tool`), so final workflow conclusion, actual pass/skip counts, canonical issue criteria and any retries remain **UNVERIFIED**. B must not be marked formally CLOSED until they are checked. The original Issue #133 description is historical; do not rewrite it to make its pre-authorization state appear current. Parent [Issue #131](https://github.com/nshaokiet/ai-ip-description-generator/issues/131) and MCP SQLite [Issue #126](https://github.com/nshaokiet/ai-ip-description-generator/issues/126) stay OPEN.

### Provisional B-01…B-08 implementation mapping — verify against current Issue #133

| Check | Recorded evidence / remaining gate |
|---|---|
| B-01/B-02 | Existing synthetic PDF/DOCX browser and backend E2E; normal counters required zero. Verify exact postmerge job output. |
| B-03 | Test-only negative probes blocked two missing-runtime fallbacks and four SDK constructors; deliberate blocks counted separately. |
| B-04 | Five outbound socket/DNS/async probes blocked; loopback communication tested. This is process interception, not OS egress proof. |
| B-05 | Unknown/deleted source and extraction refusal cleanup tests; inspect canonical issue wording before closing. |
| B-06 | Draft incomplete and existing refusal/timeout/schema/export coverage; no new product code. |
| B-07 | Existing metadata/evidence checks; self-consistent foreign analysis/draft source custody remains unresolved for PREAPI-C1. |
| B-08 | Redacted counters and safe error checks; no source/key content in test evidence. |

The browser test-process metric showed normal `provider_api_requests=0`, `unexpected_provider_client_attempts=0`, `unexpected_egress_attempts=0`, and deliberate-probe count 0 during normal execution. `provider_api_requests=0` is an **inferred invariant** from blocked client construction/egress, not a directly instrumented HTTP-dispatch count. Intentional negative probes recorded blocked attempts separately. The Windows local Playwright `ECONNRESET` root cause was not proven; do not convert that local run into a full clean pass. Released v1 source custody for a self-consistent foreign pair is still open. EVAL-001 PRODUCT_RUNTIME is `NOT_DETERMINED`; model entitlement unverified; production Claims and public v2 API remain disabled. No paid provider, confidential research, Render deploy or active SQLite operation was part of this work.

## Render and closeout gate

Fresh connected Render read on 19/10/2026 in Human-confirmed workspace `tea-dav602rncjis739cu580` found backend `srv-dav6uqvpn0mc73af2j9g` and frontend `srv-dav6uqnpn0mc73af2hp0` both `autoDeploy=no`, `autoDeployTrigger=off`, preview generation `off` and `pullRequestPreviewsEnabled=no`. Each latest deployment is still `live` at historical SHA `8c36b2bc662ed41b2a9b3635d5d4d29110b1d9bb` from 14/10/2026: backend deploy `dep-db7epp3bc2fs73euislg`, frontend `dep-db7erbvavr4c73fvs3gg`. No PREAPI merge-triggered deployment appears as the latest deployment. No service change is proposed. A and B are **merged**; this receipt is a docs-only candidate. Final task closeout requires the outstanding B exact-main CI/job/count read, current Issue #133 acceptance reconciliation, independent fixed-SHA review of this docs PR, its required CI and accepted merge/postmerge check. This receipt does not self-approve those gates.
