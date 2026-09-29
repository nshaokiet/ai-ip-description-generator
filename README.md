# AI Intellectual Property Description Generator

Evidence-grounded patent-description drafting support for research teams.

Công cụ hỗ trợ chuyển bài báo khoa học thành dữ liệu có cấu trúc và bản mô tả sáng chế để rà soát thủ công.

## Project status

| Item | Status |
| --- | --- |
| MVP | **MVP COMPLETE — LOCAL/SYNTHETIC**; Human-approved bounded classification (DEC-020); P0-010 documentation closeout awaits independent review and Human merge |
| P0-008 | **CLOSED / COMPLETED — MERGED** |
| P0-009 | **CLOSED / COMPLETED — MERGED**; CI Foundation |
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
lint, build, Playwright Chromium, and synthetic E2E. The accepted post-merge
[main run](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/36521893165)
passed (backend **408 passed / 2 skipped**, lint/build PASS, Playwright
**11 passed**). P0-010 local offline verification: backend **407 passed / 3 skipped**
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

| Step | Scope |
| --- | --- |
| P0-008 | **CLOSED / COMPLETED — MERGED**; local/synthetic handover accepted |
| P0-009 | **CLOSED / COMPLETED — MERGED**; offline CI / regression automation |
| EVAL-001 PRODUCT_RUNTIME | **DEFERRED — AWAITING FUNDING**; separate Human provider/funding decision required |
| SEC-001 / BLK-003 | Production security: auth/tenant model, private storage, retention/deletion; blocker stays OPEN |
| Deployment / staging | Public deployment not performed; separate Human approval required |
| UX hardening | Deferred beyond the local/synthetic MVP |
| Prompt/model/runtime and performance/cost optimization | Deferred; no changes in P0-010 |
| Claims | Excluded from current MVP; separate scope and Human/legal review required |

## License

No repository license has been published yet.
