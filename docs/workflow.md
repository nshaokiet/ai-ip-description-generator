# MVP Processing Workflow

## 1. User Upload

Accepted initial formats:

- PDF
- DOCX

## 2. Document Analysis

The backend sends the document through the AI analysis pipeline.

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
- Status: **Gemini Review Passed — Awaiting Human Merge Approval**.

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

DOC-001 must not start until AI-003 has completed independent review, Human approval and merge.

## 8. Output

The user receives an editable DOCX draft for further technical / legal review.
