# APP-001/APP-002 backend and AI-RUNTIME-001 internal extraction

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

## Internal document preparation

APP-002 adds the internal `DocumentPreparationService.prepare_extraction_input(document_id)`
flow. Successful uploads are registered in a thread-safe in-memory metadata registry
with a SHA-256 digest. The service reads the backing file under a storage lease and
returns a strict AI-002-compatible envelope containing ordered `TEXT`/`TABLE` source
units, deterministic evidence IDs, and source locators.

PDF units preserve 1-based page order and use `pypdf`; no OCR or image extraction is
performed. DOCX units preserve direct paragraph/table body order using only `zipfile`
and `xml.etree.ElementTree`; table cells use TAB and rows use LF. Chunking defaults to
4,000 characters and does not rewrite, summarize, translate, or interpret source text.
Prompt-injection-like content remains data.

No public analysis endpoint is added. The registry stores metadata only, may be lost
on process restart, and is cleaned when storage deletion or TTL sweep removes a file.
Missing backing files and parsing failures return safe internal errors without source
content, bytes, tracebacks, or absolute paths.

## Internal OpenAI extraction runtime

AI-RUNTIME-001 adds `OpenAIExtractionRuntime.run_extraction(envelope)` as an internal,
stateless boundary. It loads the canonical AI-002 prompt and AI-001 schema from their
versioned repository paths, derives a strict OpenAI provider schema, calls the Responses
API once with `gpt-5.6-sol`, reasoning `high`, `store=False`, no tools/retrieval, and then
runs nullable normalization, canonical Draft 2020-12 validation, and deterministic
grounding/business validation.

Production policy fixes SDK retries at 2, timeout default at 180 seconds, and the approved
maximum output budget at 48,000 tokens. Configure only through backend environment:

```powershell
$env:OPENAI_API_KEY="<backend-secret>"
$env:OPENAI_TIMEOUT_SECONDS="180"
$env:OPENAI_MAX_OUTPUT_TOKENS="48000"
```

Do not use real research data: auth/private production storage/vendor-data acceptance
remains open. Runtime logs contain only safe operational identifiers/status/counters and
never source units, canonical prompt, full provider output, evidence excerpts, secrets,
authorization headers, or local paths.

## Tests

```powershell
$env:PYTHONDONTWRITEBYTECODE="1"
.\.venv\Scripts\python.exe -m unittest discover -s tests/backend -p "test_*.py" -v
```

The live smoke test is synthetic and opt-in. It is not part of default discovery:

```powershell
$env:RUN_OPENAI_LIVE_TESTS="1"
.\.venv\Scripts\python.exe -m unittest tests.live.test_openai_extraction_runtime_live -v
```

If `OPENAI_API_KEY` is absent, report the live test as not run; never fabricate a PASS.

