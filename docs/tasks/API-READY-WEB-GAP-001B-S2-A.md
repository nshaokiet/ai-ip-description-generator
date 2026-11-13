# API-READY-WEB-GAP-001B-S2-A — minimal local synthetic backend bridge

Version 0.1.0, 2026-11-13, Codex. Implementation candidate; independent Security
and Quality review PENDING. Parent issue #131. DO NOT MERGE.

## Authority and baseline

Human explicitly authorized this task in the 2026-11-13 execution instruction,
including D-GAP-02 exactly two fixtures, limited in-process R0, default-OFF S2-A,
and deferral of generic editing, standalone validation and positive Claims.
Human subsequently supplied full Prompt 14 in the same conversation. This is
the decision reference, not an inferred approval from an audit or review.
Workflow V1; no MCP enrollment/lease/state asserted (coordination tools unavailable).
Verified origin/main and PR163 merge: `6bb947c1cf67bcfb3ffc935b3a3fafcafb87f0af`.
Existing open PRs 140/143/144/146/148/150/152 were checked and left untouched.

The separate [S2-local admission](API-READY-WEB-GAP-001B-S2-A-admission.json)
preserves the original SYNTHETIC_TEST_ONLY manifests and fixture bytes. Startup
checks pinned source/analysis metadata, sizes/digests and declared hash scopes.
PDF analysis hashes the LF Git blob, explicitly normalizing checkout CRLF;
DOCX analysis hashes exact file bytes, without newline normalization. Request
source bytes never undergo normalization. The runtime checks exact parsed text,
locator and evidence identity before rebinding only actual document metadata.
C1 still validates schema, grounding and seven-original provenance independently.

## Launch and route contract

Use all S1 private state/TLS/operator prerequisites, then explicitly add
`--enable-synthetic-bridge` to `python -m backend.app.local_product_web --enable ...`.
Omitting the separate flag exposes authentication only. Neither released FastAPI
nor released Next/Render routes register these endpoints. No workspace UI is added.

All paths below are under `/api/product-web/v1`; authenticated S1 cookie, exact
loopback/Host/Origin/Fetch Metadata/private proxy checks apply. All mutations also
require the session's CSRF. Selectors are server-generated 32-hex values; they
confer no authority. Actor/context and private workflow/custody/revision credentials
never come from request JSON.

| Method/path | Request | Result/limit |
|---|---|---|
| POST `/documents` | Raw admitted bytes, exact MIME and `X-AIIP-Filename` | Intake/process; opaque document selector, revision/state; 201 |
| GET `/documents/{selector}/review` | Empty body | Complete seven C1 originals, current revision, server-owned view ID; 8 MiB maximum, no truncation |
| POST `/documents/{selector}/ack-content` | `revision`, `view_id`, `acknowledge:true` | Explicit content decision |
| POST `/documents/{selector}/ack-claims` | Same, separate affirmative request | Incomplete-Claims decision, after content |
| POST `/documents/{selector}/render` | `revision`, `view_id` | Existing validation/render; four verified artifact metadata records |
| GET `/documents/{selector}/revisions/{revision}/artifacts/{filename}` | Empty body | One of the four exact existing PDF/DOCX filenames, correct MIME/digest/length; at most 8 MiB |
| DELETE `/documents/{selector}` | `{}` | Revoke immediately; dispose after active work finishes |

Every mutation has a strict 2048-byte raw streaming/declared-length limit and
5-second body receipt deadline. Reject duplicate headers, transfer/content encoding,
missing/noncanonical/mismatched lengths and unknown source identities before any
PDF/OOXML validator/parser. The released multipart upload route is not called.
JSON duplicate keys and extra acknowledgment/render fields fail closed. A newly
fetched review invalidates the prior view ID. No edit/revise or validation route.
Claims remain HUMAN_CONFIRMATION_REQUIRED with zero positive claims.

## Ownership, R0 and disposal

Two S1 authenticated owners maximum; one active document each; one reserved
gateway operation globally, no unbounded queue. Excess operations return capacity
failure. Authorization/epoch metadata uses a separate short lock, always ordered
Sessions then gateway. No session invalidation waits for workflow/custody locks.
Logout, absolute expiry, cancel, operator revoke and shutdown fence publication.
Each operation has a 120-second deadline bounded by absolute session TTL; it
checks live session/epoch/ownership before work, after work and at ASGI publication.
The proxy explicitly allows only these routes and buffers bounded JSON/binary
responses, with 125-second upstream timeout for S2 (S1 keeps 5 seconds).

R0 does **not** interrupt running Python computations or provide hard CPU/RAM
limits. Cancel/expiry/timeout blocks publication immediately; one occupied slot
stays occupied until the computation returns. Late results are discarded and
retired through the workflow's trusted host close API using retained custody
credentials solely for disposal. Handlers never mutate private custody state.
Maintenance reaps idle retired documents; shutdown has a bounded wait and
quarantines state on failure. Unknown files are not recursively deleted by the
gateway; only custody's existing verified output cleanup and known empty roots
are removed. Cleanup failure seals the gateway and prevents reuse. Process/OS
crash cleanup is not guaranteed. Already-transmitted bytes cannot be recalled.

The renderer is unchanged. Before exposing any artifact metadata, all four files
must pass existing manifest/source/revision/digest verification and per-file size
limits. Downloads revalidate the complete bundle through custody, then their own
bytes. No renderer-output patching or partial-bundle publication.

## Verification and handoff

Focused native selection: `python -m pytest tests/backend -k "product_web or product_synthetic_workflow or preapi_provider_tripwire" -q`.
Use the project's Python 3.12 environment and a short owned basetemp on Windows.
The browser test uses the actual S1 launcher, TLS, protected OS approval channel,
explicit S2 flag, full review and all four binary downloads. Provider/network
tripwires cover both native workflows and the actual host/browser integration.
Hosted Linux evidence belongs only to the actual final HEAD run; Windows success
must not be reported as Linux verification. Full results, HEAD/TREE, CI/security
artifact identities and remaining blockers are recorded in the Draft PR handoff.

Windows 11 / Python 3.12.10 / Node 24.18.0 actual local verification:
141 focused S1/S2/workflow/provider cases PASS in 650.43 seconds, plus 3
supplementary corruption/quarantine cases PASS (one corruption case overlaps).
The final collection has 35 S2 cases, including operation timeout/capacity,
late result disposal, manifest corruption and cleanup quarantine. All 4 real
HTTPS/IPC browser cases PASS in 58.7 seconds. Lint/typecheck/build, 73+2 Node
security cases, full/prod audits (zero vulnerabilities), dependency pins,
fixture/analysis hashes/scopes, AST import and scoped secret/diff checks PASS.
Browser tripwire evidence: 252 bytes, SHA256
`eb23027a3ed8eb268c5cafeb4da44691c7277f926b67b974c7b3b1718a39fa46`;
provider client attempts/API requests/Python egress/browser egress all zero;
owned state cleanup and private-value log checks PASS. One existing Starlette
BlockingPortal deprecation warning; no test failure. Initial pre-fix failures
and abandoned Python 3.14 attempts are not acceptance evidence. Hosted Linux
and exact final SHA/security artifact verification remain separate from Windows.

Task ID: API-READY-WEB-GAP-001B-S2-A
Agent: Codex / IMPLEMENTER
Reviewer: Independent Gemini Security & Quality via ChatGPT; PENDING, not invoked
Status: Implementation candidate; local PASS, exact-HEAD hosted/independent review gates pending at authoring
Version: 0.1.0
Work completed: Scoped bridge, source pinning, review/export gates and tests
Files affected: Exact final Git diff in Draft PR
Evidence checked: Main/PR163, source fixtures/analyses, existing custody/workflow/proxy
Findings: No unresolved local test failure; final hosted CI/security evidence must be checked before independent review
Decisions: Human 2026-11-13 S2-A authorization; no new exception inferred
Issues: No merge, S2-B, provider, production or general C2 pilot authority
Security impact: Default-OFF localhost-only integration under approved limited R0
Recommended next action: Return fixed-HEAD report to ChatGPT for independent review

API budget USD 0. Provider NOT_RUN. Product Claims runtime DISABLED. Semantic
readiness NOT_DETERMINED. Live spend enforcement NOT_IMPLEMENTED.
