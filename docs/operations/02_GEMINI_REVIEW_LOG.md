# Gemini Review Log

> Bản nguồn Markdown được quản lý trong Git. Tên Google Doc đích: `02_GEMINI_REVIEW_LOG`. Trạng thái đồng bộ Google Drive: `[CẦN XÁC NHẬN TRẠNG THÁI]`.

## 1. Document Metadata

| Thuộc tính | Giá trị |
|---|---|
| Document ID | REVIEW-001 |
| Document title | Gemini Review Log |
| Project | AI Intellectual Property Description Generator |
| Project deadline | 02/10/2026 |
| Version | 0.1.0 |
| Status | Draft template |
| Owner | Human / Product Owner |
| Author | ChatGPT/Codex |
| Reviewer | Gemini Pro |
| Created date | 18/09/2026 |
| Last updated | 18/09/2026 10:40 GMT+7 |
| Related task ID | REVIEW-001 |
| Source of Truth | Review history; bản nguồn Git tại `docs/operations/02_GEMINI_REVIEW_LOG.md` |
| Confidentiality level | Internal; findings về research input có thể là Confidential |

### Lịch sử phiên bản

| Phiên bản cũ | Phiên bản mới | Ngày | Người thực hiện | Thay đổi | Lý do | Finding/Decision liên quan | Breaking change |
|---|---|---|---|---|---|---|---|
| Chưa có | 0.1.0 | 18/09/2026 | ChatGPT/Codex | Tạo review log format ban đầu | Khởi tạo quy trình independent review | REVIEW-001 | No |

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

## 6. Review Index

| Review ID | Date | Task ID | Artefact | Version | Recommendation | Status |
|---|---|---|---|---|---|---|

**Chưa có review entry chính thức.**

Không thêm dòng vào index nếu chưa có review thật tương ứng ở mục 8.

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

**Chưa có review entry chính thức.**

Review đầu tiên được đề nghị:

- Review ID dự kiến: `REV-001`.
- Artefact: `docs/system-specification.md`.
- Version: `0.1.0`.
- Trạng thái: chưa bắt đầu; đây không phải review entry.
