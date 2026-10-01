# P1-006 — UX Polish

## Metadata

| Field | Value |
| --- | --- |
| Task | P1-006 |
| Status | **CLOSED / COMPLETED — MERGED; CLOSEOUT REVIEW PENDING; MCP TOOL LIMITATION** |
| Authorization | `HUMAN-P1-006-UX-POLISH-2026-10-01` |
| Baseline main | `90ead2c0f26f17c617cfa71e6d7b3d16808d46e1` |
| Branch | `feat/p1-006-ux-polish` |
| Implementation owner | Codex under AGENTS.md standing delegation |
| Independent reviewer | Gemini 3.1 Pro High / Antigravity read-only reviewer |
| Scope | Local/synthetic MVP UX polish only; no pipeline semantic change |
| Data | Synthetic/reproducible test data only |
| BLK-003 | **OPEN** |
| DEPLOY-001 | **NOT AUTHORIZED** |
| Production | **NOT APPROVED / NOT PERFORMED** |

## Purpose

P1-006 improves the usability and clarity of the existing local/synthetic MVP without changing the underlying extraction, drafting, validation, DOCX, provider, model, schema, prompt, or runtime-policy semantics.

The target workflow remains:

`Upload → Analyze → Review/Edit → Validate → Export`

The task is intentionally bounded to presentation-layer behavior, recoverability, interaction clarity, responsiveness, and deterministic browser regression coverage.

## Authorized scope

The implementation MAY:

- improve responsive behavior across desktop, tablet, and narrow mobile viewports;
- improve visual hierarchy, spacing, readability, action priority, and workflow clarity;
- make upload, process, validation, and export busy/loading states explicit;
- disable actions that would create duplicate in-flight requests;
- improve actionable error states and recovery controls;
- preserve valid selected revisions/results during recoverable failures;
- make workflow progress states clearer for current/completed/pending steps;
- improve retry/recovery behavior without weakening current safety rules;
- preserve and strengthen existing accessibility and keyboard usability;
- add or update deterministic Playwright coverage for the authorized UX behavior;
- make narrowly scoped frontend refactors required to satisfy these acceptance criteria.

## Explicitly out of scope

P1-006 does NOT authorize:

- provider/API calls, spend, or new external AI services;
- production deployment or public release;
- DEPLOY-001 implementation;
- BLK-003 closure;
- real, confidential, unpublished, or otherwise sensitive research data;
- authentication, storage, retention, tenancy, or secret-management policy changes;
- Claims generation or Claims behavior changes;
- extraction/drafting prompt semantic changes;
- JSON schema or API breaking changes;
- provider/model/runtime-policy changes;
- patentability, legal-advice, or filing-readiness claims;
- wholesale redesign unrelated to a concrete UX acceptance criterion.

## Acceptance criteria

### AC-01 — Responsive primary workflow

At a 390 px viewport, the primary upload, processing, results, validation, export, and error/recovery states must remain usable without horizontal page overflow.

### AC-02 — Busy/loading clarity

Upload, process, validation, and export operations must expose a clear in-progress state. Controls that could duplicate the same in-flight action must be disabled or otherwise safely blocked until the operation settles.

### AC-03 — Safe error presentation

Backend, proxy, network, and validation errors must continue to avoid exposing raw internal paths, stack traces, provider details, or unredacted implementation data.

### AC-04 — Upload/process recovery

A failed or invalid upload must provide a clear path to choose another document. A process failure that invalidates the source must clearly require re-upload rather than presenting a stale or misleading retry.

### AC-05 — Export recovery

A recoverable export failure must create no download, preserve the selected validated revision, and allow the user to return to the results workspace and retry.

### AC-06 — Validation recovery

A validation failure must preserve the currently selected revision and its visible draft content so the user can correct the draft without losing context.

### AC-07 — Workflow clarity

The application must make the intended sequence `Upload → Analyze → Review/Edit → Validate → Export` understandable through visible labels, progress/state treatment, and action hierarchy without requiring knowledge of internal implementation details.

### AC-08 — Keyboard accessibility

The existing keyboard-only upload/edit/validate/review/export workflow must remain functional. Focus-visible behavior and alert/error focus handling must not regress.

### AC-09 — Contract preservation

Existing backend API contracts, prompt/schema semantics, runtime-policy behavior, validation rules, DOCX contract, safety notice semantics, and provider isolation must remain unchanged unless a strictly non-breaking frontend compatibility adjustment is required.

### AC-10 — Safety notices

The UI must retain the meaning of the existing notices that AI output requires human review, is not legal advice, and is not filing-ready.

### AC-11 — Deterministic regression coverage

Playwright coverage must verify the material P1-006 UX behavior, including narrow viewport usability, busy/disabled behavior where practical, and recovery-state preservation.

### AC-12 — Quality gates

Before merge, the final implementation SHA must satisfy all applicable repository gates:

- backend offline regression: PASS;
- Python dependency consistency: PASS;
- frontend lint: PASS;
- frontend typecheck: PASS;
- frontend build: PASS;
- synthetic Playwright: PASS;
- live flags remain disabled for CI/offline validation;
- provider/API calls: NONE.

### AC-13 — Independent fixed-SHA review

The final implementation SHA must receive independent Gemini 3.1 Pro High / Antigravity read-only review with:

- exact reviewed SHA recorded;
- decision **PASS**;
- no unresolved blocking findings;
- reviewer must not modify tracked repository files.

A new implementation commit after PASS requires review of the new final SHA before merge.

## Current behavior that must be preserved

The existing application already provides several behaviors that P1-006 must not regress:

- invalid/corrupt uploads are rejected safely;
- raw backend/proxy error text is not surfaced to the user;
- process failures requiring re-upload do not leave a stale ready state;
- export failures preserve the selected revision;
- network/non-JSON backend failures preserve current revision context;
- keyboard-only edit/validate/review/export is covered;
- a 390 px narrow viewport is covered for editing, validation, export, and error recovery;
- safety notices and human-review wording are present.

P1-006 is therefore a hardening/polish task, not a replacement of the existing frontend architecture.

## Implementation guidance

Likely implementation areas include, but are not limited to:

- `frontend/src/app/page.tsx`
- `frontend/src/app/globals.css`
- `frontend/src/components/UploadPanel.tsx`
- `frontend/src/components/WorkflowProgress.tsx`
- `frontend/src/components/ResultWorkspace.tsx`
- relevant child components only when required by an acceptance criterion;
- `frontend/e2e/integration.spec.ts` and narrowly scoped new E2E coverage if clearer.

Avoid touching backend, schema, prompts, provider/runtime policy, DOCX behavior, or unrelated governance files unless a concrete P1-006 acceptance criterion requires it.

## Required workflow

1. Start from exact baseline main `90ead2c0f26f17c617cfa71e6d7b3d16808d46e1`.
2. Work only on `feat/p1-006-ux-polish` or an equivalent isolated worktree for this task.
3. Inspect existing frontend behavior and current Playwright coverage before changing code.
4. Implement the smallest coherent changes needed to satisfy the acceptance criteria.
5. Run applicable local checks and record evidence.
6. Commit and push reviewable changes.
7. Open a PR against `main`.
8. Require successful PR CI on the final implementation head.
9. Hand off the exact final SHA to Gemini 3.1 Pro High / Antigravity for independent read-only review.
10. Remediate findings within scope and request re-review if the implementation SHA changes.
11. Merge only when AGENTS.md merge eligibility is satisfied.
12. After merge, verify `main` and final push CI, then perform governance closeout.

## Stop conditions

Escalate to the Human / Product Owner before the affected work if P1-006 would require any of the following:

- new provider/model/API authorization;
- paid service;
- production/public deployment;
- handling real/confidential research data;
- authentication/storage/retention policy change;
- breaking API/schema change;
- prompt/model/runtime semantic change;
- Claims generation/change;
- architecture change materially beyond presentation-layer UX polish;
- weakening an existing security, grounding, or legal-safety boundary.

Routine implementation, test, commit, push, PR, in-scope remediation, merge after eligible PASS, and post-merge closeout remain covered by AGENTS.md standing delegation.

## Implementation evidence

- Human authorization: **GRANTED** under `HUMAN-P1-006-UX-POLISH-2026-10-01`.
- Baseline main: `90ead2c0f26f17c617cfa71e6d7b3d16808d46e1`.
- Branch: `feat/p1-006-ux-polish`.
- Executable implementation SHA: `78772761f9a4081686db4977547ea89c96288f27`.
- PR: #50.
- Exact executable-SHA PR CI: `36831688815` — **SUCCESS**.
- Local backend regression: **442 passed / 3 skipped / 1 third-party deprecation warning**.
- PR CI backend regression: **443 passed / 2 skipped**.
- Python dependency consistency: **PASS**.
- Frontend lint: **PASS**.
- Frontend typecheck: **PASS**.
- Frontend production build: **PASS**.
- Synthetic Playwright: **19 passed** locally and in PR CI.
- Live flags: `RUN_OPENAI_LIVE_TESTS=0`; `RUN_OPENAI_DRAFT_LIVE_TESTS=0`.
- Provider/API calls: **NONE**.
- Independent review: Gemini 3.1 Pro High / Antigravity read-only — **PASS**, findings **NONE**, reviewed exact SHA `59c65deec60ae80e3ba6d28220466c2bdbfed815`; reviewer modified repository files: **NO**.
- Final exact-head PR CI `36832264774`: **SUCCESS** on `59c65deec60ae80e3ba6d28220466c2bdbfed815`.
- PR #50 merged at `659e46fa80321e037f384e0e8a09bbe90646da35`.
- Post-merge main CI `36833210498`: **SUCCESS** on exact merge SHA with backend **443 passed / 2 skipped**, Python dependency consistency **PASS**, frontend lint/typecheck/build **PASS**, synthetic Playwright **19 passed**, live flags **0 / 0**, provider/API calls **NONE**.
- MCP remains `PLANNED` with owner/approval reference unavailable; claim is **BLOCKED BY TOOL CAPABILITY** and no unsupported state is fabricated.

### Acceptance-criteria gap matrix

| AC | Pre-implementation gap | Implemented evidence | State |
| --- | --- | --- | --- |
| AC-01 | Existing 390 px coverage did not exercise the new five-stage treatment and all guarded operations. | Responsive five-stage progress CSS plus the retained 390 px edit/validate/export/error regression. | PASS |
| AC-02 | Button disabling depended on rerender timing; upload/export/validation feedback was uneven. | Immediate in-flight refs guard upload, process, validation and export; controls expose disabled and `aria-busy` state; operation callouts use live status semantics. | PASS |
| AC-03 | A JSON error message could disclose provider or internal path/stack details. | Client redacts provider, API-key, stack/trace and common internal-path patterns to safe local fallbacks; regression verifies provider/path text is absent. | PASS |
| AC-04 | Existing recovery behavior needed preservation. | Invalid upload retains document selection recovery; process failure clears the consumed source and requires re-upload. | PASS |
| AC-05 | Existing export recovery needed preservation. | Failed export creates no download, retains exact validated revision, and keeps `Return to results` retry flow. | PASS |
| AC-06 | Validation preserved context but lacked a direct recovery action. | Validation error retains the selected revision and exposes `Edit this revision`; regression uses that path. | PASS |
| AC-07 | Progress collapsed the intended sequence into three steps. | Visible `Upload → Analyze → Review / Edit → Validate → Export` progress with current/completed/upcoming semantics. | PASS |
| AC-08 | Existing keyboard and focus behavior needed preservation. | Roving tabs, keyboard-only workflow, focus-visible styling and error-heading focus remain covered. | PASS |
| AC-09 | Contract preservation required audit. | No backend, prompt, schema, model, runtime-policy, validation-rule or DOCX semantic change. | PASS |
| AC-10 | Safety notices required preservation. | Human-review, not-legal-advice and not-filing-ready wording remains in hero, draft and footer. | PASS |
| AC-11 | No deterministic duplicate-request test covered all four operations. | Controlled route promises verify one request, explicit busy state and duplicate blocking without fixed sleeps. | PASS |
| AC-12 | Final local and PR quality evidence was pending. | Local gates pass; PR CI `36831688815` succeeded on the executable implementation SHA. | PASS |
| AC-13 | Independent fixed-SHA review required. | Gemini 3.1 Pro High / Antigravity reviewed exact final SHA `59c65deec60ae80e3ba6d28220466c2bdbfed815`: PASS, findings NONE; reviewer modified tracked files NO. | PASS |

### Implementation changed files

- `frontend/src/app/page.tsx`
- `frontend/src/app/globals.css`
- `frontend/src/components/UploadPanel.tsx`
- `frontend/src/components/WorkflowProgress.tsx`
- `frontend/src/components/ResultWorkspace.tsx`
- `frontend/src/lib/api/client.ts`
- `frontend/src/lib/types/contracts.ts`
- `frontend/e2e/integration.spec.ts`
- `frontend/e2e/performance.spec.ts`
- `frontend/playwright.config.ts`

## Current handoff state

- P1-006 implementation is **CLOSED / COMPLETED — MERGED; CLOSEOUT REVIEW PENDING; MCP TOOL LIMITATION**.
- Reviewed exact SHA `59c65deec60ae80e3ba6d28220466c2bdbfed815`: Gemini 3.1 Pro High **PASS**, findings **NONE**.
- PR #50 merged at `659e46fa80321e037f384e0e8a09bbe90646da35`; post-merge main CI `36833210498` **SUCCESS**.
- MCP remains `PLANNED` / **BLOCKED BY TOOL CAPABILITY**; no fabricated `IMPLEMENTED`/`COMPLETED` state.
- BLK-003 remains **OPEN**.
- DEPLOY-001 remains **NOT AUTHORIZED**.
- EVAL-001 PRODUCT_RUNTIME remains **DEFERRED — AWAITING FUNDING**.
- Production deployment remains **NOT APPROVED / NOT PERFORMED**.
- Next gate: Gemini 3.1 Pro High fixed-SHA review of the documentation-only governance closeout PR; do not merge closeout before PASS.
