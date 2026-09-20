# ADR-001 — FastAPI Backend

## Metadata

| Thuộc tính | Giá trị |
|---|---|
| Status | Accepted |
| Date | 20/09/2026 |
| Decider | Human / Product Owner |
| Related task | APP-001 |

## Context

MVP cần một backend Python cho upload tài liệu, validation, orchestration AI và DOCX. Repository chưa có application code; các contract AI/DOCX hiện tại đều dùng Python 3.12 và automated tests offline.

## Decision

Dùng FastAPI trên Python 3.12 làm HTTP/API layer và Pydantic cho request/response validation. Application runtime tách khỏi canonical schemas, prompts và templates; ADR này không thay đổi contract AI-001/002/003/DOC-001. APP-001 chỉ được triển khai backend skeleton, `GET /health` và upload/validation cục bộ nếu Human phê duyệt implementation riêng.

## Alternatives considered

- Flask: nhẹ nhưng cần tự bổ sung nhiều phần contract/validation.
- Django/DRF: đầy đủ nhưng quá rộng cho skeleton và upload MVP nhỏ.
- Node.js backend: không tận dụng trực tiếp pipeline Python hiện có.

## Consequences

- API contract, dependency và tests backend phải được pin/version và review.
- FastAPI không tự giải quyết upload security; signature, parser, storage, cleanup và logging vẫn phải có validation riêng.
- Dependency cụ thể phải được pin trong implementation task và review trước commit.
- Quyết định này không phê duyệt backend deployment, database, authentication, AI integration hoặc dữ liệu nghiên cứu thật.
