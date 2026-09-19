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
