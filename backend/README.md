# APP-001 FastAPI backend

Local, single-tenant skeleton for secure synthetic PDF/DOCX upload validation.
It does not call a model, OCR service, database, cloud storage, or network API.
Do not use research or production data until the separate security, authentication,
private-storage, and retention decisions are approved.

## Python and dependencies

Use Python 3.12 and install the exact approved pins:

```powershell
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
```

## Run locally

Run from the repository root. The development server binds to localhost explicitly:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

The optional `AI_IP_UPLOAD_ROOT` environment variable may point to an ephemeral
directory outside the repository. If omitted, the operating-system temporary
directory is used. Never point it at a source-controlled path.

## Endpoints

- `GET /health` returns `{"status":"ok"}`.
- `POST /api/documents` accepts exactly one multipart field named `file`.

Successful uploads remain in ephemeral local storage for downstream local processing.
A downstream caller must use `DocumentStorage.lease(document_id)` while reading and
`DocumentStorage.delete(document_id)` immediately after completion. Startup and
request-time sweeps retry removal of files whose receipt time is at least one hour old.
Cleanup is best effort on operating systems that temporarily retain open handles.

PDF acceptance is deterministic: every page is inspected, mixed text/image PDFs are
accepted when at least one page has non-whitespace extractable text, blank pages are
allowed, and a document is rejected as scanned-only only when no page has extractable
text. No OCR is performed. DOCX pagination is not exact in APP-001; only the 10 MiB
upload limit is exact.

## Tests

```powershell
$env:PYTHONDONTWRITEBYTECODE="1"
.\.venv\Scripts\python.exe -m unittest discover -s tests/backend -p "test_*.py" -v
```

