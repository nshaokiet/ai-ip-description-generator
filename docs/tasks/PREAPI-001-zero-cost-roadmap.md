# PREAPI-001 — Remaining zero-cost readiness plan

| Field | Value |
|---|---|
| Version | 0.1.2 — factual readiness reconciliation; candidate PRs remain review-gated |
| Date / baseline | 21/10/2026 / verified `main` `d7516d4322f828c5802ec6d9e5ef5f8dffa5721d` |
| Source | [PREAPI v0.1.3](PREAPI-001-zero-cost-readiness.md), [frozen C1 contract](PREAPI-001-C1-source-custody-contract.md), [EVAL-001](EVAL-001-semantic-quality-evaluation.md), repository source/tests and linked PR/CI records |

This plan distinguishes merged evidence from Draft PR candidates. `OFFLINE_READY` means a bounded synthetic path was executed without a paid provider. A frozen specification is distinct from its implementation; a passing local test is distinct from final CI and independent review. `AWAITING_FUNDING` covers live provider evaluation. `LIVE_PROVIDER_VALIDATED` applies to **none** of these rows.

| Task | Current state | Implemented | Tested / evidence | Blocker | Human approval needed | Next action |
|---|---|---|---|---|---|---|
| PREAPI-A | Spec #132, governance #134 and factual closeout #136 **MERGED** | Spec v0.1.3 and A/B receipt on main | #136 merge `c113f2e…`; [exact-main CI #39229809579](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/39229809579) both jobs SUCCESS | Parent #131 remains OPEN; no product-runtime acceptance | No additional approval for this historical scope | Preserve accepted A/B closeout evidence |
| PREAPI-B | Test-only #135 and governance #136 **MERGED**; [Issue #133](https://github.com/nshaokiet/ai-ip-description-generator/issues/133) **CLOSED** | Five test files, tripwire, synthetic E2E and synced receipt | Reviewed #135 `edcad55…`, implementation merge `cdc879a…`; #136 exact-main CI #39229809579 SUCCESS | Provider counter remains inferred; custody is C1 scope; Windows ECONNRESET cause unproven | No additional approval for historical test scope | Preserve caveats and Issue #133 disposition |
| PREAPI-C1 | Spec v0.1.1 Human-frozen and [#137](https://github.com/nshaokiet/ai-ip-description-generator/pull/137) **MERGED**; implementation [Draft #139](https://github.com/nshaokiet/ai-ip-description-generator/pull/139) | Candidate source-custody runtime only on PR branch; not on main | #139 HEAD `8eee90cc4e7c4e3916c76132c1ce92e8bf85182a`; [exact-head CI #39381046966](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/39381046966) SUCCESS; Codex targeted 22 passed | Independent implementation review PENDING; no merge this session | No additional scope inferred | Hand off fixed SHA for read-only review |
| PREAPI-C2 | Contract candidate [Draft #140](https://github.com/nshaokiet/ai-ip-description-generator/pull/140) | Doc only; no adapter/UI | HEAD `0b46eea63679380cff0d93d2864f04238738a7fd`; diff check PASS; CI #39545978861 FAILED at artifact upload quota, MCP job SUCCESS | C1 implementation is unmerged; transport/auth needs separate decision | Freeze/code authorization as applicable | Review contract and dependency gates; restore CI before merge |
| PREAPI-D | Offline checker candidate [Draft #141](https://github.com/nshaokiet/ai-ip-description-generator/pull/141) | Local no-client, no-egress readiness CLI/test; not on main | HEAD `91cfdeeb49f7ba341e7700ad967e2646940430fd`; Codex local 14 passed; CI #39546171580 FAILED at artifact upload quota, MCP job SUCCESS | No live provider authorization, entitlement or budget | Separate funded live pilot decision | Review exact SHA and restore CI before merge |
| PREAPI-E | Fixture inventory validator candidate [Draft #142](https://github.com/nshaokiet/ai-ip-description-generator/pull/142) | Local read-only gold provenance checker/test; not on main | HEAD `03f696b77b6cbbed3c03f584846653eae9f4b5c1`; Codex local 33 passed; 6 cases/154 items (102 KEY/52 SECONDARY); CI #39546255007 FAILED at artifact upload quota, MCP job SUCCESS | Fixture validation is not product evaluation | Separate funded product-runtime decision | Review exact SHA; restore CI before merge |
| EVAL-001 | `AWAITING_FUNDING` / PRODUCT_RUNTIME `NOT_DETERMINED` | Evaluator and accepted gold, not provider product results | 6/6 accepted gold; no authorized live product evidence | Provider entitlement, budget, lawful corpus/use and live test approval | Explicit funded provider/model/USD/call/token decision | Keep semantic acceptance undetermined |
| BLK-003 | OPEN | No production provider/security acceptance | None claimed here | Funding and authorized live evidence | Human exception/funding decision | Keep open |
| MCP SQLite #126 | OPEN, separate rollout | No active DB migration in PREAPI | No active database verification in this Draft | Backup/restore/writer-stop and rollout gate | Separate Human rollout decision | Plan on disposable copy only |

## C2 dependency proposal

The C1 specification is frozen and merged; its implementation remains a Draft PR awaiting independent review. C2 would consume only a current trusted custody revision and invoke P2-002 reconstruction, P2-003 specification, P2-004 supported-Claims checks, P2-005 seven-original assembly and P2-006 four-file render. Its review UI must show missing/unsupported content and require a Human checkpoint; artifact downloads must verify current session, revision and manifest. A future authenticated browser route needs a separate security decision. The C2 Draft is a contract, not executable integration.

## D offline harness boundary

Default `OFFLINE_ONLY`, fail closed even when an environment key happens to exist. Inspect installed OpenAI SDK import/version compatibility, prompt/schema references, provider runtime configuration shape, model identifier **syntax only**, timeout/retry limits and output/token caps without constructing any SDK client. Report credential state as `PRESENT`/`ABSENT` without value, prefix, length or fingerprint. Use test-only tripwire to deny non-loopback egress and client construction. Machine-readable result includes candidate Git SHA, each check `PASS`/`BLOCKED`/`NOT_RUN`, zero unexpected attempts, and a readiness status. `READY_FOR_AUTHORIZED_PROVIDER_SMOKE` means offline prerequisites only; model entitlement remains `UNVERIFIED`. Future live mode requires a separately authorized kill switch, max requests/tokens/USD, verified pricing, timeouts, retry ceiling and hard stop before any client is created. No such live mode exists now.

## E fixture evaluation boundary

Use the six Human-accepted, unchanged gold packages in `eval/semantic/v1/gold/` and existing evaluator tests to validate parsing, scoring arithmetic, reporting and refusal/missing-data labels with synthetic fixture judgments only. Record fixture provenance and actual case/item totals. Do not rewrite accepted gold, download full papers in CI, treat mock scores as model outcomes, or change `PRODUCT_RUNTIME=NOT_DETERMINED`. Funded evaluation still requires a separate provider/account/model, data-rights and budget decision.

## Exit gates

Zero-cost readiness requires accepted C1 custody implementation, separate C2 synthetic flow with four verified outputs, D offline checker, E fixture scorer validation, exact-SHA review/CI/merge receipts and unchanged deployment/security boundaries. It does **not** establish `LIVE_PROVIDER_VALIDATED`, semantic acceptance, patentability, filing readiness or production release.

Version 0.1.1 → 0.1.2 (21/10/2026, Codex): reconcile merged A/B and frozen C1 specification with unmerged C1/C2/D/E Draft PRs and their separately attributed evidence. No breaking change; no product or provider authorization added.
