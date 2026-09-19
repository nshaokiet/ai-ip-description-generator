# Gemini Review Log

> Bản nguồn Markdown được quản lý trong Git. Tên Google Doc đích: `02_GEMINI_REVIEW_LOG`. Trạng thái đồng bộ Google Drive: `[CẦN XÁC NHẬN TRẠNG THÁI]`.

## 1. Document Metadata

| Thuộc tính | Giá trị |
|---|---|
| Document ID | REVIEW-001 |
| Document title | Gemini Review Log |
| Project | AI Intellectual Property Description Generator |
| Project deadline | 02/10/2026 |
| Version | 0.2.1 |
| Status | Active review log |
| Owner | Human / Product Owner |
| Author | ChatGPT/Codex |
| Reviewer | Gemini Pro |
| Created date | 18/09/2026 |
| Last updated | 19/09/2026 09:39 GMT+7 |
| Related task ID | REVIEW-001; AI-001 |
| Source of Truth | Review history; bản nguồn Git tại `docs/operations/02_GEMINI_REVIEW_LOG.md` |
| Confidentiality level | Internal; findings về research input có thể là Confidential |

### Lịch sử phiên bản

| Phiên bản cũ | Phiên bản mới | Ngày | Người thực hiện | Thay đổi | Lý do | Finding/Decision liên quan | Breaking change |
|---|---|---|---|---|---|---|---|
| Chưa có | 0.1.0 | 18/09/2026 | ChatGPT/Codex | Tạo review log format ban đầu | Khởi tạo quy trình independent review | REVIEW-001 | No |
| 0.1.0 | 0.2.0 | 18/09/2026 | ChatGPT/Codex | Ghi review entry AI-001 từ kết quả Gemini 3.1 Pro được Human xác nhận | Governance closeout trước merge | REV-AI-001, AI-001, PR #1 | No |
| 0.2.0 | 0.2.1 | 19/09/2026 | ChatGPT/Codex | Ghi Human decision, merge resolution và đóng REV-AI-001 | Governance closeout sau merge | REV-AI-001, AI-001, PR #1, merge commit `49efead593437dfc5c88397ea6f335a2d4ff84d7` | No |

## 2. Review Rules

1. Gemini Pro review độc lập và không sửa trực tiếp artefact production.
2. Mỗi review phải ghi đúng artefact, version, task, mục tiêu và nguồn thực tế đã đọc.
3. Không bịa nguồn, bằng chứng, finding, Human decision hoặc resolution.
4. Mỗi finding phải có location, description, evidence, impact, suggested change, Human-decision flag và resolution status.
5. Finding CRITICAL/HIGH không được bỏ qua hoặc đóng khi chưa có evidence resolution/Human decision.
6. Recommendation của Gemini không thay thế approval của Human.
7. ChatGPT/Codex trả lời từng finding; không sửa im lặng rồi xóa finding.
8. Review entry là append-oriented. Chỉ sửa lỗi trình bày không đổi nghĩa; thay đổi thực chất phải được ghi lịch sử.
9. Nội dung research nhạy cảm chỉ dùng excerpt ngắn cần thiết, không sao chép toàn văn paper vào log.
10. `RESOLVED` và `CLOSED` cần resolved version, evidence và người đóng phù hợp với quyền hạn trong `AGENTS.md`.

## 3. Severity Definitions

- `CRITICAL`: lỗi có thể làm sai mục tiêu, gây rủi ro pháp lý, bảo mật hoặc khiến hệ thống không thể sử dụng.
- `HIGH`: lỗi quan trọng ảnh hưởng trực tiếp đến requirement, kiến trúc, dữ liệu hoặc chất lượng đầu ra.
- `MEDIUM`: lỗi cần sửa nhưng chưa ngăn cản toàn bộ workflow.
- `LOW`: lỗi nhỏ, không ảnh hưởng lớn đến chức năng.
- `SUGGESTION`: đề xuất cải tiến không bắt buộc.

## 4. Recommendation Definitions

- `APPROVE`: artefact có thể đi tiếp trong phạm vi review; không thay Human approval.
- `APPROVE WITH CHANGES`: có thay đổi cần thực hiện nhưng không chặn toàn bộ workflow theo đánh giá reviewer.
- `REQUEST CHANGES`: cần sửa và review lại trước khi đi tiếp.
- `NEEDS HUMAN DECISION`: có lựa chọn thuộc thẩm quyền Human hoặc bất đồng không thể tự giải quyết.

## 5. Review Status Definitions

- `OPEN`: review/finding đã tạo và chưa được đánh giá xong.
- `UNDER EVALUATION`: ChatGPT/Codex hoặc Human đang đánh giá.
- `ACCEPTED`: finding được chấp nhận đầy đủ; chưa mặc định đã sửa.
- `PARTIALLY ACCEPTED`: chấp nhận một phần, có lý do/phạm vi rõ.
- `REJECTED WITH REASON`: không chấp nhận và có bằng chứng/lý do.
- `RESOLVED`: thay đổi hoặc quyết định đã có evidence trên resolved version.
- `CLOSED`: review được người có thẩm quyền đóng sau khi xác minh resolution.
- `MERGE PENDING`: reviewer đã PASS, không có finding chặn, nhưng review chưa đóng và PR chưa được Human merge.

## 6. Review Index

| Review ID | Date | Task ID | Artefact | Version | Recommendation | Status |
|---|---|---|---|---|---|---|
| REV-AI-001 | 18/09/2026 | AI-001 | Output Schema v1.0.0 và supporting artefacts | Commit `69b85be6b55cf2c46fc4f02bbfbf3083d2389299`; resolved by merge commit `49efead593437dfc5c88397ea6f335a2d4ff84d7` | APPROVE | CLOSED |

Entry `REV-AI-001` được ChatGPT/Codex ghi lại từ kết quả Gemini 3.1 Pro do Human / Product Owner xác nhận; Gemini không sửa production artefact.

## 7. Review Entry Template

Sao chép nguyên cấu trúc dưới đây cho mỗi review mới. Thay các placeholder bằng dữ liệu có bằng chứng; không xóa mục bắt buộc.

### Review ID

`REV-NNN`

### Date

`DD/MM/YYYY`

### Reviewer

Gemini Pro.

### Task ID

`[TASK ID THỰC TẾ]`

### Artefact reviewed

`[ĐƯỜNG DẪN/TÊN ARTEFACT THỰC TẾ]`

### Version reviewed

`[VERSION THỰC TẾ]`

### Review status

`OPEN`

### 1. Review Objective

Nêu phạm vi, câu hỏi review và nội dung không thuộc review.

### 2. Sources Reviewed

Liệt kê đúng file, commit, nguồn chính thức hoặc tài liệu nghiên cứu đã thực sự đọc. Nếu nguồn không truy cập được, ghi rõ; không bịa nguồn.

### 3. Summary

Tóm tắt kết luận, điểm mạnh có evidence, điểm chặn và mức độ tin cậy.

### 4. Findings

Mỗi finding sử dụng đầy đủ mẫu:

#### Finding F-NNN

| Trường | Nội dung |
|---|---|
| Finding ID | F-NNN |
| Severity | CRITICAL / HIGH / MEDIUM / LOW / SUGGESTION |
| Category | Requirement / Architecture / Grounding / Hallucination / Security / Privacy / Consistency / Testing / Documentation / Khác |
| Location | File, section, field, line hoặc object ID |
| Description | Mô tả cụ thể vấn đề |
| Evidence | Nguồn và căn cứ đã kiểm tra |
| Impact | Hậu quả nếu không xử lý |
| Suggested change | Thay đổi có thể kiểm chứng |
| Requires Human decision | Yes / No |
| Resolution status | OPEN |

### 5. Source-Grounding Issues

Liệt kê finding liên quan locator, evidence entailment, sai nhãn hoặc phát biểu không nguồn. Nếu không có, ghi `Không phát hiện trong phạm vi review` và nêu phạm vi đã kiểm tra.

### 6. Hallucination Risks

Nêu nội dung có nguy cơ được AI tự tạo hoặc biến inference thành fact.

### 7. Missing Information

Nêu requirement, dữ liệu, decision hoặc source còn thiếu và tác động.

### 8. Technical Concerns

Nêu vấn đề API, schema, prompt, parser, validation, DOCX, versioning, testing hoặc deployment.

### 9. Security and Privacy Concerns

Nêu data flow, access control, secret, log, retention, deletion, provider policy hoặc confidential research risk.

### 10. Consistency Issues

So sánh tên dự án, scope, deadline, tech stack, roles, Source of Truth, version và thuật ngữ giữa các artefact trong phạm vi review.

### 11. Suggested Changes

Tổng hợp theo thứ tự ưu tiên, owner đề xuất và acceptance evidence mong đợi.

### 12. Recommendation

Chọn đúng một:

- `APPROVE`.
- `APPROVE WITH CHANGES`.
- `REQUEST CHANGES`.
- `NEEDS HUMAN DECISION`.

### 13. Handoff to ChatGPT/Codex

```text
Task ID:
Agent: Gemini Pro
Reviewer: Human / Product Owner
Status:
Version:
Work completed:
Files affected: Review log only; production artefact not overwritten
Evidence checked:
Findings:
Decisions:
Issues:
Security impact:
Recommended next action:
```

### 14. ChatGPT/Codex Response

| Finding ID | Decision | Reason | Planned action | Target version |
|---|---|---|---|---|
| F-NNN | ACCEPT / PARTIALLY ACCEPT / REJECT WITH REASON / ESCALATE TO HUMAN | `[LÝ DO CÓ CĂN CỨ]` | `[HÀNH ĐỘNG]` | `[VERSION]` |

### 15. Human Decision

Chỉ điền khi Human đã quyết định. Ghi người/role, ngày, quyết định, phạm vi và evidence. Nếu chưa có, ghi `[CẦN XÁC NHẬN]`.

### 16. Resolution

Liệt kê finding đã xử lý, commit/file/test hoặc quyết định làm bằng chứng. Không ghi `Resolved` chỉ vì đã lên kế hoạch.

### 17. Resolved Version

`[VERSION CÓ BẰNG CHỨNG]`

### 18. Closed Date

Chỉ điền khi review thực sự đóng; định dạng `DD/MM/YYYY`.

### 19. Closed By

Human / Product Owner hoặc người được ủy quyền theo `AGENTS.md`.

## 8. Review Entries

### REV-AI-001

#### Date

`18/09/2026`

#### Reviewer

Gemini 3.1 Pro.

#### Task ID

`AI-001`

#### Artefact reviewed

Output Schema v1.0.0 và 17 supporting artefacts trong commit `69b85be6b55cf2c46fc4f02bbfbf3083d2389299`, Pull Request [#1](https://github.com/nshaokiet/ai-ip-description-generator/pull/1).

#### Version reviewed

Output Schema `1.0.0`; commit `69b85be6b55cf2c46fc4f02bbfbf3083d2389299`.

#### Review status

`CLOSED`

#### 1. Review Objective

Review độc lập contract Output Schema v1.0.0, fixtures, tests và supporting documentation của AI-001; sau đó re-review targeted thay đổi chỉ xóa trailing whitespace. Merge approval và các task ngoài AI-001 không thuộc quyền reviewer.

#### 2. Sources Reviewed

- Snapshot 17 file AI-001 tại commit `69b85be6b55cf2c46fc4f02bbfbf3083d2389299`.
- JSON Schema Draft 2020-12 tại `schemas/invention-output/v1.0.0/invention-output.schema.json`.
- Valid/invalid fixtures và automated tests dưới `tests/`.
- ADR-006, task specification và supporting documentation trong commit.
- Test evidence: Python 3.12.10, `jsonschema` 4.26.0, 15/15 tests pass.
- Whitespace evidence: `git diff --check` pass.

#### 3. Summary

Gemini 3.1 Pro full review: `PASS`. Targeted whitespace re-review: `PASS`. Không có finding ở mức BLOCKER, MAJOR, MINOR hoặc mức khác được báo cáo. Recommendation là `APPROVE`; Human / Product Owner đã merge PR #1 ngày 19/09/2026.

#### 4. Findings

Không có finding.

#### 5. Source-Grounding Issues

Không phát hiện trong phạm vi review AI-001.

#### 6. Hallucination Risks

Không phát hiện finding trong phạm vi schema/fixtures/documentation được review. Kết quả này không phải đánh giá output nghiên cứu thật hoặc tư vấn pháp lý.

#### 7. Missing Information

Không có missing information chặn AI-001. Human / Product Owner đã thực hiện quyết định merge PR #1.

#### 8. Technical Concerns

Không có finding. Logical-ID uniqueness và cross-reference existence vẫn là downstream business validation theo contract đã phê duyệt, không phải defect của AI-001.

#### 9. Security and Privacy Concerns

Không có finding. Fixtures là synthetic; review evidence xác nhận `.venv/`, cache, secret và dữ liệu nghiên cứu thật không nằm trong commit được review.

#### 10. Consistency Issues

Không có finding trong full review hoặc targeted whitespace re-review.

#### 11. Suggested Changes

Không có thay đổi kỹ thuật bắt buộc. Governance state được đóng theo bằng chứng Human merge PR #1.

#### 12. Recommendation

`APPROVE`

#### 13. Handoff to ChatGPT/Codex

```text
Task ID: AI-001
Agent: Gemini 3.1 Pro
Reviewer: Human / Product Owner
Status: CLOSED — AI-001 Completed — Merged via PR #1
Version: Output Schema 1.0.0; reviewed commit 69b85be6b55cf2c46fc4f02bbfbf3083d2389299; resolved merge commit 49efead593437dfc5c88397ea6f335a2d4ff84d7
Work completed: Full review và targeted whitespace re-review hoàn tất; Human / Product Owner đã phê duyệt và merge PR #1.
Files affected: Review log only; production artefact not overwritten
Evidence checked: Python 3.12.10; jsonschema 4.26.0; 15/15 tests pass; git diff --check pass; PR #1.
Findings: Không có.
Decisions: Recommendation APPROVE; Human / Product Owner đã thực hiện merge approval ngày 19/09/2026.
Issues: Không có finding hoặc vấn đề AI-001 còn mở.
Security impact: Không có finding; không có secret hoặc dữ liệu nghiên cứu thật trong commit được review.
Recommended next action: Lưu bằng chứng closeout; AI-002 chỉ chuyển sang specification/approval theo task riêng.
```

#### 14. ChatGPT/Codex Response

Không có finding cần `ACCEPT`, `PARTIALLY ACCEPT`, `REJECT WITH REASON` hoặc `ESCALATE TO HUMAN`. ChatGPT/Codex chỉ đồng bộ trạng thái governance và không sửa contract kỹ thuật.

#### 15. Human Decision

Human / Product Owner đã xác nhận kết quả full review `PASS`, targeted whitespace re-review `PASS`, không có finding, recommendation `APPROVE`, và quyết định phê duyệt/merge PR #1 ngày 19/09/2026.

#### 16. Resolution

Không có finding cần resolution. PR #1 đã merge thành công ngày 19/09/2026. Review evidence gắn với implementation commit `69b85be6b55cf2c46fc4f02bbfbf3083d2389299`, governance commit `b738fcd3e46c9cb9159b4c6e092c04fde83545b0` và merge commit `49efead593437dfc5c88397ea6f335a2d4ff84d7`. AI-001 được ghi `Completed — Merged via PR #1`.

#### 17. Resolved Version

`49efead593437dfc5c88397ea6f335a2d4ff84d7`

#### 18. Closed Date

`19/09/2026`

#### 19. Closed By

Human / Product Owner.
