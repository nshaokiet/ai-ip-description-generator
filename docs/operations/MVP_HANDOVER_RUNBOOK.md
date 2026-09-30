# MVP handover runbook — local/synthetic boundary

| Field | Value |
|---|---|
| Task | P0-008 — MVP Release & Handover Readiness |
| Runbook version | 0.1.2 (post-merge closeout; no product change) |
| Date | 28/09/2026 |
| Repository | Private `nshaokiet/ai-ip-description-generator` |
| Approved specification | [P0-008 v0.1.0](../tasks/P0-008-mvp-release-handover-readiness.md) at `52d3c62d3741e9e7abc98c2bf2b300b4885f316c` |
| Baseline main | `8142692c6e92670b4b09996d733f93c409e93e49` |
| Handover classification | **MVP HANDOVER READY — LOCAL/SYNTHETIC** — Human accepted after independent implementation review; see final closeout below |
| BLK-003 | **OPEN** |

This is the single operational authority for P0-008 local setup, verification,
limitations and handover evidence. The generated patent-description DOCX is a
draft requiring Human/SHTT specialist review, not legal advice or filing-ready
output. Neither a local/synthetic handover nor a `REVIEWED` browser-session flag
is a production, legal or formal Human approval.

Version history: 0.1.0 (28/09/2026, Codex) created the setup/acceptance
runbook; 0.1.1 (28/09/2026, Codex) records fresh isolated verification and
observed Windows launcher/server-teardown caveats for P0-008; 0.1.2
(28/09/2026, Codex) records the final review, Human handover acceptance and
implementation merge without changing the operational procedure. No breaking
change or approved technical contract change.

## Capability and boundary

| Area | Implemented local capability | Not established |
|---|---|---|
| Input | One text-based PDF (10 MiB/50-page limit) or DOCX (10 MiB) per run; safe validation and deterministic parsing/evidence units | OCR/scanned-only PDF, arbitrary DOCX pagination, confidential-data handling |
| Processing | APP-003 orchestrates extraction, validation, draft generation and source cleanup. Normal process uses provider-backed runtimes. | Live-provider availability/correctness; semantic quality on real papers |
| UI | P0-005/006 Next frontend: upload, grounded analysis, draft display, session-only edit/revisions/review, backend validation and exact DOCX export | Login, durable revision/audit store, formal approval, multi-user isolation |
| Offline E2E | P0-007 Playwright runs real FastAPI upload/parsing/validation/DOCX renderer and real Next/browser/download with injected fake AI runtimes and synthetic fixtures | Actual model response quality, production auth/storage/retention, public URL |

Claims generation, prior-art search, patentability/novelty scoring, fine-tuning,
multi-agent runtime and automatic patent filing remain outside MVP. No public
deployment, staging URL or production SLA has been established. Vercel/Railway
are proposed future directions only, not deployed or approved services.

## Prerequisites and isolated setup

Use an isolated fresh clone or temporary worktree at the fixed implementation
commit being handed over. Do not reuse an existing developer `.venv` or
`node_modules` as the sole reproducibility evidence; do not reset/delete an
existing workspace. On Windows, use Python 3.12. P0-007 historically verified
Node 24.18.0/npm 11.16.0; no exact Node/npm version is repo-enforced. Confirm
your chosen Node version satisfies the locked Next/Playwright requirements.

Record `git rev-parse HEAD`, `git status --short`, OS, `py -3.12 --version`,
`.\.venv\Scripts\python.exe -m pip --version`, `node --version` and
`npm --version`. In PowerShell from the fresh repository root:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt -r tests/requirements.txt
cd frontend
npm ci
npx playwright install chromium
```

For POSIX, substitute `python3.12 -m venv .venv` and `.venv/bin/python`.
`npm ci` must use the committed `frontend/package-lock.json`; do not upgrade
dependencies to make an installation pass. A failed install is **FAIL**, not an
exception silently counted as PASS. `npx playwright install chromium` supplies
the browser for the synthetic smoke. Do not place a real provider key in the
fresh environment.

On the verified Windows host, `py -3.12` failed because the launcher registered
only Python 3.14 even though Python 3.12.10 was installed. The fresh venv was
created with that *installed* 3.12 executable instead; no existing venv was
reused. A recipient whose launcher lacks 3.12 must locate a trusted installed
Python 3.12 interpreter and invoke its `python.exe -m venv .venv` (or install
3.12); a machine-specific path is not part of the portable command.

## Environment variables and secrets

`.env.example` is a sample. Backend `Settings.from_environment()` reads the
**process environment**; it does not automatically load that file. Keep real
secrets out of Git and the frontend. Local/synthetic acceptance needs no
`OPENAI_API_KEY`.

| Variable | Role | Handover setting |
|---|---|---|
| `AI_IP_ENABLE_LOCAL_ORCHESTRATION_API` | Backend flag, default `0`; adds local metadata/process/validation/export routes, not authentication. | `0` for basic normal startup; offline harness injects enabled settings. |
| `AI_IP_UPLOAD_ROOT` | Optional backend upload root; defaults to OS temp `ai-ip-generator/uploads`. | If set, use an isolated path outside repo; not a production private store. |
| `BACKEND_URL` | Next server-side `/backend/*` rewrite target, default `http://127.0.0.1:8000`. | Default or same loopback URL; not a `NEXT_PUBLIC_*` secret. |
| `OPENAI_API_KEY` | Backend provider credential for normal provider-backed processing. | **Absent** for P0-008 acceptance. Never expose or print it. |
| `OPENAI_TIMEOUT_SECONDS`, `OPENAI_MAX_OUTPUT_TOKENS` | Optional approved extraction runtime settings, defaults `180`/`48000`. | Not required offline; do not change policy. |
| `OPENAI_DRAFT_TIMEOUT_SECONDS`, `OPENAI_DRAFT_MAX_OUTPUT_TOKENS` | Optional approved draft settings, defaults `240`/`64000`. | Not required offline; do not change policy. |
| `RUN_OPENAI_LIVE_TESTS`, `RUN_OPENAI_DRAFT_LIVE_TESTS` | Opt-in live-test flags, default `0`. | Explicitly keep `0`; do not run live tests. |
| `NEXT_PUBLIC_API_BASE_URL`, `SUPABASE_*` | Not used by the current local path; removed from sample. | Not prerequisites; no client-side provider key. |

## Normal local startup and shutdown

After installing the prerequisites below, the recommended P1-004 developer path
starts both existing servers from the repository root:

```powershell
.\.venv\Scripts\python.exe tools\local_dev.py
```

On POSIX, use `.venv/bin/python tools/local_dev.py`.

The launcher performs bounded backend, frontend and proxy readiness checks and
keeps both loopback-only process groups attached. Press Ctrl+C once; it stops
only the exact process groups it created. `--check` validates prerequisites and
ports without starting servers. An occupied port is an error and the launcher
does not terminate its pre-existing owner. This tooling does not call a provider,
does not require `OPENAI_API_KEY`, rejects enabled live-test flags, and does not
silently opt into the local orchestration API.

The two-terminal procedure below remains the manual troubleshooting fallback.

Use two terminals after fresh installation. In terminal A, from repo root:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

Check `http://127.0.0.1:8000/health` returns `{"status":"ok"}`. Default
routes are health/upload, not a full offline AI workflow. In terminal B, from
`frontend/`:

```powershell
npm run dev
```

Check `http://localhost:3000` and
`http://localhost:3000/backend/health`. The latter must proxy to the backend
through the same-origin Next rewrite. A healthy frontend/proxy does **not**
prove `/process` or real-provider calls. If normal local orchestration is
enabled, processing uses the actual provider runtimes; do not exercise it
without separate provider/data authorization. Stop both **controlled**
terminals with Ctrl+C and verify ports 8000 and 3106 are free before E2E.
Never kill an unidentified process to free a port.

Observed on the verified host: plain `npm run dev` served localhost but also
listened on `0.0.0.0:3000`. For a loopback-only manual session, prefer
`npm run dev -- --hostname 127.0.0.1` and use
`http://127.0.0.1:3000`; this is a launch option, not a production-security
feature (`npx next dev --help` confirms the hostname option and default
`0.0.0.0`). The automated shell's Ctrl+C did not stop the two owned servers;
their exact PIDs were identified and stopped before E2E, with ports checked
free. A normal interactive operator should first use Ctrl+C.

## Synthetic/offline tests and final smoke

From the fresh `frontend/` after stopping the normal servers:

```powershell
npm run lint
npm run build
npm run test:e2e -- --grep "PDF session: cancel, immutable save, validate, review and exact UNREVIEWED export"
```

`frontend/playwright.config.ts` owns backend `127.0.0.1:8000` and built
frontend `127.0.0.1:3106` (`reuseExistingServer: false`). Its backend is
`tests/e2e/offline_backend.py`, **not** ordinary `backend.app.main:app`; it
injects fake extraction/draft runtimes but retains the actual FastAPI boundary,
upload, parsing, validation, renderer and browser DOCX download. The browser
case checks selected revision content in the downloaded DOCX, rejects stale or
cancelled text, and confirms draft/author-confirmation notices. This is an
offline technical oracle, not semantic AI quality evidence. It uses only
synthetic data and must make zero provider calls.

| Other command | Directory | When to run |
|---|---|---|
| `.\.venv\Scripts\python.exe -m pytest tests/backend/test_health.py tests/backend/test_document_upload.py tests/backend/test_local_orchestration_api.py -q -p no:cacheprovider` | Repo root | Targeted diagnosis after relevant backend change or startup/API failure. |
| `.\.venv\Scripts\python.exe -m pytest tests -q -p no:cacheprovider` | Repo root | Full offline regression if backend behavior changes or a finding cannot be bounded. |
| `npm run test:e2e` | `frontend/` | Full browser regression if product/harness behavior changes or targeted smoke fails. |

Set `RUN_OPENAI_LIVE_TESTS=0`, `RUN_OPENAI_DRAFT_LIVE_TESTS=0` and leave
`OPENAI_API_KEY` absent for offline Python checks. No new production code,
test harness, dependency or build behavior is planned in P0-008, so historical
P0-007 regression may be reused **with its provenance**, while fresh install,
normal startup/proxy, lint/build and one PDF smoke remain mandatory.

## Temporary data, cleanup and limitations

Backend upload root defaults to OS temp `ai-ip-generator/uploads`, optionally
overridden by `AI_IP_UPLOAD_ROOT`. Export root defaults to OS temp
`ai-ip-generator/exports` (no environment override in current settings).
Downstream processing attempts source deletion in a `finally` path; upload
TTL sweep is a fallback (one hour); DOCX response cleanup is best effort.
Open handles and forced shutdown can leave residual temporary files. The E2E
harness uses isolated temporary roots and count-only storage inspection.
Do not claim guaranteed immediate cleanup, secure private production storage,
or a production retention/deletion policy.

Deterministic validation checks schema, source pointers and rules but cannot
establish semantic support of edited prose. Browser edits, revision history and
review flags are session-only and lost on reload/reset. `UNREVIEWED` can be
exported as a draft. No OCR, Claims, prior-art search, scoring, production
auth/tenant isolation, durable storage, public deployment or production SLA
is provided. Live-provider smoke remains **UNVALIDATED / DEFERRED**. No
real/confidential research paper or provider API call is authorized here.
BLK-003 remains **OPEN** for production authentication, private storage and
retention/deletion. Human/SHTT specialist review is mandatory before any use
of generated output.

## Handover evidence and decision gates

Historical evidence is **not** a fresh P0-008 rerun. P0-007 accepted
implementation `bd43a7e9875537c4f5ebdee53626542a11500636`, final
test-code `2638c620a36e6fb4016ed2efaeb788446a5b2eff`, merge
`26b12450284b9331f79fbbffe3220d93e40c0916` and closeout
`8142692c6e92670b4b09996d733f93c409e93e49`: targeted backend
**194 passed/1 skipped**; full backend **380 passed/3 skipped**; independent
frontend lint/build **PASS**; Playwright **11/11 PASS**; PDF and DOCX
stability **3/3 each PASS**; cleanup **PASS**. See
[P0-007 task evidence](../tasks/P0-007-mvp-e2e-validation-stabilization.md)
and [review log](02_GEMINI_REVIEW_LOG.md). No provider calls or confidential
data were used in those historical tests.

| Fresh P0-008 gate | Result / evidence |
|---|---|
| Isolated SHA, OS/tool versions and clean install | **PASS at `737edec7a134620285b368a9c57d08aa63829a0a`** in a new temporary detached worktree. Windows NT `10.0.26200.0`; Python `3.12.10`; pip `25.0.1`; Node `v24.18.0`; npm `11.16.0`. New `.venv`, pinned pip install, `npm ci` (348 packages) and Playwright Chromium install all succeeded. The `py -3.12` launcher discrepancy is documented above. |
| Normal backend, frontend and proxy | **PASS at `737edec`**: ordinary `uvicorn` startup; `/health` returned `{"status":"ok"}`; `npm run dev` page HTTP 200; `/backend/health` returned `{"status":"ok"}`. Plain Next dev bound all interfaces; see loopback recommendation above. No normal provider-dependent `/process` call was made. |
| Fresh lint/build and targeted PDF browser/DOCX smoke | **PASS at `737edec`**: `npm run lint` exit 0, `npm run build` exit 0, exact grep command above reported `1 passed (2.3m)` with test case `15.7s`. It downloaded and inspected the exact selected DOCX (test oracle in `frontend/e2e/integration.spec.ts:118-175`). Playwright shutdown stalled after the case passed; only its identified child server PIDs were stopped, then runner exited 0 and ports 8000/3106 were free. |
| Exact AC-01…AC-16 implementation self-check | PENDING evidence addendum in P0-008 task |
| Independent implementation review at fixed SHA | NOT STARTED; no verdict or findings claimed |
| Human acceptance of local/synthetic handover | NOT GIVEN; proposed classification remains ungranted |

Fresh worktree tracked files stayed clean. The Next dev process generated
untracked `frontend/AGENTS.md` and `frontend/CLAUDE.md` **in the isolated
worktree**; neither was staged or copied into the implementation branch. The
implementation branch's pre-existing untracked patch/scratch and frontend
agent files likewise remain untouched. There was no provider credential in
the fresh shell, both opt-in live flags were unset (default false), the E2E
backend injected offline fake runtimes, and browser requests to non-loopback
hosts were aborted by the test helper. This supports provider calls **NONE**
and synthetic data only; it does not prove live-model behavior.

Project Orchestrator MCP reconciliation was **BLOCKED BY TOOL CAPABILITY**:
its existing P0-008 record remains `Final hardening` / `PLANNED`, with no
reviewed-spec SHA/decision or owner/lease. Human explicitly approved a
**non-blocking governance exception** to implement using authoritative Git
specification/review evidence. MCP and Git states are not synchronized; no
MCP repair, lease or approval state is fabricated. A safe administrative
metadata-update capability is a future tooling improvement, not P0-008 work.

After implementation self-check, Antigravity independently reviews a fixed
implementation SHA. Only a later Human/Product Owner acceptance can grant
`MVP HANDOVER READY — LOCAL/SYNTHETIC`; it still does not grant production,
public deployment, confidential-data use, legal/filing readiness or live
provider validation. Preserve future sequence: **P0-009** offline CI →
**EVAL-001** semantic quality → **SEC-001** production security/BLK-003 →
UX hardening as separately approved. Deployment/staging requires a separate
Human decision and task.

## Final P0-008 closeout — supersedes pending gates above

The pending independent-review and Human-acceptance statements in the historical
handover evidence above describe the pre-review state. At final closeout,
P0-008 is **CLOSED / COMPLETED — MERGED**, with specification review **PASS**,
independent implementation review **PASS** by Google Antigravity using
**Gemini 1.5 Pro (Advanced Agentic Coding)**, findings **NONE**, AC-01…AC-15
**PASS** at review time, and AC-16 **PASS** after Human / Product Owner
handover acceptance **GRANTED**. The
reviewed implementation SHA is
`956ba93048536d2a54d120752ade5540ecc0d901`; its implementation merge
SHA is `e6b2f665f6334047ec420c49d2097732f2917354`.

The accepted classification is **MVP HANDOVER READY — LOCAL/SYNTHETIC** only.
BLK-003 remains **OPEN**; live-provider smoke is **UNVALIDATED / DEFERRED**;
public deployment was **NOT PERFORMED**; production readiness is **NO**;
real/confidential-data authorization is **NO**. Synthetic evidence is not
real-paper semantic-quality or legal/filing validation.

Project Orchestrator MCP reconciliation remains **BLOCKED BY TOOL CAPABILITY**.
Human approved a **non-blocking governance exception** for the Git-evidenced
workflow. This closeout does not claim MCP task completion, approval, updated
metadata, owner, lease or synchronization.
