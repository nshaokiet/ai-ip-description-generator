# ĐẶC TẢ HỆ THỐNG

## AI Intellectual Property Description Generator

## 1. Metadata

| Thuộc tính | Giá trị |
|---|---|
| Document ID | SPEC-001 |
| Document title | Đặc tả hệ thống — AI Intellectual Property Description Generator |
| Version | 0.3.2 |
| Status | Approved baseline |
| Owner | Human / Product Owner |
| Author | ChatGPT/Codex |
| Reviewer | Gemini 3.1 Pro High |
| Created date | 18/09/2026 |
| Last updated | 21/09/2026 |
| Related task ID | SPEC-001 |
| Source of Truth | GitHub — `docs/system-specification.md` |
| Confidentiality level | Internal; tài liệu nghiên cứu đầu vào phải được xử lý như Confidential |

> Tài liệu này là approved baseline sau Gemini 3.1 Pro High review và Human decisions ngày 20/09/2026. Các mục còn nhãn `[CẦN XÁC NHẬN]` vẫn cần quyết định riêng trước phần implementation/release liên quan.

## 2. Lịch sử phiên bản

| Phiên bản cũ | Phiên bản mới | Ngày | Người thực hiện | Thay đổi | Lý do | Finding/Decision liên quan | Breaking change |
|---|---|---|---|---|---|---|---|
| Chưa có | 0.1.0 | 18/09/2026 | ChatGPT/Codex | Tạo bản đặc tả hệ thống đầu tiên | Khởi tạo Phase 1 | SPEC-001 | No |
| 0.1.0 | 0.2.0 | 18/09/2026 | ChatGPT/Codex | Liên kết Output Schema v1.0.0 và ghi rõ ranh giới contract | Đồng bộ quyết định Human cho AI-001 | AI-001, ADR-006 | No |
| 0.2.0 | 0.2.1 | 19/09/2026 | ChatGPT/Codex | Liên kết Extraction Prompt v1.0.0, input envelope và giới hạn provider integration | Đồng bộ quyết định Human cho AI-002 | AI-002, ADR-007 | No |
| 0.2.1 | 0.2.2 | 19/09/2026 | ChatGPT/Codex | Liên kết Patent Draft Generation Contract v1.0.0, Draft Generation Prompt và validation boundary | Đồng bộ quyết định Human cho AI-003 | AI-003, ADR-008 | No |
| 0.2.2 | 0.2.3 | 20/09/2026 | ChatGPT/Codex | Đồng bộ trạng thái AI-003 sau Gemini review PASS | Ghi nhận review evidence trước Human merge approval | AI-003, REV-AI-003 | No |
| 0.2.3 | 0.2.4 | 20/09/2026 | ChatGPT/Codex | Ghi nhận AI-003 hoàn tất sau khi Human merge PR #5 | Đồng bộ governance state sau merge, không đổi technical specification | AI-003, REV-AI-003, PR #5 | No |
| 0.2.4 | 0.2.5 | 20/09/2026 | ChatGPT/Codex | Liên kết Patent DOCX Template v1.0.0, mapping và offline renderer | Đồng bộ quyết định Human cho DOC-001 | DOC-001, ADR-009 | No |
| 0.2.5 | 0.2.6 | 20/09/2026 | ChatGPT/Codex | Ghi nhận Human Visual QA và Gemini independent review DOC-001 đều PASS | Đồng bộ governance state, không đổi technical specification | DOC-001, ADR-009, REV-DOC-001 | No |
| 0.2.6 | 0.2.7 | 20/09/2026 | ChatGPT/Codex | Ghi nhận DOC-001 Completed sau khi Human merge PR #7 | Post-merge governance closeout, không đổi technical specification | DOC-001, ADR-009, REV-DOC-001, PR #7 | No |
| 0.2.7 | 0.3.0 | 20/09/2026 | ChatGPT/Codex | Phê duyệt SPEC-001 baseline và khóa FastAPI/upload scope để chuẩn bị APP-001 | Đồng bộ independent review và Human decisions | SPEC-001/002/003, ADR-001…005, APP-001, DEC-001/002/003 | No |
| 0.3.0 | 0.3.1 | 20/09/2026 | ChatGPT/Codex | Đồng bộ trạng thái APP-001 sau Gemini PASS và Human merge PR #10 | Post-merge governance closeout; không thay đổi requirement hoặc API contract đã duyệt | APP-001, REV-APP-001, PR #10, merge commit `0df4814ff1eb8cd576566ac3dd403131feca3759` | No |
| 0.3.1 | 0.3.2 | 21/09/2026 | ChatGPT/Codex | Đồng bộ trạng thái APP-002 sau remediation, Gemini targeted PASS và Human merge PR #12 | Post-merge governance closeout; không thay đổi requirement hoặc API contract đã duyệt | APP-002, REV-APP-002, PR #12, merge commit `4a001d116cbf002bdd42a9151efbf3f308fce3e6` | No |

## 3. Tổng quan

AI Intellectual Property Description Generator là nền tảng web hỗ trợ chuyển một bài báo nghiên cứu khoa học dạng PDF hoặc DOCX thành dữ liệu sáng chế có cấu trúc, bản dự thảo patent specification, câu hỏi bổ sung và bằng chứng truy vết về nguồn. Đầu ra chỉ phục vụ rà soát; Human hoặc chuyên gia sở hữu trí tuệ phải kiểm tra trước khi dùng cho bất kỳ mục đích pháp lý hoặc SHTT nào.

Cụm từ “mẫu B của USPTO” trong phạm vi dự án được hiểu là tham chiếu cấu trúc trình bày của patent specification trong các bằng sáng chế tiện ích có mã tài liệu B2, không phải tên một biểu mẫu chính thức của USPTO.

## 4. Bối cảnh bài toán

Bài báo nghiên cứu thường trình bày mục tiêu học thuật, phương pháp, thí nghiệm và kết quả nhưng không được tổ chức theo cấu trúc hồ sơ sáng chế. Việc chuyển đổi thủ công đòi hỏi người thực hiện nhận diện vấn đề kỹ thuật, giải pháp, thành phần hoặc bước thực hiện, hiệu quả kỹ thuật, phương án thực hiện và mối liên hệ giữa từng phát biểu với tài liệu nguồn. Quá trình này tốn thời gian và dễ phát sinh nội dung thiếu căn cứ nếu dùng AI không có cơ chế source grounding.

## 5. Problem Statement

Cần một workflow có kiểm soát để phân tích một bài báo nghiên cứu, chuẩn hóa thông tin kỹ thuật, chỉ ra dữ liệu còn thiếu, tạo bản dự thảo theo cấu trúc patent specification và giữ được đường dẫn bằng chứng đến tài liệu nguồn. Hệ thống phải phân biệt rõ fact, paraphrase, inference và missing; không được biến suy luận thành sự kiện có nguồn.

## 6. Business Objective

- Giảm công sức chuẩn bị bản nháp ban đầu từ bài báo nghiên cứu.
- Chuẩn hóa cách thu thập thông tin kỹ thuật trước khi chuyên gia SHTT rà soát.
- Tăng khả năng truy vết giữa nội dung dự thảo và tài liệu nguồn.
- Phát hiện sớm thông tin thiếu, mâu thuẫn và phát biểu chưa có căn cứ.
- Tạo đầu ra DOCX có thể chỉnh sửa để phục vụ vòng làm việc Human-in-the-loop.

Hệ thống không thay thế luật sư, đại diện sáng chế hoặc chuyên gia SHTT.

## 7. Mục tiêu hệ thống

1. Nhận một file PDF hoặc DOCX hợp lệ trong mỗi phiên xử lý MVP.
2. Trích xuất nội dung và bằng chứng nguồn có định vị.
3. Sinh Structured JSON tuân thủ schema có version.
4. Xác định vấn đề kỹ thuật, giải pháp, thành phần, bước, đặc trưng khác biệt tiềm năng, hiệu quả và dữ liệu thí nghiệm.
5. Phát hiện thông tin thiếu và tạo câu hỏi cho tác giả.
6. Sinh bản dự thảo patent specification và Abstract tối đa 150 từ; Claims nằm ngoài MVP hiện hành.
7. Cho phép Human rà soát, chỉnh sửa và theo dõi trạng thái từng phần.
8. Kiểm tra grounding và tính nhất quán trước khi xuất DOCX.

## 8. Phạm vi hệ thống

Phạm vi tổng thể gồm giao diện upload và review, API điều phối, xử lý tài liệu, gọi AI, validation Structured Output, quản lý phiên bản nội dung, kiểm tra grounding, tạo DOCX, xử lý lỗi, audit ở mức MVP và xóa dữ liệu theo quyền của người dùng.

## 9. Phạm vi MVP

- Một bài báo cho một hồ sơ xử lý.
- MVP/APP-001 đầu vào PDF có text hoặc DOCX, tối đa 10 MiB; PDF tối đa 50 trang; scanned PDF/OCR bị loại. Exact DOCX page count không được tuyên bố nếu chưa render.
- Kiểm tra file, phân tích AI, Structured JSON, grounding, missing information và author questions.
- Draft patent specification gồm các phần có căn cứ; phần thiếu gắn `[CẦN TÁC GIẢ XÁC NHẬN]`.
- Không tạo Claims/Draft Claims trong MVP hiện hành.
- Abstract không quá 150 từ.
- Giao diện Human review, chỉnh sửa và trạng thái phê duyệt từng section.
- Xuất DOCX bằng `docxtpl`.
- Lưu activity history đủ để biết ai hoặc tác nhân nào thực hiện hành động chính.
- Structured JSON và DOCX là đầu ra chính.
- PDF, báo cáo QA và claim–description–source mapping là `[CẦN XÁC NHẬN]` đối với MVP.

## 10. Ngoài phạm vi MVP

- Tự động nộp hồ sơ lên USPTO.
- Kết luận patentability, tính mới, trình độ sáng tạo hoặc khả năng được cấp bằng.
- Prior-art search toàn diện.
- Kết luận chính thức về inventor, inventorship, assignee hoặc quan hệ với đơn khác.
- Tư vấn pháp lý hoặc cam kết đầu ra sẵn sàng nộp.
- Fine-tuning model.
- Multi-agent runtime phức tạp.
- Hỗ trợ đầy đủ mọi loại hồ sơ SHTT và mọi khu vực pháp lý.
- Tạo dữ liệu kỹ thuật, kết quả thí nghiệm, hiệu quả hoặc biến thể không có căn cứ.
- Tự động phê duyệt nội dung thay Human.
- Claims/Draft Claims trong MVP hiện hành; mở lại cần scope-change approval riêng.

## 11. Stakeholder và đối tượng sử dụng

| Stakeholder | Nhu cầu chính | Trách nhiệm |
|---|---|---|
| Human / Product Owner | Sản phẩm đúng phạm vi, kiểm soát rủi ro và quyết định | Phê duyệt scope, kiến trúc chính, breaking change và đầu ra cuối |
| Tác giả/nghiên cứu viên | Chuyển nội dung nghiên cứu thành bản nháp có thể rà soát | Cung cấp tài liệu hợp lệ, trả lời câu hỏi còn thiếu, xác nhận kỹ thuật |
| Chuyên gia SHTT | Rà soát cấu trúc, claims, căn cứ và rủi ro | Đánh giá chuyên môn trước khi sử dụng pháp lý |
| ChatGPT/Codex | Triển khai và tích hợp | Lead Developer, System Architect, Integration Owner |
| Gemini Pro | Review độc lập | Research Analyst, QA Reviewer; không ghi đè artefact production |
| Quản trị vận hành `[CẦN XÁC NHẬN]` | Quản lý truy cập, vận hành và sự cố | Vai trò và quyền cụ thể `[CẦN XÁC NHẬN]` |

## 12. Actor

- **End User:** upload, xem kết quả, chỉnh sửa, xác nhận section và yêu cầu export.
- **Human Reviewer:** xác nhận nội dung kỹ thuật và trạng thái section.
- **System:** kiểm tra file, điều phối pipeline, validation, lưu version và export.
- **OpenAI Responses API:** tạo Structured Output và bản nháp theo prompt/schema có version.
- **ChatGPT/Codex:** xây dựng, bảo trì và xử lý review.
- **Gemini Pro:** review artefact và output được giao.

## 13. User journey

1. Người dùng đăng nhập theo cơ chế `[CẦN XÁC NHẬN]`.
2. Tạo hồ sơ và upload một PDF hoặc DOCX.
3. Hệ thống kiểm tra quyền, loại file, tính toàn vẹn và giới hạn kích thước `[CẦN XÁC NHẬN]`.
4. Hệ thống trích xuất nội dung, tạo định danh đoạn và evidence chunks.
5. AI tạo Structured JSON; backend validation schema và business rules.
6. Hệ thống hiển thị dữ liệu, nhãn nguồn, thông tin thiếu và câu hỏi tác giả.
7. Người dùng chỉnh sửa và xác nhận từng section.
8. Hệ thống tạo draft, chạy grounding/consistency checks và hiển thị cảnh báo.
9. Human phê duyệt phần đủ điều kiện hoặc trả về để sửa.
10. Hệ thống xuất DOCX kèm cảnh báo đây là bản dự thảo cần review chuyên môn.

## 14. Use case chính

### UC-001 — Upload và kiểm tra tài liệu

- **Actor:** End User.
- **Mục tiêu:** Tạo hồ sơ từ một PDF hoặc DOCX hợp lệ.
- **Tiền điều kiện:** APP-001 chỉ chạy local single-tenant bằng synthetic data; authentication cho production `[CẦN XÁC NHẬN]`.
- **Luồng chính:** Chọn một file → gửi multipart upload → backend kiểm tra size/MIME/signature/parser → tạo opaque document ID → lưu ephemeral cục bộ → trả safe metadata.
- **Luồng thay thế:** File trùng được xử lý theo quy tắc duplicate `[CẦN XÁC NHẬN]`.
- **Lỗi có thể xảy ra:** Sai/mismatch loại, file rỗng/hỏng/encrypted, PDF scanned hoặc trên 50 trang, DOCX unsafe package, vượt 10 MiB; malware scanning service không thuộc APP-001.
- **Kết quả:** Hồ sơ ở trạng thái sẵn sàng phân tích hoặc lỗi có hướng xử lý.
- **Acceptance criteria:** Không nhận file ngoài PDF/DOCX; không lộ file qua public URL; lỗi trả mã và thông điệp có correlation ID; không log toàn văn tài liệu.

### UC-002 — Phân tích và trích xuất có cấu trúc

- **Actor:** End User, System, OpenAI Responses API.
- **Mục tiêu:** Tạo Structured JSON có evidence và nhãn grounding.
- **Tiền điều kiện:** UC-001 thành công; prompt/schema version hợp lệ.
- **Luồng chính:** Parse → tạo evidence chunks → gọi AI → validate schema → normalize → lưu version.
- **Luồng thay thế:** Retry có kiểm soát khi timeout hoặc output sai schema; chính sách retry `[CẦN XÁC NHẬN]`.
- **Lỗi có thể xảy ra:** Không trích xuất được text, AI timeout, rate limit, output sai schema, không đủ căn cứ.
- **Kết quả:** Analysis version hoặc trạng thái lỗi; dữ liệu thiếu được đánh dấu.
- **Acceptance criteria:** Mọi trường quan trọng có evidence hoặc nhãn `INFERENCE`/`MISSING`; không chuyển `INFERENCE` thành `SOURCE_FACT`; output qua schema validation trước khi hiển thị là hợp lệ.

### UC-003 — Rà soát và bổ sung thông tin

- **Actor:** End User, Human Reviewer.
- **Mục tiêu:** Sửa dữ liệu, trả lời câu hỏi và xác nhận từng phần.
- **Tiền điều kiện:** Có analysis version.
- **Luồng chính:** Xem dữ liệu/evidence → chỉnh sửa → ghi lý do → lưu version → đặt section status.
- **Luồng thay thế:** Phần chưa đủ căn cứ giữ trạng thái cần xác nhận.
- **Lỗi có thể xảy ra:** Xung đột phiên bản, mất quyền, dữ liệu không hợp lệ.
- **Kết quả:** Analysis đã chỉnh sửa có lịch sử và attribution.
- **Acceptance criteria:** Không ghi đè im lặng; lưu người/tác nhân, thời điểm và phiên bản. Canonical Human confirmation/audit model `[CẦN XÁC NHẬN]` và không thuộc Output Schema v1.0.0.

### UC-004 — Tạo và kiểm tra bản dự thảo

- **Actor:** End User, System, OpenAI Responses API, Human Reviewer.
- **Mục tiêu:** Sinh patent specification draft có grounding.
- **Tiền điều kiện:** Có Structured JSON hợp lệ.
- **Luồng chính:** Tạo claim-free draft sections → tạo Abstract → validation grounding/consistency → Human review.
- **Luồng thay thế:** Phần không đủ dữ liệu được tạo với `[CẦN TÁC GIẢ XÁC NHẬN]` hoặc bỏ theo quy tắc template đã phê duyệt.
- **Lỗi có thể xảy ra:** Nội dung mới không có nguồn, thuật ngữ không nhất quán, AI timeout; Claims không được tạo trong MVP hiện hành.
- **Kết quả:** Draft version và validation report.
- **Acceptance criteria:** Abstract tối đa 150 từ; không sinh Claims; các phần bắt buộc không bị âm thầm bỏ qua; draft mang disclaimer rõ ràng.

### UC-005 — Xuất DOCX

- **Actor:** End User, System.
- **Mục tiêu:** Tải bản dự thảo có thể chỉnh sửa.
- **Tiền điều kiện:** Có draft version; điều kiện section approval trước export `[CẦN XÁC NHẬN]`.
- **Luồng chính:** Chọn version → kiểm tra trạng thái/cảnh báo → render `docxtpl` → kiểm tra file → cung cấp tải xuống có kiểm soát.
- **Luồng thay thế:** Cho phép export có watermark/cảnh báo khi chưa duyệt `[CẦN XÁC NHẬN]`.
- **Lỗi có thể xảy ra:** Template lỗi, thiếu dữ liệu, render thất bại, liên kết hết hạn.
- **Kết quả:** DOCX gắn version và audit event.
- **Acceptance criteria:** File mở được, đúng version, giữ nhãn cần xác nhận và không chứa trường kỹ thuật ngoài draft được chọn.

### UC-006 — Xóa hồ sơ và dữ liệu phát sinh

- **Actor:** End User có quyền, System.
- **Mục tiêu:** Xóa file nguồn và dữ liệu liên quan theo chính sách.
- **Tiền điều kiện:** Xác thực và authorization thành công.
- **Luồng chính:** Yêu cầu xóa → cảnh báo phạm vi → xác nhận → xóa/đánh dấu xóa → ghi audit event không chứa nội dung nhạy cảm.
- **Luồng thay thế:** Legal hold hoặc backup retention `[CẦN XÁC NHẬN]`.
- **Lỗi có thể xảy ra:** Không đủ quyền, xóa một phần, storage không khả dụng.
- **Kết quả:** Trạng thái xóa có thể kiểm chứng.
- **Acceptance criteria:** Không còn truy cập qua API; báo rõ phạm vi dữ liệu còn trong backup nếu có; không tuyên bố xóa hoàn toàn khi chưa xác minh.

## 15. Functional Requirements

Trạng thái `Draft — cần xác nhận` nghĩa là requirement được đề xuất trong đặc tả nhưng chưa được Human phê duyệt triển khai.

| ID | Tên | Mô tả | Actor | Input | Output | Priority | Dependency | Acceptance criteria | Trạng thái xác nhận |
|---|---|---|---|---|---|---|---|---|---|
| FR-001 | Upload PDF/DOCX | Nhận đúng một PDF có text hoặc DOCX cho local single-tenant APP-001 | End User | Multipart file | Safe document metadata | Must | ADR-001, APP-001 | Từ chối zero/multiple/unsupported file; không lộ local path | Implemented and verified in APP-001; merged via PR #10 |
| FR-002 | File validation | Xác minh extension, MIME, signature, parser readability, encryption và unsafe package content | System | File | Validation result | Must | FR-001 | File giả định dạng, hỏng, encrypted, scanned PDF hoặc unsafe DOCX bị từ chối | Implemented and verified in APP-001; merged via PR #10 |
| FR-003 | Kiểm tra giới hạn | Áp 10 MiB cho PDF/DOCX và 50 trang cho PDF | System | File bytes/pages | Pass/fail | Must | FR-001 | File `>10 MiB` hoặc PDF `>50` trang bị từ chối; DOCX exact pagination nằm ngoài APP-001 | Implemented and verified in APP-001; merged via PR #10 |
| FR-004 | Phân tích tài liệu | Điều phối deterministic parsing/evidence preparation rồi AI analysis | System | Valid document | Evidence envelope rồi analysis job/result | Must | FR-002, AI-002 | Parsing giữ source order, evidence IDs/locators; AI job có trạng thái, lỗi và correlation ID | APP-002 parsing/evidence preparation implemented and verified; AI runtime/orchestration remains Draft — cần xác nhận |
| FR-005 | Structured extraction | Sinh JSON theo schema có version | System, AI | Parsed content | Structured JSON | Must | FR-004, AI-001 | JSON hợp lệ theo đúng schema version | Draft — cần xác nhận |
| FR-006 | Trích xuất vấn đề kỹ thuật | Nhận diện vấn đề có evidence | AI, Human | Evidence chunks | Technical problems | Must | FR-005 | Mỗi mục có evidence hoặc nhãn phù hợp | Draft — cần xác nhận |
| FR-007 | Trích xuất giải pháp kỹ thuật | Nhận diện giải pháp và quan hệ với vấn đề | AI, Human | Evidence chunks | Technical solutions | Must | FR-005 | Không tạo giải pháp không có căn cứ | Draft — cần xác nhận |
| FR-008 | Trích xuất thành phần/bước | Chuẩn hóa component hoặc process step | AI, Human | Evidence chunks | Components/process steps | Must | FR-005 | Giữ thuật ngữ và thứ tự có nguồn | Draft — cần xác nhận |
| FR-009 | Đặc trưng khác biệt tiềm năng | Ghi nhận đặc trưng được bài báo hỗ trợ; không kết luận novelty | AI, Human | Analysis | Candidate features | Must | FR-005 | Có disclaimer và evidence | Draft — cần xác nhận |
| FR-010 | Hiệu quả kỹ thuật | Trích xuất effect có căn cứ | AI, Human | Evidence chunks | Technical effects | Must | FR-005 | Không suy diễn công dụng thành fact | Draft — cần xác nhận |
| FR-011 | Dữ liệu thí nghiệm | Trích bảng, điều kiện, số liệu có định vị nguồn | AI, Human | Tables/text | Experimental data | Must | FR-005 | Giá trị và đơn vị truy vết được | Draft — cần xác nhận |
| FR-012 | Phát hiện thông tin thiếu | So sánh dữ liệu với yêu cầu draft | System, AI | Structured JSON | Missing list | Must | FR-005 | Mục thiếu không được tự điền | Draft — cần xác nhận |
| FR-013 | Source evidence | Lưu file, trang, mục, đoạn, bảng/hình, excerpt và trạng thái | System, AI | Parsed content | Evidence records | Must | FR-004 | Nội dung quan trọng liên kết evidence khi có thể | Draft — cần xác nhận |
| FR-014 | Phân loại grounding | Output Schema v1.0.0 dùng `SOURCE_FACT`, `PARAPHRASE`, `INFERENCE`; dữ liệu thiếu dùng collection `missing_information` | System, AI | Content/evidence | Grounding label hoặc missing item | Must | FR-013 | Mọi grounding label có evidence; không tự nâng cấp `INFERENCE` | Human-approved for AI-001 contract |
| FR-015 | Câu hỏi tác giả | Tạo câu hỏi cụ thể cho dữ liệu thiếu/mơ hồ | AI, Human | Missing list | Author questions | Must | FR-012 | Câu hỏi gắn section và lý do | Draft — cần xác nhận |
| FR-016 | Draft generation | Tạo các section patent specification theo dữ liệu đã kiểm tra | System, AI | Structured JSON | Draft sections | Must | FR-005, FR-014 | Phần thiếu gắn nhãn xác nhận | Draft — cần xác nhận |
| FR-017 | Draft Claims | Tính năng tương lai; không thuộc MVP hiện hành | AI, Human | Validated analysis | Draft Claims | Won't for current MVP | Scope-change approval | Không endpoint/prompt/schema/runtime hiện hành nào được tạo Claims | Human decision: excluded from current MVP |
| FR-018 | Abstract | Tạo Abstract tối đa 150 từ | AI, Human | Draft | Abstract | Must | FR-016 | Bộ đếm xác nhận không quá 150 từ | Draft — cần xác nhận |
| FR-019 | Human review | Hiển thị content cùng evidence và cảnh báo | Human | Analysis/draft | Review decisions | Must | FR-013, FR-016 | Human có thể chấp nhận, trả sửa hoặc giữ cần xác nhận | Draft — cần xác nhận |
| FR-020 | Chỉnh sửa nội dung | Cho phép sửa field/section có attribution | Human | User edits | New content version | Must | FR-019 | Không ghi đè version trước | Draft — cần xác nhận |
| FR-021 | Section approval | Theo dõi trạng thái từng section | Human | Review action | Section status | Must | FR-019 | Danh sách trạng thái `[CẦN XÁC NHẬN]`; audit được lưu | Draft — cần xác nhận |
| FR-022 | DOCX generation | Render draft bằng template có version | System | Valid Patent Draft Contract v1.0.0 payload | DOCX | Must | FR-016, DOC-001 | File mở được, đúng version, disclaimer, fixed order và evidence appendix | Human-approved for DOC-001 template contract |
| FR-023 | Error handling | Trả lỗi nhất quán, không lộ dữ liệu | System | Failure | Error response | Must | API contract | Có error code, safe message, correlation ID | Draft — cần xác nhận |
| FR-024 | Version tracking | Quản lý version prompt, schema, template, analysis và draft | System | Artefact change | Version metadata | Must | Version policy | Xác định được artefact nào tạo mỗi output | Draft — cần xác nhận |
| FR-025 | Activity history | Ghi sự kiện upload, analyze, edit, approve, export, delete | System | User/system actions | Audit events | Must | Auth `[CẦN XÁC NHẬN]` | Có actor, action, time, object/version; không ghi toàn văn | Draft — cần xác nhận |
| FR-026 | Grounding validation | Kiểm tra nội dung draft với evidence | System, AI, Human | Draft/evidence | Validation results | Must | FR-013, FR-016 | Nội dung không nguồn bị cảnh báo; không tự coi là hợp lệ | Draft — cần xác nhận |
| FR-027 | Consistency validation | Phát hiện thuật ngữ, số liệu, mâu thuẫn và claim support | System, AI | Analysis/draft | Findings | Must | FR-016 | Finding có location, severity và trạng thái | Draft — cần xác nhận |
| FR-028 | Data deletion | Xóa hồ sơ và dữ liệu phát sinh theo quyền/chính sách | End User, System | Delete request | Deletion result | Must | Auth/storage policy | API không còn trả dữ liệu đã xóa; backup retention được công bố | Draft — cần xác nhận |

## 16. Non-functional Requirements

| ID | Mô tả | Chỉ số hoặc tiêu chí kiểm tra | Priority | Cách xác minh | Trạng thái xác nhận |
|---|---|---|---|---|---|
| NFR-001 | Security | Không có secret trong client/repository; authorization trên mọi tài nguyên | Must | Secret scan, API security test, code review | Draft — cần xác nhận |
| NFR-002 | Privacy | Không log toàn văn paper; chỉ truyền dữ liệu cho nhà cung cấp được phê duyệt | Must | Log inspection, data-flow review | Draft — cần xác nhận |
| NFR-003 | Confidentiality | File nguồn private và không có public URL ổn định | Must | Access-control test | Draft — cần xác nhận |
| NFR-004 | Traceability | Mỗi nội dung kỹ thuật quan trọng có evidence hoặc nhãn không có evidence | Must | Golden-set và manual audit | Draft — cần xác nhận |
| NFR-005 | Reliability | Job thất bại có trạng thái rõ, không tạo output thành công giả | Must | Failure injection; ngưỡng định lượng `[CẦN XÁC NHẬN]` | Draft — cần xác nhận |
| NFR-006 | Maintainability | Module, API, prompt, schema và template có version/tài liệu | Should | Repository review, tests | Draft — cần xác nhận |
| NFR-007 | Scalability | Kiến trúc không khóa khả năng tăng số job; mục tiêu tải `[CẦN XÁC NHẬN]` | Should | Load test sau khi xác nhận workload | Draft — cần xác nhận |
| NFR-008 | Performance | Thời gian upload/analyze/export mục tiêu `[CẦN XÁC NHẬN]` | Should | Performance test theo dữ liệu thực | Draft — cần xác nhận |
| NFR-009 | Logging | Log có level, correlation ID và redaction | Must | Automated log tests và review | Draft — cần xác nhận |
| NFR-010 | Monitoring | Theo dõi error rate, latency, job failure, provider error; ngưỡng cảnh báo `[CẦN XÁC NHẬN]` | Should | Dashboard/alert test khi triển khai | Draft — cần xác nhận |
| NFR-011 | Secret management | Secret chỉ ở backend environment/secret manager, có rotation process | Must | Deployment review và rotation drill | Draft — cần xác nhận |
| NFR-012 | Accessibility | Luồng chính dùng được bằng bàn phím, label rõ; chuẩn đích `[CẦN XÁC NHẬN]` | Should | Accessibility audit | Draft — cần xác nhận |
| NFR-013 | Data deletion | Có thể xóa file nguồn và derived data; thời hạn hoàn tất `[CẦN XÁC NHẬN]` | Must | Deletion end-to-end test | Draft — cần xác nhận |
| NFR-014 | Backup/recovery | Phạm vi, tần suất, RPO/RTO và retention `[CẦN XÁC NHẬN]` | Should | Restore drill sau khi chính sách được duyệt | Draft — cần xác nhận |
| NFR-015 | Version compatibility | Output lưu schema/prompt/template version và có strategy migration | Must | Compatibility/regression tests | Draft — cần xác nhận |
| NFR-016 | Data retention | Retention của source, output, log và backup `[CẦN XÁC NHẬN]` | Must | Policy review và automated expiry test | Draft — cần xác nhận |

## 17. Kiến trúc hệ thống

Luồng kiến trúc định hướng:

`Next.js → FastAPI → OpenAI Responses API → Structured Outputs → Validation → Draft generation → docxtpl → DOCX`

| Thành phần | Trách nhiệm |
|---|---|
| Next.js + TypeScript | Upload, trạng thái xử lý, review evidence/content, chỉnh sửa, section approval, export |
| FastAPI + Python | Authorization, API contract, orchestration, parsing, validation, versioning, audit, export |
| OpenAI Responses API | Extraction và draft generation theo prompt/schema được version hóa |
| Structured Outputs / JSON Schema | Ràng buộc hình dạng dữ liệu và kiểu dữ liệu |
| Validation layer | Schema, business rules, grounding, consistency và claim support checks |
| `docxtpl` | Render draft đã chọn bằng DOCX template có version |
| Private storage | Lưu file nguồn và export; lựa chọn cụ thể `[CẦN XÁC NHẬN]` |
| Supabase/PostgreSQL | Optional/MVP+ hoặc chỉ dùng khi Human phê duyệt; không mặc định đã chọn |
| Vercel | Frontend deployment theo định hướng, cấu hình `[CẦN XÁC NHẬN]` |
| Railway | Backend deployment theo định hướng, cấu hình `[CẦN XÁC NHẬN]` |

## 18. Data flow

| Dữ liệu | Nguồn | Xử lý | Đích | Quy tắc |
|---|---|---|---|---|
| File nguồn | User | Validation, private upload | Private storage | Không public, không commit, có delete path |
| Parsed content | Parser | Chuẩn hóa text/structure | Temporary/private processing store | Retention `[CẦN XÁC NHẬN]` |
| Evidence chunks | Parsed content | Gắn page/section/paragraph/table/figure IDs | Analysis store | Không làm mất định vị nguồn |
| Structured JSON | AI + validator | Schema/business validation | Versioned analysis | Ghi prompt/schema/model metadata phù hợp |
| Patent Draft Contract | Validated Structured JSON | Draft generation + schema/business validation | Versioned grounded draft | Nội dung thiếu giữ heading và `[AUTHOR CONFIRMATION REQUIRED]`; conflict không tự giải quyết |
| User edits | Human | Validate + version | Analysis/draft history | Attribution và không ghi đè im lặng |
| Export file | Selected draft | `docxtpl` render | Private download/storage | Gắn template/content version |
| Logs | Components | Redact | Logging platform `[CẦN XÁC NHẬN]` | Không chứa full paper, secret hoặc prompt payload nhạy cảm |
| Temporary data | Upload/pipeline | Dùng trong local job | Ephemeral local storage | APP-001 xóa ngay khi validation fail, sau downstream completion, hoặc muộn nhất sau 1 giờ; production policy cần approval riêng |

## 19. AI processing flow

1. **Ingestion:** xác nhận quyền, file metadata và checksum phù hợp.
2. **Parsing:** trích text, heading, bảng và hình tham chiếu; MVP từ chối scanned PDF và không OCR.
3. **Chunking/file retrieval:** giữ context và locator; chiến lược dùng OpenAI File Search hoặc chunking backend `[CẦN XÁC NHẬN]`.
4. **Extraction:** runtime tương lai gọi model bằng extraction prompt và schema version cụ thể; AI-002 mới chỉ kiểm tra canonical prompt contract offline.
5. **Normalization:** chuẩn hóa thuật ngữ, đơn vị và quan hệ nhưng không sửa giá trị nguồn.
6. **Validation:** kiểm tra schema, kiểu, business rules và tham chiếu evidence.
7. **Missing-information detection:** gắn `MISSING`, lý do và author question.
8. **Draft generation:** dùng Patent Draft Generation Contract v1.0.0; chỉ dùng dữ liệu đã phân loại, mọi technical paragraph có source path/evidence và inference phải hiển thị rõ.
9. **Grounding check:** so nội dung dự thảo với evidence; tạo finding cho unsupported content.
10. **Human review:** chỉnh sửa, xác nhận hoặc yêu cầu làm lại.
11. **Export:** render version đã chọn và lưu audit event.

Trạng thái triển khai hiện hành dừng tại `PDF/DOCX → APP-001 validation → APP-002 deterministic text/table parsing → source units/evidence IDs/locators → AI-002 Extraction Input Envelope`. APP-002 đã `Completed — Merged via PR #12` tại merge commit `4a001d116cbf002bdd42a9151efbf3f308fce3e6`. OpenAI Responses API, Structured Outputs provider adapter, model invocation, draft runtime integration, DOCX export API, frontend và end-to-end pipeline chưa được triển khai.

## 20. Structured Output concept

Contract đã triển khai cho AI-001 là JSON Schema Draft 2020-12 tại `schemas/invention-output/v1.0.0/invention-output.schema.json`. Version `1.0.0` chỉ bao phủ structured invention analysis, evidence, missing information và author questions. Claims, draft sections, validation results, Human approval/audit state và các kết luận pháp lý không thuộc contract này.

Mọi object trong v1.0.0 là strict (`additionalProperties: false`). Grounding object chỉ dùng `SOURCE_FACT`, `PARAPHRASE`, `INFERENCE`, và cả ba đều phải có ít nhất một `evidence_id`. `output_notice` bắt buộc thể hiện draft cần Human review, `is_legal_advice: false`, `filing_ready: false` và `includes_patentability_assessment: false`.

| Object | Mục đích và quan hệ chính |
|---|---|
| `document_metadata` | File ID, tên, loại, checksum, parser metadata và locator conventions |
| `title_candidates` | Danh sách tiêu đề đề xuất, rationale và evidence; không tự coi là tiêu đề đã duyệt |
| `technical_field` | Lĩnh vực kỹ thuật với grounding record |
| `background` | Bối cảnh từ paper; không biến thành prior-art search |
| `technical_problems` | Vấn đề và evidence; liên kết tới solutions/effects |
| `technical_solutions` | Giải pháp; liên kết components/process steps/problems |
| `components` | Thành phần, thuộc tính, quan hệ và evidence |
| `process_steps` | Bước, thứ tự, điều kiện và evidence |
| `potential_distinguishing_features` | Đặc trưng khác biệt tiềm năng, không phải kết luận novelty |
| `technical_effects` | Hiệu quả, điều kiện và mức grounding |
| `embodiments` | Phương án thực hiện có nguồn; biến thể thiếu nguồn không được tự tạo |
| `experimental_data` | Bảng/đo, điều kiện, giá trị, đơn vị và source locator |
| `drawing_requirements` | Hình có sẵn hoặc hình được đề nghị; hình mới cần Human xác nhận |
| `missing_information` | Field/section thiếu, lý do, impact và owner trả lời |
| `author_questions` | Câu hỏi liên kết tới missing item |
| `evidence` | Evidence ID, file, page, section, paragraph, table/figure, excerpt, type, status |
| `draft_sections` | Sáu technical sections có thứ tự, status `PRESENT`/`MISSING`, paragraphs, source paths và evidence IDs theo Patent Draft Contract v1.0.0 |
| `validation_results` | Rule, severity, location, evidence, trạng thái và resolution |

Nguyên tắc validation: JSON Schema kiểm tra shape, type, enum và constraint cục bộ. `uniqueItems` không bảo đảm uniqueness của logical ID bên trong object; ID uniqueness và cross-reference existence phải được kiểm tra bởi downstream business validation. Các quy tắc Abstract/claims/draft chỉ áp dụng cho artefact tương lai đã được phê duyệt, không thuộc Output Schema v1.0.0.

Extraction Prompt v1.0.0 được triển khai tại `prompts/extraction/v1.0.0/extraction-prompt.md`. Caller cung cấp JSON input envelope đã chuẩn hóa, document metadata và source units có evidence ID/type/locator; caller phải từ chối nội dung rỗng hoặc chỉ có khoảng trắng trước model invocation. Prompt dùng nguồn English/Vietnamese, giữ ngôn ngữ kỹ thuật chính và evidence excerpt nguyên văn. Claims và kết luận pháp lý không thuộc prompt này.

AI-002 chỉ bảo đảm canonical offline validation bằng fixtures synthetic. Canonical schema dùng keyword/conditional và optional properties không tương thích nguyên trạng với OpenAI Structured Outputs strict subset. Vì vậy AI-002 không sửa schema, không tạo provider-specific generation schema/adapter, không gọi model thật và không tuyên bố đã tích hợp Responses API. Adapter và live evaluation phải thuộc task runtime riêng được Human phê duyệt.

Patent Draft Generation Contract v1.0.0 được triển khai cho AI-003 tại `schemas/patent-draft/v1.0.0/patent-draft.schema.json`; canonical drafting prompt nằm tại `prompts/draft-generation/v1.0.0/draft-generation-prompt.md`. Contract nhận Output Schema v1.0.0 đã qua schema/business validation và tạo `PATENT_DESCRIPTION_DRAFT` bằng English. Caller/Human chọn một title candidate; prompt không tự tạo title mới. Abstract hỗ trợ `PRESENT`/`MISSING`, tối đa 150 từ theo NFKC và Unicode word-count rule.

Contract cố định 11 phần cho future DOCX, sáu technical draft sections và bảy subsection. Mỗi technical paragraph bắt buộc có JSON Pointer source paths tương đối với `source_analysis` và evidence IDs. Missing content giữ heading với `[AUTHOR CONFIRMATION REQUIRED]`; conflict có ít nhất hai evidence IDs, giữ `UNRESOLVED` và không tự chọn phía đúng. Evidence appendix chỉ chứa evidence thực sự được dùng và có reverse usage references.

AI-003 tách JSON Schema validation khỏi downstream business validation. Business rules kiểm tra logical-ID uniqueness, cross-reference existence, source-pointer resolution, paragraph ordering, Abstract word count, evidence closure/reverse usage và minimal legal-assertion patterns. Claims, Draft Claims, legal/patentability conclusions, Human approval state, DOCX rendering, provider adapter và live-model evaluation đều ngoài phạm vi AI-003. Human / Product Owner đã merge PR #5 tại `fb522bc5ecbb5ad66bab6226fa88ae51020cef52`; trạng thái artefact hiện tại là **Completed — Merged via PR #5**.

DOC-001 triển khai `templates/patent-docx/v1.0.0/patent-description-template.docx` và `tests/docx/render_patent_docx_v1.py`. Renderer validate payload bằng canonical Patent Draft Generation Contract v1.0.0 trước khi dùng `docxtpl` với automatic XML escaping. DOCX giữ exact eleven-part order, section headings khi thiếu, marker `[AUTHOR CONFIRMATION REQUIRED]`, conflict `UNRESOLVED`, explicit `INFERENCE`, author questions và evidence appendix. Template dùng A4, lề 2.54 cm, Times New Roman và notice Human review trong footer. Claims, legal/patentability conclusions, PDF, model/API calls và technical-image generation không thuộc DOC-001. Human Microsoft Word Visual QA, Gemini 3.1 Pro High independent review và targeted governance review đều `PASS`; không có finding hoặc required change; regression và DOCX tests đạt 85/85. Human / Product Owner đã merge PR #7 ngày 20/09/2026; implementation commit `d3f7c7d9596b77a39e9a56fcdf97c76cb972612a`, merge commit `d208a7925da844c5b43578bac8ebdbb1c5c6b5b8`. Trạng thái: **Completed — Merged via PR #7**.

## 21. API dự kiến

`GET /health` và local single-tenant `POST /api/documents` đã được triển khai và merge qua PR #10 trong phạm vi APP-001. APP-002 chỉ thêm internal document/evidence preparation và không thêm public parsing/analyze endpoint. Các endpoint còn lại trong bảng vẫn là contract đề xuất, chưa được khẳng định đã triển khai; authentication/authorization production vẫn `[CẦN XÁC NHẬN]`.

| Endpoint | Mục đích | Input | Output | Authentication | Error responses | Idempotency |
|---|---|---|---|---|---|---|
| `GET /health` | Health check tối thiểu | Không có | `{"status":"ok"}` | Không có trong local APP-001 | 500 | Safe/idempotent |
| `POST /api/documents` | Upload/tạo ephemeral document | Chính xác một multipart PDF/DOCX, tối đa 10 MiB | Safe metadata, validation status, PDF page count | Không có trong local APP-001; production `[CẦN XÁC NHẬN]` | 400, 413, 415, 422, 500 | Idempotency/checksum dedup ngoài APP-001 |
| `GET /api/documents/{id}` | Lấy metadata/trạng thái | Document ID | Document view | Required | 401, 403, 404, 500 | Safe/idempotent |
| `POST /api/documents/{id}/analyze` | Khởi chạy analysis | Document ID, prompt/schema version tùy chọn được phép | Job/status | Required | 400, 403, 404, 409, 422, 429, 500, 502, 504 | Idempotency key cần hỗ trợ |
| `GET /api/documents/{id}/analysis` | Lấy analysis version | Document ID, version query | Structured analysis | Required | 403, 404, 500 | Safe/idempotent |
| `PUT /api/documents/{id}/analysis` | Lưu chỉnh sửa analysis | Base version, patch/full payload `[CẦN XÁC NHẬN]` | New analysis version | Required | 400, 403, 404, 409, 422, 500 | Conditional on base version |
| `POST /api/documents/{id}/generate-draft` | Tạo draft | Analysis version, generation config được duyệt | Draft job/status | Required | 400, 403, 404, 409, 422, 429, 500, 502, 504 | Idempotency key cần hỗ trợ |
| `GET /api/documents/{id}/draft` | Lấy draft version | Document ID, version query | Draft sections | Required | 403, 404, 500 | Safe/idempotent |
| `PUT /api/documents/{id}/draft` | Lưu chỉnh sửa/trạng thái section | Base version, edits/status | New draft version | Required | 400, 403, 404, 409, 422, 500 | Conditional on base version |
| `POST /api/documents/{id}/validate` | Chạy grounding/consistency | Analysis/draft version, ruleset version | Validation results | Required | 400, 403, 404, 409, 422, 500, 502 | Idempotent theo input/ruleset version |
| `POST /api/documents/{id}/export` | Tạo DOCX | Draft/template version | Export metadata/download token | Required | 400, 403, 404, 409, 422, 500 | Idempotent theo version hoặc key `[CẦN XÁC NHẬN]` |
| `DELETE /api/documents/{id}` | Yêu cầu xóa | Document ID, confirmation | Deletion status | Required + delete permission | 401, 403, 404, 409, 500 | Repeated delete không phục hồi dữ liệu |

Mọi lỗi API phải có mã máy đọc được, thông điệp an toàn, correlation ID và chi tiết validation không chứa nội dung tài liệu nhạy cảm.

## 22. Error handling

| Tình huống | Hành vi yêu cầu |
|---|---|
| File không hợp lệ/hỏng | Từ chối trước AI; nêu lý do an toàn và cách chọn lại file |
| PDF không trích xuất được text | Không tiếp tục như thành công; MVP trả safe unsupported/no-text error và không OCR |
| Scanned PDF | APP-001 từ chối là unsupported/no text layer; không OCR |
| DOCX không đọc được | Từ chối hoặc yêu cầu file khác; không gửi bytes hỏng tới AI |
| AI timeout/rate limit | Job ở trạng thái retryable/failed; retry policy `[CẦN XÁC NHẬN]` |
| AI trả sai schema | Không publish output; validate, retry có giới hạn hoặc yêu cầu xử lý |
| Không đủ căn cứ | Trả `MISSING`/warning và author question, không bịa nội dung |
| Export DOCX thất bại | Không tạo link giả; giữ draft, ghi error event và cho thử lại |
| Mất kết nối | Client hiển thị trạng thái chưa xác định và kiểm tra lại job bằng ID |
| Không có quyền | Trả 401/403 mà không tiết lộ document có tồn tại hay không theo policy |
| File quá lớn | APP-001 trả 413 khi vượt 10 MiB, trước parser/AI processing |
| Lỗi không xác định | Trả generic message + correlation ID; chi tiết chỉ ở log đã redaction |

## 23. Logging và monitoring

- Được log: timestamp, correlation ID, actor ID dạng phù hợp, action, object ID, version, trạng thái job, latency, token/cost metadata không chứa payload, error code và provider request ID nếu an toàn.
- Không được log: API key, password/token, toàn văn paper, full parsed text, full AI prompt/response chứa dữ liệu nghiên cứu, signed URL, dữ liệu cá nhân không cần thiết.
- Level tối thiểu: `INFO`, `WARN`, `ERROR`; `DEBUG` trong production phải mặc định không chứa payload nhạy cảm.
- Audit event: upload, analysis started/completed/failed, edit, Human confirmation, section status, validation, export và deletion.
- Monitoring: API availability, job failure, provider error, schema failure, export failure, latency và chi phí; ngưỡng alert `[CẦN XÁC NHẬN]`.
- Retention period cho application log, audit log và provider metadata: `[CẦN XÁC NHẬN]`.

## 24. Security

- OpenAI API key chỉ ở FastAPI backend; không gửi sang Next.js client.
- Authentication/authorization model và tenant isolation: `[CẦN XÁC NHẬN]` trước khi triển khai dữ liệu thật.
- File nguồn và export ở private storage; download dùng kiểm tra quyền và URL hết hạn nếu áp dụng.
- Validation extension, MIME, magic bytes, parser isolation và tên file an toàn.
- APP-001 reject encrypted PDF/DOCX, PDF không có text layer, macro/embedded/external-relationship DOCX; original filename không bao giờ được dùng làm storage path.
- APP-001 local ephemeral storage chỉ dùng synthetic data; cleanup ngay khi lỗi, sau downstream completion hoặc TTL tối đa 1 giờ.
- APP-002 giữ nguyên APP-001 security boundary: verify SHA-256, parse dưới storage lease, registry chỉ giữ safe metadata, không network/model call và chỉ được xác minh bằng synthetic/offline tests.
- Malware scanning: `[CẦN XÁC NHẬN]`; nếu chưa có, không được tuyên bố file đã scan.
- Encryption in transit bắt buộc; encryption at rest và nhà cung cấp storage `[CẦN XÁC NHẬN]`.
- Có data deletion workflow; backup retention và legal hold `[CẦN XÁC NHẬN]`.
- Secret rotation, least privilege và tách môi trường development/staging/production.
- Dependency lock, vulnerability scanning và cập nhật có kiểm thử.
- Không commit confidential paper, sample chứa dữ liệu thật, `.env`, token hoặc generated document nhạy cảm.
- Chính sách dữ liệu của nhà cung cấp AI phải được Human kiểm tra và phê duyệt trước dữ liệu chưa công bố.

## 25. Testing strategy

| Loại test | Phạm vi | Bằng chứng mong đợi |
|---|---|---|
| Unit test | Parser helpers, validators, mapping, word count, redaction | Automated test results |
| Integration test | FastAPI với storage/AI adapter/docxtpl bằng test fixtures an toàn | CI result và logs không chứa fixture nhạy cảm |
| API test | Contract, authz, validation, idempotency, error shape | Contract test report |
| Schema validation | Valid/invalid output, enums, references, version | Deterministic test cases |
| DOCX generation | Required sections, labels, format, file integrity | Generated test DOCX mở được |
| Security test | Upload abuse, broken access control, secret scan, injection | Security findings/resolution |
| Regression test | Prompt/schema/template/code versions trên golden set | Comparison report |
| End-to-end test | Upload → analysis → review → validation → export → delete | Traceable run result |
| Manual acceptance | Human kiểm tra chất lượng, disclaimer, evidence và workflow | Signed acceptance result |

Không dùng bài báo mật làm fixture trong public CI. Test data và quyền sử dụng phải được xác minh.

## 26. AI evaluation strategy

| Tiêu chí | Cách đánh giá đề xuất |
|---|---|
| Hallucination | Tỷ lệ phát biểu kỹ thuật không có support; ngưỡng `[CẦN XÁC NHẬN]` |
| Completeness | Coverage của thông tin có trong nguồn so với annotation Human |
| Source grounding | Độ đúng locator và entailment giữa nội dung với evidence |
| Missing-information detection | Precision/recall trên danh sách thiếu do Human gán nhãn |
| Terminology consistency | Số mâu thuẫn thuật ngữ/đơn vị giữa sections |
| Internal consistency | Mâu thuẫn problem–solution–effect–experiment |
| Claim support | Tỷ lệ claim elements có description/evidence support |
| Regression | So sánh phiên bản prompt/schema/model trên cùng golden set |
| Human reviewer agreement | Mức đồng thuận giữa output và reviewer; cách đo `[CẦN XÁC NHẬN]` |

Đề xuất xây dựng golden set gồm tài liệu được cấp quyền, annotation và expected evidence. Hiện chưa có bằng chứng golden set đã tồn tại: `[FILE CHƯA TỒN TẠI]`. Kích thước, lĩnh vực, người gán nhãn và ngưỡng pass cần Human phê duyệt.

## 27. Traceability

Chuỗi truy vết bắt buộc:

`Requirement → Use case → API → Test case → Evidence → Acceptance result`

Mỗi requirement phải map tới ít nhất một use case và test; mỗi API contract có test; mỗi acceptance result tham chiếu commit/build/test run. Với nội dung AI, cần thêm chuỗi `Output field/draft sentence → Evidence ID → Source locator → Human status`.

## 28. Tiêu chí hoàn thành MVP

MVP chỉ đạt khi có bằng chứng cho toàn bộ tiêu chí sau:

- Luồng một PDF/DOCX hợp lệ đến Structured JSON và DOCX chạy end-to-end trong môi trường được phê duyệt.
- File invalid, corrupt, unauthorized và unsupported bị xử lý đúng.
- Structured JSON qua schema và business-rule validation.
- Nội dung kỹ thuật quan trọng có evidence hoặc nhãn `INFERENCE`/`MISSING` rõ ràng.
- Human có thể review, edit và xác nhận section mà không mất version cũ.
- Draft có các phần đã phê duyệt và Abstract tối đa 150 từ; không có Claims.
- Grounding/consistency validation phát hiện test cases unsupported và mâu thuẫn đã định nghĩa.
- DOCX mở được, đúng content/template version và giữ disclaimer/nhãn xác nhận.
- Security, deletion, secret scan và access-control acceptance tests đạt theo tiêu chí đã phê duyệt.
- Không còn finding CRITICAL/HIGH mở; finding được chấp nhận có quyết định Human.
- Tài liệu triển khai, vận hành và handover đủ để tái hiện bản build.

## 29. Roadmap

| Giai đoạn | Kết quả dự kiến | Điều kiện chuyển giai đoạn |
|---|---|---|
| Phase 1 — Specification and architecture | Đặc tả, context, AGENTS, ADR, schema/prompt/template proposal | Human phê duyệt phạm vi và quyết định còn mở |
| Phase 2 — Core pipeline | Upload, parse, extraction, validation và evidence mapping | Core tests đạt; grounding được review |
| Phase 3 — Draft generation and DOCX | Draft sections, claims scope đã chốt, review UI, DOCX | Template và export acceptance đạt |
| Phase 4 — Evaluation and stabilization | Golden set, regression, security, error handling | Không còn blocker release |
| Phase 5 — Deployment and handover | Vercel/Railway theo cấu hình duyệt, runbook, acceptance | Human phê duyệt release |
| Post-MVP | Các tính năng được quyết định sau MVP | Scope/chi phí/rủi ro được phê duyệt riêng |

Ngày hoàn thành từng phase: `[CẦN XÁC NHẬN]`. Mục tiêu hoàn thành nội bộ là 30/09/2026; ngày 01–02/10 dành cho buffer/test/handover; deadline bàn giao chính thức vẫn là 02/10/2026.

## 30. Rủi ro kỹ thuật

| Risk ID | Mô tả | Khả năng | Ảnh hưởng | Biện pháp giảm thiểu | Owner | Status |
|---|---|---|---|---|---|---|
| RISK-001 | AI tạo nội dung không có nguồn | Cao | Cao | Schema/evidence bắt buộc, grounding check, Human review | ChatGPT/Codex + Human | Open |
| RISK-002 | PDF phức tạp làm sai locator | Trung bình | Cao | Parser tests, page mapping, manual evidence preview | ChatGPT/Codex | Open |
| RISK-003 | Claim vượt support của description | Cao | Cao | Claim-element mapping, warning, chuyên gia SHTT review | Human / chuyên gia SHTT | Open |
| RISK-004 | Rò rỉ nghiên cứu chưa công bố | Trung bình | Critical | Private storage, access control, redaction, vendor policy review | Human / Product Owner | Open |
| RISK-005 | Schema/prompt thay đổi làm hỏng output cũ | Trung bình | Cao | Semantic version, compatibility tests, migration policy | ChatGPT/Codex | Open |
| RISK-006 | Deadline ngắn dẫn tới over-scope | Cao | Cao | Giữ luồng 1 paper, hoãn optional items, quyết định nhanh open questions | Human / Product Owner | Open |
| RISK-007 | Không có golden set đủ đại diện | Cao | Trung bình | Chọn tài liệu được cấp quyền, annotation protocol, review độc lập | Human + Gemini Pro | Open |
| RISK-008 | DOCX template không phản ánh yêu cầu chuyên môn | Trung bình | Cao | Template review với chuyên gia SHTT trước khóa version | Human / chuyên gia SHTT | Open |

## 31. Assumptions

- Repository `ai-ip-description-generator` được giữ private.
- Mỗi lần xử lý MVP có một bài báo PDF hoặc DOCX.
- Người dùng có quyền hợp pháp để cung cấp và xử lý tài liệu.
- Human/chuyên gia SHTT sẵn sàng review trước khi dùng đầu ra.
- OpenAI Responses API và Structured Outputs là production AI đã định hướng, nhưng model cụ thể `[CẦN XÁC NHẬN]`.
- Supabase/PostgreSQL chưa mặc định thuộc MVP nếu chưa được phê duyệt.
- Hai bằng sáng chế B2 là tài liệu tham chiếu cấu trúc, không phải “mẫu B” chính thức.

## 32. Dependencies

- Quyền sử dụng OpenAI API và chính sách dữ liệu phù hợp.
- Tài liệu nghiên cứu được cấp quyền và test fixtures không nhạy cảm.
- Quyết định storage, authentication/authorization và retention.
- Prompt, schema, API contract và DOCX template có version.
- Human/chuyên gia SHTT review cấu trúc draft; Claims tương lai cần scope-change approval riêng.
- Vercel/Railway account/config khi đến Phase 5.
- Google Drive/NotebookLM chỉ phục vụ phối hợp và research, không thay GitHub Technical Source of Truth.

## 33. Open questions

1. Cơ chế authentication, organization/tenant và vai trò người dùng production là gì?
2. Private production storage nào được dùng trước khi Supabase/PostgreSQL được phê duyệt?
3. Retention cho source, derived data, export, logs và backup production là bao lâu? APP-001 local TTL đã khóa tối đa 1 giờ.
6. Có malware scanning trong MVP không?
7. Model OpenAI, giới hạn chi phí, timeout và retry policy là gì?
8. Sử dụng File Search hay backend parsing/chunking cho từng loại tài liệu?
9. Nếu Human mở lại Claims sau MVP/scope change, số lượng, loại và cấu trúc được phép là gì?
10. Có bắt buộc mọi section được Human approve trước export không?
11. PDF, QA report và claim mapping có thuộc MVP không?
12. Bộ test/golden set dùng tài liệu nào, ai annotation và pass threshold là gì?

## 34. Các vấn đề cần Human xác nhận

| ID | Quyết định cần xác nhận | Ảnh hưởng nếu chưa quyết định | Người quyết định |
|---|---|---|---|
| HD-001 | Phê duyệt phạm vi MVP và ngoài phạm vi | Không thể khóa acceptance criteria | Human / Product Owner |
| HD-002 | OCR/scanned PDF | Human đã loại khỏi MVP/APP-001; chỉ mở lại qua scope-change approval riêng | Human / Product Owner |
| HD-003 | File size/page limits | Human đã chốt 10 MiB cho PDF/DOCX và 50 trang cho PDF; exact DOCX pagination hoãn sang parser/rendering task | Human / Product Owner |
| HD-004 | Auth, authorization và private storage | Chặn xử lý dữ liệu thật an toàn | Human / Product Owner |
| HD-005 | Retention/deletion/backup | Chặn phê duyệt privacy và vận hành | Human / Product Owner |
| HD-006 | Model, File Search/chunking, timeout, retry và cost limit | Chặn khóa AI architecture/runtime | Human / Product Owner |
| HD-007 | Phạm vi Draft Claims và người review chuyên môn | Human đã loại Claims khỏi MVP hiện hành; chỉ ảnh hưởng scope-change task tương lai | Human / chuyên gia SHTT |
| HD-008 | DOCX template và các section áp dụng | Đã được Human quyết định cho DOC-001 v1.0.0; Human Visual QA/Gemini reviews PASS; Completed — Merged via PR #7 | Human / chuyên gia SHTT |
| HD-009 | Optional PDF/QA/claim mapping | Ảnh hưởng workload trước deadline | Human / Product Owner |
| HD-010 | Golden set, metrics và threshold | Không thể kết luận chất lượng AI đạt | Human / Product Owner |
