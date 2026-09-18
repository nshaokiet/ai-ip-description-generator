# ADR-006 — Output Schema v1

## Metadata

| Thuộc tính | Giá trị |
|---|---|
| ADR ID | ADR-006 |
| Status | Accepted |
| Decision date | 18/09/2026 |
| Decision owner | Human / Product Owner |
| Implementer | ChatGPT/Codex |
| Reviewer | Gemini Pro |
| Related task | AI-001 |

## Context

Hệ thống cần một hợp đồng dữ liệu ổn định, kiểm tra được bằng máy cho output phân tích sáng chế trước khi triển khai API hoặc AI integration. Contract phải giảm dữ liệu tự do không kiểm soát, bắt buộc source grounding, thể hiện rõ output chỉ là bản nháp, và không tạo ấn tượng rằng hệ thống cung cấp tư vấn pháp lý hay đánh giá patentability.

AGENTS.md mô tả mô hình grounding rộng của toàn dự án, nhưng AI-001 không có canonical collection cho Human approval/audit state. Phạm vi Draft Claims cũng chưa được chốt cho các giai đoạn sau. Vì vậy schema v1 cần tách rõ structured invention analysis khỏi claims và workflow approval.

## Decision

1. Dùng JSON Schema Draft 2020-12.
2. Canonical artefact là `schemas/invention-output/v1.0.0/invention-output.schema.json` với semantic version `1.0.0` và `$id` ổn định.
3. Tất cả object dùng `additionalProperties: false`; mọi root section có mặt, các collection có thể rỗng khi không có dữ liệu.
4. Notice bắt buộc xác định output là `DRAFT`, cần Human review, không filing-ready, không phải legal advice và không chứa patentability assessment.
5. Claims bị loại hoàn toàn khỏi v1.0.0. Root property `claims` là lỗi validation.
6. Grounding label chỉ gồm `SOURCE_FACT`, `PARAPHRASE`, `INFERENCE`; mỗi grounding record phải có ít nhất một `evidence_id`.
7. Missing data được biểu diễn riêng bằng `missing_information.grounding_label = MISSING`, không dùng `MISSING` trong grounding record thông thường.
8. `HUMAN_CONFIRMED` và `human_confirmation_reference` không có trong v1.0.0. Approval/audit state thuộc workflow ngoài schema này.
9. Schema validation chỉ kiểm tra cấu trúc. Logical-ID uniqueness và cross-reference existence là downstream business validation.
10. Validation tests dùng Python 3.12 và test-only dependency `jsonschema==4.26.0`.

## Alternatives considered

### Dùng schema phẳng, ít ràng buộc

Không chọn vì khó truy vết evidence, dễ nhận dữ liệu tự do và chuyển lỗi sang runtime.

### Đưa claims vào dưới dạng optional

Không chọn vì dễ tạo hiểu nhầm claims thuộc contract đã phê duyệt trong khi phạm vi claims chưa được Human chốt cho giai đoạn sản phẩm tiếp theo.

### Đưa `HUMAN_CONFIRMED` vào grounding

Không chọn vì chưa có canonical confirmation collection hoặc audit reference. Nhãn này sẽ làm payload thể hiện một trạng thái không kiểm chứng được.

### Dùng validator tự viết không có dependency

Có thể kiểm tra một phần bằng mã chuẩn Python, nhưng không nên chọn vì việc triển khai đầy đủ Draft 2020-12 dễ sai và tạo một validator riêng phải bảo trì.

### Dùng draft JSON Schema cũ hơn

Không chọn vì Draft 2020-12 là chuẩn hiện hành được Human phê duyệt và hỗ trợ cấu trúc/conditional validation rõ ràng.

## Rationale

Thiết kế này tạo contract rõ ràng trước khi có runtime, bắt lỗi ở biên dữ liệu, giữ evidence bắt buộc cho mọi phát biểu có grounding và đặt các disclaimer ở dạng machine-enforced constants. Việc loại claims và Human confirmation giữ AI-001 đúng phạm vi đã phê duyệt.

## Consequences and trade-offs

- Producer phải gửi đủ root sections và đúng version, ngay cả khi một collection rỗng.
- Strict objects giúp phát hiện drift sớm nhưng mọi field mới đều cần versioned schema change.
- `uniqueItems` chỉ so sánh toàn object/giá trị JSON; hai object khác nhau vẫn có thể dùng cùng logical ID.
- Schema không thể bảo đảm referenced ID tồn tại. Runtime sau này phải kiểm tra ID uniqueness, cross-reference existence và document/evidence consistency.
- Việc không lưu Human confirmation trong v1 làm contract nhỏ và kiểm chứng được, nhưng approval workflow phải dùng artefact khác trong task tương lai.
- Test dependency chỉ phục vụ validation/test; không trở thành production application dependency trong AI-001.

## Evolution strategy

- Patch version: sửa constraint/documentation tương thích, không thay nghĩa contract.
- Minor version: thêm field optional hoặc capability tương thích sau Human approval.
- Major version: thay field bắt buộc, enum, semantics hoặc thêm claims theo cách breaking.
- Không sửa nội dung đã phát hành dưới cùng version. Mỗi version có thư mục riêng, fixtures và regression tests riêng.
- Nếu claims được phê duyệt sau này, tạo decision record và version/schema riêng; không backport vào `1.0.0`.

## Review status

Decision đã được Human/Product Owner phê duyệt. Implementation hiện **Awaiting Gemini Review**; ADR acceptance không đồng nghĩa AI-001 đã `Completed`.
