# AI-002 — Extraction Prompt v1.0.0

## Metadata

| Thuộc tính | Giá trị |
|---|---|
| Task ID | AI-002 |
| Owner | ChatGPT/Codex |
| Reviewer | Gemini 3.1 Pro (High) |
| Approver | Human / Product Owner |
| Status | Completed — Merged via PR #3 |
| Prompt version | 1.0.0 |
| Output contract | Output Schema v1.0.0 |
| Base commit | `c78ac5bcd0514dfedee2983d9155ee278a34cfd5` |
| Branch | `ai/extraction-prompt-v1` |
| Implementation commit | `f8772b228a23bf7cdec10fa0c463e6d1f672c341` |
| Governance commit | `9f2a78b1396cdadb747c263a2bbbbacb8d7f4292` |
| Pull Request | [#3](https://github.com/nshaokiet/ai-ip-description-generator/pull/3) — merged 19/09/2026 |
| Merge commit | `8f2b7082881961cc1a2cf7fa56ece81976759c7f` |
| Date | 19/09/2026 |

## Mục tiêu

Xây dựng prompt extraction có version để chuyển một document envelope đã chuẩn hóa thành structured invention analysis có grounding, tuân thủ Output Schema v1.0.0 và bắt buộc Human review.

## In scope

- Prompt tiếng Anh tại canonical path.
- JSON input envelope do caller chuẩn bị, gồm document metadata và source units có evidence metadata/locator.
- Nguồn tiếng Anh hoặc tiếng Việt; output theo ngôn ngữ kỹ thuật chính của nguồn.
- Grounding, verbatim excerpt, missing/conflict handling, prompt-injection defense và output-only JSON rules.
- Fixture synthetic và automated offline tests bằng Python 3.12, `unittest`, `jsonschema==4.26.0` đã có.
- Tài liệu sử dụng, ADR và cập nhật governance cần thiết.

## Out of scope

- OpenAI API, Responses API integration, live-model evaluation hoặc provider configuration.
- Provider-specific strict schema hoặc adapter chuyển đổi canonical schema.
- Thay đổi Output Schema v1.0.0.
- API, frontend, database, parsing/OCR runtime, DOCX export hoặc deployment.
- Claims/Draft Claims, tư vấn pháp lý, patentability, novelty hoặc inventive-step assessment.
- Dữ liệu nghiên cứu thật, PII, secret hoặc tài liệu chưa công bố.

## Input/output contract

Caller phải từ chối document rỗng hoặc chỉ có khoảng trắng trước model invocation. Với input không rỗng nhưng thiếu dữ liệu kỹ thuật, prompt phải tạo payload thưa nhưng schema-valid, dùng `missing_information` và không phát minh nội dung.

Expected outputs trong fixtures là oracle offline cho contract validation; chúng không được mô tả là output quan sát từ model.

## Acceptance criteria

- [x] Có prompt version `1.0.0` tại canonical path và tham chiếu Output Schema v1.0.0.
- [x] Prompt định nghĩa rõ input envelope, pre-validation, source trust boundary và output-only JSON.
- [x] Prompt xử lý nguồn EN/VI, giữ evidence excerpt nguyên văn và chỉ dùng input evidence IDs.
- [x] Prompt phân loại `SOURCE_FACT`, `PARAPHRASE`, `INFERENCE`; mọi grounding có ít nhất một evidence ID.
- [x] Prompt chuyển thiếu/mơ hồ/mâu thuẫn/không đủ chi tiết sang `missing_information` và câu hỏi có cross-reference hợp lệ.
- [x] Prompt cấm claims, tư vấn pháp lý và các kết luận patentability/novelty/inventive step.
- [x] Có đủ sáu fixture synthetic: baseline, missing information, conflicting evidence, prompt injection, non-research content và empty input.
- [x] Empty/whitespace input được đánh dấu `REJECT_BEFORE_MODEL`.
- [x] Mọi expected output không bị reject đều validate với canonical schema.
- [x] Automated tests kiểm tra prompt metadata/sections/security rules, fixtures, evidence traceability, ID uniqueness và cross-reference existence.
- [x] AI-001 regression tests đạt 15/15.
- [x] AI-002 offline tests đạt; không dùng dependency mới.
- [x] `git diff --check` đạt và diff chỉ chứa file được Human phê duyệt.
- [x] Không chứa secret, PII hoặc dữ liệu nghiên cứu thật.
- [x] Gemini 3.1 Pro High independent review hoàn tất với verdict `PASS`, không có finding hoặc required change.
- [x] Human merge approval cho PR #3 được thực hiện ngày 19/09/2026; merge commit `8f2b7082881961cc1a2cf7fa56ece81976759c7f`.

## Verification commands

```powershell
$env:PYTHONDONTWRITEBYTECODE="1"
.\.venv\Scripts\python.exe -m unittest discover -s tests/schema -p "test_*.py" -v
.\.venv\Scripts\python.exe -m unittest discover -s tests/prompt -p "test_*.py" -v
git diff --check
git status --short
git diff --stat
git diff --name-only
```

## Không phải bằng chứng runtime

AI-002 chưa gọi model thật. Test pass chỉ chứng minh prompt/fixture contract, schema conformance của expected outputs và business invariants offline; không chứng minh model sẽ luôn tuân thủ prompt. Live evaluation cần task, dataset và Human approval riêng.

## Closeout evidence

AI-002 đã `Completed — Merged via PR #3`. Gemini 3.1 Pro High review `PASS`, không có finding hoặc required change; AI-001 regression 15/15 và AI-002 offline tests 17/17 pass. Human / Product Owner đã phê duyệt và merge PR #3 ngày 19/09/2026. Prompt vẫn ở version `1.0.0`; claims, DOCX template, backend, frontend, runtime, Responses API integration và live-model evaluation không được triển khai trong task này.
