# AI Intellectual Property Description Generator

Evidence-grounded patent-description drafting support for research teams.

Công cụ hỗ trợ chuyển bài báo khoa học thành dữ liệu có cấu trúc và bản mô tả sáng chế để rà soát thủ công.

## Project status

| Item | Status |
| --- | --- |
| MVP | **MVP COMPLETE — LOCAL/SYNTHETIC**; P0-010 **CLOSED / COMPLETED — MERGED** via PR #30 at `9f31dae104438a598b0fe3c9bd09aba005f9026c`; final main CI `36526457334` SUCCESS |
| P0-008 | **CLOSED / COMPLETED — MERGED** |
| P0-009 | **CLOSED / COMPLETED — MERGED**; CI Foundation |
| P0-010 | **CLOSED / COMPLETED — MERGED**; Gemini 3.1 Pro High final closeout review PASS, findings NONE |
| CI | **ACTIVE** — offline regression gates on `pull_request(main)` and `push(main)` |
| EVAL-001 PRODUCT_RUNTIME | **DEFERRED — AWAITING FUNDING**; no product-runtime evidence or semantic acceptance |
| Provider authorization / budget | **NOT GRANTED / 0**; no paid calls authorized |
| Live-provider smoke | **UNVALIDATED / DEFERRED** |
| BLK-003 | **OPEN** |
| Production deployment | **NOT APPROVED / NOT PERFORMED** |
| Public URL | **NOT AVAILABLE** |

## Overview

The application helps researchers, innovation teams, and IP/patent drafting support
teams turn one text-based scientific PDF or DOCX into structured invention
information, source-linked evidence, a patent-description draft, and an editable
DOCX. It highlights missing information for the author and keeps review with people.

This is **drafting support, not legal advice**. Generated content requires
Human or IP-specialist review before any use. The current validated end-to-end
path is local and synthetic; it does not establish real-paper accuracy or
production readiness.

## Key capabilities

- PDF/DOCX upload with file validation and safe local handling.
- Deterministic parsing into ordered source and evidence units.
- Structured invention extraction with source/evidence grounding.
- Missing-information detection and questions for the author.
- Patent-description draft generation, with no Claims in the current MVP.
- Human review, prose editing, and immutable revisions within one browser session.
- Backend validation of the selected draft before export.
- Editable DOCX export of the exact validated revision.

**Claims are outside the current MVP.** Browser edits and review markers are
session-only, not a durable audit trail or formal approval.

## End-to-end workflow

```text
Scientific Paper (PDF/DOCX)
          ↓
Upload & Validation
          ↓
Parsing & Evidence Units
          ↓
Structured Extraction
          ↓
Grounding & Validation
          ↓
Missing Information
          ↓
Draft Generation
          ↓
Human Review
          ↓
DOCX Export
```

## Architecture

```text
Browser
   ↓
Next.js / TypeScript
   ↓  same-origin /backend/* proxy
FastAPI / Python
   ↓
OpenAI Responses API
   ↓
Validation / Grounding
   ↓
DOCX Renderer
```

The **normal application path** uses provider-backed extraction and drafting when
local orchestration is enabled; starting the servers does not make processing
offline. The **offline/synthetic test path** injects fake extraction/draft runtimes
while exercising the actual browser, HTTP, upload, parsing, validation, and DOCX
boundaries. Fake output does not establish live-model or semantic quality. See the
[MVP handover runbook](docs/operations/MVP_HANDOVER_RUNBOOK.md).

## Tech stack

| Layer | Technology |
| --- | --- |
| Frontend | Next.js 16, React, TypeScript |
| Backend | FastAPI, Python 3.12 |
| Provider-backed AI | OpenAI Responses API |
| Validation | JSON Schema and deterministic grounding/business rules |
| Document generation | `docxtpl`, `python-docx` |
| Testing | pytest, unittest, Playwright, ESLint |
| Version control | GitHub |

No database or deployment platform is active infrastructure in this local
baseline. P0-009 CI covers deterministic local/synthetic regression only.

## Quick start

Use Windows PowerShell from the repository root. Python 3.12 and compatible Node/npm
are required; the repository does not pin an exact Node/npm pair.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt -r tests/requirements.txt
cd frontend
npm ci
cd ..
```

If `py -3.12` cannot locate an installed Python 3.12, invoke that trusted
interpreter's `python.exe -m venv .venv` directly. The backend reads process
environment variables; it does not automatically load `.env.example`.

Start the backend from the repository root in one terminal:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

Start the frontend from `frontend/` in another terminal, bound to loopback:

```powershell
cd frontend
npm run dev -- --hostname 127.0.0.1
```

Check the [frontend](http://127.0.0.1:3000),
[backend health](http://127.0.0.1:8000/health), and
[frontend-to-backend proxy](http://127.0.0.1:3000/backend/health).
Next.js rewrites `/backend/*` using server-side `BACKEND_URL` (default
`http://127.0.0.1:8000`). Stop both controlled servers with Ctrl+C. For the
isolated synthetic full-flow setup and environment-variable matrix, follow
the [runbook](docs/operations/MVP_HANDOVER_RUNBOOK.md); do not supply a
provider key or real/confidential paper for this handover.

## Testing

From the repository root, run the offline backend regression with the local
virtual environment:

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q -p no:cacheprovider
```

From `frontend/`, install Playwright Chromium once, then run:

```powershell
npx playwright install chromium
npm run lint
npm run build
npm run test:e2e
```

The active [CI workflow](.github/workflows/ci.yml) runs on pull requests targeting
`main` and pushes to `main`: Python 3.12 full pytest, Node 24.18.0 `npm ci`,
lint, build, Playwright Chromium, and synthetic E2E. The final P0-010 post-merge
[main run](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/36526457334)
passed on merge SHA `9f31dae104438a598b0fe3c9bd09aba005f9026c` (backend **408 passed / 2 skipped**, lint/build PASS, Playwright
**11 passed**, live-test flags 0/0). P0-010 local offline verification: backend **407 passed / 3 skipped**
on Windows, lint/build PASS, Playwright **11 passed**. **Historical P0-007 evidence:** offline backend
**380 passed / 3 skipped**; Playwright **11 passed**. P0-008's fresh PDF-to-DOCX smoke and
environment details are in the runbook. CI does not validate a live provider
or real-paper semantic quality.

## Repository structure

```text
backend/    FastAPI routes, parsing, orchestration, validation
frontend/   Next.js UI and Playwright browser tests
prompts/    Versioned extraction and drafting prompts
schemas/    Structured JSON contracts
templates/  Patent-description DOCX template
tests/      Offline backend, contract, DOCX, and synthetic fixtures
docs/       Specifications, decisions, tasks, and operations
tools/      Internal project coordination and developer tooling
```

## Documentation

- [Project context](PROJECT_CONTEXT.md)
- [System specification](docs/system-specification.md)
- [Processing workflow](docs/workflow.md)
- [MVP handover runbook](docs/operations/MVP_HANDOVER_RUNBOOK.md)
- [Final local/synthetic MVP closeout](docs/operations/FINAL_MVP_CLOSEOUT.md)
- [Project Control Center](docs/operations/01_PROJECT_CONTROL_CENTER.md)
- [Independent review log](docs/operations/02_GEMINI_REVIEW_LOG.md)
- [AI collaboration rules](AGENTS.md)

Detailed task, commit, review, and governance history lives in those documents and Git history.

## Safety and current limitations

- Generated output is a **draft** requiring Human/IP-specialist review. It is not
  legal advice, a patentability or novelty/inventive-step conclusion, an inventorship determination, or a filing guarantee.
- Claims, OCR/scanned-PDF processing, prior-art search, and patentability
  scoring are outside the current MVP.
- Live-provider smoke is **UNVALIDATED / DEFERRED**. Synthetic tests do not
  validate provider behavior or real-paper semantic quality.
- EVAL-001 framework and Human-accepted six-case corpus/gold benchmark are merged;
  PRODUCT_RUNTIME semantic validation is **DEFERRED — AWAITING FUNDING**.
  Product-runtime evidence is **NONE** and semantic acceptance **NOT_DETERMINED**.
  Consumer UI or synthetic output is not equivalent to product-runtime evidence.
- Current file handling is local/ephemeral and cleanup is best effort. There is no
  approved private **production** storage or retention guarantee.
- BLK-003 remains **OPEN** for production authentication, private production storage,
  and retention/deletion policy. Real or confidential research data is **not authorized**.
- No public deployment, production approval, or public URL exists.

## Future Work

These are separate future gates, not a committed production release scope:

| Step | Status | Function / scope |
| --- | --- | --- |
| P1-001 | **CLOSED / COMPLETED — MERGED** | Frontend accessibility, keyboard/focus behavior, TypeScript typecheck and CI hardening |
| P1-002 | **PLANNED** | Expand deterministic offline adversarial regression coverage; no provider calls |
| P1-003 | **PLANNED** | Local security hardening before any public demo; does not resolve production BLK-003 |
| P1-004 | **PLANNED** | One-command local developer run/setup and DX improvements |
| P1-005 | **PLANNED** | Offline performance baseline and repeatable local measurements |
| P1-006 | **PLANNED** | UX polish, responsive behavior and error recovery |
| DEPLOY-001 | **PLANNED — implementation not authorized** | Zero-cost demo/staging deployment that can provide a public HTTPS demo URL using synthetic/demo data only; platform selection and implementation require a separate Human decision |
| EVAL-001 PRODUCT_RUNTIME | **DEFERRED — AWAITING FUNDING** | Product-runtime semantic validation; provider authorization/budget remain separate Human gates |
| SEC-001 / BLK-003 | **OPEN / DEFERRED** | Production auth/tenant model, private storage, retention/deletion; required before production or real/confidential-data use |
| Production deployment | **NOT APPROVED / NOT PERFORMED** | Separate from DEPLOY-001 demo/staging; requires security acceptance and Human approval |
| Prompt/model/runtime optimization | **DEFERRED** | Separate scope; no paid/provider work authorized |
| Claims | **OUT OF SCOPE** | Separate Human/legal scope and review required |

DEPLOY-001 is a roadmap registration only. It does not select Vercel, Railway or another hosting platform, does not authorize deployment, does not resolve BLK-003, and does not permit real/confidential research data or paid provider/API calls.

## License

No repository license has been published yet.
