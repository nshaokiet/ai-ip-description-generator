# AGENTS.md

## Quy tắc phối hợp AI của dự án

### Metadata

| Thuộc tính | Giá trị |
|---|---|
| Document ID | SPEC-003 |
| Document title | AGENTS.md — Quy tắc phối hợp AI của dự án |
| Version | 0.1.1 |
| Status | Draft |
| Owner | Human / Product Owner |
| Author | ChatGPT/Codex |
| Reviewer | Gemini Pro |
| Created date | 18/09/2026 |
| Last updated | 18/09/2026 |
| Related task ID | SPEC-003 |
| Source of Truth | GitHub — `AGENTS.md` |
| Confidentiality level | Internal |

### Lịch sử phiên bản

| Phiên bản cũ | Phiên bản mới | Ngày | Người thực hiện | Thay đổi | Lý do | Finding/Decision liên quan | Breaking change |
|---|---|---|---|---|---|---|---|
| Chưa có | 0.1.0 | 18/09/2026 | ChatGPT/Codex | Tạo quy tắc phối hợp AI ban đầu | Khởi tạo Phase 1 | SPEC-003 | No |
| 0.1.0 | 0.1.1 | 18/09/2026 | ChatGPT/Codex | Ghi nhận repository GitHub Private đã được xác minh | Đồng bộ trạng thái thực tế trước khi publish | Yêu cầu Human đưa artefact lên GitHub | No |

## 1. Project identity

- **Project:** AI Intellectual Property Description Generator.
- **Repository:** `ai-ip-description-generator`.
- **GitHub:** `https://github.com/nshaokiet/ai-ip-description-generator` — Private, đã xác minh ngày 18/09/2026.
- **Mục tiêu MVP:** nhận một bài báo khoa học PDF/DOCX, tạo Structured JSON có source evidence, bản dự thảo patent specification cần Human review và DOCX.
- **Deadline MVP:** 02/10/2026.
- **Trạng thái dự án:** Phase 1 — Specification & Architecture; trạng thái phê duyệt thực tế `[CẦN XÁC NHẬN TRẠNG THÁI]`.
- **Nguyên tắc pháp lý:** output là bản dự thảo, không phải bằng sáng chế, kết luận patentability, tư vấn pháp lý hoặc hồ sơ được bảo đảm chấp thuận.

## 2. Mục tiêu của AGENTS.md

Tài liệu này quy định quyền hạn, thứ tự đọc, workflow, review, versioning, source grounding, bảo mật và handoff cho mọi Human hoặc AI làm việc trong repository. Mọi agent phải tuân thủ tài liệu này trước khi sửa artefact. Nếu task của Human xung đột với quy tắc hiện hành, agent phải nêu xung đột và xin quyết định thay vì âm thầm chọn.

## 3. Source of Truth

| Loại thông tin | Nguồn chính thức | Giới hạn |
|---|---|---|
| Kỹ thuật | GitHub repository | Source code, API, schema, prompt, template, docs, tests, ADR, release version |
| Trạng thái vận hành | `01_PROJECT_CONTROL_CENTER` | Cầu nối Human/AI; không ghi đè nội dung kỹ thuật trong GitHub |
| Review | `02_GEMINI_REVIEW_LOG` | Lịch sử review; finding chưa phải quyết định dự án |
| Nghiên cứu | NotebookLM | Research workspace; không phải Source of Truth, không sửa code |

Khi có mâu thuẫn, ưu tiên theo thứ tự:

1. Quyết định mới nhất được Human phê duyệt và ghi lại.
2. ADR/decision record đã được phê duyệt trong `docs/decisions/`.
3. Artefact production hiện hành trong GitHub.
4. `docs/system-specification.md`.
5. `PROJECT_CONTEXT.md`.
6. Project Control Center.
7. Gemini Review Log.
8. Ghi chú hoặc tổng hợp từ NotebookLM.

Mọi mâu thuẫn phải được ghi thành issue, finding, open question hoặc handoff. Không được âm thầm xóa một quan điểm.

## 4. Vai trò Human

Human / Product Owner:

- Xác nhận requirement, scope, deadline, chi phí và release.
- Phê duyệt thay đổi kiến trúc chính, tech stack, security/data policy và breaking change.
- Quyết định cấu trúc đầu ra, phạm vi Draft Claims và việc dùng output cho mục đích SHTT/pháp lý.
- Giải quyết bất đồng CRITICAL/HIGH hoặc bất đồng ảnh hưởng kiến trúc/pháp lý.
- Xác nhận việc xử lý tài liệu chưa công bố và nhà cung cấp dữ liệu.
- Không mặc định đã phê duyệt chỉ vì một đề xuất xuất hiện trong tài liệu.

## 5. Vai trò ChatGPT/Codex

ChatGPT/Codex là **Lead Developer + System Architect + Integration Owner**:

- Phân tích requirement, thiết kế kiến trúc, API, schema, prompt và template.
- Viết và tích hợp frontend/backend/AI/DOCX khi có task được phê duyệt.
- Test, debug, deployment, tài liệu kỹ thuật và versioning.
- Đánh giá từng finding của Gemini, ghi quyết định và tạo version sửa đổi.
- Được tự sửa lỗi chính tả, formatting, bổ sung giải thích không đổi requirement và refactor không đổi hành vi.
- Được xử lý finding LOW/SUGGESTION khi có đủ căn cứ và ghi lại thay đổi.
- Không được tự phê duyệt quyết định thuộc quyền Human.

## 6. Vai trò Gemini Pro

Gemini Pro là **Research Analyst + Independent Reviewer + QA Reviewer**:

- Phân tích paper, patent mẫu và nguồn SHTT được cấp quyền.
- Review schema, prompt, system specification và output.
- Kiểm tra hallucination, grounding, missing information, mâu thuẫn, security/privacy và second opinion.
- Ghi finding vào Gemini Review Log với bằng chứng và recommendation.
- Không phải implementation owner, không tự thay đổi kiến trúc, không sửa trực tiếp artefact production và không tự đóng finding.

## 7. Vai trò NotebookLM

NotebookLM là **Research Workspace**:

- Lưu/tra cứu nguồn được cấp quyền và hỗ trợ tổng hợp, so sánh, grounding.
- Không phải production AI, Source of Truth, implementation owner hoặc nơi phê duyệt quyết định.
- Không sửa code, không tự cập nhật repository và không thay thế tài liệu nguồn gốc.

## 8. Ma trận quyền hạn

Ký hiệu: `Có` = được thực hiện trong phạm vi task; `Review` = chỉ nhận xét; `Human` = chỉ Human phê duyệt/quyết định; `Không` = bị cấm; `Theo task` = chỉ khi được giao rõ.

| Artefact/Hành động | Actor | Create | Read | Review | Edit | Approve | Reject | Deploy | Close review |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Source code | Human | Theo task | Có | Có | Theo task | Human | Human | Human/ủy quyền | Không áp dụng |
| Source code | ChatGPT/Codex | Có | Có | Có | Có | Không | Không | Theo task đã duyệt | Không áp dụng |
| Source code | Gemini Pro | Không | Có | Review | Không | Không | Không | Không | Không áp dụng |
| System specification / Project context | Human | Có | Có | Có | Có | Human | Human | Không áp dụng | Human |
| System specification / Project context | ChatGPT/Codex | Có | Có | Có | Có | Không | Không | Không áp dụng | Không |
| System specification / Project context | Gemini Pro | Không | Có | Review | Không | Không | Không | Không áp dụng | Không |
| Prompt / Schema / Template | Human | Theo task | Có | Có | Theo task | Human | Human | Không áp dụng | Human |
| Prompt / Schema / Template | ChatGPT/Codex | Có | Có | Có | Có | Không | Không | Không áp dụng | Không |
| Prompt / Schema / Template | Gemini Pro | Không | Có | Review | Không | Không | Không | Không áp dụng | Không |
| ADR | Human | Có | Có | Có | Có | Human | Human | Không áp dụng | Human |
| ADR | ChatGPT/Codex | Có | Có | Có | Có | Không | Không | Không áp dụng | Không |
| ADR | Gemini Pro | Không | Có | Review | Không | Không | Không | Không áp dụng | Không |
| Project status | Human | Có | Có | Có | Có | Human | Human | Không áp dụng | Human |
| Project status | ChatGPT/Codex | Theo bằng chứng | Có | Có | Theo bằng chứng | Không | Không | Không áp dụng | Không |
| Project status | Gemini Pro | Không | Có | Review | Không | Không | Không | Không áp dụng | Không |
| Review log | Human | Có | Có | Có | Quyết định Human | Human | Human | Không áp dụng | Human |
| Review log | ChatGPT/Codex | Response/resolution | Có | Có | Chỉ response/resolution | Không | Không | Không áp dụng | Không |
| Review log | Gemini Pro | Review entry | Có | Có | Entry của Gemini | Không | Không | Không áp dụng | Không |
| Production release | Human | Theo quy trình | Có | Có | Theo quy trình | Human | Human | Human/ủy quyền | Human |
| Production release | ChatGPT/Codex | Build theo task | Có | Có | Theo task | Không | Không | Theo task đã duyệt | Không |
| Production release | Gemini Pro | Không | Có | Review | Không | Không | Không | Không | Không |

## 9. Tài liệu bắt buộc phải đọc

Trước khi hành động, đọc theo thứ tự:

1. `AGENTS.md`.
2. `PROJECT_CONTEXT.md`.
3. `docs/system-specification.md`.
4. ADR liên quan trong `docs/decisions/`, nếu tồn tại.
5. Project Control Center, nếu có quyền truy cập.
6. Gemini Review Log, nếu task liên quan review.

Trạng thái tại phiên bản 0.1.1:

- `AGENTS.md`: tồn tại.
- `PROJECT_CONTEXT.md`: tồn tại trong cùng commit khởi tạo; nếu checkout riêng không thấy thì ghi `[FILE CHƯA TỒN TẠI]`.
- `docs/system-specification.md`: tồn tại.
- ADR trong `docs/decisions/`: `[FILE CHƯA TỒN TẠI]` tại thời điểm tạo tài liệu này.
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

`ChatGPT/Codex tạo → Gemini review → ChatGPT/Codex đánh giá → Human quyết định nếu cần → ChatGPT/Codex sửa → tạo version mới → đóng review`

- Gemini ghi nguồn thực tế, location, evidence, impact và suggested change cho từng finding.
- ChatGPT/Codex trả lời từng finding bằng `ACCEPT`, `PARTIALLY ACCEPT`, `REJECT WITH REASON` hoặc `ESCALATE TO HUMAN`.
- Finding CRITICAL/HIGH không được bỏ qua, sửa im lặng hoặc đóng khi chưa có resolution evidence.
- `APPROVE` của reviewer không thay thế release approval của Human.

## 12. Quy tắc không overwrite

- Gemini không sửa trực tiếp artefact production.
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

Khi ChatGPT/Codex và Gemini không thống nhất:

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
- Gemini ghi đè production artefact; ChatGPT/Codex bỏ qua finding HIGH/CRITICAL không lý do.
- Đánh dấu `Completed` khi không có bằng chứng.
- Tự động nộp hồ sơ lên USPTO.
