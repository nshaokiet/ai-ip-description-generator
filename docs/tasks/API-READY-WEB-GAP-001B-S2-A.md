# API-READY-WEB-GAP-001B-S2-A — minimal local synthetic backend bridge

Version 0.2.0, 2026-11-18, Codex. Security remediation candidate under explicit
Human amendment; fresh exact-HEAD CI and independent Security/Quality re-review
required. Parent issue #131. PR164 remains DRAFT / DO NOT MERGE.

0.1.0 -> 0.2.0, 2026-11-18, Codex: implement Human-approved
S2A-PUBLICATION-COORDINATION-001, publication/revocation serialization, ASGI
post-start abort handling and safe error distinctions. Breaking change: No
product route/schema/fixture/provider change; security coordination and HTTP
error corrections expressly authorized. Earlier verification/handoff below is
preserved history, not review of the remediation candidate.

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

## S2A-PUBLICATION-COORDINATION-001 — authorized remediation

Human explicitly approved LIMITED SECURITY REMEDIATION in the current task
conversation on 2026-11-18, naming task, PR164, reviewed head
`e22e1cd3810912385622d5bf095ff73044fd5d29` and base
`6bb947c1cf67bcfb3ffc935b3a3fafcafb87f0af`. Authority covers F-01/F-02/F-03,
minimal cross-process coordination, deterministic tests, normal continuation
commits/push and fresh exact-HEAD CI/security artifacts. It excludes merge,
Draft-to-Ready, Gemini invocation by Codex, S2-B/R1, deployment, real/arbitrary
papers, paid providers, Claims activation and fixture/gold/policy changes.

### Defect and review provenance

Preserved local baseline diagnostics reproduced four real HTTPS/Chromium cases:
36,343-byte seven-original reviews after completed logout, cancel and protected
operator revoke-all, plus a 46,974-byte artifact after operator revoke-all.
The latter matched its pre-revocation artifact digest. This was a reproducible
contract violation, not a probability-based timing acceptance. h11 backpressure
also allowed private upstream body delivery after both ASGI checks had passed.

The original and backup external review reports remain unchanged privately:
39,656 bytes each, byte-equal SHA256
`11b16f1aba72cc4e7ade2da98d0b056635ab65b430be27810d9f972f8295c43c`.
Requested model was Gemini 3.8 Flash High; actual reviewer-reported UI model
was Gemini 4 Argon High / Antigravity, reused reviewer conversation, application
tests NOT_RUN locally by reviewer. Its reported Security/Quality/overall PASS
and three Low findings remain history; Codex does not adopt the non-blocking
classification for the demonstrated publication gap. A changed HEAD is not
independently reviewed by those historical reports.

### Shared private gate and linearization

The existing owner-private host state now contains `publication/state.json`,
at most two one-shot receipts, and an exclusive `publication/gate` directory.
Atomic mkdir on the local filesystem serializes Python receipt issue/revocation
and Node's final transport handoff. This is private local IPC using standard
libraries, not a database, queue, listener, new service or R1 worker. Startup
verifies the state file and containing directory through the existing ACL/path
checks. The state file is updated under the gate while preserving its provisioned
ACL; partial/corrupt state denies publication. No stale-lock recovery or restart
adoption exists. The existing empty-parent startup requirement still applies.

Backend-issued receipts bind host instance, server-owned principal, session
digest, document, revision, revocation epoch, operation sequence, action/path,
response digest/size/status/MIME and deadline budget. No raw session, CSRF,
custody token, control key or proxy credential is stored in the channel. The
receipt header is consumed only by the private Node proxy and stripped from
browser responses. Browser headers cannot supply publication authority.

For a successful protected response, Node takes the same gate, validates the
complete receipt and payload, consumes the receipt, then synchronously transfers
the response to the connected TLS socket. No await occurs between validation
and handoff. Any HTTP outputData remaining for a later callback causes connection
destruction; transport corks are flushed synchronously before releasing the gate.
**Publication linearizes at acceptance into the connected TLS transport while
the shared gate is held.** This includes the TLS transport's output queue; it
does not claim browser receipt, kernel delivery or cryptographic acknowledgment.

Revocation immediately retires backend authority and then, outside all session,
gateway/workflow/custody locks, acquires the shared gate and invalidates the
owner's outstanding receipts. Completing this transaction is the revocation
acknowledgment. Logout/cancel/operator/shutdown cannot acknowledge success before
that point. Either Node's synchronous commit precedes invalidation or invalidation
precedes and denies that commit; a later callback cannot revive a deleted receipt.
Successful prior commits can reach the browser later and cannot be recalled.

Gate waits use real monotonic time with a one-second bound; flush serialization
also has a one-second bound. Missing peer state, malformed state, stale instance,
replay, identity/digest/deadline mismatch and gate-owner failure deny publication.
Gate timeout persists a failure marker; neither process silently clears/reuses
that channel. Failed invalidation does not return successful revocation, and
gateway quarantine prevents trusted reuse. Uncertain owned files remain for
operator inspection, consistent with existing cleanup/quarantine semantics.

Node's deadline is conservatively measured from before upstream submission,
using the floored remaining session/operation budget at backend operation
admission. This avoids comparing unrelated monotonic clock epochs and avoids
extending authority by buffering/network delay. Expiry also retires backend
receipts via maintenance and the HTTP boundary. The R0 timing model assumes
normal same-host monotonic clocks; no hard real-time, OS scheduling, disk-I/O,
process-crash recovery or CPU/RAM guarantee is introduced.

### ASGI and error semantics

Both existing ASGI checks remain. Denial before start yields 401; denial after
start returns an incomplete upstream response for Uvicorn to close. It never
sends a second start or protected body to conceal that denial. If an already
awaited h11 send resumes after revocation, the data can still enter Node's private
buffer; the shared final gate prevents browser publication. Tests exercise this
actual h11 drain path and the final Node gate together.

Malformed acknowledgment/render input yields safe 400, stale validly-shaped
revision/view and missing review/Claims acknowledgments yield 409, revoked
authority yields 401, and response-limit failures retain 503 response_limit.
Corrupt/unexpected workflow output yields a redacted 503 and retires the affected
resource. Error responses contain no protected document payload or exception
internals; they are distinct from successful data requiring a receipt.

### Targeted verification and handoff

`tests/backend/test_product_web_publication.py` runs the actual Node publication
function in separate processes. It controls both serialization orders and covers
single use, cross-owner/path/revision/action/digest/epoch/operation binding,
deadline expiry, missing/corrupt/closed peer state, gate timeout and persistent
failure, private HTTP output buffering, and real h11 backpressure/response-start.
Existing S1/S2/workflow/provider regression suites remain required.

The real HTTPS test uses only the trusted test host's Node preload and clock
fixture, inaccessible from production flags or browser routes. An end-listener
barrier holds the unchanged proxy callback after FastAPI has completely delivered
the response. Actual logout/cancel/operator/expiry completes, a fresh request
confirms denial, then the barrier releases. Each held response must return 401
with zero protected bytes. The artifact case plus the existing four-file positive
download test preserve binary integrity. Safe per-case event summaries and
provider/egress/cleanup/privacy counters are emitted; no raw host logs are stored.

Final native Windows results, exact new HEAD/TREE/diff, hosted Linux run/jobs,
new downloadable security archive/digest/audits and remaining limitations belong
in the PR handoff. Old CI43387044778 and expired artifact14020490721 cannot prove
the new candidate. Original diagnostics are preserved, not overwritten. All
new independent review remains PENDING; no completion or merge claim is made.

Task ID: API-READY-WEB-GAP-001B-S2-A
Agent: Codex / IMPLEMENTER
Reviewer: ChatGPT-coordinated independent Gemini re-review PENDING; not invoked
Status: Remediation candidate; exact-final-HEAD CI/artifact/re-review gates required
Version: 0.2.0
Work completed: Shared private gate, revocation acknowledgment, ASGI/error fixes, deterministic coverage
Files affected: Exact continuation diff in PR164
Evidence checked: Human amendment, previous raw diagnostics, current baseline and scoped tests
Findings: F-01/F-02/F-03 remediated in candidate; no independent closure claimed
Decisions: Explicit Human S2A-PUBLICATION-COORDINATION-001, 2026-11-18
Issues: Final hosted verification and independent review pending
Security impact: Private local cross-process serialization; existing R0/account trust retained
Recommended next action: Verify new CI/artifact, then return fixed SHA to ChatGPT; keep Draft, do not merge
