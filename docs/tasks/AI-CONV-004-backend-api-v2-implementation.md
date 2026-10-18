# AI-CONV-004-IMPL — Candidate A Backend API v2 implementation

| Field | Value |
|---|---|
| Task | AI-CONV-004-IMPL / Issue #123 |
| Version | 0.1.1 — factual governance status reconciliation (no runtime change) |
| Status | IMPLEMENTATION MERGED / EXACT-MAIN CI VERIFIED — governance docs sync and Issue disposition pending |
| Workflow | V1 |
| Authorization | `HUMAN-AI-CONV-004-CANDIDATE-A-IMPLEMENTATION-2026-10-17` |
| Frozen contract | AI-CONV-004 specification v0.1.3, blob `cdee9c041932ec911cd84dd1c16ab7dbb5bb7f94` |
| Original implementation baseline | `main` at branch creation `34c457100127f3f3954aa0fdc0a13791e40e998a` |
| Verified implementation merge/main | `92a9dc182e8aef98f51a9dc71da8f309a7f680a1` — PR #124 |
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

The above tests are **implementer-reported** outcomes, not substituted for independent verification. The original premerge stop was correctly observed. Subsequent exact-SHA Gemini and GitHub CI evidence, protected governance merge and postmerge main CI are recorded below. No production release or Claims-runtime authority follows from merge.

## Postmerge closeout evidence — 2026-10-18 (factual status reconciliation)

- [PR #124](https://github.com/nshaokiet/ai-ip-description-generator/pull/124) **MERGED** by normal merge commit with expected-head protection: reviewed head `2305ae4a1cb367370328d660b8313f8d0c621587`, prior main `34c457100127f3f3954aa0fdc0a13791e40e998a`, merge/final main [`92a9dc182e8aef98f51a9dc71da8f309a7f680a1`](https://github.com/nshaokiet/ai-ip-description-generator/commit/92a9dc182e8aef98f51a9dc71da8f309a7f680a1).
- Reviewed candidate tree and merge tree are identical `955b102fc2af5f3f0f99fcc00c31560000854e8d`; exactly the six authorized implementation/test/docs files `+1455/-2`, with no frozen spec, released `backend/app/main.py`, runtime Claims, provider, seven-input provenance or dependency edits.
- [Gemini 3.8 Flash High / Antigravity STRICT READ-ONLY fixed-head independent PASS receipt](https://github.com/nshaokiet/ai-ip-description-generator/pull/124#issuecomment-6245541963): **five INFO / zero reported blocking findings**, session `25b1e601-98eb-40ec-8dbf-7fff70f5e616`, **REUSED YES** (continuation of prior specification reviewer session, not the Codex implementation session). Reviewer-reported re-execution **37 passed/1 warning** AC suite, **149 passed/1 warning** selected regressions; do not describe these as ChatGPT independent re-execution or GitHub-native approval.
- [Exact-head PR CI #39008524882](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/39008524882) **COMPLETED/SUCCESS**; [exact-merge/main push CI #39097292502](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/39097292502) **COMPLETED/SUCCESS**, **34/34 job steps**.
- Both Render services verified Auto-Deploy **OFF**, previews **OFF**, latest live commit `8c36b2bc662ed41b2a9b3635d5d4d29110b1d9bb` remains unchanged; this candidate was **not deployed**.
- [PR merge closeout receipt](https://github.com/nshaokiet/ai-ip-description-generator/pull/124#issuecomment-6245735212) and [Issue #123 postmerge verification](https://github.com/nshaokiet/ai-ip-description-generator/issues/123#issuecomment-6245759992) preserve audit history. **Issue #123 remains OPEN** pending a separate docs-only status reconciliation review/merge and governance disposition.
- Project Orchestrator MCP returned `Unknown task: AI-CONV-004-IMPL`: mark **BLOCKED BY TOOL CAPABILITY**; no invented lease, transition or completion. Native GitHub `main` lacked required branch-protection contexts at merge; exact expected-head protection was used, no platform bypass. Hardening `main` protection is a separate policy/permissions decision, **not** part of this documentation sync.
- **Remaining STOP boundaries:** isolated synthetic-only same-process GETs, no public listener, browser/IPC, real/confidential research, paid/live AI provider, published/positive Claims, production deployment, Render changes, Workflow V2/Phase H or further downstream implementation authorization.

## Historical premerge handoff

The following identifies the **former implementation-stage handoff**, superseded by the verified merge/CI facts above. It is preserved solely for audit; it does not represent current PR/CI status.

## Handoff

```text
Task ID: AI-CONV-004-IMPL
Agent: Codex
Reviewer: Gemini 3.8 Flash High / Antigravity STRICT READ-ONLY — PENDING (historical premerge record)
Status: IMPLEMENTATION IN PROGRESS — STOP BEFORE MERGE (historical premerge record)
Version: 0.1.0
Work completed: Candidate A implementation and AC-01–AC-29 tests prepared
Files affected: isolated v2 ASGI module, default-off setting, tests, this task record
Evidence checked: frozen spec blob cdee9c…; baseline 34c4571…; 37 targeted, 522/1 relevant and 1093/3 full local tests
Findings: Independent review pending
Decisions: Workflow V1; same-process synthetic-only; exact two GETs; no Claims/deploy
Issues: MCP Unknown task — BLOCKED BY TOOL CAPABILITY
Security impact: Additive local proof-of-contract only; released/default v1 remains unchanged
Recommended next action (historical): Push exact SHA, open Draft PR, verify CI, obtain fixed-SHA review; do not merge
Current next action (2026-10-18): independent fixed-SHA review and exact-head CI for this docs-only status-sync PR, separate merge decision/eligibility, then review Issue #123 closure against observed postmerge evidence
```
