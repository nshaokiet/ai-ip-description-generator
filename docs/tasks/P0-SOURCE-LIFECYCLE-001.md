# P0-SOURCE-LIFECYCLE-001 — Source custody and revision handoff

| Field | Value |
|---|---|
| ID / version | P0-SOURCE-LIFECYCLE-001 / 0.1.0 |
| Prepared | 2026-11-22, Asia/Ho_Chi_Minh |
| Status | **DRAFT SPECIFICATION / HUMAN SECURITY-DATA DECISION REQUIRED / IMPLEMENTATION NOT AUTHORIZED BY THIS DOCUMENT** |
| Author / recorder | ChatGPT, project coordination |
| Scope | Minimal offline/synthetic integration design across accepted C1 and unmerged P0-PRIOR, P0-ASSETS, P0-CONF, P0-OUTPUT candidates |
| Baseline | Accepted `main` `6bb947c1cf67bcfb3ffc935b3a3fafcafb87f0af`; tree `aaece7b6128648deae0ebb2b60749f786cb0ca8f` |
| Workflow / budget | Existing Workflow V1, USD 0, provider NOT_RUN, product Claims runtime DISABLED |
| Authorization | Owner instruction to continue project integration planning on 2026-11-22; **this is not authorization to mutate runtime, retention, auth, Claims, provider or merge** |
| Dependencies | [PR #165](https://github.com/nshaokiet/ai-ip-description-generator/pull/165), [#164](https://github.com/nshaokiet/ai-ip-description-generator/pull/164), [#169](https://github.com/nshaokiet/ai-ip-description-generator/pull/169), [#170](https://github.com/nshaokiet/ai-ip-description-generator/pull/170), [#171](https://github.com/nshaokiet/ai-ip-description-generator/pull/171), [#172](https://github.com/nshaokiet/ai-ip-description-generator/pull/172) — all **unmerged candidates** |

## 1. Problem and verified root cause

**Finding:** `SOURCE_LIFECYCLE_HANDOFF_NOT_VERIFIED` — **OPEN, blocks unified website workflow acceptance**.

The current accepted `backend/app/services/preapi_source_custody.py` does all of the following in `TrustedCustodyCoordinator.commit_upload()`:

1. Obtains a real `DocumentStorage.lease(document_id)`, checks registry record, file identity/size/SHA-256, produces source envelope, runs the injected synthetic extraction runtime, validates and derives seven canonical originals; it creates an internal custody record with provenance digests.
2. **After the source lease exits**, calls `storage.delete(document_id)`. A failed delete revokes custody; successful delete is by design. The storage constructor at `backend/app/main.py` sets `on_removed=registry.remove`. `DocumentStorage._unlink_path` invokes that callback on successful deletion.
3. Retains a validated source envelope, derived originals and digests within bounded volatile custody. It does **not** promise continued access to the raw PDF/DOCX.

The unmerged candidate `manual_prior_art.py` (#170) checks the actual registered source and file under its own lease on `save`, `snapshot` and `decide`. The unmerged `document_assets.py` (#172) similarly requires the original registered file and lease for `inspect`. **Both correctly reject access once C1 deletes the source and registry metadata.** This is not a reason to weaken their validation or silently keep copies.

`backend/app/services/product_synthetic_workflow.py` already coordinates local admitted synthetic intake and calls C1 `commit_upload` during `start`; it does not currently orchestrate pre-commit manual Prior Art or asset inspection. The default website / S2-A bridge is not the accepted integrated business flow. `business_document_outputs.py` (#171) takes a validated canonical package/originals, not a raw upload, but source/manifest/revision handoff is still unverified.

**Additional concurrency design risk to test:** `DocumentStorage.lease` tracks `_active_ids` as a `set`. If two nested leases of the same document overlap, exiting the inner lease discards the ID while the outer lease may still be active. C1 calls `preparation.prepare_extraction_input` inside an outer lease; ASSETS uses separated leases. This requires a focused race test and appropriate bounded fix if reproduced. No assertion is made that the race has occurred in production.

## 2. Proposed integration contract — pre-delete decision, post-delete provenance

**Do not construct a second persistent storage system.** The preferred next design is a **trusted host-owned pre-commit sequence** on a single admitted synthetic document and owner:

`UPLOAD / VALIDATE / REGISTER`
  → `RECHECK SOURCE IDENTITY + OWNER`
  → `P0-ASSETS: INSPECT while original exists`
  → `P0-PRIOR: MANUAL EVIDENCE + actual Human STOP/CONTINUE decision before drafting`
  → `VERIFY CURRENT SOURCE HASH, PRINCIPAL, DECISION, SNAPSHOT AND TTL`
  → `C1.commit_upload: SYNTHETIC PROCESS → CREATE CUSTODY → DELETE RAW FILE / REGISTRY`
  → `BOUND POST-DELETE REVIEW PROJECTION / VALIDATE / RENDER / DOWNLOAD`

This order is a **proposal** pending security, authority, and lifecycle decisions. In particular, it does not authorize source retention, adapter changes, external network access or use of real research.

- **Before C1 commit:** execute P0-ASSETS and P0-PRIOR only with actual storage/registry guards and trusted host callbacks. No browser-provided `owner`/`actor`/`context` or untrusted display label constitutes authorization.
- **On manual Prior Art STOP:** deny all later drafting; record an auditable bounded stop decision without pretending novelty is established. If incomplete, require an explicit authorized CONTINUE decision with `Prior Art Search Incomplete` and preserved warnings; never silently skip the step.
- **Handoff object:** a bounded, **non-bearer**, host-private, immutable snapshot may carry only authenticated principal/owner binding, document ID, source SHA-256, source-envelope digest (when available), Prior Art dossier revision/digest/decision, asset metadata/locator/hash summaries, audit event IDs, created/expiry/revocation epoch and policy flags. No raw paper bytes, private host/session keys or unrestricted source content in logs/UI/receipt. All consumer trust must derive from current server-owned authority, not values in this object alone.
- **Raw figure bytes:** `SourceAsset` currently contains original image `data`. Do not retain or serialize those bytes past approved source lifecycle by default. A later redraw operation requiring these bytes must run **while source is authorized and alive**, or await a separately approved bounded retention and deletion policy. A digest/locator alone does not permit reconstruction after deletion.
- **C1 processing boundary:** `commit_upload` must still verify the source under its own lease and fail closed on changed/expired/missing bytes. A pre-commit snapshot is **not** permission to skip C1 validation. The source may disappear between preliminary operations and C1 commit; in that case abort and clean up rather than extend TTL or synthesize evidence.
- **After delete:** use C1's retained seven-original provenance and manifest only, plus separately validated minimal metadata needed for user review. Neither PRIOR nor ASSETS may attempt to re-open deleted file or assume their pre-delete snapshots authorize an arbitrary later revision.
- **Revision invalidation:** bind Prior Art and asset decisions to the *exact current source/custody revision and digest domains*. A C1 `revise` or invalidation must invalidate dependent review/decision claims; re-check/reauthorize the resulting review or require a source-independent explicitly approved rule. Never map `dossier_revision` (#170) to `custody.revision` merely because both are integers.
- **Claims and outputs:** maintain `claims_runtime_implemented=false` / product Claims OFF and all seven canonical originals' existing contracts. #171's Patent Draft / Annotated Draft / Analysis Report remain drafts with unchanged source technical prose and figure/Claims limitations. Do not weaken QA, integrity, manifest or export authorization.

## 3. Key architecture questions requiring Human/security disposition

| ID | Decision required | Recommended default / reason |
|---|---|---|
| SL-D01 | May PRIOR/ASSETS be executed in same trusted local source window **before** C1 consumes raw upload? | **Yes only for synthetic/admitted content**, under authorized host, with independently accepted candidates |
| SL-D02 | What may survive raw-source deletion? | **Only minimum validated source-bound metadata already allowed by custody**; no second PDF/DOCX copy and no unapproved original image bytes |
| SL-D03 | Is any temporary image-byte retention for later redraw authorized? | **No** by default; separate security/data/retention approval necessary before persistent, durable or long-lived bytes |
| SL-D04 | What revokes/invalidate bound Prior Art, asset, review and output metadata on `revise`/logout/TTL/source mutation? | Fail closed; define source revision ≠ dossier revision; decision must be explicit before runtime integration |
| SL-D05 | What is the allowed host principal/session/actor binding across #164 S2-A, C1 and services? | Server-derived authenticated owner and current session; never trust browser-supplied identity |
| SL-D06 | May existing `DocumentStorage.lease` implementation change if nested-lease race is confirmed? | Permit only through separate scoped change with negative concurrency tests; do not silently weaken TTL/deletion |
| SL-D07 | How is `P0-CONF` enforced at actual provider/search egress? | Default-deny and source/revision/payload/destination-scope recheck at every actual egress boundary; standalone #169 is not yet such enforcement |
| SL-D08 | What must remain usable when original source is deleted by design? | Custody-approved review/export on immutable validated originals only; no raw file-dependent consumer after delete |

Until these decisions are approved, **P0-SOURCE-LIFECYCLE-001 is specification-only**. Existing PROD/real-data/security/Claims restrictions remain.

## 4. Smallest proposed implementation slice (not yet authorized)

After accepted dependencies and SL-D decisions, implement **one** carefully scoped host-side adapter/orchestrator extension around existing components, rather than modifying all services or rewriting C1:

1. Add an explicit `PRE_COMMIT` state and fail-closed manual Prior Art/asset preflight for the same source hash and authorized owner, with a bounded source-bound metadata snapshot and STOP/CONTINUE.
2. Keep APP-001/APP-002 and C1's canonical seven originals, raw-upload cleanup semantics and source-validation checks. Avoid calling other services under C1's per-record lock; define deterministic lock ordering. Do not hold a file lease throughout a Human pause or extend upload TTL.
3. Use `commit_upload` only after preflight and fresh same-source recheck; map to custody ID/revision only from a successful C1 receipt. On error, seal/abort bound preflight; no partial export, no leaking raw bytes, no replay.
4. Preserve explicit invalidation across every revise/revoke/abort/timeout/cleanup. Expose only safe review warnings and hashes to browser; confidentiality consent remains separately enforced before **any** external provider/prior-art query.
5. Avoid new network services, schema replacement, production DB, claims activation, data-retention expansion, or non-essential new frontend UI. Build a thin API/website bridge only after #164 and dependent security decisions are accepted.

Implementation file candidates **subject to verified final integration diff**: `backend/app/services/product_synthetic_workflow.py` (or a minimal host-side integration service if needed); optionally `backend/app/services/document_storage.py` only if lease race proven; tests in `tests/backend` and later `frontend/e2e`. #169–#172 branches are unmerged and must not be imported as accepted-main dependencies. Any modifications to security/data/authority contracts require an explicit authorized task and review.

## 5. Acceptance test matrix — proposed, not executed

| AC | Setup / action | Pass criterion |
|---|---|---|
| SL-01 | Admitted synthetic PDF before C1 | Hash/size/owner confirmed; manual Prior Art explicit CONTINUE; source provenance bound |
| SL-02 | Admitted synthetic DOCX with PNG/JPEG/table | Asset locators and hashes recorded before deletion; no raw image bytes persist without authority |
| SL-03 | Prior Art STOP | Draft generation rejected; no export; actual decision/audit retained within approved lifecycle |
| SL-04 | Incomplete Prior Art with explicit CONTINUE | Warning survives review/export without claiming novelty/patentability |
| SL-05 | Missing or unapproved Prior Art decision | Fail closed; no silent drafting or stale approval |
| SL-06 | File modified/replaced between preflight and C1 | C1 rejects source hash/size mismatch, no stale custody/manifest |
| SL-07 | Source removed/TTL expired before commit | Fail closed; no TTL extension, no synthetic source revival |
| SL-08 | Normal successful C1 commit | Raw file deleted and registry removed; seven validated originals/manifest retained as designed |
| SL-09 | Attempt PRIOR or ASSETS after C1 cleanup | Existing source-unavailable error preserved; post-delete review uses only authorized retained projection |
| SL-10 | Revision changed after approval | Invalidate source/revision-bound decisions and stale manifest; require appropriate new authorization |
| SL-11 | Other user/session/custody ID or forged receipt | Deny; host authorization revalidated; no cross-owner source/outputs |
| SL-12 | Revocation/logout/host restart | Revoke capabilities/decisions; no authenticated revival from old snapshots |
| SL-13 | Concurrency: nested leases, TTL sweeper, delete | No deletion while **any** live lease exists; no premature release; deterministic race test |
| SL-14 | Expired/error/exception during callbacks | No partial published snapshot, stale revision, leaked bytes or false success |
| SL-15 | Export Patent/Annotated/Analysis using approved synthetic originals | File hashes/MIME/provenance/required warnings correct; DOCX/PDF QA; draft-only marker |
| SL-16 | Provider/prior-art search egress attempt without current P0-CONF decision | Default-deny before any network/SDK invocation; no key/token in logs |
| SL-17 | Two distinct admitted technical sources PDF + DOCX | Full same-source-bound browser workflow E2E once #164/P0-WEB is integrated |
| SL-18 | Claims support absent or figure not verified | Claims product stays OFF; missing/refusal and figure REVIEW_REQUIRED; no fabricated patentability |
| SL-19 | Time-of-check/time-of-use and stale/principal confusion | Mutation/delete/revise/revoke between steps cannot permit later stale consumer action |
| SL-20 | Regression/security | Existing C1, APP, P2, claims-negative, MIME/digest/TTL, 135 glob security, backend/MCP, browser and CI gates unchanged |

Do not label tests PASS until executed on the exact committed implementation HEAD. The proposal does **not** imply that every UI route exists today.

## 6. Dependency and review gates

1. **Dependency PR #165:** exact current candidate `4186b7afd4845497decc041f3016968fada2c754`, CI `44905331090` SUCCESS; new SHA requires genuine Security and Quality review, MEDIUM finding independent closure and actual-date historical authorization disposition, followed by explicit Human merge authorization. Previous old-SHA PASS does not transfer.
2. **PR #166/#167/#168:** reviewer-model and product roadmap documents are not all merged. PR #168 is stacked and **NOT_EFFECTIVE** pending separate Owner authorization. Read-only inventory is not runtime authority.
3. **PR #164:** default-OFF local S2-A bridge unmerged. Integration cannot pretend the documented browser endpoints are active on main.
4. **PR #169–#172:** candidate services have local tests but are unmerged, some CI fail inherited Next audit. Review exact HEADs separately, then reconcile dependencies and overlapping README/Control Center edits with accepted-main history.
5. **This design document:** security/quality design review, Human decisions SL-D01–08, scoped implementation authorization and host platform/CI checks **PENDING**. No auto-merge on document publication.
6. **After implementation:** tests including concurrency and raw-source removal, exact-head hosted CI/security/audits, independent same-HEAD Gemini 4 Argon (High) Security **and** Quality reviews with genuinely distinct actual contexts, and applicable Human decision before merge. Post-merge exact-main verification if/when authorized.

## 7. Next handoff and no-go boundaries

**Next requested Human decision:** review the proposed **pre-delete handoff** approach and the eight SL-D decisions, then issue a bounded implementation task for the minimum C1/host sequencing after required accepted dependencies. Do not create a durable copy or retain original images by default.

**Current status:** `SPECIFICATION CANDIDATE / INTEGRATION BLOCKED / RUNTIME NOT IMPLEMENTED / REVIEW NOT RUN`.

No commits to implementation branches; no merge, Draft-to-Ready, CI/security bypass, public/production deployment, live/paid AI, confidential/real paper handling, current backend policy change, Claims activation or fabricated original 2026-11-18 receipt.
