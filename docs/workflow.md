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

## 4. Validation

The backend validates:

- Required fields
- JSON schema compliance
- Missing information
- Unsupported or low-confidence drafting content

JSON Schema không kiểm tra uniqueness của logical ID hoặc sự tồn tại của cross-reference; các quy tắc đó thuộc downstream business validation.

## 5. Human Review

The user reviews and edits generated sections before export.

## 6. DOCX Generation

Validated content is mapped into the configured DOCX template using `docxtpl`.

## 7. Output

The user receives an editable DOCX draft for further technical / legal review.
