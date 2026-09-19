# Prompts

This directory contains version-controlled prompt specifications used by the AI pipeline.

Planned prompt groups:

- Research-paper extraction
- Invention-oriented technical analysis
- Patent-description section generation
- Validation / unsupported-claim detection
- Claim-support information extraction

Canonical extraction prompt:

- `extraction/v1.0.0/extraction-prompt.md` — AI-002, implemented and awaiting independent review.
- `extraction/v1.0.0/README.md` — input/output contract and integration limits.

Recommended versioning:

```text
prompts/
├── extraction/
│   └── v1.0.0/
└── README.md
```

Prompts should be treated as application logic and tested against a fixed evaluation set.

AI-002 uses only synthetic offline fixtures. It does not call a live model or claim provider integration.
