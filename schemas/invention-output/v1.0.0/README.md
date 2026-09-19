# Invention Output Schema v1.0.0

Canonical schema: `schemas/invention-output/v1.0.0/invention-output.schema.json`
JSON Schema dialect: Draft 2020-12
Status: **Gemini Review Passed — Awaiting Human Merge Approval**

## Purpose and boundary

Schema này mô tả structured invention analysis để máy validation và Human tiếp tục review. Payload không phải tư vấn pháp lý, không chứa đánh giá patentability, không phải hồ sơ sáng chế hoàn chỉnh hoặc sẵn sàng nộp.

Claims bị loại hoàn toàn khỏi v1.0.0. `claims` ở root sẽ bị từ chối. Schema cũng không có `HUMAN_CONFIRMED` hoặc `human_confirmation_reference`; Human approval/audit state nằm ngoài contract này.

## Root field contract

Mọi field dưới đây đều **required**. Không có giá trị mặc định; producer phải gửi giá trị rõ ràng. Mọi object đều có `additionalProperties: false`.

| Field | Type | Constraints | Purpose |
|---|---|---|---|
| `schema_version` | string | `const: "1.0.0"` | Chọn đúng contract version |
| `output_type` | string | `const: "STRUCTURED_INVENTION_ANALYSIS"` | Phân loại payload |
| `output_notice` | object | Xem notice contract | Disclaimer kiểm tra được bằng máy |
| `document_metadata` | object | Xem metadata contract | Nhận diện input synthetic/production |
| `title_candidates` | array | unique JSON items | Tiêu đề đề xuất có grounding |
| `technical_field` | object | `PRESENT` hoặc `MISSING` | Lĩnh vực kỹ thuật |
| `background` | array | grounded statements | Bối cảnh; không phải prior-art search |
| `technical_problems` | array | grounded problems | Vấn đề kỹ thuật |
| `technical_solutions` | array | grounded solutions | Giải pháp và problem references |
| `components` | array | strict component objects | Thành phần và quan hệ |
| `process_steps` | array | sequence integer >= 1 | Các bước và điều kiện |
| `potential_distinguishing_features` | array | grounded feature objects | Đặc trưng tiềm năng, không phải novelty conclusion |
| `technical_effects` | array | grounded effect objects | Hiệu quả kỹ thuật được báo cáo |
| `embodiments` | array | grounded embodiment objects | Phương án thực hiện |
| `experimental_data` | array | mỗi experiment có >= 1 result | Dữ liệu thử nghiệm có nguồn |
| `drawing_requirements` | array | conditional constraints | Hình nguồn hoặc hình đề xuất |
| `missing_information` | array | `grounding_label: MISSING` | Thông tin chưa có và owner xử lý |
| `author_questions` | array | priority enum | Câu hỏi liên kết missing item |
| `evidence` | array | locator không rỗng | Bằng chứng nguồn |

## Nested field contract

`R` = required, `O` = optional. Không field nào có default.

| Object / field | R/O | Type and constraints | Purpose |
|---|---:|---|---|
| `output_notice.status` | R | const `DRAFT` | Chặn diễn giải output là final |
| `output_notice.human_review_required` | R | const `true` | Bắt buộc Human review |
| `output_notice.is_legal_advice` | R | const `false` | Xác nhận không phải tư vấn pháp lý |
| `output_notice.filing_ready` | R | const `false` | Xác nhận chưa sẵn sàng nộp |
| `output_notice.includes_patentability_assessment` | R | const `false` | Xác nhận không đánh giá patentability |
| `document_metadata.document_id` | R | identifier | ID tài liệu |
| `document_metadata.file_name` | R | nonblank, max 255 | Tên file |
| `document_metadata.media_type` | R | PDF hoặc DOCX MIME enum | Loại file nguồn |
| `document_metadata.sha256` | O | 64 lowercase hex | Checksum nguồn |
| `grounding.label` | R | `SOURCE_FACT`, `PARAPHRASE`, `INFERENCE` | Loại quan hệ với nguồn |
| `grounding.evidence_ids` | R | identifier array, min 1, unique JSON values | Evidence bắt buộc cho mọi label |
| `title_candidate.title_id` | R | identifier | ID ứng viên |
| `title_candidate.title` | R | nonblank, max 500 | Tiêu đề đề xuất |
| `title_candidate.rationale` | R | nonblank text | Lý do đề xuất |
| `title_candidate.grounding` | R | grounding object | Căn cứ |
| `technical_field.status` | R | `PRESENT`, `MISSING` | Trạng thái field |
| `technical_field.item` | Conditional | required khi `PRESENT`, forbidden khi `MISSING` | Chi tiết lĩnh vực |
| `technical_field.item.field_id/name/grounding` | R | identifier / short name / grounding | Nội dung field có nguồn |
| `technical_field.item.description` | O | nonblank text | Mô tả bổ sung |
| `grounded_statement.statement_id/text/grounding` | R | identifier / text / grounding | Cấu trúc statement dùng lại |
| `technical_problem.problem_id/statement/grounding` | R | identifier / text / grounding | Một vấn đề kỹ thuật |
| `technical_solution.solution_id/statement/grounding` | R | identifier / text / grounding | Một giải pháp kỹ thuật |
| `technical_solution.addresses_problem_ids` | R | identifier array, min 1 | Tham chiếu problem |
| `component.component_id/name/related_component_ids/grounding` | R | identifier / short name / ID array / grounding | Thành phần và quan hệ |
| `component.description` | O | nonblank text | Mô tả thành phần |
| `process_step.step_id/sequence/action` | R | identifier / integer >= 1 / text | Danh tính, thứ tự, hành động |
| `process_step.input_component_ids/output_component_ids` | R | identifier arrays | Component references |
| `process_step.conditions` | R | grounded-statement array | Điều kiện thực hiện |
| `process_step.grounding` | R | grounding | Căn cứ bước |
| `potential_distinguishing_feature.feature_id/statement/rationale` | R | identifier / text / text | Đặc trưng và lý do |
| `potential_distinguishing_feature.related_component_ids/related_step_ids` | R | identifier arrays | References liên quan |
| `potential_distinguishing_feature.grounding` | R | grounding | Căn cứ; không kết luận novelty |
| `technical_effect.effect_id/statement` | R | identifier / text | Hiệu quả được báo cáo |
| `technical_effect.related_solution_ids/conditions/grounding` | R | ID array / grounded statements / grounding | Quan hệ, điều kiện, căn cứ |
| `embodiment.embodiment_id/name/description` | R | identifier / short name / text | Phương án thực hiện |
| `embodiment.component_ids/process_step_ids/grounding` | R | ID arrays / grounding | References và căn cứ |
| `experiment.experiment_id/name/description` | R | identifier / short name / text | Thử nghiệm |
| `experiment.conditions` | R | condition array | Điều kiện thử nghiệm |
| `experiment.results` | R | result array, min 1 | Kết quả bắt buộc |
| `experiment.grounding` | R | grounding | Căn cứ thử nghiệm |
| `condition.parameter/value` | R | short name / nonblank string, number hoặc boolean | Tham số và giá trị |
| `condition.unit` | O | nonblank, max 64 | Đơn vị |
| `result.metric/value` | R | short name / nonblank string, number hoặc boolean | Chỉ số và giá trị |
| `result.unit` | O | nonblank, max 64 | Đơn vị |
| `drawing_requirement.drawing_id/title` | R | identifier / short name | ID và tiêu đề hình |
| `drawing_requirement.kind` | R | `SOURCE_FIGURE`, `PROPOSED_DRAWING` | Loại hình |
| `drawing_requirement.status` | R | `AVAILABLE`, `PROPOSED`, `MISSING` | Trạng thái hình |
| `drawing_requirement.source_evidence_ids` | R | ID array; min 1 cho `SOURCE_FIGURE` | Evidence hình nguồn |
| `drawing_requirement.human_confirmation_required` | R | boolean; const `true` cho proposed drawing | Cờ workflow, không phải approval state |
| `missing_information.missing_id/target_path/description` | R | identifier / path bắt đầu `/` / text | Item thiếu và vị trí |
| `missing_information.reason` | R | `NOT_FOUND`, `AMBIGUOUS`, `CONFLICTING`, `INSUFFICIENT_DETAIL` | Nguyên nhân thiếu |
| `missing_information.impact` | R | `BLOCKING`, `HIGH`, `MEDIUM`, `LOW` | Mức ảnh hưởng |
| `missing_information.owner` | R | `AUTHOR`, `HUMAN_REVIEWER`, `IP_SPECIALIST` | Người cần xử lý |
| `missing_information.grounding_label` | R | const `MISSING` | Phân loại dữ liệu thiếu |
| `author_question.question_id/missing_information_id/question` | R | identifier / identifier / text | Câu hỏi và missing reference |
| `author_question.priority` | R | `HIGH`, `MEDIUM`, `LOW` | Ưu tiên |
| `evidence.evidence_id/document_id` | R | identifiers | Evidence và source document IDs |
| `evidence.evidence_type` | R | `TEXT`, `TABLE`, `FIGURE`, `METADATA` | Loại bằng chứng |
| `evidence.locator` | R | strict object, ít nhất một locator | Vị trí nguồn |
| `locator.page` | O | integer >= 1 | Trang |
| `locator.section` | O | nonblank, max 500 | Mục |
| `locator.paragraph_id/chunk_id/table_id/figure_id` | O | identifiers | Locator chi tiết |
| `evidence.excerpt` | R | nonblank, max 2000 | Trích đoạn ngắn làm căn cứ |

Identifier phải khớp `^[A-Za-z][A-Za-z0-9._:-]{0,127}$`.

## Validation layers

`uniqueItems: true` chỉ loại các phần tử JSON hoàn toàn trùng nhau; nó **không đảm bảo uniqueness của logical ID bên trong object**. Schema cũng không xác nhận một referenced ID thực sự tồn tại. Logical-ID uniqueness, cross-reference existence và consistency giữa `document_id`/`evidence_id` vẫn là downstream business validation.

## Examples

- Payload tối thiểu hợp lệ: `tests/fixtures/invention-output/v1.0.0/valid/minimal.json`.
- Payload đầy đủ đại diện, chỉ dùng dữ liệu synthetic: `tests/fixtures/invention-output/v1.0.0/valid/representative.json`.
- Payload lỗi evidence: `tests/fixtures/invention-output/v1.0.0/invalid/missing-evidence.json`.
- Payload lỗi claims: `tests/fixtures/invention-output/v1.0.0/invalid/unsupported-claims-field.json`.

Fixture `representative.json` là ví dụ đầy đủ canonical để tránh hai bản JSON sao chép bị drift.

## Setup and test

Trước khi tạo môi trường, xác nhận `.venv/` được ignore:

```powershell
git check-ignore -v .venv/
& "C:\Users\NguyenSongHaoKiet\AppData\Local\Programs\Python\Python312\python.exe" -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r tests/requirements.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests/schema -p "test_*.py" -v
```

Lệnh trên dùng Python 3.12.10 đã được Human phê duyệt cho lần triển khai này; không thay bằng Python version khác khi tái tạo evidence của AI-001.
