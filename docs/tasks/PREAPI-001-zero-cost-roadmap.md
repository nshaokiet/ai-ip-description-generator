# PREAPI-001 — Remaining zero-cost readiness plan

| Field | Value |
|---|---|
| Version | 0.1.0 — planning Draft, not implementation authorization |
| Date / baseline | 19/10/2026 / `cdc879adedbb1c5d1945d2e5722d61df4959aebb` |
| Source | [PREAPI v0.1.3](PREAPI-001-zero-cost-readiness.md), [C1 contract candidate](PREAPI-001-C1-source-custody-contract.md), [EVAL-001](EVAL-001-semantic-quality-evaluation.md), repository source/tests |

This plan distinguishes evidence already on main from proposals. `OFFLINE_READY` means a bounded synthetic path was executed without a paid provider. `SPECIFICATION_READY` means a reviewable contract exists, not that it is frozen or implemented. `IMPLEMENTATION_PENDING` means no authorized code result. `AWAITING_FUNDING` covers live provider evaluation. `LIVE_PROVIDER_VALIDATED` applies to **none** of these rows.

| Task | Current state | Implemented | Tested / evidence | Blocker | Human approval needed | Next action |
|---|---|---|---|---|---|---|
| PREAPI-A | Specification and governance PRs #132/#134 merged; factual status sync pending | Spec v0.1.3 and README history | Main ancestry `e4d0093…`; Human-provided UI result and direct authenticated GitHub Actions/log readback: CI #39210714722 SUCCESS (MCP 152/152; backend 1094 pass/2 skip; frontend 73/73; Playwright 78+77+5+8) | Final docs-only governance review/CI/merge; no product changes | Review/merge decision for new docs PR | Review factual A/B governance Draft separately |
| PREAPI-B | Test-only PR #135 merged; postmerge receipt pending | Five test files, tripwire and synthetic E2E assertions | Reviewed `edcad55…`; main `cdc879a…`; exact-head CI #39206503443 SUCCESS; exact-main postmerge CI #39215886819 independently verified SUCCESS (MCP 152/152; backend 1103 pass/2 skip; frontend 73/73; Playwright 78+77+5+8) | Canonical B acceptance mapping and independent governance documentation PR review/merge | Review/merge decision for governance Draft; no product change | Postmerge evidence verified; finish canonical B acceptance reconciliation and governance closeout |
| PREAPI-C1 | `SPECIFICATION_READY` candidate only | No runtime/API code | V2-01…V2-10 specified, **NOT RUN** | Independent review, Human freeze and separate implementation authorization | Architecture/security, TTL/review/owner decisions in C1 | Fixed-SHA review of C1 Draft |
| PREAPI-C2 | `IMPLEMENTATION_PENDING` | No new product adapter/UI | Existing AI-CONV-002/004, P2-002…P2-006 synthetic components only | C1 freeze and C1 implementation custody proof | Separate C2 scope/acceptance authorization | Plan synthetic upload → trusted custody → review → four manifest-bound artifacts; no browser bearer reuse |
| PREAPI-D | `IMPLEMENTATION_PENDING` | No executable readiness harness | Existing provider tripwire is test-only | Separate authorization and report contract | Approve CLI scope and future live pilot only when funded | Implement later a default-OFF, no-client-construction offline checker |
| PREAPI-E | Planning only | EVAL framework and accepted gold inventory exist; no PREAPI-E code | Six accepted gold cases, 154 items: 102 KEY / 52 SECONDARY; fixture scoring is not PRODUCT_RUNTIME | Separate E implementation authorization | Approve fixture-only scope | Later test scorer/report pipeline without altering gold |
| EVAL-001 | `AWAITING_FUNDING` / PRODUCT_RUNTIME `NOT_DETERMINED` | Evaluator and accepted gold, not provider product results | 6/6 accepted gold; no authorized live product evidence | Provider entitlement, budget, lawful corpus/use and live test approval | Explicit funded provider/model/USD/call/token decision | Keep semantic acceptance undetermined |
| BLK-003 | OPEN | No production provider/security acceptance | None claimed here | Funding and authorized live evidence | Human exception/funding decision | Keep open |
| MCP SQLite #126 | OPEN, separate rollout | No active DB migration in PREAPI | No active database verification in this Draft | Backup/restore/writer-stop and rollout gate | Separate Human rollout decision | Plan on disposable copy only |

## C2 dependency proposal

After C1 is reviewed, frozen and separately authorized for code, implement and test trusted source custody first. C2 then consumes only a current trusted custody revision and invokes P2-002 reconstruction, P2-003 specification, P2-004 supported-Claims checks, P2-005 seven-original assembly and P2-006 four-file render. Its review UI must show missing/unsupported content and require a Human checkpoint; artifact downloads must verify current session, revision and manifest. A future authenticated browser route needs a separate security decision. No C2 executable work is authorized by this plan.

## D offline harness design (future authorization)

Default `OFFLINE_ONLY`, fail closed even when an environment key happens to exist. Inspect installed OpenAI SDK import/version compatibility, prompt/schema references, provider runtime configuration shape, model identifier **syntax only**, timeout/retry limits and output/token caps without constructing any SDK client. Report credential state as `PRESENT`/`ABSENT` without value, prefix, length or fingerprint. Use test-only tripwire to deny non-loopback egress and client construction. Machine-readable result includes candidate Git SHA, each check `PASS`/`BLOCKED`/`NOT_RUN`, zero unexpected attempts, and a readiness status. `READY_FOR_AUTHORIZED_PROVIDER_SMOKE` means offline prerequisites only; model entitlement remains `UNVERIFIED`. Future live mode requires a separately authorized kill switch, max requests/tokens/USD, verified pricing, timeouts, retry ceiling and hard stop before any client is created. No such live mode exists now.

## E fixture evaluation design (future authorization)

Use the six Human-accepted, unchanged gold packages in `eval/semantic/v1/gold/` and existing evaluator tests to validate parsing, scoring arithmetic, reporting and refusal/missing-data labels with synthetic fixture judgments only. Record fixture provenance and actual case/item totals. Do not rewrite accepted gold, download full papers in CI, treat mock scores as model outcomes, or change `PRODUCT_RUNTIME=NOT_DETERMINED`. Funded evaluation still requires a separate provider/account/model, data-rights and budget decision.

## Exit gates

Zero-cost readiness requires accepted C1 custody implementation, separate C2 synthetic flow with four verified outputs, D offline checker, E fixture scorer validation, exact-SHA review/CI/merge receipts and unchanged deployment/security boundaries. It does **not** establish `LIVE_PROVIDER_VALIDATED`, semantic acceptance, patentability, filing readiness or production release.
