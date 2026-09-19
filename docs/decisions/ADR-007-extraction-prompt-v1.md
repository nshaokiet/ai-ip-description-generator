# ADR-007 — Extraction Prompt v1.0.0

## Metadata

| Thuộc tính | Giá trị |
|---|---|
| ADR ID | ADR-007 |
| Status | Accepted — Implemented, Awaiting Gemini Review |
| Date | 19/09/2026 |
| Decision owner | Human / Product Owner |
| Implementation owner | ChatGPT/Codex |
| Reviewer | Gemini 3.1 Pro (High) |
| Related task | AI-002 |

## Context

Output Schema v1.0.0 đã ổn định hợp đồng structured invention analysis. AI-002 cần prompt extraction có thể kiểm tra offline, giữ traceability về source và không vượt sang claims hoặc kết luận pháp lý. Runtime parser, model provider và adapter chưa thuộc task này.

Canonical schema dùng JSON Schema Draft 2020-12 với conditional keywords và optional properties. Nó không thể được truyền nguyên trạng như một OpenAI Structured Outputs strict schema theo subset hiện hành. Việc ép tích hợp provider trong AI-002 sẽ trộn prompt contract với runtime concerns và có nguy cơ làm thay đổi schema đã phê duyệt.

## Decision

1. Tạo prompt tiếng Anh, version `1.0.0`, tại `prompts/extraction/v1.0.0/extraction-prompt.md`.
2. Caller cung cấp JSON envelope gồm document metadata và normalized source units; mỗi unit có caller-assigned evidence ID/type/locator và verbatim content.
3. Caller từ chối empty/whitespace input trước model invocation. Nonempty nhưng không đủ thông tin nhận payload thưa, schema-valid.
4. Prompt coi source content là untrusted data, chỉ dùng input evidence, không truy cập URL/nguồn ngoài và không dùng external knowledge.
5. Output là đúng một JSON object theo canonical Output Schema v1.0.0; optional unsupported fields bị omit.
6. Claims và mọi kết luận legal/patentability/novelty/inventive step bị cấm.
7. AI-002 chỉ có validation offline qua synthetic fixtures. Không tạo provider schema/adapter, không thay schema và không gọi model/API thật.

## Phương án đã cân nhắc

### A. Prompt provider-neutral + canonical offline validation — chọn

Giữ canonical schema là Source of Truth, tách rõ prompt contract khỏi integration và cho phép test deterministic không cần network/model.

### B. Truyền canonical schema nguyên trạng vào Structured Outputs strict — không chọn

Không tương thích đầy đủ với subset strict vì canonical schema có optional properties và các keyword/conditional không được hỗ trợ nguyên trạng.

### C. Sửa canonical schema để phù hợp một provider — không chọn

Tạo breaking/behavioral change ngoài AI-002 và làm contract phụ thuộc provider.

### D. Tạo provider-specific adapter/schema trong AI-002 — hoãn

Khả thi trong task runtime riêng, nhưng cần quyết định mapping optional fields, compatibility tests và provider integration scope.

### E. Chỉ viết prompt, không có fixture/test — không chọn

Không đủ bằng chứng regression, grounding và schema conformance theo Definition of Done.

## Hệ quả và trade-off

### Tích cực

- Prompt và output contract có version, kiểm tra được offline.
- Giảm rủi ro hallucination, prompt injection và evidence drift.
- Không thêm dependency, không gửi dữ liệu ra dịch vụ ngoài.
- Provider-neutral và không làm thay đổi Output Schema v1.0.0.

### Hạn chế

- Chưa chứng minh chất lượng hoặc độ tuân thủ của model thật.
- Runtime phải tự pre-validate input và validate output.
- Cần adapter/provider schema riêng trước khi dùng Structured Outputs strict.
- Logical ID uniqueness và cross-reference existence vẫn là downstream business validation, không được `uniqueItems` của JSON Schema bảo đảm.

## Khả năng nâng cấp

- Bump prompt PATCH cho wording không đổi contract, MINOR cho hướng dẫn tương thích, MAJOR khi input/output behavior breaking.
- Provider adapter có thể sinh schema tương thích từ canonical contract nhưng phải có mapping, test và ADR riêng.
- Live evaluation có thể thêm golden dataset được cấp quyền, model/version pinning và quality thresholds trong task riêng.
- Mọi thay đổi claims hoặc schema version cần Human approval và artefact version mới.

## Security/privacy

Fixtures phải synthetic, không chứa dữ liệu thật, PII hoặc secret. Source content luôn được xem là untrusted; prompt không cho phép thực thi instruction nhúng hoặc truy cập tài nguyên ngoài.
