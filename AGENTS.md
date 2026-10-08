# AGENTS.md

## Quy tắc phối hợp AI của dự án

### Metadata

| Thuộc tính | Giá trị |
|---|---|
| Document ID | SPEC-003 |
| Document title | AGENTS.md — Quy tắc phối hợp AI của dự án |
| Version | 0.6.1 |
| Status | Proposed conditional Phase G adoption — pending dual review and accepted merge/postmerge verification |
| Owner | Human / Product Owner |
| Author | ChatGPT/Codex |
| Reviewer | Human / Product Owner |
| Created date | 18/09/2026 |
| Last updated | 08/10/2026 |
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
| 0.4.0 | 0.4.1 | 29/09/2026 | ChatGPT | Bắt buộc đồng bộ bảng Project status trong README khi task đổi trạng thái, đặc biệt tại closeout/merge | Human yêu cầu README luôn phản ánh tiến độ task hiện hành | Human instruction 29/09/2026; PR #38 | No |
| 0.4.1 | 0.5.0 | 07/10/2026 | Codex | Conditional V2 selection, four roles, manual/external verification and rollback; retain V1 | Human GOV-AGENT-001-E E-01–E-06; spec v0.2.1; exact base `5d8d4b555b1c11407db4671b9c2af88f4baad8bb` | Independent governance review pending | Yes — workflow governance; pre-1.0 minor follows 0.4.0 convention; no product/API change |
| 0.5.0 | 0.6.0 | 08/10/2026 | Codex | Prospective conditional project adoption; G-01–G-09; retain V1, manual gates and operational limits | HUMAN-GOV-AGENT-001-G-ADOPT-V2-CONDITIONAL-2026-10-08; frozen G spec 0.1.0 | Dual independent fixed-SHA review pending; effective after accepted G merge/postmerge verification | Yes — prospective governance; no product/API change; preserve history and separately reviewed rollback |
| 0.6.0 | 0.6.1 | 08/10/2026 | Codex | Reconcile frozen G spec v0.1.1 and preserved v0.1.0 supersession | Human SEC-001/SEC-002 remediation approval | Supported freeze spec3/provenance8; dual review pending | No — factual references only |

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

Khi handoff/closeout làm thay đổi trạng thái task, Codex phải kiểm tra và đồng bộ bảng `README.md` → `Project status` trong cùng scope trước khi task được coi là hoàn tất.

## 21. Conflict resolution

Khi Codex và Antigravity không thống nhất:

1. Ghi cả hai quan điểm, evidence và assumptions.
2. Đánh giá ảnh hưởng tới requirement, kiến trúc, bảo mật, pháp lý, chi phí và deadline.
3. Thử giải quyết bằng Source of Truth/ADR đã duyệt và targeted verification.
4. Chuyển Human quyết định nếu CRITICAL/HIGH vẫn bất đồng hoặc ảnh hưởng kiến trúc/pháp lý/scope; không merge khi còn blocker.
5. Ghi decision và artefact/version chịu ảnh hưởng.

## 22. Definition of Done

Một task chỉ `Completed` khi:

- Dòng tương ứng trong bảng `README.md` → `Project status` đã được cập nhật theo trạng thái cuối có bằng chứng của task; README chỉ là status summary và không thay thế task record/Project Control Center/Git evidence.

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

## 24. Conditional Workflow V2 governance — GOV-AGENT-001-E

### 24.1 Human decisions and effective activation

Human E-01–E-06 select MANUAL_EXTERNAL authoritative verification,
PROCEDURAL_TRUST_BASED identity, no automatic R0–R4 routing, explicit V2 enrollment,
the reviewed Phase E PR merge commit as activation commit, and evidence-preserving
rollback. The single canonical marker is
[WORKFLOW_V2_ACTIVATION.yaml](docs/operations/WORKFLOW_V2_ACTIVATION.yaml), version
1.0.0; the [manual verification runbook](docs/operations/WORKFLOW_V2_MANUAL_VERIFICATION.md)
preserves the decisions and concrete source-by-source procedure.

Sections 4–23 remain the V1 authority baseline until this reviewed activation merge
is verified on main; afterward they continue governing V1 and Human exception
authority. The marker's enabled=true setting is conditional policy on this branch.

PHASE E BRANCH PRESENT != WORKFLOW V2 ACTIVATED.
PHASE E REVIEW PASS != WORKFLOW V2 ACTIVATED.
PHASE E PR OPEN != WORKFLOW V2 ACTIVATED.

Only the reviewed Phase E PR merge commit on main becomes
WORKFLOW_V2_ACTIVATION_COMMIT after explicit Human approval, independent governance
review PASS on exact final SHA, required CI SUCCESS and satisfied merge gates.
Verify actual merge/main/reviewed ancestry and post-merge CI; record that immutable
merge SHA in durable closeout. The implementation SHA is not the activation commit;
do not embed a future merge's own SHA in its pre-merge tree or amend reviewed history.
Schema/tool/role/skill availability does not activate governance.

This Phase E implementation instruction stops at independent review. It does not
authorize merging this PR, enrollment, automatic routing, Phase F/G or AI-CONV.

### 24.2 Selection and explicit enrollment

Before each proposed admission/action, read current main's marker and accepted
activation record from real sources. Disabled, unmerged, missing or unverifiable
activation means OFF. A later main commit must retain the accepted activation
merge in its ancestry; check any later reviewed disable and Human decision.

```text
IF effective activation is OFF: new/unenrolled tasks use the authorized V1 path.
ELSE IF task is explicitly Human-authorized and V2-enrolled,
        references WORKFLOW_V2_ACTIVATION_COMMIT,
        and required role/spec/evidence state exists for the action: use V2.
ELSE: tasks with no V2 execution history use the authorized V1 path.
Existing V2 history with invalid/disabled prerequisites: BLOCK affected work,
checkpoint and obtain Human disposition; never silently translate it into V1.
```

Historical V1 tasks/evidence remain V1; no automatic migration/backfill. Enrollment
is not task authorization or implementation permission. Missing role/spec/evidence
blocks the proposed action. An authorized Human/operator may use the existing
`npm run admin -- enroll-v2 /absolute/path/to/enrollment.json` only after external
preflight with the exact accepted activation merge SHA. No enrollment is executed
during Phase E. PLANNED eligibility is not permission to execute a task.

### 24.3 Four standing roles and flow

Role defines authority; skill defines procedure; task spec defines requirements.
Use the [agents role/P0 package](agents/README.md); roles remain client/model
independent. No lower layer expands Human governance.

| Role | Responsibility / boundary |
|---|---|
| PLANNER | Plan and author versioned spec; no implementation ownership/lease; cannot self-freeze or independently approve implementation |
| IMPLEMENTER | Own scoped tracked implementation/remediation/lease; self-check is not independent Security/Quality review |
| SECURITY_REVIEWER | Independent/read-only for implementation; Security verdict only; no remediation/commit/push/merge in reviewer role |
| QUALITY_REVIEWER | Independent/read-only for implementation; Quality verdict only; no remediation/commit/push/merge in reviewer role |

Security and Quality have independent identities/sessions and separately authored
verdicts. Neither consumes the other's verdict as proof. Reviewer tracked writes
block independent PASS; all required CI/reviews target the same exact final SHA.

V2 flow: Human task authorization → explicit enrollment → Planner assignment →
versioned spec → Human-authorized freeze → Implementer assignment/lease → scoped
implementation → exact-SHA CI → required independent reviews → external authoritative
verification → merge eligibility → merge → post-merge verify → evidence-backed
closeout/README synchronization. Use the sole persisted same-task current candidate
pointer. Changed implementation/spec requires applicable fresh CI/review; old PASS
remains history. Frozen spec changes require explicit supersession/re-planning.

Automatic R0–R4 routing is NOT ACTIVATED. Risk metadata cannot reduce reviews.
The separately authorized Phase F pilot requires BOTH Security and Quality on the
same final SHA regardless of risk class. Other V2 tasks before Phase G require
explicit Human/task-spec review requirements; unclear policy fails closed.

### 24.4 Manual/external merge eligibility

Section 8.2 standing delegation stays conditional. Immediately before merge, the
integration owner follows the linked runbook: verify actual Human scope/exceptions;
committed frozen spec/version/SHA and Human freeze evidence; real Git final/base/
branch/PR; every actual required CI SUCCESS on final SHA; canonical independent
read-only required-stream PASS reports with exact identities/no blocking findings;
fresh correct repository/OPEN/mergeable PR and exact reviewed head; no newer commit,
conflict, secret/confidential exposure, scope violation or Section 19 stop condition.
Preserve source links, attribution, timestamps and each check's result.

Only all satisfied current governance/platform gates permit delegated normal merge
with expected-head protection. Head/spec movement or missing/failed evidence stops
merge and requires new applicable validation/review. A platform denial cannot be
bypassed through another tool/API/CLI. Post-merge verify actual merge/main/ancestry
and required exact main CI before completion. No force/local-merge/history bypass.

This approved MANUAL_EXTERNAL strategy is outside B3's adapter computation.
`authoritative_merge_eligible=false` remains expected and unchanged while accepted
adapters are unavailable. Do not override/reinterpret it or treat provisional_ready
as permission. A complete recorded checklist is not external source verification.

### 24.5 Identity and MCP limits

Initial identity is PROCEDURAL_TRUST_BASED, not cryptographically authenticated.
agent_id/session/model/profile and Human references do not authenticate authority;
GOV-IDENTITY-001 remains FUTURE/separately authorized. Fabrication remains forbidden.

RECORDED != VERIFIED. provisional_ready != authoritative_merge_eligible.
MCP state != authenticated external truth. model_profile != authenticated identity.
review PASS != CI PASS. CI PASS != review PASS.
review PASS + CI PASS != automatic merge permission.

MCP is operational state, not a verifier of this marker. Its installation-era
NOT ACTIVATED diagnostic does not override verified main's governance record.
Enrollment/activation preflight is procedural; Phase E does not claim automatic
runtime enforcement or modify B1/B2/B3 core behavior.

### 24.6 Disable / rollback

A separately reviewed Human governance change setting the marker enabled=false
on verified main stops NEW V2 enrollment. Preserve all database rows, specs,
assignments, reviews, CI, verifications and Git artifacts. No deletion/reset,
historical backfill or silent V2-to-V1 translation. Checkpoint in-progress V2 work;
Human decides finish-under-V2 or explicit stop/reauthorize/restart-under-V1.
Unenrolled/new tasks use approved V1 if authorized. Keep safe read/checkpoint/
handoff access and immutable activation/disable history; re-enable does not refresh
stale CI/review. Budget/quota, provider/API, confidential-data, product/production
and legal boundaries remain unchanged. Sections 16–19 stop conditions apply.

## 25. Conditional project adoption (Phase G)

The actual Human decision is **ADOPT V2 WITH CONDITIONS — APPROVED** on
2026-10-08, reference
`HUMAN-GOV-AGENT-001-G-ADOPT-V2-CONDITIONAL-2026-10-08`.
Source: attachment `017d9dd4-8e55-4e2f-a49e-f74eb7daaecf/Pasted text.txt`,
SHA-256 `19C98EDB6C1EEAC33374C293BF22DCBCFD288363FDF54329DDEE62EF3B980D60`.
This reference/hash records provenance; it is not authenticated identity or Human
review of a future commit. The [distinct-Planner specification](docs/tasks/GOV-AGENT-001-G_ADOPTION_SPEC.md)
v0.1.1 is FROZEN/spec3 at `7c42db54909506cef5d57739072a58b3dad68943` after supported
ADMIN reconciliation/freeze under the Human-approved SEC-001/SEC-002 supersession.
Provenance8 is RECORDED; v0.1.0/spec2 at
`d92c9ad5ddcb08f7b4af430bbed879c11b8a2b89` remains SUPERSEDED history.

Phase E activation remains `9c291325d409f74bc767f9b870e81d75c9b70802`;
[accepted Phase E closeout](https://github.com/nshaokiet/ai-ip-description-generator/pull/90#issuecomment-6034290739).
Phase F is canonically COMPLETED, pilot acceptance PASS, in its
[verified receipt](https://github.com/nshaokiet/ai-ip-description-generator/pull/91#issuecomment-6051437979).
Phase F operational MCP remains AWAITING_REVIEW; no completion transition is fabricated.
Its AC-12 retains actual A CI staleness, A review staleness not independently
demonstrated, and no fabricated A review.

This branch proposes the approved adoption policy. **Phase G adoption is ACTIVE
only after accepted Phase G merge/postmerge verification**: both required independent
PASS on the same final SHA, required exact-head CI SUCCESS, fresh MANUAL_EXTERNAL,
normal expected-head-protected merge, actual main ancestry/tree/policy verification,
required exact merge push/main CI SUCCESS and canonical closeout/readback.
Branch presence, Human scope approval, static checks, PR OPEN and reviewer PASS
alone do not establish that boundary. Record the actual G adoption merge externally;
it is distinct from the immutable Phase E activation commit and adds no new marker.

| Policy field | Required value |
|---|---|
| Adoption policy | CONDITIONAL |
| Adoption effective boundary | Accepted Phase G merge/postmerge verification |
| Preferred process | V2 for eligible explicitly Human-authorized tasks |
| V2 enrollment | EXPLICIT_ONLY |
| Historical/unenrolled V1 | PRESERVED |
| MANUAL_EXTERNAL | MANDATORY |
| Phase G reviews | Security AND Quality, separate identities and actual Antigravity sessions |
| Automatic R0-R4 | NOT ACTIVATED |
| Identity | PROCEDURAL_TRUST_BASED |
| Accepted verifier adapters | UNAVAILABLE |
| B3 authoritative_merge_eligible | false |
| Evidence | RECORDED != VERIFIED; provisional_ready != authoritative_merge_eligible |
| MCP completion transition | BLOCKED BY TOOL CAPABILITY — disclosed separately |
| Rollback | Preserve evidence; separately reviewed Human disable; in-progress Human disposition |
| Product/provider/production authority | NOT GRANTED |
| Phase H / AI-CONV | NOT STARTED |
| WORKFLOW_V2_ACTIVATION_COMMIT | 9c291325d409f74bc767f9b870e81d75c9b70802 |

| Condition | Required practice |
|---|---|
| G-01 | Each task still needs actual Human authorization, valid registration, approved scope, explicit enrollment with accepted activation, and action-specific roles/frozen spec/evidence. No automatic admission, approval or V1 backfill. |
| G-02 | Before every merge inspect actual Human/freeze/Git/complete diff/required CI/reviews/findings/independence/fresh PR-head-base/platform/scope/confidentiality/stop sources; preserve source-backed evidence. Complete checklists and MCP readiness are not permission. |
| G-03 | When both streams are required, separate reviewer identities AND actual sessions; separately authored read-only reports target the same exact final SHA, no borrowed verdict, no unresolved blocker. G requires both streams regardless of R3 metadata. |
| G-04 | Risk classes remain metadata; no automatic R0-R4 activation or risk-based review shortcut. Future tasks need explicit Human/task-spec review requirements; unclear policy blocks. |
| G-05 | Identity stays procedural/trust-based; hashes and model/session labels are not authentication. GOV-IDENTITY-001 remains FUTURE. |
| G-06 | Accepted authoritative adapters remain unavailable and B3 authoritative eligibility remains false; the separate authorized MANUAL_EXTERNAL path is required. Installation-era MCP/package NOT_ACTIVATED diagnostics are not global activation verifiers. |
| G-07 | Report canonical Git/governance completion separately from actual MCP state. Unsupported operational completion stops that operation; never use raw SQL, V1 transitions or recreated tasks to hide it. Any capability improvement requires separate authorization. |
| G-08 | Reviewed Human disable on verified main stops new admissions, preserves every row/report/checkpoint/Git artefact and requires explicit disposition for in-progress V2; no silent V2-to-V1 translation. Re-enable does not refresh stale evidence. |
| G-09 | This adoption grants no Phase H/AI-CONV, product/Claims/provider/paid runtime/confidential-data/authenticated-identity/adapter/routing/production/legal or budget/quota authority. Existing product contracts and stop conditions remain. |

Sections 4–24, Phase E decisions E-01–E-06 and historical V1 evidence remain.
After accepted G adoption, V2 is the preferred process for eligible future tasks
only through explicit authorization/enrollment; an authorized unenrolled task
continues under V1. Invalid/disabled prerequisites for existing V2 history require
Human disposition, never silent fallback. No migration or automatic enrollment runs.
The governance change is prospective; product/API/schema/template and MCP core stay
compatible. A separately authorized reviewed revert may restore future V1 preference,
preserving V2 history and the existing reviewed-disable procedure in §24.6.
