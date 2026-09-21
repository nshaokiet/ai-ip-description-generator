# MVP Processing Workflow

## 1. User Upload

Accepted initial formats:

- Text-based PDF, tối đa 10 MiB và 50 trang.
- DOCX OOXML, tối đa 10 MiB.

MVP/APP-001 không hỗ trợ scanned PDF/OCR. Exact DOCX page count không thể xác minh đáng tin cậy nếu không render, vì vậy không có exact 50-page enforcement cho DOCX trong APP-001; metadata nếu có chỉ được dùng để early reject trường hợp rõ ràng.

Validation phải đối chiếu extension, declared MIME, signature/package và parser readability; reject empty/multiple file, mismatch, corrupt/encrypted input, unsafe DOCX package và PDF không có text layer. Original filename không được dùng làm storage path.

APP-001 chỉ dùng local ephemeral storage trong single-tenant synthetic development. Temporary bytes bị xóa ngay khi validation thất bại, sau downstream processing, hoặc muộn nhất sau 1 giờ. Không dùng dữ liệu nghiên cứu thật trước security acceptance.

Trạng thái hiện hành: APP-001 `Completed — Merged via PR #10` ngày 20/09/2026. Backend đã triển khai `GET /health`, secure `POST /api/documents` và validation/cleanup tương ứng; frontend, AI runtime, database, authentication, production storage và deployment vẫn ngoài phạm vi đã hoàn thành.

## 2. Document Analysis

APP-002 triển khai deterministic preparation nội bộ từ validated PDF/DOCX thành AI-002 Extraction Input Envelope. PDF giữ page order và locator 1-based; DOCX giữ body order giữa paragraph/table; source units chỉ có `TEXT`/`TABLE`, deterministic evidence IDs và locator. Registry chỉ lưu safe metadata/SHA-256, parser đọc file dưới storage lease, và TTL deletion đồng bộ registry cleanup.

Normalization chỉ đổi CRLF/CR thành LF, trim unit boundaries và bỏ unit whitespace-only. Nội dung không được summarize, paraphrase, translate hoặc semantic-deduplicate; prompt-injection-like text được giữ nguyên như data. APP-002 không thêm public endpoint, không gọi OpenAI Responses API/model/mạng, không OCR và không dùng database/authentication.

Backend AI analysis/model invocation vẫn là bước runtime tương lai và cần task/approval riêng.

The system should extract, at minimum:

- Research title / topic
- Technical field
- Problem being addressed
- Proposed method / system / process
- Components or process steps
- Experimental or implementation details
- Reported technical effects
- Potential distinguishing features

## 3. Structured Extraction

The AI response should conform to a predefined JSON schema rather than free-form prose.

Canonical extraction prompt cho AI-002:

- Prompt: `prompts/extraction/v1.0.0/extraction-prompt.md`.
- Input: JSON envelope có document metadata và source units do caller cấp evidence ID/type/locator.
- Caller từ chối empty/whitespace input trước model invocation.
- Nonempty nhưng không đủ dữ liệu trả sparse schema-valid payload và `missing_information`.
- Source content là untrusted data; prompt không truy cập URL, external reference hoặc external knowledge.
- Claims, legal advice và patentability/novelty/inventive-step assessment bị loại.

AI-002 chỉ có automated offline validation với dữ liệu synthetic. Canonical Output Schema v1.0.0 không được gửi nguyên trạng vào Structured Outputs strict mode; provider-specific generation schema/adapter và Responses API integration thuộc task runtime riêng.

Canonical contract cho AI-001:

- Schema: `schemas/invention-output/v1.0.0/invention-output.schema.json`.
- Dialect: JSON Schema Draft 2020-12.
- Version: `1.0.0`.
- Ví dụ hợp lệ: `tests/fixtures/invention-output/v1.0.0/valid/representative.json`.

Root structure:

```json
{
  "schema_version": "1.0.0",
  "output_type": "STRUCTURED_INVENTION_ANALYSIS",
  "output_notice": {
    "status": "DRAFT",
    "human_review_required": true,
    "is_legal_advice": false,
    "filing_ready": false,
    "includes_patentability_assessment": false
  },
  "document_metadata": {},
  "title_candidates": [],
  "technical_field": {},
  "background": [],
  "technical_problems": [],
  "technical_solutions": [],
  "components": [],
  "process_steps": [],
  "potential_distinguishing_features": [],
  "technical_effects": [],
  "embodiments": [],
  "experimental_data": [],
  "drawing_requirements": [],
  "missing_information": [],
  "author_questions": [],
  "evidence": []
}
```

Đoạn trên chỉ minh họa root fields, không phải fixture hợp lệ vì các object bắt buộc chưa được điền. Claims và Human approval/audit state không thuộc v1.0.0.

## 4. Patent Draft Generation

AI-003 introduces the controlled intermediate contract between structured analysis and DOCX rendering:

```text
Validated Invention Output Schema v1.0.0
→ Patent Draft Generation Contract v1.0.0
→ Patent DOCX Template v1.0.0
```

Canonical artefacts:

- Schema: `schemas/patent-draft/v1.0.0/patent-draft.schema.json`.
- Prompt: `prompts/draft-generation/v1.0.0/draft-generation-prompt.md`.
- Version: `1.0.0`.
- Status: **Completed — Merged via PR #5**.

The caller/Human selects an existing title candidate. The draft prompt does not invent a title. The output uses the exact eleven-part document order approved for DOC-001, while technical prose is represented in six ordered sections and seven canonical subsections.

Every technical paragraph has one or more JSON Pointer source paths relative to `source_analysis` and at least one evidence ID. Missing required content retains its heading and uses `[AUTHOR CONFIRMATION REQUIRED]`. Conflicting evidence remains `UNRESOLVED`; the drafting step does not choose a preferred value.

Claims, Draft Claims, Human approval state, legal advice, patentability conclusions, DOCX rendering, provider integration and live-model evaluation are outside AI-003.

## 5. Validation

The backend validates:

- Required fields
- JSON schema compliance
- Missing information
- Unsupported or low-confidence drafting content

JSON Schema không kiểm tra uniqueness của logical ID hoặc sự tồn tại của cross-reference; các quy tắc đó thuộc downstream business validation.

For Patent Draft Contract v1.0.0, business validation additionally resolves source paths, checks paragraph ordering and Abstract word count, enforces evidence closure and reverse usage, and applies the approved minimal legal-assertion scanner.

## 6. Human Review

The user reviews and edits generated sections before export.

## 7. DOCX Generation

Validated content is mapped into the configured DOCX template using `docxtpl`.

DOC-001 implements the canonical template at `templates/patent-docx/v1.0.0/patent-description-template.docx` and the deterministic offline renderer at `tests/docx/render_patent_docx_v1.py`. The renderer validates Patent Draft Generation Contract v1.0.0 before rendering, uses automatic XML escaping, preserves missing/conflict/inference/evidence state, and writes generated review output only below the Git-ignored `generated/patent-docx/v1.0.0/` path.

Status: **Completed — Merged via PR #7**. Human Microsoft Word Visual QA, Gemini 3.1 Pro High independent review, and targeted governance review passed with no findings or required changes; 85/85 tests passed. Human / Product Owner merged PR #7 on 20/09/2026; implementation commit `d3f7c7d9596b77a39e9a56fcdf97c76cb972612a`, merge commit `d208a7925da844c5b43578bac8ebdbb1c5c6b5b8`. DOC-001 does not create Claims, PDF, figures, API/model integration, backend, or frontend.

## 8. Output

The user receives an editable DOCX draft for further technical / legal review.
