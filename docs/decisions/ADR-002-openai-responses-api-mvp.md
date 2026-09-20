# ADR-002 — OpenAI Responses API for MVP

## Metadata

| Thuộc tính | Giá trị |
|---|---|
| Status | Accepted |
| Date | 20/09/2026 |
| Decider | Human / Product Owner |
| Related task | Future runtime integration; not APP-001 |

## Context

MVP cần production AI cho extraction và draft generation. Canonical schema/prompt đã được triển khai, nhưng provider adapter, model, timeout, retry, chi phí và vendor data policy chưa được khóa.

## Decision

Chọn OpenAI Responses API là production AI API cho MVP. Provider adapter phải chuyển canonical contract sang provider-compatible strict subset; không gửi canonical JSON Schema nguyên trạng nếu provider không hỗ trợ đầy đủ. Quyết định này chỉ khóa hướng kiến trúc; việc tích hợp, model cụ thể, adapter, File Search/retrieval và live evaluation phải có task/approval riêng.

## Alternatives considered

- Chat Completions API: không phải hướng production được chọn.
- Gemini là runtime provider: làm mất ranh giới reviewer độc lập.
- Tự host model: tăng vận hành, bảo mật và timeline.

## Consequences

- API key chỉ được ở backend environment/secret manager.
- ChatGPT Plus không được coi là OpenAI API credit hoặc runtime credential; API key, billing và cost limit do Human cung cấp/xác nhận trong task riêng.
- Không gửi dữ liệu nghiên cứu thật trước khi Human phê duyệt security/vendor data handling.
- APP-001 không cài OpenAI SDK, không gọi model/API, không triển khai File Search và không kiểm chứng live-model behavior.
