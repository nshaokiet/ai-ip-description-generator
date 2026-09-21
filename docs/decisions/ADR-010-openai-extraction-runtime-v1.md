# ADR-010 — OpenAI Extraction Runtime v1

## Metadata

| Thuộc tính | Giá trị |
|---|---|
| ADR ID | ADR-010 |
| Status | Accepted |
| Date | 21/09/2026 |
| Decision owner | Human / Product Owner |
| Implementation owner | ChatGPT/Codex |
| Reviewer | Gemini 3.1 Pro High |
| Related task | AI-RUNTIME-001 |

## Context

APP-002 kết thúc tại AI-002 Extraction Input Envelope. Hệ thống cần một ranh giới nội bộ, fail-closed để gọi model, nhận Structured Output, rồi chứng minh output tuân thủ canonical AI-001 contract và nguồn evidence trước khi coi là validated analysis. Canonical JSON Schema Draft 2020-12 có optional properties, conditional `allOf`, compositional `allOf`, `oneOf`, `anyOf` và `uniqueItems`; không được thay đổi canonical contract chỉ để phù hợp provider subset.

## Decision

1. Dùng OpenAI Responses API với `openai==3.16.2`, model cố định `gpt-5.6-sol` và reasoning effort `high`.
2. Mỗi extraction có đúng một logical model invocation; SDK `max_retries=2`, không có application retry loop.
3. Mọi request đặt rõ `store=False`, `stream=False`, `background=False`, không tools, retrieval, conversation hoặc `previous_response_id`.
4. Timeout mặc định 180 giây, cấu hình hợp lệ 30–300 giây. `max_output_tokens` mặc định và tối đa được phê duyệt là 48.000.
5. Canonical prompt chỉ được tải từ `prompts/extraction/v1.0.0/extraction-prompt.md`; APP-002 envelope được serialize riêng như untrusted input.
6. Provider schema được sinh deterministically từ canonical AI-001 schema. Conditional logic và `uniqueItems` không được giả vờ đã enforce ở provider; canonical validation phải enforce sau model. Compositional `allOf` phải được merge an toàn hoặc fail `provider_schema_failed`.
7. Canonical optional properties trở thành provider-required nullable. Schema-aware normalization chỉ bỏ `null` nếu property là optional trong canonical schema.
8. Mọi output phải qua `Draft202012Validator`, sau đó qua deterministic grounding/business validation cho document identity, evidence provenance, exact excerpt, logical-ID uniqueness và cross-reference existence.
9. Runtime metadata nằm ngoài canonical analysis. Error taxonomy và log chỉ chứa operational metadata an toàn, không chứa source content, canonical prompt, full provider output, evidence excerpt, credential hoặc local path.
10. Live smoke test là opt-in (`RUN_OPENAI_LIVE_TESTS=1`), synthetic-only và cần `OPENAI_API_KEY`.

## Alternatives considered

### Gửi canonical schema trực tiếp

Không chọn vì provider strict subset không biểu diễn nguyên trạng toàn bộ optional/conditional semantics.

### Duy trì provider schema thủ công độc lập

Không chọn vì tạo contract drift và hai nguồn sự thật.

### Sửa canonical AI-001 schema theo provider

Không chọn vì là breaking/behavioral change ngoài AI-RUNTIME-001.

### Tự động repair bằng model call thứ hai

Không chọn vì tăng chi phí, nondeterminism và làm mờ failure boundary.

### Retrieval/File Search

Không chọn trong v1; APP-002 envelope là nguồn duy nhất được cấp cho extraction.

## Consequences and trade-offs

- Provider generation có shape chặt, nhưng canonical/business validation vẫn là authority cuối cùng.
- Một số lỗi chỉ phát hiện sau model call, đặc biệt conditional rules và logical uniqueness.
- SDK retries có thể làm thời gian thực tế gần 540 giây cộng backoff/network overhead; public orchestration tương lai không được mặc định giữ request proxy đồng bộ trong toàn bộ khoảng này.
- Không có repair loop: invalid/refused/incomplete output thất bại rõ ràng và cần caller/user chủ động chạy lại.
- Runtime hiện là internal service; không có public analyze endpoint, draft generation, DOCX rendering hoặc storage/auth expansion.

## Security and privacy

- `OPENAI_API_KEY` chỉ lấy từ backend environment; `.env.example` chỉ có tên/default, không có credential.
- `store=False` là bắt buộc, không cấu hình thành `true` trong MVP.
- Source units là untrusted data; không có tools hay external retrieval.
- BLK-003 vẫn mở: không gửi dữ liệu nghiên cứu thật trước security/vendor-data approval.
- Live/offline tests chỉ dùng synthetic data và không in source/provider payload.

## Blocker disposition

- `BLK-004`: resolved **chỉ cho Extraction Runtime v1** bằng các quyết định model/API/retry/timeout/token/retrieval nêu trên.
- `BLK-003`: vẫn `OPEN` và tiếp tục chặn real research data/production use.
- ADR này không phê duyệt draft runtime, public HTTP orchestration hoặc model configuration cho task tương lai.
