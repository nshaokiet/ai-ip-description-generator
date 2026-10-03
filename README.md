<p align="center">
  <img src="frontend/public/brand/vnuhcm-innovation-hub-logo.png" alt="VNUHCM Innovation Hub" width="190" />
</p>

# AI Intellectual Property Description Generator

Evidence-grounded drafting support that helps research and innovation teams turn a scientific paper into structured invention information, a reviewable USPTO-style patent-specification draft, and an editable DOCX.

The repository combines a Next.js interface, a FastAPI processing architecture, versioned data contracts, source-linked evidence, Human review controls, validation, and deterministic synthetic tests.

> **Important:** Generated content is a draft for User and qualified intellectual-property specialist review. It is not legal advice, a patentability conclusion, an inventorship determination, a filing-ready application, or a guarantee of acceptance.

## Public Demo

**Demo:** https://ai-ip-synthetic-demo-frontend.onrender.com

The public interface supports PDF/DOCX selection. Real-paper AI conversion is not enabled yet; controlled synthetic samples remain available for the working demonstration flow. Selected arbitrary files remain in the browser UI and are not connected to synthetic results.

The deployment is non-production. Do not use real, confidential, unpublished, sensitive, or regulated research data.

## Current Status

- **P2-001:** CLOSED / COMPLETED — MERGED. The USPTO Patent Specification Target v2 contract, template, reference maps, fixtures, and offline tests are established.
- **P2-000:** CLOSED / COMPLETED — MERGED. The enterprise five-stage web workflow and its reviewed P2-000-R1 and P2-000-R2 interface remediations are on `main`; P2-000-R2 merged through PR #65 at `a394a98b0a86b1ce686fac4871f7e5b0c0c3c44f`, with main CI `37012025003` SUCCESS.
- **P2-000-R3:** IMPLEMENTATION READY FOR FIXED-SHA INDEPENDENT REVIEW — NOT MERGED. The bounded Human-review gate and Validation/DOCX workflow correction is implemented on its review branch; completion remains gated on exact-SHA independent PASS, required CI, merge, and post-merge verification.
- **BLK-003:** OPEN. Production authentication, tenant isolation, private storage, retention, and deletion controls are not approved.
- **EVAL-001 PRODUCT_RUNTIME:** DEFERRED / AWAITING FUNDING. Real-paper provider/runtime semantic validation has not been performed.
- **Claims runtime:** NOT IMPLEMENTED. Claims exist only in the P2-001 target contract.
- **Production security and real/confidential-data use:** NOT APPROVED.

Detailed task, SHA, pull-request, CI, and review evidence remains in the [Project Control Center](docs/operations/01_PROJECT_CONTROL_CENTER.md), [review log](docs/operations/02_GEMINI_REVIEW_LOG.md), task records, and Git history.

## Main Features

### Currently working demo flow

- PDF/DOCX selection and client-side validation UI.
- Controlled synthetic PDF and DOCX end-to-end samples.
- Source parsing and traceable evidence architecture.
- Structured invention-analysis architecture.
- USPTO-style patent-draft workflow.
- Human review, prose revision, and immutable session revisions.
- Exact-revision backend validation before export.
- Editable DOCX export.
- Deterministic backend, frontend, and browser regression coverage.
- USPTO Patent Specification Target v2 contract and template.

### Deferred real-paper AI runtime

- Arbitrary selected papers are not currently sent through provider-backed AI conversion in the public demo.
- Live provider evaluation and semantic acceptance remain deferred pending explicit funding and authorization.
- Production use, confidential-data processing, and Claims generation require separate approved work.

## Current Workflow

```text
1. Source Upload
2. AI Extraction
3. Review & Refine
4. Validation
5. DOCX Export
```

The controlled samples exercise the complete workflow. Reached-step navigation reuses the current session without replaying processing requests, while reset and source-removal actions keep local selection, uploaded-document, and generated-result lifecycles distinct.

## Prerequisites

- Python 3.12
- Node.js 24+
- npm
- Git

Windows PowerShell is the primary documented local environment.

## Installation

```powershell
git clone https://github.com/nshaokiet/ai-ip-description-generator.git
cd ai-ip-description-generator
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt -r tests/requirements.txt
cd frontend
npm ci
cd ..
```

Do not add an `OPENAI_API_KEY` for the documented offline/synthetic workflow.

## Usage

Start the local frontend and backend from the repository root:

```powershell
.\.venv\Scripts\python.exe tools\local_dev.py
```

Open:

- Web application: http://127.0.0.1:3000
- Backend health: http://127.0.0.1:8000/health
- Frontend proxy health: http://127.0.0.1:3000/backend/health

Check prerequisites and ports without starting services:

```powershell
.\.venv\Scripts\python.exe tools\local_dev.py --check
```

Press `Ctrl+C` to stop the services owned by the launcher.

## Testing

Backend regression:

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q -p no:cacheprovider
```

Frontend and standard browser workflow:

```powershell
cd frontend
npm ci
npm run lint
npm run typecheck
npm run build
npm run test:e2e
```

Static public-demo workflow:

```powershell
$env:RENDER_STATIC_EXPORT = "1"
$env:NEXT_PUBLIC_DEMO_STAGING = "1"
npm run build
npm run test:e2e:demo
```

All repository CI paths keep `RUN_OPENAI_LIVE_TESTS=0` and `RUN_OPENAI_DRAFT_LIVE_TESTS=0`.

## Project Structure

```text
backend/     FastAPI routes, parsing, orchestration, and validation
frontend/    Next.js application and Playwright browser tests
prompts/     Versioned extraction and drafting prompts
schemas/     Structured analysis and patent-specification contracts
templates/   Editable DOCX templates
tests/       Offline backend, schema, integration, and synthetic fixtures
docs/        Specifications, decisions, task records, reviews, and runbooks
tools/       Local development and project tooling
```

## Documentation

- [Project Context](PROJECT_CONTEXT.md)
- [System Specification](docs/system-specification.md)
- [P2-000 Product Workflow Specification](docs/tasks/P2-000-product-webapp-simplification.md)
- [Project Control Center](docs/operations/01_PROJECT_CONTROL_CENTER.md)
- [Independent Review Log](docs/operations/02_GEMINI_REVIEW_LOG.md)
- [MVP Handover Runbook](docs/operations/MVP_HANDOVER_RUNBOOK.md)
- [Render Demo Runbook](docs/operations/DEPLOY_001_RENDER_RUNBOOK.md)
- [AI Collaboration Rules](AGENTS.md)

## Troubleshooting

### Python 3.12 is not found

Run `py -0p`, then create `.venv` with the full path to an installed Python 3.12 interpreter if necessary.

### Port 3000 or 8000 is already in use

Run `.\.venv\Scripts\python.exe tools\local_dev.py --check`, stop the process using the required loopback port, and retry.

### Frontend dependencies are inconsistent

Run `npm ci` from `frontend/`.

### The backend is unavailable

Check http://127.0.0.1:8000/health and follow the [MVP Handover Runbook](docs/operations/MVP_HANDOVER_RUNBOOK.md).

## Contributing

1. Branch from the current `main`.
2. Keep changes within an explicitly authorized task.
3. Run relevant offline tests before opening a pull request.
4. Do not commit secrets, API keys, private research papers, or generated confidential data.
5. Include exact verification evidence and request independent fixed-SHA review.

## License / Contact

No open-source license has been published. Do not assume permission to reuse, modify, or redistribute this repository outside the authorized project scope.

- GitHub: [@nshaokiet](https://github.com/nshaokiet)
- Support: [GitHub Issues](https://github.com/nshaokiet/ai-ip-description-generator/issues)
