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

Example conceptual structure:

```json
{
  "invention_title": "",
  "technical_field": "",
  "background": "",
  "technical_problem": "",
  "technical_solution": "",
  "novel_features": [],
  "technical_advantages": [],
  "embodiments": [],
  "missing_information": []
}
```

## 4. Validation

The backend validates:

- Required fields
- JSON schema compliance
- Missing information
- Unsupported or low-confidence drafting content

## 5. Human Review

The user reviews and edits generated sections before export.

## 6. DOCX Generation

Validated content is mapped into the configured DOCX template using `docxtpl`.

## 7. Output

The user receives an editable DOCX draft for further technical / legal review.
