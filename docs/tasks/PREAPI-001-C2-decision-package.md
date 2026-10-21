# PREAPI-C2 — Human architecture decision package

| Field | Value |
|---|---|
| Version | 0.1.0 — decision candidate |
| Date | 21/10/2026 |
| Task | PREAPI-C2 / parent [Issue #131](https://github.com/nshaokiet/ai-ip-description-generator/issues/131) |
| Evidence | [C1 contract](PREAPI-001-C1-source-custody-contract.md), [C2 Draft #140](https://github.com/nshaokiet/ai-ip-description-generator/pull/140), [C1 merge #139](https://github.com/nshaokiet/ai-ip-description-generator/pull/139) |
| Decision status | **OPEN — Human decision not recorded here** |

## Current boundary

C1 source custody is merged on main at `7abc63e12e18a8027de1d4be4c71ad7aa182cb91`; its postmerge CI #39555439292 failed because GitHub artifact storage remained full. C1 is default-off, process-local and synthetic-only. It does not expose an authenticated browser route or establish a production Human reviewer identity. C2 PR #140 contains a specification Draft only, based on older main `d7516d4322f828c5802ec6d9e5ef5f8dffa5721d`; its CI #39545978861 also failed at artifact upload. C1 completion and C2 freeze cannot be inferred from those PRs.

The proposed internal adapter takes an APP-001 registered synthetic PDF/DOCX ID, obtains the APP-002 envelope through C1 custody, and carries the same trusted source through P2-002, P2-003, P2-004, P2-005 and P2-006. A current revision needs explicit content review; incomplete Claims need a second affirmative acknowledgment. Export requires all seven originals and exactly four verified manifest-bound draft files with `filing_ready=false`. Caller-authored envelope, analysis, digest, review decision, package or path cannot establish authority. Released v1 and Candidate A isolation remain unchanged.

## Decision 1 — scope of the next C2 implementation

| Option | Effect | Risk and prerequisite |
|---|---|---|
| A — internal synthetic adapter first (**recommended**) | A default-off, same-process integration and synthetic tests consume C1 custody. A trusted test/operator component supplies owner and review callbacks; no browser UI or new HTTP route. | Demonstrates source-to-four-output integration, but gives no end-user review identity or public product acceptance. Freeze an exact interface, scoped acceptance criteria and rollback before code approval. |
| B — browser review/UI now | Adds authenticated transport, reviewer session and download route. | Requires a separate Human security architecture: user/tenant identity, authorization, capability non-exposure, CSRF/session lifecycle, retention/deletion, threat model and deployment boundary. Do not implement from the C1 test callback alone. |
| C — hold C2 | Keep C1 and existing offline P2 components separate. | Lowest immediate change, but full v2 upload-to-export integration remains untested. |

Recommendation A is limited to offline synthetic proof. If Human selects B, record its separate security/data decisions and compatibility plan before any frontend/API implementation. Neither option changes funded provider, real-paper, production Claims or deployment permissions.

## Decision 2 — trusted actor and review authority

For A, name the exact internal component that creates owner context and invokes the review callback. Treat its identity as process-local test/operator authority, not a browser login or production Human identity. Define how the actor and current immutable revision are recorded without accepting caller-authored JSON as approval. For B, separately approve authentication, per-session ownership, browser transport and audit/retention policy. The current C1 token is a revision capability inside the process, not authentication.

## Proposed acceptance and rollback for Option A

- Positive synthetic PDF and DOCX: fresh source digest, canonical retained envelope, current owner/revision, seven original digests, explicit content acknowledgment, separate incomplete-Claims acknowledgment where applicable, exactly four fixed PDF/DOCX outputs and verified whole manifest.
- Negative integration cases: forged/foreign source and evidence, stale revision or wrong owner, absent acknowledgment, altered config/original, missing one of seven inputs, path traversal/symlink, manifest corruption, interrupted render and cleanup failure. Verify zero advertised artifacts on each denial and no leaked raw source/path/secret.
- The PREAPI-B tripwire must block SDK client construction and non-loopback egress in the test process. Record normal-flow unexpected attempts separately from intentional blocked probes. Existing v1 regression remains unchanged.
- Rollback disables the default-off adapter and revokes or expires process-local sessions; it must not rewrite C1 custody, accepted EVAL gold or released v1 output. Process restart recovery is not promised.

## Human decision record to complete

- Selected scope: **[CẦN XÁC NHẬN]** A / B / C.
- Trusted owner/reviewer component and authority: **[CẦN XÁC NHẬN]**.
- Exact frozen C2 specification SHA/version and implementation acceptance criteria: **[CẦN XÁC NHẬN]**.
- If browser transport is selected, security/data/retention/rollback decision: **[CẦN XÁC NHẬN]**.
- Merge authorization: **[CẦN XÁC NHẬN]** after independent exact-head review and required CI SUCCESS.

This package records alternatives and a recommendation. It is not an approval, frozen specification, implementation acceptance, CI waiver or permission to merge #140.
