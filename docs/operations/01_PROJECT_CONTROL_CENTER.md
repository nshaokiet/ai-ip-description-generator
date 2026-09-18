# AI IP Generator – Project Control Center

> Bản nguồn Markdown được quản lý trong Git. Tên Google Doc đích: `01_PROJECT_CONTROL_CENTER`. Trạng thái đồng bộ Google Drive: `[CẦN XÁC NHẬN TRẠNG THÁI]`.

## 1. Document Metadata

| Thuộc tính | Giá trị |
|---|---|
| Document ID | OPS-001 |
| Document title | AI IP Generator – Project Control Center |
| Version | 0.1.1 |
| Status | Draft |
| Owner | Human / Product Owner |
| Author | ChatGPT/Codex |
| Reviewer | Gemini Pro |
| Created date | 18/09/2026 |
| Last updated | 18/09/2026 10:49 GMT+7 |
| Related task ID | SPEC-004 |
| Source of Truth | Operational status bridge; bản nguồn Git tại `docs/operations/01_PROJECT_CONTROL_CENTER.md` |
| Confidentiality level | Internal |

### Lịch sử phiên bản

| Phiên bản cũ | Phiên bản mới | Ngày | Người thực hiện | Thay đổi | Lý do | Finding/Decision liên quan | Breaking change |
|---|---|---|---|---|---|---|---|
| Chưa có | 0.1.0 | 18/09/2026 | ChatGPT/Codex | Tạo Project Control Center ban đầu | Khởi tạo điều phối Phase 1 | SPEC-004 | No |
| 0.1.0 | 0.1.1 | 18/09/2026 | ChatGPT/Codex | Cập nhật GitHub URL, Private visibility và trạng thái publish | Đồng bộ operational status với repository thực tế | Yêu cầu Human đưa artefact lên GitHub | No |

## 2. Project

**AI Intellectual Property Description Generator**

Mục tiêu: chuyển một bài báo PDF/DOCX thành Structured JSON có evidence, thông tin thiếu, bản dự thảo patent specification cần Human review và DOCX.

## 3. Repository

`ai-ip-description-generator`

- GitHub remote URL: `https://github.com/nshaokiet/ai-ip-description-generator`.
- Default branch: `main`.
- GitHub repository visibility: **Private**, đã xác minh ngày 18/09/2026.

## 4. Deadline

**02/10/2026 — ngày 02 tháng 10 năm 2026**

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
- [x] Tạo bản Draft `docs/system-specification.md` 0.1.0.
- [x] Tạo và cập nhật bản Draft `AGENTS.md` 0.1.1.
- [x] Tạo và cập nhật bản Draft `PROJECT_CONTEXT.md` 0.1.1.
- [x] Tạo và cập nhật bản nguồn Draft Project Control Center 0.1.1.
- [x] Tạo bản nguồn Draft Gemini Review Log 0.1.0.
- [ ] Human review/phê duyệt specification và context.
- [ ] Gemini review chính thức các artefact hiện hành.
- [ ] Tạo/phê duyệt ADR.
- [ ] Tạo/phê duyệt output schema v1.
- [ ] Tạo/phê duyệt prompt specification v1.
- [ ] Chốt phạm vi Draft Claims.
- [ ] Tạo/phê duyệt DOCX template v1.
- [ ] Khởi tạo application code.
- [ ] Chạy core pipeline end-to-end.
- [ ] Evaluation, stabilization, deployment và handover.

Các ô `[x]` chỉ xác nhận file hoặc repository local tồn tại; không có nghĩa nội dung đã được Human/Gemini approve.

## 8. Completed

Chưa có hạng mục production hoặc phase nào được Human xác nhận `Completed`.

Các deliverable Draft đã tạo, có bằng chứng file:

| Task ID | Deliverable | Evidence | Kết luận được phép |
|---|---|---|---|
| SPEC-001 | System Specification 0.1.0 | `docs/system-specification.md` trên GitHub `main` | Draft produced; pending review |
| SPEC-002 | Project Context 0.1.1 | `PROJECT_CONTEXT.md` trên GitHub `main` | Draft produced; pending review |
| SPEC-003 | AI Collaboration Rules 0.1.1 | `AGENTS.md` trên GitHub `main` | Draft produced; pending review |
| SPEC-004 | Project Control Center source 0.1.1 | File hiện tại trên GitHub `main` | Draft produced; Google Doc sync pending confirmation |
| REVIEW-001 | Gemini Review Log source 0.1.0 | `docs/operations/02_GEMINI_REVIEW_LOG.md` | Template produced; chưa có review entry |

## 9. In Progress

| Task ID | Công việc | Owner | Reviewer | Status | Evidence/Blocker |
|---|---|---|---|---|---|
| SPEC-001 | Review và chốt system specification | Human / Product Owner | Gemini Pro | Pending review | Draft 0.1.0 tồn tại |
| SPEC-002 | Review và chốt project context | Human / Product Owner | Gemini Pro | Pending review | Draft 0.1.1 tồn tại |
| SPEC-003 | Review và chốt AGENTS.md | Human / Product Owner | Gemini Pro | Pending review | Draft 0.1.1 tồn tại |
| SPEC-004 | Đồng bộ Project Control Center sang Google Docs | Human / Product Owner | ChatGPT/Codex | `[CẦN XÁC NHẬN TRẠNG THÁI]` | Chưa có bằng chứng Google Doc/link |
| REVIEW-001 | Đồng bộ Gemini Review Log và thực hiện review đầu tiên | Gemini Pro | Human / Product Owner | Pending | Chưa có review entry chính thức |

## 10. Next Tasks

| Task ID | Task | Owner | Reviewer | Priority | Status | Dependency | Target date |
|---|---|---|---|---|---|---|---|
| REVIEW-001 | Review 3 artefact kỹ thuật hiện hành | Gemini Pro | Human / Product Owner | High | Not started | SPEC-001/002/003 Draft | `[CẦN XÁC NHẬN]` |
| ADR-001 | Quyết định FastAPI backend | ChatGPT/Codex đề xuất; Human phê duyệt | Gemini Pro | High | Proposed | System spec review | `[CẦN XÁC NHẬN]` |
| ADR-002 | Quyết định OpenAI Responses API cho MVP | ChatGPT/Codex đề xuất; Human phê duyệt | Gemini Pro | High | Proposed | Data/vendor review | `[CẦN XÁC NHẬN]` |
| ADR-003 | Ghi nhận Gemini chỉ là reviewer | ChatGPT/Codex đề xuất; Human phê duyệt | Gemini Pro | Medium | Proposed | AGENTS review | `[CẦN XÁC NHẬN]` |
| ADR-004 | Ghi nhận GitHub là Technical Source of Truth | ChatGPT/Codex đề xuất; Human phê duyệt | Gemini Pro | High | Proposed | AGENTS review | `[CẦN XÁC NHẬN]` |
| ADR-005 | Ghi nhận Human review bắt buộc | ChatGPT/Codex đề xuất; Human phê duyệt | Gemini Pro | Critical | Proposed | Legal/product review | `[CẦN XÁC NHẬN]` |
| AI-001 | Tạo `invention-schema-v1` | ChatGPT/Codex | Gemini Pro | Critical | Not started | Human decisions về output/claims | `[CẦN XÁC NHẬN]` |
| AI-002 | Tạo `extraction-prompt-v1` | ChatGPT/Codex | Gemini Pro | Critical | Not started | AI-001 Draft | `[CẦN XÁC NHẬN]` |
| DOC-001 | Tạo `patent-template-v1` | ChatGPT/Codex | Gemini Pro + Human | High | Not started | Claims/section decisions | `[CẦN XÁC NHẬN]` |

Mọi target date cụ thể cần được xếp trước deadline chung 02/10/2026 và do Human xác nhận.

## 11. Current Blockers

| Blocker ID | Blocker | Ảnh hưởng | Owner quyết định | Status |
|---|---|---|---|---|
| BLK-002 | Chưa xác nhận OCR/scanned PDF | Chưa khóa parser scope | Human / Product Owner | Open |
| BLK-003 | Chưa chốt auth/private storage/retention | Không nên dùng dữ liệu nghiên cứu thật | Human / Product Owner | Open |
| BLK-004 | Chưa chốt model, retrieval, retry, timeout, cost | Chưa khóa AI runtime design | Human / Product Owner | Open |
| BLK-005 | Chưa chốt phạm vi Draft Claims | Chưa thể khóa schema/prompt/template | Human + chuyên gia SHTT | Open |
| BLK-006 | Chưa có review chính thức từ Gemini | Các artefact hiện hành chưa có independent QA | Gemini Pro | Open |
| BLK-007 | Chưa có bằng chứng Google Docs được tạo/đồng bộ | Operational bridge chưa sẵn sàng trên Drive | Human / Product Owner | Open |

## 12. Architecture Decisions

| ID | Date | Decision | Reason | Alternatives | Approver | Status | Related artefact |
|---|---|---|---|---|---|---|---|
| ADR-001 | 18/09/2026 | Use FastAPI backend | Phù hợp tech stack đã định hướng và Python AI/document pipeline | `[CẦN XÁC NHẬN]` | Human / Product Owner | PROPOSED | `docs/system-specification.md` |
| ADR-002 | 18/09/2026 | Use OpenAI Responses API for MVP | Production AI đã định hướng, hỗ trợ Structured Outputs | `[CẦN XÁC NHẬN]` | Human / Product Owner | PROPOSED | `docs/system-specification.md` |
| ADR-003 | 18/09/2026 | Gemini acts as reviewer, not production AI dependency | Tách implementation và independent review | Gemini runtime dependency | Human / Product Owner | PROPOSED | `AGENTS.md` |
| ADR-004 | 18/09/2026 | GitHub is Technical Source of Truth | Version control và traceability | Google Drive làm technical source | Human / Product Owner | PROPOSED | `AGENTS.md` |
| ADR-005 | 18/09/2026 | Human review is mandatory | Giảm hallucination/rủi ro pháp lý và kỹ thuật | Fully automated approval | Human / Product Owner | PROPOSED | Tất cả artefact |

Không có ADR nào ở bảng trên được ghi `Approved`.

## 13. Current AI Assignments

| Task ID | Task | Owner | Reviewer | Status | Expected output |
|---|---|---|---|---|---|
| SPEC-001 | System Specification Draft | ChatGPT/Codex | Gemini Pro + Human | Ready for review | `docs/system-specification.md` 0.1.0 |
| SPEC-002 | Project Context Draft | ChatGPT/Codex | Gemini Pro + Human | Ready for review | `PROJECT_CONTEXT.md` 0.1.1 |
| SPEC-003 | AGENTS.md Draft | ChatGPT/Codex | Gemini Pro + Human | Ready for review | `AGENTS.md` 0.1.1 |
| SPEC-004 | Control Center source | ChatGPT/Codex | Human | Ready for review | File hiện tại 0.1.1 |
| REVIEW-001 | Review Log template | ChatGPT/Codex | Gemini Pro + Human | Ready for use | `02_GEMINI_REVIEW_LOG.md` 0.1.0 |

## 14. Latest ChatGPT/Codex Handoff

```text
Task ID: SPEC-001, SPEC-002, SPEC-003, SPEC-004, REVIEW-001
Agent: ChatGPT/Codex
Reviewer: Gemini Pro + Human / Product Owner
Status: Published to private GitHub main; pending Human/Gemini review and Google Docs sync
Version: 0.1.1 operational state
Work completed: Published five independent Draft artefacts, rewrote README and preserved the previous system specification in the archive.
Files affected: README.md; docs/system-specification.md; AGENTS.md; PROJECT_CONTEXT.md; docs/operations/01_PROJECT_CONTROL_CENTER.md; docs/operations/02_GEMINI_REVIEW_LOG.md; docs/archive/system-specification-before-2026-09-18.md
Evidence checked: GitHub repository metadata, Private visibility, main branch, file paths, required section coverage, consistency and commit result.
Findings: No official Gemini review exists; several product, security and claim-scope decisions remain open.
Decisions: No Human decision was invented or marked Approved.
Issues: Google Drive synchronization is not verified; Human decisions and Gemini review remain pending.
Security impact: Documentation only; no paper, credential, secret or application code added.
Recommended next action: Request Gemini review and Human decisions for the listed blockers, then synchronize the two operational documents to Google Docs.
```

## 15. Latest Gemini Handoff

```text
Task ID: REVIEW-001
Agent: Gemini Pro
Reviewer: Human / Product Owner
Status: Not started
Version: [CẦN XÁC NHẬN]
Work completed: Chưa có review entry chính thức.
Files affected: Không có.
Evidence checked: Chưa có.
Findings: Chưa có.
Decisions: Chưa có.
Issues: Gemini chưa thực hiện review chính thức trên các artefact hiện hành.
Security impact: Chưa đánh giá.
Recommended next action: Gemini đọc AGENTS.md, PROJECT_CONTEXT.md và docs/system-specification.md rồi tạo REV-001.
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

## 17. Prompt and Schema Versions

| Artefact | Current version | Status | Owner | Reviewer | Last updated |
|---|---|---|---|---|---|
| Extraction prompt | Chưa có | `[FILE CHƯA TỒN TẠI]` | ChatGPT/Codex | Gemini Pro | Chưa có |
| Draft generation prompt | Chưa có | `[FILE CHƯA TỒN TẠI]` | ChatGPT/Codex | Gemini Pro | Chưa có |
| Invention JSON Schema | Chưa có | `[FILE CHƯA TỒN TẠI]` | ChatGPT/Codex | Gemini Pro | Chưa có |
| DOCX template | Chưa có | `[FILE CHƯA TỒN TẠI]` | ChatGPT/Codex | Gemini Pro + Human | Chưa có |
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
| Q-006 | Draft Claims gồm loại/số lượng nào? | Patent output | `[CẦN XÁC NHẬN]` | Chặn schema/prompt/template | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |
| Q-007 | PDF/QA report/claim mapping có thuộc MVP? | Optional output | Include / Exclude / Post-MVP | Workload trước deadline | `[CẦN XÁC NHẬN]` | `[CẦN XÁC NHẬN]` |

## 20. Pending Reviews

| Review ID | Artefact | Version | Reviewer | Status | Blocking |
|---|---|---|---|---|---|
| REV-001 | `docs/system-specification.md` | 0.1.0 | Gemini Pro | Not started | Yes |
| REV-002 | `AGENTS.md` | 0.1.1 | Gemini Pro | Not started | Yes |
| REV-003 | `PROJECT_CONTEXT.md` | 0.1.1 | Gemini Pro | Not started | Yes |
| REV-004 | Hai operational templates | Project Control Center 0.1.1; Review Log 0.1.0 | Gemini Pro + Human | Not started | No |

## 21. Recent Decisions

**Chưa có quyết định chính thức được Human phê duyệt và ghi nhận trong repository.**

Các ADR-001 đến ADR-005 chỉ là `PROPOSED`.

## 22. Next Recommended Action

1. Human đọc mục 19 và ưu tiên trả lời Q-003, Q-004, Q-006 vì liên quan dữ liệu và cấu trúc output.
2. Gửi ba artefact kỹ thuật hiện hành cho Gemini review và ghi REV-001 đến REV-003 thật.
3. ChatGPT/Codex xử lý từng finding, tạo phiên bản mới khi cần.
4. Đồng bộ hai tài liệu vận hành sang Google Docs và ghi link sau khi xác minh.
5. Sau khi Human phê duyệt ADR/phạm vi, bắt đầu AI-001 (schema), AI-002 (prompt) và DOC-001 (template).

## 23. Last Updated

**18/09/2026 10:49 GMT+7**
