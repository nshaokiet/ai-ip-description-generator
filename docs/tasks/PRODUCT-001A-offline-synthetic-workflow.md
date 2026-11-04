# PRODUCT-001A — internal offline synthetic upload-to-export

Version: 0.1.0. Date: 2026-11-04. Owner/implementer: Codex.
Status: implementation candidate; independent review and CI pending. Not completed.
Authorization: Human `RESUME-AIIP-PRODUCT-001A-20261104`; USD 0, no merge or deployment.
Breaking change: No. Additive internal service; existing routes and C1 defaults retained.

## Base and scope

Base: public main `53c253be874236c6f38a5333a6f7f3390de9f51e`, containing C1
PR #139 merge `7abc63e12e18a8027de1d4be4c71ad7aa182cb91`. Required custody,
reconstruction, specification, supported draft Claims, assembly and renderer code
already exists there. PRODUCT-001A was absent. This isolated branch imports no
other implementation branch or local dependency candidate.

Primary design reference: [PREAPI-C2 REVISION-004, PR #146](https://github.com/nshaokiet/ai-ip-description-generator/pull/146),
specification head `29daeb208f7736a448297f699e674192c124c7da`. That proposed
specification is a reference, not evidence that all C2 capabilities are implemented.
Human's newer PRODUCT-001A scope permits this smaller independently tested increment.

## Implemented behavior

`OfflineSyntheticWorkflow` is a trusted same-process host service. Construction
pins one injected offline runtime, fixture byte identities, live invocation
authorization and the existing Human-review authorizer. It is disabled by default;
an empty fixture policy admits nothing. No application route enables it.

1. The trusted host registers synthetic PDF/DOCX bytes using existing upload
   validation/storage/registry services. `start(document_id)` checks the configured
   byte identity, MIME, size and actual stored hash before any extraction.
2. C1 leases and rehashes that newly registered document, prepares the actual
   envelope, validates extraction grounding against it, then executes the existing
   reconstruction/specification/Claims/assembly validators. Source bytes and
   registry entry are removed by existing custody cleanup.
3. `review(ref)` returns all seven retained originals as immutable object/array
   nodes, with original digests and a content snapshot digest. `review_documents`
   converts them to a detached complete JSON tree for a trusted presenter. Optional
   absent fields, explicit nulls, array order, warnings, source text, Claims support,
   questions and missing information survive without flattening/truncation.
4. The host must present that complete tree before an affirmative `acknowledge`
   using its snapshot digest. C1 additionally binds the actual locked custody,
   owner, document, revision, token hash, actor, context and decision. Missing or
   mismatched binding fails closed. Incomplete Claims require a separate subsequent
   affirmative invocation. Local acknowledgment never changes source review labels
   or establishes legal/semantic acceptance.
5. `render(ref)` invokes the existing assembler/validator/renderer. It returns only
   the four fixed draft filenames, MIME, size and hashes, bound to custody, document,
   source, revision, snapshot and a canonical manifest digest. `download` requires
   that exact digest and revalidates C1 custody and all artifacts before returning
   bytes; it also checks the returned bytes against the advertised artifact hash.
6. `revise` rederives from the retained source, rotates private revision authority,
   clears review and deletes old exports. Old references/snapshots/manifests fail.
   `abort` removes generated outputs. Expiry invalidates authority and cleans output.

References select private host handles; possession is insufficient without current
trusted invocation authorization. Each host instance serves one principal; the
callback must verify that same principal, not merely any authenticated user.
Host operations are serialized, live sessions
are limited to four, and no projection/challenge history is cached. Reads do not
extend idle TTL. Snapshot construction rejects non-JSON/nonfinite values, more than
100,000 nodes, depth over 64, strings over 1 MiB, or payloads over 8 MiB before
creating the immutable copy. These are projection limits, not a process RAM bound.
No private C1 records are accessed by the adapter.

## Deliberate limits relative to full C2

- This is an internal product/test increment, not the full C2 pilot, public upload
  bridge, browser review UI, CLI presenter or authentication system.
- The trusted host directly supplies current invocation authorization; there is
  no OperatorRef registry, upload-lease protocol or presenter/challenge ledger.
  Review content is not automatically displayed, interpreted or acknowledged.
  The host must not wire this interface directly to an untrusted transport.
- Complete review data is grouped under `projection.originals` rather than seven
  duplicate DTO properties. All seven schema documents remain available verbatim.
- Four deterministic binaries and a pinned hash manifest are local **test inputs**,
  not Human-approved C2 pilot sources. Tests verify pinned bytes rather than deriving
  an allowlist from arbitrary uploaded data. No Human fixture approval is claimed;
  approval/admission and presenter requirements for a broader C2 pilot remain open.
- The narrowly source-checking injected test runtime accepts the exact synthetic
  technical text, binds analysis metadata/evidence to the actual new upload, and
  rejects unsupported text. It is not a semantic extractor for arbitrary papers.
- The adapter serializes snapshot creation and retains none. Full C2 cross-host
  aggregate projection accounting and a trusted inert presenter remain future work.
- Supported draft Claims are used internally under existing synthetic validators;
  production Claims, real papers, provider authorization and filing readiness stay off.

## Validation and review

Acceptance tests: `tests/backend/test_product_synthetic_workflow.py`. Run with the
repository's Python test environment:

```text
python -m pytest tests/backend/test_product_synthetic_workflow.py -q
```

Coverage includes new registered PDF/DOCX identity, complete source/evidence/digest
preservation, parsed PDF/DOCX outputs, Human and incomplete-Claims gates, mixed
documents, stale references/reviews/manifests, forged evidence, tampered artifacts
and MIME, unauthorized invocations, expiry during reads/review, cleanup/retry,
projection/revision concurrency, resource limits and bounded session capacity.
Provider/network tripwires cover both complete happy paths. Related C1 custody and
existing v1 local-orchestration tests are regression targets.

Exact results and immutable review SHA belong in the fixed-SHA review handoff and
Draft PR. Independent Gemini review must be actually obtained; self-check is not PASS.
Final local per-case results: PRODUCT-001A **33 PASS**, C1 custody **22 PASS**,
existing v1 API **19 PASS**, with **0 unresolved FAIL / 0 SKIP**. These results combine
targeted runs: 31 product cases passed together; the two happy paths were rerun and
passed after correcting a DOCX-header assertion. C1/v1 successes were retained
without repeating unchanged tests. Earlier missing-temp-directory and test-expectation
failures are preserved in local JUnit evidence, not represented as successful runs.
One existing Starlette/AnyIO deprecation warning was observed.
No required CI or security finding is waived. Frontend dependencies are inherited
unchanged from public main (Next 16.3.8); known dependency/minimatch findings remain
open. The separately reviewed local dependency patch is not incorporated here.

## Handoff

Task ID: PRODUCT-001A
Agent: Codex — Lead Implementer
Reviewer: Gemini / Antigravity — strict read-only; pending actual review
Status: Implementation candidate; not merged/completed
Version: 0.1.0
Work completed: Internal upload/custody/review/export adapter and additive bound C1 review
Files affected: Three service modules, focused tests, synthetic inputs, README and this note
Evidence checked: Public base/ancestry, C1 implementation, C2 REVISION-004, local functional tests
Findings: Full C2 pilot/presenter and semantic AI extraction remain outside this increment
Decisions: Use public main and existing validated pipeline; no other branch imported
Issues: Independent review, hosted CI and inherited security blockers pending
Security impact: Opt-in trusted-process full review data; explicit live authority and byte pinning
Recommended next action: Fixed-SHA independent review, then separately scoped trusted presentation
