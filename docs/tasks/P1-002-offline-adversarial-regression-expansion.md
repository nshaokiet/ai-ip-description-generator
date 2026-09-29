# P1-002 — Offline Adversarial Regression Expansion

| Field | Value |
|---|---|
| Version | 0.1.1 |
| Status | **IMPLEMENTED LOCALLY — AWAITING PR CI / INDEPENDENT REVIEW** |
| Owner | Codex |
| Baseline | `f065ad8b9bd7644df050e3697685d27d7b45ea32` |
| Human authorization | `HUMAN-P1-002-OFFLINE-ADVERSARIAL-2026-09-29` |
| Branch | `feat/p1-002-offline-adversarial` |
| Independent reviewer | Gemini 3.1 Pro High |

Version 0.1.1 (29/09/2026): record six implemented regressions and the final green local verification matrix; merge and completion remain blocked on fixed-SHA independent review, PR CI, merge, and main CI.

Version 0.1.0 (29/09/2026): register the authorized scope, coverage audit, and implementation plan.

## Scope

Expand deterministic offline/synthetic adversarial regression coverage without changing prompts, schemas, models, runtime/provider configuration, deployment, Claims, or production/data policy.

## Coverage audit and implementation plan

Existing tests already cover corrupt/encrypted PDF and DOCX inputs, MIME/signature mismatch, unsafe OOXML content, parsing order and Unicode, canonical schema failures, grounding/cross-reference failures, missing-information propagation, draft business rules, DOCX cleanup, and browser error/recovery flows.

The implementation therefore targets six concrete gaps:

1. Prove the exact 10 MiB streaming limit is accepted, preventing an off-by-one regression.
2. Prove the exact 50-page PDF limit is accepted while the existing 51-page rejection remains intact.
3. Reject a disguised double extension before PDF parsing.
4. Reject duplicate emitted evidence IDs at the second conflicting entry.
5. Fail malformed JSON safely at both public draft-validation and DOCX-export boundaries without runtime or renderer work.
6. Bind export authorization to the exact revision identifier as well as draft content.

## Preserved boundaries

- Provider/API calls: **PROHIBITED / NONE**; paid services: **NONE**.
- Provider/live test flags must remain `0 / 0`.
- Project classification remains **MVP COMPLETE — LOCAL/SYNTHETIC**.
- EVAL-001 PRODUCT_RUNTIME remains **DEFERRED — AWAITING FUNDING**.
- BLK-003 remains **OPEN**; no production/deployment or real/confidential-data authorization.
- P1-003 through P1-006 and DEPLOY-001 remain **PLANNED**.

## Verification gates

- Targeted new/affected backend regressions.
- Full offline pytest suite and `pip check`.
- Frontend lint, typecheck, build, and synthetic Playwright suite.
- PR CI on the final implementation SHA.
- Fixed-SHA independent Gemini 3.1 Pro High review before merge.

## Local implementation evidence

- Newly added regression tests: **6**.
- Targeted affected backend suites: **73 passed / 1 skipped**.
- Full offline backend: **413 passed / 3 skipped / 1 warning**.
- Python dependency consistency: `pip check` **PASS**.
- Frontend lint: **PASS**.
- Frontend typecheck: **PASS**.
- Frontend production build: **PASS**.
- Synthetic Playwright: **15 passed** using the repository-approved `PLAYWRIGHT_PYTHON` override.
- Live flags: `RUN_OPENAI_LIVE_TESTS=0`, `RUN_OPENAI_DRAFT_LIVE_TESTS=0`.
- Provider/API calls: **NONE**.

README remains `Incomplete — Planned` until the required fixed-SHA review, CI, merge, final main CI, and post-merge closeout gates are complete.
