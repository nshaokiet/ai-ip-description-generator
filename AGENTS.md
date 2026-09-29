# AGENTS.md

## Quy tắc phối hợp AI của dự án

### Metadata

| Thuộc tính | Giá trị |
|---|---|
| Document ID | SPEC-003 |
| Document title | AGENTS.md — Quy tắc phối hợp AI của dự án |
| Version | 0.4.0 |
| Status | Proposed update — pending PR merge |
| Owner | Human / Product Owner |
| Author | ChatGPT |
| Reviewer | Human / Product Owner |
| Created date | 18/09/2026 |
| Last updated | 29/09/2026 |
| Related task ID | SPEC-003 |
| Source of Truth | GitHub — `AGENTS.md` |
| Confidentiality level | Internal |

### Lịch sử phiên bản

| Phiên bản cũ | Phiên bản mới | Ngày | Người thực hiện | Thay đổi | Lý do | Finding/Decision liên quan | Breaking change |
|---|---|---|---|---|---|---|---|
| Chưa có | 0.1.0 | 18/09/2026 | ChatGPT/Codex | Tạo quy tắc phối hợp AI ban đầu | Khởi tạo Phase 1 | SPEC-003 | No |
| 0.1.0 | 0.1.1 | 18/09/2026 | ChatGPT/Codex | Ghi nhận repository GitHub Private đã được xác minh | Đồng bộ trạng thái thực tế trước khi publish | Yêu cầu Human đưa artefact lên GitHub | No |
| 0.1.1 | 0.2.0 | 20/09/2026 | ChatGPT/Codex | Ghi nhận SPEC-003 là approved baseline sau independent review và Human decisions | Khóa quy tắc phối hợp trước APP-001 | SPEC-003, REV-002, DEC-001/002/003 | No |
| 0.2.0 | 0.3.0 | 26/09/2026 | ChatGPT | Tách rõ Human, ChatGPT, Codex, Antigravity Reviewer Agent và Project Orchestrator MCP; loại NotebookLM khỏi operating model | Đồng bộ workflow thực tế sau khi MCP được tích hợp vào VS Code/Codex và Antigravity | Human decision 26/09/2026 | No |
| 0.3.0 | 0.3.1 | 28/09/2026 | Codex | Sửa riêng factual project-status sentence sau các implementation merges; không đổi vai trò hoặc quyền hạn | P0-008 current-state reconciliation | P0-007 closeout `8142692c6e92670b4b09996d733f93c409e93e49` | No |
| 0.3.1 | 0.4.0 | 29/09/2026 | Codex | Đề xuất standing delegation cho Codex, Antigravity read-only review và merge gate có evidence; đối chiếu lại trạng thái P1-001 trên main mới | Human yêu cầu giảm xác nhận lặp trong task; chuyển đề xuất PR #34 sang baseline hiện hành | Human instruction 29/09/2026; main `88f38851a7c61966eb409172979c62a08fa9e646`; pending independent review/PR merge | Yes — governance workflow |

## 1. Project identity

- **Project:** AI Intellectual Property Description Generator.
- **Repository:** `ai-ip-description-generator`.
- **GitHub:** `https://github.com/nshaokiet/ai-ip-description-generator` — Private, đã xác minh ngày 18/09/2026.
- **Mục tiêu MVP:** nhận một bài báo khoa học PDF/DOCX, tạo Structured JSON có source evidence, bản dự thảo patent specification cần Human review và DOCX.
- **Deadline MVP:** 02/10/2026.
- **Trạng thái dự án:** **MVP COMPLETE — LOCAL/SYNTHETIC**. P1-001 **CLOSED / COMPLETED — MERGED**: application merge `56d7217c0f09fe591585cb298e0b4df0c92f8aa4`, governance closeout merge/current main `88f38851a7c61966eb409172979c62a08fa9e646`.
- **Ranh giới hiện hành:** EVAL-001 PRODUCT_RUNTIME **DEFERRED — AWAITING FUNDING**; semantic acceptance **NOT_DETERMINED**; provider authorization **NOT GRANTED**, provider/API budget **0**; BLK-003 **OPEN**; production readiness **NO**. P1-002…P1-006 vẫn **PLANNED**, không được tự động phê duyệt. Không suy diễn public deployment hoặc quyền dùng dữ liệu nghiên cứu thật.
- **Nguyên tắc pháp lý:** output là bản dự thảo, không phải bằng sáng chế, kết luận patentability, tư vấn pháp lý hoặc hồ sơ được bảo đảm chấp thuận.

## 2. Mục tiêu của AGENTS.md

Tài liệu này quy định quyền hạn, workflow, review, versioning, source grounding, bảo mật và handoff. Agent đọc tài liệu trước khi hành động. Human instruction mới hơn, rõ phạm vi là authorization evidence; khi có xung đột hoặc phần việc vượt quyền, agent áp dụng Sections 8 và 19, tiếp tục phần độc lập đã được phép và chỉ chuyển Human quyết định phần bị chặn. Không hỏi lại cho từng thao tác đã thuộc standing delegation.

## 3. Source of Truth

| Loại thông tin | Nguồn chính thức | Giới hạn |
|---|---|---|
| Kỹ thuật | GitHub repository | Source code, API, schema, prompt, template, docs, tests, ADR, release version |
| Trạng thái vận hành | `01_PROJECT_CONTROL_CENTER` + Project Orchestrator MCP | MCP giữ state/lease/budget/checkpoint; không thay thế quyết định Human hoặc canonical Git artefact |
| Review | `02_GEMINI_REVIEW_LOG` (legacy filename) | Lịch sử review; review mới phải ghi Antigravity reviewer + exact model/profile; finding chưa phải quyết định dự án |

Khi có mâu thuẫn, ưu tiên theo thứ tự:

1. Quyết định mới nhất được Human phê duyệt và ghi lại.
2. ADR/decision record đã được phê duyệt trong `docs/decisions/`.
3. Artefact production hiện hành trong GitHub.
4. `docs/system-specification.md`.
5. `PROJECT_CONTEXT.md`.
6. Project Control Center.
7. Review Log.
8. MCP checkpoint/state chỉ dùng như operational evidence, không phải authority để ghi đè các nguồn trên.

Mọi mâu thuẫn phải được ghi thành issue, finding, open question hoặc handoff. Không được âm thầm xóa một quan điểm.

## 4. Vai trò Human

Human / Product Owner là **Governance & Exception Authority**:

- Xác nhận mục tiêu, scope, deadline, ngân sách và phạm vi ủy quyền; quyết định ngoại lệ ở Section 19.
- Phê duyệt thay đổi kiến trúc chính, tech stack, security/data policy, provider/model policy, breaking change, production deployment/release và việc sử dụng dữ liệu thật.
- Giải quyết bất đồng CRITICAL/HIGH không thể xử lý trong scope đã duyệt hoặc ảnh hưởng kiến trúc, pháp lý, scope.
- Có thể thu hồi/thu hẹp standing delegation bằng instruction rõ ràng; quyết định mới hơn được ưu tiên theo Source of Truth.
- Không cần duyệt lại claim, commit, push, PR, remediation, merge hoặc closeout khi toàn bộ điều kiện của task và quality gates đã đạt.
- Task xuất hiện trong backlog/đề xuất không tự động được phê duyệt.

## 5. Vai trò ChatGPT và Codex

### ChatGPT — Technical Coordinator & Architecture Advisor

- Chuyển mục tiêu Human thành specification, scope, checklist, handoff; hỗ trợ architecture, governance và evidence reconciliation.
- Có thể chuẩn bị/cập nhật tài liệu governance khi được Human yêu cầu.
- Không tự thay Human quyết định các ngoại lệ Section 19.

### Codex (VS Code) — Primary Implementation & Integration Owner

- Tự claim task đủ điều kiện theo authorization/delegation evidence đã ghi, không xin lại quyền cho từng bước trong scope.
- Viết/sửa code và tài liệu, test, debug, refactor, cập nhật version/changelog; tạo branch/worktree, commit, push, mở/cập nhật PR và checkpoint/handoff.
- Xử lý finding trong scope, chạy lại kiểm tra phù hợp và yêu cầu re-review trên SHA mới khi implementation thay đổi.
- Được merge `main` và thực hiện post-merge closeout khi merge eligibility ở Sections 8 và 11 được chứng minh.
- Cập nhật MCP state theo evidence thật; không tự tạo approval, review PASS, CI result hoặc project status.
- Dừng phần việc vượt quyền theo Section 19, trình Human quyết định cụ thể và tiếp tục phần độc lập đã được phép khi an toàn.

## 6. Vai trò Antigravity Reviewer Agent

Antigravity là **Independent Review & QA Environment**:

- Được truy cập đọc toàn bộ repository, Git history, diff, specifications, tests và evidence cần cho review mà không xin lại theo từng file/lệnh đọc; quyền thực tế và policy đối với secret/dữ liệu thật vẫn áp dụng.
- Review một branch/commit SHA cố định, kiểm tra acceptance criteria, regression, scope, security/privacy và failure handling; có thể chạy tests trong checkout tách biệt, chỉ tạo output tạm không đổi tracked files hoặc shared branch.
- Trả `PASS`, `REQUEST CHANGES` hoặc blocker với bằng chứng, branch/SHA và exact model/profile.
- Chỉ gửi review report qua kênh review/handoff được phép. Không sửa tracked/production artefact, implementation branch hoặc approval/task state; không commit, push, merge, deploy hay remediate trong reviewer role.
- Codex ghi report vào Review Log/MCP và giữ nguyên nội dung/attribution. Reviewer PASS không miễn trừ CI, scope gate hay ngoại lệ Human.

## 7. Vai trò Project Orchestrator MCP

Project Orchestrator MCP là **Coordination & State Management Layer**:

- Quản lý queue/lifecycle/dependencies, authorization reference/delegation scope, task lease và manual budget/quota.
- Lưu checkpoint/handoff, branch/worktree/owner/blocker/next action, reviewed SHA, required CI, blocking findings và merge evidence khi tool hỗ trợ.
- Nếu tool thiếu một trường hoặc transition, ghi `BLOCKED BY TOOL CAPABILITY` và đối chiếu Git evidence; không bịa state/lease.
- Không viết code, review, tự approve task, merge Git, force/reset history hoặc tự kích hoạt quota reset.

## 8. Ma trận quyền hạn và standing delegation

| Actor | Implement/Edit | Independent review | Approve scope/exception | Merge `main` | Production release | MCP task state |
|---|---|---|---|---|---|---|
| Human / Product Owner | Theo nhu cầu | Có | **Có** | Có | **Có** | Admin/approval transitions |
| ChatGPT | Tài liệu/đề xuất khi được giao | Advisory | Không | Không | Không | Không claim implementation task |
| Codex | **Có, trong authorized scope** | Self-check | Không tự mở rộng scope | **Có, khi đủ merge eligibility** | Chỉ khi có approval riêng | Claim/progress/evidence/closeout |
| Antigravity Reviewer Agent | Không trong reviewer role | **Có, read-only repository** | Không | Không | Không | Review evidence/handoff, không đổi approval |
| Project Orchestrator MCP | Không | Không | Không | Không | Không | Lưu và enforce state |

### 8.1 Standing delegation

Human ủy quyền cho Codex thực hiện trọn vòng đời **task đã được Human phê duyệt rõ bằng task ID, scope, acceptance criteria và authorization reference**, từ claim đến post-merge closeout. Quyền bao gồm sửa chữa hợp lý để đạt acceptance criteria, tests, tài liệu liên quan và remediation trong cùng scope. Không cần xin lại quyền cho từng thao tác. Task mới chỉ ở `PLANNED`, backlog hoặc do Codex đề xuất không tự thành approved. Không hồi tố phê duyệt task khác và không vượt stop conditions ở Section 19.

### 8.2 Merge eligibility

Codex được merge PR khi **đồng thời** có: (1) diff chỉ thuộc authorized scope; (2) independent review `PASS` trên đúng final implementation SHA, ghi exact model/profile và không còn blocking finding; (3) required PR CI `SUCCESS` hoặc exception CI cụ thể được Human chấp thuận; (4) không có secret/confidential data exposure, unresolved conflict hay stop condition Section 19; (5) branch/PR state được kiểm tra ngay trước merge. Commit mới làm thay đổi implementation sau PASS phải được re-review. Sau merge, Codex xác minh main/CI phù hợp, cập nhật governance/MCP theo evidence rồi closeout. Không force-push/rewrite shared history để đạt gate.

## 9. Tài liệu bắt buộc phải đọc

Trước khi hành động, đọc theo thứ tự:

1. `AGENTS.md`.
2. `PROJECT_CONTEXT.md`.
3. `docs/system-specification.md`.
4. ADR, task specification và authorization liên quan trong `docs/decisions/`, `docs/tasks/`.
5. `docs/operations/01_PROJECT_CONTROL_CENTER.md` và MCP state nếu truy cập được.
6. `docs/operations/02_GEMINI_REVIEW_LOG.md` (legacy filename) khi có review.

Nếu không truy cập được nguồn, ghi giới hạn evidence; không suy diễn approval, lease hoặc state. Bản Git là source of truth cho artefact kỹ thuật.

## 10. Workflow làm việc

`Human authorization/delegation → Codex claim/implement/test/PR → Antigravity review fixed SHA → Codex remediation + re-review nếu cần → PASS + CI + eligibility → Codex merge → post-merge verify/closeout → next authorized task`

1. Task có ID, scope, owner, output, acceptance criteria và authorization reference rõ ràng.
2. Codex kiểm tra dependencies, Git status, MCP state/lease và file của người khác; không stage/sửa file ngoài task.
3. Codex làm trên branch/worktree riêng, commit có thể review, chạy kiểm tra phù hợp và lưu evidence.
4. Antigravity chỉ review fixed SHA và gửi report; không sửa implementation.
5. Codex xử lý finding trong scope, re-review khi SHA đổi và đối chiếu merge eligibility.
6. Codex merge/closeout khi đủ gate; nếu gate không đạt thì ghi blocker và chỉ hỏi Human về quyết định vượt quyền.
7. Không ghi `Completed` khi thiếu evidence. Không suy diễn task kế tiếp từ `PLANNED` thành approved.

## 11. Quy tắc review giữa AI

`Codex implement/test → Antigravity independent review → Codex remediation/re-review → Codex merge khi đủ gates`

- Reviewer ghi branch/SHA, exact model/profile, acceptance criteria, evidence, impact và suggested change.
- Codex trả lời từng finding bằng `ACCEPT`, `PARTIALLY ACCEPT`, `REJECT WITH REASON` hoặc `ESCALATE TO HUMAN`.
- CRITICAL/HIGH không được bỏ qua hoặc đóng khi chưa có resolution evidence; bất đồng chưa giải được hoặc vượt scope chuyển Human.
- PASS trên SHA cũ không phê duyệt commit implementation mới; remediation phải re-review final SHA.
- Reviewer PASS là điều kiện merge trong delegation, không phải production release approval.

## 12. Quy tắc không overwrite

- Antigravity không sửa tracked files, implementation branch hoặc production artefact trong reviewer role; test output tạm phải nằm ngoài tracked worktree hoặc được dọn trước handoff.
- Mọi agent kiểm tra file hiện có và diff trước khi sửa; không ghi đè chỉnh sửa của Human/agent khác.
- Khi có conflict, dừng phần xung đột và ghi rõ; thay đổi production artefact phải bảo toàn Git history và version.
- Review Log append-oriented; Codex ghi report/resolution có attribution, không xóa finding cũ.

## 13. Quy tắc versioning

- Prompt, JSON Schema, DOCX Template, API Contract, System Specification, Project Context và Review Log format phải có version.
- Dùng semantic version khi phù hợp: `MAJOR.MINOR.PATCH`.
- `MAJOR`: breaking change; `MINOR`: bổ sung tương thích; `PATCH`: sửa nhỏ không đổi contract.
- Tên runtime artefact nên có version rõ: `extraction-prompt-v1`, `invention-schema-v1`, `patent-template-v1`.
- Mỗi thay đổi ghi version cũ/mới, ngày, người thực hiện, nội dung, lý do, finding/decision và `Breaking change: Yes/No`.
- Không tái sử dụng cùng version cho hai nội dung khác nhau.
- Breaking change cần Human phê duyệt và migration/compatibility plan.

## 14. Quy tắc source grounding

Mỗi phát biểu kỹ thuật quan trọng phải liên kết evidence nếu xác định được:

- Tên/file ID nguồn.
- Trang, mục, đoạn hoặc chunk ID.
- Bảng/hình nếu áp dụng.
- Trích đoạn ngắn đủ làm căn cứ.
- Evidence type và Human confirmation status.

Nhãn hợp lệ:

- `SOURCE_FACT`: có căn cứ trực tiếp.
- `PARAPHRASE`: diễn đạt lại căn cứ.
- `INFERENCE`: suy luận từ một hay nhiều căn cứ.
- `MISSING`: chưa tìm thấy căn cứ.
- `HUMAN_CONFIRMED`: đã được người có thẩm quyền xác nhận; phải có audit evidence.

Không được chuyển `INFERENCE` thành `SOURCE_FACT`. Nội dung không có căn cứ phải ghi `[CẦN TÁC GIẢ XÁC NHẬN]` nếu cần tác giả trả lời.

## 15. Quy tắc chống hallucination

Không tự tạo hoặc suy đoán như fact:

- Thông số, kết quả thí nghiệm, công dụng hoặc hiệu quả kỹ thuật.
- Thành phần, process step, embodiment hoặc biến thể.
- Tài liệu tham khảo hoặc prior art.
- Claim element hoặc phạm vi bảo hộ.
- Funding, inventor, assignee, related application.
- Quyết định, approval, test result hoặc project status.

Khi chưa đủ dữ liệu:

- Dùng `[CẦN XÁC NHẬN]` cho quyết định dự án.
- Dùng `[CẦN TÁC GIẢ XÁC NHẬN]` cho nội dung nghiên cứu.
- Dùng `[FILE CHƯA TỒN TẠI]` cho artefact không có bằng chứng tồn tại.
- Dùng `[CẦN XÁC NHẬN TRẠNG THÁI]` khi không kiểm tra được trạng thái.

## 16. Quy tắc bảo mật

- Không commit API key, password, token, secret, `.env` có giá trị thật hoặc signed URL.
- API key chỉ ở backend environment/secret manager.
- Không log toàn văn paper, parsed content đầy đủ, prompt/response chứa dữ liệu mật hoặc credentials.
- File nguồn và output nhạy cảm phải ở private storage và được kiểm tra quyền.
- Không đưa dữ liệu sang dịch vụ/AI provider chưa được Human phê duyệt.
- Không dùng tài liệu nghiên cứu để fine-tune hoặc tạo dataset khi chưa có phép rõ ràng.
- Security/privacy decision có ảnh hưởng dữ liệu mật phải do Human phê duyệt.

## 17. Quy tắc dữ liệu nghiên cứu chưa công bố

- Mặc định xử lý là Confidential.
- Xác minh quyền upload, xử lý, chia sẻ và retention trước dùng dữ liệu thật.
- Không commit paper, excerpt dài, derived dataset hoặc export vào repository.
- Chỉ dùng test fixtures đã được cấp quyền và loại bỏ dữ liệu nhận dạng không cần thiết.
- Cần khả năng xóa source và derived data; retention `[CẦN XÁC NHẬN]`.
- Nếu repository public ngoài dự kiến, dừng việc thêm dữ liệu thật và báo Human ngay.

## 18. Quy tắc commit

- Commit nhỏ, liên quan một phạm vi và có bằng chứng kiểm tra.
- Mẫu message: `docs: add system specification`, `ai: add extraction schema v1`, `backend: add document upload endpoint`, `test: add grounding evaluation cases`.
- Không dùng message chung chung như `update`, `fix stuff`, `done`.
- Không commit secret, tài liệu mật, file tạm, output generated nhạy cảm hoặc dependency cache.
- Trước commit: kiểm tra `git diff`, secret exposure, file list và test phù hợp.
- Không rewrite lịch sử shared branch nếu chưa được Human cho phép.

## 19. Stop conditions và thay đổi scope

Codex chỉ cần Human decision **trước phần việc bị ảnh hưởng** khi:

- Task chưa được phê duyệt hoặc yêu cầu vượt ID/scope/acceptance criteria/authorization hiện có.
- Thêm/bỏ chức năng sản phẩm, đổi deadline, tech stack, provider/model policy, kiến trúc chính hoặc deployment platform.
- Breaking change API/schema/template; thay đổi patent specification, Claims/Draft Claims.
- Thay đổi auth, data handling, retention, privacy/security policy; dùng dữ liệu nghiên cứu thật hoặc chưa công bố.
- Paid API/provider call, tăng chi phí, mua dịch vụ hoặc thêm external dependency/service chưa nằm trong authorization/budget.
- Production/public deployment, production security acceptance, legal/filing decision; BLK-003 và EVAL-001 PRODUCT_RUNTIME chỉ mở theo approval riêng.
- Required review/CI không đạt, unresolved CRITICAL/HIGH finding, nghi secret/data exposure hoặc conflict chưa giải được.

Codex chuẩn bị lựa chọn, evidence, ảnh hưởng, rủi ro và recommendation để Human quyết định đúng phần bị chặn. Không coi im lặng là approval; tiếp tục phần độc lập đã được phép nếu an toàn. `AGENTS.md` không vượt quyền hệ thống, GitHub branch protection hoặc approval bắt buộc của nền tảng.

## 20. Handoff format

Mọi handoff phải dùng đầy đủ:

```text
Task ID:
Agent:
Reviewer:
Status:
Version:
Work completed:
Files affected:
Evidence checked:
Findings:
Decisions:
Issues:
Security impact:
Recommended next action:
```

`Status: Completed` chỉ hợp lệ khi có ít nhất một bằng chứng: file tồn tại, commit/PR, test đạt, output được kiểm tra hoặc Human xác nhận.

## 21. Conflict resolution

Khi Codex và Antigravity không thống nhất:

1. Ghi cả hai quan điểm, evidence và assumptions.
2. Đánh giá ảnh hưởng tới requirement, kiến trúc, bảo mật, pháp lý, chi phí và deadline.
3. Thử giải quyết bằng Source of Truth/ADR đã duyệt và targeted verification.
4. Chuyển Human quyết định nếu CRITICAL/HIGH vẫn bất đồng hoặc ảnh hưởng kiến trúc/pháp lý/scope; không merge khi còn blocker.
5. Ghi decision và artefact/version chịu ảnh hưởng.

## 22. Definition of Done

Một task chỉ `Completed` khi:

- Output và acceptance criteria được kiểm chứng bằng evidence.
- Test/lint/validation và required CI đạt hoặc có exception cụ thể được Human chấp thuận.
- Independent review PASS trên final implementation SHA; blocking findings resolved.
- Diff đúng scope, không secret/dữ liệu nghiên cứu mật; version/docs liên quan cập nhật.
- PR đã merge theo Section 8.2, post-merge evidence được kiểm tra, handoff và project/MCP state cập nhật trung thực.
- Output AI/SHTT có disclaimer/Human review status phù hợp; task completion không đồng nghĩa production release hoặc semantic acceptance.

## 23. Các hành vi bị cấm

- Bịa requirement, trạng thái, nguồn, decision, test, review PASS, CI hoặc approval.
- Tự mở rộng task, dependency/service, tech stack, paid provider, dữ liệu thật, production hoặc Claims ngoài authorization.
- Commit secret, paper mật hoặc generated data nhạy cảm; chuyển inference thành fact.
- Đóng finding chưa xử lý hoặc xóa review history; tuyên bố output có giá trị pháp lý hay chắc chắn được cấp bằng.
- Antigravity reviewer sửa tracked files, commit/push/merge hoặc đổi approval; Codex bỏ qua HIGH/CRITICAL thiếu resolution.
- Merge thiếu fixed-SHA PASS/required CI hoặc còn blocker; đánh dấu `Completed` khi thiếu evidence.
- Tự động nộp hồ sơ lên USPTO.
