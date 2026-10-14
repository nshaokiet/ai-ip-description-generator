# AI-CONV-002 — Offline orchestration implementation handoff

| Attribute | Value |
|---|---|
| Document version | 0.1.0 |
| Status | IMPLEMENTED — INDEPENDENT FIXED-SHA REVIEW PENDING |
| Workflow | V1 |
| Human authorization | `HUMAN-AI-CONV-002-OFFLINE-WORKFLOW-V1-2026-10-14`; [Issue #111](https://github.com/nshaokiet/ai-ip-description-generator/issues/111) |
| Authorized baseline | `d358018e093a8db4161afb6d9caecfa51c8e00d3` |
| Frozen architecture | `AI-CONV-001-source-grounded-uspto-v2-orchestration.md` v0.1.1 |
| Implementation branch | `feat/ai-conv-002-offline-orchestration` |
| Data boundary | Offline synthetic/authorized inputs only |

## Implemented boundary

`OfflineUSPTOOrchestrator` is an additive internal service. It is not registered with FastAPI and does not change any public route, frontend type, released schema, prompt, renderer, provider configuration or deployment file.

Primary interfaces:

- `start_session(...)`: validate/canonicalize the APP-002 envelope, retain both explicit generation configurations and create revision 1 in `SOURCE_READY`.
- `run_uspto_v2_offline_pipeline(...)`: create a session and execute P2-002 → P2-003 → P2-004 → P2-005, with optional P2-006 rendering.
- `advance_session(session_id, expected_revision_token, output_dir=None)`: resume only the current revision and advance monotonically.
- `validate_session(...)`: recompute session integrity and validate P2-005 using all seven retained upstream objects.
- `render_session(...)`: render from a current `PACKAGE_VALID` session only; there is no package-only rendering method.
- `revise_session(...)`: create a new revision, issue a new immutable token and invalidate outputs from the earliest affected stage.
- `get_session_status(...)`: return safe source identity, stage, digests, package identity and path-free render metadata without source prose.
- `get_validated_package(...)`: return a deep copy only after complete seven-input revalidation.
- `cleanup_session(...)`: verify and remove only the four recorded P2-006 files and their dedicated output directory, then erase the in-memory session.

The manager is bounded to 32 sessions by default (configurable from 1 through 256), uses an in-process lock and has no persistence. It stores no authentication, tenant or production retention policy.

## Provenance and revision integrity

The retained authoritative bundle contains these exact keys:

1. `source_envelope`
2. `structured_analysis`
3. `reconstruction`
4. `specification`
5. `p2_003_generation_config`
6. `supported_claims`
7. `p2_004_generation_config`

Canonical SHA-256 values use the released canonical JSON helper. Digests are checked before every transition, validation, package read, render and cleanup. They are indexes only: P2-005/P2-006 always receive full deep-copied objects. The service explicitly calls `validate_uspto_document_package(package, **seven_inputs)` after assembly, and rendering revalidates the same objects before calling `render_uspto_document_package`.

Revision invalidation is deterministic:

| Changed input | New state | Discarded outputs |
|---|---|---|
| APP-002 envelope or structured analysis | `SOURCE_READY` | Reconstruction through render |
| P2-003 generation config | `RECONSTRUCTION_READY` | Specification through render |
| P2-004 generation config | `SPECIFICATION_READY` | Supported Claims through render |

Old revision tokens return `STALE_REVISION`. Missing retained objects, canonical digest changes, package tampering and cross-document artifacts fail closed. Actual stage failure moves that revision to `FAILED`; source-derived exception text is not returned.

## Claims behavior

No Claims semantics changed. The authentic-style APP-002 fixture reconstructs P2-002 elements with `essentiality=UNKNOWN`; P2-004 therefore returns no eligible Claims. The session records `CLAIMS_REVIEW_REQUIRED`, while P2-005 remains valid with:

- `filing_view.claims.status = HUMAN_CONFIRMATION_REQUIRED`;
- `filing_view.claims.claims = []`;
- `review_boundary.p2_003_claims_runtime_implemented = false`;
- the released P2-006 incomplete-Claims marker in every rendered format.

METHOD/PROCESS/COMPOSITION authority is not inferred. The separately released positive P2-004 synthetic component fixture remains covered by its unchanged regression suite.

## Security and failure behavior

- The module imports no HTTP, provider, retrieval, database or subprocess client.
- Sessions and full provenance remain private in process and are deep-copy isolated at service boundaries.
- Status includes `document_id` and source SHA-256, but excludes source text, file name and filesystem paths.
- Errors have stable codes, fixed safe messages and bounded contract paths.
- The released renderer rejects relative, missing and symlinked output roots and atomically publishes exactly four files.
- The session manifest retains only filename, file SHA-256 and byte size. Cleanup refuses unknown, changed, missing or symlinked output entries.
- No real/confidential paper, paid API, provider runtime, new dependency, Render change or deployment was used.

## Validation evidence

Commands run from the isolated worktree:

```text
python -m pytest tests/backend/test_uspto_offline_orchestration.py -q -p no:cacheprovider
22 passed

python -m pytest <P2-002…P2-006 schema/service suites plus orchestration> -q -p no:cacheprovider
360 passed, 1 host-library deprecation warning

PYTHONUTF8=1 PYTHONIOENCODING=utf-8 RUN_OPENAI_LIVE_TESTS=0 RUN_OPENAI_DRAFT_LIVE_TESTS=0 \
python -m pytest tests -q -p no:cacheprovider
941 passed, 3 skipped, 1 host-library deprecation warning
```

The first full Windows run without forced UTF-8 reached 939 passed / 3 skipped and one unchanged governance CLI test failure. The child process emitted CP1252 while the test decoded as UTF-8. Its isolated rerun passed under the UTF-8 environment used for the final rerun. This was a local host encoding issue; no application or test source was changed to mask it.

## Review handoff and remaining gates

The independent reviewer must inspect the exact final implementation SHA and report the actual Antigravity model/profile, session ID, findings and `PASS` / `REQUEST CHANGES` / `BLOCKED` verdict. Reviewer selection is pending explicit Human authorization for AI-CONV-002 and cannot be inherited from AI-CONV-001.

Merge remains blocked until fixed-SHA review PASS, exact-head CI SUCCESS, complete scope/secret checks and fresh Workflow V1 merge preflight. AI-CONV-003/004/005/006, Phase H/V2 enrollment, provider/runtime work, real/confidential data, production security and deployment remain separately gated.
