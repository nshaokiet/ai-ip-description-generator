# AI IP Generator – Project Control Center

> Bản nguồn Markdown được quản lý trong Git. Tên Google Doc đích: `01_PROJECT_CONTROL_CENTER`. Trạng thái đồng bộ Google Drive: `[CẦN XÁC NHẬN TRẠNG THÁI]`.

## 1. Document Metadata

| Thuộc tính | Giá trị |
|---|---|
| Document ID | OPS-001 |
| Document title | AI IP Generator – Project Control Center |
| Version | 0.3.3 |
| Status | Active — approved specification baseline |
| Owner | Human / Product Owner |
| Author | ChatGPT/Codex |
| Reviewer | Gemini 3.1 Pro High |
| Created date | 18/09/2026 |
| Last updated | 21/09/2026 GMT+7 |
| Related task ID | SPEC-004 |
| Source of Truth | Operational status bridge; bản nguồn Git tại `docs/operations/01_PROJECT_CONTROL_CENTER.md` |
| Confidentiality level | Internal |

### Lịch sử phiên bản

| Phiên bản cũ | Phiên bản mới | Ngày | Người thực hiện | Thay đổi | Lý do | Finding/Decision liên quan | Breaking change |
|---|---|---|---|---|---|---|---|
| Chưa có | 0.1.0 | 18/09/2026 | ChatGPT/Codex | Tạo Project Control Center ban đầu | Khởi tạo điều phối Phase 1 | SPEC-004 | No |
| 0.1.0 | 0.1.1 | 18/09/2026 | ChatGPT/Codex | Cập nhật GitHub URL, Private visibility và trạng thái publish | Đồng bộ operational status với repository thực tế | Yêu cầu Human đưa artefact lên GitHub | No |
| 0.1.1 | 0.2.0 | 18/09/2026 | ChatGPT/Codex | Ghi nhận AI-001 implementation trước independent review | Đồng bộ bằng chứng schema, fixtures và tests | AI-001, ADR-006 | No |
| 0.2.0 | 0.2.1 | 18/09/2026 | ChatGPT/Codex | Ghi nhận Gemini review PASS, không có finding và PR #1 đang chờ Human merge approval | Governance closeout trước merge | AI-001, REV-AI-001, PR #1 | No |
| 0.2.1 | 0.2.2 | 19/09/2026 | ChatGPT/Codex | Chuyển AI-001 sang Completed sau khi Human merge PR #1 | Governance closeout sau merge với bằng chứng repository | AI-001, REV-AI-001, PR #1, merge commit `49efead593437dfc5c88397ea6f335a2d4ff84d7` | No |
| 0.2.2 | 0.2.3 | 19/09/2026 | ChatGPT/Codex | Ghi nhận AI-002 implementation, ADR-007 và offline test evidence | Đồng bộ trạng thái task sau Human approval | AI-002, ADR-007 | No |
| 0.2.3 | 0.2.4 | 19/09/2026 | ChatGPT/Codex | Ghi nhận Gemini review PASS và PR #3 đang chờ Human merge approval | Đồng bộ review evidence thực tế trước merge | AI-002, REV-AI-002, PR #3 | No |
| 0.2.4 | 0.2.5 | 19/09/2026 | ChatGPT/Codex | Chuyển AI-002 sang Completed sau khi Human merge PR #3 | Governance closeout sau merge với bằng chứng repository | AI-002, REV-AI-002, PR #3, merge commit `8f2b7082881961cc1a2cf7fa56ece81976759c7f` | No |
| 0.2.5 | 0.2.6 | 19/09/2026 | ChatGPT/Codex | Ghi nhận AI-003 implementation, ADR-008, Patent Draft Contract và offline tests | Đồng bộ trạng thái task sau Human approval | AI-003, ADR-008 | No |
| 0.2.6 | 0.2.7 | 20/09/2026 | ChatGPT/Codex | Ghi nhận Gemini 3.1 Pro High independent review AI-003 PASS, không có finding hoặc required change | Đồng bộ review evidence thực tế trước commit, PR và merge | AI-003, ADR-008, REV-AI-003 | No |
| 0.2.7 | 0.2.8 | 20/09/2026 | ChatGPT/Codex | Chuyển AI-003 sang Completed sau khi Human merge PR #5 | Governance closeout sau merge với bằng chứng repository | AI-003, REV-AI-003, PR #5, merge commit `fb522bc5ecbb5ad66bab6226fa88ae51020cef52` | No |
| 0.2.8 | 0.2.9 | 20/09/2026 | ChatGPT/Codex | Ghi nhận DOC-001 implementation và automated validation, chờ Human visual QA/Gemini review | Đồng bộ bằng chứng task được Human phê duyệt | DOC-001, ADR-009 | No |
| 0.2.9 | 0.2.10 | 20/09/2026 | ChatGPT/Codex | Ghi nhận Human Visual QA và Gemini independent review DOC-001 đều PASS, không có finding | Đồng bộ governance state trước Human merge approval | DOC-001, ADR-009, REV-DOC-001 | No |
| 0.2.10 | 0.2.11 | 20/09/2026 | ChatGPT/Codex | Chuyển DOC-001 sang Completed sau khi Human merge PR #7 | Post-merge governance closeout với bằng chứng repository | DOC-001, ADR-009, REV-DOC-001, PR #7, merge commit `d208a7925da844c5b43578bac8ebdbb1c5c6b5b8` | No |
| 0.2.11 | 0.3.0 | 20/09/2026 | ChatGPT/Codex | Ghi approved baseline SPEC-001/002/003, accept ADR-001…005 và chuẩn bị APP-001 specification | Đồng bộ Gemini review và Human decisions | REV-001/002/003, DEC-001/002/003, APP-001 | No |
| 0.3.0 | 0.3.1 | 20/09/2026 | ChatGPT/Codex | Chuyển APP-001 sang Completed sau Gemini PASS và Human merge PR #10; đóng REV-APP-001 | Post-merge governance closeout | APP-001, REV-APP-001, PR #10, merge commit `0df4814ff1eb8cd576566ac3dd403131feca3759` | No |
| 0.3.1 | 0.3.2 | 21/09/2026 | ChatGPT/Codex | Chuyển APP-002 sang Completed sau remediation, Gemini targeted PASS và Human merge PR #12; đóng REV-APP-002 | Post-merge governance closeout | APP-002, REV-APP-002, PR #12, merge commit `4a001d116cbf002bdd42a9151efbf3f308fce3e6` | No |
| 0.3.2 | 0.3.3 | 21/09/2026 | ChatGPT/Codex | Ghi AI-RUNTIME-001 internal extraction runtime đã triển khai và chờ independent review | Đồng bộ Human-approved implementation, ADR-010 và BLK-004 disposition | AI-RUNTIME-001, ADR-010 | No |

## 2. Project

**AI Intellectual Property Description Generator**

Mục tiêu: chuyển một bài báo PDF/DOCX thành Structured JSON có evidence, thông tin thiếu, bản dự thảo patent specification cần Human review và DOCX.

## 3. Repository

`ai-ip-description-generator`

- GitHub remote URL: `https://github.com/nshaokiet/ai-ip-description-generator`.
- Default branch: `main`.
- GitHub repository visibility: **Private**, đã xác minh ngày 18/09/2026.

## 4. Deadline

**02/10/2026 — ngày bàn giao chính thức.** Mục tiêu hoàn thành nội bộ: **30/09/2026**; ngày **01–02/10/2026** dành cho buffer, test và handover.

## 5. Current Phase

Giá trị đề xuất: **Phase 1 — Specification & Architecture**.

SPEC-001/002/003 là approved baseline. Toàn bộ Phase 1 chưa được tuyên bố hoàn tất; Phase 2 chưa bắt đầu.

## 6. Current Objective

- Chốt system specification.
- Chốt project context.
- Chốt AI collaboration protocol.
- Chốt output schema.
- Chốt prompt specification.
- Giữ Claims ngoài MVP hiện hành; chỉ mở lại qua scope-change approval.
- Chốt template DOCX.

Các mục trên chưa được coi là đã chốt chỉ vì có tài liệu Draft.

## 7. Overall Progress

- [x] Khởi tạo local Git repository.
- [x] Xác minh GitHub repository và Private visibility.
- [x] Publish bộ 5 artefact cùng README lên nhánh `main` trong commit đồng bộ này.
- [x] SPEC-001 `docs/system-specification.md` 0.3.0 — Approved baseline.
- [x] SPEC-003 `AGENTS.md` 0.2.0 — Approved baseline.
- [x] SPEC-002 `PROJECT_CONTEXT.md` 0.3.0 — Approved baseline.
- [x] Project Control Center 0.3.2 và Gemini Review Log 0.3.2 được cập nhật cho APP-002 post-merge closeout.
- [x] Gemini 3.1 Pro High review SPEC-001/002/003: `PASS WITH HUMAN DECISIONS REQUIRED`; không có document finding.
- [x] Human phê duyệt SPEC-001/002/003 là baseline và chốt DEC-001/002/003.
- [x] ADR-001…ADR-005 đã được tạo với trạng thái `Accepted`.
- [x] APP-001 specification đã merge qua PR #9; implementation đã merge qua PR #10.
- [x] Human phê duyệt ADR-006 và contract Output Schema v1.0.0.
- [x] Implement Output Schema v1.0.0, fixtures và automated tests.
- [x] Gemini 3.1 Pro full review và targeted whitespace re-review cho AI-001: PASS, không có finding.
- [x] Human đã phê duyệt và merge PR #1 ngày 19/09/2026; AI-001 `Completed` tại merge commit `49efead593437dfc5c88397ea6f335a2d4ff84d7`.
- [x] Human phê duyệt AI-002 và ADR-007; Extraction Prompt v1.0.0 cùng fixtures/tests offline đã được triển khai.
- [x] Gemini 3.1 Pro High independent review AI-002: PASS, không có finding hoặc required change.
- [x] Human đã phê duyệt và merge PR #3 ngày 19/09/2026; AI-002 `Completed` tại merge commit `8f2b7082881961cc1a2cf7fa56ece81976759c7f`.
- [x] Human phê duyệt AI-003 và ADR-008; Patent Draft Contract v1.0.0, Draft Generation Prompt v1.0.0 cùng synthetic fixtures/tests đã được triển khai.
- [x] Gemini 3.1 Pro High independent read-only review AI-003: PASS, không có finding hoặc required change.
- [x] Human đã phê duyệt và merge PR #5 ngày 20/09/2026; AI-003 `Completed` tại merge commit `fb522bc5ecbb5ad66bab6226fa88ae51020cef52`.
- [x] Human loại Claims/Draft Claims khỏi MVP hiện hành; task tương lai cần approval riêng.
- [x] Triển khai Patent DOCX Template v1.0.0, mapping, renderer, synthetic fixtures và automated tests.
- [x] Human Microsoft Word Visual QA DOC-001: PASS, không có finding.
- [x] Gemini 3.1 Pro High independent review DOC-001: PASS, không có finding hoặc required change; recommendation `APPROVE`.
- [x] Human / Product Owner đã approve và merge PR #7 ngày 20/09/2026; DOC-001 `Completed` tại merge commit `d208a7925da844c5b43578bac8ebdbb1c5c6b5b8`.
- [x] Khởi tạo FastAPI local skeleton và secure upload trong phạm vi APP-001.
- [x] APP-002 deterministic document/evidence preparation được triển khai; Gemini initial review `REQUEST CHANGES` với F-001 `HIGH` và F-002 `MEDIUM`, remediation `8b6f909a0f5787d72c002e163395656a666c9b78`, targeted re-review `PASS` và Human merge PR #12 tại `4a001d116cbf002bdd42a9151efbf3f308fce3e6`.
- [x] AI-RUNTIME-001 internal Responses API extraction, provider adapter, canonical validation và grounding/business validation đã triển khai; đang chờ Gemini independent implementation review và chưa `Completed`.
- [ ] Chạy core pipeline end-to-end.
- [ ] Evaluation, stabilization, deployment và handover.

Các ô `[x]` chỉ xác nhận bằng chứng được nêu ngay trên từng dòng; không suy rộng thành Human/Gemini approval cho các artefact hoặc phase khác.

## 8. Completed

AI-001, AI-002, AI-003, DOC-001, APP-001 và APP-002 là các hạng mục đã được Human xác nhận `Completed`. SPEC-001/002/003 là approved baseline, nhưng điều này không đánh dấu toàn bộ Phase 1, Phase 2 hoặc MVP `Completed`.

Các deliverable Draft đã tạo, có bằng chứng file:

| Task ID | Deliverable | Evidence | Kết luận được phép |
|---|---|---|---|
| SPEC-001 | System Specification 0.3.2 | Approved baseline; APP-001/APP-002 merge evidence đồng bộ đến 21/09/2026 | Approved baseline |
| SPEC-002 | Project Context 0.3.2 | Approved baseline; APP-001/APP-002 merge evidence đồng bộ đến 21/09/2026 | Approved baseline |
| SPEC-003 | AI Collaboration Rules 0.2.0 | Gemini 3.1 Pro High review + Human decisions ngày 20/09/2026 | Approved baseline |
| SPEC-004 | Project Control Center source 0.3.2 | File hiện tại | Active; Google Doc sync pending confirmation |
| REVIEW-001 | Gemini Review Log source 0.3.2 | `REV-APP-002` và các review task có bằng chứng | Active log; listed reviews CLOSED |
| AI-001 | Output Schema v1.0.0 | PR [#1](https://github.com/nshaokiet/ai-ip-description-generator/pull/1), merge commit `49efead593437dfc5c88397ea6f335a2d4ff84d7`, 19/09/2026; Gemini review PASS; 15/15 tests pass; không có finding | Completed — Merged via PR #1 |
| AI-002 | Extraction Prompt v1.0.0 | PR [#3](https://github.com/nshaokiet/ai-ip-description-generator/pull/3), merge commit `8f2b7082881961cc1a2cf7fa56ece81976759c7f`, 19/09/2026; implementation `f8772b228a23bf7cdec10fa0c463e6d1f672c341`; governance `9f2a78b1396cdadb747c263a2bbbbacb8d7f4292`; Gemini review PASS; AI-001 15/15 và AI-002 17/17 tests pass; không có finding | Completed — Merged via PR #3 |
| AI-003 | Patent Draft Generation Contract v1.0.0 | PR [#5](https://github.com/nshaokiet/ai-ip-description-generator/pull/5), implementation `ae7e8fb573ea4681a9db1bafa711d19a3c598666`, merge commit `fb522bc5ecbb5ad66bab6226fa88ae51020cef52`, 20/09/2026; Gemini reviews PASS; 57/57 tests pass; không có finding hoặc required change | Completed — Merged via PR #5 |
| DOC-001 | Patent DOCX Template v1.0.0 | PR [#7](https://github.com/nshaokiet/ai-ip-description-generator/pull/7), implementation `d3f7c7d9596b77a39e9a56fcdf97c76cb972612a`, merge commit `d208a7925da844c5b43578bac8ebdbb1c5c6b5b8`, 20/09/2026; Human Visual QA và Gemini reviews PASS; 85/85 tests pass; không có finding hoặc required change | Completed — Merged via PR #7 |
| APP-001 | FastAPI Backend Skeleton and Secure Document Upload | Specification PR [#9](https://github.com/nshaokiet/ai-ip-description-generator/pull/9), merge `1bf957162eba78c069d3ba976af7fe1d174cab30`; implementation PR [#10](https://github.com/nshaokiet/ai-ip-description-generator/pull/10), head `bd39b9f7bdd9f7a1796d9a405e7998070e124e07`, merge `0df4814ff1eb8cd576566ac3dd403131feca3759`, 20/09/2026; Gemini PASS, 22/22 AC, Security/Scope PASS, 109/109 tests | Completed — Merged via PR #10 |
| APP-002 | Document Parsing & Evidence Source Units | PR [#12](https://github.com/nshaokiet/ai-ip-description-generator/pull/12), initial implementation `477b8fda6afbae0049d8d691c213dc6355ba67da`, remediation `8b6f909a0f5787d72c002e163395656a666c9b78`, merge `4a001d116cbf002bdd42a9151efbf3f308fce3e6`, 21/09/2026; initial Gemini `REQUEST CHANGES`, F-001/F-002 resolved, targeted `PASS`; 30/30 AC; 135 executed, 134 pass, 1 skip, 0 failure/error | Completed — Merged via PR #12 |

APP-002 capability boundary: `Validated PDF/DOCX → deterministic text/table parsing → safe metadata registry + SHA-256 integrity verification → source units → evidence IDs/source locators → AI-002 Extraction Input Envelope`. APP-002 không cung cấp OpenAI Responses API, model invocation, Structured Outputs provider adapter, OCR, database, authentication, frontend, deployment hoặc public analyze endpoint. Core pipeline end-to-end vẫn chưa hoàn thành.

## 9. In Progress

| Task ID | Công việc | Owner | Reviewer | Status | Evidence/Blocker |
|---|---|---|---|---|---|
| AI-RUNTIME-001 | OpenAI Responses API + Structured Outputs Extraction Runtime | ChatGPT/Codex | Gemini 3.1 Pro High + Human | Implementation — Awaiting Independent Review | Approved baseline `f8070a5c94290ff44c65bc1b0831458662e14e11`; ADR-010; offline tests required before handoff |
| SPEC-004 | Đồng bộ Project Control Center sang Google Docs | Human / Product Owner | ChatGPT/Codex | `[CẦN XÁC NHẬN TRẠNG THÁI]` | Chưa có bằng chứng Google Doc/link |

## 10. Next Tasks

| Task ID | Task | Owner | Reviewer | Priority | Status | Dependency | Target date |
|---|---|---|---|---|---|---|---|
| NEXT-TBD | Task sau AI-RUNTIME-001 do Human xác định | Human / Product Owner | `[CẦN PHÂN CÔNG]` | `[CẦN XÁC NHẬN]` | NOT STARTED — Awaiting Human assignment | AI-RUNTIME-001 review/merge decision | Trước 02/10/2026 nếu được giao |

Mọi target date cụ thể cần được xếp trước deadline chung 02/10/2026 và do Human xác nhận.

## 11. Current Blockers

| Blocker ID | Blocker | Ảnh hưởng | Owner quyết định | Status |
|---|---|---|---|---|
| BLK-003 | Chưa chốt auth/private production storage/retention | Không được dùng dữ liệu nghiên cứu thật; AI-RUNTIME-001 chỉ synthetic/offline hoặc opt-in synthetic live smoke | Human / Product Owner | Open — production/real-data blocker |
| BLK-004 | Chưa chốt model, retrieval, retry, timeout, cost | Extraction Runtime v1 đã khóa; draft runtime/task tương lai không được suy rộng | Human / Product Owner | Resolved for Extraction Runtime v1 only — AI-RUNTIME-001/ADR-010 |
| BLK-005 | Chưa chốt phạm vi Draft Claims tương lai | Không chặn AI-001, AI-002, claim-free AI-003 hoặc claim-free DOC-001; chỉ ảnh hưởng task claims riêng nếu được phê duyệt sau | Human + chuyên gia SHTT | Open — non-blocker for AI-001/AI-002/AI-003/DOC-001 |
| BLK-007 | Chưa có bằng chứng Google Docs được tạo/đồng bộ | Operational bridge chưa sẵn sàng trên Drive | Human / Product Owner | Open |

## 12. Architecture Decisions

| ID | Date | Decision | Reason | Alternatives | Approver | Status | Related artefact |
|---|---|---|---|---|---|---|---|
| ADR-001 | 20/09/2026 | Use FastAPI backend | Phù hợp Python AI/document pipeline và typed API | Flask, Django/DRF, Node.js | Human / Product Owner | ACCEPTED — IMPLEMENTED BY APP-001 — MERGED VIA PR #10 | `docs/decisions/ADR-001-fastapi-backend.md` |
| ADR-002 | 20/09/2026 | Use OpenAI Responses API for production AI MVP | Khóa provider direction; tích hợp/model/data policy theo task riêng | Chat Completions, Gemini runtime, self-hosted model | Human / Product Owner | ACCEPTED | `docs/decisions/ADR-002-openai-responses-api-mvp.md` |
| ADR-003 | 20/09/2026 | Gemini acts as reviewer, not production AI dependency | Tách implementation và independent review | Gemini runtime/implementation owner | Human / Product Owner | ACCEPTED | `docs/decisions/ADR-003-gemini-reviewer-role.md` |
| ADR-004 | 20/09/2026 | GitHub is Technical Source of Truth | Version control và traceability | Google Drive/NotebookLM làm technical source | Human / Product Owner | ACCEPTED | `docs/decisions/ADR-004-github-technical-source-of-truth.md` |
| ADR-005 | 20/09/2026 | Human review is mandatory | Giảm hallucination/rủi ro pháp lý và kỹ thuật | Fully automated approval | Human / Product Owner | ACCEPTED | `docs/decisions/ADR-005-human-review-required.md` |
| ADR-006 | 18/09/2026 | JSON Schema Draft 2020-12, strict Output Schema v1.0.0; loại claims và Human confirmation state | Tạo contract kiểm thử được, đúng phạm vi AI-001 | Schema lỏng; claims optional; Human confirmation trong payload | Human / Product Owner | ACCEPTED | `docs/decisions/ADR-006-output-schema-v1.md` |
| ADR-007 | 19/09/2026 | Extraction Prompt v1.0.0 dùng normalized JSON envelope và canonical offline validation; hoãn provider adapter/live evaluation | Tách prompt contract khỏi runtime/provider concerns và giữ schema hiện hành | Truyền schema nguyên trạng; sửa schema; tạo adapter ngay | Human / Product Owner | ACCEPTED — COMPLETED — MERGED VIA PR #3 | `docs/decisions/ADR-007-extraction-prompt-v1.md` |
| ADR-008 | 19/09/2026 | Thêm strict Patent Draft Generation Contract v1.0.0 giữa validated analysis và DOCX; không claims; offline-only validation | Tách extraction, technical drafting và presentation; giữ paragraph-level evidence traceability | Render Output Schema trực tiếp; sửa Output Schema; free-form draft | Human / Product Owner | ACCEPTED — COMPLETED — MERGED VIA PR #5 | `docs/decisions/ADR-008-patent-draft-contract-v1.md` |
| ADR-009 | 20/09/2026 | Dùng versioned `docxtpl` template và deterministic offline renderer cho DOCX claim-free | Tách presentation khỏi drafting contract; giữ mapping, escaping, evidence và visual-review gate | Procedural-only DOCX; render trực tiếp Output Schema; PDF; auto-generated figures | Human / Product Owner | ACCEPTED — COMPLETED — MERGED VIA PR #7 | `docs/decisions/ADR-009-patent-docx-template-v1.md` |
| ADR-010 | 21/09/2026 | OpenAI Responses API extraction với `gpt-5.6-sol`, provider adapter, canonical/grounding post-validation và `store=false` | Tạo internal fail-closed boundary mà không đổi AI-001/AI-002 | Raw canonical schema; provider schema copy; repair call; retrieval | Human / Product Owner | ACCEPTED — IMPLEMENTED — AWAITING REVIEW | `docs/decisions/ADR-010-openai-extraction-runtime-v1.md` |

ADR-001 đến ADR-010 đã được Human phê duyệt trong phạm vi từng decision record. `Accepted` không tự động cho phép implementation ngoài task được duyệt.

## 13. Current AI Assignments

| Task ID | Task | Owner | Reviewer | Status | Expected output |
|---|---|---|---|---|---|
| SPEC-001 | System Specification | ChatGPT/Codex | Gemini Pro + Human | Approved baseline | `docs/system-specification.md` 0.3.3; REV-001 CLOSED |
| SPEC-002 | Project Context | ChatGPT/Codex | Gemini Pro + Human | Approved baseline | `PROJECT_CONTEXT.md` 0.3.3; REV-003 CLOSED |
| SPEC-003 | AGENTS.md | ChatGPT/Codex | Gemini Pro + Human | Approved baseline | `AGENTS.md` 0.2.0; REV-002 CLOSED |
| SPEC-004 | Control Center source | ChatGPT/Codex | Human | Active | File hiện tại 0.3.3 |
| REVIEW-001 | Review Log | ChatGPT/Codex | Gemini Pro + Human | Active | `02_GEMINI_REVIEW_LOG.md` 0.3.2; REV-APP-002 và prior task reviews CLOSED |
| APP-001 | FastAPI Backend Skeleton and Secure Document Upload | ChatGPT/Codex | Gemini 3.1 Pro High + Human | Completed — Merged via PR #10 | Implementation head `bd39b9f7bdd9f7a1796d9a405e7998070e124e07`; merge `0df4814ff1eb8cd576566ac3dd403131feca3759`; 109/109 tests pass |
| APP-002 | Document Parsing & Evidence Source Units | ChatGPT/Codex | Gemini 3.1 Pro High + Human | Completed — Merged via PR #12 | Initial `477b8fda6afbae0049d8d691c213dc6355ba67da`; remediation `8b6f909a0f5787d72c002e163395656a666c9b78`; merge `4a001d116cbf002bdd42a9151efbf3f308fce3e6`; 30/30 AC; final Gemini PASS; 135 executed, 134 pass, 1 skip |
| AI-RUNTIME-001 | OpenAI Responses API + Structured Outputs Extraction Runtime | ChatGPT/Codex | Gemini 3.1 Pro High + Human | Implementation — Awaiting Independent Review | `docs/tasks/AI-RUNTIME-001-openai-extraction-runtime.md`; ADR-010; internal runtime and synthetic tests |
| AI-001 | Output Schema v1.0.0 | ChatGPT/Codex | Gemini 3.1 Pro | Completed — Merged via PR #1 | Merge commit `49efead593437dfc5c88397ea6f335a2d4ff84d7`; Gemini review PASS; 15/15 tests pass; không có finding |
| AI-002 | Extraction Prompt v1.0.0 | ChatGPT/Codex | Gemini 3.1 Pro High | Completed — Merged via PR #3 | Merge commit `8f2b7082881961cc1a2cf7fa56ece81976759c7f`; implementation `f8772b228a23bf7cdec10fa0c463e6d1f672c341`; governance `9f2a78b1396cdadb747c263a2bbbbacb8d7f4292`; 15/15 regression và 17/17 AI-002 tests pass |
| AI-003 | Patent Draft Generation Contract v1.0.0 | ChatGPT/Codex | Gemini 3.1 Pro High | Completed — Merged via PR #5 | Implementation `ae7e8fb573ea4681a9db1bafa711d19a3c598666`; merge `fb522bc5ecbb5ad66bab6226fa88ae51020cef52`; 57/57 tests pass |
| DOC-001 | Patent DOCX Template v1.0.0 | ChatGPT/Codex | Gemini 3.1 Pro High + Human | Completed — Merged via PR #7 | Implementation `d3f7c7d9596b77a39e9a56fcdf97c76cb972612a`; merge `d208a7925da844c5b43578bac8ebdbb1c5c6b5b8`; Human Visual QA/Gemini reviews PASS; 85/85 tests pass |

## 14. Latest ChatGPT/Codex Handoff

```text
Task ID: AI-RUNTIME-001
Agent: ChatGPT/Codex
Reviewer: Gemini 3.1 Pro High
Status: Implementation — Awaiting Independent Review
Version: Specification 1.0.0; approved baseline f8070a5c94290ff44c65bc1b0831458662e14e11
Work completed: Internal Responses API extraction runtime, deterministic provider-schema adapter, nullable normalization, canonical Draft 2020-12 validation, grounding/business validation, safe error taxonomy, runtime configuration and opt-in synthetic live smoke test.
Files affected: Targeted backend runtime/config/dependencies, synthetic tests, ADR-010, task specification and necessary governance/documentation synchronization; AI-001 schema and AI-002 prompt unchanged.
Evidence checked: 32/32 acceptance criteria; 61/61 new offline tests; AI-001 15/15, AI-002 17/17, AI-003 25/25, DOC-001 28/28, backend 111 executed (110 pass, 1 Windows skip); aggregate 196 executed, 195 pass, 1 skip, 0 failure/error; pip check PASS.
Findings: Independent implementation review not yet performed; no implementation finding recorded.
Decisions: Human approved AI-RUNTIME-001 Specification v1.0.0 and ADR-010 on 21/09/2026.
Issues: Live provider smoke NOT RUN because OPENAI_API_KEY is unavailable; BLK-003 remains open; public orchestration and draft runtime remain out of scope.
Security impact: Synthetic only; `store=false`; no tools/retrieval; no secret, PII, real research data or source/prompt/provider-output logging.
Recommended next action: Gemini 3.1 Pro High independent implementation review, then Human finding/merge decision. Do not start the next task.
```

## 15. Latest Gemini Handoff

```text
Task ID: APP-002
Agent: Gemini 3.1 Pro High
Reviewer: Human / Product Owner
Status: CLOSED — APP-002 Completed — Merged via PR #12
Version: Initial implementation 477b8fda6afbae0049d8d691c213dc6355ba67da; remediation 8b6f909a0f5787d72c002e163395656a666c9b78; resolved by merge 4a001d116cbf002bdd42a9151efbf3f308fce3e6
Work completed: Independent review ban đầu REQUEST CHANGES; Codex remediated F-001/F-002; targeted re-review xác nhận cả hai RESOLVED và final verdict PASS; Human / Product Owner approved and merged PR #12.
Files affected: Review only; production artefact không bị Gemini ghi đè.
Evidence checked: 30/30 acceptance criteria; 135 tests executed, 134 pass, 1 Windows skip, 0 failure/error; pip check và diff check PASS.
Findings: F-001 HIGH — root-level w:sdt omission; F-002 MEDIUM — nested-table omission; cả hai RESOLVED trong remediation commit; không có finding mới.
Decisions: Final recommendation APPROVE; Human / Product Owner approved and merged PR #12 on 21/09/2026.
Issues: StarletteDeprecationWarning là non-blocking NOTE; không có blocking finding hoặc required change sau targeted re-review.
Security impact: PASS; synthetic/offline only, không secret, cache, PII, dữ liệu nghiên cứu thật, dependency change hoặc network/model call.
Recommended next action: Targeted review post-merge governance closeout; task tiếp theo NOT STARTED — Awaiting Human assignment.
```

## 16. Files Changed

| Date | File | Version | Change | Changed by | Related task |
|---|---|---|---|---|---|
| 18/09/2026 | `docs/system-specification.md` | 0.1.0 | Tạo Draft ban đầu | ChatGPT/Codex | SPEC-001 |
| 18/09/2026 | `AGENTS.md` | 0.1.0 | Tạo quy tắc phối hợp AI | ChatGPT/Codex | SPEC-003 |
| 18/09/2026 | `PROJECT_CONTEXT.md` | 0.1.0 | Tạo bối cảnh dự án | ChatGPT/Codex | SPEC-002 |
| 18/09/2026 | `docs/operations/01_PROJECT_CONTROL_CENTER.md` | 0.1.0 | Tạo dashboard trạng thái nguồn | ChatGPT/Codex | SPEC-004 |
| 18/09/2026 | `docs/operations/02_GEMINI_REVIEW_LOG.md` | 0.1.0 | Tạo review log template nguồn | ChatGPT/Codex | REVIEW-001 |
| 18/09/2026 | `README.md` | 1.0.0 | Viết lại README tiếng Việt theo trạng thái thực tế | ChatGPT/Codex | SPEC-005 |
| 18/09/2026 | `AGENTS.md` | 0.1.1 | Ghi nhận repository Private đã xác minh | ChatGPT/Codex | SPEC-003 |
| 18/09/2026 | `PROJECT_CONTEXT.md` | 0.1.1 | Đồng bộ URL và visibility repository | ChatGPT/Codex | SPEC-002 |
| 18/09/2026 | `docs/operations/01_PROJECT_CONTROL_CENTER.md` | 0.1.1 | Cập nhật trạng thái publish GitHub | ChatGPT/Codex | SPEC-004 |
| 18/09/2026 | `docs/archive/system-specification-before-2026-09-18.md` | Archived snapshot | Bảo toàn đặc tả cũ trước khi thay bản 0.1.0 đầy đủ | ChatGPT/Codex | SPEC-001 |
| 18/09/2026 | `schemas/invention-output/v1.0.0/invention-output.schema.json` | 1.0.0 | Tạo Output Schema Draft 2020-12 | ChatGPT/Codex | AI-001 |
| 18/09/2026 | `docs/decisions/ADR-006-output-schema-v1.md` | ADR-006 | Ghi quyết định kiến trúc đã được Human phê duyệt | ChatGPT/Codex | AI-001 |
| 18/09/2026 | `tests/schema/test_invention_output_schema_v1.py` | 1.0.0 | Thêm automated schema validation | ChatGPT/Codex | AI-001 |
| 19/09/2026 | `prompts/extraction/v1.0.0/extraction-prompt.md` | 1.0.0 | Tạo canonical extraction prompt | ChatGPT/Codex | AI-002 |
| 19/09/2026 | `docs/decisions/ADR-007-extraction-prompt-v1.md` | ADR-007 | Ghi quyết định prompt contract và offline-only validation | ChatGPT/Codex | AI-002 |
| 19/09/2026 | `tests/prompt/test_extraction_prompt_v1.py` | 1.0.0 | Thêm automated offline prompt-contract validation | ChatGPT/Codex | AI-002 |
| 19/09/2026 | `PROJECT_CONTEXT.md` | 0.2.4 | Ghi nhận Gemini review PASS cho AI-002 | ChatGPT/Codex | AI-002, REV-AI-002 |
| 19/09/2026 | `docs/operations/01_PROJECT_CONTROL_CENTER.md` | 0.2.4 | Đồng bộ trạng thái AI-002 chờ Human merge approval | ChatGPT/Codex | AI-002, REV-AI-002 |
| 19/09/2026 | `docs/operations/02_GEMINI_REVIEW_LOG.md` | 0.2.2 | Thêm review entry REV-AI-002 từ evidence được Human xác nhận | ChatGPT/Codex | REV-AI-002 |
| 19/09/2026 | `PROJECT_CONTEXT.md` | 0.2.5 | Ghi nhận AI-002 Completed sau khi Human merge PR #3 | ChatGPT/Codex | AI-002, REV-AI-002 |
| 19/09/2026 | `docs/operations/01_PROJECT_CONTROL_CENTER.md` | 0.2.5 | Đồng bộ AI-002 post-merge governance closeout | ChatGPT/Codex | AI-002, REV-AI-002 |
| 19/09/2026 | `docs/operations/02_GEMINI_REVIEW_LOG.md` | 0.2.3 | Ghi Human merge decision và đóng REV-AI-002 | ChatGPT/Codex | AI-002, REV-AI-002 |
| 19/09/2026 | `schemas/patent-draft/v1.0.0/patent-draft.schema.json` | 1.0.0 | Tạo strict Patent Draft Generation Contract | ChatGPT/Codex | AI-003, ADR-008 |
| 19/09/2026 | `prompts/draft-generation/v1.0.0/draft-generation-prompt.md` | 1.0.0 | Tạo canonical offline draft-generation prompt | ChatGPT/Codex | AI-003, ADR-008 |
| 19/09/2026 | `tests/draft/test_patent_draft_contract_v1.py` | 1.0.0 | Thêm schema và business-validation tests | ChatGPT/Codex | AI-003 |
| 19/09/2026 | `PROJECT_CONTEXT.md` | 0.2.6 | Ghi nhận AI-003 Implemented — Awaiting Gemini Review | ChatGPT/Codex | AI-003 |
| 19/09/2026 | `docs/operations/01_PROJECT_CONTROL_CENTER.md` | 0.2.6 | Đồng bộ trạng thái implementation AI-003 | ChatGPT/Codex | AI-003 |
| 20/09/2026 | `PROJECT_CONTEXT.md` | 0.2.7 | Ghi nhận Gemini review PASS cho AI-003 | ChatGPT/Codex | AI-003, REV-AI-003 |
| 20/09/2026 | `docs/operations/01_PROJECT_CONTROL_CENTER.md` | 0.2.7 | Đồng bộ AI-003 chờ Human merge approval | ChatGPT/Codex | AI-003, REV-AI-003 |
| 20/09/2026 | `docs/operations/02_GEMINI_REVIEW_LOG.md` | 0.2.4 | Thêm review entry REV-AI-003 từ evidence được Human xác nhận | ChatGPT/Codex | REV-AI-003 |
| 20/09/2026 | `docs/system-specification.md` | 0.2.4 | Ghi nhận AI-003 Completed sau merge PR #5 | ChatGPT/Codex | AI-003, REV-AI-003 |
| 20/09/2026 | `PROJECT_CONTEXT.md` | 0.2.8 | Ghi nhận AI-003 Completed sau merge PR #5 | ChatGPT/Codex | AI-003, REV-AI-003 |
| 20/09/2026 | `docs/operations/01_PROJECT_CONTROL_CENTER.md` | 0.2.8 | Đồng bộ AI-003 post-merge governance closeout | ChatGPT/Codex | AI-003, REV-AI-003 |
| 20/09/2026 | `docs/operations/02_GEMINI_REVIEW_LOG.md` | 0.2.5 | Ghi Human merge decision và đóng REV-AI-003 | ChatGPT/Codex | AI-003, REV-AI-003 |
| 20/09/2026 | `templates/patent-docx/v1.0.0/patent-description-template.docx` | 1.0.0 | Tạo canonical claim-free Patent DOCX Template | ChatGPT/Codex | DOC-001, ADR-009 |
| 20/09/2026 | `tests/docx/render_patent_docx_v1.py` | 1.0.0 | Tạo deterministic offline schema-first renderer | ChatGPT/Codex | DOC-001, ADR-009 |
| 20/09/2026 | `docs/operations/01_PROJECT_CONTROL_CENTER.md` | 0.2.9 | Ghi nhận DOC-001 implemented, chờ Human visual QA và Gemini review | ChatGPT/Codex | DOC-001 |
| 20/09/2026 | `PROJECT_CONTEXT.md` | 0.2.10 | Ghi nhận Human Visual QA và Gemini independent review DOC-001 PASS | ChatGPT/Codex | DOC-001, REV-DOC-001 |
| 20/09/2026 | `docs/system-specification.md` | 0.2.6 | Đồng bộ DOC-001 review evidence, không đổi technical specification | ChatGPT/Codex | DOC-001, REV-DOC-001 |
| 20/09/2026 | `docs/operations/01_PROJECT_CONTROL_CENTER.md` | 0.2.10 | Chuyển DOC-001 sang chờ Human merge approval | ChatGPT/Codex | DOC-001, REV-DOC-001 |
| 20/09/2026 | `docs/operations/02_GEMINI_REVIEW_LOG.md` | 0.2.6 | Thêm `REV-DOC-001` với trạng thái `MERGE PENDING` | ChatGPT/Codex | DOC-001, REV-DOC-001 |
| 20/09/2026 | `PROJECT_CONTEXT.md` | 0.2.11 | Ghi nhận DOC-001 Completed sau merge PR #7 | ChatGPT/Codex | DOC-001, REV-DOC-001 |
| 20/09/2026 | `docs/system-specification.md` | 0.2.7 | Ghi nhận DOC-001 post-merge closeout, không đổi technical specification | ChatGPT/Codex | DOC-001, REV-DOC-001 |
| 20/09/2026 | `docs/operations/01_PROJECT_CONTROL_CENTER.md` | 0.2.11 | Chuyển DOC-001 sang Completed sau merge PR #7 | ChatGPT/Codex | DOC-001, REV-DOC-001 |
| 20/09/2026 | `docs/operations/02_GEMINI_REVIEW_LOG.md` | 0.2.7 | Ghi Human merge decision và đóng `REV-DOC-001` | ChatGPT/Codex | DOC-001, REV-DOC-001 |
| 20/09/2026 | `docs/system-specification.md` / `PROJECT_CONTEXT.md` / `AGENTS.md` | 0.3.0 / 0.3.0 / 0.2.0 | Ghi approved baseline sau review và Human decisions | ChatGPT/Codex | SPEC-001/002/003, REV-001/002/003 |
| 20/09/2026 | `docs/decisions/ADR-001…005-*.md` | ADR-001…ADR-005 | Tạo năm decision records `Accepted` | ChatGPT/Codex | DEC-002, APP-001 |
| 20/09/2026 | `docs/tasks/APP-001-fastapi-backend-upload.md` | Specification | Chuẩn bị scope, API, security, dependencies và 22 acceptance criteria; không implementation | ChatGPT/Codex | APP-001 |
| 20/09/2026 | `docs/operations/01_PROJECT_CONTROL_CENTER.md` / `docs/operations/02_GEMINI_REVIEW_LOG.md` | 0.3.0 / 0.3.0 | Đồng bộ baseline/ADR/APP-001 và đóng REV-001/002/003 | ChatGPT/Codex | REVIEW-001, APP-001 |
| 20/09/2026 | `backend/app/`, `backend/requirements.txt`, `tests/backend/`, `backend/README.md` | APP-001 implementation | FastAPI local skeleton và secure PDF/DOCX upload được Human merge qua PR #10 | ChatGPT/Codex | APP-001, ADR-001, REV-APP-001 |
| 20/09/2026 | Governance/documentation closeout | 0.3.1 | Ghi Gemini PASS, Human merge decision và đóng REV-APP-001 | ChatGPT/Codex | APP-001, PR #10, merge `0df4814ff1eb8cd576566ac3dd403131feca3759` |
| 21/09/2026 | Governance/documentation closeout | 0.3.2 | Bảo toàn initial REQUEST CHANGES/F-001/F-002, ghi remediation, targeted PASS, Human merge PR #12 và đóng REV-APP-002 | ChatGPT/Codex | APP-002, REV-APP-002, PR #12, merge `4a001d116cbf002bdd42a9151efbf3f308fce3e6` |

## 17. Prompt and Schema Versions

| Artefact | Current version | Status | Owner | Reviewer | Last updated |
|---|---|---|---|---|---|
| Extraction prompt | 1.0.0 | Completed — Merged via PR #3 | ChatGPT/Codex | Gemini 3.1 Pro High | 19/09/2026 |
| Draft generation prompt | 1.0.0 | Completed — Merged via PR #5 | ChatGPT/Codex | Gemini 3.1 Pro High | 20/09/2026 |
| Invention JSON Schema | 1.0.0 | Completed — Merged via PR #1 | ChatGPT/Codex | Gemini 3.1 Pro | 19/09/2026 |
| Patent Draft JSON Schema | 1.0.0 | Completed — Merged via PR #5 | ChatGPT/Codex | Gemini 3.1 Pro High | 20/09/2026 |
| DOCX template | 1.0.0 | Completed — Merged via PR #7 | ChatGPT/Codex | Gemini 3.1 Pro High + Human | 20/09/2026 |
| API contract | APP-001 | Completed — Merged via PR #10; public surface unchanged by APP-002 | ChatGPT/Codex | Gemini 3.1 Pro High + Human | 21/09/2026 |
| Document parsing/evidence preparation | APP-002 | Completed — Merged via PR #12 | ChatGPT/Codex | Gemini 3.1 Pro High + Human | 21/09/2026 |
| OpenAI extraction runtime | AI-RUNTIME-001 / spec 1.0.0 | Implementation — Awaiting Independent Review | ChatGPT/Codex | Gemini 3.1 Pro High + Human | 21/09/2026 |

## 18. Risks

| Risk ID | Risk | Probability | Impact | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|
| RISK-001 | AI hallucination/unsupported content | High | High | Evidence schema, grounding validator, Human review | ChatGPT/Codex + Human | Open |
| RISK-002 | Confidential research exposure | Medium | Critical | Private repo/storage, authz, vendor review, no raw paper in Git | Human / Product Owner | Open |
| RISK-003 | Draft Claims vượt source support | High | High | Claim mapping, expert review, unresolved labels | Human + chuyên gia SHTT | Open |
| RISK-004 | Deadline bị ảnh hưởng bởi scope chưa chốt | High | High | Quyết định blockers sớm, giữ 1-paper MVP | Human / Product Owner | Open |
| RISK-005 | Prompt/schema/template version drift | Medium | High | Version policy, regression tests, single technical source | ChatGPT/Codex | Open |
| RISK-006 | Git/Drive trạng thái lệch nhau | Medium | Medium | Git là technical source; log sync và last-updated | Human + ChatGPT/Codex | Open |

## 19. Questions Requiring Human Decision

| Question ID | Question | Context | Options | Impact | Deadline | Decision |
|---|---|---|---|---|---|---|
| Q-001 | Có OCR/scanned PDF trong APP-001 không? | Parser scope | Human decision | Scanned input bị từ chối; không OCR | 20/09/2026 | Không; scope rộng hơn cần approval riêng |
| Q-002 | Giới hạn file/page APP-001 là bao nhiêu? | Upload/performance | Human decision | Validation và cost | 20/09/2026 | 10 MiB cho PDF/DOCX; PDF 50 trang; DOCX exact pagination hoãn |
| Q-003 | Auth và private storage dùng phương án nào? | Dữ liệu mật | Phương án trong tech stack được duyệt | Chặn real-data use | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |
| Q-004 | Retention/deletion/backup policy là gì? | Privacy/operations | Thời hạn và SLA do Human xác nhận | Chặn security acceptance | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |
| Q-005 | Model/retrieval/retry/timeout/output budget là gì? | AI runtime | Cấu hình được Human phê duyệt | Schema/prompt/runtime tests | 21/09/2026 | Resolved for Extraction Runtime v1: `gpt-5.6-sol`, no retrieval, SDK retries 2, timeout 180, 48.000 tokens; future runtimes remain separate |
| Q-006 | Nếu mở lại Claims sau MVP/scope change, loại/số lượng nào? | Claims ngoài MVP và canonical contracts hiện hành | `[CẦN XÁC NHẬN]` trong task tương lai | Không chặn APP-001; ảnh hưởng prompt/template/schema tương lai | `[CẦN XÁC NHẬN]` | Current MVP: EXCLUDED; phạm vi tương lai chưa quyết định |
| Q-007 | PDF/QA report/claim mapping có thuộc MVP? | Optional output | Include / Exclude / Post-MVP | Workload trước deadline | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |

## 20. Pending Reviews

| Review ID | Artefact | Version | Reviewer | Status | Blocking |
|---|---|---|---|---|---|
| REV-001 | `docs/system-specification.md` | Reviewed baseline at `595113a6c5337a78b72ff4887383ef4a2b2ef49e`; resolved as 0.3.0 | Gemini 3.1 Pro High | CLOSED — PASS WITH HUMAN DECISIONS REQUIRED; decisions recorded | No |
| REV-002 | `AGENTS.md` | Reviewed baseline at `595113a6c5337a78b72ff4887383ef4a2b2ef49e`; resolved as 0.2.0 | Gemini 3.1 Pro High | CLOSED — PASS WITH HUMAN DECISIONS REQUIRED; decisions recorded | No |
| REV-003 | `PROJECT_CONTEXT.md` | Reviewed baseline at `595113a6c5337a78b72ff4887383ef4a2b2ef49e`; resolved as 0.3.0 | Gemini 3.1 Pro High | CLOSED — PASS WITH HUMAN DECISIONS REQUIRED; decisions recorded | No |
| REV-004 | Hai operational documents | Project Control Center 0.2.5; Review Log 0.2.3 | Gemini Pro + Human | Not started | No |
| REV-AI-001 | Output Schema v1.0.0 và ADR-006 | 1.0.0 / ADR-006 | Gemini 3.1 Pro | CLOSED — merged via PR #1 | No |
| REV-AI-002 | Extraction Prompt v1.0.0 và ADR-007 | 1.0.0 / ADR-007 | Gemini 3.1 Pro High | CLOSED — merged via PR #3 | No |
| REV-AI-003 | Patent Draft Contract v1.0.0, Draft Generation Prompt v1.0.0 và ADR-008 | 1.0.0 / ADR-008 | Gemini 3.1 Pro High | CLOSED — merged via PR #5 | No |
| REV-DOC-001 | Patent DOCX Template v1.0.0, renderer, fixtures, tests và ADR-009 | 1.0.0 / ADR-009 | Gemini 3.1 Pro High + Human visual QA | CLOSED — merged via PR #7 | No |
| REV-APP-001 | FastAPI Backend Skeleton and Secure Document Upload | Implementation head `bd39b9f7bdd9f7a1796d9a405e7998070e124e07`; resolved by merge `0df4814ff1eb8cd576566ac3dd403131feca3759` | Gemini 3.1 Pro High | CLOSED — PASS; merged via PR #10 | No |
| REV-APP-002 | Document Parsing & Evidence Source Units | Initial `477b8fda6afbae0049d8d691c213dc6355ba67da`; remediation `8b6f909a0f5787d72c002e163395656a666c9b78`; resolved by merge `4a001d116cbf002bdd42a9151efbf3f308fce3e6` | Gemini 3.1 Pro High | CLOSED — initial REQUEST CHANGES; F-001/F-002 RESOLVED; final PASS; merged via PR #12 | No |
| REV-AI-RUNTIME-001 | OpenAI extraction runtime, adapter, validators, tests and ADR-010 | Implementation branch `feat/ai-runtime-001-openai-extraction` | Gemini 3.1 Pro High | PENDING — implementation awaiting independent review | Yes — merge gate |

## 21. Recent Decisions

Human đã phê duyệt ADR-006 và Output Schema v1.0.0 cho AI-001, sau đó merge PR #1 ngày 19/09/2026. Human cũng đã phê duyệt AI-002/ADR-007, AI-003/ADR-008 và DOC-001/ADR-009 theo bằng chứng merge hiện có. Ngày 20/09/2026, Human phê duyệt SPEC-001/002/003 là baseline, accept ADR-001…005 và chốt upload APP-001. Ngày 21/09/2026, Human approve/merge APP-002 qua PR #12, sau đó phê duyệt AI-RUNTIME-001 Specification v1.0.0 và ADR-010: Responses API, `gpt-5.6-sol`, reasoning high, `store=false`, không retrieval, timeout 180, SDK retries 2 và 48.000 output tokens. Quyết định này chỉ áp dụng Extraction Runtime v1 và không phê duyệt frontend, public analyze endpoint, draft runtime, database/auth, production storage hoặc deployment.

| Decision ID | Human decision ngày 20/09/2026 | Trạng thái |
|---|---|---|
| DEC-001 | Phê duyệt SPEC-001/002/003 là baseline hiện hành | Recorded |
| DEC-002 | Accept nguyên trạng ADR-001…005 theo phạm vi từng ADR | Recorded |
| DEC-003 | Khóa upload/local single-tenant ephemeral scope, synthetic-only và retention tối đa 1 giờ cho APP-001 | Recorded and implemented in APP-001; merged via PR #10 |
| DEC-004 | Phê duyệt AI-RUNTIME-001 Specification v1.0.0 và runtime configuration tại baseline `f8070a5c94290ff44c65bc1b0831458662e14e11` | Recorded and implemented; awaiting independent review |

## 22. Next Recommended Action

1. Gemini 3.1 Pro High independent implementation review AI-RUNTIME-001.
2. Human xử lý finding và quyết định merge sau review; task kế tiếp `NOT STARTED — Awaiting Human assignment`.
3. Không đánh dấu toàn bộ Phase 1, Phase 2 hoặc MVP `Completed` khi chưa có bằng chứng và Human decision riêng.
4. Chỉ xử lý public orchestration, auth/private storage, production retention, draft runtime, frontend và claims theo task/approval riêng.

## 23. Last Updated

**21/09/2026 GMT+7**
