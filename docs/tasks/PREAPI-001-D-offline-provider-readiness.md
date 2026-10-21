# PREAPI-D — Offline provider readiness preflight

| Field | Value |
|---|---|
| Version | 0.1.0, review candidate |
| Status | Draft implementation; independent review pending; no provider authorization |
| Task / authority | PREAPI-D; Human zero-cost development instruction, 21/10/2026 |
| Base | `d7516d4322f828c5802ec6d9e5ef5f8dffa5721d` |

## Purpose and boundary

Run `python -m tools.preapi_d_offline_readiness` to check local static
prerequisites for a **future** funded smoke test. This command imports the
installed OpenAI package but never constructs a client, sends a request,
performs model discovery or reads credential contents into a report. It does
not start extraction or Draft runtime. It may return
`READY_FOR_AUTHORIZED_PROVIDER_SMOKE` only for the offline checks below; that
label is not permission to call a provider, proof of model entitlement,
evidence of semantic quality, or completion of EVAL-001. Current provider
authorization is NOT_GRANTED, budget USD 0 and product runtime
NOT_DETERMINED.

## Static checks and source map

| Check | Source | Failure |
|---|---|---|
| SDK pin/import | `backend/requirements.txt`, installed package metadata, local Python import | `BLOCKED` if absent, mismatched or unimportable; no remote version query |
| Prompts | `prompts/extraction/v1.0.0`, `prompts/draft-generation/v1.0.0` | `BLOCKED` if missing or empty |
| Schemas | Canonical analysis and patent Draft schema paths in the two runtimes | `BLOCKED` if absent or invalid Draft 2020-12 schema |
| Model syntax | Fixed model constants in `backend/app/core/config.py` | Syntax only; entitlement `UNVERIFIED` |
| Timeouts and token caps | Existing `Settings` constraints, nonsecret `OPENAI_*` numeric environment | `BLOCKED` if invalid or over approved local caps |
| Retry ceiling | Existing extraction/Draft max-retry constants | `BLOCKED` if outside 0–2 |
| Default-off | `RUN_OPENAI_LIVE_TESTS`, `RUN_OPENAI_DRAFT_LIVE_TESTS` | `BLOCKED` unless both exactly `0` or absent |
| Credential presence | `OPENAI_API_KEY` | `PRESENT`/`ABSENT` only; never value, length, prefix, suffix or hash |

The checker exposes no live mode. Tests patch `OpenAI` and socket transport to
fail if the checker attempts construction or egress, and reuse the existing
`tests/backend/test_preapi_provider_tripwire.py` negative probe. The report's
`tripwire_verification=TEST_SUITE_ONLY` deliberately distinguishes test
evidence from an action performed by the CLI. No broad network isolation is
claimed for arbitrary other processes. JSON is deterministic for the same
environment and installed package state, with no timestamp or path to a
private source file.

Sample sanitized fields (actual report values depend on local files and SDK):

```json
{
  "mode": "OFFLINE_ONLY",
  "credential_status": "ABSENT",
  "provider_execution": "NOT_RUN",
  "provider_authorization": "NOT_GRANTED",
  "provider_budget_usd": 0,
  "model_entitlement": "UNVERIFIED",
  "product_runtime": "NOT_DETERMINED",
  "future_live_budget_enforcement": "NOT_IMPLEMENTED",
  "readiness": "READY_FOR_AUTHORIZED_PROVIDER_SMOKE"
}
```

## Future live gate

No request/token/USD hard stop is implemented in this preflight. A live pilot
must have a separate Human decision specifying account, model, allowed corpus,
request count, token ceilings, current price schedule and USD cap. A future
runtime must enforce the cap before client construction, including retry cost,
with a kill switch and redacted logs. Entitlement and pricing must be verified
at that time; the local model identifier and SDK pin alone do not prove them.
No existing live flag is enabled by this task.

## Acceptance and review

Tests cover D-01 SDK metadata/import, D-02/03 credential status and redaction,
D-04/05 missing prompt and invalid schema, D-06 syntax, D-07 retry ceiling,
D-08 timeout/token bounds, D-09 default-off, D-10 tripwire through the existing
suite, D-11 no network, D-12 JSON report, D-13 deterministic result, D-14 no
secret marker and D-15 no provider execution. An independent reviewer must
inspect the exact SHA and distinguish static success from funded pilot
authorization. CI and review remain pending for this Draft; no merge follows
from local tests alone.
