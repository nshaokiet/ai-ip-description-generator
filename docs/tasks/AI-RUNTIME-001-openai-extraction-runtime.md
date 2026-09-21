# AI-RUNTIME-001 — OpenAI Responses API + Structured Outputs Extraction Runtime

## Metadata

| Thuộc tính | Giá trị |
|---|---|
| Task ID | AI-RUNTIME-001 |
| Specification version | 1.0.0 |
| Status | F-001 Remediated — Awaiting Targeted Re-review |
| Owner | ChatGPT/Codex |
| Reviewer | Gemini 3.1 Pro High + Human / Product Owner |
| Human decision | APPROVED — 21/09/2026 |
| Approved baseline | `f8070a5c94290ff44c65bc1b0831458662e14e11` |
| Specification review | Initial `REQUEST CHANGES`; targeted re-review `PASS`; no remaining blocker |
| Implementation review | `PASS WITH NON-BLOCKING NOTES`; F-001 `MEDIUM` remediated; F-002 `NOTE` live smoke remains not run |

## Objective

Convert an APP-002 `ExtractionInputEnvelope` into a validated AI-001 Structured Invention Analysis through this internal boundary:

```text
AI-002 Extraction Input Envelope
→ OpenAI Responses API / gpt-5.6-sol / reasoning high
→ strict provider schema generated from canonical AI-001
→ schema-aware nullable normalization
→ canonical Draft 2020-12 validation
→ deterministic grounding/business validation
→ validated analysis + separate safe runtime metadata
```

Provider output is never canonical truth until both canonical and grounding/business validation succeed.

## Scope

### In scope

- Internal, stateless OpenAI Responses API service with one logical model invocation.
- Exact SDK/model/runtime policy: `openai==3.16.2`, `gpt-5.6-sol`, reasoning `high`, `store=False`, timeout 180 seconds, SDK retries 2 and 48.000 output tokens.
- Deterministic provider-schema adapter derived from AI-001.
- Schema-aware optional-null normalization without content rewriting.
- `jsonschema==4.26.0` `Draft202012Validator` canonical validation.
- Evidence provenance, exact excerpt, logical-ID and cross-reference validation.
- Safe error taxonomy, safe operational logging and separate runtime metadata.
- Mocked synthetic offline tests and an opt-in synthetic live smoke test.
- ADR-010 and targeted project-state synchronization.

### Out of scope

- Public analyze endpoint, frontend, database, auth, production storage, deployment, OCR/vision, Web Search, File Search, other retrieval, embeddings/vector DB, queue/worker, draft runtime, DOCX export API, Claims, prior-art search, patentability/legal conclusions and real research data.
- Changes to AI-001 schema, AI-002 prompt, AI-003 contract/prompt or DOC-001 template.

## Runtime contract

- Input: strict APP-002 `ExtractionInputEnvelope`.
- Output: `ExtractionRuntimeResult` containing canonical `analysis` and separate `runtime` metadata.
- Canonical prompt and schema are loaded from their versioned repository paths.
- Source content remains data only; it is never concatenated into instruction authority.
- Success requires completed response, parseable JSON object, canonical validation and business validation.

## Provider-schema decisions

- Every provider object is closed and requires every defined property.
- Canonical optional properties become required plus nullable at provider level.
- Conditional `allOf` is deferred to canonical post-validation while base schema remains.
- Non-conditional `allOf` is deterministically resolved/merged; unsafe conflicts fail before a model call.
- `oneOf` becomes supported nested `anyOf`; nested compatible `anyOf` remains.
- `evidence_locator` presence logic is deferred through required-nullable locator fields.
- `uniqueItems` is omitted only at provider layer and remains enforced by canonical validation.
- Root `anyOf` and unsupported conditional composition are rejected.

## Grounding/business rules

- Output document ID, filename and media type equal input; emitted SHA-256 equals input.
- Every emitted evidence ID exists in input and copies exact document ID, type and locator.
- Evidence excerpt is an exact contiguous Python substring of source-unit content.
- Every grounding reference resolves to caller input and an emitted evidence record.
- Logical IDs are unique across applicable output collections.
- Problem, component, step, solution, missing-information and drawing evidence references resolve deterministically.
- Semantic adequacy and correctness of grounding labels remain Human/model-quality review concerns.

## Safe errors

`runtime_not_configured`, `provider_timeout`, `provider_connection_error`, `provider_rate_limited`, `provider_request_rejected`, `provider_error`, `model_refusal`, `model_incomplete`, `response_parse_failed`, `provider_schema_failed`, `canonical_validation_failed`, `grounding_validation_failed`.

Safe messages and logs do not expose credentials, source content, prompt, provider output, evidence excerpt, traceback or absolute path.

## Acceptance criteria

- [x] AC-01 — Implementation is based on `f8070a5c94290ff44c65bc1b0831458662e14e11`.
- [x] AC-02 — This v1.0.0 task specification exists.
- [x] AC-03 — `openai==3.16.2` is pinned.
- [x] AC-04 — `jsonschema==4.26.0` is pinned.
- [x] AC-05 — `gpt-5.6-sol` is fixed in production configuration.
- [x] AC-06 — Reasoning effort `high` is fixed in production configuration.
- [x] AC-07 — Runtime uses `client.responses.create`.
- [x] AC-08 — Every request explicitly sends `store=False`.
- [x] AC-09 — No tool, Web/File Search or external retrieval is enabled.
- [x] AC-10 — Canonical AI-002 prompt is loaded from its versioned file.
- [x] AC-11 — Serialized APP-002 envelope is separate untrusted input.
- [x] AC-12 — Canonical AI-001 schema is unchanged.
- [x] AC-13 — Provider schema is derived deterministically from canonical AI-001.
- [x] AC-14 — Adapter covers actual conditional/compositional `allOf`, `oneOf`, nested `anyOf`, `uniqueItems` and optional semantics.
- [x] AC-15 — Every provider object is strict and all properties are required.
- [x] AC-16 — Canonical optional properties map to provider nullable-required semantics.
- [x] AC-17 — Normalization is deterministic and canonical-schema-aware.
- [x] AC-18 — Canonical `Draft202012Validator` validation is mandatory.
- [x] AC-19 — Deterministic grounding/business validation is mandatory.
- [x] AC-20 — Invented evidence IDs are rejected.
- [x] AC-21 — Evidence document/type/locator mismatch is rejected.
- [x] AC-22 — Modified, case-changed and non-contiguous excerpts are rejected.
- [x] AC-23 — Incomplete responses fail closed.
- [x] AC-24 — Refusals fail closed.
- [x] AC-25 — Provider/API failures map to safe runtime errors.
- [x] AC-26 — Timeout defaults to 180 seconds and validates range 30–300.
- [x] AC-27 — SDK retries equal 2 and no application retry loop exists.
- [x] AC-28 — Default/approved maximum output budget is 48.000 tokens.
- [x] AC-29 — Secret, source, prompt and full provider output are not logged.
- [x] AC-30 — Live provider smoke is opt-in and synthetic-only.
- [x] AC-31 — No public endpoint or other out-of-scope system is added.
- [x] AC-32 — Existing regressions and new AI-RUNTIME-001 offline tests pass.

## Validation commands

```powershell
$env:PYTHONDONTWRITEBYTECODE="1"
.\.venv\Scripts\python.exe -m unittest discover -s tests/schema -p "test_*.py" -v
.\.venv\Scripts\python.exe -m unittest discover -s tests/prompt -p "test_*.py" -v
.\.venv\Scripts\python.exe -m unittest discover -s tests/draft -p "test_*.py" -v
.\.venv\Scripts\python.exe -m unittest discover -s tests/docx -p "test_*.py" -v
.\.venv\Scripts\python.exe -m unittest discover -s tests/backend -p "test_*.py" -v
.\.venv\Scripts\python.exe -m pip check
git diff --check
```

Live verification is separate and must not be represented as PASS without credential-backed execution:

```powershell
$env:RUN_OPENAI_LIVE_TESTS="1"
.\.venv\Scripts\python.exe -m unittest tests.live.test_openai_extraction_runtime_live -v
```

## Security and open blockers

- Fixtures and offline/live smoke input are synthetic only.
- `BLK-004` is resolved only for Extraction Runtime v1.
- `BLK-003` remains open; real research data and production usage remain blocked.
- Human review is mandatory; this runtime does not produce legal advice, claims or patentability conclusions.

## Implementation evidence

- Python 3.12.10; `openai==3.16.2`; `jsonschema==4.26.0`; `pip check` PASS.
- New AI-RUNTIME-001 offline tests: 66/66 pass, including optional-SHA F-001 regression coverage.
- Full suites: AI-001 15/15, AI-002 17/17, AI-003 25/25, DOC-001 28/28, backend 116 executed / 115 pass / 1 intentional Windows POSIX skip.
- Aggregate: 201 executed / 200 pass / 1 skip / 0 failure/error.
- Live provider smoke: `NOT RUN — OPENAI_API_KEY not available`.
- Canonical AI-001 schema and AI-002 prompt have no diff.
