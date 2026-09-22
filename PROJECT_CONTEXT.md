# PROJECT_CONTEXT.md

## Bối cảnh dự án

## 1. Metadata

| Thuộc tính | Giá trị |
|---|---|
| Document ID | SPEC-002 |
| Document title | Project Context — AI Intellectual Property Description Generator |
| Version | 0.3.8 |
| Status | Approved baseline |
| Owner | Human / Product Owner |
| Author | ChatGPT/Codex |
| Reviewer | Gemini 3.1 Pro High |
| Created date | 18/09/2026 |
| Last updated | 22/09/2026 |
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
| 0.2.4 | 0.2.5 | 19/09/2026 | ChatGPT/Codex | Chuyển AI-002 sang Completed sau khi Human merge PR #3 | Đồng bộ governance state sau merge | AI-002, REV-AI-002, PR #3, merge commit `8f2b7082881961cc1a2cf7fa56ece81976759c7f` | No |
| 0.2.5 | 0.2.6 | 19/09/2026 | ChatGPT/Codex | Ghi nhận Patent Draft Generation Contract v1.0.0 và Draft Generation Prompt v1.0.0 đã triển khai, chờ Gemini review | Đồng bộ quyết định Human và bằng chứng AI-003 | AI-003, ADR-008 | No |
| 0.2.6 | 0.2.7 | 20/09/2026 | ChatGPT/Codex | Ghi nhận Gemini 3.1 Pro High independent review AI-003 PASS, không có finding hoặc required change | Đồng bộ review evidence thực tế trước commit, PR và merge | AI-003, ADR-008, REV-AI-003 | No |
| 0.2.7 | 0.2.8 | 20/09/2026 | ChatGPT/Codex | Chuyển AI-003 sang Completed sau khi Human merge PR #5 | Đồng bộ governance state sau merge | AI-003, REV-AI-003, PR #5, merge commit `fb522bc5ecbb5ad66bab6226fa88ae51020cef52` | No |
| 0.2.8 | 0.2.9 | 20/09/2026 | ChatGPT/Codex | Ghi nhận Patent DOCX Template v1.0.0, offline renderer và automated validation đã triển khai | Đồng bộ quyết định Human và bằng chứng DOC-001 trước visual QA/review | DOC-001, ADR-009 | No |
| 0.2.9 | 0.2.10 | 20/09/2026 | ChatGPT/Codex | Ghi nhận Human Visual QA và Gemini independent review DOC-001 đều PASS, không có finding | Đồng bộ governance state trước Human merge approval | DOC-001, ADR-009, REV-DOC-001 | No |
| 0.2.10 | 0.2.11 | 20/09/2026 | ChatGPT/Codex | Chuyển DOC-001 sang Completed sau khi Human merge PR #7 | Đồng bộ governance state sau merge | DOC-001, ADR-009, REV-DOC-001, PR #7, merge commit `d208a7925da844c5b43578bac8ebdbb1c5c6b5b8` | No |
| 0.2.11 | 0.3.0 | 20/09/2026 | ChatGPT/Codex | Phê duyệt baseline SPEC-002, ghi nhận ADR-001…005 và khóa scope upload APP-001 | Đồng bộ Gemini review và Human decisions trước backend implementation | SPEC-001/002/003, REV-001/002/003, DEC-001/002/003, APP-001 | No |
| 0.3.0 | 0.3.1 | 20/09/2026 | ChatGPT/Codex | Ghi APP-001 hoàn tất sau Gemini PASS và Human merge PR #10 | Đồng bộ post-merge governance evidence, không đổi contract kỹ thuật | APP-001, REV-APP-001, PR #10, merge commit `0df4814ff1eb8cd576566ac3dd403131feca3759` | No |
| 0.3.1 | 0.3.2 | 21/09/2026 | ChatGPT/Codex | Ghi APP-002 hoàn tất sau remediation, Gemini targeted PASS và Human merge PR #12 | Đồng bộ post-merge governance evidence, không đổi contract kỹ thuật | APP-002, REV-APP-002, PR #12, merge commit `4a001d116cbf002bdd42a9151efbf3f308fce3e6` | No |
| 0.3.2 | 0.3.3 | 21/09/2026 | ChatGPT/Codex | Ghi AI-RUNTIME-001 internal extraction runtime đã triển khai và chờ independent review | Đồng bộ runtime configuration, validation boundary và blocker disposition đã được Human phê duyệt | AI-RUNTIME-001, ADR-010 | No |
| 0.3.3 | 0.3.4 | 21/09/2026 | ChatGPT/Codex | Chuyển AI-RUNTIME-001 sang Completed sau remediation, targeted re-review PASS và Human merge PR #14 | Post-merge governance closeout; không đổi technical contract | AI-RUNTIME-001, REV-AI-RUNTIME-001, PR #14, merge commit `597f6c7b074eb2c5e445790b8c4f48f336f04da5` | No |
| 0.3.4 | 0.3.5 | 22/09/2026 | Gemini 3.8 Flash High | Chuyển AI-RUNTIME-002 sang Completed sau remediation, independent review APPROVED và Human merge PR #16 | Post-merge governance closeout; không đổi technical contract | AI-RUNTIME-002, REV-AI-RUNTIME-002, PR #16, merge commit `978516a4f5caa90bbd2189668237c6e028597361` | No |
| 0.3.5 | 0.3.6 | 22/09/2026 | Gemini 3.8 Flash High | Ghi nhận hoàn tất đặc tả kỹ thuật APP-003 Core Pipeline Orchestration v1.0.0, chờ independent review | Đặc tả kỹ thuật nội bộ trước implementation | APP-003, `docs/tasks/APP-003-core-pipeline-orchestration.md` | No |
| 0.3.6 | 0.3.7 | 22/09/2026 | Gemini 3.8 Flash High | Cập nhật đặc tả kỹ thuật APP-003 v1.1.0 sau independent review, chờ re-review | Đồng bộ trạng thái remediated chờ re-review | APP-003, REV-APP-003 | No |
| 0.3.7 | 0.3.8 | 22/09/2026 | Gemini 3.8 Flash High | Làm cứng đặc tả APP-003 v1.2.0: xử lý residual findings H-001 (cleanup exception safety helper), H-002 (Python 3.12 portable regression), H-003 (AC-29 framework routes) | Đồng bộ trạng thái hardened trước targeted re-review | APP-003, H-001, H-002, H-003 | No |

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

MVP/APP-001 chỉ nhận PDF có text và DOCX, tối đa 10 MiB; PDF tối đa 50 trang. Scanned PDF/OCR bị loại khỏi MVP. DOCX không thể kiểm đếm trang exact một cách tin cậy nếu không render; APP-001 không tuyên bố exact page-limit enforcement cho DOCX.

Người dùng phải có quyền hợp pháp để upload và xử lý tài liệu. Không commit bài báo chưa công bố vào repository.

## 7. Output

- Structured invention information.
- Evidence mapping tới file/trang/mục/đoạn/bảng/hình khi xác định được.
- Missing-information list và câu hỏi cho tác giả.
- Draft patent specification.
- Claims/Draft Claims nằm ngoài MVP hiện hành; task tương lai cần Human scope approval riêng.
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
- APP-001 chỉ dùng local ephemeral storage cho single-tenant/synthetic development; xóa ngay khi validation thất bại, sau pipeline/rendering, hoặc muộn nhất sau 1 giờ.
- Private production storage/authentication/database: thiết kế cụ thể `[CẦN XÁC NHẬN]`; không dùng dữ liệu nghiên cứu thật trước security acceptance.
- Supabase/PostgreSQL chỉ là optional/MVP+ hoặc dùng khi được Human phê duyệt.

## 10. Tech Stack

| Lớp | Công nghệ đã định hướng | Trạng thái |
|---|---|---|
| Frontend | Next.js + TypeScript | Requirement; chưa có bằng chứng triển khai |
| Backend | FastAPI + Python 3.12 | APP-001/APP-002, AI-RUNTIME-001 và AI-RUNTIME-002 Completed; internal extraction và draft runtimes đã merge qua PR #14 và PR #16; public surface chưa đổi |
| Production AI | OpenAI Responses API | AI-RUNTIME-001: `gpt-5.6-sol`, reasoning high, `store=false`, timeout 180s, max 48k tokens; AI-RUNTIME-002: `gpt-5.6-sol`, reasoning high, `store=false`, timeout 240s, max 64k tokens; internal only; live provider smoke NOT RUN — DEFERRED due to unavailable API funding |
| Structured data | JSON Schema Draft 2020-12 | Output Schema v1.0.0 — Completed — Merged via PR #1 |
| Extraction prompt | Markdown prompt contract | v1.0.0 — Completed — Merged via PR #3 |
| Patent draft contract | JSON Schema Draft 2020-12 | v1.0.0 — Completed — Merged via PR #5 |
| Draft generation prompt | Markdown prompt contract | v1.0.0 — Completed — Merged via PR #5 |
| Retrieval | Không dùng trong Extraction Runtime v1 hoặc Draft Runtime v1 | AI-RUNTIME-001/AI-RUNTIME-002 chỉ dùng input envelopes; task tương lai cần approval riêng |
| Database | Supabase/PostgreSQL | Optional/MVP+ hoặc khi được phê duyệt |
| DOCX | `docxtpl==0.20.2`, `python-docx==1.2.0` | Patent DOCX Template v1.0.0 — Completed — Merged via PR #7 |
| Frontend deployment | Vercel | Định hướng; config `[FILE CHƯA TỒN TẠI]` |
| Backend deployment | Railway | Định hướng; config `[FILE CHƯA TỒN TẠI]` |
| Version control | GitHub | Technical Source of Truth |

Không tự ý thêm framework, dịch vụ hoặc dependency.

## 11. AI Architecture

1. Parse paper và giữ locator.
2. APP-002 tạo deterministic evidence source units; Extraction Runtime v1 không dùng File Search hoặc external retrieval.
3. AI-RUNTIME-001 extraction bằng prompt/schema version cụ thể và provider schema được dẫn xuất.
4. Validate canonical JSON, provenance và logical reference.
5. Detect missing information, tạo author questions.
6. AI-RUNTIME-002 patent draft generation từ validated analysis, strict provider schema, schema-aware normalization, canonical Draft 2020-12 validation và deterministic business validation.
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
- Draft patent specification và Abstract; không Claims.
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
- Claims/Draft Claims trong MVP hiện hành.
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

SPEC-001, SPEC-002 và SPEC-003 là **Approved baseline** sau Gemini 3.1 Pro High review và Human decisions ngày 20/09/2026. Implementation đã tiến vào các task thuộc Phase 2/Phase 3, nhưng Human / Product Owner chưa tuyên bố toàn bộ Phase 1, Phase 2, Phase 3 hoặc MVP `Completed`.

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
| System Specification | `docs/system-specification.md` | 0.3.5 | SPEC-001 Approved baseline; AI-RUNTIME-002 post-merge state đã đồng bộ |
| AI Collaboration Rules | `AGENTS.md` | 0.2.0 | SPEC-003 Approved baseline |
| Project Context | `PROJECT_CONTEXT.md` | 0.3.5 | SPEC-002 Approved baseline; AI-RUNTIME-002 post-merge state đã đồng bộ |
| Project Control Center source | `docs/operations/01_PROJECT_CONTROL_CENTER.md` | 0.3.5 | AI-RUNTIME-002 Completed — Merged via PR #16; Phase 1/Phase 2/MVP chưa được tuyên bố hoàn tất |
| Gemini Review Log source | `docs/operations/02_GEMINI_REVIEW_LOG.md` | 0.3.4 | `REV-AI-RUNTIME-002` và các task review có bằng chứng đều `CLOSED` |
| Foundational ADRs | `docs/decisions/ADR-001…005-*.md` | ADR-001…ADR-005 | Accepted theo Human decisions ngày 20/09/2026 |
| APP-001 backend | `backend/app/`, `backend/requirements.txt`, `tests/backend/` | Implementation head `bd39b9f7bdd9f7a1796d9a405e7998070e124e07` | Completed — Merged via PR #10; 24/24 APP-001 tests và 109/109 tổng tests pass |
| APP-002 document preparation | `backend/app/`, `tests/backend/test_document_parsing.py` | Implementation `477b8fda6afbae0049d8d691c213dc6355ba67da`; remediation `8b6f909a0f5787d72c002e163395656a666c9b78` | Completed — Merged via PR #12 at `4a001d116cbf002bdd42a9151efbf3f308fce3e6`; Gemini final PASS; 30/30 AC; 135 executed, 134 pass, 1 Windows skip, 0 failure/error |
| AI extraction runtime | `backend/app/services/extraction_runtime.py`, `provider_schema.py`, `extraction_validation.py` | AI-RUNTIME-001 / ADR-010 | Completed — Merged via PR #14 at `597f6c7b074eb2c5e445790b8c4f48f336f04da5`; 32/32 AC; 201 executed, 200 pass, 1 skip; live provider smoke not run |
| AI draft runtime | `backend/app/services/draft_runtime.py`, `draft_provider_schema.py`, `draft_validation.py`, `draft_business_validation.py` | AI-RUNTIME-002 | Completed — Merged via PR #16 at `978516a4f5caa90bbd2189668237c6e028597361` (implementation head `a59ce0219d7039f24fa8c7bd71d4e9829dbbf612`); backend suite 240 pass, 2 skip; tests/draft 25 pass; live smoke deferred |
| Core pipeline orchestration spec | `docs/tasks/APP-003-core-pipeline-orchestration.md` | 1.1.0 | APP-003 Specification — Remediated — Awaiting Independent Re-review; internal composition và offline E2E harness |
| ADR | `docs/decisions/ADR-006-output-schema-v1.md` | ADR-006 | Accepted; Completed — Merged via PR #1 |
| Production JSON Schema | `schemas/invention-output/v1.0.0/invention-output.schema.json` | 1.0.0 | Completed — Merged via PR #1; Gemini review PASS; 15/15 tests pass |
| Production extraction prompt | `prompts/extraction/v1.0.0/extraction-prompt.md` | 1.0.0 | Completed — Merged via PR #3; canonical offline validation only |
| Extraction prompt ADR | `docs/decisions/ADR-007-extraction-prompt-v1.md` | ADR-007 | Accepted — Completed — Merged via PR #3 |
| Patent Draft Schema | `schemas/patent-draft/v1.0.0/patent-draft.schema.json` | 1.0.0 | Completed — Merged via PR #5 |
| Draft generation prompt | `prompts/draft-generation/v1.0.0/draft-generation-prompt.md` | 1.0.0 | Completed — Merged via PR #5; offline only |
| Patent draft ADR | `docs/decisions/ADR-008-patent-draft-contract-v1.md` | ADR-008 | Accepted — Completed — Merged via PR #5 |
| DOCX template | `templates/patent-docx/v1.0.0/patent-description-template.docx` | 1.0.0 | Completed — Merged via PR #7 |
| Application code | `backend/app/` | APP-001 + APP-002 + AI-RUNTIME-001 + AI-RUNTIME-002 | FastAPI local upload/preparation cùng internal extraction và draft runtimes; public analyze/draft endpoints, public orchestration, frontend, database/auth và deployment chưa triển khai |

## 26. Open questions

1. Auth, user roles, tenant model và private production storage nào được dùng?
2. Data/log/backup retention và deletion SLA production là gì? APP-001 chỉ khóa local ephemeral TTL tối đa 1 giờ.
5. Model/cost policy cho draft runtime hoặc task AI tương lai là gì? Extraction Runtime v1 (AI-RUNTIME-001) đã khóa `gpt-5.6-sol`, timeout 180s, 48.000 output tokens; Draft Runtime v1 (AI-RUNTIME-002) đã khóa `gpt-5.6-sol`, timeout 240s, 64.000 output tokens; không retrieval; task tương lai cần approval riêng.
6. Nếu Human mở lại Claims sau MVP/scope change, loại/số lượng và reviewer chuyên môn là ai?
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

1. Gemini 3.1 Pro High independent read-only re-review cho tài liệu đặc tả APP-003 v1.1.0.
2. Human / Product Owner xem xét kết quả review và phê duyệt đặc tả trước khi bắt đầu implementation.
3. Chỉ tiếp tục public orchestration, auth/private storage, production retention, DOCX integration endpoint, frontend, Draft Claims hoặc optional outputs bằng task/approval riêng.

AI-002 được merge với implementation commit `f8772b228a23bf7cdec10fa0c463e6d1f672c341` và governance commit `9f2a78b1396cdadb747c263a2bbbbacb8d7f4292`; Gemini review `PASS`, không có finding, AI-001 regression 15/15 và AI-002 tests 17/17 pass. AI-002 tự thân không chứng minh Responses API hoặc live-model integration; provider adapter/runtime sau đó được Human phê duyệt riêng trong AI-RUNTIME-001. Claims vẫn nằm ngoài Output Schema và Extraction Prompt v1.0.0.

AI-003 triển khai contract trung gian `Validated Output Schema v1.0.0 → Patent Draft Generation Contract v1.0.0 → DOCX template`. Contract giữ exact 11-part order cho DOC-001, paragraph-level source paths/evidence, explicit missing/conflict state và loại hoàn toàn Claims, legal advice, patentability conclusions cùng Human approval state. Fixtures chỉ là synthetic offline oracles; chưa có live-model hoặc provider integration. Gemini 3.1 Pro High review `PASS`, không có finding hoặc required change. Human / Product Owner đã approve và merge PR #5 ngày 20/09/2026; implementation commit `ae7e8fb573ea4681a9db1bafa711d19a3c598666`, merge commit `fb522bc5ecbb5ad66bab6226fa88ae51020cef52`. Trạng thái hiện tại: **Completed — Merged via PR #5**.

DOC-001 triển khai Patent DOCX Template v1.0.0 và deterministic offline renderer từ payload Patent Draft Generation Contract v1.0.0. Template dùng A4, lề 2.54 cm, Times New Roman, exact eleven-part order, header/footer và PAGE/NUMPAGES fields. Renderer validate schema trước khi dùng `docxtpl`, không gọi API/model/mạng, giữ missing/conflict/inference/evidence và loại Claims khỏi mapping. Fixtures hoàn toàn synthetic. Human Microsoft Word Visual QA, Gemini 3.1 Pro High independent review và targeted governance review đều `PASS`; không có finding hoặc required change; 85/85 tests pass. Human / Product Owner đã approve và merge [PR #7](https://github.com/nshaokiet/ai-ip-description-generator/pull/7) ngày 20/09/2026; implementation commit `d3f7c7d9596b77a39e9a56fcdf97c76cb972612a`, merge commit `d208a7925da844c5b43578bac8ebdbb1c5c6b5b8`. Trạng thái hiện tại: **Completed — Merged via PR #7**.

APP-001 triển khai FastAPI local single-tenant skeleton với `GET /health`, secure `POST /api/documents`, layered validation cho PDF/DOCX, safe structured errors, opaque storage identifiers, local ephemeral cleanup và synthetic offline tests. Không có frontend, OpenAI/model call, database, authentication, production storage hoặc deployment. Gemini 3.1 Pro High review `PASS`: 22 acceptance criteria pass, 0 failed, 0 unverifiable; Security và Scope đều `PASS`; không có blocker hoặc required remediation. Human / Product Owner đã approve và merge [PR #10](https://github.com/nshaokiet/ai-ip-description-generator/pull/10) ngày 20/09/2026; specification merge `1bf957162eba78c069d3ba976af7fe1d174cab30`, implementation head `bd39b9f7bdd9f7a1796d9a405e7998070e124e07`, merge commit `0df4814ff1eb8cd576566ac3dd403131feca3759`. Trạng thái hiện tại: **Completed — Merged via PR #10**.

AI-RUNTIME-001 triển khai internal OpenAI Responses API extraction boundary từ APP-002 envelope tới validated Structured Invention Analysis. Gemini implementation review trả `PASS WITH NON-BLOCKING NOTES`; F-001 `MEDIUM` được sửa tại `5247cbcbe591d8b29917d9982b9066e393901c7e` và targeted re-review `PASS`. Human / Product Owner đã approve và merge [PR #14](https://github.com/nshaokiet/ai-ip-description-generator/pull/14) ngày 21/09/2026 tại merge commit `597f6c7b074eb2c5e445790b8c4f48f336f04da5`. 32/32 acceptance criteria đạt; regression ghi nhận 201 executed, 200 pass, 1 intentional Windows skip. Live provider smoke vẫn `NOT RUN — OPENAI_API_KEY not available`; BLK-003 vẫn mở. Trạng thái hiện tại: **Completed — Merged via PR #14**.
AI-RUNTIME-002 triển khai internal OpenAI Responses API draft generation runtime từ validated Structured Invention Analysis (AI-001) qua deterministic AI-003 Draft Input Envelope tới validated Patent Description Draft JSON. Runtime sử dụng `gpt-5.6-sol`, reasoning high, `store=false`, timeout 240 giây, SDK retries 2 và `max_output_tokens=64000`. Output đi qua provider-schema adaptation, schema-aware normalization, canonical Patent Draft 2020-12 validation và deterministic business/grounding validation. Đợt remediation cuối đã xử lý abstract validation governance contract, F-D12 JSON Pointer `/` handling, F-D13 dead helper removal, F-D14 test target_path precision, sửa test imports từ `httpx2` sang `httpx` và bổ sung các biến môi trường draft cần thiết vào `.env.example`; F-D15 prohibited-substring scanner false-positive risk được giữ lại như non-blocking NOTE. Independent final review kết luận `APPROVED`. Human / Product Owner đã approve và merge [PR #16](https://github.com/nshaokiet/ai-ip-description-generator/pull/16) ngày 22/09/2026 tại merge commit `978516a4f5caa90bbd2189668237c6e028597361` (implementation head `a59ce0219d7039f24fa8c7bd71d4e9829dbbf612`). Automated evidence: backend test suite 240 pass, 2 skip, 1 warning; tests/draft 25 pass. Live provider smoke ghi nhận `NOT RUN — DEFERRED due to unavailable API funding`; BLK-003 vẫn mở. Trạng thái hiện tại: **Completed — Merged via PR #16**.
