# PROJECT_CONTEXT.md

## Bối cảnh dự án

## 1. Metadata

| Thuộc tính | Giá trị |
|---|---|
| Document ID | SPEC-002 |
| Document title | Project Context — AI Intellectual Property Description Generator |
| Version | 0.2.4 |
| Status | Draft |
| Owner | Human / Product Owner |
| Author | ChatGPT/Codex |
| Reviewer | Gemini Pro |
| Created date | 18/09/2026 |
| Last updated | 19/09/2026 |
| Related task ID | SPEC-002 |
| Source of Truth | GitHub — `PROJECT_CONTEXT.md` |
| Confidentiality level | Internal; research inputs are Confidential by default |

### Lịch sử phiên bản

| Phiên bản cũ | Phiên bản mới | Ngày | Người thực hiện | Thay đổi | Lý do | Finding/Decision liên quan | Breaking change |
|---|---|---|---|---|---|---|---|
| Chưa có | 0.1.0 | 18/09/2026 | ChatGPT/Codex | Tạo project context ban đầu | Khởi tạo Phase 1 | SPEC-002 | No |
| 0.1.0 | 0.1.1 | 18/09/2026 | ChatGPT/Codex | Ghi nhận URL và visibility của repository GitHub | Đồng bộ trạng thái đã kiểm chứng | Yêu cầu Human đưa artefact lên GitHub | No |
| 0.1.1 | 0.2.0 | 18/09/2026 | ChatGPT/Codex | Ghi nhận contract Output Schema v1.0.0 và ranh giới AI-001 | Đồng bộ quyết định Human đã phê duyệt | AI-001, ADR-006 | No |
| 0.2.0 | 0.2.1 | 18/09/2026 | ChatGPT/Codex | Ghi nhận Gemini review PASS và PR #1 đang chờ Human merge approval | Đồng bộ governance state có bằng chứng | AI-001, REV-AI-001, PR #1 | No |
| 0.2.1 | 0.2.2 | 19/09/2026 | ChatGPT/Codex | Ghi nhận AI-001 hoàn tất sau khi Human merge PR #1 | Đồng bộ governance state sau merge | AI-001, REV-AI-001, PR #1, merge commit `49efead593437dfc5c88397ea6f335a2d4ff84d7` | No |
| 0.2.2 | 0.2.3 | 19/09/2026 | ChatGPT/Codex | Ghi nhận Extraction Prompt v1.0.0 và ranh giới canonical offline validation | Đồng bộ quyết định Human cho AI-002 | AI-002, ADR-007 | No |
| 0.2.3 | 0.2.4 | 19/09/2026 | ChatGPT/Codex | Ghi nhận Gemini 3.1 Pro High review PASS và PR #3 đang chờ Human merge approval | Đồng bộ review evidence thực tế | AI-002, REV-AI-002, PR #3 | No |

## 2. Project name

**AI Intellectual Property Description Generator**

## 3. Repository

`ai-ip-description-generator`

Repository: `https://github.com/nshaokiet/ai-ip-description-generator`.

Visibility: **Private**, đã xác minh ngày 18/09/2026.

## 4. Problem Statement

Bài báo nghiên cứu khoa học không được viết theo cấu trúc patent specification. Việc chuyển đổi thủ công cần nhiều thời gian và dễ mất liên kết giữa phát biểu kỹ thuật với tài liệu nguồn. Dự án xây một workflow có kiểm soát để trích xuất, chuẩn hóa, phát hiện thiếu thông tin, tạo bản dự thảo và giữ source evidence cho từng nội dung quan trọng.

## 5. Business Objective

- Rút ngắn giai đoạn chuẩn bị bản nháp ban đầu.
- Chuẩn hóa thông tin để tác giả và chuyên gia SHTT review.
- Giảm hallucination bằng source grounding và Human-in-the-loop.
- Tạo DOCX có thể chỉnh sửa và truy vết về phiên bản đầu vào/output.

Sản phẩm không thay thế chuyên gia SHTT và không đưa ra kết luận pháp lý.

## 6. Input

Một scientific research paper:

- PDF.
- DOCX.

Scanned PDF và OCR: **[CẦN XÁC NHẬN]**.

Người dùng phải có quyền hợp pháp để upload và xử lý tài liệu. Không commit bài báo chưa công bố vào repository.

## 7. Output

- Structured invention information.
- Evidence mapping tới file/trang/mục/đoạn/bảng/hình khi xác định được.
- Missing-information list và câu hỏi cho tác giả.
- Draft patent specification.
- Draft Claims với số lượng/loại claim `[CẦN XÁC NHẬN]`.
- Abstract tối đa 150 từ.
- Structured JSON.
- DOCX.
- PDF, QA report và claim–description–source mapping: `[CẦN XÁC NHẬN]` đối với MVP.

Mọi đầu ra là **bản dự thảo cần Human hoặc chuyên gia SHTT review**. Đây không phải bằng sáng chế đã cấp, tư vấn pháp lý, kết luận patentability, hồ sơ chắc chắn đủ điều kiện nộp hoặc được USPTO chấp thuận.

## 8. Core Workflow

`Research paper → validation → AI analysis → structured extraction → grounding validation → missing-information detection → draft → human review → DOCX`

Pipeline MVP ưu tiên một paper cho một hồ sơ. Nội dung thiếu không được tự bịa; dùng `[CẦN TÁC GIẢ XÁC NHẬN]`.

## 9. Architecture

`Next.js → FastAPI → OpenAI Responses API → Structured Outputs → Validation → Draft generation → docxtpl → DOCX`

- Next.js: upload, progress, review, edit, section status và export UI.
- FastAPI: API, orchestration, validation, versioning, audit và document generation.
- OpenAI Responses API: extraction/drafting theo prompt và schema có version.
- Validation: schema, business rules, grounding, consistency và claim support.
- `docxtpl`: render DOCX template có version.
- Private storage/authentication/database: thiết kế cụ thể `[CẦN XÁC NHẬN]`.
- Supabase/PostgreSQL chỉ là optional/MVP+ hoặc dùng khi được Human phê duyệt.

## 10. Tech Stack

| Lớp | Công nghệ đã định hướng | Trạng thái |
|---|---|---|
| Frontend | Next.js + TypeScript | Requirement; chưa có bằng chứng triển khai |
| Backend | FastAPI + Python | Requirement; chưa có bằng chứng triển khai |
| Production AI | OpenAI Responses API | Requirement; model `[CẦN XÁC NHẬN]` |
| Structured data | JSON Schema Draft 2020-12 | Output Schema v1.0.0 — Completed — Merged via PR #1 |
| Extraction prompt | Markdown prompt contract | v1.0.0 — Gemini Review Passed — Awaiting Human Merge Approval |
| Retrieval | OpenAI File Search nếu cần | Quyết định `[CẦN XÁC NHẬN]` |
| Database | Supabase/PostgreSQL | Optional/MVP+ hoặc khi được phê duyệt |
| DOCX | `docxtpl` | Requirement; template `[FILE CHƯA TỒN TẠI]` |
| Frontend deployment | Vercel | Định hướng; config `[FILE CHƯA TỒN TẠI]` |
| Backend deployment | Railway | Định hướng; config `[FILE CHƯA TỒN TẠI]` |
| Version control | GitHub | Technical Source of Truth |

Không tự ý thêm framework, dịch vụ hoặc dependency.

## 11. AI Architecture

1. Parse paper và giữ locator.
2. Tạo evidence chunks hoặc dùng File Search theo quyết định được duyệt.
3. Extraction bằng prompt/schema version cụ thể.
4. Validate JSON và reference.
5. Detect missing information, tạo author questions.
6. Generate draft từ dữ liệu đã phân loại.
7. Grounding/consistency validation.
8. Human review trước export.

Không fine-tune và không xây multi-agent runtime phức tạp trong MVP nếu chưa có quyết định riêng.

## 12. Source-grounding model

| Nhãn | Ý nghĩa | Quy tắc |
|---|---|---|
| `SOURCE_FACT` | Có căn cứ trực tiếp | Phải có evidence locator khi xác định được |
| `PARAPHRASE` | AI diễn đạt lại nội dung có nguồn | Không làm đổi ý nghĩa kỹ thuật |
| `INFERENCE` | AI suy luận | Hiển thị rõ, không nâng thành fact |
| `MISSING` | Chưa có căn cứ | Không tự điền; tạo câu hỏi nếu cần |
| `HUMAN_CONFIRMED` | Human có thẩm quyền xác nhận | Phải có audit record |

Evidence nên gồm source file, page, section, paragraph/chunk, table/figure, excerpt ngắn, evidence type và Human status.

Output Schema v1.0.0 có phạm vi hẹp hơn mô hình toàn hệ thống: grounding object chỉ chấp nhận `SOURCE_FACT`, `PARAPHRASE`, `INFERENCE`, đều phải có `evidence_ids`. `MISSING` nằm trong `missing_information`; `HUMAN_CONFIRMED` và audit reference không thuộc v1.0.0. Claims cũng bị loại hoàn toàn khỏi contract này.

## 13. MVP Scope

- Upload/validation PDF và DOCX.
- Parse và AI document analysis.
- Structured extraction cho problem, solution, components/process steps, distinguishing features tiềm năng, effects, embodiments và experiments.
- Evidence, grounding labels, missing information và author questions.
- Draft patent specification, Draft Claims và Abstract.
- Human review, edit, section status và version tracking.
- Grounding/consistency validation.
- DOCX export.
- Error handling, activity history, privacy/security tối thiểu được phê duyệt.

## 14. Non-MVP Scope

- Tự động nộp USPTO.
- Patentability/novelty/inventive-step conclusion.
- Prior-art search toàn diện.
- Inventorship hoặc legal advice.
- Cam kết đầu ra sẵn sàng nộp/được cấp.
- Fine-tuning, complex multi-agent runtime.
- Hỗ trợ đầy đủ mọi loại hồ sơ SHTT/jurisdiction.

## 15. Data handling principles

- Source paper, parsed content, evidence, output và logs là các loại dữ liệu riêng.
- Source/derived data phải ở private storage; storage provider `[CẦN XÁC NHẬN]`.
- Chỉ thu thập và log metadata cần thiết; không log toàn văn paper.
- Có delete path cho source và derived data.
- Retention cho source, output, logs, backup: `[CẦN XÁC NHẬN]`.
- Không dùng dữ liệu để fine-tune/dataset nếu chưa có phép.
- Không mặc định provider AI được phép lưu/sử dụng dữ liệu; phải review policy.

## 16. Security principles

- API key backend-only và lấy từ environment/secret manager.
- Authentication, authorization, tenant isolation: `[CẦN XÁC NHẬN]`.
- TLS in transit; encryption at rest `[CẦN XÁC NHẬN]` theo provider.
- Validate file type/signature/size; malware scanning `[CẦN XÁC NHẬN]`.
- Least privilege, private download, redacted logs và secret rotation.
- Không commit paper mật, secret, `.env` thật hoặc generated output nhạy cảm.

## 17. Current assumptions

- Deadline MVP là 02/10/2026.
- Mục tiêu hoàn thành nội bộ là 30/09/2026; ngày 01–02/10 dành cho buffer, test và handover.
- Một paper cho một hồ sơ MVP.
- Repository dự kiến private.
- OpenAI là production AI; Gemini là reviewer, không phải dependency runtime.
- Human/chuyên gia SHTT sẽ review output.
- Hai tài liệu US11367264B2 và US11044591B2 là patent references có mã B2, không phải biểu mẫu USPTO tên “mẫu B”.
- Các assumption chưa được Human phê duyệt vẫn là assumption, không phải decision.

## 18. Important terminology

| Thuật ngữ | Giải thích trong dự án |
|---|---|
| Patent specification | Phần mô tả hồ sơ sáng chế; output của hệ thống chỉ là draft |
| B2 | Kind code của bằng sáng chế tiện ích đã được cấp theo tài liệu tham chiếu; không phải tên form |
| Structured Output | JSON tuân thủ schema để máy kiểm tra và xử lý |
| Source grounding | Liên kết phát biểu với bằng chứng trong nguồn |
| Evidence | Locator và excerpt hỗ trợ một nội dung |
| Human-in-the-loop | Human bắt buộc review/xác nhận trước sử dụng quan trọng |
| Hallucination | Nội dung AI tạo nhưng không có căn cứ hoặc sai nguồn |
| Claim | Câu xác định phạm vi bảo hộ được yêu cầu; ở đây chỉ là Draft Claim |
| Embodiment | Phương án thực hiện cụ thể được mô tả và có support |
| Prior art | Thông tin công khai trước thời điểm liên quan; MVP không làm search toàn diện |
| ADR | Architecture Decision Record ghi quyết định, lý do và phương án thay thế |
| Source of Truth | Nguồn chính thức được ưu tiên khi có mâu thuẫn |

## 19. Current project phase

Giai đoạn khởi tạo đề xuất: **Phase 1 — Specification & Architecture**.

Trạng thái Phase 1 đã được Human phê duyệt: **[CẦN XÁC NHẬN TRẠNG THÁI]**.

Các file đặc tả/quản trị hiện hành tồn tại trong repository; chúng vẫn ở `Draft` và chưa đồng nghĩa đã được Human/Gemini approve.

## 20. AI Roles

- **Human / Product Owner:** scope, approval, decision, final output/release.
- **ChatGPT/Codex:** Lead Developer, System Architect, Integration Owner.
- **Gemini Pro:** Research Analyst, Independent Reviewer, QA Reviewer; không overwrite production.
- **NotebookLM:** Research Workspace; không phải Source of Truth hoặc production AI.

Chi tiết quyền hạn nằm trong `AGENTS.md`.

## 21. Source of Truth

1. Human-approved decision.
2. Approved ADR.
3. Current production artefact in GitHub.
4. `docs/system-specification.md`.
5. `PROJECT_CONTEXT.md`.
6. Project Control Center.
7. Gemini Review Log.
8. NotebookLM notes.

## 22. Communication Bridge

Google Drive dùng để chia sẻ:

- `01_PROJECT_CONTROL_CENTER`: trạng thái vận hành.
- `02_GEMINI_REVIEW_LOG`: review history.

Bản nguồn Git hiện ở `docs/operations/`. Trạng thái tạo/đồng bộ Google Docs: `[CẦN XÁC NHẬN TRẠNG THÁI]`. Google Docs không ghi đè technical artefacts trong GitHub.

## 23. Research Workspace

NotebookLM lưu và tra cứu nguồn được cấp quyền, hỗ trợ grounding và so sánh. Nó không sửa code, không phê duyệt quyết định, không tự cập nhật GitHub và không thay thế tài liệu gốc.

## 24. Critical project rules

1. Không bịa thông tin kỹ thuật, source, decision, test hoặc trạng thái.
2. Human review bắt buộc.
3. API key chỉ ở backend.
4. Prompt/schema/template/API contract phải có version.
5. Repository GitHub phải private trước dữ liệu nhạy cảm.
6. Không commit confidential paper nếu chưa được phép.
7. Không mô tả output là tài liệu pháp lý hoàn chỉnh.
8. Không tự thay scope, deadline, tech stack hoặc architecture.
9. Mỗi nội dung kỹ thuật quan trọng phải có evidence hoặc nhãn thiếu/suy luận.
10. Gemini review; ChatGPT/Codex implement; Human quyết định phần thuộc thẩm quyền.

## 25. Current artefacts

| Artefact | Location | Version | Status có bằng chứng |
|---|---|---|---|
| System Specification | `docs/system-specification.md` | 0.2.1 | Draft file cập nhật cho AI-002 |
| AI Collaboration Rules | `AGENTS.md` | 0.1.1 | Draft file tồn tại |
| Project Context | `PROJECT_CONTEXT.md` | 0.2.4 | Ghi nhận Gemini review PASS cho AI-002 và PR #3 đang chờ Human merge approval |
| Project Control Center source | `docs/operations/01_PROJECT_CONTROL_CENTER.md` | 0.2.4 | Theo dõi AI-002 đang chờ Human merge approval |
| Gemini Review Log source | `docs/operations/02_GEMINI_REVIEW_LOG.md` | 0.2.2 | REV-AI-001 đã `CLOSED`; REV-AI-002 đã `APPROVED` và chưa đóng |
| ADR | `docs/decisions/ADR-006-output-schema-v1.md` | ADR-006 | Accepted; Completed — Merged via PR #1 |
| Production JSON Schema | `schemas/invention-output/v1.0.0/invention-output.schema.json` | 1.0.0 | Completed — Merged via PR #1; Gemini review PASS; 15/15 tests pass |
| Production extraction prompt | `prompts/extraction/v1.0.0/extraction-prompt.md` | 1.0.0 | Gemini Review Passed — Awaiting Human Merge Approval; canonical offline validation only |
| Extraction prompt ADR | `docs/decisions/ADR-007-extraction-prompt-v1.md` | ADR-007 | Accepted — Gemini Review Passed — Awaiting Human Merge Approval |
| DOCX template | Chưa xác định | Chưa có | `[FILE CHƯA TỒN TẠI]` |
| Application code | Chưa khởi tạo | Chưa có | `[FILE CHƯA TỒN TẠI]` |

## 26. Open questions

1. Có OCR/scanned PDF trong MVP không?
2. File size/page limit là bao nhiêu?
3. Auth, user roles, tenant model và private storage nào được dùng?
4. Data/log/backup retention và deletion SLA là gì?
5. Model OpenAI, File Search/chunking, retry, timeout và cost limit là gì?
6. Loại/số lượng Draft Claims và reviewer chuyên môn là ai?
7. PDF/QA report/claim mapping có thuộc MVP không?
8. Golden set, metrics, threshold và tài liệu test được cấp quyền là gì?
9. Hai tài liệu vận hành đã được đồng bộ sang Google Docs hay chưa?

## 27. Recommended reading order

1. `AGENTS.md` — quyền hạn và workflow.
2. `PROJECT_CONTEXT.md` — bối cảnh nhanh.
3. `docs/system-specification.md` — requirement/architecture đầy đủ.
4. ADR trong `docs/decisions/` khi tồn tại.
5. `docs/operations/01_PROJECT_CONTROL_CENTER.md` — trạng thái và quyết định đang chờ.
6. `docs/operations/02_GEMINI_REVIEW_LOG.md` — findings và resolution.

## 28. Recommended next action

1. Human review/phê duyệt hoặc chỉnh sửa phạm vi trong system specification.
2. Gemini review độc lập ba tài liệu kỹ thuật hiện hành và ghi review entry thật.
3. Human xử lý các câu hỏi chặn về OCR, auth/storage, retention, AI runtime, Draft Claims và optional outputs.
4. Human xem xét merge PR #3 sau Gemini 3.1 Pro High review `PASS`, không có finding hoặc required change; chưa ghi AI-002 là `Completed` khi PR chưa merge.

AI-002 không chứng minh Responses API hoặc live-model integration. Canonical Output Schema v1.0.0 không được gửi nguyên trạng vào Structured Outputs strict mode; provider-specific generation schema/adapter cần task runtime và approval riêng.
