# AI Intellectual Property Description Generator

Nền tảng AI hỗ trợ chuyển bài báo nghiên cứu khoa học thành dữ liệu sáng chế có cấu trúc và bản dự thảo patent specification để con người rà soát.

> **Trạng thái hiện tại:** Phase 1 — Specification & Architecture. Output Schema v1.0.0 có trạng thái **Completed — Merged via PR #1** ngày 19/09/2026 tại merge commit `49efead593437dfc5c88397ea6f335a2d4ff84d7`; frontend, backend và AI pipeline chưa được triển khai.
>
> **Deadline MVP:** 02/10/2026.

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
6. Tạo bản dự thảo patent specification, Draft Claims và Abstract.
7. Rà soát, chỉnh sửa và xác nhận từng phần bằng Human-in-the-loop.
8. Xuất DOCX có thể tiếp tục biên tập.

## 2. Input và Output

### Input

- Một scientific research paper dạng PDF hoặc DOCX.
- Scanned PDF/OCR: `[CẦN XÁC NHẬN]` đối với MVP.
- Chỉ sử dụng tài liệu mà người dùng có quyền hợp pháp để xử lý.

### Output chính

- Structured invention information dưới dạng JSON.
- Evidence mapping tới file, trang, mục, đoạn, bảng hoặc hình.
- Danh sách thông tin còn thiếu và câu hỏi cho tác giả.
- Draft patent specification.
- Draft Claims với số lượng và loại claim `[CẦN XÁC NHẬN]`.
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
- Draft patent specification, Draft Claims và Abstract.
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
- [x] System Specification 0.2.0.
- [x] AGENTS.md 0.1.1.
- [x] Project Context 0.2.2.
- [x] Project Control Center 0.2.2.
- [x] Gemini Review Log 0.2.1 với review entry `REV-AI-001` đã đóng.
- [x] Output Schema v1.0.0, fixtures và automated validation tests — Completed — Merged via PR #1; Gemini review `PASS`, 15/15 tests pass, không có finding.

### Chưa hoàn thành

- [ ] Human/Gemini review bộ tài liệu Draft.
- [ ] Extraction Prompt v1.
- [ ] DOCX Template v1.
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
| Phase 1 | Specification & Architecture | Đang review |
| Phase 2 | Core pipeline | Chưa bắt đầu |
| Phase 3 | Draft generation & DOCX | Chưa bắt đầu |
| Phase 4 | Evaluation & stabilization | Chưa bắt đầu |
| Phase 5 | Deployment & handover | Chưa bắt đầu |
| Post-MVP | Tính năng mở rộng được phê duyệt riêng | Chưa xác định |

## 14. Các quyết định cần Human xác nhận

- OCR/scanned PDF có thuộc MVP không.
- Giới hạn file và số trang.
- Authentication, authorization và private storage.
- Data/log/backup retention và deletion SLA.
- OpenAI model, retrieval, timeout, retry và cost limit.
- Loại và số lượng Draft Claims.
- PDF, QA report và claim mapping có thuộc MVP không.
- Golden set, evaluation metrics và pass threshold.

Danh sách chi tiết nằm trong [`docs/system-specification.md`](docs/system-specification.md).

## 15. Bắt đầu phát triển

Repository hiện chưa có application code. AI-001 chỉ bổ sung test dependency manifest tại `tests/requirements.txt`; hướng dẫn validation nằm tại `schemas/invention-output/v1.0.0/README.md`.

AI-001 đã `Completed` sau khi Human merge PR #1. Bước tiếp theo có thể là:

1. Chuẩn bị specification và approval package cho AI-002; AI-002 chưa bắt đầu.
2. Chỉ tạo `extraction-prompt-v1` sau khi task AI-002 được Human phê duyệt.
3. Tạo `patent-template-v1` theo task được phê duyệt riêng.
4. Khởi tạo FastAPI và Next.js theo task riêng.

## 16. License

Repository hiện chưa có file license: **[CẦN XÁC NHẬN]**.
