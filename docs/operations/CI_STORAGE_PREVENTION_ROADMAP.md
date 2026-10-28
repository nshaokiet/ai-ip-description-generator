# CI storage prevention and execution roadmap

| Field | Value |
| --- | --- |
| Version / previous version | 0.1.0 / none |
| Date / task / author | 2026-10-28 / AIIP-CI-STORAGE-ROADMAP-20261028 REVISION 2 / Codex |
| Revision summary | Initial dependency-ordered planning roadmap and current evidence boundaries |
| Authorization | Human AIIP-CI-STORAGE-ROADMAP-20261028 REVISION 2: planning and documentation integration only |
| Implementation status | PLANNING ONLY; future work PLANNED / NOT AUTHORIZED unless independently authorized |
| Dependencies | Verified account capacity, existing PR gates and separately authorized implementation/reviews |
| Security / compatibility | Mandatory security archives, CI and review gates remain; no runtime, CI or status-contract change |
| Breaking change | No — documentation only |

## Current evidence and boundaries

GitHub main was verified at `53c253be874236c6f38a5333a6f7f3390de9f51e`. PR [#147](https://github.com/nshaokiet/ai-ip-description-generator/pull/147) is Draft with attributed Gemini PASS on `c50be576b39acd2eac9da096efd11060545463d1`; the reviewer executed on a tree-identical local commit and narrow documentary correction remains pending. Required hosted CI [40081813108](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/40081813108) failed quota; this is not CI SUCCESS. PR [#146](https://github.com/nshaokiet/ai-ip-description-generator/pull/146) is Draft with attributed Gemini PASS on `29daeb208f7736a448297f699e674192c124c7da`; review used the staged tree, and hosted CI [40078806412](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/40078806412) failed audit and uploads. Each PASS applies to its own reviewed candidate; refreshed heads require applicable fresh review. PR [#144](https://github.com/nshaokiet/ai-ip-description-generator/pull/144) is Draft, reviewed at `43e07dfa36b217066647af23f2dda2c6c715bd0c`, CI failed quota and a conflict requires reconciliation. Verify current PR state and policies again before action.

On 2026-10-28 the read-only repository artifact scan found zero currently visible artifacts/bytes. This is not an account-wide billing or capacity measurement. Human reported 0.5 GB / 0.5 GB on 2026-10-24; accumulated GB-hours, Packages, inaccessible repositories and quota enforcement remain unverified. No new CI is justified by the visible repository inventory alone. The successful 2026-10-22 cleanup and elapsed time do not prove quota recovery. No fixture approval, paid provider, real paper or deployment follows from this plan.

## Dependency sequence

1. **P0 — capacity:** obtain positive account-side evidence of usable Actions storage, identify accounting/period and preserve required evidence. No speculative rerun.
2. **P0 — security:** for PR147, obtain required exact-head CI SUCCESS and all current review, platform, scope and security gates. Its previous Human authority is conditional; this roadmap does not authorize a merge. After eligible merge under applicable separate authority, verify main and postmerge CI.
3. **P0 — CI-V2-001:** reconcile PR144 conflict on the verified base, preserve history, assess whether changes require fresh fixed-SHA review, and complete only after all required gates succeed.
4. **P0 — storage prevention:** independently review [CI-V2-003](../tasks/CI-V2-003-artifact-storage-specification.md), obtain separate Human implementation authorization, implement and measure complete mandatory security evidence and compact storage against a comparable historical baseline. Preserve full review-required evidence; success <1 MB and functional failure <5 MB are goals, not truncation limits.
5. **P1 — specification:** refresh PR146 non-destructively onto appropriate verified main, preserve canonical REVISION-004 bytes (SHA-256 `1e2f5376f526e7e3176c8731deb2d49dccf1ef1de7b347643a60d4b011f8ce3f`) and review evidence, obtain applicable fresh final-SHA review and required CI, then close only under all governance gates.
6. **P1 — tiered CI:** review [CI-V2-002](../tasks/CI-V2-002-tiered-ci-specification.md), obtain separate Human implementation authorization, then validate risk classification, aggregate gate and coverage without weakening existing required checks or migration contracts.
7. **P1/P2 — product:** separately plan/authorize C1 additive extensions and C2 adapter, prepare a synthetic fixture approval package, and implement T01–T80 only after the required approvals and prerequisites. Offline end-to-end patent drafting validation follows within separately authorized synthetic scope. Future real-paper/provider evaluation needs independent Human authorization and budget.

This order is a planning dependency map, not an instruction to begin future tasks. Local tests and external Gemini verdicts cannot replace hosted CI; unknown account metrics cannot establish storage recovery. Prior independent reviews do not authorize later changed SHAs. No new PR for this roadmap while its pull_request trigger would knowingly run against unverified quota.

## Acceptance and operational safeguards

Review both 0.2.0 specifications, the preserved 0.1.0 provenance and this roadmap at one exact final SHA; independently verify no workflow/application changes and the required status and security contracts. Any later implementation separately proves complete evidence, raw/upload byte measurement, provenance/hash integrity, retention, fail-closed selection, required CI, rollback and governance. Proposed 60/80/90% alerts require verified account metrics and never suppress mandatory evidence or acceptance gates. USD 0; no billing changes, protected deletion, CI waiver, C1/C2 code, fixture approval or deployment is authorized here.
