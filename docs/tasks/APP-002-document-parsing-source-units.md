# APP-002 — Document Parsing and Evidence Source Units

## Metadata

| Thuộc tính | Giá trị |
|---|---|
| Task ID | APP-002 |
| Status | Remediation Implemented — Awaiting Gemini Targeted Re-review |
| Owner | ChatGPT/Codex |
| Reviewer | Gemini 3.1 Pro High + Human / Product Owner |
| Contract version | 1.0.0 |
| Compatibility target | AI-002 Extraction Prompt v1.0.0 input contract |
| Baseline | Python 3.12; APP-001; merge commit `b337c0353627f0df2ee57a4d087b759e82e45a52` |
| Implementation date | 21/09/2026 |

## 1. Objective

Convert an APP-001-validated local PDF or DOCX into a strict, deterministic AI-002 extraction input envelope:

```text
Validated PDF/DOCX
→ text/table extraction
→ minimal normalization
→ deterministic evidence IDs and locators
→ typed AI-002 Extraction Input Envelope
```

APP-002 does not invoke a model, network service, OCR, database, frontend, or public analysis endpoint.

## 2. In scope

- Strict Pydantic models: `DocumentMetadata`, `SourceLocator`, `SourceUnit`, and `ExtractionInputEnvelope`.
- Thread-safe in-memory metadata registry populated only after successful APP-001 validation.
- SHA-256 calculation using `hashlib`, with lowercase 64-character hexadecimal output.
- Ordered text extraction from text-based PDFs using existing `pypdf`.
- Ordered paragraph/table extraction from `word/document.xml` using `zipfile` and `xml.etree.ElementTree`.
- Deterministic Unicode-safe chunking with default maximum 4,000 characters.
- Stable evidence IDs, source locators, storage lease usage, and registry cleanup on storage deletion/TTL sweep.
- Safe internal errors and synthetic offline automated tests.

## 3. Out of scope

- OpenAI SDK, Responses API, Structured Outputs adapter, model invocation, OCR, vision, embeddings, vector database, Supabase/PostgreSQL, authentication, frontend, deployment, export API, draft runtime, Claims, prior art, patentability analysis, and real research data.
- `POST /api/documents/{id}/analyze` or any other new public endpoint.
- Changes to AI-001 schema, AI-002 canonical prompt, AI-003 contract/prompt, or DOC-001 template.

## 4. Extraction input contract

The typed envelope has exactly two root fields:

```json
{
  "document_metadata": {
    "document_id": "opaque identifier",
    "file_name": "sanitized source filename",
    "media_type": "application/pdf",
    "sha256": "lowercase 64-character digest"
  },
  "source_units": [
    {
      "evidence_id": "EV-P0001-C001",
      "evidence_type": "TEXT",
      "locator": {"page": 1, "chunk_id": "P0001-C001"},
      "content": "verbatim normalized source content"
    }
  ]
}
```

All objects reject unknown fields. `source_units` is nonempty; evidence IDs are unique; content is non-whitespace; evidence type is `TEXT` or `TABLE`; every locator contains at least one AI-002-supported locator field. APP-002 never produces `FIGURE`.

## 5. Registry and lifecycle

The in-memory `DocumentRegistry` stores only document ID, sanitized filename, canonical media type, size, optional PDF page count, and SHA-256. It never stores source content, source bytes, a public filesystem path, or database state. Registration occurs only after validation succeeds. State may be lost on process restart in this local MVP.

`prepare_extraction_input(document_id)` performs registry lookup, obtains a storage lease, verifies the backing file and digest, parses by canonical media type, validates the typed envelope, returns it, and releases the lease. Successful parsing does not delete the backing file. Missing or expired backing files invalidate the registry record. Storage deletion and TTL sweep invoke registry cleanup.

## 6. Parsing and normalization

- PDF order follows source page order; pages are 1-based. Empty pages create no units. No OCR or image extraction occurs.
- DOCX order follows direct `w:body` paragraph/table order. Paragraph IDs count body paragraphs, including omitted empty paragraphs; table IDs count body tables.
- Table cells are joined with TAB and rows with LF, preserving row/cell order without semantic inference.
- CRLF/CR becomes LF; unit boundaries are trimmed; whitespace-only units are omitted. Terms, numbers, units, language, and meaning are not edited.
- Chunking prefers newline, then whitespace, then a Unicode code-point boundary. It never summarizes, paraphrases, translates, or semantically deduplicates.

## 7. Deterministic identifiers and locators

- PDF: `EV-P####-C###`, locator contains 1-based `page` and matching `chunk_id`.
- DOCX paragraph: `EV-P####-C###`, locator contains deterministic `paragraph_id` and `chunk_id`.
- DOCX table: `EV-T####-C###`, locator contains deterministic `table_id` and `chunk_id`.
- IDs contain no filesystem path, secret, random value, or source content.

## 8. Safe internal errors

| Code | Meaning |
|---|---|
| `document_unknown` | No registry record exists. |
| `document_expired_or_missing` | Registry record exists but backing file is gone. |
| `no_extractable_text` | Parsing yields no non-whitespace text/table unit. |
| `parse_failed` | Integrity check or parser failed safely. |

Messages do not expose absolute paths, XML tracebacks, source text, or bytes.

## 9. Dependencies

No dependency was added or changed. APP-002 uses Python standard library, `pypdf==6.19.0`, and `pydantic==2.13.5` already pinned by APP-001.

## 10. Implemented paths

- `backend/app/schemas/__init__.py`
- `backend/app/schemas/analysis_input.py`
- `backend/app/services/document_registry.py`
- `backend/app/services/document_parsing.py`
- `backend/app/services/document_storage.py`
- `backend/app/api/routes/documents.py`
- `backend/app/core/config.py`
- `backend/app/main.py`
- `tests/backend/test_document_parsing.py`
- `backend/README.md`
- `docs/workflow.md`
- `docs/tasks/APP-002-document-parsing-source-units.md`

## 11. Acceptance criteria

- [x] AC-01 Main baseline contains PR #11 merge commit.
- [x] AC-02 APP-002 task specification exists.
- [x] AC-03 Successful uploads register safe metadata.
- [x] AC-04 SHA-256 is exact lowercase hexadecimal.
- [x] AC-05 PDF page order is preserved.
- [x] AC-06 PDF page locators are 1-based.
- [x] AC-07 Chunking is deterministic.
- [x] AC-08 DOCX paragraph order is preserved.
- [x] AC-09 DOCX paragraph/table interleaving is preserved, including approved block-level `w:sdt` traversal.
- [x] AC-10 Tables preserve row/cell order.
- [x] AC-11 Whitespace-only units are omitted.
- [x] AC-12 No extractable content returns a safe failure.
- [x] AC-13 Evidence IDs are unique within a document.
- [x] AC-14 Same input/parser version yields the same ordering and IDs.
- [x] AC-15 APP-002 produces only `TEXT` and `TABLE`.
- [x] AC-16 Every source unit has a supported locator.
- [x] AC-17 Envelope is compatible with AI-002 input contract.
- [x] AC-18 Metadata contains correct document ID, filename, media type, and SHA-256.
- [x] AC-19 Output/errors do not expose filesystem paths.
- [x] AC-20 Registry/backing-file state fails safely.
- [x] AC-21 Parsing occurs under a storage lease.
- [x] AC-22 Prompt-injection-like text remains untrusted data.
- [x] AC-23 No network or model call exists.
- [x] AC-24 No OCR or vision exists.
- [x] AC-25 No database or authentication exists.
- [x] AC-26 No public endpoint was added.
- [x] AC-27 AI-001 was not changed.
- [x] AC-28 AI-002 canonical prompt was not changed.
- [x] AC-29 AI-003 and DOC-001 were not changed.
- [x] AC-30 Existing regression suites pass.

## 12. Validation commands

```powershell
$env:PYTHONDONTWRITEBYTECODE="1"
.\.venv\Scripts\python.exe -m unittest discover -s tests/schema -p "test_*.py" -v
.\.venv\Scripts\python.exe -m unittest discover -s tests/prompt -p "test_*.py" -v
.\.venv\Scripts\python.exe -m unittest discover -s tests/draft -p "test_*.py" -v
.\.venv\Scripts\python.exe -m unittest discover -s tests/docx -p "test_*.py" -v
.\.venv\Scripts\python.exe -m unittest discover -s tests/backend -p "test_*.py" -v
.\.venv\Scripts\python.exe -m pip check
git diff --check
```

## 13. Gemini remediation F-001/F-002

- F-001 (`HIGH`): block-level `w:sdt/w:sdtContent` traversal implemented with deterministic paragraph/table ordering. Technical remediation is implemented and awaits Gemini targeted verification.
- F-002 (`MEDIUM`): nested tables inside `w:tc` are serialized recursively at their original cell position without creating standalone source units. Technical remediation is implemented and awaits Gemini targeted verification.
- Targeted coverage includes root-level SDT paragraphs/tables/mixed blocks, nested tables, nested SDT in table cells, ordering and repeated-run determinism.

## 14. Completion boundary

Implementation remediation and automated validation are ready for Gemini targeted re-review. APP-002 is not `Completed`, no public analysis endpoint exists, and no OpenAI runtime task has started. Human merge approval remains required.
