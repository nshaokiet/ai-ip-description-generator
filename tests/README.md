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
