# PROJECT_CONTEXT.md

## Bối cảnh dự án

## 1. Metadata

| Thuộc tính | Giá trị |
|---|---|
| Document ID | SPEC-002 |
| Document title | Project Context — AI Intellectual Property Description Generator |
| Version | 0.4.29 |
| Status | Approved baseline |
| Owner | Human / Product Owner |
| Author | ChatGPT |
| Reviewer | Human / Product Owner |
| Created date | 18/09/2026 |
| Last updated | 02/10/2026 |
| Related task ID | SPEC-002 |
| Source of Truth | GitHub — `PROJECT_CONTEXT.md` |
| Confidentiality level | Internal; research inputs are Confidential by default |

### Lịch sử phiên bản

| Phiên bản cũ | Phiên bản mới | Ngày | Người thực hiện | Thay đổi | Lý do | Finding/Decision liên quan | Breaking change |
|---|---|---|---|---|---|---|---|
| Chưa có | 0.1.0 | 18/09/2026 | ChatGPT/Codex | Tạo project context ban đầu | Khởi tạo Phase 1 | SPEC-002 | No |
| 0.1.0 | 0.1.1 | 18/09/2026 | ChatGPT/Codex | Ghi nhận URL và visibility của repository GitHub | Đồng bộ trạng thái đã kiểm chứng | Yêu cầu Human đưa artefact lên GitHub | No |
| 0.1.1 | 0.2.0 | 18/09/2026 | ChatGPT/Codex | Ghi nhận contract Output Schema v1.0.0 và ranh giới AI-001 | Đồng bộ quyết định Human đã phê duyệt | AI-001, ADR-006 | No |
| 0.2.0 | 0.2.1 | 18/09/2026 | ChatGPT/Codex | Ghi nhận Gemini review PASS và PR #1 đang chờ Human merge approval | Đồng bộ governance state có bằng chứng | AI-001, REV-AI-001, PR #1 | No |
| 0.2.1 | 0.2.2 | 19/09/2026 | ChatGPT/Codex | Ghi nhận AI-001 hoàn tất sau khi Human merge PR #1 | Đồng bộ governance state sau merge | AI-001, REV-AI-001, PR #1, merge commit `49efead593437dfc5c88397ea6f335a2d4ff84d7` | No |
| 0.2.2 | 0.2.3 | 19/09/2026 | ChatGPT/Codex | Ghi nhận Extraction Prompt v1.0.0 và ranh giới canonical offline validation | Đồng bộ quyết định Human cho AI-002 | AI-002, ADR-007 | No |
| 0.2.3 | 0.2.4 | 19/09/2026 | ChatGPT/Codex | Ghi nhận Gemini 3.1 Pro High review PASS và PR #3 đang chờ Human merge approval | Đồng bộ review evidence thực tế | AI-002, REV-AI-002, PR #3 | No |
| 0.2.4 | 0.2.5 | 19/09/2026 | ChatGPT/Codex | Chuyển AI-002 sang Completed sau khi Human merge PR #3 | Đồng bộ governance state sau merge | AI-002, REV-AI-002, PR #3, merge commit `8f2b7082881961cc1a2cf7fa56ece81976759c7f` | No |
| 0.2.5 | 0.2.6 | 19/09/2026 | ChatGPT/Codex | Ghi nhận Patent Draft Generation Contract v1.0.0 và Draft Generation Prompt v1.0.0 đã triển khai, chờ Gemini review | Đồng bộ quyết định Human và bằng chứng AI-003 | AI-003, ADR-008 | No |
| 0.2.6 | 0.2.7 | 20/09/2026 | ChatGPT/Codex | Ghi nhận Gemini 3.1 Pro High independent review AI-003 PASS, không có finding hoặc required change | Đồng bộ review evidence thực tế trước commit, PR và merge | AI-003, ADR-008, REV-AI-003 | No |
| 0.2.7 | 0.2.8 | 20/09/2026 | ChatGPT/Codex | Chuyển AI-003 sang Completed sau khi Human merge PR #5 | Đồng bộ governance state sau merge | AI-003, REV-AI-003, PR #5, merge commit `fb522bc5ecbb5ad66bab6226fa88ae51020cef52` | No |
| 0.2.8 | 0.2.9 | 20/09/2026 | ChatGPT/Codex | Ghi nhận Patent DOCX Template v1.0.0, offline renderer và automated validation đã triển khai | Đồng bộ quyết định Human và bằng chứng DOC-001 trước visual QA/review | DOC-001, ADR-009 | No |
| 0.2.9 | 0.2.10 | 20/09/2026 | ChatGPT/Codex | Ghi nhận Human Visual QA và Gemini independent review DOC-001 đều PASS, không có finding | Đồng bộ governance state trước Human merge approval | DOC-001, ADR-009, REV-DOC-001 | No |
| 0.2.10 | 0.2.11 | 20/09/2026 | ChatGPT/Codex | Chuyển DOC-001 sang Completed sau khi Human merge PR #7 | Đồng bộ governance state sau merge | DOC-001, ADR-009, REV-DOC-001, PR #7, merge commit `d208a7925da844c5b43578bac8ebdbb1c5c6b5b8` | No |
| 0.2.11 | 0.3.0 | 20/09/2026 | ChatGPT/Codex | Phê duyệt baseline SPEC-002, ghi nhận ADR-001…005 và khóa scope upload APP-001 | Đồng bộ Gemini review và Human decisions trước backend implementation | SPEC-001/002/003, REV-001/002/003, DEC-001/002/003, APP-001 | No |
| 0.3.0 | 0.3.1 | 20/09/2026 | ChatGPT/Codex | Ghi APP-001 hoàn tất sau Gemini PASS và Human merge PR #10 | Đồng bộ post-merge governance evidence, không đổi contract kỹ thuật | APP-001, REV-APP-001, PR #10, merge commit `0df4814ff1eb8cd576566ac3dd403131feca3759` | No |
| 0.3.1 | 0.3.2 | 21/09/2026 | ChatGPT/Codex | Ghi APP-002 hoàn tất sau remediation, Gemini targeted PASS và Human merge PR #12 | Đồng bộ post-merge governance evidence, không đổi contract kỹ thuật | APP-002, REV-APP-002, PR #12, merge commit `4a001d116cbf002bdd42a9151efbf3f308fce3e6` | No |
| 0.3.2 | 0.3.3 | 21/09/2026 | ChatGPT/Codex | Ghi AI-RUNTIME-001 internal extraction runtime đã triển khai và chờ independent review | Đồng bộ runtime configuration, validation boundary và blocker disposition đã được Human phê duyệt | AI-RUNTIME-001, ADR-010 | No |
| 0.3.3 | 0.3.4 | 21/09/2026 | ChatGPT/Codex | Chuyển AI-RUNTIME-001 sang Completed sau remediation, targeted re-review PASS và Human merge PR #14 | Post-merge governance closeout; không đổi technical contract | AI-RUNTIME-001, REV-AI-RUNTIME-001, PR #14, merge commit `597f6c7b074eb2c5e445790b8c4f48f336f04da5` | No |
| 0.3.4 | 0.3.5 | 22/09/2026 | Gemini 3.8 Flash High | Chuyển AI-RUNTIME-002 sang Completed sau remediation, independent review APPROVED và Human merge PR #16 | Post-merge governance closeout; không đổi technical contract | AI-RUNTIME-002, REV-AI-RUNTIME-002, PR #16, merge commit `978516a4f5caa90bbd2189668237c6e028597361` | No |
| 0.3.5 | 0.3.6 | 22/09/2026 | Gemini 3.8 Flash High | Ghi nhận hoàn tất đặc tả kỹ thuật APP-003 Core Pipeline Orchestration v1.0.0, chờ independent review | Đặc tả kỹ thuật nội bộ trước implementation | APP-003, `docs/tasks/APP-003-core-pipeline-orchestration.md` | No |
| 0.3.6 | 0.3.7 | 22/09/2026 | Gemini 3.8 Flash High | Cập nhật đặc tả kỹ thuật APP-003 v1.1.0 sau independent review, chờ re-review | Đồng bộ trạng thái remediated chờ re-review | APP-003, REV-APP-003 | No |
| 0.3.7 | 0.3.8 | 22/09/2026 | Gemini 3.8 Flash High | Làm cứng đặc tả APP-003 v1.2.0: xử lý residual findings H-001 (cleanup exception safety helper), H-002 (Python 3.12 portable regression), H-003 (AC-29 framework routes) | Đồng bộ trạng thái hardened trước targeted re-review | APP-003, H-001, H-002, H-003 | No |
| 0.3.8 | 0.3.9 | 22/09/2026 | Gemini 3.8 Flash High | Đóng vòng đời đặc tả APP-003: Human duyệt v1.2.0, merge PR #18 tại bfbcdc7; ghi nhận implementation chưa bắt đầu (hoãn đến 26/09/2026 cho Codex) | Post-merge specification governance closeout; không đổi technical contract | APP-003, REV-APP-003, PR #18, merge commit `bfbcdc760916f497b603bcd49ce0150d6819d337` | No |
| 0.3.9 | 0.4.0 | 26/09/2026 | ChatGPT | Cập nhật operating model: Codex implementation, Antigravity independent review, Project Orchestrator MCP coordination; loại NotebookLM khỏi workflow hiện tại | Đồng bộ workflow thực tế do Human quyết định | Human decision 26/09/2026 | No |
| 0.4.0 | 0.4.1 | 27/09/2026 | Codex | Ghi P0-006 Frontend/backend integration CLOSED / Completed sau independent review PASS và Human-approved merge; giữ BLK-003/GOV-P0-006-01 OPEN | Post-merge governance closeout, không đổi technical contract | P0-006, REV-P0-006-IMPLEMENTATION, merge `3207479e5cca73da3e7facbc7c482d2ce5eba2b9` | No |
| 0.4.1 | 0.4.2 | 27/09/2026 | Codex | Đối chiếu APP-003 implementation/merge evidence, chuyển trạng thái sang Completed — Merged và RESOLVED GOV-P0-006-01; BLK-003 vẫn OPEN | Sửa stale governance state; không đổi technical specification hoặc P0-006 lifecycle | APP-003, GOV-P0-006-01, merge `b5a47f6030441b438e7e1745b75b05d8b345d6c0` | No |
| 0.4.2 | 0.4.3 | 27/09/2026 | Codex | Register draft P0-007 MVP E2E Validation & Stabilization specification v0.1.0 for independent review | Plan synthetic/offline integration validation without starting implementation or changing product scope | P0-007; baseline `403deba9d33d1cc20c3d231bc08fa473420505ed`; BLK-003 OPEN | No |
| 0.4.3 | 0.4.4 | 27/09/2026 | Codex | Record P0-007 specification review PASS/Human implementation approval and test-only implementation handoff for independent implementation review | Evidence-only lifecycle update; no production or release claim | P0-007; specification `f98cf600f47a6559175c10dc3498846a7ae4395b`; code `2638c620a36e6fb4016ed2efaeb788446a5b2eff`; BLK-003 OPEN | No |
| 0.4.4 | 0.4.5 | 27/09/2026 | Codex | Record P0-007 independent implementation review PASS, Human merge approval and merge; close task while preserving production blockers | Post-merge governance closeout without technical or release change | P0-007, REV-P0-007-IMPLEMENTATION, merge `26b12450284b9331f79fbbffe3220d93e40c0916`; BLK-003 OPEN | No |
| 0.4.5 | 0.4.6 | 28/09/2026 | Codex | Register P0-008 release/handover readiness specification v0.1.0 for independent review; supersede obsolete P0-007 closeout next action | Targeted local/synthetic handover audit and planning only; no implementation, release or production claim | P0-008; base main `8142692c6e92670b4b09996d733f93c409e93e49`; BLK-003 OPEN | No |
| 0.4.6 | 0.4.7 | 28/09/2026 | Codex | Record P0-008 specification review PASS, Human implementation approval, fresh local/synthetic verification and pending implementation review; preserve MCP exception/BLK-003 | Implementation handoff without granting handover or production classification | P0-008; spec `52d3c62d3741e9e7abc98c2bf2b300b4885f316c`; `REV-P0-008-SPECIFICATION` | No |
| 0.4.7 | 0.4.8 | 28/09/2026 | Codex | Record P0-008 independent implementation PASS, Human local/synthetic handover acceptance and implementation merge | Post-merge current-state closeout only; no production claim | P0-008, `REV-P0-008-IMPLEMENTATION`, merge `e6b2f665f6334047ec420c49d2097732f2917354` | No |
| 0.4.8 | 0.4.9 | 28/09/2026 | Codex | Record Human-approved P0-009 CI implementation and Playwright interpreter portability decision; update next review gate | Current-state traceability without changing product scope or claiming review/merge | P0-009, DEC-015; baseline `bf837ef10622160fc76f80227e23f81830d69f76` | No |
| 0.4.9 | 0.4.10 | 28/09/2026 | Codex | Close P0-009 after Gemini re-review, Human-approved PR #28 merge and successful PR/main CI | Post-merge current-state reconciliation; offline CI only, no production approval | P0-009, REV-P0-009-IMPLEMENTATION, merge `1f1754607152053ed4788f7fd5208c782432a320`; BLK-003 OPEN | No |
| 0.4.10 | 0.4.11 | 28/09/2026 | Codex | Record EVAL-001 specification review, seven Human decisions and framework-only implementation handoff; product-runtime semantic evidence remains blocked | Current-state reconciliation without changing approved technical requirements or claiming semantic acceptance | EVAL-001, REV-EVAL-001-SPECIFICATION, spec `67c8d71f79712ede8780babf890a79fcbfd2769e`; BLK-003 OPEN | No |
| 0.4.11 | 0.4.12 | 28/09/2026 | Codex | Record EVAL-001 Draft PR #29 CI success and independent framework review handoff | Add verified CI evidence without changing semantic/provider authorization state | EVAL-001, CI `36404294487`, framework `b8a7ede8f18ca50dedd669fcd47365dd8ed250bc` | No |
| 0.4.12 | 0.4.13 | 29/09/2026 | Codex | Record framework review PASS, Human corpus acceptance and authorized candidate-gold completion while preserving gold/provider blocks | EVAL-001 phased-state reconciliation | EVAL-001, reviewed `1c077bbb0d53304e44ad0ff7639ea3866b30fb5f`, PR #29; BLK-003 OPEN | No |
| 0.4.13 | 0.4.14 | 29/09/2026 | Codex | Record Gemini targeted gold PASS/findings NONE and Human acceptance of all six gold packages; retain runtime/provider blockers | EVAL-001 acceptance-state transition only | EVAL-001, gold completion `98101a894b1a60b16adfd867d3276215635c26d0`, DEC-019; BLK-003 OPEN | No |
| 0.4.14 | 0.4.15 | 29/09/2026 | Codex | Record EVAL-001 framework and accepted gold baseline merge plus successful main CI; retain product-runtime gate | Post-merge governance reconciliation without semantic or provider approval | EVAL-001, PR #29, merge `2caf3e6c698745a1c2b09d5605e8fba955bca2f9`, CI `36521178496`; BLK-003 OPEN | No |
| 0.4.15 | 0.4.16 | 29/09/2026 | Codex | Record Human-approved local/synthetic MVP completion boundary and defer EVAL-001 product-runtime pending funding | P0-010 final closeout proposal; no semantic or production approval | P0-010, DEC-020, baseline `6136a0fe40a214ceec10f2f58aaa99497f62b09e`; BLK-003 OPEN | No |
| 0.4.16 | 0.4.17 | 29/09/2026 | ChatGPT | Record P0-010 independent final closeout PASS, Human-approved PR #30 merge and successful main CI; finalize bounded local/synthetic MVP classification | Post-merge final project governance reconciliation; no semantic/provider/production approval | P0-010, REV-P0-010-FINAL-CLOSEOUT, PR #30, merge `9f31dae104438a598b0fe3c9bd09aba005f9026c`, CI `36526457334`, DEC-021; BLK-003 OPEN | No |
| 0.4.17 | 0.4.18 | 29/09/2026 | ChatGPT | Record P1-001 independent review PASS/findings NONE, Human-approved PR #33 merge and successful final main CI | Post-MVP zero-cost accessibility/type-safety hardening closeout; preserve provider/semantic/production boundaries | P1-001, REV-P1-001-IMPLEMENTATION, DEC-022, merge `56d7217c0f09fe591585cb298e0b4df0c92f8aa4`, CI `36536768516`; BLK-003 OPEN | No |
| 0.4.18 | 0.4.19 | 29/09/2026 | ChatGPT | Register DEPLOY-001 as a planned zero-cost demo/staging deployment task with synthetic/demo-only public URL boundary | Make public-demo work explicit without granting production, provider, platform or real-data authorization | HUMAN-DEPLOY-001-ROADMAP-REGISTRATION-2026-09-29; baseline `166691bcdcb84636f02c3cd24631a5ad51fe3c44`; BLK-003 OPEN | No |
| 0.4.19 | 0.4.20 | 01/10/2026 | ChatGPT | Record final P1-005 closeout PASS/merge/CI and Human authorization of P1-006 UX Polish | Reconcile current Post-MVP task state before P1-006 implementation | P1-005 closeout reviewed `2765dde0eaa99e9d8d9f989876d1310b1843424e`, merge `90ead2c0f26f17c617cfa71e6d7b3d16808d46e1`, CI `36811043597`; `HUMAN-P1-006-UX-POLISH-2026-10-01`; BLK-003 OPEN | No |
| 0.4.20 | 0.4.21 | 01/10/2026 | ChatGPT | Record P1-006 implementation PASS/merge/main-CI, governance closeout PASS/merge and successful final main CI | Final post-MVP UX task reconciliation without widening provider, production, data or deployment scope | P1-006 implementation reviewed `59c65deec60ae80e3ba6d28220466c2bdbfed815`, merge `659e46fa80321e037f384e0e8a09bbe90646da35`; closeout reviewed `d46a7101d8aefedd14ece29db50c8f3b00ebbde9`, merge `829c83130c6eb6018897cd5a8f62332408193142`; final CI `36834543602`; BLK-003 OPEN | No |
| 0.4.21 | 0.4.22 | 01/10/2026 | ChatGPT | Record Human authorization of DEPLOY-001 implementation while retaining the separate hosting-platform decision gate | Open the next roadmap task after P1-006 without inferring a platform, production, provider or real-data approval | `HUMAN-DEPLOY-001-IMPLEMENTATION-2026-10-01`; baseline `ed16fbc24d0ee06d7c2294a49bf243a448e6df87`; branch `feat/deploy-001-demo-staging`; BLK-003 OPEN | No |
| 0.4.22 | 0.4.23 | 01/10/2026 | ChatGPT | Record Human selection of Render for DEPLOY-001 and hand off platform-specific implementation | Resolve the Section 19 platform gate without widening zero-cost synthetic/demo boundaries | `HUMAN-DEPLOY-001-PLATFORM-RENDER-2026-10-01`; Render; branch `feat/deploy-001-demo-staging`; BLK-003 OPEN | No |
| 0.4.23 | 0.4.24 | 01/10/2026 | Codex | Record provider-free Render demo implementation and local verification; retain review/merge/live-deploy gates | Current-state reconciliation before fixed-SHA review | DEPLOY-001; backend 447 passed / 3 skipped; Playwright 19 + 3 passed; public URLs NOT DEPLOYED / NOT RECORDED; BLK-003 OPEN | No |
| 0.4.24 | 0.4.25 | 02/10/2026 | ChatGPT | Record DEPLOY-001 implementation/rewrite reviews, merges, successful main CI, verified Render deployment and public same-origin smoke evidence | Reconcile completed public synthetic demo evidence while preserving non-production/provider/data boundaries | DEPLOY-001; reviews `d76089e49ccd4aa268375cf44ae994c04e3b9c58` and `755239a49e13775b9b2b904f38fd192f63f4264c`; merges `b72efa0579aacbb4887b30e6bd8eab49ed5e8d60` and `3a31bc7c26cd14c2529c7381e96c32fa3f1a1e0c`; CI `36952647096`; public frontend/backend verified; BLK-003 OPEN | No |
| 0.4.25 | 0.4.26 | 02/10/2026 | ChatGPT | Start P2-001 USPTO Patent Specification Target v2.0.0 and reference-corpus definition after Human authorization | Align the next productization phase with the clarified scientific-paper → USPTO-style specification objective while keeping runtime/provider/data boundaries unchanged | `HUMAN-P2-001-USPTO-TARGET-2026-10-02`; baseline `eab9cd8d9421cb5bc40dc18134716febc16ac7cd`; P2-001 specification only; BLK-003 OPEN | No |
| 0.4.26 | 0.4.27 | 02/10/2026 | Codex | Record the complete P2-001 machine-readable target contract, template, structural maps, synthetic fixtures and offline/full-regression evidence; hand off exact SHA for independent review | Reconcile the expanded Human directive without introducing runtime, provider, real-data or production behavior | `HUMAN-P2-001-USPTO-TARGET-2026-10-02`; P2-001 READY FOR INDEPENDENT FIXED-SHA REVIEW; BLK-003 OPEN | No |
| 0.4.27 | 0.4.28 | 02/10/2026 | ChatGPT | Record P2-001 Gemini 3.1 Pro High PASS/findings NONE, PR #56 merge and successful post-merge main CI; open documentation-only governance closeout | Reconcile verified implementation completion while preserving provider/data/production boundaries and MCP limitation | Reviewed `8b55fd84ab1625bf918192c889dafe64825858b4`; merge `4cb0e9501c13b9d25b427bbaf7d50c37ab6ab329`; main CI `36962586792` SUCCESS; P2-001 implementation merged; governance closeout review pending; BLK-003 OPEN | No |
| 0.4.28 | 0.4.29 | 02/10/2026 | ChatGPT | Record P2-001 closeout review PASS/findings NONE, PR #58 merge/final main CI, and start Human-authorized P2-000 specification | Close P2-001 fully and open the next product-facing frontend simplification task without expanding runtime/provider/data/production scope | P2-001 closeout reviewed `a95ac5c9d5e19dc04216a8f945ff38f1872c39a9`; PR #58 merge `461d9b33b07bb39aad11aa47b84f678e232d80a8`; final CI `36965942755`; `HUMAN-P2-000-WEBAPP-SIMPLIFICATION-2026-10-02`; BLK-003 OPEN | No |

## 2. Project name

**AI Intellectual Property Description Generator**

## 3. Repository

`ai-ip-description-generator`

Repository: `https://github.com/nshaokiet/ai-ip-description-generator`.

Visibility: **Private**, đã xác minh ngày 18/09/2026.

## 4. Problem Statement

Bài báo nghiên cứu khoa học không được viết theo cấu trúc patent specification. Việc chuyển đổi thủ công cần nhiều thời gian và dễ mất liên kết giữa phát biểu kỹ thuật với tài liệu nguồn. Dự án xây một workflow có kiểm soát để trích xuất, chuẩn hóa, phát hiện thiếu thông tin, tạo bản dự thảo và giữ source evidence cho từng nội dung quan trọng.

## 5. Business Objective

- Rút ngắn giai đoạn chuẩn bị bản nháp ban đầu.
- Chuẩn hóa thông tin để tác giả và chuyên gia SHTT review.
- Giảm hallucination bằng source grounding và Human-in-the-loop.
- Tạo DOCX có thể chỉnh sửa và truy vết về phiên bản đầu vào/output.

Sản phẩm không thay thế chuyên gia SHTT và không đưa ra kết luận pháp lý.

## 6. Input

Một scientific research paper:

- PDF.
- DOCX.

MVP/APP-001 chỉ nhận PDF có text và DOCX, tối đa 10 MiB; PDF tối đa 50 trang. Scanned PDF/OCR bị loại khỏi MVP. DOCX không thể kiểm đếm trang exact một cách tin cậy nếu không render; APP-001 không tuyên bố exact page-limit enforcement cho DOCX.

Người dùng phải có quyền hợp pháp để upload và xử lý tài liệu. Không commit bài báo chưa công bố vào repository.

## 7. Output

- Structured invention information.
- Evidence mapping tới file/trang/mục/đoạn/bảng/hình khi xác định được.
- Missing-information list và câu hỏi cho tác giả.
- Draft patent specification.
- Claims/Draft Claims nằm ngoài MVP hiện hành; task tương lai cần Human scope approval riêng.
- Abstract tối đa 150 từ.
- Structured JSON.
- DOCX.
- PDF, QA report và claim–description–source mapping: `[CẦN XÁC NHẬN]` đối với MVP.

Mọi đầu ra là **bản dự thảo cần Human hoặc chuyên gia SHTT review**. Đây không phải bằng sáng chế đã cấp, tư vấn pháp lý, kết luận patentability, hồ sơ chắc chắn đủ điều kiện nộp hoặc được USPTO chấp thuận.

## 8. Core Workflow

`Research paper → validation → AI analysis → structured extraction → grounding validation → missing-information detection → draft → human review → DOCX`

Pipeline MVP ưu tiên một paper cho một hồ sơ. Nội dung thiếu không được tự bịa; dùng `[CẦN TÁC GIẢ XÁC NHẬN]`.

## 9. Architecture

`Next.js → FastAPI → OpenAI Responses API → Structured Outputs → Validation → Draft generation → docxtpl → DOCX`

- Next.js: upload, progress, review, edit, section status và export UI.
- FastAPI: API, orchestration, validation, versioning, audit và document generation.
- OpenAI Responses API: extraction/drafting theo prompt và schema có version.
- Validation: schema, business rules, grounding, consistency và claim support.
- `docxtpl`: render DOCX template có version.
- APP-001 chỉ dùng local ephemeral storage cho single-tenant/synthetic development; xóa ngay khi validation thất bại, sau pipeline/rendering, hoặc muộn nhất sau 1 giờ.
- Private production storage/authentication/database: thiết kế cụ thể `[CẦN XÁC NHẬN]`; không dùng dữ liệu nghiên cứu thật trước security acceptance.
- Supabase/PostgreSQL chỉ là optional/MVP+ hoặc dùng khi được Human phê duyệt.

## 10. Tech Stack

| Lớp | Công nghệ đã định hướng | Trạng thái |
|---|---|---|
| Frontend | Next.js + TypeScript | P0-005 Frontend MVP CLOSED; P0-006 frontend/backend integration CLOSED / Completed — merged at `3207479e5cca73da3e7facbc7c482d2ce5eba2b9`; local synthetic-only, not production-ready |
| Backend | FastAPI + Python 3.12 | APP-001/APP-002 và AI-RUNTIME-001/002 Completed; P0-006 opt-in local validation/export API merged; no production authentication or private storage approval |
| Production AI | OpenAI Responses API | AI-RUNTIME-001: `gpt-5.6-sol`, reasoning high, `store=false`, timeout 180s, max 48k tokens; AI-RUNTIME-002: `gpt-5.6-sol`, reasoning high, `store=false`, timeout 240s, max 64k tokens; internal only; live provider smoke NOT RUN — DEFERRED due to unavailable API funding |
| Structured data | JSON Schema Draft 2020-12 | Output Schema v1.0.0 — Completed — Merged via PR #1 |
| Extraction prompt | Markdown prompt contract | v1.0.0 — Completed — Merged via PR #3 |
| Patent draft contract | JSON Schema Draft 2020-12 | v1.0.0 — Completed — Merged via PR #5 |
| Draft generation prompt | Markdown prompt contract | v1.0.0 — Completed — Merged via PR #5 |
| Retrieval | Không dùng trong Extraction Runtime v1 hoặc Draft Runtime v1 | AI-RUNTIME-001/AI-RUNTIME-002 chỉ dùng input envelopes; task tương lai cần approval riêng |
| Database | Supabase/PostgreSQL | Optional/MVP+ hoặc khi được phê duyệt |
| DOCX | `docxtpl==0.20.2`, `python-docx==1.2.0` | Patent DOCX Template v1.0.0 — Completed — Merged via PR #7 |
| Demo/staging deployment | Render | DEPLOY-001 **CLOSED / COMPLETED — PUBLIC SYNTHETIC DEMO VERIFIED; CLOSEOUT REVIEW PENDING**. Frontend `https://ai-ip-synthetic-demo-frontend.onrender.com`; backend `https://ai-ip-synthetic-demo-backend.onrender.com`; deployed main `3a31bc7c26cd14c2529c7381e96c32fa3f1a1e0c`; synthetic PDF/DOCX same-origin flows PASS; BLK-003 OPEN; production NOT APPROVED |
| Production deployment | Platform TBD | **NOT APPROVED / NOT PERFORMED**; requires SEC-001/BLK-003 resolution, real-data/security acceptance and separate Human approval |
| Version control | GitHub | Technical Source of Truth |

Không tự ý thêm framework, dịch vụ hoặc dependency.

## 11. AI Architecture

1. Parse paper và giữ locator.
2. APP-002 tạo deterministic evidence source units; Extraction Runtime v1 không dùng File Search hoặc external retrieval.
3. AI-RUNTIME-001 extraction bằng prompt/schema version cụ thể và provider schema được dẫn xuất.
4. Validate canonical JSON, provenance và logical reference.
5. Detect missing information, tạo author questions.
6. AI-RUNTIME-002 patent draft generation từ validated analysis, strict provider schema, schema-aware normalization, canonical Draft 2020-12 validation và deterministic business validation.
7. Grounding/consistency validation.
8. Human review trước export.

Không fine-tune và không xây multi-agent runtime phức tạp trong MVP nếu chưa có quyết định riêng.

## 12. Source-grounding model

| Nhãn | Ý nghĩa | Quy tắc |
|---|---|---|
| `SOURCE_FACT` | Có căn cứ trực tiếp | Phải có evidence locator khi xác định được |
| `PARAPHRASE` | AI diễn đạt lại nội dung có nguồn | Không làm đổi ý nghĩa kỹ thuật |
| `INFERENCE` | AI suy luận | Hiển thị rõ, không nâng thành fact |
| `MISSING` | Chưa có căn cứ | Không tự điền; tạo câu hỏi nếu cần |
| `HUMAN_CONFIRMED` | Human có thẩm quyền xác nhận | Phải có audit record |

Evidence nên gồm source file, page, section, paragraph/chunk, table/figure, excerpt ngắn, evidence type và Human status.

Output Schema v1.0.0 có phạm vi hẹp hơn mô hình toàn hệ thống: grounding object chỉ chấp nhận `SOURCE_FACT`, `PARAPHRASE`, `INFERENCE`, đều phải có `evidence_ids`. `MISSING` nằm trong `missing_information`; `HUMAN_CONFIRMED` và audit reference không thuộc v1.0.0. Claims cũng bị loại hoàn toàn khỏi contract này.

## 13. MVP Scope

- Upload/validation PDF và DOCX.
- Parse và AI document analysis.
- Structured extraction cho problem, solution, components/process steps, distinguishing features tiềm năng, effects, embodiments và experiments.
- Evidence, grounding labels, missing information và author questions.
- Draft patent specification và Abstract; không Claims.
- Human review, edit, section status và version tracking.
- Grounding/consistency validation.
- DOCX export.
- Error handling, activity history, privacy/security tối thiểu được phê duyệt.

## 14. Non-MVP Scope

- Tự động nộp USPTO.
- Patentability/novelty/inventive-step conclusion.
- Prior-art search toàn diện.
- Inventorship hoặc legal advice.
- Cam kết đầu ra sẵn sàng nộp/được cấp.
- Claims/Draft Claims trong MVP hiện hành.
- Fine-tuning, complex multi-agent runtime.
- Hỗ trợ đầy đủ mọi loại hồ sơ SHTT/jurisdiction.

## 15. Data handling principles

- Source paper, parsed content, evidence, output và logs là các loại dữ liệu riêng.
- Source/derived data phải ở private storage; storage provider `[CẦN XÁC NHẬN]`.
- Chỉ thu thập và log metadata cần thiết; không log toàn văn paper.
- Có delete path cho source và derived data.
- Retention cho source, output, logs, backup: `[CẦN XÁC NHẬN]`.
- Không dùng dữ liệu để fine-tune/dataset nếu chưa có phép.
- Không mặc định provider AI được phép lưu/sử dụng dữ liệu; phải review policy.

## 16. Security principles

- API key backend-only và lấy từ environment/secret manager.
- Authentication, authorization, tenant isolation: `[CẦN XÁC NHẬN]`.
- TLS in transit; encryption at rest `[CẦN XÁC NHẬN]` theo provider.
- Validate file type/signature/size; malware scanning `[CẦN XÁC NHẬN]`.
- Least privilege, private download, redacted logs và secret rotation.
- Không commit paper mật, secret, `.env` thật hoặc generated output nhạy cảm.

## 17. Current assumptions

- Deadline MVP là 02/10/2026.
- Mục tiêu hoàn thành nội bộ là 30/09/2026; ngày 01–02/10 dành cho buffer, test và handover.
- Một paper cho một hồ sơ MVP.
- Repository dự kiến private.
- OpenAI là production AI; Gemini là reviewer, không phải dependency runtime.
- Human/chuyên gia SHTT sẽ review output.
- Hai tài liệu US11367264B2 và US11044591B2 là patent references có mã B2, không phải biểu mẫu USPTO tên “mẫu B”.
- Các assumption chưa được Human phê duyệt vẫn là assumption, không phải decision.

## 18. Important terminology

| Thuật ngữ | Giải thích trong dự án |
|---|---|
| Patent specification | Phần mô tả hồ sơ sáng chế; output của hệ thống chỉ là draft |
| B2 | Kind code của bằng sáng chế tiện ích đã được cấp theo tài liệu tham chiếu; không phải tên form |
| Structured Output | JSON tuân thủ schema để máy kiểm tra và xử lý |
| Source grounding | Liên kết phát biểu với bằng chứng trong nguồn |
| Evidence | Locator và excerpt hỗ trợ một nội dung |
| Human-in-the-loop | Human bắt buộc review/xác nhận trước sử dụng quan trọng |
| Hallucination | Nội dung AI tạo nhưng không có căn cứ hoặc sai nguồn |
| Claim | Câu xác định phạm vi bảo hộ được yêu cầu; ở đây chỉ là Draft Claim |
| Embodiment | Phương án thực hiện cụ thể được mô tả và có support |
| Prior art | Thông tin công khai trước thời điểm liên quan; MVP không làm search toàn diện |
| ADR | Architecture Decision Record ghi quyết định, lý do và phương án thay thế |
| Source of Truth | Nguồn chính thức được ưu tiên khi có mâu thuẫn |

## 19. Current project phase

Giai đoạn khởi tạo đề xuất: **Phase 1 — Specification & Architecture**.

SPEC-001, SPEC-002 và SPEC-003 là **Approved baseline** sau Gemini 3.1 Pro High review và Human decisions ngày 20/09/2026. Human / Product Owner đã chốt phân loại **MVP COMPLETE — LOCAL/SYNTHETIC** cho phạm vi bounded hiện hành (DEC-020/DEC-021). P0-010 đã **CLOSED / COMPLETED — MERGED** qua PR #30 tại `9f31dae104438a598b0fe3c9bd09aba005f9026c` sau Gemini 3.1 Pro High targeted final closeout review **PASS**, findings **NONE**; main CI `36526457334` **SUCCESS**. Điều này không tuyên bố semantic PRODUCT_RUNTIME validation, production readiness, public deployment hoặc real/confidential-data readiness.

P0-006 Frontend/backend integration là **CLOSED / Completed — Merged** tại `3207479e5cca73da3e7facbc7c482d2ce5eba2b9` (accepted implementation `0f1e94db438869a980db8a1cb1e06956de2d8d3e`). Google Antigravity (Advanced Agentic Coding) independent review `PASS`, AC-01…AC-17 `PASS`, findings `NONE`; Human accepted review và approved merge. GOV-P0-006-01 được RESOLVED riêng bằng APP-003 governance reconciliation sau đó; BLK-003 vẫn OPEN. Không tuyên bố production/real-data readiness hay toàn bộ MVP Completed.

P0-007 MVP End-to-End Validation & Stabilization có **approved specification v0.1.0** tại `f98cf600f47a6559175c10dc3498846a7ae4395b`. Google Antigravity (Advanced Agentic Coding) independent **specification** review `PASS`, AC-01…AC-16 `PASS`, findings `NONE`, Human decisions required `NONE`; Human / Product Owner approved implementation. Sau historical test/harness handoff, Google Antigravity với reviewer profile Google Antigravity (Advanced Agentic Coding) independent **implementation** review accepted implementation/handoff SHA `bd43a7e9875537c4f5ebdee53626542a11500636` và final test-code SHA `2638c620a36e6fb4016ed2efaeb788446a5b2eff`: `PASS`, AC-01…AC-16 `PASS`, findings `NONE`, reviewer modified no files. Independent lint/build `PASS`, Playwright **11 passed**; reviewer accepted historical targeted backend **194 passed/1 skipped** and full offline backend **380 passed/3 skipped** because no production Python code changed, without independently rerunning those suites. Human accepted review and approved merge `26b12450284b9331f79fbbffe3220d93e40c0916`. Current P0-007 status **CLOSED / COMPLETED — MERGED**. Phạm vi local synthetic/offline; BLK-003 **OPEN**, live-provider smoke **UNVALIDATED / DEFERRED**, no real/confidential-data or production-readiness approval, Claims outside MVP.

P0-007 post-merge closeout was fast-forwarded into `main` at `8142692c6e92670b4b09996d733f93c409e93e49`. P0-008 **MVP Release & Handover Readiness Specification v0.1.0** at `52d3c62d3741e9e7abc98c2bf2b300b4885f316c` received independent Google Antigravity (Advanced Agentic Coding) specification review **PASS**, AC-01…AC-16 PASS, findings NONE, Human decisions required NONE. Human / Product Owner approved implementation. The subsequent independent **implementation** review of `956ba93048536d2a54d120752ade5540ecc0d901` was **PASS**, findings **NONE**; Human accepted the review, completed AC-16, approved the local/synthetic handover classification and merge. P0-008 is now **CLOSED / COMPLETED — MERGED** at `e6b2f665f6334047ec420c49d2097732f2917354`; the engineering baseline is **MVP HANDOVER READY — LOCAL/SYNTHETIC**. This does not grant production readiness, public deployment, real/confidential-data use, live-provider validation or real-paper semantic-quality acceptance. BLK-003 remains **OPEN** and live-provider smoke **UNVALIDATED / DEFERRED**. See the [runbook](docs/operations/MVP_HANDOVER_RUNBOOK.md) and P0-008 task closeout; historical pre-review records remain intact.

P0-009 — CI Foundation uses Human-reconciled baseline `bf837ef10622160fc76f80227e23f81830d69f76`. Original implementation `8979c72145d95f4f539b40e9e59b2d8af2f59fab` received Gemini 3.1 Pro High **PASS WITH NON-BLOCKING NOTES**; F-01 noted GitHub Actions had not run. The first PR run `36394799769` failed in the DOCX inspection helper (Playwright 7 passed/4 failed). Human approved a narrow `PLAYWRIGHT_PYTHON` interpreter-portability remediation in the test helper; final accepted SHA `ce9f723e143671d4917bf0bf5885772af3b00f7b` received targeted Gemini 3.1 Pro High **PASS**, F-01 **RESOLVED**, new findings **NONE**. Accepted PR CI `36396184226` and post-merge `push`/`main` CI `36397653688` both **SUCCESS**; the latter ran backend **381 passed/2 skipped**, lint/build **PASS**, Chromium install **PASS**, Playwright **11 passed**. Human accepted review/CI and approved PR #28 normal merge `1f1754607152053ed4788f7fd5208c782432a320`. P0-009 is **CLOSED / COMPLETED — MERGED**; CI is **ACTIVE** for `pull_request(main)` and `push(main)` deterministic local/synthetic regression only. This does not establish semantic quality, production readiness or live-provider validation; BLK-003 remains **OPEN** and real/confidential data is not authorized.

Project Orchestrator MCP reconciliation was **BLOCKED BY TOOL CAPABILITY**: existing `P0-008` metadata remains `PLANNED` under “Final hardening”, with reviewed spec not recorded and no owner/lease. Human expressly approved a **non-blocking governance exception** for this Git-evidenced implementation. MCP is not claimed reconciled and no approval/lease/state is fabricated. A future safe admin update remains needed; this exception does not resolve BLK-003.

P0-010 final closeout decision (DEC-020, 29/09/2026): Human / Product Owner prioritizes finishing the approved local/synthetic MVP before optimization or production hardening. EVAL-001 framework and Human-accepted corpus/gold are merged (6/6 each; 154 gold items, 102 KEY/52 SECONDARY), but PRODUCT_RUNTIME semantic validation is **DEFERRED — AWAITING FUNDING**. Provider authorization **NOT GRANTED**, budget **0**, calls **NONE**; product-runtime evidence **NONE** and semantic acceptance **NOT_DETERMINED**. Consumer UI or synthetic outputs cannot substitute for PRODUCT_RUNTIME. SEC-001/BLK-003 remediation, public deployment, UX hardening and prompt/model/runtime optimization are Post-MVP work. BLK-003 remains **OPEN** and prohibits production or real/confidential-data use; it does not block this limited local/synthetic MVP classification. P0-010 is **CLOSED / COMPLETED — MERGED**. P1-001 zero-cost accessibility/type-safety hardening is also **CLOSED / COMPLETED — MERGED** via PR #33 at `56d7217c0f09fe591585cb298e0b4df0c92f8aa4` after Gemini 3.1 Pro High review **PASS**, findings **NONE**, Human merge approval and final main CI `36536768516` **SUCCESS**. See [final handover](docs/operations/FINAL_MVP_CLOSEOUT.md).

## 20. AI / Agent Roles

- **Human / Product Owner — Governance & Final Approval Authority:** quyết định scope, architecture/security/data/provider policy, approve task/gate, merge và release.
- **ChatGPT — Technical Coordinator & Architecture Advisor:** specification, architecture guidance, prompt/handoff, governance và evidence reconciliation.
- **Codex (VS Code) — Primary Implementation Agent:** implement/test/debug/commit/push approved tasks trên branch/worktree riêng; không tự approve hoặc merge.
- **Antigravity Reviewer Agent — Independent Review & QA:** review độc lập branch/SHA; exact model/profile phải được ghi trong từng review record; không sửa production artefact khi đang reviewer.
- **Project Orchestrator MCP — Coordination & State Management Layer:** task queue/lifecycle, lease, budget guard, checkpoint/handoff và shared state; không code/review/approve/merge.
- **GitHub — Technical Source of Truth:** canonical technical artefacts và evidence.

**NotebookLM không thuộc toolchain/workflow hiện tại.** Tham chiếu Gemini/NotebookLM trong historical changelog/review evidence được giữ nguyên để bảo toàn provenance.

Chi tiết quyền hạn nằm trong `AGENTS.md`.

## 21. Source of Truth

1. Human-approved decision.
2. Approved ADR.
3. Current production artefact in GitHub.
4. `docs/system-specification.md`.
5. `PROJECT_CONTEXT.md`.
6. Project Control Center.
7. Review Log.
8. MCP state/checkpoint là operational evidence, không được ghi đè các nguồn authority phía trên.

## 22. Communication Bridge

Google Drive dùng để chia sẻ:

- `01_PROJECT_CONTROL_CENTER`: trạng thái vận hành.
- `02_GEMINI_REVIEW_LOG`: historical/current review log với legacy filename; review mới phải ghi Antigravity reviewer và exact model/profile.

Bản nguồn Git hiện ở `docs/operations/`. Trạng thái tạo/đồng bộ Google Docs: `[CẦN XÁC NHẬN TRẠNG THÁI]`. Google Docs không ghi đè technical artefacts trong GitHub.

## 23. Agent Coordination Layer

Project Orchestrator MCP là lớp điều phối dùng chung giữa VS Code/Codex và Antigravity. MCP lưu task state, lease, dependency, manual quota/budget, checkpoint và handoff. MCP không phải coding agent, reviewer, approval authority hoặc Git merge engine.

## 24. Critical project rules

1. Không bịa thông tin kỹ thuật, source, decision, test hoặc trạng thái.
2. Human review bắt buộc.
3. API key chỉ ở backend.
4. Prompt/schema/template/API contract phải có version.
5. Repository GitHub phải private trước dữ liệu nhạy cảm.
6. Không commit confidential paper nếu chưa được phép.
7. Không mô tả output là tài liệu pháp lý hoàn chỉnh.
8. Không tự thay scope, deadline, tech stack hoặc architecture.
9. Mỗi nội dung kỹ thuật quan trọng phải có evidence hoặc nhãn thiếu/suy luận.
10. Codex implement; Antigravity review độc lập; MCP điều phối state; Human quyết định gate/merge/release.

## 25. Current artefacts

| Artefact | Location | Version | Status có bằng chứng |
|---|---|---|---|
| System Specification | `docs/system-specification.md` | 0.3.7 | SPEC-001 Approved baseline; factual local API/frontend/E2E status updated, requirements unchanged |
| AI Collaboration Rules | `AGENTS.md` | 0.3.1 | SPEC-003 Approved baseline; factual project-state correction only |
| Project Context | `PROJECT_CONTEXT.md` | 0.4.10 | SPEC-002 Approved baseline; P0-009 CLOSED / COMPLETED — MERGED |
| Project Control Center source | `docs/operations/01_PROJECT_CONTROL_CENTER.md` | 0.3.23 | P0-009 CLOSED; CI ACTIVE; BLK-003 OPEN |
| Gemini Review Log source | `docs/operations/02_GEMINI_REVIEW_LOG.md` | 0.3.12 | REV-P0-009-IMPLEMENTATION CLOSED; initial/re-review history preserved |
| Foundational ADRs | `docs/decisions/ADR-001…005-*.md` | ADR-001…ADR-005 | Accepted theo Human decisions ngày 20/09/2026 |
| APP-001 backend | `backend/app/`, `backend/requirements.txt`, `tests/backend/` | Implementation head `bd39b9f7bdd9f7a1796d9a405e7998070e124e07` | Completed — Merged via PR #10; 24/24 APP-001 tests và 109/109 tổng tests pass |
| APP-002 document preparation | `backend/app/`, `tests/backend/test_document_parsing.py` | Implementation `477b8fda6afbae0049d8d691c213dc6355ba67da`; remediation `8b6f909a0f5787d72c002e163395656a666c9b78` | Completed — Merged via PR #12 at `4a001d116cbf002bdd42a9151efbf3f308fce3e6`; Gemini final PASS; 30/30 AC; 135 executed, 134 pass, 1 Windows skip, 0 failure/error |
| AI extraction runtime | `backend/app/services/extraction_runtime.py`, `provider_schema.py`, `extraction_validation.py` | AI-RUNTIME-001 / ADR-010 | Completed — Merged via PR #14 at `597f6c7b074eb2c5e445790b8c4f48f336f04da5`; 32/32 AC; 201 executed, 200 pass, 1 skip; live provider smoke not run |
| AI draft runtime | `backend/app/services/draft_runtime.py`, `draft_provider_schema.py`, `draft_validation.py`, `draft_business_validation.py` | AI-RUNTIME-002 | Completed — Merged via PR #16 at `978516a4f5caa90bbd2189668237c6e028597361` (implementation head `a59ce0219d7039f24fa8c7bd71d4e9829dbbf612`); backend suite 240 pass, 2 skip; tests/draft 25 pass; live smoke deferred |
| Core pipeline orchestration | `docs/tasks/APP-003-core-pipeline-orchestration.md`, `backend/app/services/core_pipeline.py` | Specification v1.2.0; governance evidence revision 1.2.1 | APP-003 Completed — Merged; implementation `3e7c2910695eed9e5ef1d7d0ff11f8f0e3ac6c38`, merge `b5a47f6030441b438e7e1745b75b05d8b345d6c0`; merge message: 32/32 AC verified, independent Antigravity PASS; exact underlying model/profile not evidenced; BLK-003 OPEN |
| P0-006 frontend/backend integration | `docs/tasks/P0-006-frontend-backend-integration.md`, `frontend/`, `backend/app/api/routes/local_orchestration.py` | Approved specification v0.2.0; implementation `0f1e94db438869a980db8a1cb1e06956de2d8d3e` | CLOSED / Completed — Merged at `3207479e5cca73da3e7facbc7c482d2ce5eba2b9`; independent Google Antigravity (Advanced Agentic Coding) PASS, AC-01…AC-17 PASS, findings NONE; BLK-003 OPEN; GOV-P0-006-01 RESOLVED separately |
| P0-007 validation/stabilization | `docs/tasks/P0-007-mvp-e2e-validation-stabilization.md`; `frontend/e2e/`; `tests/e2e/` | Approved specification v0.1.0; implementation evidence revision 0.1.2; accepted implementation `bd43a7e9875537c4f5ebdee53626542a11500636`, final test-code `2638c620a36e6fb4016ed2efaeb788446a5b2eff` | CLOSED / COMPLETED — MERGED at `26b12450284b9331f79fbbffe3220d93e40c0916`; independent AC-01…AC-16 PASS, findings NONE; lint/build PASS, Playwright 11 passed; historical backend accepted without independent rerun; synthetic/offline only; BLK-003 OPEN |
| P0-008 release/handover readiness | `docs/tasks/P0-008-mvp-release-handover-readiness.md`, `docs/operations/MVP_HANDOVER_RUNBOOK.md` | Approved specification v0.1.0 at `52d3c62d3741e9e7abc98c2bf2b300b4885f316c`; closeout addendum 0.1.2; reviewed implementation `956ba93048536d2a54d120752ade5540ecc0d901` | CLOSED / COMPLETED — MERGED at `e6b2f665f6334047ec420c49d2097732f2917354`; review PASS, findings NONE, Human handover accepted; MVP HANDOVER READY — LOCAL/SYNTHETIC only; BLK-003 OPEN |
| P0-009 CI Foundation | `.github/workflows/ci.yml`, `frontend/playwright.config.ts`, `frontend/e2e/integration.spec.ts`, `docs/tasks/P0-009-ci-foundation.md` | Baseline `bf837ef10622160fc76f80227e23f81830d69f76`; original `8979c72145d95f4f539b40e9e59b2d8af2f59fab`; accepted `ce9f723e143671d4917bf0bf5885772af3b00f7b`; task record 0.1.1 | CLOSED / COMPLETED — MERGED via PR #28 at `1f1754607152053ed4788f7fd5208c782432a320`; Gemini targeted PASS/F-01 RESOLVED; PR CI `36396184226` and main CI `36397653688` SUCCESS; CI ACTIVE for offline regression only; BLK-003 OPEN |
| ADR | `docs/decisions/ADR-006-output-schema-v1.md` | ADR-006 | Accepted; Completed — Merged via PR #1 |
| Production JSON Schema | `schemas/invention-output/v1.0.0/invention-output.schema.json` | 1.0.0 | Completed — Merged via PR #1; Gemini review PASS; 15/15 tests pass |
| Production extraction prompt | `prompts/extraction/v1.0.0/extraction-prompt.md` | 1.0.0 | Completed — Merged via PR #3; canonical offline validation only |
| Extraction prompt ADR | `docs/decisions/ADR-007-extraction-prompt-v1.md` | ADR-007 | Accepted — Completed — Merged via PR #3 |
| Patent Draft Schema | `schemas/patent-draft/v1.0.0/patent-draft.schema.json` | 1.0.0 | Completed — Merged via PR #5 |
| Draft generation prompt | `prompts/draft-generation/v1.0.0/draft-generation-prompt.md` | 1.0.0 | Completed — Merged via PR #5; offline only |
| Patent draft ADR | `docs/decisions/ADR-008-patent-draft-contract-v1.md` | ADR-008 | Accepted — Completed — Merged via PR #5 |
| DOCX template | `templates/patent-docx/v1.0.0/patent-description-template.docx` | 1.0.0 | Completed — Merged via PR #7 |
| Application code | `backend/app/`, `frontend/` | APP-001/002, AI-RUNTIME-001/002, P0-005/006 and intervening integration tasks | Local upload/orchestration, internal extraction/draft runtimes, frontend Human review and edited-draft export are merged; production database/auth/private storage and deployment are not approved or implemented |

## 26. Open questions

1. Auth, user roles, tenant model và private production storage nào được dùng?
2. Data/log/backup retention và deletion SLA production là gì? APP-001 chỉ khóa local ephemeral TTL tối đa 1 giờ.
5. Model/cost policy cho draft runtime hoặc task AI tương lai là gì? Extraction Runtime v1 (AI-RUNTIME-001) đã khóa `gpt-5.6-sol`, timeout 180s, 48.000 output tokens; Draft Runtime v1 (AI-RUNTIME-002) đã khóa `gpt-5.6-sol`, timeout 240s, 64.000 output tokens; không retrieval; task tương lai cần approval riêng.
6. Nếu Human mở lại Claims sau MVP/scope change, loại/số lượng và reviewer chuyên môn là ai?
7. PDF/QA report/claim mapping có thuộc MVP không?
8. Golden set, metrics, threshold và tài liệu test được cấp quyền là gì?
9. Hai tài liệu vận hành đã được đồng bộ sang Google Docs hay chưa?

## 27. Recommended reading order

1. `AGENTS.md` — quyền hạn và workflow.
2. `PROJECT_CONTEXT.md` — bối cảnh nhanh.
3. `docs/system-specification.md` — requirement/architecture đầy đủ.
4. ADR trong `docs/decisions/` khi tồn tại.
5. `docs/operations/01_PROJECT_CONTROL_CENTER.md` — trạng thái và quyết định đang chờ.
6. `docs/operations/02_GEMINI_REVIEW_LOG.md` — findings và resolution.

## 28. Recommended next action

1. P1-001 — **CLOSED / COMPLETED — MERGED** via PR #33 at `56d7217c0f09fe591585cb298e0b4df0c92f8aa4`; Gemini 3.1 Pro High targeted implementation review **PASS**, findings **NONE**; final main CI [`36536768516`](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/36536768516) **SUCCESS**: backend 408 passed/2 skipped, pip check/lint/typecheck/build PASS, Playwright 15 passed, live flags 0/0. Project classification remains **MVP COMPLETE — LOCAL/SYNTHETIC**.
2. P1-002 through P1-006 are **CLOSED / COMPLETED** in Git/governance. P1-003 through P1-006 retain their documented MCP tool limitations where applicable. P1-006 implementation review PASS/NONE on `59c65deec60ae80e3ba6d28220466c2bdbfed815`, PR #50 merge `659e46fa80321e037f384e0e8a09bbe90646da35`, closeout review PASS/NONE on `d46a7101d8aefedd14ece29db50c8f3b00ebbde9`, PR #51 merge `829c83130c6eb6018897cd5a8f62332408193142`, final main CI `36834543602` SUCCESS.
3. DEPLOY-001 is **CLOSED / COMPLETED — PUBLIC SYNTHETIC DEMO VERIFIED**. Implementation review PASS/NONE on `d76089e49ccd4aa268375cf44ae994c04e3b9c58`; rewrite-remediation review PASS/NONE on `755239a49e13775b9b2b904f38fd192f63f4264c`; PR #55 governance closeout review PASS/NONE and merge `eab9cd8d9421cb5bc40dc18134716febc16ac7cd`; final main CI `36954939862` SUCCESS. Public frontend/backend and same-origin PDF/DOCX flows are verified.
4. P2-001 is **CLOSED / COMPLETED — MERGED** under `HUMAN-P2-001-USPTO-TARGET-2026-10-02`. Implementation review PASS/NONE on `8b55fd84ab1625bf918192c889dafe64825858b4`; PR #56 merge `4cb0e9501c13b9d25b427bbaf7d50c37ab6ab329`; closeout review PASS/NONE on `a95ac5c9d5e19dc04216a8f945ff38f1872c39a9`; PR #58 merge/current main `461d9b33b07bb39aad11aa47b84f678e232d80a8`; final main CI `36965942755` SUCCESS with backend 467 passed / 2 skipped, lint/typecheck/build PASS, Playwright 19 + 3 PASS. No provider/API spend, real/confidential data, Claims runtime or production change was introduced.
5. P2-000 — **AUTHORIZED / IMPLEMENTATION-READY SPECIFICATION; SPEC PR REVIEW PENDING** under `HUMAN-P2-000-WEBAPP-SIMPLIFICATION-2026-10-02`. Human approved an Enterprise SaaS layout using the existing VNUHCM Innovation Hub logo/color system, five visible stages Source Upload → AI Extraction → Review & Refine → Validation → DOCX Export, product-level Go back/reached-step navigation, wrong-paper remove/replace behavior, draft-first results and compact technical metadata. No backend, provider, schema, Claims, real-data, production or deployment change is authorized.
5. EVAL-001 PRODUCT_RUNTIME remains **DEFERRED — AWAITING FUNDING**, evidence NONE, semantic acceptance NOT_DETERMINED; provider authorization NOT GRANTED / budget 0. BLK-003 remains OPEN; no production/real-confidential-data authorization.

AI-002 được merge với implementation commit `f8772b228a23bf7cdec10fa0c463e6d1f672c341` và governance commit `9f2a78b1396cdadb747c263a2bbbbacb8d7f4292`; Gemini review `PASS`, không có finding, AI-001 regression 15/15 và AI-002 tests 17/17 pass. AI-002 tự thân không chứng minh Responses API hoặc live-model integration; provider adapter/runtime sau đó được Human phê duyệt riêng trong AI-RUNTIME-001. Claims vẫn nằm ngoài Output Schema và Extraction Prompt v1.0.0.

AI-003 triển khai contract trung gian `Validated Output Schema v1.0.0 → Patent Draft Generation Contract v1.0.0 → DOCX template`. Contract giữ exact 11-part order cho DOC-001, paragraph-level source paths/evidence, explicit missing/conflict state và loại hoàn toàn Claims, legal advice, patentability conclusions cùng Human approval state. Fixtures chỉ là synthetic offline oracles; chưa có live-model hoặc provider integration. Gemini 3.1 Pro High review `PASS`, không có finding hoặc required change. Human / Product Owner đã approve và merge PR #5 ngày 20/09/2026; implementation commit `ae7e8fb573ea4681a9db1bafa711d19a3c598666`, merge commit `fb522bc5ecbb5ad66bab6226fa88ae51020cef52`. Trạng thái hiện tại: **Completed — Merged via PR #5**.

DOC-001 triển khai Patent DOCX Template v1.0.0 và deterministic offline renderer từ payload Patent Draft Generation Contract v1.0.0. Template dùng A4, lề 2.54 cm, Times New Roman, exact eleven-part order, header/footer và PAGE/NUMPAGES fields. Renderer validate schema trước khi dùng `docxtpl`, không gọi API/model/mạng, giữ missing/conflict/inference/evidence và loại Claims khỏi mapping. Fixtures hoàn toàn synthetic. Human Microsoft Word Visual QA, Gemini 3.1 Pro High independent review và targeted governance review đều `PASS`; không có finding hoặc required change; 85/85 tests pass. Human / Product Owner đã approve và merge [PR #7](https://github.com/nshaokiet/ai-ip-description-generator/pull/7) ngày 20/09/2026; implementation commit `d3f7c7d9596b77a39e9a56fcdf97c76cb972612a`, merge commit `d208a7925da844c5b43578bac8ebdbb1c5c6b5b8`. Trạng thái hiện tại: **Completed — Merged via PR #7**.

APP-001 triển khai FastAPI local single-tenant skeleton với `GET /health`, secure `POST /api/documents`, layered validation cho PDF/DOCX, safe structured errors, opaque storage identifiers, local ephemeral cleanup và synthetic offline tests. Không có frontend, OpenAI/model call, database, authentication, production storage hoặc deployment. Gemini 3.1 Pro High review `PASS`: 22 acceptance criteria pass, 0 failed, 0 unverifiable; Security và Scope đều `PASS`; không có blocker hoặc required remediation. Human / Product Owner đã approve và merge [PR #10](https://github.com/nshaokiet/ai-ip-description-generator/pull/10) ngày 20/09/2026; specification merge `1bf957162eba78c069d3ba976af7fe1d174cab30`, implementation head `bd39b9f7bdd9f7a1796d9a405e7998070e124e07`, merge commit `0df4814ff1eb8cd576566ac3dd403131feca3759`. Trạng thái hiện tại: **Completed — Merged via PR #10**.

AI-RUNTIME-001 triển khai internal OpenAI Responses API extraction boundary từ APP-002 envelope tới validated Structured Invention Analysis. Gemini implementation review trả `PASS WITH NON-BLOCKING NOTES`; F-001 `MEDIUM` được sửa tại `5247cbcbe591d8b29917d9982b9066e393901c7e` và targeted re-review `PASS`. Human / Product Owner đã approve và merge [PR #14](https://github.com/nshaokiet/ai-ip-description-generator/pull/14) ngày 21/09/2026 tại merge commit `597f6c7b074eb2c5e445790b8c4f48f336f04da5`. 32/32 acceptance criteria đạt; regression ghi nhận 201 executed, 200 pass, 1 intentional Windows skip. Live provider smoke vẫn `NOT RUN — OPENAI_API_KEY not available`; BLK-003 vẫn mở. Trạng thái hiện tại: **Completed — Merged via PR #14**.
AI-RUNTIME-002 triển khai internal OpenAI Responses API draft generation runtime từ validated Structured Invention Analysis (AI-001) qua deterministic AI-003 Draft Input Envelope tới validated Patent Description Draft JSON. Runtime sử dụng `gpt-5.6-sol`, reasoning high, `store=false`, timeout 240 giây, SDK retries 2 và `max_output_tokens=64000`. Output đi qua provider-schema adaptation, schema-aware normalization, canonical Patent Draft 2020-12 validation và deterministic business/grounding validation. Đợt remediation cuối đã xử lý abstract validation governance contract, F-D12 JSON Pointer `/` handling, F-D13 dead helper removal, F-D14 test target_path precision, sửa test imports từ `httpx2` sang `httpx` và bổ sung các biến môi trường draft cần thiết vào `.env.example`; F-D15 prohibited-substring scanner false-positive risk được giữ lại như non-blocking NOTE. Independent final review kết luận `APPROVED`. Human / Product Owner đã approve và merge [PR #16](https://github.com/nshaokiet/ai-ip-description-generator/pull/16) ngày 22/09/2026 tại merge commit `978516a4f5caa90bbd2189668237c6e028597361` (implementation head `a59ce0219d7039f24fa8c7bd71d4e9829dbbf612`). Automated evidence: backend test suite 240 pass, 2 skip, 1 warning; tests/draft 25 pass. Live provider smoke ghi nhận `NOT RUN — DEFERRED due to unavailable API funding`; BLK-003 vẫn mở. Trạng thái hiện tại: **Completed — Merged via PR #16**.

APP-003 hoàn tất vòng đời đặc tả kỹ thuật Core Pipeline Orchestration and Offline E2E Harness v1.2.0. Trải qua các vòng review độc lập bởi Gemini 3.1 Pro High (initial REQUEST CHANGES → remediation v1.1.0 PASS → final hardening v1.2.0 cho H-001/H-002/H-003 PASS), Human / Product Owner đã chính thức phê duyệt Specification v1.2.0 và merge PR #18 ngày 22/09/2026 tại merge commit `bfbcdc760916f497b603bcd49ce0150d6819d337`. REV-APP-003 đã CLOSED. Trạng thái đặc tả: **Specification — Approved & Merged**. Sau mốc đặc tả, APP-003 implementation `3e7c2910695eed9e5ef1d7d0ff11f8f0e3ac6c38` đã merge tại `b5a47f6030441b438e7e1745b75b05d8b345d6c0`: **Completed — Merged**. Thông điệp merge ghi 32/32 AC verified và independent Antigravity `PASS`; exact underlying reviewer model/profile và primary review report không được chứng minh bởi bằng chứng hiện có. GOV-P0-006-01 RESOLVED; BLK-003 vẫn OPEN. Không có bằng chứng live-provider validation hoặc production readiness.
