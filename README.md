# AI Intellectual Property Description Generator

Nền tảng AI hỗ trợ chuyển bài báo nghiên cứu khoa học thành dữ liệu sáng chế có cấu trúc và bản dự thảo patent specification để con người rà soát.

> **Trạng thái hiện tại:** APP-003 core pipeline, P0-005 frontend, P0-006 local integration và P0-007 synthetic/offline E2E validation đã merge; P0-007 đã CLOSED tại `8142692c6e92670b4b09996d733f93c409e93e49`. P0-008 đang chuẩn bị handover local/synthetic, chưa được independent implementation review hoặc Human chấp nhận. Normal processing dùng provider runtimes; chỉ E2E harness mới inject fake runtimes để chạy offline. Live-provider smoke **UNVALIDATED / DEFERRED**; BLK-003 **OPEN**. Không có phê duyệt production, public deployment hoặc dữ liệu nghiên cứu thật/bảo mật.
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
- Human review, chỉnh sửa, section status và immutable revision trong phiên trình duyệt hiện tại; chưa có durable audit/version store.
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
| Frontend deployment (proposed, unapproved) | Vercel — not deployed |
| Backend deployment (proposed, unapproved) | Railway — not deployed |
| Version control | GitHub |

Không tự ý thêm framework, dịch vụ hoặc dependency khi chưa giải thích và được Human phê duyệt.

## 8. Cấu trúc repository / Repository structure

Bản đồ Anh–Việt đầy đủ: [`FOLDER_STRUCTURE.md`](FOLDER_STRUCTURE.md).

> Giữ nguyên physical folder names tiếng Anh để không phá imports, tests, IDE/MCP config. Mỗi folder có tên hiển thị Anh / Việt và README nêu rõ nhiệm vụ.

| Path | English / Việt | Nhiệm vụ chính |
|---|---|---|
| `backend/` | Backend / Xử lý máy chủ | Upload, parsing, AI runtime, validation, grounding |
| `frontend/` | Frontend / Giao diện người dùng | Upload UI, progress, review/edit, export |
| `prompts/` | Prompts / Câu lệnh AI | Prompt production có version |
| `schemas/` | Schemas / Lược đồ dữ liệu | JSON Schema và data contracts |
| `templates/` | Templates / Mẫu tài liệu | DOCX template, manifest, mapping |
| `tests/` | Tests / Kiểm thử | Automated tests và synthetic fixtures |
| `docs/` | Documentation / Tài liệu dự án | Specification, ADR, task, operations, archive |
| `tools/` | Tools / Công cụ nội bộ | Project Orchestrator MCP và developer tooling |
| `.github/` | GitHub configuration / Cấu hình GitHub | PR template; chưa có offline CI workflow (P0-009) |

## 9. Tài liệu cần đọc

Đọc theo thứ tự:

1. [`AGENTS.md`](AGENTS.md) — vai trò, quyền hạn và quy tắc làm việc.
2. [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md) — bối cảnh dự án trong 3–5 phút.
3. [`docs/system-specification.md`](docs/system-specification.md) — requirement và kiến trúc chi tiết.
4. ADR trong `docs/decisions/` khi được tạo.
5. [`01_PROJECT_CONTROL_CENTER.md`](docs/operations/01_PROJECT_CONTROL_CENTER.md) — trạng thái và quyết định đang chờ.
6. [`02_GEMINI_REVIEW_LOG.md`](docs/operations/02_GEMINI_REVIEW_LOG.md) — lịch sử review hiện có; tên file legacy được giữ để truy vết, các review mới phải ghi rõ Antigravity reviewer và model profile thực tế.

## 10. Operating model / Phân chia vai trò

| Thành phần | Vai trò chính | Trách nhiệm và ranh giới |
|---|---|---|
| **Human / Product Owner** | **Governance & Final Approval Authority** | Quyết định scope, kiến trúc chính, security/data policy, provider/model policy, chi phí, release và output cuối; phê duyệt task/gate và quyết định merge `main`. |
| **ChatGPT** | **Technical Coordinator & Architecture Advisor** | Chuyển mục tiêu Human thành specification/prompt/handoff rõ ràng; đối chiếu bằng chứng, hỗ trợ kiến trúc, governance và điều phối giữa các agent; không tự thay Human phê duyệt hoặc release. |
| **Codex (VS Code)** | **Primary Implementation Agent** | Claim task đã được duyệt qua MCP; triển khai, test, debug, commit/push trên branch/worktree riêng; xử lý remediation; không tự approve review và không merge `main`. |
| **Antigravity Reviewer Agent** | **Independent Review & QA** | Review độc lập branch/commit cố định; kiểm tra acceptance criteria, regression, security/privacy, scope và chất lượng implementation; không sửa production artefact trong vai trò reviewer. **Exact model/profile dùng trong Antigravity phải được ghi trong từng review record, không hard-code tên model vào vai trò.** |
| **Project Orchestrator MCP** | **Coordination & State Management Layer** | Quản lý task queue/lifecycle, task lease, budget guard, checkpoint/handoff và trạng thái dùng chung giữa Codex/Antigravity; **không code, không review, không approve, không merge và không tự kích hoạt quota reset**. |
| **GitHub** | **Technical Source of Truth** | Lưu canonical source code, specification, prompt/schema/template, tests, ADR, PR/commit history và release evidence. |

### Separation of duties / Tách biệt trách nhiệm

```text
Human approves scope/task
        ↓
Codex implements + tests
        ↓
Antigravity performs independent review
        ↓
Codex remediates findings when required
        ↓
Human approves merge/release

Project Orchestrator MCP
= shared coordination/state layer across the workflow
```

**NotebookLM không còn thuộc toolchain hoặc workflow của dự án.** Các tham chiếu Gemini/NotebookLM trong changelog hoặc review history cũ chỉ là historical evidence và không mô tả operating model hiện tại.

## 11. Trạng thái hiện tại

### Đã có bằng chứng

- [x] Repository Private đã được khởi tạo.
- [x] Cấu trúc `frontend`, `backend`, `prompts`, `templates`, `tests` và `.github`.
- [x] SPEC-001 System Specification 0.3.7; SPEC-002 Project Context 0.4.7; SPEC-003 AGENTS.md 0.3.1 — approved technical/governance baselines with factual status updates.
- [x] Project Control Center 0.3.20 và Gemini Review Log 0.3.10 tại P0-008 implementation handoff; historical reviews remain intact.
- [x] ADR-001…ADR-005 — Accepted theo Human decisions ngày 20/09/2026.
- [x] Output Schema v1.0.0, fixtures và automated validation tests — Completed — Merged via PR #1; Gemini review `PASS`, 15/15 tests pass, không có finding.
- [x] Extraction Prompt v1.0.0, ADR-007 và synthetic offline tests — Completed — Merged via PR #3; Gemini review `PASS`, AI-001 regression 15/15 và AI-002 tests 17/17 pass, không có finding; chưa tích hợp model/API thật.
- [x] Patent Draft Generation Contract v1.0.0, Draft Generation Prompt v1.0.0, ADR-008, synthetic fixtures và automated offline tests — Completed — Merged via PR #5; implementation commit `ae7e8fb573ea4681a9db1bafa711d19a3c598666`, merge commit `fb522bc5ecbb5ad66bab6226fa88ae51020cef52`, 57/57 tests pass và không có finding.
- [x] Patent DOCX Template v1.0.0, manifest, mapping, offline renderer, synthetic fixtures và automated tests — Completed — Merged via PR #7; implementation `d3f7c7d9596b77a39e9a56fcdf97c76cb972612a`, merge `d208a7925da844c5b43578bac8ebdbb1c5c6b5b8`; Human Visual QA và Gemini reviews `PASS`; 85/85 tests pass; không có finding.
- [x] APP-001 FastAPI skeleton và secure upload — Completed — Merged via PR #10; implementation head `bd39b9f7bdd9f7a1796d9a405e7998070e124e07`, merge `0df4814ff1eb8cd576566ac3dd403131feca3759`; Gemini review `PASS`, 22/22 acceptance criteria và 109/109 tests pass, không có finding.
- [x] APP-002 document parsing và evidence source units — Completed — Merged via PR #12; initial `477b8fda6afbae0049d8d691c213dc6355ba67da`, remediation `8b6f909a0f5787d72c002e163395656a666c9b78`, merge `4a001d116cbf002bdd42a9151efbf3f308fce3e6`; initial Gemini `REQUEST CHANGES`, F-001/F-002 `RESOLVED`, final `PASS`; 30/30 AC; 135 executed, 134 pass, 1 Windows skip, 0 failure/error.
- [x] AI-RUNTIME-001 — Completed — Merged via PR #14 tại `597f6c7b074eb2c5e445790b8c4f48f336f04da5`; implementation review `PASS WITH NON-BLOCKING NOTES`, F-001 `MEDIUM` resolved tại `5247cbcbe591d8b29917d9982b9066e393901c7e`, targeted remediation `PASS`, 32/32 AC và 201 executed / 200 pass / 1 skip.
- [x] AI-RUNTIME-002 — Completed — Merged via PR #16 tại `978516a4f5caa90bbd2189668237c6e028597361` (implementation head `a59ce0219d7039f24fa8c7bd71d4e9829dbbf612`); independent final review APPROVED, backend suite 240 pass (2 skip, 1 warning), tests/draft 25 pass; live provider smoke deferred.
- [x] APP-003 core pipeline, P0-005 frontend MVP, P0-006 local integration và P0-007 synthetic/offline E2E validation đã merge. P0-007 closeout ở `8142692c6e92670b4b09996d733f93c409e93e49`.

### Chưa hoàn thành

- [ ] AI evaluation và golden set.
- [ ] Live-provider smoke; production auth/private storage/retention (BLK-003); public deployment.
- [ ] P0-008 independent implementation review và Human handover acceptance.

Local E2E được kiểm chứng bằng fake runtimes và synthetic fixtures; đây không phải xác nhận chất lượng AI trên paper thật.

## 12. Bảo mật và dữ liệu

- Không commit API key, password, token, `.env` thật hoặc signed URL.
- OpenAI API key chỉ được sử dụng ở backend.
- Không commit bài báo nghiên cứu chưa công bố hoặc output nhạy cảm.
- Không log toàn văn paper hoặc AI payload chứa dữ liệu mật.
- Source file và derived data phải ở private storage.
- Authentication, storage provider, retention, deletion và backup policy: `[CẦN XÁC NHẬN]`.
- Không dùng tài liệu để fine-tune hoặc tạo dataset nếu chưa được cho phép.

## 13. Roadmap

| Phase  | Nội dung | Trạng thái |
|---|---|---|
| Phase 1  | Specification & Architecture | SPEC-001/002/003 approved baseline; chưa có tuyên bố Human hoàn tất toàn bộ phase |
| Phase 2  | Core pipeline | APP-001/002/003 và AI-RUNTIME-001/002 đã merge; local orchestration API khi bật cờ, chưa có production auth/storage |
| Phase 3  | Draft generation & DOCX | AI-003 Completed — Merged via PR #5; DOC-001 Completed — Merged via PR #7 |
| Phase 4  | Evaluation & stabilization | P0-007 synthetic/offline stabilization đã merge; semantic evaluation/golden set là EVAL-001 tương lai |
| Phase 5  | Deployment & handover | P0-008 local/synthetic handover đang triển khai; deployment chưa được phê duyệt |
| Post-MVP  | Tính năng mở rộng được phê duyệt riêng | Chưa xác định |

## 14. Các quyết định cần Human xác nhận

- Authentication, authorization và private storage.
- Data/log/backup retention và deletion SLA production; APP-001 local ephemeral TTL đã khóa tối đa 1 giờ.
- Phạm vi Claims tương lai nếu Human mở lại bằng task/scope approval riêng.
- PDF, QA report và claim mapping có thuộc MVP không.
- Golden set, evaluation metrics và pass threshold.

Danh sách chi tiết nằm trong [`docs/system-specification.md`](docs/system-specification.md).

## 15. Local quickstart / Bắt đầu cục bộ

Run from repository root on Windows PowerShell with Python 3.12 and a Node/npm version compatible with the lockfile (P0-007 verified Node 24.18.0/npm 11.16.0; no exact Node pin is enforced):

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt -r tests/requirements.txt
cd frontend
npm ci
cd ..
```

Start normal backend (`.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000`) from root, then run `npm run dev -- --hostname 127.0.0.1` from `frontend/` in a second terminal for loopback-only access. Check `http://127.0.0.1:8000/health`, `http://127.0.0.1:3000` and `http://127.0.0.1:3000/backend/health`. Stop each controlled process with Ctrl+C. The normal process does **not** provide an offline full-processing demo; enabling local orchestration makes processing provider-dependent. Do not set a provider key for this local/synthetic handover.

For the full synthetic flow, use the isolated offline E2E harness and commands in the [authoritative MVP handover runbook](docs/operations/MVP_HANDOVER_RUNBOOK.md). It covers browser/DOCX smoke, tests, configuration, temporary-data limitations and evidence. Claims, OCR, prior-art search and patentability scoring remain outside MVP; outputs require Human/SHTT specialist review. P0-009 offline CI, EVAL-001 semantic evaluation, SEC-001 production security/BLK-003 and later UX hardening are separate work.

## 16. License

Repository hiện chưa có file license: **[CẦN XÁC NHẬN]**.
