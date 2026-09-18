# AI Intellectual Property Description Generator

> AI-powered platform for converting scientific research papers into structured intellectual property / patent description drafts for human review.

## Project Overview

The project aims to build a web-based AI platform where a user uploads a scientific research paper (PDF/DOCX), the system analyzes the technical content, extracts invention-relevant information, maps it into a predefined patent-description structure, and generates an editable DOCX draft.

### Input

- Scientific research paper (PDF/DOCX)
- Optional reference documents / templates
- Optional metadata supplied by the user

### Target Output

A structured draft containing fields such as:

- Proposed invention title
- Technical field
- Background / existing technical problem
- Technical objective
- Proposed technical solution
- Main components / process steps
- Novel or distinguishing technical features
- Technical advantages / effects
- Detailed embodiments / implementation examples
- Information supporting later claim drafting
- Exportable DOCX document based on a predefined template

> **Important:** Generated content is a drafting aid and must be reviewed by a qualified human before any filing or legal use.

## High-Level Workflow

```text
Research Paper
      ↓
File Upload
      ↓
Document Parsing / AI File Analysis
      ↓
Structured Technical Information Extraction
      ↓
Invention-Oriented Analysis
      ↓
Patent Description Mapping
      ↓
Validation / Human Review
      ↓
DOCX Export
```

## Proposed Architecture

```text
Frontend (Next.js + TypeScript)
        ↓
Backend (FastAPI + Python)
        ├── OpenAI Responses API
        ├── Structured Outputs
        ├── Validation
        └── docxtpl
                ↓
            DOCX Export

Optional MVP+:
Supabase / PostgreSQL for projects, metadata and versions
```

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js, TypeScript |
| Backend | FastAPI, Python |
| AI | OpenAI Responses API |
| Structured AI output | Structured Outputs / JSON Schema |
| File retrieval (optional phase) | OpenAI File Search |
| Database (MVP+) | Supabase / PostgreSQL |
| Document generation | docxtpl |
| Frontend deployment | Vercel |
| Backend deployment | Railway |
| Version control | GitHub |

## MVP Scope

The first milestone intentionally focuses on the shortest useful pipeline:

```text
1 research paper
      ↓
AI analysis
      ↓
structured JSON
      ↓
patent-description draft
      ↓
DOCX export
```

### MVP Priorities

1. Upload one scientific paper.
2. Analyze the paper with the OpenAI API.
3. Extract invention-relevant technical information into a fixed schema.
4. Prevent unsupported details from being silently invented.
5. Map structured data into the target description template.
6. Preview / review generated sections.
7. Export an editable DOCX draft.
8. Test the pipeline on representative research papers.

### Deferred Until the Core Pipeline Works

- User authentication
- Multi-user roles
- Full project/version history
- Advanced search across large patent corpora
- Automated prior-art conclusions
- Production-scale database workflows
- Complex billing / subscription logic

## Repository Structure

```text
ai-ip-description-generator/
│
├── frontend/       # Next.js web application
├── backend/        # FastAPI API and AI orchestration
├── prompts/        # Versioned prompt specifications
├── templates/      # DOCX / output templates
├── docs/           # Architecture, workflow and project documentation
├── tests/          # Test cases and evaluation scenarios
├── .github/        # GitHub collaboration templates
├── .env.example    # Environment variable template
├── .gitignore
└── README.md
```

## Design Principles

1. **Structured output first** — core extraction should follow a fixed schema instead of uncontrolled prose.
2. **Traceability** — important generated statements should be traceable to source content where possible.
3. **Human-in-the-loop** — the system assists drafting; it does not replace technical or legal review.
4. **Prompt versioning** — prompts are version-controlled under `prompts/`.
5. **Modular architecture** — frontend, backend, prompts and templates evolve independently.

## Initial Roadmap

### Phase 1 — Foundation
- [x] Initialize repository
- [x] Define architecture and MVP scope
- [ ] Initialize Next.js frontend
- [ ] Initialize FastAPI backend
- [ ] Configure environment variables

### Phase 2 — Core AI Pipeline
- [ ] Upload PDF/DOCX
- [ ] Send document to AI analysis pipeline
- [ ] Define structured extraction schema
- [ ] Implement invention-oriented extraction
- [ ] Add source-grounding / validation rules

### Phase 3 — Document Generation
- [ ] Finalize target IP / patent description template
- [ ] Map structured data to template fields
- [ ] Generate DOCX with docxtpl
- [ ] Add preview and manual editing flow

### Phase 4 — Evaluation & Deployment
- [ ] Test with representative research papers
- [ ] Add regression test cases
- [ ] Deploy frontend to Vercel
- [ ] Deploy backend to Railway
- [ ] Add Supabase if persistence is required

## Current Status

**Stage:** Architecture / MVP setup

The repository currently contains the proposed project structure and documentation. Application implementation will be added incrementally after the target output template and AI extraction schema are confirmed.
