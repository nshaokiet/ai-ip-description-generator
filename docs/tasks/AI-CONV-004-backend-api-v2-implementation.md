# AI-CONV-004-IMPL — Candidate A Backend API v2 implementation

| Field | Value |
|---|---|
| Task | AI-CONV-004-IMPL / Issue #123 |
| Version | 0.1.0 |
| Status | IMPLEMENTATION IN PROGRESS — Draft PR, CI and independent fixed-SHA review required; STOP before merge |
| Workflow | V1 |
| Authorization | `HUMAN-AI-CONV-004-CANDIDATE-A-IMPLEMENTATION-2026-10-17` |
| Frozen contract | AI-CONV-004 specification v0.1.3, blob `cdee9c041932ec911cd84dd1c16ab7dbb5bb7f94` |
| Baseline | `main` merge `34c457100127f3f3954aa0fdc0a13791e40e998a` |
| Data/runtime | Synthetic-only, offline, in-memory, single process; no provider, real research data, deployment or product Claims runtime |
| Breaking change | No — released/default v1 application remains unchanged |

## Implemented boundary

`backend/app/api/local_synthetic_v2.py` contains a deliberately isolated ASGI
proof-of-contract. `backend.app.main` does not import or register it. The
dedicated `AI_IP_ENABLE_LOCAL_SYNTHETIC_V2_API` setting defaults to `0`; setting
it alone cannot activate v2 in the released application. The isolated factory
also requires a trusted same-process runtime object and never starts a TCP
listener.

When explicitly constructed by trusted synthetic test code, the app exposes
exactly these operations:

- `GET /api/v2/sessions/{session_id}/status`
- `GET /api/v2/sessions/{session_id}/revisions/{revision}/evidence-index`

There is no HTTP capability bootstrap, session creation, review write,
package-status, Claims, render or export route. Browser, CORS, proxy, separate
process, CLI IPC and deployment use are unsupported and unauthorized.

## Security and lifecycle controls

- Authorization-first raw ASGI guard before typed route/query handling.
- Literal `127.0.0.1` or `::1` peer/server and exact Host; Origin, forwarded
  headers, duplicate Host/Authorization and preflight are rejected.
- One canonical 43-character unpadded base64url bearer from 32 CSPRNG bytes.
- Plaintext bearer is returned once to trusted calling code and is not retained;
  only a constant-time HMAC-SHA256 verifier remains in memory.
- Separate ephemeral 32-byte verifier and cursor-signing keys; process restart,
  trusted revocation or revision re-registration invalidates old capabilities.
- Absolute monotonic 900-second capability and 3600-second session deadlines;
  re-issuance cannot refresh the session deadline. At most 50 active sessions.
- Trusted cleanup is explicit and outside GET. GET performs no cleanup,
  eviction, mutation, provider/pipeline/render/export, file or database write.
- Evidence pages are stable-sorted with default 25 / maximum 50. Stateless
  HMAC-authenticated cursors contain bounded pagination metadata only and are
  independently useless without a valid bearer.

## Acceptance evidence

`tests/backend/test_local_synthetic_v2_api.py` names and exercises every frozen
criterion AC-01 through AC-29, including authorization-order, privacy,
Host/peer, TTL equality, capacity, cursor tamper/replay, exact response keys,
generic OFF/unknown-route 404 behavior and preserved seven-input P2-005/P2-006
provenance. Relevant v1 and P2-002…P2-006 / AI-CONV-002/003 regressions remain
part of the required test run.

Implementer results before commit:

- Candidate A suite: `37 passed`.
- Relevant v1 / P2-002…P2-006 / AI-CONV-002/003 regression: `522 passed, 1 skipped`.
- Full offline suite with Windows subprocess UTF-8 mode: `1093 passed, 3 skipped`.
- An initial full run without `PYTHONUTF8=1` produced `1092 passed, 3 skipped`
  plus one pre-existing Workflow V2 governance subprocess decode failure: the
  Windows child emitted CP1252 byte `0x96` while its parent explicitly decoded
  UTF-8. The isolated failing case passed with UTF-8 mode, followed by the clean
  full result above; no out-of-scope governance source/test was changed.

Current implementer evidence is not an independent verdict. The final pushed
implementation SHA must receive Gemini 3.8 Flash High / Antigravity STRICT
READ-ONLY review and exact-head CI SUCCESS. This task must stop before merge.

## Handoff

```text
Task ID: AI-CONV-004-IMPL
Agent: Codex
Reviewer: Gemini 3.8 Flash High / Antigravity STRICT READ-ONLY — PENDING
Status: IMPLEMENTATION IN PROGRESS — STOP BEFORE MERGE
Version: 0.1.0
Work completed: Candidate A implementation and AC-01–AC-29 tests prepared
Files affected: isolated v2 ASGI module, default-off setting, tests, this task record
Evidence checked: frozen spec blob cdee9c…; baseline 34c4571…; 37 targeted, 522/1 relevant and 1093/3 full local tests
Findings: Independent review pending
Decisions: Workflow V1; same-process synthetic-only; exact two GETs; no Claims/deploy
Issues: MCP Unknown task — BLOCKED BY TOOL CAPABILITY
Security impact: Additive local proof-of-contract only; released/default v1 remains unchanged
Recommended next action: Push exact SHA, open Draft PR, verify CI, obtain fixed-SHA review; do not merge
```
