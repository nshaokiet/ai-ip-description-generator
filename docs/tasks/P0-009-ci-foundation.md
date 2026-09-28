# P0-009 — CI Foundation

| Field | Value |
|---|---|
| Task ID | P0-009 |
| Document version | 0.1.0 |
| Date | 28/09/2026 |
| Status | READY FOR INDEPENDENT IMPLEMENTATION REVIEW — not merged or completed |
| Approved baseline main | `bf837ef10622160fc76f80227e23f81830d69f76` |
| Implementation branch | `feat/p0-009-ci-foundation` |
| Human design approval | GRANTED |
| Implementation agent | GPT-6 Sol (Human-assigned role) |
| Independent reviewer | Gemini 3.1 Pro High — review pending |
| Final merge authority | Human / Product Owner |

Version history: 0.1.0 (28/09/2026, Codex) records the approved CI design,
the narrow Playwright portability decision, implementation boundaries and local
validation for independent review. No production contract or product behavior
change; breaking change **No**.

## Approved design and Human decisions

Human approved a single `build-and-test` job on `ubuntu-latest` for
`pull_request` and `push` targeting `main`, with `contents: read` permissions.
The approved baseline is `bf837ef10622160fc76f80227e23f81830d69f76`:
Human reconciled the earlier baseline because this direct-child commit changed
only one README sentence. It did not change application code, tests,
dependencies, prompts, schemas, templates or runtime configuration.

The job uses Python **3.12**, Node **24.18.0**, official checkout/setup
actions, pip/npm dependency caches, pinned dependency files, and the existing
offline quality gates:

```text
python -m pytest tests -q -p no:cacheprovider
npm ci
npm run lint
npm run build
npx playwright install --with-deps chromium
npm run test:e2e
```

The workflow explicitly sets `RUN_OPENAI_LIVE_TESTS=0` and
`RUN_OPENAI_DRAFT_LIVE_TESTS=0`; it supplies no provider secret. CI bootstrap
may fetch tool/dependency/browser packages, but tests intentionally use the
offline/synthetic backend and make no provider API call. A genuine failure in
any required gate fails the job; historical test counts are not CI thresholds.

Human additionally approved one narrow exception for
`frontend/playwright.config.ts`: `PLAYWRIGHT_PYTHON` selects an explicit
interpreter for Playwright's offline Uvicorn server. With the variable unset,
the existing repository `.venv/Scripts/python.exe` (Windows) or
`.venv/bin/python` (Linux/macOS) remains the default. CI sets
`PLAYWRIGHT_PYTHON=python` to use the Python 3.12 interpreter installed on
PATH by `actions/setup-python`; CI does **not** create/cache a repository
`.venv`. The backend command, offline harness and
`reuseExistingServer: false` remain unchanged. This is interpreter
portability only: application behavior and test expectations are unchanged.

## Implementation and local evidence

| Gate | Evidence |
|---|---|
| Workflow syntax/structure | Local `js-yaml` parse PASS; asserted both `main` triggers, one job, read-only permission, disabled live flags, and Playwright override. GitHub Actions execution awaits the remote PR/main trigger. |
| Backend regression | Existing Python 3.12.10 `.venv` ran the canonical pytest arguments: **380 passed, 3 skipped, 1 warning**, exit 0. Local system `python` points to 3.14, so the approved 3.12 interpreter was invoked explicitly. |
| Frontend install/lint/build | Node **v24.18.0**, npm **11.16.0**; `npm ci` installed 348 packages, lint PASS, build PASS. |
| Chromium install | `npx playwright install --with-deps chromium` PASS on retry outside the local sandbox after Windows WMI access was denied. The GitHub `ubuntu-latest` job uses the same approved command. |
| Playwright override and full E2E | With local Python 3.12 active and `PLAYWRIGHT_PYTHON=python`, the offline Uvicorn server started; full suite **11 passed (3.7m)**, exit 0. The identified test-owned backend/frontend processes were stopped after the Windows teardown stalled; the runner then exited 0. |
| Local default | With `PLAYWRIGHT_PYTHON` unset, the config loads and lists all 11 tests; the unchanged `path.join` fallback still selects repository `.venv` by platform. |
| Provider isolation | No `OPENAI_API_KEY` in the local test environment; both live flags explicitly set to `0`; Playwright uses `tests.e2e.offline_backend`. No provider API calls were intentionally made. |

No test expectation, offline backend harness, application code, dependency
manifest, lockfile, prompt, schema or template was changed. The only test
configuration change is the Human-approved interpreter selection. No
Supabase, Vercel/Railway deployment, provider abstraction, async job,
EVAL-001 or SEC-001 implementation is included. BLK-003 remains **OPEN**;
live-provider smoke remains **UNVALIDATED / DEFERRED**. This CI task does not
grant production, public-deployment, confidential-data or legal/filing
readiness. Independent implementation review and Human merge approval are
still pending.

## Handoff

```text
Task ID: P0-009
Agent: GPT-6 Sol (Human-assigned implementation role)
Reviewer: Gemini 3.1 Pro High — independent implementation review pending
Status: READY FOR INDEPENDENT IMPLEMENTATION REVIEW; not merged
Version: Task record 0.1.0; baseline bf837ef10622160fc76f80227e23f81830d69f76; final implementation SHA in Git handoff
Work completed: Single-job provider-free CI workflow and approved Playwright interpreter override.
Files affected: .github/workflows/ci.yml; frontend/playwright.config.ts; docs/tasks/P0-009-ci-foundation.md; minimal current-state governance files.
Evidence checked: Backend 380 passed/3 skipped; npm ci/lint/build PASS; Playwright 11 passed; YAML structure PASS; git diff --check before commit.
Findings: No local quality-gate failure; independent review not yet performed.
Decisions: Human approved CI design, new baseline and narrow PLAYWRIGHT_PYTHON portability change.
Issues: GitHub Actions run and independent review pending; BLK-003 OPEN; live-provider smoke deferred.
Security impact: No provider credentials or calls; read-only workflow token; synthetic/offline tests only.
Recommended next action: GEMINI 3.1 PRO HIGH — INDEPENDENT IMPLEMENTATION REVIEW.
```
