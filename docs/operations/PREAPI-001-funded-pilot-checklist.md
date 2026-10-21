# PREAPI-001 — Future funded provider pilot checklist

| Field | Value |
|---|---|
| Version | 0.1.0 — preparation checklist |
| Date | 21/10/2026 |
| Parent | [PREAPI-001 Issue #131](https://github.com/nshaokiet/ai-ip-description-generator/issues/131), [zero-cost readiness specification](../tasks/PREAPI-001-zero-cost-readiness.md) |
| Current gate | **NOT AUTHORIZED**; paid provider/API budget USD 0; EVAL-001 PRODUCT_RUNTIME **NOT_DETERMINED** |

This checklist prepares a future Human decision. Completing an offline checker or fixture test cannot authorize a live call. The existing runtime model string `gpt-5.6-sol` is a configured value; actual API account entitlement and live pricing are unverified.

## Before requesting pilot approval

- [ ] Close the relevant zero-cost gates with immutable evidence: C1 postmerge main CI SUCCESS; C2 accepted scope and synthetic source-to-four-output integration if v2 is part of the pilot; D and E final-head CI SUCCESS and independent reviews; no unresolved security/Claims findings. Record exact merge/main SHAs.
- [ ] Choose a permitted synthetic or explicitly licensed/open corpus. Record source, license/consent, allowed provider transfer, storage and deletion terms. Do not use unpublished or confidential research while BLK-003 remains open.
- [ ] Confirm actual provider account, model availability, SDK/version, request format and current price from official provider/account sources. Record timestamp and pricing basis. A static model identifier check is insufficient.
- [ ] Human sets a numeric total USD cap, maximum requests, input/output token limits, concurrency, retries, timeout and execution window. Estimate worst-case cost including retries before running. The current values are **[CẦN XÁC NHẬN]**; no default positive spend is implied.
- [ ] Implement and test a hard stop *before* client creation/request dispatch when the approved cap, request/token allowance or expiry is missing or exhausted. Provide a kill switch, dry-run ledger and test for refusal, timeout, partial response, retry exhaustion and uncertain billing. No unbounded retry.
- [ ] Inject the key through approved backend secret management only after approval. Log key presence as PRESENT/ABSENT, never value, prefix, length or fingerprint. Redact prompts, source text, provider response and private paths; retain only approved minimal metadata and error codes.
- [ ] Define quality thresholds and reviewer rubric before product runs. Decide which EVAL-001 gold items are permitted for provider transfer and how each run links to exact source and model/config versions. Keep fixture scores separate from PRODUCT_RUNTIME.
- [ ] Record an explicit Human authorization reference for provider/model/corpus, budget, security/data handling, execution owner and rollback. Recheck BLK-003 and production/Claims boundaries; pilot authorization is not production release.

## Execution sequence after explicit authorization

1. Preflight the exact committed configuration and offline D report, then verify the account's model entitlement without exposing credentials in output. An authorized live entitlement probe counts against the approved budget.
2. Run one bounded synthetic/open-license extraction smoke. Verify source evidence, schema, refusal/error handling, measured usage and ledger. Stop on failed grounding, unexpected network destination, spend cap discrepancy or leaked data.
3. If step 2 passes and the Human approval covers it, run one bounded draft smoke and verify Draft JSON, missing/inference labels, no unsupported Claims promotion and measured usage.
4. Only if separately approved, run the end-to-end synthetic v2 flow and then the authorized EVAL-001 corpus. Compare to the predefined rubric; retain source-level failures and uncertainty. Do not turn a passing synthetic smoke into semantic acceptance.
5. Publish a redacted evidence receipt with exact code/config/model identifiers, authorized corpus IDs, counts, token/USD usage, errors, reviewer result and rollback state. Human decides any subsequent budget, production, real-data or Claims change.

## Stop and rollback

Stop new requests when the cap/ledger cannot be reconciled, entitlement fails, provider outputs lack source grounding, a secret/source appears in logs, data rights are unclear, or required review/CI changes. Disable the provider flag, revoke the pilot credential if exposed, preserve approved redacted audit evidence and clean source/derived data under the authorized retention rule. Keep `PRODUCT_RUNTIME=NOT_DETERMINED` until actual authorized runs and the predefined quality decision establish otherwise. No Render deployment or public v2 activation is part of this checklist.
