<p align="center">
  <img src="frontend/public/brand/vnuhcm-innovation-hub-logo.png" alt="VNUHCM Innovation Hub" width="190" />
</p>

# AI Intellectual Property Description Generator

## Mục tiêu sản phẩm — API-ready, tối giản

**Scientific Paper (PDF/DOCX) → Source-grounded Invention Analysis → Patent Specification + Supported Draft Claims → Human Review → DOCX/PDF**

Dự án hướng tới một **website Next.js + FastAPI** giúp nhóm nghiên cứu chuyển bài báo khoa học được phép sử dụng thành **bộ bản nháp mô tả sáng chế theo cấu trúc USPTO (Hoa Kỳ)**, bao gồm **Patent Specification** và **Draft Claims** khi có đủ căn cứ. Bản nháp bằng tiếng Anh để tác giả/chuyên gia sở hữu trí tuệ rà soát; không phải hồ sơ sẵn sàng nộp hoặc bằng sáng chế đã được cấp.

**Ưu tiên hiện tại: API-READY SCAFFOLD, không phải production.** Tận dụng các module đã có, nối các bước còn thiếu, chạy kiểm thử bằng mock và dữ liệu tổng hợp **không phát sinh phí API**. Khi có kinh phí/quyền sử dụng provider, cấu hình backend và thực hiện pilot có giới hạn để kiểm chứng luồng thực và chất lượng đầu ra. Có API key **không đồng nghĩa** hệ thống lập tức tạo được bản patent đạt yêu cầu từ mọi bài báo; kiểm thử provider thật và semantic evaluation vẫn bắt buộc.

### Đầu ra mục tiêu

- **Patent Specification Draft:** tên sáng chế, lĩnh vực kỹ thuật, bối cảnh, tóm tắt giải pháp, mô tả hình vẽ nếu có, mô tả chi tiết và abstract theo contract hiện có.
- **Supported Draft Claims:** bản nháp independent/dependent claims với claim-to-source/specification support mapping **chỉ khi** tài liệu và contract cho phép; ghi rõ phần cần tác giả xác nhận.
- **Validation & Human Review:** giữ evidence/locator, phát hiện thiếu căn cứ, mâu thuẫn và trạng thái chưa duyệt; không suy diễn tính mới, phạm vi bảo hộ tối ưu hay khả năng được cấp bằng.
- **Export:** DOCX/PDF có thể đọc và kiểm tra, với trạng thái **DRAFT / HUMAN-IP-REVIEW-REQUIRED**, không tự nhận filing-ready.

**Fail closed:** nếu bài báo không đủ thông tin kỹ thuật, hệ thống phải trả về thiếu căn cứ / `HUMAN_CONFIRMATION_REQUIRED` / Claims trống thay vì bịa claim element, invention embodiment, kết quả thí nghiệm hoặc legal claim scope.

### Ranh giới của Claims hiện tại

- Đã có thành phần **offline standalone** để sinh và kiểm tra supported draft Claims, cùng prototype semantic-authority synthetic. Đây **không phải** Claims đã tích hợp và kích hoạt trong luồng sản phẩm.
- Đầu ra dương tính hiện tập trung vào **SYSTEM / APPARATUS** khi đáp ứng đầy đủ các điều kiện support/authority; **METHOD / PROCESS / COMPOSITION** chưa được phép khẳng định positive Claims qua overlay hiện có.
- Để đưa Claims vào tài liệu xuất của sản phẩm cần **tích hợp được phê duyệt, validation và review riêng**; không tự bật `claims_runtime_implemented`, không sửa hợp đồng P2-002…P2-006 hoặc bỏ qua human/IP review.

## Những gì đã có (không xây lại)

| Thành phần | Bằng chứng/trạng thái |
|---|---|
| PDF/DOCX parsing và source evidence | Có module, kiểm thử offline; không OCR PDF chỉ có ảnh |
| Structured extraction và draft runtime | Có mã tích hợp OpenAI Responses API cho extraction/draft và các schema/validator; **chưa nghiệm thu live-provider trên bài báo thật** |
| Reconstruction / USPTO specification | Có bộ sinh, validation và offline orchestration; chưa có product E2E cho bài báo tùy ý |
| Supported Draft Claims | Có bộ sinh/validator standalone và synthetic-authority prototype; **product Claims OFF** |
| DOCX/PDF renderer | Đã kiểm thử với synthetic fixtures; demo hiện dùng mẫu cố định |
| Next.js frontend + FastAPI backend | Nền tảng đã có; chưa xác nhận luồng browser upload → mock analysis → specification + claims → export end-to-end |
| CI/backend/frontend/MCP | Có regression và security gates; CI PASS **không** chứng minh chất lượng semantic của AI |

**Trạng thái chính xác:** `LOCAL/SYNTHETIC MVP COMPLETE`; `API_READY END-TO-END = NOT VERIFIED`; `LIVE SEMANTIC ACCEPTANCE = NOT DETERMINED`; `PRODUCTION = NOT APPROVED`.

## Trạng thái dự án — 09/11/2026

Base `main` tại thời điểm cập nhật: `d74a6e8a767bfc04884bdf8a187a54f7015d7d98` (normal merge [PR #158](https://github.com/nshaokiet/ai-ip-description-generator/pull/158); exact-main [CI #42550280526](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/42550280526) đang chạy khi đối chiếu, **chưa xác nhận postmerge PASS**). Các bản ghi lịch sử đầy đủ nằm tại [Project Control Center](docs/operations/01_PROJECT_CONTROL_CENTER.md) và [review log](docs/operations/02_GEMINI_REVIEW_LOG.md); README tập trung vào mục tiêu và đường găng còn lại.

| Workstream | Trạng thái hiện hành |
|---|---|
| MCP-SECURITY-REMEDIATION-001 | [PR #158](https://github.com/nshaokiet/ai-ip-description-generator/pull/158) **MERGED** bằng normal merge được Human phê duyệt, tree khớp reviewed HEAD; [merge receipt](https://github.com/nshaokiet/ai-ip-description-generator/pull/158#issuecomment-6730713740). Exact-main [CI #42550280526](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/42550280526) đang chạy khi ghi nhận; chỉ đóng issue #157 sau khi kiểm chứng đầy đủ. Rủi ro input/resource còn lại được giữ **OPEN / PLANNED / NOT AUTHORIZED** tại [#160](https://github.com/nshaokiet/ai-ip-description-generator/issues/160). |
| Core A/C1, P2-002…P2-006 và offline Claims | Module và các kiểm thử synthetic đã có; không tự suy ra luồng website hay Claims product được bật |
| API-READY-001 — hướng ưu tiên mới | **Định hướng do Human yêu cầu**, chưa phải task implementation được đăng ký/ủy quyền; rà soát gap trước khi phê duyệt bản vá tối thiểu |
| PRODUCT-001B | Documentary baseline đã merge, WEB-001 v0.1.1 **NOT FROZEN**; D01–D07 và B1–B6 chưa được phê duyệt. **Không mặc định triển khai** website đa người dùng/phức tạp trong phase API-ready. |
| PREAPI-C2 / D / E và provider pilot | Những task đang Draft/spec-only hoặc chờ quyền/kinh phí; không được kích hoạt ngầm bằng việc sửa README |
| Real-paper AI / release | Provider budget 0; live E2E/semantic QA chưa nghiệm thu; dữ liệu nghiên cứu chưa công bố và production chưa được phép |

## Next Steps — đường ngắn nhất đến API_READY

1. **Đối chiếu hậu merge PR #158:** kiểm tra exact-main CI/security #42550280526 trước khi đóng issue #157; duy trì issue #160 cho hardening riêng, không gộp vào scope API-ready.
2. **API-READY-001 / gap inventory (planning):** đối chiếu code và test hiện có cho `PDF/DOCX → parse/evidence → mock analysis → reconstruction → specification + standalone supported claims hoặc explicit refusal → validation/human review → DOCX/PDF`. Ghi rõ điểm đứt; không viết lại module đã có.
3. **Minimal integration (chỉ sau scoped authorization):** nối các adapter/mock và export còn thiếu bằng các thay đổi nhỏ, có test. Giữ default offline, không gọi provider trả phí; không tự phát triển PRODUCT-001B B1–B6, auth/multi-user, storage production hoặc giao diện phức tạp.
4. **Offline API-readiness acceptance:** ít nhất hai nguồn synthetic PDF/DOCX thực sự khác nội dung; chạy E2E đúng đường xử lý, validate schema/evidence/Claims support hoặc explicit refusal, kiểm tra byte DOCX/PDF và test lỗi. Không đánh dấu PASS nếu chỉ chạy demo cố định.
5. **Provider activation checklist (không chạy live):** cấu hình backend secret/model có thẩm quyền; schema/response parsing, timeout/retry, token/cost budget, failure handling, network guard và smoke test `DISABLED` mặc định; ghi rõ công việc nào chỉ có thể xác minh sau khi có API.
6. **Khi có kinh phí và phê duyệt:** pilot live-provider trên tài liệu được phép dùng, đo chất lượng specification **và Claims**, kiểm tra grounding/hallucination/cost, Human/IP review; mới xem xét sản phẩm thực tế. Nếu chất lượng không đạt, không quảng bá output là patent hoàn chỉnh.

### Tiêu chí dừng phát triển để chờ kinh phí

`API_READY` chỉ được ghi khi có bằng chứng **mock E2E PASS**, cấu hình/kiểm thử provider smoke test chuẩn bị sẵn (chưa gọi API), Claims fail-closed được kiểm tra, xuất DOCX/PDF hợp lệ và không có blocker kỹ thuật thuộc scope tối thiểu. Sau đó **tạm dừng mở rộng tính năng**, chờ provider pilot; không yêu cầu multi-user, deployment hay B1–B6 để đạt mốc này.

Đây là **ưu tiên sản phẩm**, không phải phê duyệt thay đổi các contract/Claims runtime, input/security policy, dữ liệu thật, paid API hoặc production. Các thay đổi cần task/scope/review/CI theo [AGENTS.md](AGENTS.md).

## Kinh phí và bật API

- **Hiện tại:** provider/API budget **USD 0**; không gọi live provider và không commit API key. Các runtime adapter có mã không đồng nghĩa provider/model đã được phê duyệt hoặc kiểm thử.
- **Trước khi có ngân sách:** hoàn thiện scaffold, mock tests và runbook cấu hình. Dùng backend environment/secret manager cho key; không để key trong frontend, log, git hoặc tài liệu công khai.
- **Khi có ngân sách:** xác nhận provider/model và hạn mức, bật riêng trong môi trường thử nghiệm, chạy smoke test nhỏ và semantic evaluation được duyệt; đo error, latency, token/cost và chất lượng Claims. Không bảo đảm chỉ nhập key là tạo patent đạt chuẩn.
- **Production:** chỉ xem xét sau pilot và quyết định bảo mật/dữ liệu riêng; chi phí hạ tầng chưa xác định.

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
