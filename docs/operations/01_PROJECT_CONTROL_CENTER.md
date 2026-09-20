# AI IP Generator – Project Control Center

> Bản nguồn Markdown được quản lý trong Git. Tên Google Doc đích: `01_PROJECT_CONTROL_CENTER`. Trạng thái đồng bộ Google Drive: `[CẦN XÁC NHẬN TRẠNG THÁI]`.

## 1. Document Metadata

| Thuộc tính | Giá trị |
|---|---|
| Document ID | OPS-001 |
| Document title | AI IP Generator – Project Control Center |
| Version | 0.2.10 |
| Status | Draft |
| Owner | Human / Product Owner |
| Author | ChatGPT/Codex |
| Reviewer | Gemini Pro |
| Created date | 18/09/2026 |
| Last updated | 20/09/2026 GMT+7 |
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

Trạng thái Human phê duyệt phase: **[CẦN XÁC NHẬN TRẠNG THÁI]**.

## 6. Current Objective

- Chốt system specification.
- Chốt project context.
- Chốt AI collaboration protocol.
- Chốt output schema.
- Chốt prompt specification.
- Chốt phạm vi Draft Claims.
- Chốt template DOCX.

Các mục trên chưa được coi là đã chốt chỉ vì có tài liệu Draft.

## 7. Overall Progress

- [x] Khởi tạo local Git repository.
- [x] Xác minh GitHub repository và Private visibility.
- [x] Publish bộ 5 artefact cùng README lên nhánh `main` trong commit đồng bộ này.
- [x] Tạo và cập nhật bản Draft `docs/system-specification.md` 0.2.6.
- [x] Tạo và cập nhật bản Draft `AGENTS.md` 0.1.1.
- [x] Tạo và cập nhật bản Draft `PROJECT_CONTEXT.md` 0.2.10.
- [x] Tạo và cập nhật bản nguồn Draft Project Control Center 0.2.10.
- [x] Tạo và cập nhật bản nguồn Gemini Review Log 0.2.6.
- [ ] Human review/phê duyệt specification và context.
- [ ] Gemini review chính thức các artefact hiện hành.
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
- [ ] Chốt phạm vi Draft Claims.
- [x] Triển khai Patent DOCX Template v1.0.0, mapping, renderer, synthetic fixtures và automated tests.
- [x] Human Microsoft Word Visual QA DOC-001: PASS, không có finding.
- [x] Gemini 3.1 Pro High independent review DOC-001: PASS, không có finding hoặc required change; recommendation `APPROVE`.
- [ ] Human merge approval cho DOC-001; implementation commit, Pull Request và merge commit chưa tồn tại.
- [ ] Khởi tạo application code.
- [ ] Chạy core pipeline end-to-end.
- [ ] Evaluation, stabilization, deployment và handover.

Các ô `[x]` chỉ xác nhận bằng chứng được nêu ngay trên từng dòng; không suy rộng thành Human/Gemini approval cho các artefact hoặc phase khác.

## 8. Completed

AI-001, AI-002 và AI-003 là các hạng mục đã được Human xác nhận `Completed`. Không có bằng chứng để đánh dấu toàn bộ Phase 1 hoặc các SPEC-001/002/003 là đã review/hoàn thành.

Các deliverable Draft đã tạo, có bằng chứng file:

| Task ID | Deliverable | Evidence | Kết luận được phép |
|---|---|---|---|
| SPEC-001 | System Specification 0.2.6 | `docs/system-specification.md` trên branch DOC-001 | Draft updated; pending SPEC review |
| SPEC-002 | Project Context 0.2.10 | `PROJECT_CONTEXT.md` trên branch DOC-001 | Draft updated; pending SPEC review |
| SPEC-003 | AI Collaboration Rules 0.1.1 | `AGENTS.md` trên GitHub `main` | Draft produced; pending review |
| SPEC-004 | Project Control Center source 0.2.10 | File hiện tại trên branch DOC-001 | Draft updated; Google Doc sync pending confirmation |
| REVIEW-001 | Gemini Review Log source 0.2.6 | `docs/operations/02_GEMINI_REVIEW_LOG.md` | `REV-AI-001`, `REV-AI-002` và `REV-AI-003` CLOSED; `REV-DOC-001` MERGE PENDING; SPEC-001/002/003 vẫn pending |
| AI-001 | Output Schema v1.0.0 | PR [#1](https://github.com/nshaokiet/ai-ip-description-generator/pull/1), merge commit `49efead593437dfc5c88397ea6f335a2d4ff84d7`, 19/09/2026; Gemini review PASS; 15/15 tests pass; không có finding | Completed — Merged via PR #1 |
| AI-002 | Extraction Prompt v1.0.0 | PR [#3](https://github.com/nshaokiet/ai-ip-description-generator/pull/3), merge commit `8f2b7082881961cc1a2cf7fa56ece81976759c7f`, 19/09/2026; implementation `f8772b228a23bf7cdec10fa0c463e6d1f672c341`; governance `9f2a78b1396cdadb747c263a2bbbbacb8d7f4292`; Gemini review PASS; AI-001 15/15 và AI-002 17/17 tests pass; không có finding | Completed — Merged via PR #3 |
| AI-003 | Patent Draft Generation Contract v1.0.0 | PR [#5](https://github.com/nshaokiet/ai-ip-description-generator/pull/5), implementation `ae7e8fb573ea4681a9db1bafa711d19a3c598666`, merge commit `fb522bc5ecbb5ad66bab6226fa88ae51020cef52`, 20/09/2026; Gemini reviews PASS; 57/57 tests pass; không có finding hoặc required change | Completed — Merged via PR #5 |

## 9. In Progress

| Task ID | Công việc | Owner | Reviewer | Status | Evidence/Blocker |
|---|---|---|---|---|---|
| SPEC-001 | Review và chốt system specification | Human / Product Owner | Gemini Pro | Pending review | Draft 0.1.0 tồn tại |
| SPEC-002 | Review và chốt project context | Human / Product Owner | Gemini Pro | Pending review | Draft 0.1.1 tồn tại |
| SPEC-003 | Review và chốt AGENTS.md | Human / Product Owner | Gemini Pro | Pending review | Draft 0.1.1 tồn tại |
| SPEC-004 | Đồng bộ Project Control Center sang Google Docs | Human / Product Owner | ChatGPT/Codex | `[CẦN XÁC NHẬN TRẠNG THÁI]` | Chưa có bằng chứng Google Doc/link |
| REVIEW-001 | Đồng bộ Gemini Review Log và thực hiện review cho các SPEC còn lại | Gemini Pro | Human / Product Owner | Pending | `REV-AI-001` đã đóng; SPEC-001/002/003 chưa có review evidence |
| DOC-001 | Patent DOCX Template v1.0.0 | ChatGPT/Codex | Gemini 3.1 Pro High + Human | Gemini Review Passed — Awaiting Human Merge Approval | Human Visual QA PASS; Gemini independent review PASS; 85/85 tests pass; không có finding/required change; chưa có implementation commit, PR hoặc merge commit |

## 10. Next Tasks

| Task ID | Task | Owner | Reviewer | Priority | Status | Dependency | Target date |
|---|---|---|---|---|---|---|---|
| REVIEW-001 | Review 3 artefact kỹ thuật hiện hành | Gemini Pro | Human / Product Owner | High | Not started | SPEC-001/002/003 Draft | `[CẦN XÁC NHẬN]` |
| ADR-001 | Quyết định FastAPI backend | ChatGPT/Codex đề xuất; Human phê duyệt | Gemini Pro | High | Proposed | System spec review | `[CẦN XÁC NHẬN]` |
| ADR-002 | Quyết định OpenAI Responses API cho MVP | ChatGPT/Codex đề xuất; Human phê duyệt | Gemini Pro | High | Proposed | Data/vendor review | `[CẦN XÁC NHẬN]` |
| ADR-003 | Ghi nhận Gemini chỉ là reviewer | ChatGPT/Codex đề xuất; Human phê duyệt | Gemini Pro | Medium | Proposed | AGENTS review | `[CẦN XÁC NHẬN]` |
| ADR-004 | Ghi nhận GitHub là Technical Source of Truth | ChatGPT/Codex đề xuất; Human phê duyệt | Gemini Pro | High | Proposed | AGENTS review | `[CẦN XÁC NHẬN]` |
| ADR-005 | Ghi nhận Human review bắt buộc | ChatGPT/Codex đề xuất; Human phê duyệt | Gemini Pro | Critical | Proposed | Legal/product review | `[CẦN XÁC NHẬN]` |
| DOC-001 | Human merge decision cho Patent DOCX Template v1.0.0 | ChatGPT/Codex | Gemini 3.1 Pro High + Human | High | Gemini Review Passed — Awaiting Human Merge Approval | AI-003 Completed; Human Visual QA/Gemini review PASS; `REV-DOC-001` MERGE PENDING; snapshot chưa commit/PR | Trước 30/09/2026 |

Mọi target date cụ thể cần được xếp trước deadline chung 02/10/2026 và do Human xác nhận.

## 11. Current Blockers

| Blocker ID | Blocker | Ảnh hưởng | Owner quyết định | Status |
|---|---|---|---|---|
| BLK-002 | Chưa xác nhận OCR/scanned PDF | Chưa khóa parser scope | Human / Product Owner | Open |
| BLK-003 | Chưa chốt auth/private storage/retention | Không nên dùng dữ liệu nghiên cứu thật | Human / Product Owner | Open |
| BLK-004 | Chưa chốt model, retrieval, retry, timeout, cost | Chưa khóa AI runtime design | Human / Product Owner | Open |
| BLK-005 | Chưa chốt phạm vi Draft Claims tương lai | Không chặn AI-001, AI-002, claim-free AI-003 hoặc claim-free DOC-001; chỉ ảnh hưởng task claims riêng nếu được phê duyệt sau | Human + chuyên gia SHTT | Open — non-blocker for AI-001/AI-002/AI-003/DOC-001 |
| BLK-006 | Chưa có review chính thức cho SPEC-001/002/003 | Các SPEC Draft này chưa có independent QA; không ảnh hưởng kết luận review riêng của AI-001 | Gemini Pro | Open |
| BLK-007 | Chưa có bằng chứng Google Docs được tạo/đồng bộ | Operational bridge chưa sẵn sàng trên Drive | Human / Product Owner | Open |

## 12. Architecture Decisions

| ID | Date | Decision | Reason | Alternatives | Approver | Status | Related artefact |
|---|---|---|---|---|---|---|---|
| ADR-001 | 18/09/2026 | Use FastAPI backend | Phù hợp tech stack đã định hướng và Python AI/document pipeline | `[CẦN XÁC NHẬN]` | Human / Product Owner | PROPOSED | `docs/system-specification.md` |
| ADR-002 | 18/09/2026 | Use OpenAI Responses API for MVP | Production AI đã định hướng, hỗ trợ Structured Outputs | `[CẦN XÁC NHẬN]` | Human / Product Owner | PROPOSED | `docs/system-specification.md` |
| ADR-003 | 18/09/2026 | Gemini acts as reviewer, not production AI dependency | Tách implementation và independent review | Gemini runtime dependency | Human / Product Owner | PROPOSED | `AGENTS.md` |
| ADR-004 | 18/09/2026 | GitHub is Technical Source of Truth | Version control và traceability | Google Drive làm technical source | Human / Product Owner | PROPOSED | `AGENTS.md` |
| ADR-005 | 18/09/2026 | Human review is mandatory | Giảm hallucination/rủi ro pháp lý và kỹ thuật | Fully automated approval | Human / Product Owner | PROPOSED | Tất cả artefact |
| ADR-006 | 18/09/2026 | JSON Schema Draft 2020-12, strict Output Schema v1.0.0; loại claims và Human confirmation state | Tạo contract kiểm thử được, đúng phạm vi AI-001 | Schema lỏng; claims optional; Human confirmation trong payload | Human / Product Owner | ACCEPTED | `docs/decisions/ADR-006-output-schema-v1.md` |
| ADR-007 | 19/09/2026 | Extraction Prompt v1.0.0 dùng normalized JSON envelope và canonical offline validation; hoãn provider adapter/live evaluation | Tách prompt contract khỏi runtime/provider concerns và giữ schema hiện hành | Truyền schema nguyên trạng; sửa schema; tạo adapter ngay | Human / Product Owner | ACCEPTED — COMPLETED — MERGED VIA PR #3 | `docs/decisions/ADR-007-extraction-prompt-v1.md` |
| ADR-008 | 19/09/2026 | Thêm strict Patent Draft Generation Contract v1.0.0 giữa validated analysis và DOCX; không claims; offline-only validation | Tách extraction, technical drafting và presentation; giữ paragraph-level evidence traceability | Render Output Schema trực tiếp; sửa Output Schema; free-form draft | Human / Product Owner | ACCEPTED — COMPLETED — MERGED VIA PR #5 | `docs/decisions/ADR-008-patent-draft-contract-v1.md` |
| ADR-009 | 20/09/2026 | Dùng versioned `docxtpl` template và deterministic offline renderer cho DOCX claim-free | Tách presentation khỏi drafting contract; giữ mapping, escaping, evidence và visual-review gate | Procedural-only DOCX; render trực tiếp Output Schema; PDF; auto-generated figures | Human / Product Owner | ACCEPTED — IMPLEMENTED — AWAITING REVIEW | `docs/decisions/ADR-009-patent-docx-template-v1.md` |

ADR-006, ADR-007, ADR-008 và ADR-009 đã được Human phê duyệt; ADR-001 đến ADR-005 vẫn chỉ là `PROPOSED`.

## 13. Current AI Assignments

| Task ID | Task | Owner | Reviewer | Status | Expected output |
|---|---|---|---|---|---|
| SPEC-001 | System Specification Draft | ChatGPT/Codex | Gemini Pro + Human | Ready for review | `docs/system-specification.md` 0.2.6 |
| SPEC-002 | Project Context Draft | ChatGPT/Codex | Gemini Pro + Human | Ready for review | `PROJECT_CONTEXT.md` 0.2.10 |
| SPEC-003 | AGENTS.md Draft | ChatGPT/Codex | Gemini Pro + Human | Ready for review | `AGENTS.md` 0.1.1 |
| SPEC-004 | Control Center source | ChatGPT/Codex | Human | Ready for review | File hiện tại 0.2.10 |
| REVIEW-001 | Review Log | ChatGPT/Codex | Gemini Pro + Human | Active | `02_GEMINI_REVIEW_LOG.md` 0.2.6; `REV-AI-001`, `REV-AI-002` và `REV-AI-003` CLOSED; `REV-DOC-001` MERGE PENDING |
| AI-001 | Output Schema v1.0.0 | ChatGPT/Codex | Gemini 3.1 Pro | Completed — Merged via PR #1 | Merge commit `49efead593437dfc5c88397ea6f335a2d4ff84d7`; Gemini review PASS; 15/15 tests pass; không có finding |
| AI-002 | Extraction Prompt v1.0.0 | ChatGPT/Codex | Gemini 3.1 Pro High | Completed — Merged via PR #3 | Merge commit `8f2b7082881961cc1a2cf7fa56ece81976759c7f`; implementation `f8772b228a23bf7cdec10fa0c463e6d1f672c341`; governance `9f2a78b1396cdadb747c263a2bbbbacb8d7f4292`; 15/15 regression và 17/17 AI-002 tests pass |
| AI-003 | Patent Draft Generation Contract v1.0.0 | ChatGPT/Codex | Gemini 3.1 Pro High | Completed — Merged via PR #5 | Implementation `ae7e8fb573ea4681a9db1bafa711d19a3c598666`; merge `fb522bc5ecbb5ad66bab6226fa88ae51020cef52`; 57/57 tests pass |
| DOC-001 | Patent DOCX Template v1.0.0 | ChatGPT/Codex | Gemini 3.1 Pro High + Human | Gemini Review Passed — Awaiting Human Merge Approval | Human Visual QA PASS; Gemini independent review PASS; 85/85 tests pass; generated representative DOCX remains ignored; no implementation commit/PR/merge yet |

## 14. Latest ChatGPT/Codex Handoff

```text
Task ID: DOC-001
Agent: ChatGPT/Codex
Reviewer: Gemini 3.1 Pro High
Status: Gemini Review Passed — Awaiting Human Merge Approval
Version: Patent DOCX Template 1.0.0
Work completed: Canonical DOCX template, manifest, mapping, deterministic offline renderer, three synthetic fixtures, automated tests, ADR-009 và supporting documentation đã được triển khai; Human Visual QA và Gemini independent review đều PASS.
Files affected: Chính xác 19 approved paths; generated representative DOCX được Git ignore và không thuộc diff.
Evidence checked: Python 3.12.10; jsonschema 4.26.0; docxtpl 0.20.2; python-docx 1.2.0; AI-001 15/15, AI-002 17/17, AI-003 25/25 và DOC-001 28/28 tests pass; Human Microsoft Word Visual QA PASS; Gemini package/renderer/mapping/contract/layout/fixtures/scope/security review PASS; git diff --check pass.
Findings: Không có.
Decisions: Gemini recommendation `APPROVE`; Human merge decision chưa được thực hiện.
Issues: Implementation commit, Pull Request và merge commit chưa tồn tại; DOC-001 chưa `Completed`.
Security impact: Fixtures synthetic; renderer offline; autoescape enabled; no macro, active content, remote relationship, secret, PII hoặc dữ liệu nghiên cứu thật.
Recommended next action: Gemini targeted review governance update; sau đó Human / Product Owner quyết định commit, Pull Request và merge theo task riêng.
```

## 15. Latest Gemini Handoff

```text
Task ID: AI-003
Agent: Gemini 3.1 Pro High
Reviewer: Human / Product Owner
Status: CLOSED — AI-003 Completed — Merged via PR #5
Version: Patent Draft Generation Contract 1.0.0; Draft Generation Prompt 1.0.0; implementation ae7e8fb573ea4681a9db1bafa711d19a3c598666; resolved by merge fb522bc5ecbb5ad66bab6226fa88ae51020cef52
Work completed: Independent read-only review hoàn tất với verdict PASS; không có finding hoặc required change.
Files affected: Review only; production artefact không bị Gemini ghi đè.
Evidence checked: Python 3.12.10; jsonschema 4.26.0; AI-001 15/15 pass; AI-002 17/17 pass; AI-003 25/25 pass; schema/contract, business-validation, prompt/security, fixture và scope/governance reviews PASS.
Findings: Không có.
Decisions: Recommendation APPROVE; Human / Product Owner approved and merged PR #5 on 20/09/2026.
Issues: Không có finding hoặc required change; provider integration, live-model evaluation và DOCX rendering vẫn ngoài phạm vi AI-003.
Security impact: PASS; không phát hiện secret, cache, PII hoặc dữ liệu nghiên cứu thật trong phạm vi review.
Recommended next action: Targeted review post-merge governance closeout; DOC-001 preparation/approval chỉ theo task riêng.
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

## 17. Prompt and Schema Versions

| Artefact | Current version | Status | Owner | Reviewer | Last updated |
|---|---|---|---|---|---|
| Extraction prompt | 1.0.0 | Completed — Merged via PR #3 | ChatGPT/Codex | Gemini 3.1 Pro High | 19/09/2026 |
| Draft generation prompt | 1.0.0 | Completed — Merged via PR #5 | ChatGPT/Codex | Gemini 3.1 Pro High | 20/09/2026 |
| Invention JSON Schema | 1.0.0 | Completed — Merged via PR #1 | ChatGPT/Codex | Gemini 3.1 Pro | 19/09/2026 |
| Patent Draft JSON Schema | 1.0.0 | Completed — Merged via PR #5 | ChatGPT/Codex | Gemini 3.1 Pro High | 20/09/2026 |
| DOCX template | 1.0.0 | Gemini Review Passed — Awaiting Human Merge Approval | ChatGPT/Codex | Gemini 3.1 Pro High + Human | 20/09/2026 |
| API contract | Concept trong SPEC-001 | Draft only | ChatGPT/Codex | Gemini Pro | 18/09/2026 |

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
| Q-001 | Có OCR/scanned PDF trong MVP không? | Parser scope | Có / Không / Post-MVP | Timeline, dependency, quality | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |
| Q-002 | Giới hạn file/page là bao nhiêu? | Upload/performance | Giá trị do Human xác nhận | Validation và cost | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |
| Q-003 | Auth và private storage dùng phương án nào? | Dữ liệu mật | Phương án trong tech stack được duyệt | Chặn real-data use | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |
| Q-004 | Retention/deletion/backup policy là gì? | Privacy/operations | Thời hạn và SLA do Human xác nhận | Chặn security acceptance | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |
| Q-005 | Model/retrieval/retry/timeout/cost limit là gì? | AI runtime | Cấu hình được Human phê duyệt | Schema/prompt/runtime tests | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |
| Q-006 | Draft Claims gồm loại/số lượng nào? | Patent output tương lai; claims không thuộc Output Schema v1.0.0 | `[CẦN XÁC NHẬN]` | Không chặn AI-001; ảnh hưởng prompt/template/schema tương lai | `[CẦN XÁC NHẬN]` | AI-001: EXCLUDED; phạm vi tương lai chưa quyết định |
| Q-007 | PDF/QA report/claim mapping có thuộc MVP? | Optional output | Include / Exclude / Post-MVP | Workload trước deadline | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |

## 20. Pending Reviews

| Review ID | Artefact | Version | Reviewer | Status | Blocking |
|---|---|---|---|---|---|
| REV-001 | `docs/system-specification.md` | 0.2.1 | Gemini Pro | Not started | Yes |
| REV-002 | `AGENTS.md` | 0.1.1 | Gemini Pro | Not started | Yes |
| REV-003 | `PROJECT_CONTEXT.md` | 0.2.5 | Gemini Pro | Not started | Yes |
| REV-004 | Hai operational documents | Project Control Center 0.2.5; Review Log 0.2.3 | Gemini Pro + Human | Not started | No |
| REV-AI-001 | Output Schema v1.0.0 và ADR-006 | 1.0.0 / ADR-006 | Gemini 3.1 Pro | CLOSED — merged via PR #1 | No |
| REV-AI-002 | Extraction Prompt v1.0.0 và ADR-007 | 1.0.0 / ADR-007 | Gemini 3.1 Pro High | CLOSED — merged via PR #3 | No |
| REV-AI-003 | Patent Draft Contract v1.0.0, Draft Generation Prompt v1.0.0 và ADR-008 | 1.0.0 / ADR-008 | Gemini 3.1 Pro High | CLOSED — merged via PR #5 | No |
| REV-DOC-001 | Patent DOCX Template v1.0.0, renderer, fixtures, tests và ADR-009 | 1.0.0 / ADR-009 | Gemini 3.1 Pro High + Human visual QA | MERGE PENDING | Yes |

## 21. Recent Decisions

Human đã phê duyệt ADR-006 và Output Schema v1.0.0 cho AI-001, sau đó merge PR #1 ngày 19/09/2026. Human cũng đã phê duyệt AI-002 và ADR-007 rồi merge PR #3 ngày 19/09/2026. Với AI-003 và ADR-008, Gemini review `PASS`, không có finding hoặc required change; Human đã approve và merge PR #5 ngày 20/09/2026 tại `fb522bc5ecbb5ad66bab6226fa88ae51020cef52`. Human Microsoft Word Visual QA cho DOC-001 `PASS`; Gemini 3.1 Pro High independent review `PASS`, không có finding hoặc required change, recommendation `APPROVE`. DOC-001 chưa có implementation commit, Pull Request hoặc merge commit và đang chờ Human merge approval. Các ADR-001 đến ADR-005 vẫn chỉ là `PROPOSED`.

## 22. Next Recommended Action

1. Gemini thực hiện targeted review cho governance update và `REV-DOC-001`.
2. Sau targeted review, Human / Product Owner quyết định commit, Pull Request và merge theo task riêng.
3. Không đánh dấu DOC-001 hoặc Phase 1 `Completed` trước Human merge decision.
4. Chỉ bắt đầu provider adapter/live-model evaluation sau task approval riêng.
5. Tiếp tục xử lý các blocker dữ liệu, runtime và claims tương lai.

## 23. Last Updated

**20/09/2026 GMT+7**
