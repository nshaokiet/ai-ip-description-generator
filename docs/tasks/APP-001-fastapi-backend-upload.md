# APP-001 — FastAPI Backend Skeleton and Secure Document Upload

## Metadata

| Thuộc tính | Giá trị |
|---|---|
| Status | Ready for Human approval — Implementation not started |
| Owner | ChatGPT/Codex |
| Reviewer | Gemini Pro + Human / Product Owner |
| Baseline | Python 3.12; ADR-001 |
| Prepared date | 20/09/2026 |

## 1. Objective

Chuẩn bị backend FastAPI tối thiểu có health check và upload an toàn một tài liệu PDF/DOCX cho local single-tenant MVP. Task này chỉ là specification; implementation chưa được Human phê duyệt.

## 2. In scope

- FastAPI application skeleton trên Python 3.12.
- `GET /health` và `POST /api/documents`.
- Multipart upload đúng một file PDF hoặc DOCX, tối đa 10 MiB (`10 * 1024 * 1024` bytes).
- Validation extension, declared MIME, magic bytes/package signature và parser readability; không tin chỉ một tín hiệu.
- PDF text-based, không encrypted/password-protected, tối đa 50 trang và phải có extractable text layer.
- DOCX OOXML hợp lệ, không macro/embedded object/external relationship; giới hạn bắt buộc là 10 MiB.
- Local ephemeral storage bằng server-generated opaque ID, safe filename và cleanup.
- Safe structured errors, correlation ID, redacted logging và offline automated tests bằng synthetic fixtures.

## 3. Out of scope

- OpenAI Responses API, model/SDK, prompt invocation, extraction, drafting hoặc provider adapter.
- Frontend, database, Supabase/PostgreSQL, cloud/private object storage và deployment.
- Authentication, authorization, multi-tenant, background queue và persistent audit store.
- OCR/scanned PDF, exact DOCX page counting, malware scanning service và document conversion/rendering.
- DOCX export, Claims, legal advice, patentability/novelty/inventive-step assessment.
- Dữ liệu nghiên cứu thật hoặc chưa công bố.

## 4. API contract

### `GET /health`

- Success: HTTP `200`.
- Body: `{"status":"ok"}`.
- Không lộ config, secret, filesystem path hoặc dependency internals.

### `POST /api/documents`

- Content type: `multipart/form-data`.
- Field: `file`; chính xác một file, không chấp nhận zero-byte.
- Accepted declared MIME: `application/pdf` và `application/vnd.openxmlformats-officedocument.wordprocessingml.document`.
- Success: HTTP `201` với metadata an toàn gồm `document_id`, sanitized `original_filename`, `media_type`, `size_bytes`, `validation_status`, và `page_count` chỉ cho PDF. Không trả absolute/local path.
- Error body: `error.code`, `error.message`, `error.correlation_id`; có thể có safe field details nhưng không có stack trace, raw bytes, parsed full text hoặc filesystem path.
- Expected statuses: `400` malformed/empty/multiple, `413` quá 10 MiB, `415` unsupported/mismatched format, `422` corrupt/encrypted/scanned/no-text/too-many-pages/unsafe OOXML, `500` generic unexpected failure.

## 5. Validation rules

1. Giới hạn request/file được enforcement trong khi đọc, không chỉ dựa vào client metadata.
2. Original filename chỉ là metadata; path separator, traversal segment, control character và unsafe Unicode phải được neutralize.
3. Server storage name là opaque random ID; không dùng original filename làm path.
4. PDF phải bắt đầu bằng PDF signature, parser mở được, không encrypted, `1..50` trang và có non-whitespace extractable text. Không OCR.
5. DOCX phải là ZIP/OOXML package hợp lệ với required parts/content types; reject `.docm`, VBA, embedded OLE/package, external relationships và encrypted/corrupt package.
6. MIME, extension và content signature phải nhất quán.
7. DOCX không có exact page-count gate trong APP-001. Metadata nếu có chỉ có thể dùng để early reject rõ ràng `>50`, không được tuyên bố là exact validation. Exact pagination cần parser/rendering task tiếp theo.

## 6. Storage, retention and cleanup

- Local single-tenant development/MVP only; synthetic fixtures only trong development/test.
- Root storage nằm ngoài source-controlled path; không commit upload/generated content.
- Ghi file theo server-generated opaque ID; chặn overwrite và path traversal.
- Validation failure: xóa temporary bytes ngay trong `finally`/failure cleanup.
- Success: file chỉ tồn tại cho pipeline/rendering cục bộ; xóa ngay sau khi downstream processing kết thúc.
- Safety TTL: tối đa 1 giờ từ thời điểm nhận; startup/request-time sweep xóa artefact quá hạn trong skeleton không có scheduler.
- Cleanup phải idempotent; lỗi cleanup được log bằng ID an toàn, không log nội dung/tên path tuyệt đối.
- Không xử lý dữ liệu nghiên cứu thật trước security acceptance riêng.

## 7. Proposed dependencies (implementation approval required)

Chọn `backend/requirements.txt` với exact pins sau; không cài trong task specification này:

```text
fastapi==0.141.1
uvicorn==0.53.0
python-multipart==0.0.32
pydantic==2.13.5
pypdf==6.19.0
httpx==0.28.1
```

Các pin đề xuất là stable releases được đối chiếu trên PyPI ngày 20/09/2026; implementation review vẫn phải kiểm tra compatibility/lock evidence trước commit. `zipfile`, `pathlib`, `uuid`, `hashlib`, `tempfile`, `logging` và XML/package scanning dùng Python standard library. `httpx` chỉ phục vụ FastAPI/Starlette API tests. Không thêm OpenAI SDK, OCR, database hoặc cloud SDK.

## 8. Planned implementation paths

- `backend/app/__init__.py`
- `backend/app/main.py`
- `backend/app/api/__init__.py`
- `backend/app/api/routes/__init__.py`
- `backend/app/api/routes/health.py`
- `backend/app/api/routes/documents.py`
- `backend/app/core/__init__.py`
- `backend/app/core/config.py`
- `backend/app/services/__init__.py`
- `backend/app/services/document_storage.py`
- `backend/app/services/document_validation.py`
- `backend/requirements.txt`
- `backend/README.md`
- `tests/backend/test_health.py`
- `tests/backend/test_document_upload.py`
- `tests/backend/fixtures/**` chỉ khi cần, toàn bộ synthetic.
- `.env.example` chỉ khi cần khai báo config không bí mật và phải được Human cho phép trong implementation scope.

## 9. Acceptance criteria

- [ ] AC-01 FastAPI application import/khởi động thành công bằng Python 3.12 và dependency manifest dùng exact pins được duyệt.
- [ ] AC-02 `GET /health` trả `200` và chính xác `{"status":"ok"}`.
- [ ] AC-03 Upload một PDF text-based synthetic hợp lệ trả `201` và safe metadata.
- [ ] AC-04 Upload một DOCX synthetic hợp lệ trả `201` và safe metadata.
- [ ] AC-05 Zero-byte, thiếu file hoặc nhiều file bị từ chối bằng safe structured error.
- [ ] AC-06 File lớn hơn 10 MiB bị từ chối `413` trước parser/AI processing.
- [ ] AC-07 Unsupported extension/MIME/signature bị từ chối và mismatch giữa ba tín hiệu bị phát hiện.
- [ ] AC-08 Corrupt PDF/DOCX bị từ chối; không có stack trace hoặc local path trong response.
- [ ] AC-09 PDF hoặc DOCX encrypted/password-protected bị từ chối.
- [ ] AC-10 PDF trên 50 trang bị từ chối.
- [ ] AC-11 PDF không có extractable text layer bị từ chối là scanned/unsupported; không OCR.
- [ ] AC-12 DOCX macro-enabled/VBA, embedded object hoặc external relationship bị từ chối.
- [ ] AC-13 DOCX page count không được tuyên bố exact; test/doc ghi rõ giới hạn này.
- [ ] AC-14 Filename traversal/control characters không thoát storage root và không được dùng làm storage path.
- [ ] AC-15 Server-generated document/storage ID là opaque, unique trong test run và không lộ absolute path.
- [ ] AC-16 Temporary bytes của mọi validation failure được xóa ngay.
- [ ] AC-17 Success-path artefact được xóa sau downstream completion và TTL sweep xóa artefact từ 1 giờ trở lên; cleanup idempotent.
- [ ] AC-18 Logs không chứa full document text, raw bytes, secret, absolute storage path hoặc unsafe original filename.
- [ ] AC-19 Tests chỉ dùng synthetic fixtures, chạy offline và không gọi model/API/mạng.
- [ ] AC-20 Toàn bộ 85 existing AI-001/AI-002/AI-003/DOC-001 regression tests và APP-001 tests đều pass; `git diff --check` pass.
- [ ] AC-21 Diff implementation chỉ chứa paths được Human phê duyệt; không cache, upload, generated artefact, secret, PII hoặc dữ liệu nghiên cứu thật.
- [ ] AC-22 Gemini independent review và Human approval/merge phải có bằng chứng trước khi APP-001 được ghi `Completed`.

## 10. Proposed test commands

```powershell
$env:PYTHONDONTWRITEBYTECODE="1"
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m unittest discover -s tests/schema -p "test_*.py" -v
.\.venv\Scripts\python.exe -m unittest discover -s tests/prompt -p "test_*.py" -v
.\.venv\Scripts\python.exe -m unittest discover -s tests/draft -p "test_*.py" -v
.\.venv\Scripts\python.exe -m unittest discover -s tests/docx -p "test_*.py" -v
.\.venv\Scripts\python.exe -m unittest discover -s tests/backend -p "test_*.py" -v
git diff --check
```

## 11. Open blockers and non-blockers

### Blockers before implementation

- Human phê duyệt APP-001 scope, API/error contract, dependency pins và planned file list.
- Human xác nhận local ephemeral storage chỉ dùng synthetic data cho APP-001; real research data tiếp tục bị cấm trước security acceptance.

### Non-blockers for APP-001

- Exact DOCX page counting: hoãn sang parser/rendering task; APP-001 không tuyên bố enforcement 50 trang exact cho DOCX.
- Authentication/multi-tenancy, persistent storage/database, malware-scanning service, deployment và AI runtime config: không cần cho local synthetic skeleton nhưng bắt buộc phải có approval trước dữ liệu thật/production.
- Claims và optional output: nằm ngoài APP-001.

## 12. Completion rule

Tài liệu này không phải implementation approval. APP-001 chỉ được bắt đầu sau Human approval riêng và chỉ được ghi `Completed` khi AC-01…AC-22 có bằng chứng phù hợp.
