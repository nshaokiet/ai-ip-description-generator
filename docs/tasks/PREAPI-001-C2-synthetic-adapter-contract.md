# PREAPI-C2 — Internal Synthetic Adapter and Review Contract

**Consolidated v0.2.0 candidate — PREAPI-C2-RECOVERY-AND-SPEC-REVISION-004**

**Editorial provenance:** Normal revision from the recovered complete REVISION-003, SHA-256 `ceae2abe2b38bf8963e485a5108801bfbf2ab2cd8aa8870ea65ec43e0042ffa5`. The R4 packet SHA-256 `3fac039034443d616400a4ba784b296275cfd262ec43d6737799953119719db4` also matched. This is not reconstruction. Earlier drafts remain history; author-side resolution is not independent closure.

This document replaces the earlier conversational v0.2.0 candidate. It resolves the identified design gaps for independent review. It does not record Human approval, a frozen specification, implementation acceptance or an independent PASS.

| Attribute | Value |
|---|---|
| Original architecture author | Codex — Specification Architect |
| REVISION-004 author | Codex — Lead Software Architect & Specification Engineer |
| Architecture recommendation | Option A: internal, same-process, synthetic-only adapter |
| Authorized work | Isolated local documentation and offline QA; protected repository read-only |
| Budget | USD 0 |
| Implementation authorization | NOT GRANTED |
| Independent reviewer | Gemini 3.8 Flash High / Antigravity |
| Candidate status | `PREAPI-C2 REVISION-004 — SPECIFICATION CANDIDATE READY FOR INDEPENDENT REVIEW` |
| Git identity of this revision | None; standalone review artifact only |

The changes from earlier candidates are explicitly superseding proposals within the unapproved v0.2.0 draft. The earlier conversational content remains historical; it must not be represented as the same immutable reviewed artefact.

## 1. Baseline and governance

### 1.1 Source baseline

The implementation baseline is C1 merge commit:

`7abc63e12e18a8027de1d4be4c71ad7aa182cb91`

[PR #139](https://github.com/nshaokiet/ai-ip-description-generator/pull/139) is **MERGED**. Its premerge implementation HEAD was `8eee90cc4e7c4e3916c76132c1ce92e8bf85182a`.

Implementation sources were re-read as immutable local Git blobs at the cited SHAs; current remote metadata was checked through read-only GitHub connector calls. Evidence includes:

- C1 coordinator, APP-001 registry/storage and APP-002 models.
- P2-003 specification schema v2.0.0.
- P2-004 supported-Claims schema v1.0.0.
- Relevant reconstruction schema, generators, validators, renderer and C1 tests.
- C2 specification and decision package at their supplied immutable SHAs.
- PR metadata and the three CI runs below.

| Item | Evidence-backed state |
|---|---|
| C2 [PR #140](https://github.com/nshaokiet/ai-ip-description-generator/pull/140) | OPEN / DRAFT; HEAD `0b46eea63679380cff0d93d2864f04238738a7fd` |
| Decision package [PR #143](https://github.com/nshaokiet/ai-ip-description-generator/pull/143) | OPEN / DRAFT; HEAD `df2eacba73ad8d0ce580e7ed83933af4f0484fe8` |
| C1 postmerge [CI #39555439292](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/39555439292) | COMPLETED / FAILURE |
| C2 [CI #39545978861](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/39545978861) | COMPLETED / FAILURE |
| Decision package [CI #39558639521](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/39558639521) | COMPLETED / FAILURE |

All three runs show successful `mcp-tests`, failed artifact-upload steps in `build-and-test`, and skipped downstream checks. The decision package records artifact-storage quota exhaustion. No quota recovery, replacement CI SUCCESS or CI exception is established here.

C1 merge is established. C1 postmerge closeout remains pending. Previous local or premerge successes do not replace failed postmerge CI.

### 1.2 Current observation and gates

Current GitHub main, observed 23/10/2026 Asia/Saigon: `53c253be874236c6f38a5333a6f7f3390de9f51e`, tree `6459c1cecb8a4e56f2cbbbeab2e9439a39bd1b6e`. C1 merge tree: `ba835b5ca00dd399076c91ab010001d1c07ffa04`. PR #140/#143 remain Draft at their listed heads. A GitHub computed test-merge SHA is not an actual merge receipt.

Local checkout is detached at `102b7e90dc3bfc1f79c197a20184f97b89070bf2` and already has a modified `tools/project-orchestrator-mcp/package-lock.json`. It predates C1 and was not treated as current main. Explicit Git object reads avoided checkout/fetch/ref changes.

Gemini independent review PENDING; Human architecture approval PENDING; approved synthetic fixtures **0**; C1 additive extensions NOT IMPLEMENTED; C2 implementation authorization NOT GRANTED; C2 integration tests NOT RUN; required hosted CI SUCCESS NOT ESTABLISHED; product runtime readiness NOT DETERMINED; publication NO-GO; API budget USD 0.

### 1.3 Mandatory boundaries

C2 MUST preserve:

1. C1 authority over actual uploaded bytes, custody and revisions.
2. All seven retained originals and their canonical digests.
3. Supported-Claims restrictions and separate incomplete-Claims acknowledgment.
4. Exactly four manifest-bound draft artifacts.
5. Released v1 compatibility.
6. Existing source schemas, accepted gold data and baseline evidence.
7. `synthetic_draft=true` and `filing_ready=false`.

C2 remains default disabled. It introduces no HTTP endpoint, browser UI, persistent owner/tenant model, live-provider execution, production Claims activation or deployment.

The sealed offline checkpoint remains untouched.

## 2. Architecture and authority

```text
Trusted host
 ├─ Operator registry
 ├─ Newly registered upload bindings
 ├─ Session-handle registry
 ├─ Trusted review presenter
 └─ One-time challenge ledger
              |
              v
       C2SyntheticAdapter
              |
              v
 Dedicated C1 coordinator
 ├─ Existing custody/revision/expiry authority
 ├─ Proposed immutable review projection
 └─ Proposed bound-review guard
              |
              v
 Existing P2-002…P2-006 components
              |
              v
 Four verified synthetic draft artifacts
```

The trusted host establishes local operator authority. APP-001 establishes document metadata and storage identity. C1 establishes custody. These are distinct responsibilities.

The adapter is the exclusive application access path to its dedicated C1 coordinator. Direct use of that coordinator by other application components is outside the C2 contract.

Arbitrary malicious Python execution inside the trusted process is outside this boundary. Object references, opaque identifiers and hashes do not establish production authentication.

### 2.1 Required additive C1 extensions

Two additions are proposed:

| Extension | Purpose |
|---|---|
| `get_review_projection()` | Return a complete immutable, validated revision snapshot |
| Optional bound-review mode and guard | Check review authorization against the actual C1 record under its lock |

The existing callback remains:

```python
def review_authorizer(actor: str, context: str, decision: str) -> bool: ...
```

Its signature is unchanged.

The second extension is necessary because those three arguments do not identify the actual custody record being acknowledged. C2 preflight and a challenge string alone cannot prove that C1 is processing the intended record.

Legacy C1 callers retain existing behavior when bound-review mode is disabled. C2 MUST use a dedicated coordinator with bound-review mode enabled.

## 3. Typed contracts

The following are proposed interfaces, not implemented APIs.

### 3.1 Immutable, schema-preserving review data

The projection uses a recursively immutable JSON representation. This preserves the actual schemas without maintaining a second, incomplete set of flattened content DTOs.

```python
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Protocol, TypeAlias


@dataclass(frozen=True, slots=True)
class FrozenObject:
    members: tuple[tuple[str, "FrozenJSON"], ...]


@dataclass(frozen=True, slots=True)
class FrozenArray:
    values: tuple["FrozenJSON", ...]


FrozenJSON: TypeAlias = (
    None | bool | int | float | str | FrozenObject | FrozenArray
)


OriginalKey = Literal[
    "source_envelope",
    "structured_analysis",
    "reconstruction",
    "specification",
    "p2_003_generation_config",
    "supported_claims",
    "p2_004_generation_config",
]


@dataclass(frozen=True, slots=True)
class OriginalDigest:
    original: OriginalKey
    sha256: str


@dataclass(frozen=True, slots=True)
class C1ReviewProjection:
    projection_version: Literal["0.2.0"]
    coordinator_instance_id: str
    custody_id: str
    document_id: str
    revision: int
    state: str

    source_sha256: str
    originals_sha256: tuple[OriginalDigest, ...]

    source_envelope: FrozenObject
    structured_analysis: FrozenObject
    reconstruction: FrozenObject
    specification: FrozenObject
    p2_003_generation_config: FrozenObject
    supported_claims: FrozenObject
    p2_004_generation_config: FrozenObject

    claims_review_required: bool
    review_snapshot_sha256: str
    render_policy_baseline: str

    synthetic_draft: Literal[True] = True
    filing_ready: Literal[False] = False
```

Normative construction rules:

- Every JSON object becomes a `FrozenObject`; every array becomes a `FrozenArray`.
- No mutable dictionary, list, Pydantic object, `Path`, lock or `_Record` reference is retained.
- Object keys are unique; array order is preserved.
- Optional-property absence remains distinct from explicit JSON `null`.
- Strings, numbers, enum values and source IDs are preserved exactly.
- Non-finite numbers and non-JSON objects are rejected.
- Freezing must enforce these rules at runtime; annotations and `frozen=True` alone are insufficient.
- All seven originals appear exactly once in `originals_sha256`.

The seven document fields are schema-constrained values. `FrozenObject` does not permit arbitrary unvalidated additions.

### 3.2 Host references and internal handles

```python
@dataclass(frozen=True, slots=True)
class OperatorRef:
    host_epoch: str
    binding_id: str


@dataclass(frozen=True, slots=True)
class UploadLeaseRef:
    host_epoch: str
    lease_id: str


@dataclass(frozen=True, slots=True)
class C2SessionRef:
    host_epoch: str
    session_id: str


@dataclass(frozen=True, slots=True)
class C2SessionHandle:
    """Host-private; never returned in a human-facing view."""
    session_ref: C2SessionRef
    coordinator_instance_id: str
    operator_binding_id: str
    owner_scope: str = field(repr=False)
    custody_id: str
    revision: int
    revision_token: str = field(repr=False)


@dataclass(frozen=True, slots=True)
class C2ArtifactSummary:
    filename: str
    media_type: str
    size_bytes: int
    sha256: str


@dataclass(frozen=True, slots=True)
class C2SessionView:
    session_ref: C2SessionRef
    document_id: str
    revision: int
    state: str
    evidence_count: int
    claims_review_required: bool
    review_snapshot_sha256: str
    artifacts: tuple[C2ArtifactSummary, ...]
    synthetic_draft: Literal[True] = True
    filing_ready: Literal[False] = False
```

An `OperatorRef` or `C2SessionRef` is a lookup selector. Possession does not establish authority.

The trusted host MUST resolve an operator against its live registry and the current trusted invocation context. Caller-authored strings or reconstructed DTOs alone cannot establish operator authority.

### 3.3 Review references and actual C1 target

```python
ReviewDecision = Literal[
    "CONTENT_REVIEW_ACKNOWLEDGED",
    "CLAIMS_INCOMPLETE_ACKNOWLEDGED",
]


@dataclass(frozen=True, slots=True)
class ReviewDisplayRef:
    host_epoch: str
    display_id: str


@dataclass(frozen=True, slots=True)
class ReviewChallengeRef:
    host_epoch: str
    challenge_id: str


@dataclass(frozen=True, slots=True)
class C1ReviewTarget:
    """Created by C1 from the actual locked record."""
    coordinator_instance_id: str
    custody_id: str
    document_id: str
    owner: str
    revision: int
    revision_token_sha256: str
    review_snapshot_sha256: str
    actor: str
    context: str
    decision: ReviewDecision


class HumanReviewAuthorizer(Protocol):
    def __call__(
        self, actor: str, context: str, decision: str
    ) -> bool:
        ...


class BoundReviewAuthorizer(Protocol):
    def __call__(self, target: C1ReviewTarget) -> bool:
        ...
```

`C1ReviewTarget` stays inside the trusted process. It is not a human-facing projection.

### 3.4 Proposed C1 signatures

```python
# Additive constructor options:
require_bound_review: bool = False
review_binding_authorizer: BoundReviewAuthorizer | None = None

# Additive read-only projection method:
def get_review_projection(
    self,
    custody_id: str,
    *,
    owner: str,
    revision_token: str,
) -> C1ReviewProjection:
    ...
```

Existing `acknowledge_review()` and `acknowledge_incomplete_claims()` signatures remain unchanged.

For C2:

- `require_bound_review` MUST be true.
- Both authorizers MUST be installed.
- Missing configuration fails closed.
- Bound-review configuration and coordinator identity are fixed for that coordinator’s lifetime.
- Runtime replacement with a permissive callback is unsupported.

### 3.5 Proposed C2 signatures

```python
class C2SyntheticAdapter(Protocol):
    def start_session(
        self,
        upload: UploadLeaseRef,
        *,
        operator: OperatorRef,
        p2_003_generation_config: FrozenObject,
        p2_004_generation_config: FrozenObject,
    ) -> C2SessionView:
        ...

    def get_view(
        self, session: C2SessionRef, *, operator: OperatorRef
    ) -> C2SessionView:
        ...

    def get_review_projection(
        self, session: C2SessionRef, *, operator: OperatorRef
    ) -> C1ReviewProjection:
        ...

    def acknowledge_content_review(
        self,
        session: C2SessionRef,
        *,
        operator: OperatorRef,
        expected_revision: int,
        challenge: ReviewChallengeRef,
    ) -> C2SessionView:
        ...

    def acknowledge_incomplete_claims(
        self,
        session: C2SessionRef,
        *,
        operator: OperatorRef,
        expected_revision: int,
        challenge: ReviewChallengeRef,
        acknowledge: bool,
    ) -> C2SessionView:
        ...

    def revise(
        self,
        session: C2SessionRef,
        *,
        operator: OperatorRef,
        expected_revision: int,
        p2_003_generation_config: FrozenObject | None = None,
        p2_004_generation_config: FrozenObject | None = None,
    ) -> C2SessionView:
        ...

    def render(
        self,
        session: C2SessionRef,
        *,
        operator: OperatorRef,
        expected_revision: int,
        expected_snapshot_sha256: str,
    ) -> C2SessionView:
        ...

    def download(
        self,
        session: C2SessionRef,
        *,
        operator: OperatorRef,
        expected_revision: int,
        filename: str,
    ) -> bytes:
        ...

    def abort(
        self, session: C2SessionRef, *, operator: OperatorRef
    ) -> None:
        ...
```

Challenge issuance is a trusted-host operation following presentation and an explicit affirmative operator action. It is not a generic adapter method accepting caller-authored approval JSON.

## 4. Upload and session-handle lifecycle

**Additional invariant (REVISION-003):** Admission of a C2 input requires trusted synthetic-source provenance *before APP-001 registration/parsing and again before C1 custody commit*. A process-local owner binding or `SyntheticExtractionRuntime.synthetic_only=True` does not prove that source bytes are approved synthetic content. Only an exact, independently approved fixture-byte digest matching a trusted admission manifest can qualify under this pilot. The policy does not alter or purport to secure pre-existing public APP-001 upload routes.

### 4.0 Synthetic Source Admission Policy — required before upload binding

This additional C2-specific policy addresses the independent review's synthetic-provenance finding without changing APP-001, C1, accepted gold data or source schemas. The gate is mandatory for any C2 pilot invocation, including local CLI/test harness use. Untrusted documents are not silently labeled synthetic, and C2 does not admit real, private or unpublished manuscripts under the zero-cost synthetic-only authorization.

**Trust root.** The trusted host loads an explicitly Human-approved *fixture manifest* from a pinned read-only artifact or reviewed source-code constant. The manifest must be covered by an approved SHA-256 digest or equivalent immutable review identity. Unreviewed changes to the manifest, a mutable workspace file, user-authored fixture metadata, a filename, a fake `synthetic=True` flag or a mere content hash not anchored to a trusted allowlist provide no admission authority. This is an exact-byte authorization policy, not a mathematical proof that the content was artificially generated.

Each approved manifest entry MUST include:

- `fixture_id` (stable unique identifier), `sha256` (digest of the actual approved PDF/DOCX bytes), permitted `media_type`, and declared `size_bytes`;
- `provenance_kind=APPROVED_SYNTHETIC_FIXTURE`, evidence of explicit fixture approval and purpose `PREAPI_C2_OFFLINE_SYNTHETIC`; and
- the manifest version/digest, fixed for the lifetime of a trusted host epoch.

No digest is approved by default. The *current known repository baseline does not establish any reviewed binary PDF/DOCX fixture entries under `tests/fixtures`*. Accepted gold JSON records and hashes of generated *analysis* are not substitute PDF/DOCX source-byte allowlist entries. Therefore, until actual PDF/DOCX test bytes and their manifest are reviewed and approved, **C2 input admission MUST fail closed**. A future Human decision must approve additions to the fixture set; the implementation must not synthesize trust from fixture filenames or freely generate its own allowlist entries at runtime.

**Proposed types (new C2-only contract):**

```python
from dataclasses import dataclass
from typing import Literal, Protocol

@dataclass(frozen=True, slots=True)
class ApprovedSyntheticFixture:
    fixture_id: str
    sha256: str
    media_type: Literal[
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ]
    size_bytes: int
    provenance_kind: Literal["APPROVED_SYNTHETIC_FIXTURE"]
    approved_purpose: Literal["PREAPI_C2_OFFLINE_SYNTHETIC"]
    approval_reference: str

@dataclass(frozen=True, slots=True)
class SyntheticAdmissionReceipt:
    fixture_id: str
    fixture_sha256: str
    fixture_size_bytes: int
    media_type: str
    approved_manifest_sha256: str
    host_epoch: str
    admission_nonce: str

class SyntheticSourceAdmissionPolicy(Protocol):
    def authorize_source_bytes(
        self, source: bytes, *, media_type: str
    ) -> SyntheticAdmissionReceipt:
        """Verify exact bytes against the pinned manifest before APP-001 parsing."""
        ...

    def verify_registered_source(
        self, receipt: SyntheticAdmissionReceipt, *,
        registered_sha256: str, registered_size_bytes: int,
        registered_media_type: str,
        stored_sha256: str,
        stored_size_bytes: int,
        validated_media_type: str,
    ) -> None:
        """Revalidate the approved source binding before C1 custody."""
        ...
```

These signatures are conceptual. Production code may use bounded streams in place of `bytes`; the security invariants cannot be weakened. The policy must compare full lower-case SHA-256 digests, media type, and exact size against a trusted pinned manifest; validate actual file signatures using the existing APP-001 validation machinery; enforce configured source-size bounds; reject duplicate/ambiguous manifest entries; and avoid following out-of-bound paths or symlinks. The manifest is not populated from arbitrary client data.

**Normative admission sequence** (before any synthetic extraction):

1. The trusted host obtains candidate bytes from a trusted local fixture provider, not an unverified public upload ID.
2. The host computes the SHA-256 of those bytes and checks an existing approved manifest entry **before APP-001 registration or parsing**. An unknown digest, missing approved manifest, wrong MIME/size, source-size violation or untrusted provenance fails closed.
3. The host registers only the approved bytes using existing local APP-001 services, creates a one-time upload binding and stores its `SyntheticAdmissionReceipt` privately with the binding.
4. Immediately before C1 `commit_upload`, C2 validates manifest identity, host epoch, admission receipt, registered record digest, size and media type; checks that the binding belongs to the current live operator; and consumes the one-time lease.
5. C1 retains final authority to lease the registered bytes, rehash them and reject source tampering. A mismatch must not be bypassed by re-declaring a digest.
6. The host enforces the pinned runtime factory/identity checks in section 4.5 in addition to C1 marker compatibility. Source admission and runtime authorization are separate; the marker alone confers no approval.

**Boundary and failure behavior.** The gate protects the new C2 synthetic pilot. It does not retroactively prohibit APP-001's existing standalone HTTP upload route or assert that route authenticates real research owners. Existing unbound APP-001 uploads are ineligible for C2. If an unknown document is rejected *before registration*, C2 has no document registry/storage entry to clean up. If already registered by the trusted host, only resources owned by that host entry may be cleaned using existing verified cleanup semantics; foreign uploads must remain untouched. Do not promise cryptographic secure deletion or leak raw file hashes or paths in errors.

Rejection maps to proposed **`C2SourceAdmissionError`** with a fixed source-safe message, e.g. `"Input is not an approved synthetic fixture for this pilot."` This is **not** a pre-existing C1 `CustodyError` code. Log only a bounded opaque decision reference and category. Do not emit source text, user-supplied filenames, manifest path or source digest in user-facing errors. There is no automatic override from a test callback, missing manifest or user-supplied `synthetic=True` flag.

**Test fixture preparation:** For PDF/DOCX happy-path tests, first obtain separately approved deterministic synthetic binary fixtures and pin their exact hashes in the trusted manifest. If none are available, report the C2 admission happy paths **BLOCKED_BY_UNAPPROVED_FIXTURE**; do not mark tests PASS by dynamically trusting arbitrary/generated input. Negative admission tests can run with an empty allowlist. No paid provider is needed.

### 4.1 Binding a newly registered upload

APP-001 `DocumentRecord` has these fields:

`document_id`, `file_name`, `media_type`, `size_bytes`, `page_count`, `sha256`.

It has no owner field. This is confirmed by the [registry source](https://github.com/nshaokiet/ai-ip-description-generator/blob/7abc63e12e18a8027de1d4be4c71ad7aa182cb91/backend/app/services/document_registry.py).

The trusted host MUST:

1. Establish a live local operator binding.
2. Require an approved `SyntheticAdmissionReceipt` for exact source bytes, then register only those bytes through local APP-001 services.
3. Create a private upload-binding entry containing document ID, registered digest, approved fixture ID/manifest digest, operator binding, host epoch and one-time lease state.
4. Return only its `UploadLeaseRef`.
5. Reverify the approved source admission, registered digest/size/MIME, live operator and binding; atomically consume the lease before C2 custody.

A naked APP-001 document ID or a forged `synthetic=True` claim cannot initiate C2 custody. Existing HTTP uploads do not acquire authenticated ownership through possession of their IDs.

A foreign, forged or reused lease is rejected before calling C1. C2 MUST NOT delete a foreign upload while rejecting it.

This mechanism supplies local workflow ownership only. It does not establish multi-tenant isolation.

### 4.2 Closing the start/handle mismatch

`start_session()` returns `C2SessionView`, which includes `session_ref`.

The trusted host privately stores:

```text
session_ref
  → operator binding
  → owner scope
  → dedicated C1 instance
  → custody ID
  → current revision and secret token
  → operation lock
  → lifecycle state
```

Every later adapter operation accepts `session_ref`, verifies the live operator binding and resolves the private current handle.

No later operation requires the operator to obtain a `C2SessionHandle`.

The human-facing view contains no revision token, token fingerprint, owner capability or private path.

### 4.3 Publication and rotation

Before intake, C2 reserves a host session slot. It publishes a live session reference only after:

- C1 returns a valid receipt.
- The initial complete projection succeeds.
- The private handle and owner binding are installed atomically.

If postcommit projection or handle publication fails, C2 invalidates admission and attempts C1 abort using the receipt it already holds. It does not return a partially initialized session.

A successful revision atomically replaces the private handle with the new revision/token and invalidates previous challenges, display records, cached projections and artifact summaries.

The public `session_ref` may remain stable. Mutating operations require an explicit `expected_revision`; C2 must not silently apply an old operator action to the latest revision.

A failed no-op or invalid revision preserves the prior valid handle when C1 confirms that no transition occurred.

An uncertain revision result suspends local access. C2 cannot invent or recover an unknown new token.

### 4.4 Locking and invalidation

Lock order is:

```text
C2 per-session operation lock
  → C1 record lock
    → short challenge-ledger lock
```

Registry locks protect short lookup/publication operations and MUST NOT be held while invoking C1.

Authorizer callbacks MUST NOT call C1, request user input, perform I/O or acquire the C2 operation lock.

Abort atomically marks the host entry terminal, detaches its active handle and invalidates all associated challenges and display references before attempting cleanup.

Expiry is evaluated before every operation and again by C1 under its record lock. At the deadline, authorization is invalid even if a timer has not yet removed the registry entry. The first observer atomically terminalizes the host entry.

No other C2 operation can use a detached handle. A private cleanup attempt may retain the prior token briefly; it cannot restore session access.

An already returned immutable projection cannot be recalled from a caller’s memory. Abort and expiry invalidate its authority, not physically erase every copy.


### 4.5 Trusted synthetic runtime factory — R4-F01 / recovery F07

**RT-01: construction authority.** The trusted host composition root statically imports one fixed local deterministic runtime implementation and its factory from a separately reviewed implementation artifact. A proposed design ID is `C2_LOCAL_DETERMINISTIC_V1`; no approved implementation is asserted to exist today. Its real source/version identity must be assigned and reviewed during separately authorized implementation.

Session callers, source text, fixture metadata and operator actions cannot supply runtime objects, factory objects, classes, import paths, model names or provider-selection keys. No plugin framework or new external service is introduced.

```python
@dataclass(frozen=True, slots=True)
class PinnedSyntheticRuntime:
    host_epoch: str
    runtime_id: str
    implementation_reference: str
    runtime: "SyntheticExtractionRuntime" = field(repr=False)

def construct_trusted_synthetic_runtime(
    *, host_epoch: str
) -> PinnedSyntheticRuntime:
    """Host-private fixed factory; no caller-selected dependency."""
    ...

def verify_pinned_runtime(binding: PinnedSyntheticRuntime) -> None:
    """Reject accidental instance/type/method/configuration replacement."""
    ...
```

The host retains expected instance identity, exact concrete type, extraction-method identity, runtime ID, immutable implementation reference and epoch privately. This contract does not accept a factory injected by an arbitrary caller as proof of trust. Factory and identity policy are fixed imports of the reviewed composition artifact. Subclasses/wrappers require separate review.

The existing C1 `SyntheticExtractionRuntime.run_extraction(envelope, *, correlation_id=None)` protocol and returned object's `.analysis` compatibility remain. The proposed concrete runtime returns bounded deterministic synthetic analysis that must pass C1's canonical and grounding validators; this document implements none of it.

**RT-02: initialization and lifecycle.** At explicitly enabled host initialization, the fixed factory builds the expected instance using reviewed deterministic local dependencies only. The host checks the pinned binding before becoming ready, before consuming an upload lease, immediately before passing that exact runtime to C1, and before later session transitions. A host lifecycle lock prevents cooperating rebinding during intake. The runtime is never reselected from mutable configuration or environment during a session. Identity/configuration mismatch denies new extraction and suspends affected C2 sessions.

A marker-spoofing or otherwise unapproved runtime must be rejected before its `run_extraction()` is invoked. The existing C1 marker `getattr(extraction_runtime, "synthetic_only", None) is True` is only a compatibility check, not runtime authorization.

**RT-03: dependency ownership.** The factory owns only deterministic local extraction dependencies and bounded static synthetic model data. The host separately owns APP-001 storage/registry/validator, APP-002 preparation, source admission, operator/upload/session registries, presenter, ledger and dedicated C1 coordinator. Runtime identity and source fixture admission are independent: neither authorizes the other. The source manifest cannot select a runtime. Generation configs are validated and cannot introduce provider/fallback settings.

Neither factory nor runtime may construct live-provider clients, read credentials for provider selection, invoke LLMs/agents, retrieve source URLs, create subprocesses or use network fallback. Local extraction failure is a failure, not permission to select another implementation.

**RT-04: verification and threat limit.** The existing provider tripwire covers host/factory initialization, denied admission, extraction and later operations in the test process. Normal flow must show zero unexpected provider/client construction and zero disallowed egress; intentional blocked probes are reported separately. This is interception evidence, not a universal transport counter or an operating-system network sandbox.

Accidental dependency misconfiguration is in scope. Arbitrary hostile Python code that can rewrite trusted modules, identities or callback state is outside the process-local boundary. Tests may deliberately miswire a composition root and label this simulation, never a production approval.

The host remains default OFF. No runtime-factory C1 API extension is needed: C2 owns construction and passes its pinned instance through C1's existing parameter.

## 5. Complete review projection

### 5.1 Definition of completeness

A complete reviewable snapshot contains the exact validated JSON content of **all seven originals for one C1 revision**, plus source identity, digest references and the pinned render-policy baseline.

It includes every required field and every optional field actually present. No source text, warning, support reference, question or incomplete-content marker is silently dropped.

This avoids the omissions in the earlier flattened DTOs.

The projection is constructed from retained data, not regenerated independently by C2.

### 5.2 Schema-to-projection mapping

| Actual source | Projection destination | Required review content |
|---|---|---|
| APP-002 envelope | `source_envelope` | Document metadata; every source unit’s `evidence_id`, `evidence_type`, `locator`, `content` |
| AI-001 validated analysis | `structured_analysis` | Complete validated analysis and its source/evidence references |
| P2-002 reconstruction | `reconstruction` | Complete invention model, provenance, source artifacts, conflicts, evidence, missing information, questions and warnings |
| P2-003 complete output | `specification` | Metadata, section order, all sections/subsections, dedicated Claims and Abstract structures, review boundary and full review package |
| P2-003 input config | `p2_003_generation_config` | Exact validated config used for this revision |
| P2-004 complete output | `supported_claims` | Source identity, config, families, Claims, elements, review boundary and full review package |
| P2-004 input config | `p2_004_generation_config` | Exact validated config used for this revision |

The projection preserves these particular schema details:

| Concern | Exact schema content retained |
|---|---|
| Abstract | `specification.abstract`: `section_id`, sequence, heading, status, text, word count, support and missing-information IDs |
| Main sections | Section ID, sequence, heading, status, paragraphs, subsections, figures, missing-information IDs and optional not-applicable basis |
| Nested Background | `FIELD_OF_THE_INVENTION` and `DESCRIPTION_OF_RELATED_ART` subsection objects, including their own status and support |
| Paragraph support | `source_paths`, `evidence_ids`, `grounding_class`; paragraph ID and sequence |
| Figures | `figure_id`, `figure_label`, title, description, `source_figure_ids`, and complete reference-numeral entries |
| P2-003 missing information | `missing_id`, `target_section_id`, description, `author_question_ids` |
| P2-003 review package | Evidence, missing information, author questions, claim support and warnings |
| P2-004 family support | `source_paths`, `evidence_ids`, `specification_section_ids`, `issue_ids` |
| P2-004 Claim elements | Text, role, sequence, grounding, support, essentiality, upstream IDs, inheritance and optional parameter/relationship fields |
| P2-004 disclosure references | Section/paragraph IDs, specification/reconstruction paths and evidence IDs |
| P2-004 review package | Evidence, element-level claim support, issues, warnings, missing information and author questions |
| P2-004 issues | All actual fields, including entity/source/specification/evidence/missing/question references, support status and message |

The authoritative schemas are [P2-003 v2.0.0](https://github.com/nshaokiet/ai-ip-description-generator/blob/7abc63e12e18a8027de1d4be4c71ad7aa182cb91/schemas/uspto-specification/v2.0.0/uspto-specification.schema.json) and [P2-004 v1.0.0](https://github.com/nshaokiet/ai-ip-description-generator/blob/7abc63e12e18a8027de1d4be4c71ad7aa182cb91/schemas/supported-draft-claims/v1.0.0/supported-draft-claims.schema.json).

### 5.3 Reference semantics

C2 MUST preserve reference namespaces:

- APP-002 evidence locators contain the actual six supported locator fields.
- P2-003 `support.source_paths` refer to reconstruction content according to its existing validation semantics.
- P2-002 `analysis_paths` lead to retained structured analysis.
- P2-004 `specification_path` and `reconstruction_path` are resolved against their respective retained documents.
- P2-004 evidence entries retain their own locator and excerpt.
- P2-003 review evidence descriptions remain descriptions; C2 must not relabel them as APP-002 source units.

Figure `source_figure_ids` are preserved as source references. They are not assumed to be APP-002 evidence IDs or files containing rendered images.

P2-002 source-artifact data remains available to interpret drawing/source references. No missing image or drawing is fabricated.

### 5.4 Claims interpretation

P2-003’s dedicated Claims structure remains visible with its actual status. It is not overwritten with P2-004 Claims inside the projection.

P2-004 remains the source of supported Claims used by existing downstream assembly.

P2-004 Claims identify existing Claims through `claim_number`; families use `claim_family_id`. C2 MUST NOT invent unsupported Claim IDs.

An optional derived display list may identify families whose status is not `PRESENT`, using their actual family IDs. Such a list is supplementary and cannot replace the full family and issue data.

C1’s existing incomplete-Claims predicate remains authoritative:

```text
No Claims
OR overall supported-Claims status != PRESENT
OR any family status != PRESENT
```

A process-local acknowledgment does not rewrite source `review_status=UNREVIEWED`, remove missing information or create legal approval.

### 5.5 Content intentionally excluded

The projection excludes:

- Original PDF/DOCX binary bytes already removed under custody cleanup.
- Private paths, locks, mutable record objects and internal capability tokens.
- Challenge-ledger secrets.
- Rendered artifact bytes and mutable package state.
- Unavailable figure images or information absent from retained originals.

These exclusions do not remove retained textual review content. The snapshot supports review of retained extracted content and derived drafts; it does not establish visual comparison with the original binary paper.

The trusted presenter MUST make all seven documents and their reference navigation available before acknowledgment. A scalar summary or truncated preview is insufficient.

The host can record that complete content was presented and an affirmative action occurred. It cannot prove that a person read or understood every field.

## 6. Projection consistency and resource bounds

### 6.1 Construction

Under C1’s record lock, `get_review_projection()` MUST:

1. Resolve and validate owner, token, state and TTL.
2. Revalidate the seven originals and their digests.
3. Validate the entire artifact manifest when one exists.
4. Check projection resource limits before creating the immutable copy.
5. Freeze all seven documents without truncation.
6. Compute the snapshot digest.
7. Recheck expiry before returning.

It does not refresh idle TTL or change review status.

Expiry or an integrity failure may revoke custody, consistently with existing C1 reads.

### 6.2 Snapshot digest

Use the existing canonical JSON serialization rules and SHA-256 over this exact logical object:

```text
{
  "domain": "PREAPI-C2-REVIEW-0.2.0",
  "coordinator_instance_id": actual coordinator instance,
  "custody_id": actual custody ID,
  "document_id": actual document ID,
  "revision": actual revision,
  "source_sha256": retained source digest,
  "originals_sha256": exact seven-key digest map,
  "render_policy_baseline": C1 baseline commit
}
```

Each original digest binds the complete canonical content of that original.

The public projection excludes the revision token and its fingerprint. The private authorization target binds the current token separately.

State and deadlines are excluded from the content digest so that content acknowledgment followed by incomplete-Claims acknowledgment can refer to the same unchanged content.

The render-policy baseline is:

`7abc63e12e18a8027de1d4be4c71ad7aa182cb91`

Any later content-affecting rendering-policy change requires applicable specification/review reconciliation.

### 6.3 Proposed limits

These limits are C2 candidate policy, not assertions about existing C1 limits:

| Limit | Proposed value |
|---|---|
| Complete canonical projection payload | 8 MiB |
| Single UTF-8 string | 1 MiB |
| JSON nesting depth | 64 |
| Nodes per projection, including member entries | 100,000 |
| Concurrent projection constructions | 2 |
| Host-owned aggregate projection payload budget | 32 MiB |
| Host-owned aggregate projection node budget | 250,000 |
| Live C2 sessions | 4 |
| Retained complete projections per session | 1 current snapshot |

Implementation MUST count incrementally and reject before allocating an oversized immutable copy. It must not serialize an unbounded payload merely to discover its size.

Construction reservations count against the aggregate budgets. Admission may reject on resource pressure; it must not evict an active review and silently continue with partial content.

Limit failure returns a typed projection error and issues no challenge. There is no truncation, pagination-based partial approval or automatic limit increase.

These bounds control additional C2 projection allocations. They do not claim a hard process-RAM limit for existing C1 originals, Python object overhead or downstream renderer allocations.

Old projections and challenge history are not retained indefinitely. Releasing references permits ordinary memory reclamation; it is not secure erasure.

## 7. Review protocol and cross-session protection

### 7.1 Trusted presentation and challenge issuance

The trusted host:

1. Resolves the live operator and session.
2. Obtains a complete current projection.
3. Presents the content and limitations.
4. Records a display reference bound to its digest and revision.
5. Observes an explicit affirmative operator action.
6. Issues a one-time challenge.

A challenge-ledger entry binds:

```text
host epoch
coordinator instance
session reference
operator binding
owner scope
custody ID
document ID
revision
current revision-token fingerprint
review snapshot digest
actor
exact decision
display reference
issuance and expiry times
attempt state
```

Challenge lifetime is the earlier of five minutes and current C1 expiry.

A test simulation must be explicitly classified as synthetic test authority. It must never be reported as production Human authorization.

### 7.2 Dispatch and C1 enforcement

Before dispatch, C2 checks the complete binding and changes the challenge from `ISSUED` to `ATTEMPTED` under the ledger lock.

The C1 `context` is an opaque reference to that attempt. It is not caller-authored approval content.

Inside the actual C1 record lock:

1. C1 runs its existing owner/token/originals/state checks.
2. The existing three-argument callback checks actor, decision and the affirmative trusted-host attempt.
3. In bound-review mode, C1 creates `C1ReviewTarget` from the **actual record**.
4. The bound guard compares every target field with the challenge ledger.
5. The guard atomically consumes the matching attempted challenge.
6. C1 rechecks expiry before recording the acknowledgment.

Both callbacks must return the literal boolean `True`.

Any mismatch, callback exception, missing guard or absent attempt fails closed using the existing decision-appropriate C1 denial.

The guard receives no caller-supplied substitute for actual custody, owner, revision or digest.

### 7.3 Why custody A cannot authorize custody B

Even if the three-argument callback accepts A’s actor/context/decision, C1’s bound guard receives B’s actual custody ID, owner, token fingerprint and content digest when B is being acknowledged.

Those fields cannot match A’s ledger entry.

This also rejects substitution between two sessions belonging to the same operator.

The same comparison covers another coordinator instance, another host epoch and another revision.

A process-local “currently reviewing A” variable alone is insufficient and is not the enforcement mechanism.

### 7.4 One-time and uncertain outcomes

Challenge states are:

```text
ISSUED → ATTEMPTED → CONSUMED
                  ↘ BURNED
ISSUED → EXPIRED / CANCELLED
```

Once an acknowledgment attempt begins, the challenge never returns to `ISSUED`.

If the bound guard accepts it, it becomes `CONSUMED` before acknowledgment publication.

If dispatch is rejected or interrupted before consumption, C2 burns the attempted challenge in `finally`.

If C1 records the transition but the receipt is lost, the challenge remains consumed. C2 must not replay it.

For an outcome that cannot be reconciled safely, C2 suspends access and attempts abort. It does not adopt an arbitrary observed state as proof that this operator’s action succeeded.

A known denial that leaves a valid session may be followed by fresh presentation and a new explicit action. It cannot trigger an automatic authorization retry.

### 7.5 Separate incomplete-Claims decision

When content acknowledgment yields `CLAIMS_REVIEW_REQUIRED`, the host must separately present incomplete Claims and issue a new challenge for:

`CLAIMS_INCOMPLETE_ACKNOWLEDGED`

The adapter requires `acknowledge is True`.

The first challenge cannot authorize the second decision, and neither acknowledgment supplies legal approval.


### 7.6 Inert local review presenter — R4-F02 / recovery F08

**PR-01: selected medium and authority.** The pilot uses a fixed local UTF-8 plain-text presenter with a trusted output sink and a separate trusted operator-input channel. It is not a browser, rich IDE preview, Markdown/HTML interpreter, agent or shell. All strings from all seven originals are untrusted data, including metadata, keys, locators, source units, Abstract, Claims, warnings, missing information, questions and references. Approved fixture identity does not authorize embedded instructions.

```python
@dataclass(frozen=True, slots=True)
class ReviewPresentationReceipt:
    display: ReviewDisplayRef
    custody_id: str
    revision: int
    review_snapshot_sha256: str
    presentation_policy: Literal["C2_PLAINTEXT_ESCAPED_V1"]
    safe_transcript_sha256: str
    complete: bool

class InertReviewPresenter(Protocol):
    def present(
        self, projection: C1ReviewProjection, *, operator: OperatorRef
    ) -> ReviewPresentationReceipt:
        """Write only inert data to the fixed trusted sink."""
        ...
```

**PR-02: reversible escaping.** Trusted layout identifies original name/digest, JSON path/reference namespace, status and provenance/grounding labels. Source strings are quoted scalar values. Emit ASCII letters, digits, spaces and the conservative punctuation set `.,;!?_-` directly; encode all other source characters as literal ASCII `\uXXXX` (BMP) or `\UXXXXXXXX` (above BMP). Backslash is itself escaped, distinguishing source escape-looking text from encoded controls. Trusted delimiters/layout are emitted separately. Source-derived object keys, identifiers and labels use the same encoding.

The representation preserves the complete original sequence. Its inverse is a pure data decoder for QA, never `eval`, a shell or link opener. Invalid Unicode scalar values are shown as escaped code units; canonical snapshot validity remains governed by the existing validators.

Never emit raw ESC, C0/C1 controls, DEL, ANSI CSI/OSC sequences, carriage-return rewriting, bidi/invisible format controls or terminal hyperlinks from source. HTML, JavaScript, Markdown, backticks, dollar signs, shell metacharacters and URLs remain escaped data. No automatic link opening, source-driven file navigation, shell interpolation or tool dispatch is allowed.

**PR-03: canonical integrity and explicit input.** Presentation is a separate derived stream; it never edits or normalizes seven-original content, Claims, evidence references, original digests or the snapshot digest. Every required/optional field, array element and full reference remains available in order. No silent summarization, truncation or omission is allowed.

Source instructions such as "ignore policy", "approve this" or displayed acknowledgment keywords cannot become operator input, alter admission/runtime policy or issue a challenge. The presenter never calls an LLM/agent to interpret them. The host uses fixed trusted confirmation prompts and explicit input from its distinct operator channel. Review support metadata never becomes filing content.

**PR-04: bounds and receipts.** Encode incrementally using at most a 4 KiB transient output chunk. Bound the total safe transcript, including expansion/layout, at 128 MiB. Do not concatenate an unbounded full transcript. This is separate from the 8 MiB canonical projection bound.

On sink failure, cancellation, expiry or limit violation, issue no complete presentation receipt and no challenge. Partially displayed content cannot establish review authority. Calculate `safe_transcript_sha256` over exact safe UTF-8 display bytes separately from `review_snapshot_sha256`. Before challenge issuance, verify complete receipt, current revision/digest, operator, presentation-policy identity and host display ledger.

The safe display is restricted review content, not a diagnostic log. Logs contain bounded opaque references/results only. Releasing memory is not secure erasure. Supporting another display medium later requires a separately reviewed safe-encoding policy, never automatic reuse as HTML/Markdown.

## 8. State, concurrency and failure behavior

### 8.1 State boundaries

| State | Permitted next actions |
|---|---|
| `REVIEW_PENDING` | Read complete projection, explicitly acknowledge content, revise, abort |
| `CLAIMS_REVIEW_REQUIRED` | Read, separately acknowledge incomplete Claims, revise, abort |
| `REVIEW_RECORDED` | Read, render, revise, abort |
| `RENDERED` / `DOWNLOADED` | Verified download, read, revise, abort |
| Host suspended or terminal | No normal access; reconciliation/cleanup only |
| C1 `ABORTED` / `EXPIRED` | No restoration |

Content review, incomplete-Claims review and render are non-idempotent.

Repeated verified downloads remain permitted by C1.

A repeated abort cannot restore access; an unavailable/terminal reference returns a source-safe unavailable result.

### 8.2 Revision races

C2 serializes operations per session. C1 separately serializes its record.

If revision changes before acknowledgment obtains the C1 record lock, token/revision/binding checks reject the stale action.

If acknowledgment obtains the lock first, it may complete for the current revision. A subsequent successful revision clears that acknowledgment.

A failed local `expected_revision` check must not destroy a newer valid host handle.

An unexpectedly stale internal handle is suspended; C2 does not guess the current token.

### 8.3 Expiry and restart

Preserve C1’s monotonic limits:

- Thirty-minute idle TTL.
- Two-hour absolute lifetime from custody commit.
- Earlier deadline wins.
- Projection/status reads do not refresh TTL.
- Successful state changes follow existing C1 refresh behavior.

Restart creates a new host epoch and loses handles, upload bindings, challenges and C1 volatile custody.

Existing files, manifests, a v1 `PipelineResult` or caller-authored JSON cannot reconstruct authority.

### 8.4 Intake cleanup before custody commit

The host records ownership of its new upload before invoking C1.

For a bound upload whose admission fails before C1 invocation, the host removes its owned bytes and registry entry using existing APP-001 cleanup semantics.

For failures during C1 intake, C1’s existing cleanup remains primary. C2 verifies or retries cleanup for its own bound upload only. It does not assume every C1 preflight failure performed cleanup.

Cleanup occurs after active storage use has ended; cancellation must not delete a file while C1 is using its lease.

If cancellation arrives during intake, C2 marks admission cancelled. If C1 subsequently returns a receipt, C2 aborts it before publishing a session.

A cleanup failure:

- Invalidates the upload lease.
- Prevents further admission.
- Records a bounded sanitized marker.
- Leaves any residual bytes unavailable through C2.
- Does not claim secure deletion.

Registry removal must follow the configured storage removal callback or explicit verified cleanup. Foreign uploads are never cleanup targets.

### 8.5 Fatal render errors

C1 can leave `REVIEW_RECORDED` after `RENDER_INCOMPLETE` when cleanup succeeds. This is verified in the [C1 implementation](https://github.com/nshaokiet/ai-ip-description-generator/blob/7abc63e12e18a8027de1d4be4c71ad7aa182cb91/backend/app/services/preapi_source_custody.py).

C2 adopts a stricter rule:

**A render-execution failure is fatal to that C2 session.**

| Condition | Classification and behavior |
|---|---|
| Missing review detected before render | Nonfatal gate denial; no renderer call |
| Render replay after success | Nonfatal invalid-state denial; valid artifacts remain intact |
| Stale request detected before dispatch | Reject stale request |
| C1 `REVIEW_REQUIRED` / `CLAIMS_REVIEW_REQUIRED` before execution | Gate denial; reconcile state, no automatic retry |
| `RENDER_INCOMPLETE` | Fatal; invalidate C2 handle and attempt C1 abort |
| `CLEANUP_FAILED` during render | Fatal; access remains revoked, report cleanup issue |
| `PROVENANCE_MISMATCH` or manifest integrity failure | Fatal integrity failure |
| `SESSION_UNAVAILABLE` due expiry/revocation | Terminal unavailable |
| Unexpected exception or uncertain render outcome | Fatal/uncertain; suspend, deny exports, attempt abort |

On fatal failure, C2 invalidates handles, challenges, display records and advertised artifacts before cleanup. It then calls existing C1 `abort()` if the current valid capability permits it.

If abort fails or cannot be verified, C2 remains terminal and records a reconciliation blocker. It does not bypass C1 or directly alter `_Record`.

There is no automatic same-session render retry.

Logical revocation, ordinary filesystem cleanup and secure deletion are distinct. Only the first two are in scope.

## 9. Error contract

REVISION-003 additionally proposes `C2SourceAdmissionError` for unapproved, missing-manifest, changed or foreign source admission. This is a C2-only admission error, not an extra C1 code. The verified direct C1 inventory remains 19 unique codes.

Source inspection found **52 direct raises containing 19 unique `CustodyError` codes**.

The three names `RECORD_NOT_FOUND`, `TOKEN_MISMATCH` and `OWNER_MISMATCH` are absent. They must not be represented as current C1 codes.

| Actual C1 code | Deterministic C2 mapping |
|---|---|
| `CUSTODY_DISABLED` | `C2DisabledError` |
| `PROVIDER_BLOCKED` | `C2ProviderPolicyError` |
| `SOURCE_MISSING` | `C2SourceUnavailableError` |
| `CUSTODY_CAPACITY` | `C2CapacityError` |
| `INTAKE_CONFLICT` | `C2IntakeConflictError` |
| `SOURCE_HASH_MISMATCH` | `C2SourceIntegrityError` |
| `EVIDENCE_INVALID` | `C2EvidenceInvalidError` |
| `CLEANUP_FAILED` | `C2CleanupFailedError` |
| `INTAKE_REJECTED` | `C2IntakeRejectedError` |
| `SESSION_UNAVAILABLE` | `C2SessionUnavailableError` |
| `STALE_REVISION` | `C2StaleRevisionError` |
| `PROVENANCE_MISMATCH` | `C2ProvenanceError` |
| `EXPORT_UNAVAILABLE` | `C2ExportUnavailableError` |
| `REVISION_UNCHANGED` | `C2RevisionUnchangedError` |
| `INVALID_REVISION_INPUT` | `C2InvalidRevisionError` |
| `INVALID_STATE` | `C2InvalidStateError` |
| `REVIEW_REQUIRED` | `C2ReviewRequiredError` |
| `CLAIMS_REVIEW_REQUIRED` | `C2ClaimsReviewRequiredError` |
| `RENDER_INCOMPLETE` | `C2RenderFailedError` |

Mapping uses exact code lookup. Unknown codes and unexpected exceptions produce `C2InternalError`, with operation-specific fail-closed handling.

New proposal-level errors are separate from this existing inventory:

| Proposed condition | C2 result |
|---|---|
| Projection size/depth/node limit | `C2ProjectionLimitError` |
| Projection resource reservation unavailable | `C2CapacityError` |
| Forged, stale, replayed or wrong-target challenge | `C2ReviewAuthorizationError` |
| Invalid/foreign/reused upload lease | `C2UploadBindingError` |
| Unknown/unapproved fixture bytes or manifest | `C2SourceAdmissionError` |
| Unapproved/replaced runtime or factory binding | `C2RuntimePolicyError` |
| Unsafe/failed/incomplete presentation | `C2PresentationError` |

The additive projection API may use a separate typed `ReviewProjectionError` for limit/capacity failures. It must not invent an existing `CustodyError` code.

C2 preflight distinguishes incomplete Claims from generic review gating and render replay from missing review. These are C2 classifications, not changes to the verified C1 inventory.

Messages are fixed and source-safe. They contain no raw exceptions, source excerpts, tokens, private paths or ownership-disclosure detail.

## 10. Artifact and privacy contract

Only these existing renderer filenames may be advertised or retrieved:

- `B2_REFERENCE_PREVIEW.pdf`
- `B2_REFERENCE_PREVIEW.docx`
- `USPTO_APPLICATION_DRAFT.pdf`
- `USPTO_APPLICATION_DRAFT.docx`

At render publication C1 verifies the four fixed filenames, expected paths, nonempty files and PDF/DOCX signatures, derives MIME from fixed suffixes and records size/SHA-256. Retrieval revalidates the entire manifest against custody/owner/revision, directory/file containment, size and digest; the baseline does not independently re-parse each file or explicitly recheck manifest MIME on every retrieval. C2 additionally compares every advertised manifest MIME with the fixed filename-to-MIME map and rejects inconsistencies; no new C1 extension is needed for this check.

C2 must not publish partial output metadata or return bytes before C1 validation succeeds.

Review content is classified **restricted synthetic review content**. It stays inside the trusted process and authorized presenter.

Capability tokens and the private challenge ledger are restricted internal authority data. Logs contain bounded opaque references and outcomes only.

The projection’s full retained documents are an explicit review-data scope expansion from the earlier summary-only proposal. It remains subject to Human architecture approval and does not authorize processing confidential research.

## 11. Acceptance and negative-test matrix

All tests below are **proposed and not executed**.

### 11.1 Original twelve scenarios

| ID | Scenario | Required result |
|---|---|---|
| T01 | Synthetic PDF lifecycle | Correct source, complete projection, explicit gates, four verified files |
| T02 | Synthetic DOCX lifecycle | Paragraph/table evidence retained; valid four-file output |
| T03 | Incomplete Claims before second acknowledgment | Render denied; no advertised exports |
| T04 | Separate affirmative Claims acknowledgment | Current bound challenge permits required transition |
| T05 | Negative Claims acknowledgment | Denied without implicit approval |
| T06 | Foreign envelope/analysis substitution | Rejected; caller data cannot establish custody |
| T07 | Wrong operator/owner | Denied without session information leakage |
| T08 | Stale revision token | Rejected; old approvals and artifacts unusable |
| T09 | Idle/absolute expiry | Authority expires; cleanup checked separately |
| T10 | Render replay | Invalid-state denial; existing valid bundle preserved |
| T11 | Partial render and cleanup failure | C2 terminalizes, attempts abort, reports residue accurately |
| T12 | Provider tripwire | No unexpected provider construction or external provider egress |

### 11.2 Required additional integration coverage

| ID | Scenario | Required result |
|---|---|---|
| T13 | Start returns view, later operation uses its reference | Host resolves private handle; token never appears in view |
| T14 | Foreign operator uses valid session reference | Rejected despite correct selector |
| T15 | Successful revision | Atomic handle rotation; old challenges/displays invalid |
| T16 | Revision response uncertain | No invented token or automatic continuation |
| T17 | Same operator substitutes A challenge into B | Rejected by actual C1 bound target |
| T18 | Different owner substitutes challenge | Rejected before acknowledgment |
| T19 | Direct guarded C1 call targets B with A context | Rejected even when three-argument callback returns True |
| T20 | Challenge from another coordinator/host epoch | Rejected |
| T21 | Snapshot changed after display | Rejected; fresh presentation required |
| T22 | Challenge replay | At most one transition |
| T23 | Callback consumes challenge, receipt lost | No reuse; uncertain session denied/reconciled safely |
| T24 | Failure before guard consumes attempted challenge | Challenge burned; cannot retry it |
| T25 | Concurrent revision before review lock | Old challenge rejected |
| T26 | Review wins lock, revision follows | Review applies only to old revision and is then invalidated |
| T27 | Projection immutability | No returned node can mutate C1 originals |
| T28 | Projection/revision race | Entire snapshot belongs to one revision |
| T29 | Complete P2-003 content | Abstract/status, nested subsections, figures, support and review records match retained original |
| T30 | Complete P2-004 content | Families, elements, disclosures, issues, support and questions match retained original |
| T31 | Optional field absent versus null | Distinction preserved |
| T32 | Cross-document reference navigation | Correct namespaces; no fabricated evidence or figure IDs |
| T33 | Projection byte/string/depth/node limits | Fail without partial snapshot or challenge |
| T34 | Concurrent projection resource exhaustion | Bounded admission; no deadlock or uncontrolled cache growth |
| T35 | Foreign/reused upload lease | Rejected before custody; foreign bytes untouched |
| T36 | Precommit failure/cancellation | Owned upload cleanup verified; no published session |
| T37 | Postcommit projection/publication failure | C1 abort attempted; no usable public reference |
| T38 | Abort races with another operation | Terminalization is atomic; no later C2 access |
| T39 | Expiry while projecting or authorizing | No late valid projection/acknowledgment |
| T40 | Missing or altered original/config | Integrity failure; no export |
| T41 | Manifest/file tampering, symlink or traversal | Entire bundle denied |
| T42 | Renderer failure leaves C1 otherwise retryable | C2 explicitly attempts abort and suppresses retry |
| T43 | Process restart | Old references, challenges and custody unavailable |
| T44 | Missing bound guard/permissive legacy callback | C2 cannot record review |
| T45 | Unsupported or absent Claims | No invented Claim IDs or unsupported Claim text |
| T46 | Error mapping | All 19 actual codes and unknown-code fallback covered |
| T47 | Released v1 and route inventory | v1 remains compatible; no new mounted C2 route |
| T48 | Logging and diagnostics | No capability, source-content or private-path leakage |

### 11.3 Synthetic Source Admission tests (REVISION-003)

| ID | Scenario | Required result |
|---|---|---|
| T49 | No fixture manifest or empty approved digest set | Fail closed before APP-001 registration and C1 invocation |
| T50 | Unknown document digest, even with `synthetic=True` flag | `C2SourceAdmissionError`; zero parsing/registry/C1/extraction activity |
| T51 | Forged client-provided SHA-256, name or approval metadata | Host computes actual bytes; deny unless exact approved manifest entry matches |
| T52 | Incorrect size, MIME or malformed binary for known digest claim | Fail closed; no C1 custody |
| T53 | Modified/replaced fixture after approved preflight but before commit | Registered digest and C1 byte-hash checks deny; no review/export |
| T54 | Host manifest SHA mismatch or unapproved manifest update | Fail closed without automatic allowlist expansion |
| T55 | Existing APP-001 public-route document ID without trusted approved binding | Reject; cannot be adopted into C2 from bare document ID |
| T56 | Rejection of foreign registered upload | Do not delete its stored bytes or registry metadata |
| T57 | Independently approved deterministic synthetic PDF fixture | Full positive C2 admission, but only after binary/manifest approval; otherwise BLOCKED_BY_UNAPPROVED_FIXTURE |
| T58 | Independently approved deterministic synthetic DOCX fixture | Same approval condition; no assertion of test PASS without fixture |
| T59 | Zero provider calls across denial and approved admission | Synthetic extraction only; reject live provider fallback |

Tests T01/T02 and T57/T58 must refer to the same specifically approved source-byte manifest, not synthetic analysis JSON or arbitrary runtime-generated PDF/DOCX. Test count measures cases, not execution success. All are NOT RUN at this specification stage.

Acceptance requires these behaviors, not merely a test count.

Execution must use disposable synthetic fixtures, injected monotonic time and provider-disabled configuration. Both live-provider flags remain `0`. Normal provider-tripwire results and intentional blocked probes are reported separately.

Windows tests must avoid mandatory LibreOffice dependency. Symlink cases requiring unavailable privileges must report explicit platform limitations; ordinary path-containment and corruption cases remain mandatory.

No accepted gold, canonical schema, baseline evidence or sealed checkpoint may be changed.

### 11.4 Incorporated binary-identity and REVISION-004 cases

All cases are proposed / NOT RUN. T01–T59 above retain their original row meanings verbatim. T60–T62 are incorporated from the recovered R2/R3 addendum. The companion TEST-MATRIX provides detailed preconditions, inputs, operations, outcomes, invariants, dependencies and execution blockers for all 80 cases.

| ID | Scenario | Required result |
|---|---|---|
| T60 | Same textual content, changed PDF binary | Reject same extracted text with a different binary digest, including incremental metadata, unless those exact bytes are separately approved. |
| T61 | Manifest/fixture confusion from identical basenames | Select the exact configured entry and verify digest/size/MIME; never select by basename, path ordering or text similarity. |
| T62 | No trust from Content Credentials alone | C2PA-labelled metadata cannot replace exact-byte approval; claim no cryptographic C2PA verification. |
| T63 | Forged synthetic runtime marker | Reject forged runtime before its run_extraction spy count becomes nonzero. |
| T64 | Caller-selected unapproved runtime | Reject caller runtime/factory/import/model selection before invoking an unapproved runtime. |
| T65 | Runtime substitution after initialization | Detect accidental instance/type/method replacement before extraction; suspend admission and do not fall back. |
| T66 | Live-provider fallback | Reject fallback configuration before unapproved extraction; local failure never selects a provider. |
| T67 | Unexpected provider/client construction | Tripwire blocks constructor/egress; deny host readiness/custody and report intentional probes separately. |
| T68 | Runtime identity change during custody | Detect before next transition; suspend affected sessions without replacing their runtime or silently reusing review. |
| T69 | ANSI and OSC terminal injection | Emit literal escapes without raw controls, active hyperlinks or title/screen changes. |
| T70 | HTML JavaScript Markdown injection | Display markup as escaped data; no script, rich preview or code execution. |
| T71 | Malicious hyperlinks | No automatic opening, filesystem navigation, tools or network activity. |
| T72 | Embedded shell commands | Display commands as data and dispatch zero subprocesses. |
| T73 | Prompt injection and forged confirmation | Source instructions/confirmation-looking text cannot change policy or become operator input/authorization. |
| T74 | Unicode and control characters | Escape bidi/invisible/C0/C1/DEL/non-BMP text reversibly without source normalization. |
| T75 | Canonical integrity and bounded display | Original/snapshot digests remain unchanged; transcript digest reproducible; display failure/limit prevents challenge. |
| T76 | Malformed PDF object structure | Actual baseline parser rejects marker-only invalid PDF; a matching model digest is insufficient. |
| T77 | Malformed DOCX package | Reject missing required part, invalid main content type or malformed XML; do not assert missing root relationships alone fails. |
| T78 | Wrong MIME | Actual validator rejects extension/MIME/signature mismatch; no registry success or extraction. |
| T79 | Valid filename invalid content | Candidate-like basename cannot bypass actual validation or source approval. |
| T80 | Correct digest of malformed bytes | Identity-model success cannot replace format validation, even under explicitly simulated trust. |

## 12. Findings resolution matrix

“Addressed in candidate” means a proposed specification resolution. Independent closure remains Gemini’s decision.

| Finding/issue | Candidate resolution | Status |
|---|---|---|
| Original F-01: insufficient receipt/projection | Complete immutable seven-document projection | Addressed in candidate |
| Original F-02: incorrect C1 merge status | Exact merge SHA and failed postmerge CI retained | Addressed in candidate |
| Original F-03: APP-001 owner assumption | Trusted new-upload binding; no owner-field claim | Addressed in candidate |
| Original F-04: authorizer underspecified | Explicit presentation, one-time challenge, unchanged callback plus actual-record guard | Addressed in candidate |
| Original F-05: inaccurate error contract | Verified 19-code mapping; nonexistent names rejected | Addressed in candidate |
| Original F-06: replay/lifecycle ambiguity | Non-idempotent review/render; explicit retry and revocation rules | Addressed in candidate |
| Additional: start/handle mismatch | Public session reference resolves host-private handle | Addressed in candidate |
| Additional: cross-session challenge substitution | C1 creates target under record lock; guard compares full binding | Addressed in candidate |
| Additional: omitted review content | Schema-preserving full originals and explicit mapping | Addressed in candidate |
| Additional: bounded projection behavior | Concrete limits, reservations and no truncation | Addressed in candidate |
| Additional: uncertain challenge failure | Attempted challenges consumed or burned permanently | Addressed in candidate |
| Additional: abort/expiry atomicity | Host terminalization and access invalidation before cleanup | Addressed in candidate |
| Additional: precommit cleanup | Owned-upload transaction and cancellation rules | Addressed in candidate |
| Additional: fatal renderer classification | Defined fatal/nonfatal cases and explicit abort policy | Addressed in candidate |
| R3 F-07: Synthetic source admission | Empty approved set, exact-byte gate, actual stored-byte checks, T49–T62 | Addressed in candidate; independent closure PENDING |
| R4-F01 / recovery F07 | Fixed host-owned runtime factory, identity pin, no fallback; section 4.5, T63–T68 | Addressed in candidate; independent closure PENDING |
| R4-F02 / recovery F08 | Inert complete local presentation, separate input and digest preservation; section 7.6, T69–T75 | Addressed in candidate; independent closure PENDING |
| R4-F03 / recovery F09 | Layer A/B/C separation and actual validator nuance; section 15, T76–T80 | Addressed in candidate; independent closure PENDING |

## 13. Change impact and remaining Human decisions

### 13.1 Implementation impact

The proposed C1 changes are additive internal APIs and an opt-in stricter review mode. The projection and guard share one deterministic snapshot-binding definition.

C2 requires new host registries, a trusted exact-byte synthetic fixture manifest/admission gate, upload bindings, presentation/challenge handling, lifecycle orchestration and integration tests. The manifest must be reviewed and approved separately from this design.

No canonical source schema, APP-001 `DocumentRecord`, released v1 API, P2 generation semantics, accepted gold data or renderer output contract needs modification.

Implementation changes to C1 require new applicable independent review and CI. Previous C1 PASS or merge does not approve those additions.

Rollback disables new C2 admission and revokes/expires its sessions through C1’s authorized interfaces. It preserves Git history, source contracts and historical review evidence.

### 13.2 Remaining decisions and gates

| Item | Required disposition |
|---|---|
| Architecture | Human selects Option A |
| Synthetic fixture provenance | Human approves authoritative fixture binaries and immutable manifest/digest before positive C2 admission; default deny while absent |
| Trusted host | Human names/accepts operator, registrar, fixed runtime factory and inert presenter |
| Runtime implementation | Separate authorization/review of exact deterministic runtime and factory before enabling a host |
| C1 extensions | Human authorizes projection and optional bound-review mode |
| Review-data scope and limits | Human accepts complete synthetic-original projection and proposed resource policy |
| Render policy | Human accepts fatal-render C2 revocation |
| Specification | Fresh independent review, then explicit Human approval/freeze of an identified artefact |
| Implementation | Separate scoped authorization |
| CI/quota | Verify recovery and required SUCCESS, or obtain a specific applicable exception |
| C1 closeout | Reconcile outstanding postmerge gate honestly |

These are approval and execution gates. They do not leave an unspecified design alternative inside this candidate.

Production identity, real research data, provider spending, browser transport and Claims activation remain outside the proposal.

## 14. Exact Gemini review instructions

See `PREAPI-C2-REVISION-004-GEMINI-HANDOFF.md` for this finalized candidate's SHA-256 and full review scope. The manifest pins all packaged files except itself and the outer ZIP; those hashes are published separately to avoid circular hashing.

Gemini 3.8 Flash High / Antigravity must use an independent actual session, STRICT READ-ONLY, budget USD 0. Record model/profile/session/reuse, read the entire new candidate/matrices/source evidence and disposition original findings plus R4-F01/F02/F03. Return PASS / CHANGES_REQUIRED / BLOCKED with source/document references. No Gemini verdict is claimed here.

Do not substitute old PR #140 or the REVISION-003 digest. Review of these uncommitted bytes is advisory. A later gate-eligible review requires separately authorized committed final SHA/tree/blob, required CI and Human decisions. No commit/push/PR/Actions/deployment/provider/fixture approval follows from this handoff.


## 15. Verification layers and authority — R4-F03 / recovery F09

Success at one layer never establishes success at another.

| Layer | Scope and authority | What success cannot establish |
|---|---|---|
| A — packet/static/model QA | ZIP metadata/containment/CRC, SHA-256, manifests, document structure, source-reference checks; lightweight format indicators and hypothetical admission models | Actual parser acceptance, fixture approval, C1/C2 enforcement, semantic quality or Gemini verdict |
| B — actual application validators | Existing `DocumentValidator.validate` and PDF strict parsing/text/page/encryption checks; DOCX ZIP limits, required parts, content-type/XML/relationships checks; APP-002 byte/registry/parsing checks where actually exercised | Human fixture approval, complete OOXML compliance, malware freedom, production security or full C2 lifecycle |
| C — C1/C2 integration | Exact-byte admission, storage/registry/source binding, custody/provenance, actual bound review, Claims, revision/TTL, rendering, whole-manifest retrieval and cleanup | Production authentication, legal approval, paid-provider qualification or publication readiness |

Human governance authorizes fixtures and scope. Layer B is authoritative for the actual format checks it executes. The pinned approved manifest plus trusted host govern C2 source permission. C1 remains authoritative for custody/provenance and its lifecycle. Layer A only establishes its stated static/model observation.

**Observed helper limits.** R3 `validate_pdf` can accept marker-looking bytes without a valid PDF object graph. Its `validate_docx` checks a lightweight ZIP/XML skeleton. Its `admission_model` can accept arbitrary bytes if a hypothetical in-memory allowlist names them. R4 reproduces these as expected observations. None is an APP-001 validator or C2 admission implementation.

**Actual validator nuance.** Baseline DOCX validation requires `[Content_Types].xml` and `word/document.xml`, validates the main content type, parses XML, enforces ZIP limits and rejects external relationships where relationship parts exist. It does not explicitly require `_rels/.rels` or certify all OOXML constraints. Missing root relationships alone is not a verified baseline rejection criterion. Use concrete failures such as missing required part, invalid main content type or malformed XML in negative expectations. Stronger validator requirements would need separate scope.

**Admission order and fresh bytes.** First hash bounded candidate bytes and match an already approved immutable manifest entry before APP-001 registration/parsing. Host-owned staging then uses actual APP-001 validation with filename/MIME/size checks; no registry success is published before validation. Immediately before C1, lease and freshly hash the stored bytes, compare actual size/validated MIME, registered identity and approved receipt, then release that preflight lease before C1's existing lease. Host locks prevent its own replacements; C1's rehashes and retained APP-002 envelope remain final authority. A storage lease protects cooperating TTL deletion, not arbitrary external modification.

The typed `verify_registered_source()` contract additionally takes `stored_sha256`, `stored_size_bytes` and `validated_media_type` computed by trusted host code from actual stored bytes. Registered metadata alone is insufficient; caller-supplied digest fields cannot stand in for these observations.

Correct text with another binary digest, incremental updates, C2PA/Content Credentials labels, identical names, `synthetic=True`, a matching digest for malformed bytes or Layer A success cannot bypass source approval and actual validation.

**Execution scope.** Direct Layer B probes may use disposable wholly synthetic malformed bytes solely to call the baseline validator offline, without registration/admission or fixture approval. A deliberately allowlisted malformed-row unit model must be labelled `SIMULATED_TRUST_FOR_NEGATIVE_TEST_ONLY` and cannot populate the operational approved manifest. Full positive C2 tests require separately approved exact binary fixtures plus implemented C1 extensions/C2. No Layer B/C tests were executed in this task.

The recovered manifest remains `approved_fixtures: []`. PDF/DOCX candidates and the incremental PDF variant remain UNAPPROVED. Recorded candidate hashes are historical identity evidence, not admission authority.

## 16. Requirement traceability and readiness

| Requirement | Verified/source authority | Sections / proposed cases |
|---|---|---|
| Option A, default OFF, v1 compatibility | C1 contract, C2 #140/#143, Human recovery prompt | 1–3, 10; T01–T12, T47 |
| Seven originals and custody | C1 commit_upload/_require/_validate_originals; P2-005 | 4–6, 8–10; T06, T40–T41 |
| Complete P2-003/P2-004 review | Actual schemas at C1 merge | 3, 5–6; T27–T34 |
| Operator/upload/session authority | APP-001 ownerless registry; Human requirements | 3–4; T13–T20, T35–T39, T55–T56 |
| Actual-record-bound review | C1 callback limitation; recovered original findings | 2.1, 3.3–3.4, 7; T17–T26, T44 |
| Exact-byte source admission | Full REVISION-003 and R3/R4 addenda | 4.0, 15; T49–T62, T79–T80 |
| Trusted runtime factory | R4-F01 / recovery F07 | 4.5; T63–T68 |
| Inert presenter | R4-F02 / recovery F08 | 7.6; T69–T75 |
| QA qualification | R4-F03; actual APP-001 source | 15; T76–T80 |
| Lifecycle and fatal-render revocation | Actual C1 behavior plus C2 stricter proposal | 7–9; T08–T11, T15–T26, T36–T43 |
| Exact 19-code mapping | 52 direct C1 raises | 9; T46 |

Documentation readiness is separate from Human approval, Gemini review, fixture approval, C1/C2 implementation, integration execution and required hosted CI. Runtime readiness is NOT DETERMINED; publication is NO-GO; API budget USD 0.

### Required format/identity scenarios without duplicate IDs

| Obligation | Planned test |
|---|---|
| Malformed PDF object graph | T76 |
| Malformed DOCX package | T77 |
| Wrong MIME | T78 |
| Valid filename with invalid bytes | T79 |
| Correct digest for malformed bytes | T80 |
| Forged synthetic/approval metadata | T50–T51 |
| Same text with different binary digest | T60 |
| Modified C2PA-bearing PDF | T62 (and T60) |
| Replacement after registration/before custody | T53 |

These mappings preserve the existing test meanings and avoid allocating duplicate cases merely to increase the count.


**Final status: PREAPI-C2 REVISION-004 — SPECIFICATION CANDIDATE READY FOR INDEPENDENT REVIEW. Human approval and Gemini review remain PENDING.**
