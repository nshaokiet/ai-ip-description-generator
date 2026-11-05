# RESUME-FOUNDATION-001 — Tiếp nối và chuẩn hóa nền tảng

Version: 1.0.1. Date: 05/11/2026, Asia/Saigon. Owner: Codex.
Status: DOCUMENTATION CANDIDATE; independent review/required CI PENDING; not completed.
Workflow: V1 / no V2 history asserted. Breaking change: No.
Authorization: Human direct instruction05/11/2026 (source retained privately);
actual SHA-256 recorded in [evidence](../qa/resume-foundation-001-20261105.json).

## Scope và acceptance

Human yêu cầu read/reconcile Git, PR/review/checks/logs, checkpoint và hướng web;
cập nhật tài liệu trên nhánh riêng; chuẩn bị backlog và một task kế tiếp; có thể
push/Draft PR. Không có quyền merge implementation, đóng PR khác, sửa runtime,
dependency/CI/settings, deploy, dùng dữ liệu thật hoặc gọi AI trả phí trong gói này.

| AC | Kết quả cần kiểm chứng / vị trí |
|---|---|
| F01 | Root checkout/dirty files và worktree khác được giữ; nhánh riêng từ actual main; evidence ghi HEAD/tree/remote và worktree liên quan. |
| F02 | [Control Center canonical](../operations/01_PROJECT_CONTROL_CENTER.md#resume-foundation-001-current-baseline) ghi snapshot có ngày, phân biệt main/PR/proposal, PR140–149, exact heads/checks/reviews/blockers và bước resume. |
| F03 | [Decision hướng web](../decisions/RESUME-FOUNDATION-001-web-direction.md) ghi Human direction và supersession; không tự approve auth/implementation. |
| F04 | [B v0.2.0](PRODUCT-001B-trusted-local-review-presenter.md) có server/browser boundary, fixture PDF/DOCX khác nhau, bốn file đúng contract, failure matrix; bản terminal v0.1.0 giữ nguyên. |
| F05 | Backlog bên dưới và [một task kế tiếp](DEP-001-SR-20261024-continuation.md) đủ scope/AC/test/review/dependencies; đều ghi đúng mức đề xuất. |
| F06 | README đồng bộ; report A giữ byte-identical privately, chỉ public summary/correction riêng; không ghi reviewer PASS/CI SUCCESS mới. |
| F07 | Diff/links/governance checks phù hợp; sau commit cố định mới tạo handoff có base/head/tree, file list, validation và câu hỏi review trong PR body / bản local evidence. |

## Backlog theo dependency — đề xuất, không đăng ký/approve tự động

| Thứ tự / task hiện có hoặc công việc chưa có ID | Vấn đề → kết quả, phạm vi / non-goals | Dependencies, modules dự kiến | AC / validation / review |
|---|---|---|---|
| A1 — DEP-001-SR-20261024, tiếp tục PR147 | Graph frontend hiện vẫn fail full audit; sửa compatible dependency graph, giữ lint adapter; không đổi app/CI/auth | Không cần A/B runtime review; package.json/lock, task/audit evidence; kiểm tra candidate local efa1856 trước khi làm trùng | Full/prod audit0, clean deterministic install/tree, lint-security73, lint/typecheck/build/browser/static/demo và required hosted CI; fresh independent exact-SHA review. [Spec tiếp tục](DEP-001-SR-20261024-continuation.md). |
| A2 — MCP dependency security continuation, ID/registry UNVERIFIED | SDK/Zod và transitive graph còn3HIGH/5MODERATE; nâng compatible trong package MCP riêng; không migrate active DB, không đổi task authority | tools/project-orchestrator-mcp manifest/lock; scope/authorization riêng và quyết định rollout riêng nếu cần | Full/prod audit0 hoặc disposition được Human duyệt riêng; typecheck/build/152 test baseline trên disposable DB; fresh read-only security/quality review và exact-head MCP CI. Chưa chọn phiên bản sửa. |
| A3 — CI-V2-001 / PR144; QA installer là proposed extension riêng | Conflict integration và upload ordering; sửa installer transient503 hữu hạn/fail-closed nếu được duyệt; không giảm mandatory archives/pins/gates | Candidate local41cef282 có sẵn; workflow/tests/task/PCC; extension tests/backend/install_p2_006_qa.sh và focused tests; A1 cần trước full hosted acceptance | Resolve đúng conflict, 25 focused CI checks, YAML/actionlint; transient503 phục hồi, persistent503 dừng trước install, real Ubuntu pinned QA; required artifact tồn tại/hash/content + toàn bộ exact-head CI SUCCESS. Head đổi phải re-review; quota hiện tại không được giả định. |
| A4 — repository protection administration, chưa có task ID | main unprotected/rulesets rỗng; chuẩn bị policy áp dụng checks/reviews mong muốn | Quyết định quản trị riêng, không thuộc foundation; không sửa settings ở đây | Diff settings cụ thể được duyệt; API readback đúng enforcement/check names. Thiếu native protection không miễn AGENTS. |
| B — C1 closeout / PR146 / PRODUCT-001A PR149 | Khép custody/workflow và spec gates đang dở; không tạo runtime song song | A1/A3 cho required CI; đọc receipt146, archive/provenance149; C1 exact-main push CI còn fail | Fresh required CI + đúng-SHA review/provenance/disposition, không mix advisory candidate PASS với Git-SHA PASS; C1 postmerge có evidence; không merge trong foundation. |
| C — PRODUCT-001B web synthetic increment | Người dùng upload/review/edit/validate/export trên browser | A/B được chấp nhận, B spec/auth/fixture approval riêng; Next UI, FastAPI adapter, server registry và A/C1/P2 reuse | AC-W01–W12 tại [B](PRODUCT-001B-trusted-local-review-presenter.md); thực chạy browser với2nguồn tổng hợp khác nội dung PDF/DOCX, parse bốn file/source/hash; security+quality review trên cùng final SHA và required CI. |
| D — PRODUCT-001B follow-up persistence/author answers, ID chưa cấp | Giữ review history, câu trả lời tác giả, recovery/retention theo quyền dữ liệu rõ | Chỉ sau C, storage/auth/data/retention decisions; server repository/storage modules dự kiến, không MCP DB | Restart/recovery và owner isolation, invalidation sau answer/edit, deletion/retention và crash tests; security/data review riêng. Increment C chỉ fail-closed volatile. |
| E — PREAPI-D/E + EVAL-001 PRODUCT_RUNTIME pilot | Offline readiness không thay semantic acceptance; pilot thật có giới hạn | PR141/142 review/CI riêng, provider/model/data/budget/call/token approval; giữ accepted gold/rubric | Tripwire/readiness trước client; bounded live execution và semantic evaluation theo ngưỡng đã duyệt; không đổi gold/rubric để đạt điểm. Hiện AWAITING FUNDING, NOT_DETERMINED. |

STABILIZE-001/WEB-001/WEB-002/PILOT-001 trong báo cáo chỉ là nhãn gói. Không tạo
registry entries hoặc coi chúng APPROVED. Không gộp các dòng trên vào một PR.

## Một task kế tiếp được chọn

**PROPOSED: tiếp tục DEP-001-SR-20261024 tại PR147.** Audit mới cho thấy full audit
vẫn exit1 dù production graph sạch; đây là blocker cụ thể mà lặp CI không sửa
được. Task độc lập với provenance/review PRODUCT-001A. Bước đầu là đọc spec
continuation, đối chiếu actual PR147 và local efa1856/graph để chuẩn bị scope
remediation; không cherry-pick hay sửa dependency trong foundation. Scope extension
phải được duyệt trước thực thi, không suy từ task lịch sử thành approval mới.

Nếu chờ external review, có thể phân tích graph và chuẩn bị patch đề xuất hoặc
review contract B độc lập trong quyền planning hiện có; không sửa code chưa được
duyệt. CI144/custody149 có blockers riêng, không bị tự đóng.

## Evidence và giới hạn

- [Evidence dated snapshot](../qa/resume-foundation-001-20261105.json): actual API
  heads/steps/artifacts, byte/lock hashes, graph audit summaries/path/advisory URLs,
  Render live settings/deploy metadata. Các API read có thời điểm riêng; refresh
  ngay trước action. Snapshot không phải dịch vụ theo dõi live.
- Không tìm thấy `AIIP_Project_Review_Roadmap_20261105.md` trong repository/local
  evidence và attachment directories đã tìm. Dùng snapshot được Human dán như
  historical input; không tuyên bố đã đọc report đó. Các PASS1127/152/55 từ yêu
  cầu không phải fresh tests lượt này và không cộng với hosted1160.
- MCP Project Orchestrator tools không được expose trong tool registry lượt này:
  **BLOCKED BY TOOL CAPABILITY**. Đã đọc documented register-task CLI/schema v4:
  yêu cầu exact GitHub comment authorization_ref và selected active DB; active
  migration/rollout có gate riêng. Chưa xác minh DB/schema/lease hoặc source URL
  đáp ứng registration; không start writer/SQL, không bịa Unknown task/approval.
  Git/PR/Control Center là fallback evidence; MCP registration/state UNVERIFIED.
- Default shell/Node runtime ban đầu lỗi sandbox setup; elevated read commands
  sau đó thành công. Không dùng lỗi cũ để tuyên bố attachment hiện vẫn không đọc được.
- Không chạy lại full backend/MCP/frontend/browser, không live AI, không smoke
  Render endpoint; metadata live không chứng minh app health hay semantic quality.

## Handoff

Task ID: RESUME-FOUNDATION-001
Agent: Codex — documentary implementer, V1
Reviewer: Gemini/Antigravity independent strict read-only; actual session PENDING
Status: DOCUMENTATION CANDIDATE / review, required CI and merge PENDING
Version: 1.0.0
Work completed: Reconciled baseline, PRs, CI causes, audit graphs, Render metadata; web delta and proposed next task
Files affected: Documentation/public technical summaries only; raw report excluded; exact list in fixed-candidate PR handoff
Evidence checked: Actual main/PR140–149, reviews/comments, run jobs/logs/artifacts, code contracts, exact lock graphs, Render services/deploys
Findings: Public/unprotected repo; current audit findings; old quota vs503; reviewer149 provenance incomplete
Decisions: Human web direction recorded; existing gates retained; no task auto-approval
Issues: Review/CI/security and C1 closeout pending; MCP unavailable; browser/product/persistence/provider work not executed
Security impact: No runtime/auth/dependency/CI/settings changes; no secret or research data added
Recommended next action: Review fixed foundation candidate, then separately authorize/continue DEP-001-SR scope; read Control Center first

1.0.0→1.0.1,05/11/2026,Codex: explicit Human public-safe publication disposition;
exclude raw internal report/personal paths/sensitive metadata; preserve full local
originals and exact private candidate history. Public branch starts directly at
main and contains no internal commits. Handoff/PR publishes only safe technical
summary/SHAs/test results/links; inaccessible mandatory sources remain PENDING.
Breaking change: No—documentary redaction, no gate change.
