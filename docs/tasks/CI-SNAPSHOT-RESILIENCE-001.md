# CI-SNAPSHOT-RESILIENCE-001 — bounded pinned-index recovery

| Field | Value |
|---|---|
| Version / date | 1.0.0 / 2026-11-24 Asia/Saigon |
| Owner / implementer | Human Product Owner / Codex |
| Authority | Current Human attachment “CODEX — CI-SNAPSHOT-RESILIENCE-001”, sections 1–10 |
| Baseline | `448de79be9720d4d1fd5b6b7e1cb87a360a0d5a7` |
| Status | IMPLEMENTED_CANDIDATE / exact-HEAD CI and independent review PENDING; not Completed |
| Scope | QA snapshot-index helper, deterministic regressions and execution evidence only |
| Merge authority | NOT GRANTED; dependent branches remain unchanged |

## Reproduced mechanism

Original classification retries only 502/503 on three InRelease URLs. Preserved
official dependency CI logs also contain 500 and component Packages, English
Translation and command-not-found index failures. Replaying the actual diagnostics
from all four failed PRs returns original=False / corrected=True. Before the fix,
new deterministic regressions produced 14 failures / 38 passes, preserved privately.

## Bounded policy

Retry only 500/502/503 at the exact HTTPS official host and caller-pinned timestamp,
under noble/noble-updates/noble-security, for InRelease or main/universe index paths:
binary-amd64/all Packages, i18n Translation-en, cnf Commands-amd64, with explicitly
named compression suffixes. No pool/package downloads, other architecture, other
component/language, query suffix, traversal, host or timestamp is allowed.

Three attempts maximum, delays 2 and 5 seconds, fresh isolated lists per attempt.
Unknown/permanent/mixed errors and signature/hash/certificate failures deny. An
existing attempt directory cannot be reused. Success additionally requires all
three nonempty InRelease files and six main/universe amd64 Packages indexes outside
partial/, with no symlink, fetch error, partial summary or integrity error, and APT
exit zero. APT remains responsible for signature and package-index hash verification.

Optional Translation/cnf acquisition is NOT disabled. There is no generic retry,
live fallback, mirror, partial-index reuse, integrity bypass or package/pin change.
Retries cannot guarantee availability; exhaustion remains BLOCKED_EXTERNAL.

## Validation and gates

Targeted snapshot-index, exact QA-environment and unchanged renderer regressions:
**74 passed**, 16.03s. Full backend and required hosted CI gates must be read from
their actual final-SHA receipts; targeted results are not full CI acceptance.

All Ubuntu/architecture/snapshot/package/LibreOffice/Poppler/keyring definitions,
installer signature/hash options, layout criteria, fixtures, gold, workflow gates,
product runtime and dependency candidate branches remain unchanged.

Fresh independent Security AND Quality, separate actual sessions under standing
Gemini 4 Argon (High), must target the exact final HEAD/TREE. Desktop Node helper
initialization currently fails before app/model/session inventory; BLOCKED_REVIEW,
not a quota finding. Manual role-specific review prompts are prepared privately;
no reviewer identity, session, verdict or report hashes are invented.

Only after separate review, Human merge authorization, accepted merge and postmerge
verification may the shared repair be reconciled into dependency PRs164/169/170/172.
No model substitution, automatic merge or dependency integration is performed here.
Claims OFF, USD0 provider budget, synthetic inputs only, production NOT APPROVED.

## Handoff

```text
Task ID: CI-SNAPSHOT-RESILIENCE-001
Agent: Codex
Reviewer: NOT_RUN / desktop helper initialization blocked
Status: IMPLEMENTED_CANDIDATE / CI_REVIEW_PENDING
Version: 1.0.0
Work completed: actual-log replay, bounded classifier correction, complete-index checks, deterministic regressions
Files affected: snapshot helper, regression test, this record and README task status
Evidence checked: original failed CI logs, exact QA pins, red/green JUnit, unchanged installer/workflow
Findings: mixed allowed HTTP500/component-index errors were incorrectly nonretryable
Decisions: actual scoped Human authorization; no unrelated policy adoption
Issues: external snapshot availability and genuine reviewer dispatch remain independent gates
Security impact: no integrity relaxation; require complete fresh package indexes before success
Recommended next action: exact-HEAD full CI/security and independent dual review; no merge without Human approval
```

## History

None → 1.0.0, 2026-11-24, Codex: initial scoped remediation and evidence record under
actual Human authorization. Breaking change: No product/API/pin change; QA retry
classification expands narrowly and successful-index completeness is strengthened.
