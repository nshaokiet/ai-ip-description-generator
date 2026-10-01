# P1-006 — UX Polish

## Metadata

| Field | Value |
| --- | --- |
| Task | P1-006 |
| Status | **AUTHORIZED FOR IMPLEMENTATION — SPECIFICATION CREATED** |
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

## Initial handoff state

- Human authorization: **GRANTED** under `HUMAN-P1-006-UX-POLISH-2026-10-01`.
- Baseline main: `90ead2c0f26f17c617cfa71e6d7b3d16808d46e1`.
- Branch: `feat/p1-006-ux-polish`.
- Implementation: **NOT STARTED** at specification creation.
- Independent review: **NOT STARTED**.
- PR: **NOT OPENED**.
- CI evidence for P1-006 implementation: **NONE YET**.
- BLK-003 remains **OPEN**.
- DEPLOY-001 remains **NOT AUTHORIZED**.
- Production deployment remains **NOT APPROVED / NOT PERFORMED**.
