# P0-SOURCE-LIFECYCLE-001 — bounded execution

Version1.0.1, actual2026-11-23, Codex; Owner Nguyễn Song Hào Kiệt — Independent Developer.
Status: IMPLEMENTED_CANDIDATE / REVIEW_PENDING / INTEGRATION_PENDING, not Completed.
Authority: actual Human P0-SOURCE-LIFECYCLE-001 execution instruction permits reproducible non-policy fixes and isolated contract tests. The earlier PR173 spec75d6778576d56b6d19b61bf018179869623a9dfb remains proposed, not adopted. Latest instruction permits the bounded lease correction, not blanket SL-D approval.
Base6bb947c1cf67bcfb3ffc935b3a3fafcafb87f0af; branch fix/p0-source-lifecycle-lease-20261122.

## Root cause and correction

Storage's set loses active-document protection when an inner or overlapping lease exits before another live lease. Deterministic original-code execution:5FAIL/3PASS; initial8setup errors from inaccessible system temp are preserved separately and are not defect evidence. Reproducer covers nested delete/sweep, expiry, exceptions, overlapping threads and external mutation/unlink.

Replace only active-ID membership with lock-protected reference counts. Delete and sweep still refuse while any lease lives, and behave as before after the final exit. No TTL/mtime refresh, new persistent storage, file/content lock, source-copy retention or policy/HTTP/API change. A lease still cannot stop external filesystem writes/unlinks; real C1 boundary regressions require source revalidation/fail-closed cleanup. Tests use Events/futures and explicit timestamps, not wall-clock sleeps.

Executed new regressions:14PASS/0FAIL/0SKIP,16.39s (one existing Starlette deprecation warning). Broader upload/parser/C1/product regression and final hosted results are recorded in the PR receipt; not inferred here.

## Source sequence and executable probe

Opt-in `tests/contracts/probe_source_lifecycle.py` runs ONLY in a disposable checkout containing four exact candidate service blobs, each checked against its Git object before import. It is not normal pytest discovery or an accepted backend import. Pin169=3f34217638c0ed1fcf7e91b74fa47b163fa1cd96,170=5a8abca89889433f99199b1ca0c6a687f64433b6,171=87b39dc8e0bd6241cfea5dc2e7912255bba178f1,172=e6ed73a702e8a9fbf9126ca1a651f2e3e57d57fb. Copy only their new service files and this candidate's storage into that disposable main checkout; set PYTHONPATH to it and P0_SOURCE_PROBE_OUTPUT to a fresh owned directory; invoke this script with the existing project Python environment. Requires local pinned Git objects, no fetch/provider/network.

Executed on admitted controller.pdf and research-b.docx: actual HTTP upload/register → source preparation/hash → confidentiality payload-change/revoke checks → manual save/CONTINUE/STOP/CONTINUE and edit/stale-revision denials → asset inspection → discard asset object → C1 start/commit → raw file absent and registry absent → PRIOR/ASSETS both SOURCE_UNAVAILABLE_OR_CHANGED → retained C1 review/canonical package → six business exports plus hash manifest. All source hashes agree; tripwire counters0. Test callbacks/principals are explicit test doubles, not Human approval or real session authentication. STOP is assessed before calling C1; this does NOT establish a mandatory integrated runtime gate. No source lease spans Human interaction.

Existing C1 derives draft/Claims during commit, before deleting source. Retained seven originals allow existing authorized custody review/export, not raw-file reopening. Standalone business exports from supplied originals in the probe are not authenticated website downloads. No handoff metadata authority is introduced here.

## Proposed interface matrix — not implemented runtime

| Component | Input → output | Ownership/trust | Digest/revision | Invalidation |
|---|---|---|---|---|
| Upload/registry | admitted bytes → opaque ID/record | existing host/storage | actual SHA,size,media | deletion/TTL/mutation |
| Assets | registered ID → metadata summary | host callback, no browser identity | source SHA/asset SHA/locator | source change; no image bytes retained after delete |
| Prior | manual dossier → assessment | actual authorized specialist via future trusted host | source SHA,dossier revision/digest,latest decision | STOP/edit/revoke/source loss |
| Precommit boundary | current assessments → C1 invocation | future server-derived principal; no bearer snapshot | source vs dossier domains kept separate | missing/stale decision/session/logout/expiry |
| C1 | source/config → custody receipt,raw deletion | existing canonical validator/host | custody ID/revision/token plus seven digests | revise/revoke/custody TTL |
| Review/export | custody projection → existing artifacts | existing current host authorization | current originals/manifest/output hashes | stale token/revise/revoke/expiry |

Future sequence: independent short source operations → actual STOP/CONTINUE → fresh source/principal/revision recheck → canonical C1 commit/delete → current bound custody projection → authorized review/export. Never treat snapshot/hash as a bearer capability, equate dossier revision with custody revision, or keep raw source/images for later redraw. Future implementation must define atomic invalidation and failure cleanup without wrapping Human pauses in leases or calling cross-service callbacks under C1 record locks.

## Decisions and acceptance disposition

SL-D01–D08 remain PROPOSED. Current instruction authorizes only narrow confirmed D06-related bug remediation under existing live-lease deletion semantics; it does not approve general concurrency redesign. D03 raw-image retention is NOT authorized. D04 revision/revocation and D05 principal/session trust need explicit disposition before handoff runtime; D01/D02/D07/D08 integration also depends on accepted services/current policy. No approval inferred from this record.

SL-01/04/08/09/15/18: bounded native probe/regression evidence only, not complete website acceptance. SL-03/05/10/11/12/14/16/19: existing service negative regressions and test-double observations do not prove a new integrated gate; runtime contract pending. SL-02 full PNG/JPEG/table admitted C1 flow and SL-17 browser E2E remain BLOCKED; no new fixture admission invented. SL-06/07/13 receive actual deterministic source mutation/unlink/TTL/lease regressions. SL-20 regression counts and hosted evidence are recorded in the exact-HEAD PR receipt; do not infer PASS before execution.

## Gates and handoff

Required genuine Gemini4 Argon(High) Security AND Quality on the same final HEAD/TREE; two separate strict-read-only sessions/transcripts. Current desktop runtime previously failed before inventory; reviewer execution NOT_RUN/BLOCKED_REVIEW until actual dispatch succeeds. Self-checks are not independent PASS. CI must remain unchanged; inherited Next audit may still fail.165 initiation AUTHORIZATION_PROVENANCE_NOT_VERIFIED remains open;168 NOT_EFFECTIVE. MCP task/lease NOT_VERIFIED. No merge/Ready/deploy, real paper, paid API, Claims activation or runtime integration.

Task ID:P0-SOURCE-LIFECYCLE-001
Agent:Codex
Reviewer:required independent Security/Quality NOT_RUN
Status:IMPLEMENTED_CANDIDATE /REVIEW_PENDING /INTEGRATION_PENDING
Version:1.0.0
Work completed:narrow lease correction,deterministic regressions,opt-in pinned contract probe,interface/decision matrix
Files affected:storage,two regression files,opt-in probe,this record,README,Control Center
Evidence checked:real Git/spec/custody paths,red-phase XML,two-source probe;final tests/CI/SHA in PR receipt
Findings:nested lease premature release;external source writes remain possible and must fail C1 checks
Decisions:no SL-D blanket approval or policy amendment
Issues:unaccepted dependencies and trusted revision/principal handoff block website integration
Security impact:restore protection during all live leases;no retention/TTL/auth policy change
Recommended next action:genuine fixed-SHA dual review;accepted dependencies and explicit decision disposition before runtime handoff


1.0.0→1.0.1,actual23/11/2026,Codex: reconcile174 against accepted175/main986c49782326487fd2b619f6f3603e618d9f806d. Original baseline/review/test entries remain history. No lease/backend/test implementation changes. Fresh final-HEAD CI and review required; previous Gemini3.8 one-cycle approval is not assumed renewed. Proposed new model selection requires actual-date disposition before dispatch. Strict age admission and SL-D04/D05 remain pending.
