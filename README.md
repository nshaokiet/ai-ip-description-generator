# AI Intellectual Property Description Generator

Nền tảng AI hỗ trợ chuyển bài báo nghiên cứu khoa học thành dữ liệu sáng chế có cấu trúc và bản dự thảo patent specification để con người rà soát.

> **Trạng thái hiện tại:** Phase 1 — Specification & Architecture. SPEC-001/002/003 là approved baseline; ADR-001…005 đã `Accepted`. AI-001, AI-002, AI-003 và DOC-001 đã merge. APP-001 specification đã được chuẩn bị và đang chờ Gemini review/Human approval; implementation chưa bắt đầu. Phase 1 chưa được tuyên bố hoàn tất và Phase 2 chưa bắt đầu.
>
> **Deadline MVP:** bàn giao chính thức 02/10/2026; mục tiêu hoàn thành nội bộ 30/09/2026, ngày 01–02/10 dành cho buffer/test/handover.

## Lưu ý quan trọng

Đầu ra của hệ thống chỉ là **bản dự thảo cần Human hoặc chuyên gia SHTT kiểm tra**. Hệ thống không tạo ra:

- Bằng sáng chế đã được cấp.
- Hồ sơ chắc chắn đủ điều kiện nộp hoặc được USPTO chấp thuận.
- Kết luận pháp lý về tính mới, trình độ sáng tạo hoặc patentability.
- Kết luận chính thức về inventorship.
- Tư vấn pháp lý.

Hai tài liệu tham chiếu `US11367264B2` và `US11044591B2` là bằng sáng chế có mã loại tài liệu B2; “mẫu B của USPTO” không phải tên một biểu mẫu chính thức.

## 1. Mục tiêu dự án

Xây dựng một nền tảng web cho phép người dùng:

1. Upload một bài báo nghiên cứu dạng PDF hoặc DOCX.
2. Phân tích và trích xuất thông tin kỹ thuật bằng AI.
3. Chuẩn hóa kết quả thành Structured JSON có version.
4. Liên kết nội dung quan trọng với bằng chứng trong tài liệu nguồn.
5. Phát hiện thông tin thiếu và tạo câu hỏi cho tác giả.
6. Tạo bản dự thảo patent specification và Abstract; Claims nằm ngoài MVP hiện hành.
7. Rà soát, chỉnh sửa và xác nhận từng phần bằng Human-in-the-loop.
8. Xuất DOCX có thể tiếp tục biên tập.

## 2. Input và Output

### Input

- Một scientific research paper dạng PDF hoặc DOCX.
- MVP/APP-001 chỉ nhận PDF có text hoặc DOCX tối đa 10 MiB; PDF tối đa 50 trang; scanned PDF/OCR bị loại. DOCX exact page count không được tuyên bố nếu chưa render.
- Chỉ sử dụng tài liệu mà người dùng có quyền hợp pháp để xử lý.

### Output chính

- Structured invention information dưới dạng JSON.
- Evidence mapping tới file, trang, mục, đoạn, bảng hoặc hình.
- Danh sách thông tin còn thiếu và câu hỏi cho tác giả.
- Draft patent specification.
- Draft Claims: ngoài MVP hiện hành; chỉ mở lại bằng scope-change approval riêng.
- Abstract tối đa 150 từ.
- DOCX có thể chỉnh sửa.

PDF, báo cáo QA và bảng claim–description–source mapping chỉ được đưa vào MVP khi Human phê duyệt.

## 3. Core Workflow

```text
Research paper
    ↓
Upload và file validation
    ↓
Document parsing / retrieval
    ↓
AI analysis và structured extraction
    ↓
Schema + source-grounding validation
    ↓
Missing-information detection
    ↓
Draft generation
    ↓
Human review và chỉnh sửa
    ↓
DOCX export
```

## 4. Nguyên tắc Source Grounding

Mỗi nội dung kỹ thuật quan trọng phải có evidence nếu xác định được. Hệ thống sử dụng các nhãn:

| Nhãn | Ý nghĩa |
|---|---|
| `SOURCE_FACT` | Có căn cứ trực tiếp trong tài liệu nguồn |
| `PARAPHRASE` | AI diễn đạt lại nội dung có căn cứ |
| `INFERENCE` | AI suy luận từ một hoặc nhiều nội dung |
| `MISSING` | Chưa tìm thấy căn cứ |
| `HUMAN_CONFIRMED` | Đã được người có thẩm quyền xác nhận |

Không được chuyển `INFERENCE` thành `SOURCE_FACT`. Nội dung chưa có căn cứ phải được đánh dấu `[CẦN TÁC GIẢ XÁC NHẬN]` thay vì tự điền.

Riêng Output Schema v1.0.0 chỉ chấp nhận `SOURCE_FACT`, `PARAPHRASE`, `INFERENCE`, và mỗi nhãn phải có ít nhất một evidence ID. `MISSING` được biểu diễn trong collection `missing_information`; `HUMAN_CONFIRMED` và audit state nằm ngoài contract v1.0.0.

## 5. Phạm vi MVP

### Trong phạm vi

- Một paper cho mỗi hồ sơ xử lý.
- Upload và kiểm tra PDF/DOCX.
- AI document analysis và Structured Output.
- Trích xuất vấn đề, giải pháp, thành phần, process steps, hiệu quả và dữ liệu thí nghiệm.
- Evidence mapping, missing-information detection và author questions.
- Draft patent specification và Abstract; không Claims.
- Human review, chỉnh sửa, section status và version tracking.
- Grounding/consistency validation.
- Xuất DOCX bằng `docxtpl`.

### Ngoài phạm vi

- Tự động nộp hồ sơ lên USPTO.
- Kết luận patentability, novelty hoặc inventive step.
- Prior-art search toàn diện.
- Kết luận chính thức về inventor, assignee hoặc inventorship.
- Fine-tuning trong MVP.
- Multi-agent runtime phức tạp.
- Cam kết đầu ra sẵn sàng nộp hoặc chắc chắn được cấp bằng.
- Claims/Draft Claims trong MVP hiện hành.

## 6. Kiến trúc định hướng

```text
Next.js + TypeScript
        ↓
FastAPI + Python
        ↓
OpenAI Responses API
        ↓
Structured Outputs / JSON Schema
        ↓
Validation + Grounding Check
        ↓
Draft Generation
        ↓
docxtpl → DOCX
```

Supabase/PostgreSQL chỉ thuộc MVP+ hoặc được sử dụng khi Human phê duyệt.

## 7. Tech Stack

| Lớp | Công nghệ |
|---|---|
| Frontend | Next.js + TypeScript |
| Backend | FastAPI + Python |
| Production AI | OpenAI Responses API |
| Structured data | Structured Outputs / JSON Schema |
| Retrieval | OpenAI File Search nếu cần và được phê duyệt |
| Database | Supabase/PostgreSQL — optional/MVP+ |
| Document generation | `docxtpl` |
| Frontend deployment | Vercel |
| Backend deployment | Railway |
| Version control | GitHub |

Không tự ý thêm framework, dịch vụ hoặc dependency khi chưa giải thích và được Human phê duyệt.

## 8. Cấu trúc repository

```text
ai-ip-description-generator/
├── AGENTS.md
├── PROJECT_CONTEXT.md
├── README.md
├── frontend/                         # Next.js — chưa khởi tạo mã ứng dụng
├── backend/                          # FastAPI — chưa khởi tạo mã ứng dụng
├── prompts/                          # Prompt có version
├── templates/                        # DOCX template có version
├── tests/                            # Test cases và AI evaluation
├── schemas/                          # JSON Schema production có version
├── docs/
│   ├── system-specification.md       # Đặc tả hệ thống đầy đủ
│   ├── architecture.md               # Ghi chú kiến trúc ban đầu
│   ├── workflow.md                   # Ghi chú workflow ban đầu
│   ├── decisions/                    # Architecture Decision Records
│   ├── tasks/                        # Task specification và acceptance criteria
│   ├── operations/
│   │   ├── 01_PROJECT_CONTROL_CENTER.md
│   │   └── 02_GEMINI_REVIEW_LOG.md
│   └── archive/                      # Snapshot tài liệu cũ được bảo toàn
├── .github/
├── .env.example
└── .gitignore
```

## 9. Tài liệu cần đọc

Đọc theo thứ tự:

1. [`AGENTS.md`](AGENTS.md) — vai trò, quyền hạn và quy tắc làm việc.
2. [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md) — bối cảnh dự án trong 3–5 phút.
3. [`docs/system-specification.md`](docs/system-specification.md) — requirement và kiến trúc chi tiết.
4. ADR trong `docs/decisions/` khi được tạo.
5. [`01_PROJECT_CONTROL_CENTER.md`](docs/operations/01_PROJECT_CONTROL_CENTER.md) — trạng thái và quyết định đang chờ.
6. [`02_GEMINI_REVIEW_LOG.md`](docs/operations/02_GEMINI_REVIEW_LOG.md) — review findings và resolution.

## 10. Phân chia vai trò

| Vai trò | Trách nhiệm chính |
|---|---|
| Human / Product Owner | Quyết định scope, kiến trúc chính, dữ liệu, release và output cuối |
| ChatGPT/Codex | Lead Developer, System Architect, Integration Owner |
| Gemini Pro | Research Analyst, Independent Reviewer, QA Reviewer |
| NotebookLM | Research Workspace; không phải production AI hoặc Source of Truth |

GitHub là **Technical Source of Truth**. Gemini không ghi đè production artefact; ChatGPT/Codex không tự phê duyệt quyết định thuộc quyền Human.

## 11. Trạng thái hiện tại

### Đã có bằng chứng

- [x] Repository Private đã được khởi tạo.
- [x] Cấu trúc `frontend`, `backend`, `prompts`, `templates`, `tests` và `.github`.
- [x] SPEC-001 System Specification 0.3.0 — Approved baseline.
- [x] SPEC-002 Project Context 0.3.0 — Approved baseline.
- [x] SPEC-003 AGENTS.md 0.2.0 — Approved baseline.
- [x] Project Control Center 0.3.0.
- [x] Gemini Review Log 0.3.0 với `REV-001`, `REV-002`, `REV-003` và các review task có bằng chứng đều `CLOSED`.
- [x] ADR-001…ADR-005 — Accepted theo Human decisions ngày 20/09/2026.
- [x] Output Schema v1.0.0, fixtures và automated validation tests — Completed — Merged via PR #1; Gemini review `PASS`, 15/15 tests pass, không có finding.
- [x] Extraction Prompt v1.0.0, ADR-007 và synthetic offline tests — Completed — Merged via PR #3; Gemini review `PASS`, AI-001 regression 15/15 và AI-002 tests 17/17 pass, không có finding; chưa tích hợp model/API thật.
- [x] Patent Draft Generation Contract v1.0.0, Draft Generation Prompt v1.0.0, ADR-008, synthetic fixtures và automated offline tests — Completed — Merged via PR #5; implementation commit `ae7e8fb573ea4681a9db1bafa711d19a3c598666`, merge commit `fb522bc5ecbb5ad66bab6226fa88ae51020cef52`, 57/57 tests pass và không có finding.
- [x] Patent DOCX Template v1.0.0, manifest, mapping, offline renderer, synthetic fixtures và automated tests — Completed — Merged via PR #7; implementation `d3f7c7d9596b77a39e9a56fcdf97c76cb972612a`, merge `d208a7925da844c5b43578bac8ebdbb1c5c6b5b8`; Human Visual QA và Gemini reviews `PASS`; 85/85 tests pass; không có finding.

### Chưa hoàn thành

- [ ] Gemini review và Human approval gói APP-001 specification.
- [ ] APP-001 FastAPI skeleton/secure upload implementation.
- [ ] Next.js application.
- [ ] FastAPI application.
- [ ] Core pipeline end-to-end.
- [ ] AI evaluation và golden set.
- [ ] Deployment Vercel/Railway.

Không đánh dấu application đã hoạt động khi mới chỉ có folder/README placeholder.

## 12. Bảo mật và dữ liệu

- Không commit API key, password, token, `.env` thật hoặc signed URL.
- OpenAI API key chỉ được sử dụng ở backend.
- Không commit bài báo nghiên cứu chưa công bố hoặc output nhạy cảm.
- Không log toàn văn paper hoặc AI payload chứa dữ liệu mật.
- Source file và derived data phải ở private storage.
- Authentication, storage provider, retention, deletion và backup policy: `[CẦN XÁC NHẬN]`.
- Không dùng tài liệu để fine-tune hoặc tạo dataset nếu chưa được cho phép.

## 13. Roadmap

| Phase | Nội dung | Trạng thái |
|---|---|---|
| Phase 1 | Specification & Architecture | SPEC-001/002/003 approved baseline; APP-001 spec chờ review/approval; chưa hoàn tất phase |
| Phase 2 | Core pipeline | Chưa bắt đầu; APP-001 implementation chưa được phê duyệt |
| Phase 3 | Draft generation & DOCX | AI-003 Completed — Merged via PR #5; DOC-001 Completed — Merged via PR #7 |
| Phase 4 | Evaluation & stabilization | Chưa bắt đầu |
| Phase 5 | Deployment & handover | Chưa bắt đầu |
| Post-MVP | Tính năng mở rộng được phê duyệt riêng | Chưa xác định |

## 14. Các quyết định cần Human xác nhận

- Authentication, authorization và private storage.
- Data/log/backup retention và deletion SLA production; APP-001 local ephemeral TTL đã khóa tối đa 1 giờ.
- OpenAI model, retrieval, timeout, retry và cost limit.
- Phạm vi Claims tương lai nếu Human mở lại bằng task/scope approval riêng.
- PDF, QA report và claim mapping có thuộc MVP không.
- Golden set, evaluation metrics và pass threshold.

Danh sách chi tiết nằm trong [`docs/system-specification.md`](docs/system-specification.md).

## 15. Bắt đầu phát triển

Repository hiện chưa có application code. AI-001 bổ sung test dependency manifest tại `tests/requirements.txt`; AI-002 và AI-003 dùng lại dependency đó cho validation offline và không gọi OpenAI API.

AI-001 đã `Completed` sau khi Human merge PR #1. AI-002 đã `Completed — Merged via PR #3`. AI-003 đã `Completed — Merged via PR #5` ngày 20/09/2026 tại merge commit `fb522bc5ecbb5ad66bab6226fa88ae51020cef52`. Bước tiếp theo:

1. Gemini review APP-001 specification và các ADR/baseline updates.
2. Human phê duyệt hoặc yêu cầu sửa APP-001; chỉ sau approval riêng mới được khởi tạo FastAPI/upload implementation.
3. Provider adapter, OpenAI runtime, Next.js, database và deployment vẫn cần task/approval riêng.

## 16. License

Repository hiện chưa có file license: **[CẦN XÁC NHẬN]**.
