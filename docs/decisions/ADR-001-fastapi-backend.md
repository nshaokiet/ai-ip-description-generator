# ADR-001 — FastAPI Backend

## Metadata

| Thuộc tính | Giá trị |
|---|---|
| Status | Accepted — Implemented by APP-001 — Merged via PR #10 |
| Date | 20/09/2026 |
| Decider | Human / Product Owner |
| Related task | APP-001 |

## Context

Tại thời điểm ra quyết định, MVP cần một backend Python cho upload tài liệu, validation, orchestration AI và DOCX; repository chưa có application code, còn các contract AI/DOCX đã dùng Python 3.12 và automated tests offline.

## Decision

Dùng FastAPI trên Python 3.12 làm HTTP/API layer và Pydantic cho request/response validation. Application runtime tách khỏi canonical schemas, prompts và templates; ADR này không thay đổi contract AI-001/002/003/DOC-001. Human đã phê duyệt implementation riêng cho APP-001 trong phạm vi backend skeleton, `GET /health` và upload/validation cục bộ.

## Alternatives considered

- Flask: nhẹ nhưng cần tự bổ sung nhiều phần contract/validation.
- Django/DRF: đầy đủ nhưng quá rộng cho skeleton và upload MVP nhỏ.
- Node.js backend: không tận dụng trực tiếp pipeline Python hiện có.

## Consequences

- API contract, dependency và tests backend phải được pin/version và review.
- FastAPI không tự giải quyết upload security; signature, parser, storage, cleanup và logging vẫn phải có validation riêng.
- Dependency cụ thể phải được pin trong implementation task và review trước commit.
- Quyết định này không phê duyệt backend deployment, database, authentication, AI integration hoặc dữ liệu nghiên cứu thật.

## Implementation evidence

APP-001 đã được triển khai, Gemini 3.1 Pro High review `PASS` và Human / Product Owner merge [PR #10](https://github.com/nshaokiet/ai-ip-description-generator/pull/10) ngày 20/09/2026. Specification merge commit: `1bf957162eba78c069d3ba976af7fe1d174cab30`; implementation head: `bd39b9f7bdd9f7a1796d9a405e7998070e124e07`; merge commit: `0df4814ff1eb8cd576566ac3dd403131feca3759`. Trạng thái APP-001: `Completed — Merged via PR #10`. Bằng chứng này không mở rộng ADR sang frontend, AI runtime, database, authentication, production storage hoặc deployment.
