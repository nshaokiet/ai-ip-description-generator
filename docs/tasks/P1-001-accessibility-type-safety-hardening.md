# P1-001 — Frontend Accessibility + Type Safety Hardening

| Field | Value |
|---|---|
| Version | 0.1.0 |
| Status | Local implementation verified; Draft PR/independent review pending |
| Owner | Codex (GPT-6 Sol) |
| Baseline | `d509152e160bfc641324800de0d34b2c6cc7392a` |
| Human implementation authorization | `HUMAN-P1-001-ZERO-COST-2026-09-29` |
| Branch | `feat/p1-001-accessibility-type-safety` |
| Independent implementation review | Gemini 3.1 Pro High — pending |

## Scope

Post-MVP frontend keyboard/focus accessibility, static TypeScript typecheck, CI gates, and deterministic offline regression only. This task adds no product capability, dependency, provider call, deployment, or test-expectation weakening.

## Preserved boundaries

- Project classification: **MVP COMPLETE — LOCAL/SYNTHETIC**; P1-001 does not change it.
- Provider authorization: **NOT GRANTED**; provider/API budget: **0**; paid/provider calls: **NONE**.
- EVAL-001 PRODUCT_RUNTIME: **DEFERRED — AWAITING FUNDING**; semantic acceptance remains undetermined.
- BLK-003: **OPEN**. No production, public deployment, or real/confidential-data authorization is implied.
- Claims remain outside the MVP.

## Implementation and evidence

- `frontend/package.json`: `typecheck` uses the existing TypeScript compiler without a new dependency.
- `.github/workflows/ci.yml`: offline Python dependency check and frontend typecheck gates.
- Frontend: result-tab keyboard navigation/roving focus, current workflow-step semantics, new global-error focus, visible keyboard focus.
- `frontend/e2e/integration.spec.ts`: synthetic browser regressions for these behaviors.
- `frontend/src/components/UploadPanel.tsx`: audited; existing file label, canonical Select document button, error alert and selected-file live status are preserved without modification.
- Python 3.12 `pip check`: PASS, no broken requirements.
- Full offline backend suite with live flags `0/0`: **407 passed, 3 skipped, 1 warning**. The first attempt hit a Windows default-Temp permission error in six pytest fixture setups; rerunning with a dedicated worktree `--basetemp` passed without backend/test-code changes.
- Frontend `npm run lint`, `npm run typecheck`, `npm run build`: PASS.
- Synthetic Playwright `npm run test:e2e`: **15 passed**, including new tab-keyboard, edit restriction, global-error focus and workflow-current-step regressions.
- Implementation SHA, Draft PR and PR CI: pending commit/remote verification.

## Handoff

After local checks and CI pass, hand the fixed implementation SHA to Gemini 3.1 Pro High for independent targeted review. Human / Product Owner retains merge authority; this task does not merge `main`.
