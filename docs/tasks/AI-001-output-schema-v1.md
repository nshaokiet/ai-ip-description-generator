# AI-001 — Output Schema v1

## Metadata

| Thuộc tính | Giá trị |
|---|---|
| Task ID | AI-001 |
| Owner | ChatGPT/Codex |
| Reviewer | Gemini Pro |
| Approver | Human / Product Owner |
| Status | Implemented — Awaiting Gemini Review |
| Schema version | 1.0.0 |
| Base repository state | Commit `29ec432` |
| Implementation branch | `ai/output-schema-v1` |
| Approval date | 18/09/2026 |

## Mục tiêu

Tạo hợp đồng dữ liệu JSON có version cho kết quả phân tích sáng chế có cấu trúc. AI-001 chỉ định nghĩa và kiểm thử hợp đồng dữ liệu; output là bản nháp cần Human review, không phải tư vấn pháp lý, đánh giá khả năng cấp bằng hay hồ sơ sẵn sàng nộp.

## In scope

- JSON Schema Draft 2020-12 tại đường dẫn canonical đã phê duyệt.
- Các cấu trúc kỹ thuật, evidence, grounding, missing information và author questions.
- Strict objects bằng `additionalProperties: false`.
- Fixtures synthetic tối thiểu, đại diện và không hợp lệ.
- Automated validation tests bằng Python 3.12 và `jsonschema==4.26.0`.
- ADR, hướng dẫn sử dụng và cập nhật trạng thái tài liệu quản trị.

## Out of scope

- Claims và nội dung claim.
- Kết luận pháp lý, patentability, novelty hoặc inventive step.
- API, frontend, database, LLM integration, prompt, DOCX export và deployment.
- Trạng thái/audit Human confirmation trong payload.
- Kiểm tra uniqueness của logical ID và tồn tại của cross-reference; đây là downstream business validation.

## Deliverables

- `schemas/invention-output/v1.0.0/invention-output.schema.json`
- `schemas/invention-output/v1.0.0/README.md`
- `tests/fixtures/invention-output/v1.0.0/valid/minimal.json`
- `tests/fixtures/invention-output/v1.0.0/valid/representative.json`
- `tests/fixtures/invention-output/v1.0.0/invalid/missing-evidence.json`
- `tests/fixtures/invention-output/v1.0.0/invalid/unsupported-claims-field.json`
- `tests/schema/test_invention_output_schema_v1.py`
- `tests/requirements.txt`
- `docs/decisions/ADR-006-output-schema-v1.md`

## Acceptance criteria

- [x] Schema khai báo Draft 2020-12 và tự validation thành công.
- [x] Root contract có `schema_version` cố định là `1.0.0`.
- [x] Mọi object trong contract từ chối thuộc tính không khai báo.
- [x] `output_notice.is_legal_advice` và `output_notice.includes_patentability_assessment` đều bắt buộc và cố định `false`.
- [x] Field `claims` bị từ chối tại root.
- [x] Ba grounding label `SOURCE_FACT`, `PARAPHRASE`, `INFERENCE` đều yêu cầu ít nhất một `evidence_id`.
- [x] `minimal.json` và `representative.json` hợp lệ.
- [x] `missing-evidence.json` chỉ lỗi `minItems` tại `/technical_problems/0/grounding/evidence_ids`.
- [x] `unsupported-claims-field.json` chỉ lỗi `additionalProperties` tại root do `claims`.
- [x] Test tự động kiểm tra schema, fixtures, strict objects, notice flags, grounding và các constraint quan trọng.
- [x] Tài liệu nêu rõ `uniqueItems` không đảm bảo logical-ID uniqueness hoặc cross-reference existence.
- [x] Fixtures chỉ dùng dữ liệu synthetic, không chứa secret, PII hoặc dữ liệu nghiên cứu thật.
- [ ] Gemini Pro review và ghi finding trong review log.
- [ ] Human xử lý finding nếu có; AI-001 chưa được đánh dấu `Completed`.

## Verification command

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests/schema -p "test_*.py" -v
```

Kết quả implementation trước review: 15 test pass, 0 fail. Trạng thái vẫn là **Implemented — Awaiting Gemini Review**.
