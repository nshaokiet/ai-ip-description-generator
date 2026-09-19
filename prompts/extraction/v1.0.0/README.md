# Extraction Prompt v1.0.0

Artefact chính: `extraction-prompt.md`.

Prompt này chuyển input envelope đã chuẩn hóa thành một payload tuân thủ Output Schema v1.0.0. Caller chịu trách nhiệm tạo `document_metadata`, chia source thành `source_units`, cấp `evidence_id`, `evidence_type`, `locator` và từ chối input rỗng/ chỉ có khoảng trắng trước khi gọi model.

## Contract

- Input: JSON envelope mô tả trong prompt; nội dung source được xem là dữ liệu không tin cậy.
- Output: đúng một JSON object theo `schemas/invention-output/v1.0.0/invention-output.schema.json`.
- Ngôn ngữ: English hoặc Vietnamese theo ngôn ngữ kỹ thuật chính của nguồn; evidence excerpt luôn giữ nguyên văn.
- Grounding: chỉ `SOURCE_FACT`, `PARAPHRASE`, `INFERENCE`; tất cả phải có ít nhất một evidence ID từ input.
- Thiếu hoặc mâu thuẫn: ghi vào `missing_information`, không tự bịa dữ liệu.
- Claims, tư vấn pháp lý và kết luận patentability/novelty/inventive step không thuộc phạm vi.

## Giới hạn tích hợp

AI-002 chỉ cung cấp prompt contract và kiểm thử offline. Canonical JSON Schema Draft 2020-12 hiện dùng các keyword/conditional và optional property không thể truyền nguyên trạng làm OpenAI Structured Outputs strict schema. Task này không thay đổi canonical schema, không tạo provider-specific schema/adapter và không chứng minh tích hợp Responses API. Việc chuyển đổi/adapter cùng live-model evaluation được hoãn sang task runtime riêng sau khi Human phê duyệt.

## Kiểm thử

Fixtures trong `tests/fixtures/extraction-prompt/v1.0.0/` là dữ liệu synthetic kèm expected output do test định nghĩa. Chúng kiểm tra prompt contract và invariants offline, không phải bằng chứng về hành vi thực tế của model.
