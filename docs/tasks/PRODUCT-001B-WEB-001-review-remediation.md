# PRODUCT-001B-WEB-001 — seven-finding reconciliation

| Field | Value |
|---|---|
| Version / date / author | 1.0.0 / 2026-11-06 Asia/Saigon / Codex, implementer reconciliation only |
| Authority | Human RESUME-PRODUCT-001B-WEB-001 — REVIEW REMEDIATION; documentary/evidence scope only |
| Reviewed candidate | `22d070c64ef7328ca893b06ad40044ac4f5ae722`, tree `a51d7314dcd914fea3d6dba1870b7429550040b5` |
| Remediated specification | [PRODUCT-001B-WEB-0010.1.1](PRODUCT-001B-WEB-001.md), DRAFT/not frozen/not approved |
| QA receipt | [Public-safe remediation evidence](../qa/product-001b-web-001-remediation-20261106.json) |
| Final remediation SHA/tree | Recorded after commit in PR152 handoff and fixed-SHA reviewer prompt; never self-embedded into its own pre-commit tree |

## Original report, attribution and gate separation

Original report: AIIP-PRODUCT-001B-WEB-001-INDEPENDENT-DESIGN-REVIEW.md,
**50927bytes**, SHA-256
`43646a9cec166466e90b3d534a1f842a04fef951c5f91cb59db1a6ac2bb4a0de`.
Size/hash match the Human-provided expectation; backup and original Antigravity
source match byte-for-byte. The complete226-line report was read. Original bytes
remain unchanged locally; raw report, individual session ID and personal paths
are not published.

Reported actual model/profile is **Gemini4 Argon High**, Antigravity STRICT
READ-ONLY, reused reviewer session at Turn15; reviewer attests no implementation
of152/151/149/147/146 and no tracked edits/commit/push/merge/deploy/state changes.
These are source-attributed claims, not authenticated runtime identity. Actual
model differs from AGENTS§6.1/GOV-REVIEWER-001 default **Gemini3.8 Flash High**.
Human's remediation instruction retains Argon as **ADVISORY ONLY**, with no
retroactive model-selection approval. Fresh gate review must confirm the actual
selected-default runtime/profile/session/reuse/independence or stop the gate.

Preserved report verdicts: documentary scope/public-safe inspection PASS;
**technical design REQUEST CHANGES**, **3 HIGH / 3 MEDIUM / 1 LOW**;
governance/merge/runtime BLOCKED. The scoped documentary PASS is not a technical
PASS or model exception. Codex accepts the actionable technical findings under
the explicit remediation instruction; this does not approve the reviewer model.

Manual [CI42048919315](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/42048919315)
on22d070c was COMPLETED/SUCCESS, both jobs SUCCESS. Mandatory artifact13427265002
was downloaded/checked:14385bytes, SHA256
`854638d81f3962b6a08734c807024dbb4aa0462055c315e3fba4edb473e14abe`,
full/production audit0, four expected members. This is historical branch
workflow_dispatch validation, not required main-target PR CI and not evidence
for the changed remediation SHA. No PASS on22d070c is reused as new approval.

## Findings, source lines and dispositions

Line references below refer to the unchanged original report and the old spec at
22d070c, not moving line numbers in0.1.1. A-source references use cf9097fd;
C1/P2/Next sources use the accepted code tree inherited by22d070c.

| Finding / severity | Source line and root cause | Affected contract and remediation | Acceptance / unresolved decisions |
|---|---|---|---|
| F-WEB-01 **HIGH** — ACCEPT | ReportL147–149; old specL137–158/310–318; C1 commit_uploadL167–245/renderL483–527; A.startL153+. Parent-owned RLocks/closures/records cannot be moved wholesale through spawn, and child-rendered files cannot commit C1 state | Spec§4.1–4.2/§8: parent-only ticket, explicit prepare/execute/validate/commit/cancel hooks, pure bounded child JSON/data functions, short ordered locks, recheck generation/epoch/deadline/revision, parent-owned promotion/manifest/RENDERED. Windows Job Object and Linux RLIMIT_AS startup enforcement/readback; precise memory metrics, fail closed unsupported | T01; D03/D06/BF-01/BP4 remain OPEN. Native OS probes and B implementation NOT RUN |
| F-WEB-02 **HIGH** — ACCEPT | ReportL152–154; old specL130/134/158/332–334; C1L194–245, storage.deleteL98–109 and main on_removed=registry.remove. C1 deletes raw bytes/registry after committed envelope retention | Spec§4.3/§5/§6/§9: revision0 raw-file/storage TTL/hash+lease; revision>=1 retained source hash/envelope/doc identity/all7original digests/current revision/private manifest and actual4output hashes. No second raw copy or deleted-file rehash/deadline; revision0 deletion does not call nonexistent A ref | T02; D03/D04/D06. Preserve all owner/stale/tamper/manifest checks |
| F-WEB-03 **HIGH** — ACCEPT gap; correct arithmetic | ReportL157–159; old specL244–265; actual generated originals and P2 identity functions. Missing nested specification/support-Claims document IDs and conflated hash/metadata domains | Spec§5.2: all **7** actual pointer patterns (including both omitted paths), untouched raw originals, canonical public_value hashes, stable public-view domain separate from private snapshot/manifest. Derived draft/Claims/P2 IDs classified as non-authority provenance references, PDF/DOCX metadata scanned; no authority serialization | T03; D02/D04/D05. Report says6 but enumerates7; source execution independently confirms7. No severity change or hidden dropped pointer |
| F-WEB-04 **MEDIUM** — ACCEPT | ReportL162–164; old specL69–86/170–171. GET allocation with2pending slots can self-exhaust/overwrite prelogin; unspecified host control/E2E approval channel | Spec§3.1/§5/§8: POST bootstrap with exact Origin/Host/Fetch Metadata/private proxy/custom header, idempotent existing-cookie binding,8pending vs2auth, TTL/rate/sweep. Protected OS-account IPC/HMAC/nonce/replay checks and same real authenticated approval path in E2E; no HTTP approval backdoor | T04; D01/D02. Host IPC ACL/native behavior remains proposed and requires actual Human approval/tests |
| F-WEB-05 **MEDIUM** — ACCEPT | ReportL167–169; old specL180–183/207/215–233/297/300; C1.review transitionsL443–473. Claims pending incorrectly summarized; validate ordering and positive/error DTO overlap | Spec§5.1/§5.2a/§5.3: explicit CLAIMS_ACK_REQUIRED, server-derived state table and content→Claims-if-needed→validate→render order. Missing reviews409; success200 valid=true plus nonblocking WarningCode; negative422 ErrorDTO with error issues, no positive receipt/export | T05; D04. Standalone validate facade remains proposed, not current A capability |
| F-WEB-06 **MEDIUM** — ACCEPT | ReportL172–174; old specL272–283/342–374; A test-only SourceCheckingRuntime; canonical short_name/grounding and P2 eligibility. Missing non-test2source runtime; typed edits could retain unsupported SOURCE_FACT | Spec§5.2/§7/§8: proposed app-services product_synthetic_runtime.py implements the existing protocol for admitted source-specific inputs, no tests/ imports. SOURCE_FACT titles read-only; host-pinned admitted PARAPHRASE/INFERENCE edit variants/evidence, no upgrade. Keep P2 inference eligibility/exclusion; W02 uses a proven eligible paraphrase edit | T06; D04/D05/D06. New restriction/variant records still require Human admission; DOCX-B bytes/hash absent |
| F-WEB-07 **LOW** — ACCEPT | ReportL177–179; old specL59–67/126/B1/B6; frontend next.config.ts and playwright.config.tsL14/33. Buffered upload/TLS bootstrapping/test discovery not pinned | Spec§3.1/§8: pass request.body with counting/backpressure/duplex:half, abort/length checks and no request.formData buffer; node:https wrapper with offline pre-provisioned/ephemeral certificate, no mkcert/download. Actual frontend/e2e/product-web.spec.ts and separate real HTTPS project; preserve v1 HTTP project/suites | T07; D01/D03/D06. No transport/E2E code or real memory/TLS acceptance executed here |

All seven are **DOCUMENTARY REMEDIATION PROPOSED — RE-REVIEW REQUIRED**.
Implementer acceptance/edits do not close an independent finding, erase its old
REQUEST CHANGES or establish feasibility. No additional severity was invented.

Source precision corrections: C1 intake already uses short global reservation
locks; A.start spans heavy work under its own RLock, and C1.render uses the
per-record lock. The split-phase plan targets those actual boundaries, rather
than incorrectly claiming C1 holds one global lock throughout intake. Linux
address-space and Windows committed-memory limits are not identical RSS caps.
Title max500characters is canonical; rationale has no canonical500-character
limit, but B's4096UTF8byte command bound/admitted-variant policy still applies.

## Detailed acceptance proposals — NOT IMPLEMENTED / NOT RUN

- **T01:** reject attempts to send A/C1/locks/callbacks/tickets across child IPC;
  validate only bounded inert result bytes. Supported Linux/Windows preflight,
  under-limit real parse/render and over-limit allocation/readback/peak metrics;
  native assignment failure denies startup. Abort/logout/revision/timeout/parent
  death before commit: kill/reap, discard late result, no state/manifest promotion;
  lock remains available during heavy work. Unsupported host cannot enable B.
- **T02:** revision0 hash/size/admission checks before/after lease and source TTL;
  successful process removes file AND registry, cleanup failure revokes custody;
  later review/validate/render/download succeeds without raw bytes only when
  retained provenance is valid. Corrupt envelope source hash/one original digest,
  owner/revision/manifest or any output file: deny and revoke as applicable.
- **T03:** enumerate every occurrence, including wildcard arrays at all7patterns;
  alias public copies consistently, preserve originals/digests exactly; recompute
  public canonical hashes, prove they differ where aliases differ, bind stable
  content view separately from volatile decision flags. Scan all DTO/errors/logs
  and parsed PDF/DOCX metadata/text for raw authority; allow only classified
  one-way business provenance IDs, never token hashes/private paths/capabilities.
- **T04:** GET/prefetch bootstrap405/no slot, repeated cookie reuses exact pairing/
  CSRF/deadline, two contexts/ordinary reload do not consume2slot-only capacity;
  race/new-cookie cases bounded by8slots, TTL/rate/reaping, 2auth cap independent.
  Invalid IPC peer/ACL/HMAC/nonce/replay/expired binding cannot approve; real E2E
  host uses the same authenticated control protocol, not an always-true callback.
- **T05:** missing content409 REVIEW_REQUIRED; content-only incomplete Claims state
  is CLAIMS_ACK_REQUIRED and validate409; separate affirmative ack enables REVIEWED;
  validate200 valid=true warnings-only, package failure422 errors-only and clears
  old receipt. Invalid/no-op/duplicate/stale transitions never fabricate approval.
- **T06:** per-source runtime rejects mismatched hash/units/locators/excerpts and
  never imports tests/provider. SOURCE_FACT edit denied; admitted paraphrase edit
  preserves exact evidence and yields new eligible title through existing P2;
  inference never promoted or forced into filing prose. Title501characters fails;
  rationale501 is evaluated against actual schema/4096bytes/admission, not an
  invented500limit. Canonical uniqueItems/prohibited filing-ready/pointer attacks
  still fail; invalid edits leave original revision/decisions unchanged.
- **T07:** near-limit/chunked/oversize/disconnected multipart traverses Next with
  bounded buffers/backpressure, correct boundary, duplex and abort/cleanup; deny
  demo-sample/internal-header bypass. Local HTTPS starts from approved offline
  certificate without network/tool download. New test is discovered under
  frontend/e2e/, actual product project runs HTTPS+real host IPC; existing v1 and
  mandatory suites stay enabled.

Executed pure-function pointer enumeration and any existing C1/P2 regression
results are recorded separately in the QA receipt. They do not prove the planned
B hooks, native OS limits, IPC, TLS, streaming or browser flows work.

## Blockers and handoff

The specification retains full **BF-01..BF-05** and **BP4-01..BP4-05** matrices.
BF-01 needs selected-default re-review; BF-02 model gate cannot use unapproved
Argon as the freeze gate; BF-03 Human security/design decisions absent; BF-04
foundation151bc991c7 review/acceptance pending; BF-05 real fixture/variant byte
admission incomplete. BP4 additionally requires actual A/C2 dependency disposition,
accepted foundation/main-target PR CI and separate Phase4 implementation authority.

Old0.1.0 is immutable at22d070c; no raw original report or source-review history is
deleted. New0.1.1 remains DRAFT, not FROZEN/APPROVED; no B runtime/auth/fixture/CI
policy code is introduced. Final HEAD/tree, normal-FF push and actual new manual
CI are recorded after commit in the PR handoff; manualCI is never required
main-target PR CI. New reviewer prompt selects Gemini3.8 Flash High and must
report actual runtime/profile/session/reuse/independence, exact target and verdict.

Task ID: PRODUCT-001B-WEB-001 — REVIEW REMEDIATION
Agent: Codex — documentary implementer/reconciler
Reviewer: Prior reported Gemini4 Argon High advisory; new Gemini3.8 Flash High STRICT READ-ONLY review PENDING
Status: Seven documentary fixes proposed; independent closure/freeze/implementation PENDING/BLOCKED
Version: Reconciliation1.0.0; spec0.1.1
Work completed: Read/verified complete original report, reconciled all7findings and source corrections, updated contract/test/blocker matrices
Files affected: Spec, this reconciliation, safe QA receipt, README/Control Center/Review Log only
Evidence checked: Exact old HEAD/tree, report size/hash/source identity, actual C1/A/P2/Next source, existing pure generation pointer inventory
Findings: Original REQUEST CHANGES preserved; all7pending re-review; Argon model mismatch not approved retroactively
Decisions: New default3.8 review required; D01–D07/fixture/dependency/security/runtime gates retained
Issues: BF/BP4, native feasibility and future B tests NOT RUN; MCP registration/lease UNVERIFIED
Security impact: Public-safe documentation only; originals/session/private paths retained locally
Recommended next action: Independent fixed-SHA3.8review and actual Human design/fixture/scope decisions; no merge/deploy/runtime
