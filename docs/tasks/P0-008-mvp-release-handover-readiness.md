# P0-008 — MVP Release & Handover Readiness Specification

## Metadata and version history

| Field | Value |
|---|---|
| Task ID | P0-008 |
| Specification version | 0.1.0 |
| Status | Specification v0.1.0 reviewed PASS and Human-approved for implementation; implementation self-check READY FOR INDEPENDENT IMPLEMENTATION REVIEW; handover classification NOT GRANTED |
| Owner / final decision authority | Human / Product Owner |
| Author | Codex |
| Independent specification reviewer | Google Antigravity; profile Google Antigravity (Advanced Agentic Coding); PASS, AC-01…AC-16 PASS, findings NONE; underlying model not evidenced |
| Independent implementation reviewer | Pending separate fixed-SHA review; no verdict claimed |
| Implementation evidence revision | 0.1.1; approved technical specification remains v0.1.0 |
| Date | 28/09/2026 |
| Fixed audit baseline | `main` at `8142692c6e92670b4b09996d733f93c409e93e49` |
| Branch | `docs/p0-008-mvp-release-handover-readiness-spec` |
| Confidentiality | Internal; only synthetic inputs are permitted for this task |

| From | To | Date | Author | Change | Reason | Related decision | Breaking change |
|---|---|---|---|---|---|---|---|
| None | 0.1.0 | 28/09/2026 | Codex | Define targeted release-readiness audit, documentation reconciliation, fresh-environment and synthetic handover gates | Specify a truthful local/synthetic baseline without implementing P0-008 or claiming production readiness | P0-007 closeout at `8142692c6e92670b4b09996d733f93c409e93e49`; BLK-003 OPEN | No |
| 0.1.0 | 0.1.1 evidence addendum | 28/09/2026 | Codex | Record specification review PASS/Human implementation approval, documentation/runbook changes and fresh isolated self-check; do not change AC wording or technical requirements | Fixed-SHA implementation handoff for independent review | `REV-P0-008-SPECIFICATION`; Human-approved MCP exception; BLK-003 OPEN | No |
| 0.1.1 evidence addendum | 0.1.2 closeout addendum | 28/09/2026 | Codex | Record independent implementation PASS, Human handover acceptance and implementation merge; preserve specification v0.1.0 | Close P0-008 local/synthetic handover lifecycle without a production claim | `REV-P0-008-IMPLEMENTATION`; merge `e6b2f665f6334047ec420c49d2097732f2917354`; BLK-003 OPEN | No |

## 1. Purpose and exact classification

The *proposed*, not yet attained, successful classification is **MVP HANDOVER READY — LOCAL/SYNTHETIC**. It means a technically competent recipient can reproduce the pinned local environment, start the documented services, exercise the existing PDF/DOCX path with synthetic/offline runtimes, verify the handover evidence, and understand every known limit. It is an engineering/handover baseline, not a production release. P0-008 implementation, independent review, Human acceptance and closeout remain future gates.

The classification **does not** prove live-provider availability or output quality, semantic support on real papers, confidential-data safety, authenticated multi-user operation, production storage/retention/deletion, deployment, legal suitability, patentability or filing readiness. Forbidden synonyms for this classification include **Production Ready**, **Production Approved**, **Ready for confidential data**, **Fully validated AI quality**, **Filing Ready**, and **USPTO Ready**. Every user-facing description must continue to call generated content a draft requiring Human/specialist review. Session `REVIEWED` is not formal approval; Claims remain outside MVP.

BLK-003 remains **OPEN** for production authentication, private production storage and retention/deletion policy. Live-provider smoke remains **UNVALIDATED / DEFERRED**. No real/confidential research input, provider API call, production deployment or production-readiness claim is authorized by this specification. These limitations do not prevent a future *local/synthetic* handover classification once its own gates pass.

## 2. Audit scope, provenance and fixed capability baseline

This specification is a read-only, targeted audit of repository state at the fixed main SHA. No tests, dependency installs, startup smoke or implementation were run for this specification. Historical results are recorded as historical, not converted into fresh P0-008 results. Inspected: root/component/test READMEs, folder map, AGENTS, Project Context, System Specification, workflow, operations control/review/protocol, `.env.example`, pinned backend/frontend/test dependencies and lockfile, backend settings/app factory, Next rewrite/API client, Playwright config/browser cases and offline harness, P0-006/P0-007 evidence, `.gitignore`, `.github/`, and relevant tools documentation. Only local setup, release and privacy-relevant code was inspected.

| Completed capability | Existing evidence / boundary |
|---|---|
| SPEC-001/002/003 | Approved baselines; later factual status prose may be stale, but approved rules/technical requirements remain unchanged. |
| AI-001/002/003 and DOC-001 | Output Schema v1, Extraction Prompt v1, Patent Draft Contract/Prompt v1 and claim-free DOCX template/renderer are merged; no contract redesign here. |
| APP-001/002 and AI-RUNTIME-001/002 | Secure local PDF/DOCX upload, deterministic source units/evidence and internal extraction/draft runtimes are merged. Live provider smoke is still deferred. |
| APP-003, P0-005, P0-006 | Internal orchestration, frontend MVP and local frontend/backend integration are merged; this is not production auth/storage. |
| P0-007 | CLOSED / COMPLETED — MERGED: implementation merge `26b12450284b9331f79fbbffe3220d93e40c0916`; post-merge closeout `8142692c6e92670b4b09996d733f93c409e93e49`; independent Google Antigravity (Advanced Agentic Coding) review PASS, findings NONE, AC-01…AC-16 PASS. |

P0-007 accepted implementation/handoff SHA is `bd43a7e9875537c4f5ebdee53626542a11500636`; final test-code SHA is `2638c620a36e6fb4016ed2efaeb788446a5b2eff`. Historical targeted backend: **194 passed / 1 skipped**; full offline backend: **380 passed / 3 skipped** (accepted by reviewer without independent rerun because no production Python code changed); independent frontend lint/build **PASS**, Playwright **11/11 PASS**; PDF and DOCX stability **3/3 each PASS**; source/export cleanup **PASS**; provider API calls **NONE**; real/confidential data **NONE**. Reuse only with these SHA/provenance qualifications. Do not rerun or invalidate this evidence merely to write this specification.

Operational-state audit: Project Orchestrator MCP currently reports task `P0-008` as `PLANNED` with the older title “Final hardening”, no approval reference, owner or lease; its manually recorded quota decision is `CONTINUE`. MCP state is lower-priority operational evidence, not authority to override this Human-requested Git specification. No MCP claim or implementation transition is made here. Before a later implementation claim, Human/MCP administration must align its task title/scope and approval reference with the reviewed specification; do not fabricate approval or silently treat `PLANNED` as `APPROVED`. This is coordination reconciliation, not a new product/security decision.

## 3. Actual local topology and configuration audit

| Concern | Observed repository behavior | P0-008 documentation rule |
|---|---|---|
| Python / dependencies | Documentation targets Python 3.12; `backend/requirements.txt` pins runtime packages, `tests/requirements.txt` pins pytest/jsonschema. No repository Python-version file exists. | Document Python 3.12 and a new isolated virtual environment; install both requirement files for testing. Record actual interpreter/pip versions. Do not embed a developer-specific Python path. |
| Node / lock | `frontend/package.json` pins Next 16.3.6, React 19.3.0, Playwright 1.63.0; lockfile v3 is committed. Next lock entry says Node >=20.9.0, but root package has no `engines` or `.nvmrc`. P0-007 used Node 24.18.0/npm 11.16.0. | Recommend the historically verified Node 24/npm 11 pair for handover; disclose that it is a verified environment, not a repo-enforced exact requirement. Use `npm ci` from `frontend/`. Other supported versions need their own verification, not an invented guarantee. |
| Normal backend | `backend/app/main.py` creates `app`; `backend/app/core/config.py` defaults local orchestration flag to off. `uvicorn backend.app.main:app --host 127.0.0.1 --port 8000` runs from repository root. | Health/upload can run without an API key. With `AI_IP_ENABLE_LOCAL_ORCHESTRATION_API=1`, process routes exist, but the ordinary process path uses real provider runtimes; without a key it cannot complete that path. Never describe ordinary startup as an offline full-workflow demo. The flag is not authentication. |
| Normal frontend | `frontend/next.config.ts` rewrites same-origin `/backend/*` to server-side `BACKEND_URL`, default `http://127.0.0.1:8000`; `frontend/src/lib/api/client.ts` uses `/backend`. `npm run dev` runs from `frontend/` and normally serves `http://localhost:3000`. | Start backend before frontend for manual local checks; verify `/health` and `/backend/health`. No `NEXT_PUBLIC_*` backend URL or secret is needed. Document port conflicts and stop both terminals with Ctrl+C; do not kill an unidentified process. |
| Offline full workflow | `tests/e2e/offline_backend.py` injects synthetic extraction/draft runtimes into the real FastAPI app, with real upload, parsing, validation and DOCX rendering. `frontend/playwright.config.ts` owns backend `127.0.0.1:8000` and built Next frontend `127.0.0.1:3106` with `reuseExistingServer: false`. | This is the canonical no-provider synthetic handover path. Build first; install Playwright Chromium; free ports before running. Never point it at an unidentified existing server or confidential input. |
| Temporary data | `AI_IP_UPLOAD_ROOT` optionally overrides OS-temp upload root; default is OS temp/`ai-ip-generator/uploads`. Export root defaults to OS temp/`ai-ip-generator/exports` and has no environment override in `Settings.from_environment`. Pipeline source cleanup is best effort in `finally`; upload TTL sweep is fallback; DOCX response cleanup is best effort. Test harness uses its own temporary roots and exposes count-only `/__test/storage`. | Document exact roots/limits and honest failure behavior. Never promise immediate cleanup after forced shutdown or a production retention guarantee. Check residuals in the isolated test roots and report failures; do not delete user files during audit. |

Configuration inventory, based on `Settings.from_environment`, Next config and live-test guards:

| Variable | Actual role/default | Handover treatment |
|---|---|---|
| `AI_IP_ENABLE_LOCAL_ORCHESTRATION_API` | Backend `0` by default; `1` enables local metadata/process/validation/export routes; not auth. | Normal local only; offline harness injects its own enabled settings. Document the distinction. |
| `AI_IP_UPLOAD_ROOT` | Optional backend path; OS temp upload root if absent. | Document isolated, non-repository location; absent from `.env.example` today. |
| `BACKEND_URL` | Next server rewrite target; defaults to `http://127.0.0.1:8000`. | Server-side only; `.env.example` uses equivalent `localhost` spelling. Standardize examples to one loopback spelling. |
| `OPENAI_API_KEY` | Optional backend env; required only to execute actual provider-backed process/live smoke, not the injected offline harness. | Leave absent for local/synthetic acceptance. Never commit or print its value. |
| `OPENAI_TIMEOUT_SECONDS`, `OPENAI_MAX_OUTPUT_TOKENS`, `OPENAI_DRAFT_TIMEOUT_SECONDS`, `OPENAI_DRAFT_MAX_OUTPUT_TOKENS` | Optional validated provider runtime settings; defaults 180/48000 and 240/64000. | Describe as provider configuration, not offline prerequisites. Do not change approved policy. |
| `RUN_OPENAI_LIVE_TESTS`, `RUN_OPENAI_DRAFT_LIVE_TESTS` | Default false; when explicitly enabled with a key, live tests may call provider. | Force `0` in offline verification; never run opt-in live tests for P0-008. |
| `NEXT_PUBLIC_API_BASE_URL`; `SUPABASE_*` | Present in `.env.example` but not consumed by current frontend/backend path; Supabase is MVP+ only. | Remove or label as unused/future in the example; do not imply required setup or client-side API-key exposure. |

`.env.example` is a sample, not evidence that Python reads a dotenv file: backend code uses process environment directly. No real secret belongs in Git. Do not export a real API key into the fresh-env smoke shell. Explicitly distinguish optional provider settings from required offline settings (none beyond installed dependencies).

Repository-hygiene audit: `git ls-files` shows no tracked real `.env`, generated PDF, test report or local patch/scratch artefact; the tracked DOCX template and brand PNG are intentional product assets. `.gitignore` covers `.env`, `.venv`, `node_modules`, `.next`, Playwright output, caches, uploads and generated files, but does **not** ignore arbitrary `diff.patch`/`diff.txt`/`diff_out.patch` or `scratch.py`. Those four protected files, plus untracked `frontend/AGENTS.md` and `frontend/CLAUDE.md`, were present locally at preflight; none is part of P0-008 and none may be deleted or staged. A filename/ignore audit is not a secret-content scan: implementation must review exact staged content for secrets and confidential fixtures before commit. `.github/` contains a PR template but no CI workflow at this baseline; P0-009 owns CI and its absence is not mislabeled as a P0-008 failure when manual evidence passes.

## 4. Current-State Documentation Reconciliation Inventory

Only the *current-state* claim is to be corrected during a later approved implementation. Preserve historical changelog, original task handoffs and reviews as they were true when written. The following is an actionable inventory, not a claim these edits have already been made.

| File | Current statement/problem at baseline | Authoritative evidence | Required P0-008 action | Acceptance evidence |
|---|---|---|---|---|
| `README.md` opening status | Says core pipeline E2E is unfinished and omits P0-005/006/007. | Merged APP-003/P0-005/006 and P0-007 `26b1245`; closeout `8142692`. | Replace present-tense status with local/synthetic completed capability and explicit no-production/no-live claim. | Current-state paragraph agrees with PCC and P0-007 closeout. |
| `README.md` sections 7, 11–15 | Lists old 0.3.5/0.2.0/0.3.4 governance versions, Next/core E2E unchecked, APP-003 implementation NOT STARTED, public surface only health/upload; deployment providers appear as stack rather than unapproved plan. No reproducible quickstart. | `docs/system-specification.md` is 0.3.6; `AGENTS.md` 0.3.0; PCC 0.3.18; Review Log 0.3.9; local routes in `backend/app/main.py`; P0-007 closeout. | Reconcile current-status table/roadmap and route boundary; label Vercel/Railway proposed/unapproved; add quickstart pointing to runbook. Preserve historical facts only if explicitly dated. | Version/status/route/link cross-check; no production deployment implication. |
| `backend/README.md` | Assumes `.venv` already exists; normal process can call provider but no canonical offline full-flow command or shutdown guide. | `config.py`, `main.py`, `offline_backend.py`, `playwright.config.ts`. | Add fresh-env link/creation, explain ordinary-vs-injected backend, port/flag/key and cleanup caveat; link runbook. | Commands and caveat match code and smoke. |
| `frontend/README.md` | `npm install` precedes optional `npm ci`; documents P0-006 but not P0-007 handover; Node exact version not pinned. | Lockfile v3, package pins/engines, P0-007 evidence. | Prefer `npm ci` for clean clone; record verified Node/npm pair without false universal support claim; link runbook and P0-007 scope. | Clean install/build evidence and no contradictory startup ports. |
| `tests/README.md` | Uses a named developer’s absolute Python executable; “planned future categories” include already-implemented coverage. | Python 3.12 project convention, `tests/` tree and P0-007 380/3 + 11/11 evidence. | Replace machine-specific setup with portable virtual-env commands and mark planned list historical/current accurately; link canonical test table. | Fresh recipient can run copied commands from documented directory. |
| `.env.example` | Contains unused `NEXT_PUBLIC_API_BASE_URL`/`SUPABASE_*` alongside current variables; omits optional `AI_IP_UPLOAD_ROOT`; default `BACKEND_URL` spelling differs from Next fallback. | `Settings.from_environment`, `next.config.ts`, `api/client.ts`. | Reconcile sample/comments only; no real values or new security policy. | Every listed current variable maps to code; unused/future fields clearly marked or removed. |
| `docs/workflow.md` sections 1–2 | Present-tense text says frontend, public orchestration and DOCX API/E2E still need implementation. | Local routes, frontend code and P0-006/007 merges. | Update factual current-state sentences, not historical architecture contract. | Workflow description distinguishes local enabled routes from proposed production API. |
| `docs/system-specification.md` sections 19, 21 | Says frontend/E2E/export API not implemented and route table treats locally implemented routes as only future/protected endpoints. | `backend/app/main.py`, `local_orchestration.py`, `frontend/`, P0-006/007 merges. | Versioned *factual status addendum* or targeted status correction only; do not change approved technical requirements, proposed production API or auth policy. | Local existing versus proposed production routes explicitly separated. |
| `AGENTS.md` section 1 | Project identity says Phase 2 has not begun. Protocol and roles remain approved baseline. | PCC sections 5, 8 and P0-007 closeout. | Correct only factual project-status sentence with version/changelog if approved; do not revise authority/rules. | No policy change; current phase statement matches PCC. |
| `PROJECT_CONTEXT.md` section 25 and PCC sections 8, 13 | Current artefact/assignment rows still cite System Specification 0.3.5, Project Context 0.3.5 or AGENTS 0.2.0 as if current. | Actual file metadata: System Specification 0.3.6, Project Context 0.4.5 at audit base, AGENTS 0.3.0; this specification bumps Context/PCC separately. | Reconcile only present-tense version pointers to actual files; preserve dated change history. | File metadata and current indexes agree after implementation. |
| `PROJECT_CONTEXT.md` section 28 | Next action still says HUMAN MERGE P0-007 CLOSEOUT, already merged into `main`. | `main` `8142692c6e92670b4b09996d733f93c409e93e49`. | During this specification task register P0-008 review as current next gate; later add implementation/handover result only when evidenced. | Present-tense next action matches branch/review gate. |
| `docs/operations/01_PROJECT_CONTROL_CENTER.md` sections 10, 22 | Next task/action still asks Human to merge the P0-007 closeout branch. | `main` `8142692` and P0-007 CLOSED row. | During this specification task replace that current action with P0-008 specification review; leave historical handoffs/change rows intact. | No pending P0-007 merge in current queue. |
| `docs/operations/AUTONOMOUS_AGENT_PROTOCOL.md` opening | Operational scope still says APP-003 frozen until 26/09/2026. | APP-003 implementation merged `b5a47f6` and reconciled; P0-007 closed. | Mark that sentence historical or remove present-tense freeze in a versioned factual-only update; do not change MCP authority/lease rules. | No misleading current freeze or new autonomous permission. |
| `FOLDER_STRUCTURE.md` and `docs/README.md` | Structural descriptions are consistent; they do not establish setup/release state. | Tracked folder map and current code. | No edit unless a documented path/link is actually wrong. | No redundant reconciliation diff. |

Review Log `02_GEMINI_REVIEW_LOG.md` is already current for P0-007: `REV-P0-007-IMPLEMENTATION` CLOSED. It is append-oriented; no P0-008 review record is created before an actual independent review, absent a mandatory pending-entry convention. Historical P0-007 “pending” prose in pre-review sections is not a current-state error when explicitly superseded by its closeout.

## 5. P0-008 implementation boundary and minimal deliverables

The minimum coherent documentation architecture is:

1. `README.md`: concise project identity, current local/synthetic classification *only after achieved*, safe quickstart and link to one authoritative runbook.
2. `docs/operations/MVP_HANDOVER_RUNBOOK.md`: **single authority** for repository identity, completed capability matrix, setup, environment matrix, normal versus offline operation, startup/shutdown, canonical test/smoke commands, acceptance checklist, final evidence table, known limitations, BLK-003/live-provider status, data restrictions, post-MVP roadmap and Human sign-off. No separate `MVP_HANDOVER_CHECKLIST.md` or `MVP_RELEASE_EVIDENCE.md` unless a later reviewer shows a concrete need that cannot be met by sections of this runbook.
3. `backend/README.md`, `frontend/README.md`, `tests/README.md` and `.env.example`: short component-specific details and corrections, linking to the runbook rather than duplicating it.
4. Factual current-state reconciliation only where listed in section 4: `docs/workflow.md`, `docs/system-specification.md`, `AGENTS.md`, `PROJECT_CONTEXT.md` and PCC, each with appropriate version/changelog and no technical-policy rewrite. Edit an item only if it remains materially stale at implementation time.

The runbook owns **setup, operation, acceptance, limitations and release/handover evidence**. Root README is the entrypoint, not a second evidence ledger; component READMEs own component detail only. The canonical P0-007 implementation evidence stays in its task document and review log, linked by SHA. No helper script is justified now: existing virtual-env, `npm ci` and Playwright commands can demonstrate reproducibility. If a *specific* unreproducible manual step is proven, propose the smallest developer-only helper with evidence and Human approval before adding it.

No production application feature, schema, prompt, template, dependency/model upgrade, API contract change or frontend redesign is approved by default. A discovered production-code requirement is **BLOCKED / separate Human decision**, except an explicitly approved documentation-adjacent no-behavior defect with a stated test oracle. No new E2E framework, CI (P0-009), semantic evaluation (EVAL-001), production security design (SEC-001), deployment or UX polish belongs here.

## 6. Fresh-environment verification design

Use a fresh clone or isolated temporary worktree at the approved implementation SHA, outside the developer’s existing live environment. Do not delete or reset existing workspaces. Record repository URL/visibility, `git rev-parse HEAD`, OS, Python/Node/npm versions, command transcripts (redacted), install/build/smoke result and any exception. The exact eventual handover SHA must be recorded in the runbook; the `8142692…` SHA is the audit *starting* baseline, not a future final verification SHA.

For Windows PowerShell, the proposed canonical fresh-clone setup is:

```powershell
# Repository root; use Python 3.12. On POSIX use python3.12 and .venv/bin/python.
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt -r tests/requirements.txt
cd frontend
npm ci
npx playwright install chromium
```

The implementation must verify these commands in an isolated environment, not assume the author’s existing `.venv` or `node_modules`. Record failed dependency downloads as failures, not PASS. The historically validated pair is Node v24.18.0/npm 11.16.0; record the actual fresh pair and explain any variance. No container build, unpinned install, dependency upgrade or destructive cleanup is required.

Normal local startup checks (after returning to repository root) are separate from the offline full-flow smoke:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
# In a second terminal, from frontend/:
npm run dev
```

Verify backend `http://127.0.0.1:8000/health`, frontend `http://localhost:3000` and same-origin proxy `http://localhost:3000/backend/health`. The normal backend flag defaults off; this check does **not** establish offline processing through ordinary application runtimes. Stop both controlled terminals with Ctrl+C before Playwright takes ports 8000/3106; verify they exited, and do not terminate an unknown process. A pending upload may remain until best-effort TTL cleanup; record residual state rather than claiming guaranteed shutdown cleanup.

Sufficient fresh-environment evidence is a documented clean dependency installation, successful normal startup/proxy check, successful fresh build and one synthetic Playwright smoke at the fixed implementation SHA, plus no secret/provider call. A failed mandatory step blocks the classification even if P0-007 historical tests passed. Do not require a second full backend suite solely to repeat unchanged behavior.

## 7. Minimal final synthetic handover smoke

After stopping normal servers and building `frontend/`, run one *existing* browser case in the fresh environment:

```powershell
# From frontend/; Playwright owns both isolated localhost servers.
npm run test:e2e -- --grep "PDF session: cancel, immutable save, validate, review and exact UNREVIEWED export"
```

This single PDF case already uploads synthetic input, invokes fake-runtime processing through actual FastAPI/Next boundaries, displays a grounded draft, edits and selects immutable revisions, records local review status, obtains backend validation, downloads the exact selected DOCX and checks its content. `playwright.config.ts` starts the synthetic backend and built frontend on 8000/3106 with `reuseExistingServer: false`; the browser test aborts non-loopback requests. Record one-pass result, command, versions, SHA and no provider credential/call. The existing P0-007 DOCX browser case (11/11 overall) and six-run PDF/DOCX cleanup evidence may be **reused** if relevant code/tests remain unchanged; do not rerun both formats three times merely for ceremony. The chosen PDF case does not itself assert file counts, so cite the historical cleanup evidence honestly. If cleanup-related code or harness changes, run the affected existing cleanup test/case anew and record fresh zero-residual evidence before PASS. No paid provider is needed.

The full user-facing workflow through the ordinary `backend.app.main:app` still requires configured real provider runtimes; the synthetic harness is a test-only application. Handover documentation must label it visibly and never present fake-runtime output as AI quality validation. If either port is occupied by an unknown process, stop and diagnose; do not silently reuse it.

## 8. Implementation-phase command and evidence plan — not executed here

| Tier / command | Working directory | Purpose | Mandatory during implementation? | Historical substitution / expected result |
|---|---|---|---|---|
| `git rev-parse HEAD`; `git status --short` | Fresh clone root | Fixed SHA and clean tracked baseline; identify unrelated untracked files. | Yes | No substitution; exact SHA/status recorded. |
| `py -3.12 -m venv .venv`; `.\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt -r tests/requirements.txt` | Fresh clone root | Reproduce Python environment. | Yes on Windows; equivalent Python 3.12 commands on other OS. | No substitution; successful install and versions. |
| `npm ci`; `npx playwright install chromium` | Fresh clone `frontend/` | Lockfile-resolved frontend and browser prerequisite. | Yes for browser smoke. | No substitution; clean install, browser available. |
| `.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000`; check `/health` | Fresh clone root | Normal backend startup only; stop with Ctrl+C. | Yes | No substitution; healthy local response, no process/provider claim. |
| `npm run dev`; check `/` and `/backend/health` | Fresh clone `frontend/`, backend already running | Normal frontend and rewrite startup; stop with Ctrl+C. | Yes | No substitution; frontend and proxy reachable. |
| `npm run lint`; `npm run build` | Fresh clone `frontend/` | Verify fresh dependency tree and build. | Yes | Historical P0-007 PASS is context, not a substitute for fresh install/build evidence. |
| `npm run test:e2e -- --grep "PDF session: cancel, immutable save, validate, review and exact UNREVIEWED export"` | Fresh clone `frontend/`, ports free after build | One synthetic final handover smoke. | Yes | Historical PDF/11-case evidence supports scope, but cannot replace fresh handover reproducibility. |
| `.\.venv\Scripts\python.exe -m pytest tests/backend/test_health.py tests/backend/test_document_upload.py tests/backend/test_local_orchestration_api.py -q -p no:cacheprovider` | Fresh clone root | Targeted backend diagnosis if startup/API docs or relevant backend behavior changed. | Conditional; required after affected code change or unexplained smoke failure. | Historical backend counts can otherwise be reused with SHA qualification. |
| `.\.venv\Scripts\python.exe -m pytest tests -q -p no:cacheprovider` | Fresh clone root | Full offline regression. | Optional when docs/config examples only; mandatory if backend production behavior changes, or reviewer finds affected regression cannot be bounded. | P0-007 380 passed/3 skipped is historical, not a new P0-008 result. |
| `npm run test:e2e` | Fresh clone `frontend/` | Complete 11-case synthetic browser regression. | Conditional on frontend/harness behavior change or targeted failure; otherwise optional. | P0-007 11/11 may be cited unchanged, never relabeled fresh. |
| `git diff --check`; `git diff --name-only`; `git status --short` | Implementation branch root | Verify scope, whitespace and hygiene. | Yes | Exact final output; inspect staged paths explicitly. |

For offline Python checks, set `RUN_OPENAI_LIVE_TESTS=0` and `RUN_OPENAI_DRAFT_LIVE_TESTS=0` in the isolated shell and do not supply `OPENAI_API_KEY`. The extraction live test and draft live test are opt-in when their flags/key are set; never run or claim them for this handover. `PYTHONDONTWRITEBYTECODE=1` and `-p no:cacheprovider` limit local test artifacts. Commands above are *planned implementation commands*, not executed evidence for this specification.

## 9. Objective acceptance criteria

Each AC is a future implementation gate. `PASS` requires the listed evidence at an exact SHA; historical evidence alone cannot satisfy a new fresh-environment gate.

| ID | Requirement | Evidence required | Failure condition |
|---|---|---|---|
| AC-01 | Fix repo identity, audit base and final handover SHA; differentiate P0-007 merge/closeout from P0-008 work. | Git SHAs and runbook evidence ledger with provenance. | Missing/mismatched SHA or historical result relabeled fresh. |
| AC-02 | A recipient can create a clean Python 3.12 virtual environment outside the author’s existing setup. | Fresh clone/worktree path, interpreter version and successful venv creation. | Absolute developer path or pre-existing environment is required. |
| AC-03 | Install pinned backend/test dependencies and lockfile frontend/browser dependencies reproducibly. | Successful pip install, `npm ci` and Chromium prerequisite with versions and no upgrade. | Install fails, unpinned substitution is needed or lockfile is bypassed. |
| AC-04 | Normal backend command, root working directory, loopback host/port and health/upload-only default are accurate. | Fresh startup and `/health` check; flag/key boundary documented. | Wrong route/port, unreported failure or normal process falsely described offline. |
| AC-05 | Normal frontend command, directory, port and same-origin rewrite are accurate. | Fresh `npm run dev`, page and `/backend/health` check. | Proxy misroutes, requires `NEXT_PUBLIC_*` backend URL or startup instructions fail. |
| AC-06 | Environment guide separates required, optional, unused/future and live-only variables; secrets stay backend-only. | Code-to-doc variable matrix and clean sample review. | Conflicting names, hidden required key or client-exposed secret. |
| AC-07 | Offline/synthetic processing uses only injected fake runtimes and loopback, with zero provider calls and no confidential input. | `offline_backend.py`/Playwright config review, safe environment check and smoke log. | Real provider, external browser request or real/confidential fixture used. |
| AC-08 | Canonical test/install/start commands state directory, version, isolation and historical-substitution policy. | Runbook command table checked against package scripts/test layout. | Command cannot be copied to fresh environment or implies every suite is mandatory. |
| AC-09 | One fresh handover smoke proves synthetic PDF upload → process → browser display → edit/review → backend validation → exact DOCX export; cleanup provenance is explicit. | Targeted existing PDF Playwright PASS at final SHA, downloaded-content oracle and historical or affected fresh cleanup evidence. | Any stage fails, false download, or historical cleanup is claimed freshly executed. |
| AC-10 | Root/component/governance current-state prose agrees with merged capability and only planned production scope; historical entries remain intact. | Section 4 inventory closed with file/line evidence and versioned factual changes. | Present-tense “not implemented” or obsolete P0-007 next action remains, or history is rewritten. |
| AC-11 | A single handover package links capability, run/setup/test commands, review evidence, limitations, final SHA and Human sign-off. | Runbook sections and evidence links, P0-007 review `REV-P0-007-IMPLEMENTATION`. | Duplicate conflicting checklist/evidence authorities or missing provenance. |
| AC-12 | Repo hygiene excludes generated/build/cache/env/scratch/patch material and real secrets; protected local files remain untouched. | `git status`/tracked-file review, `.gitignore` checks, staged path and secret review. | Accidental secret/data/artifact commit, deletion of protected file or `git add .`. |
| AC-13 | Security/privacy copy states BLK-003 OPEN, no approved production auth/storage/retention or confidential-data use. | Cross-document terminology check and PCC blocker row. | Implied production security, authenticated multi-user use or real-data permission. |
| AC-14 | Known limitations include deferred live smoke, fake semantic oracle, session-only edits/review, no Claims/OCR/prior-art/scoring and no production SLA. | Runbook limitation register mapped to P0-007/code. | Any limitation omitted or untested live quality asserted. |
| AC-15 | P0-009 → EVAL-001 → SEC-001 → UX hardening remains a post-P0-008 sequence, not P0-008 implementation. | Backlog boundary and scope diff. | CI/eval/security/deployment/UX feature work slips into this task. |
| AC-16 | Independent review and Human acceptance are recorded before declaring `MVP HANDOVER READY — LOCAL/SYNTHETIC`; no production/release approval inferred. | Fixed-SHA review verdict, finding resolution, Human handover decision and governance closeout. | Classification made before approval or conflated with production release. |

## 10. AC traceability matrix

| AC | Existing evidence reusable | New P0-008 implementation evidence required | Expected file / command | Reviewer verification method |
|---|---|---|---|---|
| AC-01 | P0-007 merge `26b1245`/closeout `8142692`. | Final handover SHA and Git relationship. | Runbook ledger; `git rev-parse HEAD`. | Compare exact SHAs to Git. |
| AC-02 | Python 3.12 convention, P0-007 3.12.10. | New venv proof in isolated path. | Runbook setup; `py -3.12 -m venv .venv`. | Check transcript/path/version. |
| AC-03 | Pinned requirements, lockfile v3. | Clean pip/npm/Chromium install outcome. | Requirements, lockfile; `pip install`, `npm ci`, `npx playwright install chromium`. | Check no lockfile/dependency mutation. |
| AC-04 | `main.py`, `config.py`, backend README. | Fresh backend health and default route evidence. | Runbook; `uvicorn` and `/health`. | Reproduce commands/flag boundary. |
| AC-05 | Next rewrite and client; frontend README. | Fresh frontend and proxy check. | Runbook; `npm run dev` and `/backend/health`. | Verify port and same-origin proxy. |
| AC-06 | Settings/Next code and sample audit. | Corrected variable table/example. | `.env.example`, runbook, component READMEs. | Map each current variable to code; inspect no secret. |
| AC-07 | P0-007 no-provider evidence; injected offline harness. | Fresh smoke isolation/no-key evidence. | `tests/e2e/offline_backend.py`, `playwright.config.ts`. | Inspect fake injection, ports and outbound guard. |
| AC-08 | P0-007 section 7 commands, package scripts. | Copyable canonical command matrix. | Runbook; `frontend/package.json`. | Check cwd, env and mandatory/optional labels. |
| AC-09 | P0-007 PDF/DOCX 11/11, stability/cleanup 3/3 each. | One fresh PDF Playwright case and SHA; fresh cleanup only if affected. | `npm run test:e2e -- --grep "PDF session"`. | Check selected test result/download oracle; compare cleanup provenance. |
| AC-10 | P0-007/current governance closeout. | Inventory closure with factual-only diffs. | README, workflow, system spec, AGENTS, Context, PCC. | Spot-check every section 4 row; historical records unchanged. |
| AC-11 | Task/review log SHAs and findings. | One signed-off evidence/handover package. | `MVP_HANDOVER_RUNBOOK.md`. | Follow links/SHAs; no duplicated authority. |
| AC-12 | Existing `.gitignore` and tracked-file inventory. | Final staged/secret/artifact scan. | `git status --short`, `git diff --cached --name-only`. | Verify protected files unstaged and no secrets/artifacts. |
| AC-13 | BLK-003 PCC row; ADR-002/005. | Consistent handover wording. | Runbook and current READMEs. | Search forbidden production claims and inspect blocker. |
| AC-14 | P0-006/007 limitations. | Explicit current limitations register. | Runbook. | Match each stated omission to evidence. |
| AC-15 | Human-provided roadmap boundary. | Post-P0-008 backlog section and scope diff. | Runbook/spec; `git diff --name-only`. | Confirm no future-task implementation. |
| AC-16 | Human approval authority in AGENTS/ADR-005. | Independent review and separate Human handover decision. | Future Review Log/PCC closeout entry. | Reject premature status or production implication. |

## 11. Risk register

| Risk | Impact | Mitigation | Acceptance evidence |
|---|---|---|---|
| Stale current-state docs | Wrong setup or false capability claim | Close section 4 inventory with versioned factual edits. | AC-10 cross-document review. |
| Hidden developer-machine dependency | Recipient cannot reproduce | Fresh isolated clone/venv, no absolute personal paths. | AC-02/03 transcripts. |
| Provider accidentally required/called | Cost, privacy breach, false offline claim | Inject fake runtimes; unset key/disable live flags; loopback guard. | AC-07 smoke/config evidence. |
| Conflicting environment names | Wrong proxy or leaked config | Code-to-doc matrix; server-only `BACKEND_URL`. | AC-06 review. |
| Committed secret/real input | Confidentiality breach | Explicit stage, tracked/staged review, synthetic fixtures only. | AC-12 secret/artifact check. |
| Temporary-file leakage | Sensitive residuals | Isolated temp roots, historical cleanup plus fresh affected check; honest best-effort language. | AC-09/14 evidence. |
| Misleading production terminology | Unsafe data/deployment decision | Fixed classification and forbidden-synonym check. | AC-13/16 copy review. |
| Stale test evidence reused as fresh | False readiness | Per-result SHA/date/executor labels; fresh setup/build/smoke mandatory. | AC-01/09/11 ledger. |
| Scope expansion into CI/eval/security/UX | Delays baseline, unapproved behavior | Post-P0-008 boundary and Human escalation for code. | AC-15 diff review. |
| Last-minute dependency upgrade/regression | Lockfile drift or new failures | `npm ci` and pinned pip; no upgrade in P0-008. | AC-03 lockfile/dependency diff. |

## 12. Known limitations, Human decisions and post-P0-008 backlog boundary

Known limitations for the future handover: local single-tenant session only; no authenticated identity or durable/audited revision store; reload loses edits/review status; deterministic validation does not prove semantic support of edited prose; fake extraction/draft outputs do not prove real-paper accuracy; live provider smoke, cost and latency unvalidated; best-effort temporary cleanup is not a production retention/deletion guarantee; no production SLA; no real/confidential input; Claims, OCR, prior-art search, patentability scoring and legal conclusions excluded. No patent filing or production deployment is approved.

**Human decisions required to approve this specification: NONE** beyond the ordinary independent specification review and Human gate. Do not manufacture a new product/security decision to write a local/synthetic handover spec. MCP task-title/status reconciliation is an administrative prerequisite before claiming implementation, not evidence of a new scope decision. The *future final handover classification* requires separate evidenced Human acceptance after implementation/review; this does not resolve BLK-003 or approve production use.

**Post-P0-008 backlog boundary:** **P0-009 — Offline CI / Regression Automation → EVAL-001 — Semantic Quality Evaluation Framework → SEC-001 — Production Security / BLK-003 Specification → UX hardening as needed.** These are future tasks, not P0-008 acceptance requirements. P0-008 may record dependencies and limitations only. No database, production auth/storage, deployment, new provider/model policy, prompt/schema/template redesign, frontend redesign, multi-agent runtime or fine-tuning is authorized.

## 13. Specification self-review and handoff

Self-review at this specification SHA must confirm: 16 objective AC and 16 trace rows; fresh versus reusable evidence clearly distinguished; one runbook instead of three overlapping artefacts; no code/test/config/dependency changes in this specification task; no provider call/test suite executed; historical entries preserved; no arbitrary performance threshold; BLK-003 OPEN; Claims outside MVP; and P0-008 implementation/handover classification **not** yet started/declared. If independent review finds a material gap, remediate this specification and re-review before implementation approval.

```text
Task ID: P0-008
Agent: Codex
Reviewer: Antigravity independent specification reviewer — actual identity/model/profile pending
Status: READY FOR INDEPENDENT SPECIFICATION REVIEW; implementation NOT STARTED
Version: Specification v0.1.0; audit baseline 8142692c6e92670b4b09996d733f93c409e93e49
Work completed: Targeted repository audit and objective local/synthetic release-handover specification.
Files affected: docs/tasks/P0-008-mvp-release-handover-readiness.md; PROJECT_CONTEXT.md; docs/operations/01_PROJECT_CONTROL_CENTER.md.
Evidence checked: Repository docs/config/lockfile/startup/test/harness and P0-007 closeout at fixed baseline; no tests or provider calls run for this specification.
Findings: Current-state reconciliation inventory in section 4; no implementation defects claimed.
Decisions: No new product/security/provider decision; final handover classification awaits future Human approval.
Issues: BLK-003 OPEN; live-provider smoke UNVALIDATED / DEFERRED; no real/confidential-data authorization; MCP P0-008 record remains PLANNED under older “Final hardening” title and needs Human-admin synchronization before implementation claim.
Security impact: Documentation-only specification; no production-readiness claim.
Recommended next action: ANTIGRAVITY INDEPENDENT SPECIFICATION REVIEW.
```

## 14. Implementation evidence addendum 0.1.1 — specification v0.1.0 unchanged

Sections 1–13, including the exact AC and traceability wording, are the
approved specification and historical specification-phase record. This
addendum supersedes only their then-current lifecycle/next-action statements.
Google Antigravity (profile: **Google Antigravity (Advanced Agentic Coding)**)
independently reviewed specification v0.1.0 at
`52d3c62d3741e9e7abc98c2bf2b300b4885f316c`: **PASS**, specification
AC-01…AC-16 **PASS**, findings **NONE**, Human decisions required **NONE**.
The exact underlying model, review date and primary per-file report were not
supplied. Human / Product Owner explicitly approved implementation and a
**non-blocking MCP governance exception**; this is not Human handover or
production/public-deployment approval. See `REV-P0-008-SPECIFICATION` in the
review log. Independent *implementation* review has not happened.

### Implementation scope and documentation inventory

Checkpoint A `2f57a87` reconciled `.env.example`, root/component/test READMEs,
`docs/workflow.md`, `docs/system-specification.md`, `AGENTS.md` and the MCP
protocol's stale APP-003 freeze prose. Checkpoint B
`737edec7a134620285b368a9c57d08aa63829a0a` added the single
`docs/operations/MVP_HANDOVER_RUNBOOK.md`. This final evidence addendum,
`PROJECT_CONTEXT.md`, PCC and Review Log close the remaining current-state
governance gaps. Section 4 inventory: **13/13 actionable items reconciled**;
`FOLDER_STRUCTURE.md`/`docs/README.md` needed no edit. Historical changelog,
review and task-handoff statements were retained. No production application
code, test code, dependencies, prompt, schema or template changed.

### Fresh verification versus historical evidence

Fresh detached temporary worktree at `737edec7a134620285b368a9c57d08aa63829a0a`
was tracked-clean before installation. Host: Windows NT `10.0.26200.0`,
Python `3.12.10`, pip `25.0.1`, Node `v24.18.0`, npm `11.16.0`.
`py -3.12 --version` failed because this Windows launcher registered only
Python 3.14; the separately installed Python 3.12.10 executable created a
**new** `.venv` in the isolated worktree. Pinned backend/test pip install,
`npm ci` (348 packages), `npx playwright install chromium`, normal uvicorn
startup, backend `/health`, `npm run dev`, frontend HTTP 200 and
`/backend/health` proxy all **PASS**. Fresh `npm run lint` and `npm run build`
**PASS**. Normal `/process` was **not** called: it remains provider-dependent.

From fresh `frontend/`, the exact command
`npm run test:e2e -- --grep "PDF session: cancel, immutable save, validate, review and exact UNREVIEWED export"`
reported **1 passed (2.3m)**, case **15.7s**, exit **0** at `737edec`.
`frontend/e2e/integration.spec.ts:118-175` uploaded synthetic PDF, processed
through the injected fake runtimes and real HTTP/UI boundary, saved a selected
immutable revision, validated/reviewed and downloaded/inspected the exact DOCX
text and notices. Playwright teardown stalled on Windows *after* the case
passed; only its two identified child server PIDs were stopped, then the
runner exited 0. The ordinary `npm run dev` served localhost but listened on
`0.0.0.0:3000`; the runbook recommends explicit loopback binding for a
recipient. The fresh worktree retained only Next-generated, untracked
`frontend/AGENTS.md`/`frontend/CLAUDE.md`; neither was staged. Ports were
free afterward. No provider credential was present, live flags were unset,
fake runtimes were injected and the browser test aborts non-loopback requests:
provider calls **NONE**, real/confidential data **NONE**.

Historical P0-007 evidence, **not rerun for P0-008**: accepted implementation
`bd43a7e9875537c4f5ebdee53626542a11500636`, final test-code
`2638c620a36e6fb4016ed2efaeb788446a5b2eff`, targeted backend
**194 passed/1 skipped**, full offline backend **380 passed/3 skipped**,
independent lint/build **PASS**, Playwright **11/11 PASS**, PDF and DOCX
stability **3/3 each PASS**, source/export cleanup **PASS**, provider calls
**NONE**, real/confidential data **NONE**. No affected backend/frontend product,
config, test harness or dependency code changed in this P0-008 branch; fresh
full regressions were therefore not repeated. The single fresh PDF case does
not independently assert storage file counts; cleanup is historical evidence.

### AC-01…AC-16 implementation self-check and traceability

Exact requirement wording remains in section 9. The evidence below maps each
approved AC to its source and fresh/historical provenance. A gate awaiting an
independent reviewer or Human cannot be self-certified as PASS.

| AC | Requirement (section 9) | Implementation evidence / exact source or command | Self-check |
|---|---|---|---|
| AC-01 | Fix repo identity, audit base and final handover SHA; differentiate P0-007 merge/closeout from P0-008 work. | Runbook identity/evidence ledger; `git rev-parse HEAD` at isolated `737edec`; P0-007 merge `26b1245` and closeout `8142692`; final handoff SHA in Git commit/report. | PASS |
| AC-02 | A recipient can create a clean Python 3.12 virtual environment outside the author’s existing setup. | New temp worktree `.venv` created by installed Python 3.12.10 at `737edec`; `py -3.12` launcher variance documented in runbook. | PASS |
| AC-03 | Install pinned backend/test dependencies and lockfile frontend/browser dependencies reproducibly. | Fresh `pip install -r backend/requirements.txt -r tests/requirements.txt`, `npm ci` and `npx playwright install chromium` all succeeded at `737edec`; no manifest/lock changes. | PASS |
| AC-04 | Normal backend command, root working directory, loopback host/port and health/upload-only default are accurate. | Fresh root `python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000`; `/health` returned `{"status":"ok"}`; `config.py` default flag `0`; runbook normal-vs-provider caveat. | PASS |
| AC-05 | Normal frontend command, directory, port and same-origin rewrite are accurate. | Fresh `frontend/` `npm run dev`: HTTP 200 on localhost:3000, `/backend/health` returned `{"status":"ok"}`; `next.config.ts` server-side rewrite; all-interface bind caveat documented. | PASS |
| AC-06 | Environment guide separates required, optional, unused/future and live-only variables; secrets stay backend-only. | `.env.example`, runbook variable table, `backend/app/core/config.py`, `frontend/next.config.ts`; unused `NEXT_PUBLIC_API_BASE_URL`/`SUPABASE_*` removed; no key in fresh shell. | PASS |
| AC-07 | Offline/synthetic processing uses only injected fake runtimes and loopback, with zero provider calls and no confidential input. | `tests/e2e/offline_backend.py`, `frontend/playwright.config.ts`, `frontend/e2e/integration.spec.ts:26-32`; fresh key absent/live flags unset at `737edec`; synthetic PDF case PASS. | PASS |
| AC-08 | Canonical test/install/start commands state directory, version, isolation and historical-substitution policy. | Runbook setup/normal startup/test table, component READMEs; fresh commands executed at `737edec`, launcher discrepancy and regression substitution documented. | PASS |
| AC-09 | One fresh handover smoke proves synthetic PDF upload → process → browser display → edit/review → backend validation → exact DOCX export; cleanup provenance is explicit. | Exact targeted Playwright command above: 1 passed/2.3m, DOCX oracle `integration.spec.ts:118-175`; P0-007 cleanup 3/3 per format cited as historical, not fresh. | PASS |
| AC-10 | Root/component/governance current-state prose agrees with merged capability and only planned production scope; historical entries remain intact. | Section 4 inventory 13/13 actionable items; README/component docs/workflow/System Spec/AGENTS/Context/PCC/protocol factual diffs only. | PASS |
| AC-11 | A single handover package links capability, run/setup/test commands, review evidence, limitations, final SHA and Human sign-off. | One `MVP_HANDOVER_RUNBOOK.md` with evidence and explicit **pending** independent/Human sign-off gates; final branch SHA in implementation report; no duplicate checklist/evidence file. | PASS — package complete; sign-off pending as gate |
| AC-12 | Repo hygiene excludes generated/build/cache/env/scratch/patch material and real secrets; protected local files remain untouched. | `git diff --cached --name-only/--stat/--check` and added-line secret-pattern scan passed; `git ls-files` found only `.env.example` among env/patch/scratch/generated paths; original six untracked files untouched, isolated generated files unstaged. | PASS |
| AC-13 | Security/privacy copy states BLK-003 OPEN, no approved production auth/storage/retention or confidential-data use. | Runbook limitations, README, PCC blocker row and ADR-002/005 boundary; no production claim. | PASS |
| AC-14 | Known limitations include deferred live smoke, fake semantic oracle, session-only edits/review, no Claims/OCR/prior-art/scoring and no production SLA. | Runbook limitations register; frontend/backend READMEs; P0-006/007 evidence. | PASS |
| AC-15 | P0-009 → EVAL-001 → SEC-001 → UX hardening remains a post-P0-008 sequence, not P0-008 implementation. | Runbook roadmap and `git diff --name-only 52d3c62...HEAD`; no CI/eval/security/UX product files changed. | PASS |
| AC-16 | Independent review and Human acceptance are recorded before declaring `MVP HANDOVER READY — LOCAL/SYNTHETIC`; no production/release approval inferred. | Runbook/Context/PCC mark classification **NOT GRANTED**; implementation review and Human acceptance not yet performed. | BLOCKED — future review/Human gate; no premature classification |

Project Orchestrator MCP reconciliation remains **BLOCKED BY TOOL CAPABILITY**:
existing task `P0-008` still has title “Final hardening”, state `PLANNED`, no
spec/review metadata and no owner/lease. Human expressly approved this as a
**non-blocking governance exception** for Git-evidenced implementation. No
MCP metadata, state, approval or lease was invented. BLK-003 remains OPEN,
live-provider smoke UNVALIDATED / DEFERRED, public deployment NOT PERFORMED,
real/confidential data NONE, production readiness NOT APPROVED. No
`MVP HANDOVER READY — LOCAL/SYNTHETIC` classification is granted yet.

### Implementation handoff

```text
Task ID: P0-008
Agent: Codex
Reviewer: Google Antigravity (Advanced Agentic Coding) for specification; independent implementation reviewer pending
Status: READY FOR INDEPENDENT IMPLEMENTATION REVIEW; not CLOSED/COMPLETED or handover-ready
Version: Approved specification v0.1.0 at 52d3c62d3741e9e7abc98c2bf2b300b4885f316c; implementation evidence addendum 0.1.1
Work completed: Current-state documentation/configuration reconciliation, one authoritative runbook, isolated fresh install/startup/proxy/lint/build/synthetic PDF-to-DOCX verification and AC self-check.
Files affected: Documentation and .env.example only; exact paths in Git diff from approved spec SHA.
Evidence checked: Fresh worktree at 737edec7a134620285b368a9c57d08aa63829a0a; targeted Playwright 1 passed (2.3m); historical P0-007 backend/browser/stability/cleanup results kept distinct.
Findings: No self-check implementation finding; Windows Python launcher and controlled-server teardown caveats documented. Independent implementation review pending.
Decisions: Human approved implementation and non-blocking MCP governance exception; no Human handover/production acceptance.
Issues: AC-16 future gate; MCP reconciliation BLOCKED BY TOOL CAPABILITY; BLK-003 OPEN; live-provider smoke UNVALIDATED / DEFERRED.
Security impact: Synthetic/offline only; no provider key/calls or real/confidential input; no production/public deployment approval.
Recommended next action: ANTIGRAVITY INDEPENDENT IMPLEMENTATION REVIEW.
```

## 15. Final lifecycle closeout 0.1.2 — specification v0.1.0 unchanged

The preceding implementation handoff and its pending gates are historical;
this section supersedes their current-state wording without changing any
approved acceptance criterion or technical requirement. Specification review
**PASS** and independent implementation review **PASS** have findings
**NONE**. The implementation reviewer was **Google Antigravity**, using
**Gemini 1.5 Pro (Advanced Agentic Coding)**; this is historical review
metadata, not the model assigned to future reviews. AC-01…AC-15 passed
independent review; Human / Product Owner
completed AC-16 by explicitly accepting the review and granting local/synthetic
handover. AC-01…AC-16 are therefore **PASS**. Human handover acceptance is
**GRANTED**; Human also approved merging the exact reviewed implementation.

Reviewed implementation SHA: `956ba93048536d2a54d120752ade5540ecc0d901`.
Implementation merge SHA: `e6b2f665f6334047ec420c49d2097732f2917354`.
Lifecycle: **CLOSED / COMPLETED — MERGED**. Classification:
**MVP HANDOVER READY — LOCAL/SYNTHETIC**. The specification remains **v0.1.0**
at `52d3c62d3741e9e7abc98c2bf2b300b4885f316c`. See
`REV-P0-008-IMPLEMENTATION` in the review log and the final runbook closeout.

BLK-003 remains **OPEN**; live-provider smoke **UNVALIDATED / DEFERRED**;
public deployment **NOT PERFORMED**; production readiness **NO**;
real/confidential-data authorization **NO**. MCP reconciliation remains
**BLOCKED BY TOOL CAPABILITY** under a Human-approved **non-blocking governance
exception**; no MCP owner, lease, metadata update or completion is claimed.
