<p align="center">

## Project status — CI-SNAPSHOT-RESILIENCE-001 (2026-11-24)

## Project status — dependency acceptance 28/11/2026

| Workstream | Verified status / boundary |
|---|---|
| Accepted main / PR #164 | `3b3891f5452083bf09cc4f10388b7145d73ea5c4`, TREE `2252e514c339de12bd2d43a02ae5650e93b8ed13`; **MERGED_VERIFIED / POSTMERGE_CI_SECURITY_SUCCESS**. [Exact-main CI46124575472](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/46124575472) SUCCESS, both jobs/DEP-001 SUCCESS, artifact15254653794 zero full/production vulnerabilities. [Canonical closeout](https://github.com/nshaokiet/ai-ip-description-generator/pull/164#issuecomment-7236596530). |
| P0-CONF / PR #169 | Authorized reconciliation of accepted main into existing candidate; original consent service and tests unchanged. **RECONCILED_CANDIDATE / EXACT_HEAD_CI_PENDING / FRESH_DUAL_REVIEW_PENDING**; no merge or Ready transition. [Task](docs/tasks/P0-CONF.md). |
| Independent review | Gemini 4 Argon (Medium), separate STRICT READ-ONLY Security and Quality sessions on final BASE/HEAD/TREE; NOT_RUN. Computer Use prohibited by Human; prepare manual prompts if direct connector dispatch is unavailable. Prior PASS does not transfer. |
| Remaining dependency gates | PR #170 has a verified branch/PR API HEAD+BASE metadata discrepancy; no force-push or refresh commit. PR #172 waits for the required accepted baseline. PR #171/#173 merges excluded. |
| Preserved boundaries | SL-D04/SL-D05/TTL Option A approved; architecture commit `23d847f3a441c2db8c7f6a9eced75868aefbbb87` preserved. Precommit runtime and role reversal NOT ACTIVATED. Claims OFF; provider NOT_RUN; API USD0; synthetic only; production NOT APPROVED. |

Current dated status above supersedes older pending/audit snapshots below; all historical entries remain. Component acceptance is distinct from integrated website acceptance. MCP state/lease/completion is not asserted.


| Task | Current status |
|---|---|
| CI-SNAPSHOT-RESILIENCE-001 | [Bounded shared QA snapshot remediation](docs/tasks/CI-SNAPSHOT-RESILIENCE-001.md): IMPLEMENTED_CANDIDATE; exact-HEAD CI and independent Security/Quality pending. No merge or dependency integration authorized. |

Earlier checkpoints below remain historical; existing product/provider/production boundaries remain.

  <img src="frontend/public/brand/vnuhcm-innovation-hub-logo.png" alt="VNUHCM Innovation Hub" width="190" />
</p>

# AI Intellectual Property Description Generator

## Current accepted status — P0-SOURCE-LIFECYCLE-001 (2026-11-23)

- **PR #174 bounded nested/concurrent lease correction:** `MERGED_VERIFIED`; reviewed HEAD `2f79c83f2f0050591cdf8468a52dac2007382d9a`, merged main `f988aac71bd8615c9b56ab66d352a6becd39d487`, identical TREE `6ce55d0d3393973b361dc20a19b37efd07d54ed5`.
- **Postmerge gates:** [push CI #45105551647](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/45105551647) `COMPLETED/SUCCESS`; both jobs PASS; security graph audit PASS. [Evidence/limitations](https://github.com/nshaokiet/ai-ip-description-generator/pull/174#issuecomment-7090856152).
- **NOT complete:** `SOURCE_LIFECYCLE_HANDOFF_NOT_VERIFIED` remains OPEN; strict-age TTL admission NOT_IMPLEMENTED; PR #173 / SL-D01–08 still PROPOSED, SL-D04/SL-D05 and other dependencies require separate decisions. No policy, Claims, provider, real-document or production authorization. The preceding 22/11 and original baseline status entries below are historical snapshots, not live PR #174 status.

## Project status — DEP-SEC postmerge22/11/2026

Current23/11 checkpoint: PR175 MERGED at986c49782326487fd2b619f6f3603e618d9f806d; exact-main CI45097285617 SUCCESS. The22Nov pending-closeout wording below is preserved history. It grants no174 merge authority.

| Task | Current evidence / boundary |
|---|---|
| DEP-SEC-20261118-001 | PR165 implementation MERGED_VERIFIED at50072fc; exact-main CI45041622472 SUCCESS, full/prod audit0, fresh reviewed4186b7a tree identical. [Evidence](docs/tasks/DEP-SEC-20261118-001.md). Governance closeout pending this docs candidate's review/merge gates. Historical authorization limitation retained with actual-date prospective disposition. |
| P0-SOURCE-LIFECYCLE-001 | [Execution record](docs/tasks/P0-SOURCE-LIFECYCLE-001-execution.md): PR174 lease candidate reconciled with accepted main; fresh exact-HEAD CI/review pending, not merged; source handoff/strict-age admission not implemented. |
| Integration |174 requires fresh new-HEAD CI and independent dual review;168 NOT_EFFECTIVE; ClaimsOFF/APIUSD0/productionNOT_APPROVED. |

Historical status follows unchanged.

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

## Project status — P0-CONF checkpoint22/11/2026

| Workstream | Current evidence / boundary |
|---|---|
| main baseline | `6bb947c1cf67bcfb3ffc935b3a3fafcafb87f0af`; new candidate below not merged |
| P0-CONF | [Task/review package](docs/tasks/P0-CONF.md): IMPLEMENTED_CANDIDATE /INTEGRATION_PENDING /BLOCKED_REVIEW; offline source/revision/payload/destination/purpose-bound consent, no provider-route integration |
| REALIGN-001 | [Existing PR167](https://github.com/nshaokiet/ai-ip-description-generator/pull/167), not integrated; source inventory/roadmap kept there, not duplicated here |
| Security / funding | Existing next16.4.1 audit1MODERATE/build block;165 remediation unmerged. USD0, live providerNOT_RUN, ClaimsOFF, no deployment |

### Historical status — 09/11/2026

The following snapshot is historical; current P0-CONF status is the table above. This task does not independently adopt the unmerged product/governance proposals.


**Mốc source-of-truth:** `main` tại thời điểm đồng bộ tài liệu = `b7a82b8183de734cd8ac6d84ffbdd9a90db94a4b` (PR #142 normal merge), gồm các increment không tốn phí #161, #141 và #142. [Exact-main CI #42625564182](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/42625564182) **đang chạy ở lần đối chiếu**: MCP SUCCESS, build-and-test/chứng cứ hậu merge còn PENDING; **không ghi postmerge PASS trước khi đủ bằng chứng**. Các receipt có SHA/CI/security chi tiết nằm tại [Issue #131](https://github.com/nshaokiet/ai-ip-description-generator/issues/131) và từng PR; không tái tạo nhật ký lịch sử trong README.

| Workstream | Trạng thái và giới hạn đã xác minh |
|---|---|
| API-READY-001-A | [PR #161](https://github.com/nshaokiet/ai-ip-description-generator/pull/161) **MERGED / postmerge CI/security PASS**; kiểm thử offline **2 nguồn synthetic khác nội dung** qua pipeline hiện có. Không có xác nhận API thật hoặc xử lý tùy ý mọi paper. |
| PREAPI-D | [PR #141](https://github.com/nshaokiet/ai-ip-description-generator/pull/141) **MERGED**, [exact-main CI #42616869824](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/42616869824) SUCCESS; CLI offline preflight chỉ kiểm tra SDK, prompt/schema, cấu hình và cờ default-OFF. `future_live_budget_enforcement=NOT_IMPLEMENTED`, model entitlement UNVERIFIED. |
| PREAPI-E | [PR #142](https://github.com/nshaokiet/ai-ip-description-generator/pull/142) **MERGED**; exact-main #42625564182 đang chờ closeout hậu merge khi ghi nhận. Bộ dữ liệu gold đã chấp nhận: **6 cases / 154 items (102 KEY, 52 SECONDARY)**; không đo chất lượng của AI thật. |
| Core A/C1, PDF/DOCX, USPTO, Claims standalone | Các bộ xử lý/validator/rendering và synthetic tests đã có. **Product Claims runtime OFF**, không suy ra browser upload-to-patent v2 hay sản phẩm filing-ready. |
| PRODUCT-001B / PREAPI-C2 | WEB-001 v0.1.1 chỉ có documentary baseline; **NOT FROZEN**; scope B1–B6, D01–D07 và C2 runtime chưa tự cấp phép. |
| API-READY-WEB-GAP-001B-S1 | [Local transport/auth foundation](docs/tasks/API-READY-WEB-GAP-001B-S1.md): Human cho phép D-GAP-01/03 ngày 11/11/2026, **implementation candidate / independent review pending**; chỉ HTTPS/pairing/session, chưa có document routes hoặc fixture admission. |
| API-READY-WEB-GAP-001B-S2-A | [Minimal local synthetic backend bridge](docs/tasks/API-READY-WEB-GAP-001B-S2-A.md): **security remediation candidate / fresh exact-HEAD CI and independent re-review required** under Human-approved S2A-PUBLICATION-COORDINATION-001 (18/11/2026); shared private publication/revocation gate, deterministic race coverage; default OFF, exactly two fixtures, limited R0, Claims disabled. PR164 remains Draft; no merge or S2-B. |
| DEP-SEC-20261118-001 | [PR #165](https://github.com/nshaokiet/ai-ip-description-generator/pull/165) OPEN/DRAFT/UNMERGED; Human2026-11-21 authorized bounded dynamic-directory/resolver compatibility correction. **IMPLEMENTER-REMEDIATED / separate Security/Quality review PENDING**; exact-new-HEAD CI/security evidence is required and recorded in the PR. Old Quality PASS superseded by REQUEST CHANGES; historical initiation AUTHORIZATION_PROVENANCE_NOT_VERIFIED remains; no merge authority. [Task/evidence](docs/tasks/DEP-SEC-20261118-001.md). |
| MCP Security / maintenance | [PR #158](https://github.com/nshaokiet/ai-ip-description-generator/pull/158) đã merge; [Issue #160](https://github.com/nshaokiet/ai-ip-description-generator/issues/160) giữ các rủi ro input/resource cần quyết định riêng. |
| Funded provider pilot / EVAL-001 Product Runtime | **NOT RUN / NOT DETERMINED**; model/account entitlement và semantic-quality chưa nghiệm thu; API budget **USD 0**. |

## Next Steps — đường ngắn nhất đến API_READY

1. **Hoàn tất exact-main closeout PR #142:** chỉ nhận [CI #42625564182](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/42625564182) khi đủ kết quả hai job và artifact security hậu merge; không dùng CI trước merge thay thế.
2. **Không xây lại các checker/pipeline đã có:** giữ các mốc offline hai nguồn synthetic (#161), preflight provider mặc định OFF (#141) và kiểm tra gold (#142). Không coi ba mốc này là bằng chứng chất lượng model thực hoặc UI E2E cho bài báo bất kỳ.
3. **Chỉ audit gap tối thiểu còn lại:** kiểm tra thực trạng đường **website upload → evidence → mock reconstruction/specification → supported Claims hoặc explicit refusal → human/IP review → DOCX/PDF**. Nếu thiếu integration/test, lập task/acceptance cụ thể và xin phê duyệt phạm vi riêng; không tự kích hoạt PRODUCT-001B, Claims authority hoặc mở rộng multi-user/production.
4. **Bảo toàn checklist để bật provider sau này:** SDK/model entitlement, key backend-only, token/timeouts/retry, fail-closed khi vượt hạn mức, kế hoạch smoke test **DISABLED**. Kiểm tra cấu hình offline **không phải** biện pháp enforce chi tiêu API live; chưa chấp thuận provider.
5. **Khi có kinh phí và chấp thuận độc lập:** chạy pilot trên nguồn hợp pháp, đo grounding/Claims hallucination, chất lượng specification, chi phí/token và review người; chỉ sau đó mới quyết định phát triển tiếp.

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


## PR #164 official dependency recovery — 2026-11-24

Human authorization: “HUMAN AUTHORIZATION — OFFICIAL DEPENDENCY RECOVERY”,
2026-11-24, P0-WEB-PRECOMMIT-001. Normal merge of accepted main `448de79be9720d4d1fd5b6b7e1cb87a360a0d5a7`
into original candidate `f08b071ee76468f01ad20bfa917d1b6360e5b453`; history and earlier authorization/review dates retained.
Accepted PR165 security graph, PR174 reference-count leases and PR176 governance retained.
Candidate business runtime is unchanged relative to the non-documentary merge projection.

Current state: RECOVERY_COMMITTED / EXACT_HEAD_CI_PENDING / FRESH_DUAL_REVIEW_PENDING.
Earlier pending/merged statements above are historical snapshots, not this recovered PR's verdict.
Standing reviewer Gemini 4 Argon (High), separate Security/Quality sessions on this final SHA.
No new review/PASS or original-report hashes fabricated. Desktop reviewer dispatch currently
blocked by node_repl Windows sandbox helper setup failure before app/model selection.
Original source-attributed authorization limitations remain; this new recovery authorization
is prospective, not retrospective approval.

No merge/Ready authority, precommit runtime, new admission hook, strict-age TTL, publicationV2,
workspace, auth/retention change, Claims, paid API, real research or production deployment.
Metadata version increases on this branch record recovery only; canonical acceptance pending.

## PR #169 official dependency recovery — 2026-11-24

Human authorization: “HUMAN AUTHORIZATION — OFFICIAL DEPENDENCY RECOVERY”,
2026-11-24, P0-WEB-PRECOMMIT-001. Normal merge of accepted main `448de79be9720d4d1fd5b6b7e1cb87a360a0d5a7`
into original candidate `3f34217638c0ed1fcf7e91b74fa47b163fa1cd96`; history and earlier authorization/review dates retained.
Accepted PR165 security graph, PR174 reference-count leases and PR176 governance retained.
Candidate business runtime is unchanged relative to the non-documentary merge projection.

Current state: RECOVERY_COMMITTED / EXACT_HEAD_CI_PENDING / FRESH_DUAL_REVIEW_PENDING.
Earlier pending/merged statements above are historical snapshots, not this recovered PR's verdict.
Standing reviewer Gemini 4 Argon (High), separate Security/Quality sessions on this final SHA.
No new review/PASS or original-report hashes fabricated. Desktop reviewer dispatch currently
blocked by node_repl Windows sandbox helper setup failure before app/model selection.
Original source-attributed authorization limitations remain; this new recovery authorization
is prospective, not retrospective approval.

No merge/Ready authority, precommit runtime, new admission hook, strict-age TTL, publicationV2,
workspace, auth/retention change, Claims, paid API, real research or production deployment.
Metadata version increases on this branch record recovery only; canonical acceptance pending.
