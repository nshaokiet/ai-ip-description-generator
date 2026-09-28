# AGENTS.md

## Quy tắc phối hợp AI của dự án

### Metadata

| Thuộc tính | Giá trị |
|---|---|
| Document ID | SPEC-003 |
| Document title | AGENTS.md — Quy tắc phối hợp AI của dự án |
| Version | 0.3.1 |
| Status | Approved baseline |
| Owner | Human / Product Owner |
| Author | ChatGPT |
| Reviewer | Human / Product Owner |
| Created date | 18/09/2026 |
| Last updated | 28/09/2026 |
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

## 1. Project identity

- **Project:** AI Intellectual Property Description Generator.
- **Repository:** `ai-ip-description-generator`.
- **GitHub:** `https://github.com/nshaokiet/ai-ip-description-generator` — Private, đã xác minh ngày 18/09/2026.
- **Mục tiêu MVP:** nhận một bài báo khoa học PDF/DOCX, tạo Structured JSON có source evidence, bản dự thảo patent specification cần Human review và DOCX.
- **Deadline MVP:** 02/10/2026.
- **Trạng thái dự án:** SPEC-001/002/003 là approved baseline; APP-001/002/003, P0-005/006/007 đã triển khai và merge cho local/synthetic workflow. Chưa có Human approval cho production/public deployment hoặc dữ liệu nghiên cứu thật; BLK-003 vẫn OPEN. Không suy diễn toàn bộ phase hoặc release đã hoàn tất.
- **Nguyên tắc pháp lý:** output là bản dự thảo, không phải bằng sáng chế, kết luận patentability, tư vấn pháp lý hoặc hồ sơ được bảo đảm chấp thuận.

## 2. Mục tiêu của AGENTS.md

Tài liệu này quy định quyền hạn, thứ tự đọc, workflow, review, versioning, source grounding, bảo mật và handoff cho mọi Human hoặc AI làm việc trong repository. Mọi agent phải tuân thủ tài liệu này trước khi sửa artefact. Nếu task của Human xung đột với quy tắc hiện hành, agent phải nêu xung đột và xin quyết định thay vì âm thầm chọn.

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

Human / Product Owner là **Governance & Final Approval Authority**:

- Xác nhận requirement, scope, deadline, chi phí và release.
- Phê duyệt thay đổi kiến trúc chính, tech stack, security/data policy, provider/model policy và breaking change.
- Phê duyệt task/gate, quyết định merge `main`, release và output cuối.
- Giải quyết bất đồng CRITICAL/HIGH hoặc bất đồng ảnh hưởng kiến trúc/pháp lý/scope.
- Xác nhận việc xử lý tài liệu chưa công bố và nhà cung cấp dữ liệu.
- Không mặc định đã phê duyệt chỉ vì một đề xuất xuất hiện trong tài liệu.

## 5. Vai trò ChatGPT và Codex

### ChatGPT — Technical Coordinator & Architecture Advisor

- Chuyển mục tiêu Human thành specification, task scope, prompt, review checklist và handoff rõ ràng.
- Hỗ trợ kiến trúc, integration planning, governance, evidence reconciliation và quyết định kỹ thuật cần trình Human.
- Có thể chuẩn bị/cập nhật tài liệu governance khi được Human yêu cầu.
- Không tự thay Human phê duyệt scope, security/data policy, paid API, merge hoặc release.

### Codex (VS Code) — Primary Implementation Agent

- Claim task đã được Human approve thông qua Project Orchestrator MCP.
- Viết/sửa code, test, debug, refactor trong approved scope.
- Làm việc trên branch/worktree riêng; commit/push evidence thật.
- Chạy targeted/regression/E2E tests phù hợp và báo progress/checkpoint qua MCP.
- Xử lý remediation sau independent review.
- Không tự approve review, không tự chuyển task thành MERGED/COMPLETED và không merge `main`.

## 6. Vai trò Antigravity Reviewer Agent

Antigravity là **Independent Review & QA Environment**:

- Review độc lập một branch/commit SHA cố định sau implementation.
- Kiểm tra acceptance criteria, regression, scope compliance, security/privacy, failure handling và evidence.
- Trả kết quả `PASS`, `REQUEST CHANGES` hoặc blocker có bằng chứng.
- Không sửa trực tiếp production artefact trong vai trò reviewer; remediation quay lại Codex trừ khi Human giao task riêng.
- Tên vai trò không gắn cứng với một model/provider. **Mỗi review record phải ghi exact Antigravity model/profile thực tế được sử dụng.**
- Reviewer approval không thay thế Human merge/release approval.

## 7. Vai trò Project Orchestrator MCP

Project Orchestrator MCP là **Coordination & State Management Layer**, không phải implementation/review agent:

- Quản lý task queue, lifecycle, dependencies và eligibility.
- Cấp/renew/release task lease để tránh hai agent cùng sửa một task.
- Lưu budget/quota state thủ công và thực thi stop threshold.
- Lưu checkpoint/handoff để Codex và Antigravity dùng chung trạng thái.
- Ghi branch/worktree/owner/blocker/next action dưới dạng operational state.
- Không viết code, không review artefact, không approve task, không merge Git, không force/reset history và không tự kích hoạt banked quota reset.

## 8. Ma trận quyền hạn

| Actor | Implement/Edit production | Independent review | Approve scope/gate | Merge `main` / Release | MCP task state |
|---|---|---|---|---|---|
| Human / Product Owner | Theo nhu cầu | Có | **Có** | **Có** | Admin/approval transitions |
| ChatGPT | Tài liệu/đề xuất khi được giao | Advisory | Không | Không | Không claim implementation task |
| Codex | **Có, trong approved task** | Self-check, không phải independent approval | Không | Không | Claim / progress / finish / checkpoint |
| Antigravity Reviewer Agent | Không trong reviewer role | **Có** | Không | Không | Review evidence / handoff |
| Project Orchestrator MCP | Không | Không | Không | Không | **Lưu và enforce workflow state** |

## 9. Tài liệu bắt buộc phải đọc

Trước khi hành động, đọc theo thứ tự:

1. `AGENTS.md`.
2. `PROJECT_CONTEXT.md`.
3. `docs/system-specification.md`.
4. ADR liên quan trong `docs/decisions/`, nếu tồn tại.
5. Project Control Center, nếu có quyền truy cập.
6. Gemini Review Log, nếu task liên quan review.

Trạng thái tại phiên bản 0.2.0:

- `AGENTS.md`: tồn tại.
- `PROJECT_CONTEXT.md`: tồn tại trong cùng commit khởi tạo; nếu checkout riêng không thấy thì ghi `[FILE CHƯA TỒN TẠI]`.
- `docs/system-specification.md`: tồn tại.
- ADR-001…ADR-005 trong `docs/decisions/`: tồn tại và `Accepted` theo Human decisions ngày 20/09/2026; các ADR runtime artefact khác tiếp tục theo history riêng.
- Bản nguồn Git của Project Control Center: `docs/operations/01_PROJECT_CONTROL_CENTER.md`.
- Bản nguồn Git của Gemini Review Log: `docs/operations/02_GEMINI_REVIEW_LOG.md`.
- Trạng thái đồng bộ hai bản nguồn sang Google Docs: `[CẦN XÁC NHẬN TRẠNG THÁI]`.

## 10. Workflow làm việc

`Task → Assign → Execute → Review → Decision → Update state → Next task`

1. Task phải có ID, owner, output và acceptance criteria.
2. Agent kiểm tra artefact hiện có và dependencies trước khi sửa.
3. Tạo thay đổi nhỏ, có thể review, đúng phạm vi.
4. Chạy kiểm tra phù hợp và lưu bằng chứng.
5. Review độc lập khi task yêu cầu.
6. Finding cần quyết định được chuyển Human.
7. Cập nhật version, change log, state và handoff.
8. Không ghi `Completed` nếu không có file/commit/test/output/Human confirmation làm bằng chứng.

## 11. Quy tắc review giữa AI

`Human approve task → Codex implement/test → Antigravity independent review → Codex remediation nếu cần → Human approve merge/release`

- Antigravity reviewer ghi branch/SHA, exact model/profile, evidence, impact và suggested change cho từng finding.
- Codex xử lý remediation trong approved scope; ChatGPT hỗ trợ đánh giá/escalation khi finding chạm kiến trúc, scope hoặc governance.
- Finding CRITICAL/HIGH không được bỏ qua, sửa im lặng hoặc đóng khi chưa có resolution evidence.
- `APPROVE` của reviewer không thay thế release approval của Human.

## 12. Quy tắc không overwrite

- Antigravity không sửa trực tiếp artefact production khi đang thực hiện independent review.
- Mọi agent phải kiểm tra file hiện có và diff trước khi sửa.
- Không ghi đè chỉnh sửa của Human/agent khác; nếu có xung đột, dừng và ghi rõ conflict.
- Thay đổi production artefact phải tạo version mới theo chính sách, bảo toàn history trong Git.
- Review log là append-oriented; không xóa finding cũ để làm sạch trạng thái.

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

## 19. Quy tắc thay đổi scope

Các thay đổi sau cần Human approval trước khi triển khai:

- Thêm/bỏ chức năng MVP hoặc đổi deadline.
- Đổi tech stack, provider, kiến trúc chính hoặc deployment platform.
- Breaking change API/schema/template.
- Thay đổi cấu trúc patent specification hoặc phạm vi Draft Claims.
- Thay đổi auth, data handling, retention, privacy hoặc security policy.
- Tăng chi phí đáng kể hoặc thêm dịch vụ/dependency mới.

Agent phải trình bày lựa chọn, lý do, ảnh hưởng, rủi ro, migration và recommendation; không được coi im lặng là chấp thuận.

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

Khi implementation evidence của Codex và finding của Antigravity không thống nhất:

1. Ghi hai quan điểm mà không xóa quan điểm còn lại.
2. Ghi nguồn/bằng chứng, assumption và độ tin cậy của mỗi bên.
3. Đánh giá ảnh hưởng tới requirement, kiến trúc, bảo mật, pháp lý, chi phí và deadline.
4. Thử giải quyết bằng Source of Truth/ADR đã phê duyệt.
5. Chuyển Human quyết định nếu severity CRITICAL/HIGH hoặc ảnh hưởng kiến trúc/pháp lý/scope.
6. Ghi decision và artefact/version chịu ảnh hưởng sau khi Human trả lời.

## 22. Definition of Done

Một task chỉ `Completed` khi:

- Output đúng đường dẫn/tên và không thiếu phần bắt buộc.
- Acceptance criteria được kiểm chứng và evidence được ghi.
- Test/lint/validation phù hợp đạt hoặc có exception được Human chấp thuận.
- Diff đã được review; không có secret hoặc dữ liệu nghiên cứu mật.
- Version/change log/API docs liên quan đã cập nhật.
- Finding CRITICAL/HIGH đã resolved hoặc có Human decision.
- Handoff đầy đủ và project state được cập nhật bằng bằng chứng.
- Output AI/SHTT có disclaimer và Human review status phù hợp.

## 23. Các hành vi bị cấm

- Tự bịa requirement, trạng thái, nguồn, quyết định, test result hoặc approval.
- Tự thêm framework, dependency, dịch vụ hoặc thay đổi tech stack.
- Commit secret, paper mật hoặc generated data nhạy cảm.
- Chuyển inference thành fact hoặc bỏ source warning.
- Tự đóng finding chưa xử lý hoặc xóa review history.
- Tuyên bố output có giá trị pháp lý, chắc chắn đủ điều kiện nộp hoặc được cấp bằng.
- Tự thay đổi scope, deadline, architecture, claim scope hoặc data policy.
- Antigravity reviewer ghi đè production artefact; Codex bỏ qua finding HIGH/CRITICAL không có resolution/evidence.
- Đánh dấu `Completed` khi không có bằng chứng.
- Tự động nộp hồ sơ lên USPTO.
