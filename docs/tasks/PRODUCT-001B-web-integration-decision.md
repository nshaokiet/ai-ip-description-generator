# PRODUCT-001B — Web integration direction and bounded next increment

**Version:** 0.1.0 — 2026-11-05 (Asia/Ho_Chi_Minh)  
**Task:** PRODUCT-001B (existing proposed workstream); RESUME-FOUNDATION-001 decision/delta  
**Status:** WEB PRODUCT DIRECTION CONFIRMED BY HUMAN; IMPLEMENTATION SPECIFICATION PROPOSED / NOT FROZEN; NOT IMPLEMENTED  
**Owner:** Human / Product Owner; proposed implementer Codex, independent reviewer Gemini/Antigravity strict read-only  
**Workflow:** existing V1 unless a task is explicitly enrolled in V2; USD 0, no live provider  
**Source:** Human's explicit 2026-11-05 continuation instruction; GitHub baseline main `53c253be874236c6f38a5333a6f7f3390de9f51e`.

## 1. Decision, precedence and history

The end product is a **website** (existing Next.js frontend + FastAPI backend), not a terminal application. Target user journey: **PDF/DOCX upload → actual-source custody/preparation → draft generated from that source → browser Human review/edit → revision-bound validation/decisions → four USPTO v2 draft exports**.

This is a prospective product-direction decision, not proof of an implemented browser pipeline, approved public HTTP exposure, approved provider, deployment, security exception, or authorization to merge other PRs.

The historical `PRODUCT-001B — Trusted Local Review Presenter` planning document at [commit `ff511e5`](https://github.com/nshaokiet/ai-ip-description-generator/blob/ff511e5b4e384268224d586a8abd3cea11313655/docs/tasks/PRODUCT-001B-trusted-local-review-presenter.md) proposed **terminal-first**. That document remains intact as historical evidence. **Its terminal-first priority is superseded by the newer explicit Human website direction on 2026-11-05.** Its valuable private-authority, inert presentation, complete review and stale-session guards remain design inputs. No terminal UI implementation is assumed.

The [PREAPI-C2 REVISION-004 specification, Draft #146](https://github.com/nshaokiet/ai-ip-description-generator/pull/146) and [PRODUCT-001A candidate, Draft #149](https://github.com/nshaokiet/ai-ip-description-generator/pull/149) are *dependencies/reference candidates*, not features merged to main. #149 implements a same-process test adapter and no browser route. C1 custody itself was merged via [PR #139](https://github.com/nshaokiet/ai-ip-description-generator/pull/139). The existing P2 components and [P2-006 contract](P2-006-uspto-b2-pdf-docx-rendering.md) define four draft outputs; the current demo shows precomputed samples.

## 2. Bounded browser increment — proposed acceptance scope

**Product result:** An authenticated test operator in a local/isolated web QA environment can use *two intentionally different synthetic source documents*, including a valid text PDF and a DOCX, and export a distinct source-bound four-file package for each, after explicit review. This is a proposed WEB increment, not a public deployment or production readiness declaration.

### Existing services to reuse

- APP-001 validated intake, registry/storage, APP-002 source-envelope parser, C1 actual-byte custody/revision/expiry, and the P2-002…P2-006 reconstruction/specification/Claims/assembly/rendering contracts.
- Reuse a reviewed/accepted PRODUCT-001A adapter or its approved core, without copying a second analysis pipeline into Next.js or a public route. Its constructor/invocation authorization is **trusted-process only**; never serialize the Python adapter or its private handles.
- Existing Next.js UX and FastAPI services are the chosen product stack. A public static demo and a proposed interactive private web workflow are distinct environments.

### Server ownership and transport boundary

- **FastAPI (server)** creates and owns upload admission, original-byte hash, opaque external session ID, authenticated actor/owner, source/custody binding, active revision, full review snapshot, review decisions, validation, export manifest and expiry.
- **Next.js (browser)** receives only a deliberately allowlisted presentation DTO: safe session status, source metadata/hash, reviewable source/evidence, source/revision identifiers safe for display, warnings/missing data, draft sections, explicit review state, and artifact metadata/authorized downloads. Source text is inert escaped data, never executable markup or instruction.
- Browser/URL/log/storage/telemetry MUST NOT receive C1 revision token, token hash, custody capability/handle, private coordinator references, provider secrets, authorization callback implementation, or internal runtime. The browser cannot submit its own custody/owner/review authority.
- The web transport must have a **reviewed session and authentication design**: server-validated user identity and owner isolation; server-side session, HttpOnly cookie, Secure in HTTPS, explicit SameSite policy, CSRF protection on state-changing operations, and Origin/Host validation. If architecture uses a separate backend origin, explicitly specify cookie, proxy and CORS topology before implementation. CORS, unpredictability of URLs and mere possession of a session ID are not authorization.
- **First increment is isolated local synthetic QA, default OFF**. No public HTTP route may be enabled without authentication/security acceptance, authorized fixture policy and explicit deployment task. `render.yaml` is a declarative template, not evidence of the live Render service/configuration.

### Review/revision and export invariants

1. Every upload is a newly registered and independently validated PDF/DOCX. Server owns source SHA-256, MIME and byte size; all downstream evidence/analysis/exports must bind to the same actual source, document and revision.
2. A complete schema-preserving review snapshot is available in the browser, including the **seven originals** from the A/C2 contract, source locator/evidence, warnings, missing data and Claims support. Navigation or pagination may be used, but a partial display must never count as review of an undisplayed snapshot. The server validates full snapshot hash before accepting an affirmative review.
3. Review of draft **content** and separate **incomplete-Claims acknowledgment** are two explicit, non-default decisions. No auto-approve from loading, refresh, Enter, generic checkbox, uploaded instructions or failed rendering. Marks remain `synthetic_draft=true`, `filing_ready=false`; Human acknowledgment is not semantic or legal acceptance.
4. Editing or regenerating source-derived content creates a new authoritative revision (or an explicitly defined edit provenance), invalidating affected prior review, validation and export manifests. Stale revision, stale source, stale decision or changed snapshot rejects render and download.
5. Exactly four *source- and revision-bound* artifacts on successful render, with the existing fixed filenames and MIME:
   
   | Filename | MIME |
   |---|---|
   | `B2_REFERENCE_PREVIEW.pdf` | `application/pdf` |
   | `B2_REFERENCE_PREVIEW.docx` | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` |
   | `USPTO_APPLICATION_DRAFT.pdf` | `application/pdf` |
   | `USPTO_APPLICATION_DRAFT.docx` | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` |
   
   Return only validated bytes through an authenticated, revision- and manifest-bound download; compare actual digest, size and MIME. Never substitute fixed demo files or generate filing-ready/issued-patent assertions.
6. Retain existing custody TTL semantics (C1 idle 1800 s; absolute 7200 s) unless an independently reviewed, expressly authorized change is made. Revocation, expiry, abort and source cleanup fail closed.
7. For **refresh within a live server session**, re-query server authority and revision; re-display as necessary. **Process restart without explicit persistence invalidates all sessions/decisions** and denies stale downloads. Cross-session, cross-owner, tamper and logout deny operations even when an opaque ID is known. No promise of restoration after restart without a separate persisted-state design.

### Measurable web verification

- Two distinct and explicitly admitted synthetic documents: one text-based PDF and one DOCX, with **different source content and source hashes**. Confirm resulting review/source bindings differ; the outputs must derive from each respective source and be nonidentical for source-dependent content.
- In a real browser using the authorized local QA web stack: upload each, inspect complete review, perform deliberate content acknowledgment and (where Claims incomplete) separate acknowledgment, validate, and download all four files. Parse the PDF/DOCX bytes and verify filenames, MIME, SHA-256, manifest and matching actual source/revision.
- Negative tests: unreviewed, incomplete-Claims gate, edit invalidation, stale reference, altered file/digest/MIME, cross-user/session, missing CSRF/origin, forged owner/source, logout, expiry, refresh, server restart and injected script/text. Provider/network tripwires prove USD 0/offline. Include regression for existing v1 routes, C1 and P2; require real browser execution, not solely unit mocks.
- Record exact candidate SHA/tree and test environment. A browser test skipped due Chromium/QA outage is **SKIPPED**, not PASS. A mock/synthetic success does not grant arbitrary-paper semantic acceptance.

## 3. Dependency-aware backlog (proposed, not approved tasks)

| Order | Work package / existing evidence | Technical/user outcome and acceptance | Status/dependency |
|---|---|---|---|
| A | Existing [DEP-001-SR PR #147](https://github.com/nshaokiet/ai-ip-description-generator/pull/147), CI-V2-001 [#144](https://github.com/nshaokiet/ai-ip-description-generator/pull/144), C1 closeout; QA installer | Reconcile **current** audit graph/severity, ensure critical/high gates; isolate Ubuntu snapshot HTTP 503; make required functional checks reachable without weakening evidence upload. Exact-SHA CI, review and protected governance closeout required. No `--force`, waiver or blanket `continue-on-error`. | Existing Drafts; security/CI blockers. Separate small implementation PRs where needed. |
| B | PRODUCT-001A [#149](https://github.com/nshaokiet/ai-ip-description-generator/pull/149), PREAPI-C2 REVISION-004 [#146](https://github.com/nshaokiet/ai-ip-description-generator/pull/146) | Verify original external review provenance and full CI; finalize server-owned web DTO/session/owner/security contract over current C1 and P2 with no second pipeline. | Dependent on candidacy/gate disposition; no merge assumed. |
| C | PRODUCT-001B web increment (**this proposed specification**) | Two distinct sources through browser review/ack to four valid source-bound files, with negative browser/security tests. | Must obtain implementation-scope review and authorization and address A/B gates before merge/deploy. |
| D | Persistence/author answers/review history/retention | Explicit DB schema and tenancy/retention/restore contract; reload survives restart only after verified persistence and migrations. | **PROPOSED**, not part of first web increment; otherwise fail closed. |
| E | EVAL-001 provider/semantic pilot | Funded and authorized model, legal data rights, rubric and gold; measure actual semantic quality and cost. | **AWAITING FUNDING / NOT_DETERMINED**; no provider call authorized. |

**Next single execution target:** Continue existing **DEP-001-SR-20261024 / PR #147** and associated current audit/CI reconciliation, *not* open another parallel security PR. First action: compare `frontend/package-lock.json` and vulnerability graph at #147 HEAD against currently published advisory evidence and [PR #148's 2026-11-04 audit failure](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/41770184393); identify which direct/transitive paths and gates remain unresolved. Audit and necessary remediation are separate from this documentation-only foundation. If independent review or hosted CI is blocked, the separate read-only PRODUCT-001B browser transport/security design can be reviewed without bypassing gates.

## 4. Scope limits, candidate handoff and source status

**No runtime change in RESUME-FOUNDATION-001.** No AI provider/payment, confidential research file, GitHub settings, CI workflow, deployment, production Claims, merge/PR closure, new browser auth release, or assumption of production readiness. Existing C1/P2 and historical terminal plan retain their provenance.

Observations dated 2026-11-05: `main` SHA `53c253be874236c6f38a5333a6f7f3390de9f51e`, tree `6459c1cecb8a4e56f2cbbbeab2e9439a39bd1b6e`; #149 implementation `cf9097fda4688db08fd505e21fcbf3c0e53a9d5c` (OPEN/DRAFT). GitHub PR #149 shows no GitHub-native review submissions; its external Technical PASS is **reported by Human, provenance NOT VERIFIED** with the original Markdown not archived in this verification. [#149 CI](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/41848393889) FAILED; layout install Ubuntu HTTP 503 and a missing security evidence directory; backend and MCP completed, later frontend/browser steps SKIPPED. Prior CI/artifact-quota results remain historical by exact SHA. Remote GitHub metadata does not verify any agent's local dirty worktree or live Render settings.

**Review handoff:** Document-only foundation candidate must be reviewed on its final immutable SHA/tree, with changed paths and a human-assessed scope decision. Do not call any external reviewer PASS until the actual fixed-SHA report exists. A new candidate SHA requires renewed review and CI assessment.

**Resume:** Read `docs/operations/01_PROJECT_CONTROL_CENTER.md` top **RESUME-FOUNDATION-001** section, this file, [PR #147](https://github.com/nshaokiet/ai-ip-description-generator/pull/147), [PR #149](https://github.com/nshaokiet/ai-ip-description-generator/pull/149), and the exact-head CI runs; begin with current security graph/audit reconciliation. Keep the browser target and no-merge gate intact.
