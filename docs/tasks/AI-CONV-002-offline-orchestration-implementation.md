# AI-CONV-002 — Offline orchestration implementation handoff

| Attribute | Value |
|---|---|
| Document version | 0.1.1 |
| Status | REMEDIATED CANDIDATE — NEW FIXED-SHA REVIEW REQUIRED |
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

These reset states are upper bounds: without a retained reconstruction the new state is `SOURCE_READY`; without a retained specification it is `RECONSTRUCTION_READY`. No revision creates a ready state from missing prerequisites.

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

Historical candidate handoff (superseded by the remediation record below): the independent reviewer must inspect the exact final implementation SHA and report the actual Antigravity model/profile, session ID, findings and `PASS` / `REQUEST CHANGES` / `BLOCKED` verdict. Reviewer selection is pending explicit Human authorization for AI-CONV-002 and cannot be inherited from AI-CONV-001.

Merge remains blocked until fixed-SHA review PASS, exact-head CI SUCCESS, complete scope/secret checks and fresh Workflow V1 merge preflight. AI-CONV-003/004/005/006, Phase H/V2 enrollment, provider/runtime work, real/confidential data, production security and deployment remain separately gated.


## MEDIUM-01 / MEDIUM-02 remediation — 2026-10-15

Document **0.1.0 → 0.1.1**; internal orchestration contract **1.0.0 → 1.0.1**.
Author: Codex. Reason: [confirmed blocker receipt](https://github.com/nshaokiet/ai-ip-description-generator/pull/112#issuecomment-6182824064) and explicit Human remediation instruction. Breaking change: **No**; released stage/API/schema contracts are unchanged.

- **MEDIUM-01 — ACCEPT / remediated pending independent review:** readiness now follows the actual retained validated reconstruction/specification after downstream invalidation. Initial, intermediate, completed and failed-stage recovery cases are tested, including both configs changed together. Missing upstream outputs are not manufactured by revision preparation.
- **MEDIUM-02 — ACCEPT / remediated pending independent review:** prepare an isolated candidate; reject non-JSON types, non-string keys, cycles and nonfinite numbers before coercion; validate source/analysis and both configs using released validators, verify retained upstream artifacts and config agreement; compute candidate digests/token/status before filesystem cleanup. Only verified cleanup success permits replacing the live record under its existing lock. No candidate-validation failure changes the prior record, token, package, timestamps, manifest or output bytes.
- Invalid canonical input uses `INVALID_CANONICAL_INPUT`; semantic/config/preparation errors use source-safe `INVALID_REVISION_INPUT`. Both are caller rejection, not failure of the valid live revision.
- Cleanup failure explicitly marks the old revision `FAILED` with `CLEANUP_FAILED`; candidate inputs/revision/token are never committed. Filesystem deletion is not transactional: injected failures after 0/1/3 deletes are covered. Partial deletion preserves the original manifest as evidence and blocks integrity-dependent operations. External filesystem recovery is required for partially deleted artifacts; no rollback or automatic successful cleanup is claimed.
- The seven original provenance objects, strict P2-005/P2-006 boundaries, no-Claims behavior and draft status remain unchanged. Source/config edits must still be mutually compatible; revision does not silently repair a stale nested P2-003 config in P2-004 input.

### Review attribution and LOW reconciliation

[Original PASS receipt](https://github.com/nshaokiet/ai-ip-description-generator/pull/112#issuecomment-6182751500) is historical for `beb69bf9ff0972b27147c62a938323a74f3a0193`, and predates the two confirmed blockers. It is not PASS for this remediation. Reviewer: **Gemini 3.8 Flash High / Antigravity STRICT READ-ONLY** under the Human standing authorization. Reported conversation ID `82c3975a-d2a2-446b-b2aa-7d1353d1d4b0` was reused; no distinct new conversation is established. The external report attributes 22 newly executed tests and 302 prior regression tests; it is not authenticated GitHub-native approval.

- **LOW inventory:** collection on original SHA `beb69bf9` independently reproduces **360 collected** using the six backend service/orchestration files (302), the two P2 schema files (42), and synthetic delivery (16). This identifies a reproducible inventory; collection is not a rerun of the historical 360 PASS. The 302 prior reviewer run remains separately attributed. Exact paths are below.
- **LOW Windows temp locking:** tests may use an absolute, unique disposable scratch `--basetemp` outside tracked files if host locking occurs. Never point it at an existing valuable directory: pytest can clear that directory. No source change or release/security exception is implied.

### Remediation validation and remaining gates

Validation results are recorded in the final PR remediation handoff with exact commands and candidate SHA. New independent review and exact-new-SHA CI are mandatory; old PASS/CI cannot transfer. No merge/deploy/Issue #111 closeout is authorized by this handoff. AI-CONV-003+, Phase H/V2, paid providers and confidential data remain excluded.

MCP read returned `Unknown task: AI-CONV-002`; task lease/progress transition is **BLOCKED BY TOOL CAPABILITY**. Git/PR evidence remains authoritative; no MCP lease or lifecycle change is fabricated.


Reproducible historical 360-case collection (original SHA; not a fresh execution result):

```text
python -m pytest --collect-only -q -p no:cacheprovider
  tests/backend/test_invention_reconstruction.py
  tests/backend/test_uspto_specification_generation_v2.py
  tests/backend/test_supported_draft_claims_v1.py
  tests/backend/test_uspto_document_package_v1.py
  tests/backend/test_uspto_offline_renderer.py
  tests/backend/test_uspto_offline_orchestration.py
  tests/schema/test_invention_reconstruction_v1.py
  tests/schema/test_uspto_specification_v2.py
  tests/backend/test_uspto_synthetic_delivery.py
```

Join the displayed command/path lines into one shell command. For the six-file 302 inventory, omit the last three paths. The same files collect more cases on the remediation SHA because of the added regressions.


Local remediation validation (Windows, Python 3.14.6, Node 24.18.0):

- `python -m pytest tests/backend/test_uspto_offline_orchestration.py -q -p no:cacheprovider`: **88 passed** on the final implementation (66 added regression cases).

- `PYTHONUTF8=1`, `PYTHONIOENCODING=utf-8`, `PYTHONDONTWRITEBYTECODE=1`, `RUN_OPENAI_LIVE_TESTS=0`, `RUN_OPENAI_DRAFT_LIVE_TESTS=0`; `python -m pytest tests -q -p no:cacheprovider`: **1007 passed, 3 skipped**, one existing host Starlette/AnyIO deprecation warning. Includes all **88 orchestration cases** (22 original + 66 remediation cases).
- `python -m pytest` with `tests/backend/test_invention_reconstruction.py`, `test_uspto_specification_generation_v2.py`, `test_supported_draft_claims_v1.py`, `test_uspto_document_package_v1.py`, `test_uspto_offline_renderer.py` (all under `tests/backend/`), plus `tests/schema/test_invention_reconstruction_v1.py` and `tests/schema/test_uspto_specification_v2.py`, flags `-q -p no:cacheprovider`: **322 passed**. This deliberately excludes orchestration and synthetic-delivery cases, which are covered in the full suite.
- Frontend `npm run lint`, `npm run typecheck`, `npm run build`: **PASS**. `npm run test:lint-security`: **73/73 passed**. `npm audit` and `npm audit --omit=dev`: **0 vulnerabilities** each. `python -m pip check`: no broken requirements.
- `git diff --check`, six-file scope guard and added-line credential/private-key marker scan: **PASS**. Marker scan is not an exhaustive secret detector.
- Initial sandbox npm installation failed on cache/network access; retry using a task-specific temporary cache and approved sandbox escalation succeeded. No dependency/lockfile changes. Browser E2E and Linux document layout/reference QA are required in exact-head GitHub CI, not claimed as local Windows executions.
