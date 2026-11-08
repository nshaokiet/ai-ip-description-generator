# PREAPI-C2 REVISION-004 — Human architecture approval and specification integration

| Field | Value |
|---|---|
| Version / date / author | 1.0.0 / 24/10/2026 Asia/Saigon / Codex |
| Task / workflow | PREAPI-C2 REVISION-004 — SPECIFICATION-ONLY / V1; no V2 enrollment |
| Authority | Direct Human instruction in this Codex conversation, followed by explicit source/copy instructions |
| Audit reference | HUMAN-PREAPI-C2-REVISION-004-SPECIFICATION-ONLY-2026-10-24 |
| Status | Architecture accepted; specification Git integration candidate; fixed-SHA review and required CI pending |
| Integration base | 53c253be874236c6f38a5333a6f7f3390de9f51e |
| Branch | docs/preapi-c2-revision-004-specification |
| Owner / reviewer | Codex / Gemini 3.8 Flash High, Antigravity STRICT READ-ONLY |

## Actual Human decision

The following is the operative Human message received directly on 24/10/2026.
It is actual session authorization, not a proposed decision template, inferred
approval, or reviewer permission. The audit label above records provenance;
it does not authenticate a person cryptographically.

> **HUMAN ARCHITECTURE DECISION — PREAPI-C2 REVISION-004**
>
> Tôi phê duyệt kiến trúc **Option A — Internal Synthetic Adapter First** dựa trên:
>
> - REVISION-004 SHA-256: `1e2f5376f526e7e3176c8731deb2d49dccf1ef1de7b347643a60d4b011f8ce3f`
> - Gemini 3.8 Flash High technical review: PASS.
> - Review receipt correction ngày 24/10/2026: PASS affirmed.
>
> Phạm vi phê duyệt: kiến trúc C2, synthetic-only, default OFF, C1 additive extensions được đặc tả, và quy trình review bắt buộc.
>
> **Ủy quyền Codex thực hiện gói SPECIFICATION-ONLY:**
>
> 1. Xác minh final review receipt và tạo checksum bên ngoài receipt.
> 2. Tạo task branch riêng.
> 3. Đưa nguyên văn REVISION-004 đã review vào Git.
> 4. Tạo PR specification và lưu bằng chứng governance.
> 5. Yêu cầu Gemini independent review trên fixed Git SHA.
> 6. Chỉ merge khi required CI SUCCESS và tất cả governance gates đạt.
>
> **Chưa ủy quyền triển khai C1/C2 application code.**
>
> **Chưa phê duyệt bất kỳ synthetic fixture nào.**
>
> Không bypass CI, không kích hoạt paid API, không deploy production, không xử lý bài báo nghiên cứu thật.
>
> Tiếp tục tự động các công việc trong phạm vi đã duyệt mà không hỏi lại từng thao tác. Nếu bị chặn bởi GitHub artifact storage, giữ PR mở và ghi nhận blocker; không tự bỏ quality gate.

Later Human instructions supplied the exact specification/ZIP paths, then the
Antigravity receipt path and explicit permission to copy its bytes into the
output directory, verify both hashes and keep its checksum in a separate manifest.
Those instructions reconfirmed candidate immutability and specification-only scope.

## Verified source bytes and review attribution

- [Canonical specification](../tasks/PREAPI-001-C2-synthetic-adapter-contract.md):
  **80,892 bytes**, SHA-256
  `1e2f5376f526e7e3176c8731deb2d49dccf1ef1de7b347643a60d4b011f8ce3f`.
  Copied directly from
  `D:\AIIP-C2-REVISION-004-OUTPUT\PREAPI-C2-REVISION-004-CANDIDATE.md`;
  no reconstruction, text edits, newline normalization or BOM conversion.
- [Final corrected receipt](../review-receipts/PREAPI-C2-REVISION-004-REVIEW-RECEIPT-CORRECTION.md):
  **4,993 bytes**, SHA-256
  `bb0e666ff38fbbd44891e947383a1e90eb2d2df5369827baed796639500d5e80`.
  Original:
  `C:\Users\NguyenSongHaoKiet\.gemini\antigravity-ide\brain\ad05f382-626d-4391-90fa-1b8080cf9759\PREAPI-C2-REVISION-004-REVIEW-RECEIPT-CORRECTION.md`.
  Original, authorized output-directory copy and repository copy must match.
- Original review packet: **668,104 bytes**, measured SHA-256
  `48cc6fd70c9066bc6da9d8081d069b6f22d471fd0caaee4a44856b1cad3b8b16`.
  Preserved at the Human-provided output path; ZIP and unapproved binary fixture
  candidates are not added by this specification integration.
- [Repository checksum manifest](../review-receipts/PREAPI-C2-REVISION-004-SHA256SUMS.txt)
  pins the two committed artifacts using repository-relative paths.
  Output-directory `PREAPI-C2-REVISION-004-FINAL-SHA256SUMS.txt` separately pins
  candidate, receipt and ZIP. Neither manifest hashes itself.
- Receipt reports **Gemini 3.8 Flash High / Antigravity IDE, STRICT READ-ONLY,
  PASS affirmed**, session `ad05f382-626d-4391-90fa-1b8080cf9759`,
  **REUSED YES** across earlier reviews. Its identity and “Cryptographic
  Sign-Off” heading are preserved as source wording; hashes establish byte
  integrity, not authenticated model/Human identity or a digital signature.
- Receipt corrects the review narrative's `SourceCustodyCoordinator` to actual
  `TrustedCustodyCoordinator`. Direct Git source inspection at C1 merge
  `7abc63e12e18a8027de1d4be4c71ad7aa182cb91` confirms the latter.
  Neither class name occurs in the candidate; correction requires no candidate edit.
- The receipt affirms a prior technical review. The prior full report is not
  embedded or claimed independently read here. This is an attributed advisory
  file-digest review, **not** a final Git-SHA PASS or GitHub-native approval.

The candidate's original “PENDING”, “standalone” and “no commit” statements
describe its authoring-time status and are intentionally preserved. This dated
record supplies later Human approval and Git integration provenance. Plain
companion filenames inside the candidate refer to the retained standalone review
packet; they are not claims that all packet members were committed here.
The new fixed-SHA handoff governs the proposed Git review.

## Scope and gates

Architecture approval covers Option A, the specified additive C1 design and
review process. It grants **no executable C1/C2 implementation**, runtime-factory
enablement or fixture approval. Approved C2 fixtures remain **0**; T01–T80 remain
**PROPOSED / NOT RUN**. Source admission remains default-deny; adapter default OFF.
Released v1, Claims/provider configuration, accepted gold, workflows and application
files receive no change. EVAL-001 PRODUCT_RUNTIME remains NOT_DETERMINED;
BLK-003 OPEN; provider budget USD 0; production/publication NO-GO.

Conditional specification merge authority comes from the Human message above.
Before any merge: independent Gemini PASS on the exact final Git SHA with actual
model/profile/session/reuse and no blocking findings; all required exact-head CI
SUCCESS; fresh complete-diff/PR/head/base/mergeability and platform verification;
no scope/security/Section 19 blocker; expected-head-protected ordinary merge.
A changed candidate needs fresh applicable CI/review. Check Render auto-deploy/
previews remain OFF before merge so integration cannot cause an unauthorized deploy.
A platform denial may not be bypassed. Postmerge requires actual ancestry/tree/
main-CI verification and truthful governance/README closeout. No new permission
request is needed for operations already authorized; missing gates block merge.

Historical C1 postmerge #39555439292 and old C2 #39545978861 CI failures are
preserved. Storage recovery is not inferred from elapsed time or artifact cleanup.
The new PR's own exact-head run is authoritative for its CI gate. On a storage
failure, retain OPEN/DRAFT state and record the actual error; do not waive uploads,
modify CI, loop reruns, approve fixtures or claim task completion.

## Operational limits and version history

The initial checkpoint is preserved in
[PR #140 comment 6379436412](https://github.com/nshaokiet/ai-ip-description-generator/pull/140#issuecomment-6379436412).
Windows sandbox startup failed; a platform-approved elevated read restored access
to the specified Windows files without changing sandbox policy. A local HTTPS
fetch could not authenticate; GitHub connector handles remote publication, without
credential access or another interactive login attempt. Work uses a separate
worktree; original checkout and its existing modifications remain untouched.

MCP returned `Unknown task: PREAPI-C2`; lease/state synchronization is
**BLOCKED BY TOOL CAPABILITY**, with no fabricated registration, lease, approval
or completion. Workflow V1 remains the task path.

None → **1.0.0**, 24/10/2026, Codex: record actual Human architecture/spec-only
authority and verified immutable source/review provenance. Breaking change:
**No — documentation only**. The 0.1.0 draft remains in PR #140 history; this
canonical file introduces the distinct reviewed v0.2.0 REVISION-004 bytes without
reusing an old immutable artifact identity.
