# P1-002 — Offline Adversarial Regression Expansion

| Field | Value |
|---|---|
| Version | 0.2.0 |
| Status | **IMPLEMENTATION MERGED — GOVERNANCE CLOSEOUT REVIEW PENDING** |
| Owner | Codex |
| Baseline | `f065ad8b9bd7644df050e3697685d27d7b45ea32` |
| Human authorization | `HUMAN-P1-002-OFFLINE-ADVERSARIAL-2026-09-29` |
| Branch | `feat/p1-002-offline-adversarial` |
| Independent reviewer | Gemini 3.1 Pro High |
| Reviewed implementation SHA | `4742b0f8a88a51d4e085b209bceeec1f942a8deb` |
| Review decision | **PASS** |
| Findings | **NONE** |
| Implementation PR | [#40](https://github.com/nshaokiet/ai-ip-description-generator/pull/40) |
| Implementation merge / main SHA | `f568df382a07f38b03dfb8aaddebf8dc6accf6b7` |
| Implementation main CI | `36583295714` — **SUCCESS** |

Version 0.2.0 (29/09/2026): record Gemini 3.1 Pro High fixed-SHA PASS/findings NONE, PR #40 merge, successful main CI, and governance-closeout handoff; final task completion remains gated on review and merge of the closeout PR, final main CI, and MCP completion.

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

## Implementation review and merge evidence

- Gemini 3.1 Pro High reviewed exact SHA `4742b0f8a88a51d4e085b209bceeec1f942a8deb`: **PASS**; findings **NONE**.
- PR CI `36580517321`: **SUCCESS** on the exact reviewed SHA.
- PR [#40](https://github.com/nshaokiet/ai-ip-description-generator/pull/40) merged normally at `f568df382a07f38b03dfb8aaddebf8dc6accf6b7`.
- Resulting `main`: `f568df382a07f38b03dfb8aaddebf8dc6accf6b7`.
- Push/main CI `36583295714`: **SUCCESS** on the exact merge SHA.
- Final implementation evidence: backend **413 passed / 3 skipped / 1 warning**; `pip check` **PASS**; frontend lint/typecheck/build **PASS**; synthetic Playwright **15 passed**; live flags `0 / 0`; provider/API calls **NONE**.

README now proposes P1-002 as `Completed` in this governance-only closeout branch. Final task closeout remains pending fixed-SHA independent review of these governance changes, closeout PR merge, final main CI, and evidence-backed MCP transition to `COMPLETED`.
