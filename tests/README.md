# Tests

## AI-001 schema validation

Python baseline: 3.12. Test-only dependency được khóa trong `tests/requirements.txt`:

```text
jsonschema==4.26.0
```

Setup và chạy test trên Windows PowerShell:

```powershell
git check-ignore -v .venv/
& "C:\Users\NguyenSongHaoKiet\AppData\Local\Programs\Python\Python312\python.exe" -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r tests/requirements.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests/schema -p "test_*.py" -v
```

Test AI-001 kiểm tra schema Draft 2020-12, hai fixture hợp lệ, nguyên nhân/vị trí lỗi chính xác của hai fixture không hợp lệ, strict objects, notice flags, grounding evidence và các conditional constraint.

Fixtures là dữ liệu synthetic. Không đưa paper nghiên cứu, PII, secret hoặc output nhạy cảm vào test repository.

## Planned future categories

- File upload validation
- Prompt regression tests
- Downstream logical-ID and cross-reference validation
- Missing-information handling
- Source-grounding checks
- DOCX field mapping
- End-to-end sample-paper tests

Golden set dùng research paper chỉ được tạo sau khi có quyền sử dụng và data policy được Human phê duyệt.

## AI-002 extraction prompt contract

Chạy test offline bằng Python 3.12 và dependency `jsonschema==4.26.0` đã khóa cho AI-001:

```powershell
$env:PYTHONDONTWRITEBYTECODE="1"
.\.venv\Scripts\python.exe -m unittest discover -s tests/prompt -p "test_*.py" -v
```

Test AI-002 kiểm tra prompt metadata, required sections, security constraints, sáu fixture synthetic, canonical schema validation của expected outputs, evidence traceability, logical-ID uniqueness và cross-reference existence. Fixture có expected output là oracle offline, không phải bằng chứng về hành vi của model thật.

## AI-003 patent draft contract

AI-003 dùng lại Python 3.12 và `jsonschema==4.26.0`; không thêm dependency. Chạy:

```powershell
$env:PYTHONDONTWRITEBYTECODE="1"
.\.venv\Scripts\python.exe -m unittest discover -s tests/draft -p "test_*.py" -v
```

Test AI-003 kiểm tra Patent Draft Schema Draft 2020-12, strict objects, fixed section/subsection order, title/Abstract missing behavior, Abstract word count, paragraph grounding, JSON Pointer source paths, logical-ID uniqueness, cross-references, evidence closure, reverse usage, unresolved conflicts, prompt-injection resistance và claims/legal-assertion exclusion.

Fixtures tại `tests/fixtures/patent-draft/v1.0.0/` hoàn toàn synthetic. Expected outputs là offline oracle; chúng không chứng minh live-model compliance hoặc provider integration.

## DOC-001 Patent DOCX Template v1.0.0

DOC-001 uses Python 3.12 with pinned dependencies in `tests/docx/requirements.txt`:

```text
-r ../requirements.txt
docxtpl==0.20.2
python-docx==1.2.0
```

Setup and test:

```powershell
$env:PYTHONDONTWRITEBYTECODE="1"
.\.venv\Scripts\python.exe -m pip install -r tests/docx/requirements.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests/docx -p "test_*.py" -v
```

The DOCX tests validate the canonical template package, manifest, schema-valid synthetic contexts, safe rendering, A4 page setup, approved typography, header/footer fields, exact section order, missing/conflict/inference handling, evidence traceability, Jinja/XML escaping, rejected invalid input, Git-ignore behavior, and scope integrity.

Render the representative Human-review output with:

```powershell
.\.venv\Scripts\python.exe tests/docx/render_patent_docx_v1.py `
  tests/fixtures/patent-docx/v1.0.0/representative-context.json `
  generated/patent-docx/v1.0.0/representative-patent-draft.docx
```

Fixtures are synthetic. Generated DOCX files stay outside Git. Automated checks do not establish Human visual QA or live-model compliance.
