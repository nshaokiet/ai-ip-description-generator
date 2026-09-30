# P1-004 — Developer Experience / One-command Local Run

| Field | Value |
|---|---|
| Task | P1-004 |
| Status | IMPLEMENTED — REVIEW PENDING |
| Authorization | `HUMAN-P1-004-ONE-COMMAND-LOCAL-RUN-2026-09-30` |
| Baseline | `208f17344b429c50ffa181d986511fc9f120efce` |
| Branch | `feat/p1-004-one-command-local-run` |
| Owner | Codex |
| Reviewer gate | Gemini 3.1 Pro High fixed-SHA review — PENDING |
| Classification | MVP COMPLETE — LOCAL/SYNTHETIC |

## Scope and exclusions

P1-004 adds a Python 3.12 stdlib launcher for the existing FastAPI and Next.js
development servers, deterministic readiness checks, safe port validation,
launcher-owned process cleanup, offline regressions, and developer documentation.

Production deployment/authentication, tenant isolation, private production
storage, retention/deletion policy, providers/paid services, prompt/schema/model
or runtime-policy changes, real/confidential data, Claims, P1-005, P1-006 and
DEPLOY-001 are excluded. BLK-003 remains OPEN. EVAL-001 PRODUCT_RUNTIME remains
DEFERRED — AWAITING FUNDING. Production remains NOT APPROVED / NOT PERFORMED.

## Pre-implementation DevEx findings

| Area | Evidence before P1-004 | Disposition |
|---|---|---|
| Startup | Runbook required separate uvicorn and npm terminals | Add one root command; preserve manual fallback |
| Frontend binding | Plain Next dev historically bound `0.0.0.0` | Always pass `--hostname 127.0.0.1` |
| Readiness | URLs were manually checked | Poll backend, frontend and proxy with finite timeouts |
| Ports | Operators manually checked ports | Refuse occupied 8000/3000 before any spawn; never kill owner |
| Windows teardown | Historical automated Ctrl+C left child servers | Create process groups and target only tracked root PIDs/trees |
| Provider boundary | Normal startup needs no key, but processing is provider-backed when opt-in API is enabled | Keep API opt-in default `0`; reject enabled live-test flags; do not process data |

## Acceptance criteria

AC-01 through AC-23 are the authorized criteria in the Human task instruction.
The implementation maps them as follows: one-command startup and loopback command
construction (AC-01–03); real HTTP health/frontend/proxy polling and bounded
timeouts (AC-04–07); pre-spawn port refusal and owned cleanup (AC-08–13);
environment/provider/dependency safety (AC-14–18); pytest integration and docs
(AC-19–20); scope/boundary preservation (AC-21–23).

## Implementation evidence

- Launcher: `tools/local_dev.py`; Python stdlib only.
- Command: `.\.venv\Scripts\python.exe tools\local_dev.py`.
- Backend: current interpreter runs uvicorn on `127.0.0.1:8000`.
- Frontend: npm runs Next dev with explicit `127.0.0.1:3000`.
- Readiness: exact backend health JSON, frontend HTTP success, then proxy health.
- Ownership: Windows `CREATE_NEW_PROCESS_GROUP` + exact tracked PID tree cleanup;
  POSIX new sessions + signals to exact owned process-group IDs.
- Safety: port probes occur before spawn and never identify/terminate an existing
  owner; startup errors trigger cleanup of only `owned` children.
- Environment: `OPENAI_API_KEY` is optional/unused; live flags must be `0`;
  local orchestration remains default `0` and only an explicit valid caller value
  is preserved.

## Test evidence

Local implementation verification on Windows 30/09/2026:

| Gate | Result |
|---|---|
| Targeted launcher regression | **12 passed** |
| Full offline pytest | **430 passed, 3 skipped, 1 dependency warning** |
| `pip check` | **PASS** — no broken requirements |
| Frontend lint / typecheck / build | **PASS / PASS / PASS** |
| Synthetic Playwright | **17 passed**; known post-test server shutdown stall required exact owned web-server PID cleanup, then runner exited 0 |
| Real Windows one-command smoke | **PASS** — backend, frontend and proxy readiness; programmatic Ctrl+Break produced launcher exit 0; ports 8000/3000 free afterward |
| Live flags | `RUN_OPENAI_LIVE_TESTS=0`; `RUN_OPENAI_DRAFT_LIVE_TESTS=0` |
| Provider/API calls | **NONE** |

Exact implementation SHA and PR CI remain pending until the implementation is
committed and pushed.

## Implementation self-review findings matrix

| Area | Severity | Evidence / result |
|---|---|---|
| Launcher architecture | NOTE | Single stdlib file; no dependency/toolchain expansion |
| Process ownership | NOTE | Only objects appended after successful spawn are eligible for cleanup |
| Windows process tree shutdown | MEDIUM — RESOLVED | First programmatic Ctrl+Break ended the launcher with `0xC000013A` and left children; explicit `SIGBREAK` handling was added, then the real smoke exited 0 with both ports free |
| POSIX behavior | MEDIUM — RESOLVED | Initial construction referenced Windows-unavailable `os.killpg`/`SIGKILL`; lookup/constants were made platform-safe; POSIX fake asserts SIGINT → SIGTERM → SIGKILL against the owned process group |
| Port collision handling | NOTE | Both loopback ports validated before first spawn; no PID kill path in validation |
| Readiness semantics | NOTE | HTTP response checks, not process existence alone |
| Timeout behavior | NOTE | Per-readiness finite timeout and bounded graceful shutdown |
| Environment/provider safety | NOTE | No provider call/key requirement; live flags constrained to `0` |
| Developer ergonomics | NOTE | One root command, concise stages, actionable failures, `--check` |
| Test determinism | NOTE | Process/HTTP failure regressions use fakes; real smoke is separate evidence |
| Documentation accuracy | NOTE | Recommended path added; historical/manual instructions retained |

No evidence-backed CRITICAL, HIGH, MEDIUM or LOW finding remains open after the
two remediations above. Independent review is not claimed.

## Governance boundary

Provider/API calls: **NONE**. BLK-003: **OPEN**. P1-005, P1-006 and DEPLOY-001:
**PLANNED / NOT AUTHORIZED**. P1-004 must not be marked Completed before the
fixed-SHA independent review, merge, successful main CI and closeout evidence.
