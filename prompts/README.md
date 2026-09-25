# Prompts / Câu lệnh AI

**Nhiệm vụ / Responsibilities**

- Lưu prompt production theo semantic version.
- Quy định input/output, grounding, uncertainty và injection resistance.
- Tách extraction prompt và draft-generation prompt theo artefact/version.
- Mọi thay đổi prompt phải có task/review/test tương ứng.

---

This directory contains version-controlled prompt specifications used by the AI pipeline.

Planned prompt groups:

- Research-paper extraction
- Invention-oriented technical analysis
- Patent-description section generation
- Validation / unsupported-claim detection
- Claim-support information extraction

Canonical extraction prompt:

- `extraction/v1.0.0/extraction-prompt.md` — AI-002, Completed — Merged via PR #3 ngày 19/09/2026; Gemini review `PASS`, không có finding.
- `extraction/v1.0.0/README.md` — input/output contract and integration limits.

Canonical draft-generation prompt:

- `draft-generation/v1.0.0/draft-generation-prompt.md` — AI-003, Completed — Merged via PR #5.
- `draft-generation/v1.0.0/README.md` — input/output boundary, grounding and integration limits.

Recommended versioning:

```text
prompts/
├── extraction/
│   └── v1.0.0/
├── draft-generation/
│   └── v1.0.0/
└── README.md
```

Prompts should be treated as application logic and tested against a fixed evaluation set.

AI-002 uses only synthetic offline fixtures. It does not call a live model or claim provider integration.

AI-003 also uses only synthetic offline fixtures. Its expected outputs are test oracles, not evidence of live-model behavior. Claims, legal conclusions, provider integration and DOCX rendering are outside AI-003.
