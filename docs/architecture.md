# System Architecture

## Objective

Transform a scientific research paper into a structured intellectual-property / patent-description draft while preserving traceability, deterministic structure, and human review.

## Core Components

### Frontend

**Next.js + TypeScript**

Responsibilities:

- Accept user uploads
- Show processing state
- Display structured AI output
- Allow review / correction
- Request final DOCX export

### Backend

**FastAPI + Python**

Responsibilities:

- Validate uploaded files
- Orchestrate AI calls
- Apply prompt and schema versions
- Validate structured results
- Generate documents
- Return downloadable output

### AI Layer

**OpenAI Responses API**

Primary use:

- Analyze uploaded research papers
- Extract technical information
- Convert research-oriented language into invention-oriented structured data
- Produce constrained outputs using a predefined schema

### Document Generation

**docxtpl**

The backend maps structured fields into a controlled DOCX template.

## Data Flow

```text
Upload
  ↓
Validation
  ↓
AI Analysis
  ↓
Structured JSON
  ↓
Schema Validation
  ↓
Human Review
  ↓
Template Mapping
  ↓
DOCX Export
```

## Reliability Requirements

1. Do not silently invent missing technical facts.
2. Separate source-derived facts from model-generated drafting language.
3. Flag missing or ambiguous information for human review.
4. Keep prompt and schema versions reproducible.
5. Avoid exposing API keys to the browser.
