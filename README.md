<p align="center">
  <img src="frontend/public/brand/vnuhcm-innovation-hub-logo.png" alt="VNUHCM Innovation Hub" width="190" />
</p>

# AI Intellectual Property Description Generator

## Project Overview

Hỗ trợ nhóm nghiên cứu chuyển bài báo khoa học thành phân tích sáng chế có nguồn dẫn và bản nháp mô tả theo cấu trúc USPTO để con người rà soát.

**Scientific Paper → Invention Analysis → Human Review → Patent Specification Draft → PDF/DOCX**

**COMPLETED — Local/Synthetic MVP.** Các thành phần offline và luồng minh họa đã hoạt động với dữ liệu tổng hợp; chuyển đổi bài báo bằng AI thật chưa được xác thực.
Mọi đầu ra đều cần người dùng và chuyên gia sở hữu trí tuệ kiểm tra; không phải tư vấn pháp lý, kết luận khả năng bảo hộ hay hồ sơ sẵn sàng nộp.

## Current Capabilities

- **PDF/DOCX Input:** Kiểm tra định dạng, đọc văn bản và bảng, giữ vị trí nguồn; không hỗ trợ OCR cho PDF chỉ có ảnh.
- **Structured Invention Analysis:** Schema, nguồn dẫn, thông tin còn thiếu và quy tắc kiểm tra; adapter AI đã có mã và kiểm thử bằng mock, chưa xác thực với mô hình thật.
- **Invention Reconstruction & USPTO Contracts:** Các thành phần tái dựng sáng chế và sinh mô tả đã triển khai offline; chưa tích hợp thành luồng sản phẩm v2 cho bài báo tùy ý.
- **Human Review & Validation:** Giao diện minh họa hỗ trợ chỉnh sửa, phiên bản và kiểm tra bản nháp được chọn trước xuất DOCX.
- **Offline Claims Support:** Thành phần độc lập kiểm tra yêu cầu bảo hộ có căn cứ; Claims trong luồng sản phẩm vẫn tắt.
- **PDF/DOCX Rendering:** Bộ dựng tài liệu và gói xuất v2 đã được kiểm thử với dữ liệu tổng hợp; demo cung cấp bộ tài liệu mẫu cố định.
- **Offline & Synthetic E2E:** Kiểm thử backend, frontend, trình duyệt, nguồn dẫn, bảo mật và MCP; kết quả tổng hợp không chứng minh chất lượng AI trên bài báo thật.

## Project status

Tiến độ foundation/A được đối chiếu ngày **06/11/2026**; các dòng khác giữ snapshot có nguồn. Đọc [checkpoint canonical](docs/operations/01_PROJECT_CONTROL_CENTER.md#resume-foundation-001-current-baseline) trước khi tiếp tục. Main đã tích hợp PR #147 và foundation #151 tại `6278b081`; exact-main CI42156455402 SUCCESS. PRODUCT-001A đang được recovery trên nhánh riêng, chưa merge hoặc được chấp nhận. Draft là công việc chưa được chấp nhận hoàn tất.

| Workstream | Status | Current focus |
|---|---|---|
| PREAPI-001 / C1 | BLOCKED | Mã quản lý nguồn đã merge; còn chờ postmerge CI và closeout. |
| PREAPI-C2 REVISION-004 | PENDING CI / ACCEPTANCE | [PR #146](https://github.com/nshaokiet/ai-ip-description-generator/pull/146) có Human architecture acceptance và attributed fixed-SHA review PASS; CI fail audit/quota. Spec-only; [#140](https://github.com/nshaokiet/ai-ip-description-generator/pull/140) là Draft cũ chồng phạm vi. |
| PREAPI-D | IN PROGRESS | [Draft checker](https://github.com/nshaokiet/ai-ip-description-generator/pull/141) kiểm tra điều kiện provider offline; chưa merge, chưa xác minh quyền gọi mô hình. |
| PREAPI-E | IN PROGRESS | [Draft evaluator check](https://github.com/nshaokiet/ai-ip-description-generator/pull/142) kiểm tra bộ mẫu và phép chấm; chưa merge, chưa đánh giá AI thật. |
| CI-V2-001 | BLOCKED | [PR #144](https://github.com/nshaokiet/ai-ip-description-generator/pull/144) có external code PASS; CI lịch sử fail quota, hiện CONFLICTING. Run #148 ngày04/11 upload được artifact; không mặc định quota vẫn là nguyên nhân mọi lỗi. |
| CI-V2-002 / CI-V2-003 | PLANNED | [Đặc tả đã soạn](https://github.com/nshaokiet/ai-ip-description-generator/tree/docs/ci-v2-002-003-planning); chưa triển khai CI phân tầng và tối ưu storage. |
| Governance & Integration | PENDING | [PR #143](https://github.com/nshaokiet/ai-ip-description-generator/pull/143) CONFLICTING; reconcile overlap với #146/foundation, không tự đóng hoặc thay review. |
| EVAL-001 Product Runtime | AWAITING FUNDING | Chưa có kết quả chạy provider được chấp nhận; chất lượng ngữ nghĩa vẫn NOT_DETERMINED. |
| README-REFRESH-001 | MERGED / CI DEBT | [PR #145](https://github.com/nshaokiet/ai-ip-description-generator/pull/145) đã merge vào `53c253be`; exact-main push CI attempt2 vẫn FAILURE, không suy thành accepted closeout. |
| DEP-001-SR-20261024 | MERGED / POSTMERGE CI SUCCESS | [#147](https://github.com/nshaokiet/ai-ip-description-generator/pull/147) merged into `main` at `478f7d30` from reviewed HEAD `4c30d37`. [Postmerge CI42038735811](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/42038735811) SUCCESS with mandatory `dep-001-security` artifact, full/prod audit0 and security73+2 PASS. [Evidence and limits](docs/tasks/AIIP-INDEPENDENT-REVIEW-20261105-provenance-closeout.md). No deployment. |
| PRODUCT-001A | LOCAL105PASS / RECOVERY REVIEW-CI PENDING | [Original #149](https://github.com/nshaokiet/ai-ip-description-generator/pull/149) preserved at cf9097fd; separate normal integration onto main6278b081 retains A/C1 code, tests and four fixture bytes. [Recovery scope and gates](docs/tasks/PRODUCT-001A-post-foundation-recovery.md). No browser/security-policy change or fixture admission. |
| PRODUCT-001B | PROPOSED — WEB | [Contract browser0.2.0](docs/tasks/PRODUCT-001B-trusted-local-review-presenter.md) thay khuyến nghị terminal-first; chưa freeze/duyệt implementation/auth policy, chưa triển khai. |
| RESUME-FOUNDATION-001 | MERGED / POSTMERGE CI SUCCESS | [#151](https://github.com/nshaokiet/ai-ip-description-generator/pull/151) merged at6278b081, tree197f5919 unchanged from reviewedbc991c7. [CI42156455402](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/42156455402) SUCCESS/security artifact13475625084 verified; #150 preserved. |

## Next Steps

1. Recover PRODUCT-001A against accepted main on a separate branch, run targeted and required hosted CI/security evidence, then obtain a new independent fixed-SHA review; no merge before gates. [Recovery plan](docs/tasks/PRODUCT-001A-post-foundation-recovery.md).
2. Reconcile CI144/conflicts và QA installer503 trong task tương ứng; giữ mandatory evidence/checks, xác minh postmerge C1.
3. Hoàn tất review provenance/CI của #146/#149; duyệt contract/auth/fixtures cho B trước triển khai một luồng web tổng hợp xuyên suốt.
4. Persistence, author answers/review history/retention/recovery là increment riêng; rồi mới pilot provider khi có quyền và kinh phí.

[Backlog theo dependency và acceptance](docs/tasks/RESUME-FOUNDATION-001.md). Sản phẩm đích là website Next.js + FastAPI; local/offline/synthetic là môi trường kiểm thử. MCP điều phối phát triển, không phải database hồ sơ website.

Các bước đề xuất phải qua quyết định phạm vi tương ứng; danh sách này không tự cấp quyền thực hiện.

## Funding Requirements

**AI API runtime budget: USD 0.** Phần offline, mock và dữ liệu tổng hợp vẫn phát triển được mà không gọi AI trả phí.
Quyền truy cập mô hình trên tài khoản API và giá thực tế chưa được xác minh.

| Component | Purpose | Current status | Funding requirement |
|---|---|---|---|
| Live Extraction | Kiểm tra trích xuất và nguồn dẫn bằng AI thật | AWAITING FUNDING | Provider, mô hình và hạn mức |
| Live Draft Generation | Kiểm tra bản nháp từ kết quả phân tích thật | AWAITING FUNDING | Lượt gọi và token được duyệt |
| Real-Provider E2E | Xác minh luồng xử lý đầu cuối | AWAITING FUNDING | Pilot có giới hạn chi phí |
| Semantic Evaluation | Đánh giá chất lượng trên bộ dữ liệu được phép | AWAITING FUNDING | Lượt chạy và tiêu chí được duyệt |
| Provider Regression | Đo lỗi, retry, token và chi phí | AWAITING FUNDING | Ngân sách thử nghiệm riêng |
| Production Infrastructure | Đáp ứng bảo mật, lưu trữ và vận hành | PLANNED | Chỉ xác định sau quyết định kiến trúc |

**TBD — Pending Provider and Budget Approval:** Chưa xác định chi phí, hạn mức pilot hoặc nhu cầu hạ tầng trả phí; không bắt đầu pilot khi chưa có phê duyệt riêng.
Bài báo thật chưa được xác thực qua pipeline AI và chưa đạt semantic acceptance.
**GitHub Actions có blocker riêng:** quota upload đã lỗi ở các run tháng10; run148 đã upload thành công, còn run149 lỗi QA503 và thiếu output. Mua tín dụng AI API không xử lý các gate này.

## Production Readiness

**BLOCKED — BLK-003 còn mở.** Cần hoàn tất xác thực, phân quyền và cách ly người dùng; lưu trữ riêng, retention và xóa dữ liệu; kiểm chứng bảo mật, giám sát và khôi phục.
Việc dùng nghiên cứu thật hoặc chưa công bố, bật Claims sản phẩm và phát hành production đều cần phê duyệt riêng.

## Demo & Documentation

**[Synthetic Web Demo](https://ai-ip-synthetic-demo-frontend.onrender.com)** — Dùng mẫu tổng hợp, không phải production hoặc dịch vụ chuyển đổi bài báo thật bằng AI. Không đưa dữ liệu mật hay nghiên cứu chưa công bố vào demo.

- [System Specification](docs/system-specification.md) · [Project Context](PROJECT_CONTEXT.md)
- [Project Control Center](docs/operations/01_PROJECT_CONTROL_CENTER.md) · [Review Log](docs/operations/02_GEMINI_REVIEW_LOG.md)
- [Development Roadmap](docs/tasks/PREAPI-001-zero-cost-roadmap.md) · [Latest Roadmap & Pilot Checklist — Draft](https://github.com/nshaokiet/ai-ip-description-generator/pull/143)
- [Local Development Runbook](docs/tasks/P1-004-one-command-local-run.md) · [AI Collaboration Rules](AGENTS.md)

## Quick Start

Yêu cầu: quyền truy cập repository, Python 3.12, Node.js 24+ và npm. Chạy trong Windows PowerShell:

```powershell
git clone https://github.com/nshaokiet/ai-ip-description-generator.git
cd ai-ip-description-generator
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt -r tests/requirements.txt
cd frontend
npm ci
cd ..
.\.venv\Scripts\python.exe tools\local_dev.py --check
.\.venv\Scripts\python.exe tools\local_dev.py
```

Mở http://127.0.0.1:3000; dùng Ctrl+C để dừng. Launcher mặc định không bật API orchestration; xem runbook để kiểm thử luồng tổng hợp. Không thêm API key cho hướng dẫn này.

## Maintenance

Cập nhật tổng quan khi tính năng được chấp nhận, workstream đổi trạng thái, task được cấp quyền, blocker được gỡ, kinh phí được duyệt hoặc pilot hoàn tất.
Lưu bằng chứng, lịch sử commit/CI và checkpoint trong task record và Control Center; không nối nhật ký vào README.
Chưa công bố giấy phép mã nguồn mở. Liên hệ: [GitHub Issues](https://github.com/nshaokiet/ai-ip-description-generator/issues).

<details>
<summary>Governance Compatibility</summary>

Historical/unenrolled tasks remain V1. Xác minh merge theo [MANUAL / EXTERNAL](docs/operations/WORKFLOW_V2_MANUAL_VERIFICATION.md); closeout Phase G còn điều kiện.

| Milestone | Recorded state |
|---|---|
| GOV-AGENT-001-D | CLOSED / COMPLETED |
| GOV-AGENT-001-E | ACTIVATED — EXPLICIT_ONLY |

## Conditional project adoption (Phase G)

Khai báo dưới đây được validator đối chiếu nguyên văn; các nhãn mốc Phase G không thay thế bảng tiến độ sản phẩm.

| Policy field | Required value |
|---|---|
| Adoption policy | CONDITIONAL |
| Adoption effective boundary | Accepted Phase G merge/postmerge verification |
| Preferred process | V2 for eligible explicitly Human-authorized tasks |
| V2 enrollment | EXPLICIT_ONLY |
| Historical/unenrolled V1 | PRESERVED |
| MANUAL_EXTERNAL | MANDATORY |
| Phase G reviews | Security AND Quality, separate identities and actual Antigravity sessions |
| Automatic R0-R4 | NOT ACTIVATED |
| Identity | PROCEDURAL_TRUST_BASED |
| Accepted verifier adapters | UNAVAILABLE |
| B3 authoritative_merge_eligible | false |
| Evidence | RECORDED != VERIFIED; provisional_ready != authoritative_merge_eligible |
| MCP completion transition | BLOCKED BY TOOL CAPABILITY — disclosed separately |
| Rollback | Preserve evidence; separately reviewed Human disable; in-progress Human disposition |
| Product/provider/production authority | NOT GRANTED |
| Phase H / AI-CONV | NOT STARTED |
| WORKFLOW_V2_ACTIVATION_COMMIT | 9c291325d409f74bc767f9b870e81d75c9b70802 |

</details>
