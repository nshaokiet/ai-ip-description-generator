<p align="center">
  <img src="frontend/public/brand/vnuhcm-innovation-hub-logo.png" alt="VNUHCM Innovation Hub" width="160" />
</p>

# AI Intellectual Property Description Generator

AI-assisted drafting support that transforms scientific research documents into structured invention information and a reviewable patent-description draft.

The project is designed for research teams and innovation units that need a traceable workflow from **PDF/DOCX source material → invention analysis → human review → editable DOCX**.

> **Note:** Generated content is a draft for human/IP-specialist review. It is not legal advice, a patentability conclusion, or a filing guarantee.

## Demo

**Public demo:** https://ai-ip-synthetic-demo-frontend.onrender.com

The current public deployment is a **synthetic/demo environment**. It demonstrates the application workflow and DOCX export, but it is not yet the validated real-paper product runtime.

## Main Features

- Upload and validate PDF/DOCX research documents.
- Parse source content into traceable evidence units.
- Extract structured invention information.
- Generate a patent-description draft for human review.
- Edit, validate, and save revisions in the web application.
- Export the selected draft to editable DOCX.
- Run deterministic backend, frontend, and browser regression tests.

The next productization phase is aligning the output with a **USPTO-style nonprovisional utility patent specification**, including future Claims support and real-paper validation.

## Prerequisites

Install the following before running the project locally:

- **Python 3.12**
- **Node.js 24+**
- **npm**
- **Git**

Windows PowerShell is the primary documented local environment.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/nshaokiet/ai-ip-description-generator.git
cd ai-ip-description-generator
```

2. Create a Python virtual environment:

```powershell
py -3.12 -m venv .venv
```

3. Install backend and test dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt -r tests/requirements.txt
```

4. Install frontend dependencies:

```powershell
cd frontend
npm ci
cd ..
```

## Usage

### Start the local application

From the repository root:

```powershell
.\.venv\Scripts\python.exe tools\local_dev.py
```

Open:

- Web app: http://127.0.0.1:3000
- Backend health: http://127.0.0.1:8000/health
- Frontend-to-backend proxy: http://127.0.0.1:3000/backend/health

Press `Ctrl+C` to stop the local services.

### Check the environment without starting servers

```powershell
.\.venv\Scripts\python.exe tools\local_dev.py --check
```

### Run tests

Backend:

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q -p no:cacheprovider
```

Frontend:

```powershell
cd frontend
npm run lint
npm run typecheck
npm run build
npm run test:e2e
```

## Project Structure

```text
backend/     FastAPI backend, parsing, orchestration, validation
frontend/    Next.js web application and browser tests
prompts/     Versioned AI prompts
schemas/     Structured data contracts
templates/   DOCX templates
tests/       Backend, schema, integration, and synthetic fixtures
docs/        Specifications, ADRs, task records, and runbooks
tools/       Local development and project tooling
```

## Troubleshooting

### Python 3.12 is not found

Check:

```powershell
py -0p
```

If Python 3.12 is installed but the launcher cannot find it, create the virtual environment using the full path to the Python 3.12 executable.

### Port 3000 or 8000 is already in use

Run:

```powershell
.\.venv\Scripts\python.exe tools\local_dev.py --check
```

Stop the process currently using the required port, then start the application again.

### Frontend dependencies are inconsistent

From `frontend/`:

```powershell
npm ci
```

### Backend is not responding

Verify:

```text
http://127.0.0.1:8000/health
```

For detailed operational guidance, see [MVP_HANDOVER_RUNBOOK.md](docs/operations/MVP_HANDOVER_RUNBOOK.md).

## Contributing

1. Create a branch from the current `main`.
2. Keep changes limited to the authorized task scope.
3. Run the relevant tests before opening a pull request.
4. Do not commit secrets, private research documents, generated confidential data, or API keys.
5. Open a pull request with a clear description and verification evidence.

Project-specific collaboration and review rules are documented in [AGENTS.md](AGENTS.md).

## Documentation

- [Project Context](PROJECT_CONTEXT.md)
- [System Specification](docs/system-specification.md)
- [Project Control Center](docs/operations/01_PROJECT_CONTROL_CENTER.md)
- [MVP Handover Runbook](docs/operations/MVP_HANDOVER_RUNBOOK.md)
- [Render Demo Runbook](docs/operations/DEPLOY_001_RENDER_RUNBOOK.md)

## License

No open-source license has been published for this repository. Do not assume permission to reuse, modify, or redistribute the source code outside the project without authorization.

## Contact

- GitHub: [@nshaokiet](https://github.com/nshaokiet)
- Issues / support: [GitHub Issues](https://github.com/nshaokiet/ai-ip-description-generator/issues)
