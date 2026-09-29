# AI Intellectual Property Description Generator

Evidence-grounded patent-description drafting support for research teams.

Công cụ hỗ trợ chuyển bài báo khoa học thành dữ liệu có cấu trúc và bản mô tả sáng chế để rà soát thủ công.

## Project status

| Task | Trạng thái | Chức năng |
| --- | --- | --- |
| **SPEC-001/002/003** | ✅ Completed | Xác định yêu cầu hệ thống, kiến trúc tổng thể, bối cảnh dự án và quy tắc phối hợp giữa Human, Codex và Gemini |
| **AI-001** | ✅ Completed | Xây dựng schema chuẩn để biểu diễn thông tin sáng chế dưới dạng dữ liệu có cấu trúc |
| **AI-002** | ✅ Completed | Xây dựng prompt trích xuất thông tin kỹ thuật từ bài báo khoa học |
| **AI-003** | ✅ Completed | Xây dựng contract và prompt để tạo Patent Description Draft |
| **DOC-001** | ✅ Completed | Xây dựng template và bộ render để xuất bản mô tả sáng chế sang file DOCX |
| **APP-001** | ✅ Completed | Xây dựng backend nhận file PDF/DOCX, kiểm tra loại file, dung lượng và xử lý file an toàn |
| **APP-002** | ✅ Completed | Phân tích PDF/DOCX thành văn bản, source units, evidence IDs và source locators để truy vết nguồn |
| **AI-RUNTIME-001** | ✅ Completed | Thực thi quá trình trích xuất bằng OpenAI Responses API để chuyển bài báo thành Structured Invention Analysis |
| **AI-RUNTIME-002** | ✅ Completed | Thực thi quá trình tạo bản mô tả sáng chế từ Structured Invention Analysis thành Patent Description Draft |
| **APP-003** | ✅ Completed | Kết nối các thành phần thành core pipeline hoàn chỉnh và xây dựng offline E2E harness |
| **P0-005** | ✅ Completed | Xây dựng frontend MVP gồm tải tài liệu, theo dõi workflow và xem kết quả |
| **P0-006** | ✅ Completed | Kết nối frontend với FastAPI backend để vận hành luồng xử lý hoàn chỉnh |
| **P0-007** | ✅ Completed | Kiểm thử toàn bộ luồng E2E, xử lý lỗi tích hợp và ổn định hệ thống |
| **P0-008** | ✅ Completed | Kiểm tra mức độ sẵn sàng bàn giao của phiên bản local/synthetic MVP |
| **P0-009** | ✅ Completed | Thiết lập GitHub Actions CI để tự động kiểm tra backend, frontend và Playwright |
| **EVAL-001 Framework + Gold** | ✅ Completed (framework/gold) | Xây dựng bộ đánh giá chất lượng ngữ nghĩa, corpus/gold chuẩn và tiêu chí đo precision, coverage và grounding |
| **P0-010** | ✅ Completed | Hoàn tất MVP closeout và xác nhận trạng thái `MVP COMPLETE — LOCAL/SYNTHETIC` |
| **P1-001** | ✅ Completed | Cải thiện accessibility, điều hướng bàn phím, focus, TypeScript typecheck và tăng cường CI |
| **Project Orchestrator MCP** | ✅ Completed | Quản lý task state, owner, lease, quota, checkpoint và handoff giữa các agent |
| **P1 Task Catalog** | ✅ Completed | Đăng ký P1-001 đến P1-006 trong MCP và bảo toàn trạng thái task qua restart |
| **P1-002** | ✅ Completed | Mở rộng kiểm thử đối kháng offline để phát hiện edge case, input lỗi, dữ liệu không hợp lệ và lỗi validation |
| **P1-003** | 🟡 Incomplete — Planned | Tăng cường bảo mật môi trường local gồm upload safety, path handling, kiểm soát thông tin lỗi và rà soát attack surface |
| **P1-004** | 🟡 Incomplete — Planned | Đơn giản hóa việc chạy dự án theo hướng one-command local run cho frontend, backend và health check |
| **P1-005** | 🟡 Incomplete — Planned | Xây dựng performance baseline cho upload, parsing, validation, DOCX rendering và luồng trình duyệt |
| **P1-006** | 🟡 Incomplete — Planned | Hoàn thiện trải nghiệm người dùng gồm responsive, loading state, error state, retry/recovery và workflow clarity |
| **DEPLOY-001** | 🟡 Incomplete — Planned | Triển khai demo/staging không tốn phí để tạo public HTTPS URL cho người khác truy cập bằng synthetic/demo data |
| **EVAL-001 PRODUCT_RUNTIME** | ⏸ Incomplete — Deferred | Chạy benchmark trên provider/runtime thực tế để đánh giá chất lượng ngữ nghĩa của kết quả AI; đang chờ funding |
| **SEC-001 / BLK-003** | 🔴 Incomplete — Open | Hoàn thiện bảo mật production gồm authentication, tenant isolation, private storage, retention và deletion policy |
| **Production Deployment** | 🔴 Incomplete — Not approved | Triển khai production cho người dùng thật và dữ liệu thật sau khi hoàn tất các yêu cầu bảo mật, dữ liệu và vận hành |

**Current classification:** `MVP COMPLETE — LOCAL/SYNTHETIC`. Public demo URL is not available yet; it is planned under DEPLOY-001. Production deployment and real/confidential-data use remain unauthorized while BLK-003 is open.

> **README status-sync rule:** Bảng trên là bản tóm tắt trạng thái công khai của roadmap. Mỗi khi một task chuyển trạng thái (đặc biệt khi hoàn thành/merge, bị defer hoặc mở blocker), task closeout phải cập nhật đúng dòng tương ứng trong bảng này trong cùng thay đổi governance/closeout. Evidence chi tiết vẫn nằm trong Git history, task record và Project Control Center.

## Overview

The application helps researchers, innovation teams, and IP/patent drafting support
teams turn one text-based scientific PDF or DOCX into structured invention
information, source-linked evidence, a patent-description draft, and an editable
DOCX. It highlights missing information for the author and keeps review with people.

This is **drafting support, not legal advice**. Generated content requires
Human or IP-specialist review before any use. The current validated end-to-end
path is local and synthetic; it does not establish real-paper accuracy or
production readiness.

## Key capabilities

- PDF/DOCX upload with file validation and safe local handling.
- Deterministic parsing into ordered source and evidence units.
- Structured invention extraction with source/evidence grounding.
- Missing-information detection and questions for the author.
- Patent-description draft generation, with no Claims in the current MVP.
- Human review, prose editing, and immutable revisions within one browser session.
- Backend validation of the selected draft before export.
- Editable DOCX export of the exact validated revision.

**Claims are outside the current MVP.** Browser edits and review markers are
session-only, not a durable audit trail or formal approval.

## End-to-end workflow

```text
Scientific Paper (PDF/DOCX)
          ↓
Upload & Validation
          ↓
Parsing & Evidence Units
          ↓
Structured Extraction
          ↓
Grounding & Validation
          ↓
Missing Information
          ↓
Draft Generation
          ↓
Human Review
          ↓
DOCX Export
```

## Architecture

```text
Browser
   ↓
Next.js / TypeScript
   ↓  same-origin /backend/* proxy
FastAPI / Python
   ↓
OpenAI Responses API
   ↓
Validation / Grounding
   ↓
DOCX Renderer
```

The **normal application path** uses provider-backed extraction and drafting when
local orchestration is enabled; starting the servers does not make processing
offline. The **offline/synthetic test path** injects fake extraction/draft runtimes
while exercising the actual browser, HTTP, upload, parsing, validation, and DOCX
boundaries. Fake output does not establish live-model or semantic quality. See the
[MVP handover runbook](docs/operations/MVP_HANDOVER_RUNBOOK.md).

## Tech stack

| Layer | Technology |
| --- | --- |
| Frontend | Next.js 16, React, TypeScript |
| Backend | FastAPI, Python 3.12 |
| Provider-backed AI | OpenAI Responses API |
| Validation | JSON Schema and deterministic grounding/business rules |
| Document generation | `docxtpl`, `python-docx` |
| Testing | pytest, unittest, Playwright, ESLint |
| Version control | GitHub |

No database or deployment platform is active infrastructure in this local
baseline. P0-009 CI covers deterministic local/synthetic regression only.

## Quick start

Use Windows PowerShell from the repository root. Python 3.12 and compatible Node/npm
are required; the repository does not pin an exact Node/npm pair.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt -r tests/requirements.txt
cd frontend
npm ci
cd ..
```

If `py -3.12` cannot locate an installed Python 3.12, invoke that trusted
interpreter's `python.exe -m venv .venv` directly. The backend reads process
environment variables; it does not automatically load `.env.example`.

Start the backend from the repository root in one terminal:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

Start the frontend from `frontend/` in another terminal, bound to loopback:

```powershell
cd frontend
npm run dev -- --hostname 127.0.0.1
```

Check the [frontend](http://127.0.0.1:3000),
[backend health](http://127.0.0.1:8000/health), and
[frontend-to-backend proxy](http://127.0.0.1:3000/backend/health).
Next.js rewrites `/backend/*` using server-side `BACKEND_URL` (default
`http://127.0.0.1:8000`). Stop both controlled servers with Ctrl+C. For the
isolated synthetic full-flow setup and environment-variable matrix, follow
the [runbook](docs/operations/MVP_HANDOVER_RUNBOOK.md); do not supply a
provider key or real/confidential paper for this handover.

## Testing

From the repository root, run the offline backend regression with the local
virtual environment:

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q -p no:cacheprovider
```

From `frontend/`, install Playwright Chromium once, then run:

```powershell
npx playwright install chromium
npm run lint
npm run build
npm run test:e2e
```

The active [CI workflow](.github/workflows/ci.yml) runs on pull requests targeting
`main` and pushes to `main`: Python 3.12 full pytest, Node 24.18.0 `npm ci`,
lint, build, Playwright Chromium, and synthetic E2E. The final P0-010 post-merge
[main run](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/36526457334)
passed on merge SHA `9f31dae104438a598b0fe3c9bd09aba005f9026c` (backend **408 passed / 2 skipped**, lint/build PASS, Playwright
**11 passed**, live-test flags 0/0). P0-010 local offline verification: backend **407 passed / 3 skipped**
on Windows, lint/build PASS, Playwright **11 passed**. **Historical P0-007 evidence:** offline backend
**380 passed / 3 skipped**; Playwright **11 passed**. P0-008's fresh PDF-to-DOCX smoke and
environment details are in the runbook. CI does not validate a live provider
or real-paper semantic quality.

## Repository structure

```text
backend/    FastAPI routes, parsing, orchestration, validation
frontend/   Next.js UI and Playwright browser tests
prompts/    Versioned extraction and drafting prompts
schemas/    Structured JSON contracts
templates/  Patent-description DOCX template
tests/      Offline backend, contract, DOCX, and synthetic fixtures
docs/       Specifications, decisions, tasks, and operations
tools/      Internal project coordination and developer tooling
```

## Documentation

- [Project context](PROJECT_CONTEXT.md)
- [System specification](docs/system-specification.md)
- [Processing workflow](docs/workflow.md)
- [MVP handover runbook](docs/operations/MVP_HANDOVER_RUNBOOK.md)
- [Final local/synthetic MVP closeout](docs/operations/FINAL_MVP_CLOSEOUT.md)
- [Project Control Center](docs/operations/01_PROJECT_CONTROL_CENTER.md)
- [Independent review log](docs/operations/02_GEMINI_REVIEW_LOG.md)
- [AI collaboration rules](AGENTS.md)

Detailed task, commit, review, and governance history lives in those documents and Git history.

## Safety and current limitations

- Generated output is a **draft** requiring Human/IP-specialist review. It is not
  legal advice, a patentability or novelty/inventive-step conclusion, an inventorship determination, or a filing guarantee.
- Claims, OCR/scanned-PDF processing, prior-art search, and patentability
  scoring are outside the current MVP.
- Live-provider smoke is **UNVALIDATED / DEFERRED**. Synthetic tests do not
  validate provider behavior or real-paper semantic quality.
- EVAL-001 framework and Human-accepted six-case corpus/gold benchmark are merged;
  PRODUCT_RUNTIME semantic validation is **DEFERRED — AWAITING FUNDING**.
  Product-runtime evidence is **NONE** and semantic acceptance **NOT_DETERMINED**.
  Consumer UI or synthetic output is not equivalent to product-runtime evidence.
- Current file handling is local/ephemeral and cleanup is best effort. There is no
  approved private **production** storage or retention guarantee.
- BLK-003 remains **OPEN** for production authentication, private production storage,
  and retention/deletion policy. Real or confidential research data is **not authorized**.
- No public deployment, production approval, or public URL exists.

## Future Work

These are separate future gates, not a committed production release scope:

| Step | Status | Function / scope |
| --- | --- | --- |
| P1-001 | **CLOSED / COMPLETED — MERGED** | Frontend accessibility, keyboard/focus behavior, TypeScript typecheck and CI hardening |
| P1-002 | **CLOSED / COMPLETED — MERGED** | Six deterministic offline adversarial regressions merged via PR #40; main CI `36583295714` SUCCESS; no provider calls |
| P1-003 | **PLANNED** | Local security hardening before any public demo; does not resolve production BLK-003 |
| P1-004 | **PLANNED** | One-command local developer run/setup and DX improvements |
| P1-005 | **PLANNED** | Offline performance baseline and repeatable local measurements |
| P1-006 | **PLANNED** | UX polish, responsive behavior and error recovery |
| DEPLOY-001 | **PLANNED — implementation not authorized** | Zero-cost demo/staging deployment that can provide a public HTTPS demo URL using synthetic/demo data only; platform selection and implementation require a separate Human decision |
| EVAL-001 PRODUCT_RUNTIME | **DEFERRED — AWAITING FUNDING** | Product-runtime semantic validation; provider authorization/budget remain separate Human gates |
| SEC-001 / BLK-003 | **OPEN / DEFERRED** | Production auth/tenant model, private storage, retention/deletion; required before production or real/confidential-data use |
| Production deployment | **NOT APPROVED / NOT PERFORMED** | Separate from DEPLOY-001 demo/staging; requires security acceptance and Human approval |
| Prompt/model/runtime optimization | **DEFERRED** | Separate scope; no paid/provider work authorized |
| Claims | **OUT OF SCOPE** | Separate Human/legal scope and review required |

DEPLOY-001 is a roadmap registration only. It does not select Vercel, Railway or another hosting platform, does not authorize deployment, does not resolve BLK-003, and does not permit real/confidential research data or paid provider/API calls.

## License

No repository license has been published yet.
