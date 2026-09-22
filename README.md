# AI Intellectual Property Description Generator

Nền tảng AI hỗ trợ chuyển bài báo nghiên cứu khoa học thành dữ liệu sáng chế có cấu trúc và bản dự thảo patent specification để con người rà soát.

> **Trạng thái hiện tại:** APP-001, APP-002, AI-RUNTIME-001 và AI-RUNTIME-002 đã hoàn tất; AI-RUNTIME-001 và AI-RUNTIME-002 là internal OpenAI Responses API extraction & draft runtimes đã merge qua PR #14 và PR #16. Runtimes dùng `gpt-5.6-sol`, reasoning high, `store=false`, strict provider schema, canonical post-validation và grounding/business validation. Live provider smoke ghi nhận `NOT RUN — DEFERRED due to unavailable API funding`; không có public analyze/draft endpoint và không được dùng dữ liệu nghiên cứu thật khi BLK-003 còn mở. Toàn bộ Phase 1, Phase 2, core pipeline end-to-end và MVP chưa được tuyên bố hoàn tất.
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
├── backend/                          # Upload, evidence preparation + internal extraction runtime
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
- [x] SPEC-001 System Specification 0.3.5 — Approved baseline; AI-RUNTIME-002 post-merge state đã đồng bộ.
- [x] SPEC-002 Project Context 0.3.5 — Approved baseline; AI-RUNTIME-002 post-merge state đã đồng bộ.
- [x] SPEC-003 AGENTS.md 0.2.0 — Approved baseline.
- [x] Project Control Center 0.3.5 và Gemini Review Log 0.3.4.
- [x] Gemini Review Log 0.3.4 với `REV-AI-RUNTIME-002` và các review task có bằng chứng đều `CLOSED`.
- [x] ADR-001…ADR-005 — Accepted theo Human decisions ngày 20/09/2026.
- [x] Output Schema v1.0.0, fixtures và automated validation tests — Completed — Merged via PR #1; Gemini review `PASS`, 15/15 tests pass, không có finding.
- [x] Extraction Prompt v1.0.0, ADR-007 và synthetic offline tests — Completed — Merged via PR #3; Gemini review `PASS`, AI-001 regression 15/15 và AI-002 tests 17/17 pass, không có finding; chưa tích hợp model/API thật.
- [x] Patent Draft Generation Contract v1.0.0, Draft Generation Prompt v1.0.0, ADR-008, synthetic fixtures và automated offline tests — Completed — Merged via PR #5; implementation commit `ae7e8fb573ea4681a9db1bafa711d19a3c598666`, merge commit `fb522bc5ecbb5ad66bab6226fa88ae51020cef52`, 57/57 tests pass và không có finding.
- [x] Patent DOCX Template v1.0.0, manifest, mapping, offline renderer, synthetic fixtures và automated tests — Completed — Merged via PR #7; implementation `d3f7c7d9596b77a39e9a56fcdf97c76cb972612a`, merge `d208a7925da844c5b43578bac8ebdbb1c5c6b5b8`; Human Visual QA và Gemini reviews `PASS`; 85/85 tests pass; không có finding.
- [x] APP-001 FastAPI skeleton và secure upload — Completed — Merged via PR #10; implementation head `bd39b9f7bdd9f7a1796d9a405e7998070e124e07`, merge `0df4814ff1eb8cd576566ac3dd403131feca3759`; Gemini review `PASS`, 22/22 acceptance criteria và 109/109 tests pass, không có finding.
- [x] APP-002 document parsing và evidence source units — Completed — Merged via PR #12; initial `477b8fda6afbae0049d8d691c213dc6355ba67da`, remediation `8b6f909a0f5787d72c002e163395656a666c9b78`, merge `4a001d116cbf002bdd42a9151efbf3f308fce3e6`; initial Gemini `REQUEST CHANGES`, F-001/F-002 `RESOLVED`, final `PASS`; 30/30 AC; 135 executed, 134 pass, 1 Windows skip, 0 failure/error.
- [x] AI-RUNTIME-001 — Completed — Merged via PR #14 tại `597f6c7b074eb2c5e445790b8c4f48f336f04da5`; implementation review `PASS WITH NON-BLOCKING NOTES`, F-001 `MEDIUM` resolved tại `5247cbcbe591d8b29917d9982b9066e393901c7e`, targeted remediation `PASS`, 32/32 AC và 201 executed / 200 pass / 1 skip.
- [x] AI-RUNTIME-002 — Completed — Merged via PR #16 tại `978516a4f5caa90bbd2189668237c6e028597361` (implementation head `a59ce0219d7039f24fa8c7bd71d4e9829dbbf612`); independent final review APPROVED, backend suite 240 pass (2 skip, 1 warning), tests/draft 25 pass; live provider smoke deferred.

### Chưa hoàn thành

- [ ] Next.js application.
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
| Phase 1 | Specification & Architecture | SPEC-001/002/003 approved baseline; chưa có tuyên bố Human hoàn tất toàn bộ phase |
| Phase 2 | Core pipeline | APP-001, APP-002, AI-RUNTIME-001 và AI-RUNTIME-002 đã merge; đặc tả APP-003 core pipeline orchestration đã remediate v1.1.0 và chờ independent re-review; chưa có public orchestration, DOCX integration endpoint, frontend hoặc end-to-end completion |
| Phase 3 | Draft generation & DOCX | AI-003 Completed — Merged via PR #5; DOC-001 Completed — Merged via PR #7 |
| Phase 4 | Evaluation & stabilization | Chưa bắt đầu |
| Phase 5 | Deployment & handover | Chưa bắt đầu |
| Post-MVP | Tính năng mở rộng được phê duyệt riêng | Chưa xác định |

## 14. Các quyết định cần Human xác nhận

- Authentication, authorization và private storage.
- Data/log/backup retention và deletion SLA production; APP-001 local ephemeral TTL đã khóa tối đa 1 giờ.
- Phạm vi Claims tương lai nếu Human mở lại bằng task/scope approval riêng.
- PDF, QA report và claim mapping có thuộc MVP không.
- Golden set, evaluation metrics và pass threshold.

Danh sách chi tiết nằm trong [`docs/system-specification.md`](docs/system-specification.md).

## 15. Bắt đầu phát triển

Repository hiện có APP-001 secure upload, APP-002 deterministic evidence preparation, AI-RUNTIME-001 internal extraction runtime và AI-RUNTIME-002 internal draft generation runtime. Phạm vi triển khai đạt `PDF/DOCX → validation → parsing → source units/evidence envelope → extraction Structured Output → canonical/grounding validation → validated analysis → draft envelope → draft Structured Output → canonical/business validation → validated Patent Description Draft JSON`. Public surface vẫn chỉ gồm `GET /health` và `POST /api/documents`; runtimes chưa được nối vào public endpoint.

AI-RUNTIME-002 đã `Completed — Merged via PR #16`. Đặc tả kỹ thuật APP-003 core pipeline orchestration và offline E2E harness v1.0.0 đã hoàn tất tại `docs/tasks/APP-003-core-pipeline-orchestration.md` và đang chờ independent review. Live provider smoke ghi nhận `NOT RUN — DEFERRED due to unavailable API funding`, BLK-003 vẫn mở và core E2E chưa hoàn tất. Không tự động triển khai public orchestration, DOCX integration endpoint, frontend, database/auth, production storage hoặc deployment.

## 16. License

Repository hiện chưa có file license: **[CẦN XÁC NHẬN]**.
