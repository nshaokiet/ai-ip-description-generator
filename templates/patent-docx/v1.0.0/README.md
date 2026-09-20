# Patent DOCX Template v1.0.0

Canonical template: `templates/patent-docx/v1.0.0/patent-description-template.docx`

Status: **Completed — Merged via PR #7**

This template renders a validated Patent Draft Generation Contract v1.0.0 payload into an English, editable DOCX. It is a technical description draft, not legal advice, a patentability assessment, a filing-ready application, or a complete patent filing.

## Rendering

```powershell
$env:PYTHONDONTWRITEBYTECODE="1"
.\.venv\Scripts\python.exe tests/docx/render_patent_docx_v1.py `
  tests/fixtures/patent-docx/v1.0.0/representative-context.json `
  generated/patent-docx/v1.0.0/representative-patent-draft.docx
```

The renderer validates the input against `schemas/patent-draft/v1.0.0/patent-draft.schema.json` before rendering, uses `docxtpl` with automatic XML escaping, performs no network calls, and refuses output outside `generated/patent-docx/v1.0.0/`.

Generated files under `generated/` are ignored and must not be committed.

## Human review

Open the representative output in Microsoft Word and inspect page size, margins, typography, heading hierarchy, header/footer, page numbering, section order, lists, the evidence appendix, clipping, unresolved placeholders, and absence of Claims. If Word has not refreshed fields, press `Ctrl+A`, then `F9`.

Human Microsoft Word Visual QA completed with all checks `PASS` and no findings. Gemini 3.1 Pro High independent and targeted governance reviews also returned `PASS`, no findings, and no required changes. Human / Product Owner approved and merged PR #7 on 20/09/2026; implementation commit `d3f7c7d9596b77a39e9a56fcdf97c76cb972612a`, merge commit `d208a7925da844c5b43578bac8ebdbb1c5c6b5b8`.
