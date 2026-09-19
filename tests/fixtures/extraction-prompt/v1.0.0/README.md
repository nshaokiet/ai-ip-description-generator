# Extraction Prompt v1.0.0 fixtures

Toàn bộ fixture trong `cases/` là dữ liệu synthetic, không mô phỏng tài liệu hoặc kết quả nghiên cứu thật.

Mỗi fixture gồm:

- `case_id` và `description`;
- `expected_outcome`: `SCHEMA_VALID_OUTPUT` hoặc `REJECT_BEFORE_MODEL`;
- `input`: JSON envelope mà caller chuẩn bị;
- `expected_output`: oracle offline, chỉ có khi model invocation được phép.

Expected output không phải output quan sát từ model. Test dùng chúng để kiểm tra canonical schema, evidence traceability, logical-ID uniqueness, cross-reference existence và các invariants đã phê duyệt.

`empty-input.json` cố ý chứa source content chỉ có khoảng trắng và phải bị caller từ chối trước khi gọi model.
