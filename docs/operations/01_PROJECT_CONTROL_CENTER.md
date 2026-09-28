# AI IP Generator – Project Control Center

> Bản nguồn Markdown được quản lý trong Git. Tên Google Doc đích: `01_PROJECT_CONTROL_CENTER`. Trạng thái đồng bộ Google Drive: `[CẦN XÁC NHẬN TRẠNG THÁI]`.

## 1. Document Metadata

| Thuộc tính | Giá trị |
|---|---|
| Document ID | OPS-001 |
| Document title | AI IP Generator – Project Control Center |
| Version | 0.3.25 |
| Status | Active — approved specification baseline |
| Owner | Human / Product Owner |
| Author | ChatGPT/Codex |
| Reviewer | Gemini 3.1 Pro High |
| Created date | 18/09/2026 |
| Last updated | 28/09/2026 GMT+7 |
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
| 0.3.3 | 0.3.4 | 21/09/2026 | ChatGPT/Codex | Chuyển AI-RUNTIME-001 sang Completed, đóng REV-AI-RUNTIME-001 sau remediation, targeted PASS và Human merge PR #14 | Post-merge governance closeout | AI-RUNTIME-001, REV-AI-RUNTIME-001, PR #14, merge commit `597f6c7b074eb2c5e445790b8c4f48f336f04da5` | No |
| 0.3.4 | 0.3.5 | 22/09/2026 | Gemini 3.8 Flash High | Chuyển AI-RUNTIME-002 sang Completed, đóng REV-AI-RUNTIME-002 sau remediation, independent review APPROVED và Human merge PR #16 | Post-merge governance closeout | AI-RUNTIME-002, REV-AI-RUNTIME-002, PR #16, merge commit `978516a4f5caa90bbd2189668237c6e028597361` | No |
| 0.3.5 | 0.3.6 | 22/09/2026 | Gemini 3.8 Flash High | Ghi nhận hoàn tất đặc tả kỹ thuật APP-003 Core Pipeline Orchestration v1.0.0, chờ independent review | Đặc tả kỹ thuật nội bộ trước implementation | APP-003, `docs/tasks/APP-003-core-pipeline-orchestration.md` | No |
| 0.3.6 | 0.3.7 | 22/09/2026 | Gemini 3.8 Flash High | Cập nhật APP-003 specification sau independent review (F-001/F-002 remediation: mandatory source cleanup, determinism contract) | Đồng bộ trạng thái remediated chờ re-review | APP-003, REV-APP-003 | No |
| 0.3.7 | 0.3.8 | 22/09/2026 | Gemini 3.8 Flash High | Làm cứng đặc tả APP-003 v1.2.0: xử lý residual findings H-001 (cleanup exception safety helper), H-002 (Python 3.12 portable regression), H-003 (AC-29 framework routes) | Đồng bộ trạng thái hardened trước targeted re-review | APP-003, H-001, H-002, H-003 | No |
| 0.3.8 | 0.3.9 | 22/09/2026 | Gemini 3.8 Flash High | Đóng vòng đời đặc tả APP-003: Human duyệt v1.2.0, merge PR #18 tại bfbcdc7, đóng REV-APP-003, implementation chưa bắt đầu (deferred đến 26/09/2026) | Post-merge specification governance closeout; không đổi technical contract | APP-003, REV-APP-003, PR #18, merge commit `bfbcdc760916f497b603bcd49ce0150d6819d337` | No |
| 0.3.9 | 0.3.10 | 26/09/2026 | Codex | Chuyển P0-005 Frontend MVP sang `CLOSED` theo Human closeout instruction sau independent review `ACCEPT`; final accepted SHA `43907213f14c8c55294f55af34afcc0cbcc9dc66`; không có release-blocking finding | Governance closeout trên feature branch; không merge `main` | P0-005 | No |
| 0.3.10 | 0.3.11 | 27/09/2026 | Codex | Ghi P0-006 specification 0.1.0 chờ independent review và GOV-P0-006-01 về APP-003 status cũ mâu thuẫn với merged implementation | Current-state audit; không đổi APP-003 status hoặc bắt đầu P0-006 implementation | P0-006, GOV-P0-006-01 | No |
| 0.3.11 | 0.3.12 | 27/09/2026 | Codex | Ghi review P0-006 v0.1.0 `PASS WITH HUMAN DECISIONS REQUIRED`, findings `NONE`, Gemini 3.8 Flash High; Human duyệt HD-P0-006-01…07; nâng specification lên v0.2.0 chờ targeted re-review | Human decision gate RESOLVED; implementation chưa bắt đầu hoặc được phê duyệt | P0-006, HD-P0-006-01…07 | No |
| 0.3.12 | 0.3.13 | 27/09/2026 | Codex | Ghi targeted specification review `PASS`, Human approval và P0-006 implementation/test evidence trên feature branch; chuyển sang chờ independent implementation review | Handoff implementation, không đóng task hoặc merge | P0-006, DEC-009; `8af6e499f22ecace4181f9422de525176c39aaf7` | No |
| 0.3.13 | 0.3.14 | 27/09/2026 | Codex | Đóng P0-006 sau independent implementation review PASS, Human acceptance và merge vào main; giữ BLK-003/GOV-P0-006-01 OPEN | Post-merge governance closeout, không sửa code | P0-006, REV-P0-006-IMPLEMENTATION, DEC-010, merge `3207479e5cca73da3e7facbc7c482d2ce5eba2b9` | No |
| 0.3.14 | 0.3.15 | 27/09/2026 | Codex | Đối chiếu Git, chuyển APP-003 implementation sang Completed — Merged và đóng GOV-P0-006-01; BLK-003 vẫn OPEN | Sửa trạng thái governance lỗi thời, không đổi technical scope/code/test | APP-003, GOV-P0-006-01, implementation `3e7c2910695eed9e5ef1d7d0ff11f8f0e3ac6c38`, merge `b5a47f6030441b438e7e1745b75b05d8b345d6c0` | No |
| 0.3.15 | 0.3.16 | 27/09/2026 | Codex | Register draft P0-007 MVP E2E validation/stabilization specification v0.1.0 for independent review; governance reconciliation branch already merged | Define next validation task without implementation, product-scope or release change | P0-007; main `403deba9d33d1cc20c3d231bc08fa473420505ed`; BLK-003 OPEN | No |
| 0.3.16 | 0.3.17 | 27/09/2026 | Codex | Record P0-007 specification PASS and Human implementation approval; hand off synthetic/offline implementation and AC-01…AC-16 self-check for independent implementation review | Evidence-only lifecycle update; no product/release approval | P0-007, REV-P0-007-SPECIFICATION, implementation `2638c620a36e6fb4016ed2efaeb788446a5b2eff`; BLK-003 OPEN | No |
| 0.3.17 | 0.3.18 | 27/09/2026 | Codex | Close P0-007 after independent implementation PASS, Human review acceptance/merge approval and main merge; preserve BLK-003 and deferred live smoke | Post-merge governance closeout; no code, tests or release change | P0-007, REV-P0-007-IMPLEMENTATION, DEC-012, merge `26b12450284b9331f79fbbffe3220d93e40c0916` | No |
| 0.3.18 | 0.3.19 | 28/09/2026 | Codex | Register P0-008 local/synthetic release/handover readiness specification v0.1.0 for independent review; replace obsolete P0-007 closeout next action | Targeted documentation/readiness audit only; P0-007 closeout now on main, BLK-003 still open | P0-008; baseline `8142692c6e92670b4b09996d733f93c409e93e49` | No |
| 0.3.19 | 0.3.20 | 28/09/2026 | Codex | Record P0-008 specification review PASS/Human implementation approval, fresh local/synthetic implementation evidence and pending implementation review; preserve MCP exception | Handoff without granting handover/production classification | P0-008, REV-P0-008-SPECIFICATION; spec `52d3c62d3741e9e7abc98c2bf2b300b4885f316c`; BLK-003 OPEN | No |
| 0.3.20 | 0.3.21 | 28/09/2026 | Codex | Close P0-008 after independent implementation PASS, Human local/synthetic handover acceptance and merge; retain MCP exception and BLK-003 | Post-merge current-state reconciliation only, no production approval | P0-008, REV-P0-008-IMPLEMENTATION, DEC-014, merge `e6b2f665f6334047ec420c49d2097732f2917354` | No |
| 0.3.21 | 0.3.22 | 28/09/2026 | Codex | Record Human-approved P0-009 offline CI implementation and narrow Playwright interpreter portability decision; hand off for independent review | Current-state traceability, not review or merge approval | P0-009, DEC-015; baseline `bf837ef10622160fc76f80227e23f81830d69f76` | No |
| 0.3.22 | 0.3.23 | 28/09/2026 | Codex | Close P0-009 after two-stage Gemini review, Human-approved PR #28 merge and successful PR/main CI | Post-merge governance closeout; offline regression only | P0-009, REV-P0-009-IMPLEMENTATION, DEC-016, merge `1f1754607152053ed4788f7fd5208c782432a320`; BLK-003 OPEN | No |
| 0.3.23 | 0.3.24 | 28/09/2026 | Codex | Record EVAL-001 spec review/Human framework-only decisions and candidate corpus/scorer handoff without product-runtime acceptance | Prevent stale PLANNED/implementation-not-approved state while retaining provider/production blocks | EVAL-001, REV-EVAL-001-SPECIFICATION, DEC-017; spec `67c8d71f79712ede8780babf890a79fcbfd2769e` | No |
| 0.3.24 | 0.3.25 | 28/09/2026 | Codex | Record successful EVAL-001 Draft PR #29 CI on fixed framework implementation SHA; independent framework review remains pending | Post-CI handoff evidence without product-runtime semantic claim | EVAL-001, PR #29, CI `36404294487`, framework `b8a7ede8f18ca50dedd669fcd47365dd8ed250bc` | No |

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

Trạng thái hiện hành: specification/architecture baseline đã được phê duyệt; implementation đã tiến vào các task thuộc Phase 2/Phase 3.

Human / Product Owner chưa tuyên bố toàn bộ Phase 1, Phase 2, Phase 3 hoặc MVP `Completed`; chỉ các task có evidence riêng được đánh dấu `Completed`.

## 6. Current Objective

- Preserve the Human-accepted **MVP HANDOVER READY — LOCAL/SYNTHETIC** baseline
  and the completed P0-009 offline CI Foundation. CI is active for
  `pull_request(main)` and `push(main)`; EVAL-001 specification v0.1.0 has
  passed independent review and Human approved its framework phase only.
- Preserve Claims outside MVP, BLK-003 OPEN, live-provider smoke deferred, and
  no production/public deployment or real/confidential-data approval.
- Keep production, public deployment and real/confidential-data approval
  separate from this limited handover classification.

SPEC-001/002/003, schema, prompts and DOCX template retain their previously
approved versions/contracts; this task does not re-approve or redesign them.

## 7. Overall Progress

- [x] Khởi tạo local Git repository.
- [x] Xác minh GitHub repository và Private visibility.
- [x] Publish bộ 5 artefact cùng README lên nhánh `main` trong commit đồng bộ này.
- [x] SPEC-001 `docs/system-specification.md` 0.3.0 — Approved baseline.
- [x] SPEC-003 `AGENTS.md` 0.2.0 — Approved baseline.
- [x] SPEC-002 `PROJECT_CONTEXT.md` 0.3.0 — Approved baseline.
- [x] Project Control Center 0.3.5 và Gemini Review Log 0.3.4 được cập nhật cho AI-RUNTIME-002 post-merge closeout.
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
- [x] AI-RUNTIME-001 internal Responses API extraction đã `Completed — Merged via PR #14`; implementation review `PASS WITH NON-BLOCKING NOTES`, F-001 `MEDIUM` resolved và targeted remediation re-review `PASS`.
- [x] AI-RUNTIME-002 internal Responses API draft generation runtime đã `Completed — Merged via PR #16`; implementation head `a59ce0219d7039f24fa8c7bd71d4e9829dbbf612`, merge commit `978516a4f5caa90bbd2189668237c6e028597361`; backend suite 240 pass, 2 skip, 1 warning; tests/draft 25 pass; independent final review APPROVED; live provider smoke NOT RUN — DEFERRED due to unavailable API funding.
- [x] P0-005 Frontend MVP `CLOSED`; final accepted SHA `43907213f14c8c55294f55af34afcc0cbcc9dc66`; independent review `ACCEPT`; logo asset, desktop visual, narrow visual, `npm run lint`, `npm run build`, `git diff --check` và remediation scope `PASS`; release-blocking findings `NONE`.
- [x] P0-006 Frontend/backend integration **CLOSED / Completed — Merged**; accepted implementation SHA `0f1e94db438869a980db8a1cb1e06956de2d8d3e`, merge `3207479e5cca73da3e7facbc7c482d2ce5eba2b9`; Google Antigravity (Advanced Agentic Coding) independent review `PASS`, AC-01…AC-17 `PASS`, findings `NONE`; Human accepted review and approved merge.
- [x] P0-007 specification v0.1.0 at `f98cf600f47a6559175c10dc3498846a7ae4395b` received independent specification `PASS` (AC-01…AC-16, findings NONE, no Human decisions required); Human approved implementation. Historical test/harness handoff was ready for implementation review at final test-code SHA `2638c620a36e6fb4016ed2efaeb788446a5b2eff`. Independent implementation review subsequently `PASS` at accepted implementation/handoff SHA `bd43a7e9875537c4f5ebdee53626542a11500636`, AC-01…AC-16 `PASS`, findings `NONE`; Human accepted and approved merge `26b12450284b9331f79fbbffe3220d93e40c0916`. Current state **CLOSED / COMPLETED — MERGED**; BLK-003 OPEN.
- [x] P0-007 post-merge closeout fast-forwarded into `main` at `8142692c6e92670b4b09996d733f93c409e93e49`; implementation review CLOSED. No production-readiness or MVP-release approval.
- [x] P0-008 specification v0.1.0 at `52d3c62d3741e9e7abc98c2bf2b300b4885f316c` received Google Antigravity (Advanced Agentic Coding) specification review PASS; reviewed implementation `956ba93048536d2a54d120752ade5540ecc0d901` received Google Antigravity / Gemini 1.5 Pro (Advanced Agentic Coding) independent implementation PASS, findings NONE; Human completed AC-16, accepted local/synthetic handover and approved merge `e6b2f665f6334047ec420c49d2097732f2917354`. **CLOSED / COMPLETED — MERGED; MVP HANDOVER READY — LOCAL/SYNTHETIC** only.
- [x] Chạy core pipeline end-to-end **offline/synthetic** cho PDF/DOCX: APP-003 backend regression và P0-007 browser validation evidence; không phải live-provider hoặc production run.
- [x] P0-009 CI Foundation **CLOSED / COMPLETED — MERGED** via PR #28 at `1f1754607152053ed4788f7fd5208c782432a320`; original `8979c72145d95f4f539b40e9e59b2d8af2f59fab`, accepted remediation `ce9f723e143671d4917bf0bf5885772af3b00f7b`; Gemini 3.1 Pro High initial PASS WITH NON-BLOCKING NOTES, targeted PASS/F-01 RESOLVED, findings NONE remaining; Human approved merge; PR CI `36396184226` and main CI `36397653688` SUCCESS. Offline/synthetic only; BLK-003 OPEN.
- [x] EVAL-001 specification v0.1.0 at `67c8d71f79712ede8780babf890a79fcbfd2769e`: Gemini 3.1 Pro High `PASS WITH HUMAN DECISIONS REQUIRED`, AC-01…AC-18 PASS, findings NONE; Human approved seven decisions and framework-only implementation. Six local-only public/open-access candidate papers, six incomplete `PENDING_HUMAN` draft gold files, deterministic scorer and blocked-state report prepared; targeted evaluator 26 passed, full offline pytest 406 passed/3 skipped. Draft PR #29 CI `36404294487` SUCCESS at framework SHA `b8a7ede8f18ca50dedd669fcd47365dd8ed250bc` (Linux backend 407 passed/2 skipped, lint/build PASS, Playwright 11 passed). Independent framework implementation review pending; product-runtime evidence blocked, provider budget 0.
- [ ] EVAL-001 semantic evaluation, production security/BLK-003 and any separately approved deployment; P0-008 local/synthetic handover is accepted, not production readiness.

Các ô `[x]` chỉ xác nhận bằng chứng được nêu ngay trên từng dòng; không suy rộng thành Human/Gemini approval cho các artefact hoặc phase khác.

## 8. Completed

AI-001, AI-002, AI-003, DOC-001, APP-001, APP-002, AI-RUNTIME-001, AI-RUNTIME-002, APP-003, P0-005, P0-006, P0-007 và P0-008 có bằng chứng `Completed`/`CLOSED` tương ứng. APP-003 được xác nhận qua Git merge và thông điệp merge; không suy diễn thêm Human approval chưa có bằng chứng. SPEC-001/002/003 là approved baseline; P0-008 chỉ cấp classification local/synthetic, không tuyên bố production-ready hoặc mọi phase `Completed`.

Các deliverable Draft đã tạo, có bằng chứng file:

| Task ID | Deliverable | Evidence | Kết luận được phép |
|---|---|---|---|
| SPEC-001 | System Specification 0.3.7 | Approved baseline; factual local implementation status updated without changing requirements | Approved baseline |
| SPEC-002 | Project Context 0.4.12 | Approved baseline; EVAL-001 framework handoff recorded without semantic acceptance | Approved baseline |
| SPEC-003 | AI Collaboration Rules 0.3.1 | Approved baseline; factual project-status sentence updated, rules unchanged | Approved baseline |
| SPEC-004 | Project Control Center source 0.3.25 | File hiện tại | Active; Google Doc sync pending confirmation |
| REVIEW-001 | Gemini Review Log source 0.3.13 | `REV-EVAL-001-SPECIFICATION` CLOSED after Human decisions; framework implementation review pending; prior history preserved | Active log |
| AI-001 | Output Schema v1.0.0 | PR [#1](https://github.com/nshaokiet/ai-ip-description-generator/pull/1), merge commit `49efead593437dfc5c88397ea6f335a2d4ff84d7`, 19/09/2026; Gemini review PASS; 15/15 tests pass; không có finding | Completed — Merged via PR #1 |
| AI-002 | Extraction Prompt v1.0.0 | PR [#3](https://github.com/nshaokiet/ai-ip-description-generator/pull/3), merge commit `8f2b7082881961cc1a2cf7fa56ece81976759c7f`, 19/09/2026; implementation `f8772b228a23bf7cdec10fa0c463e6d1f672c341`; governance `9f2a78b1396cdadb747c263a2bbbbacb8d7f4292`; Gemini review PASS; AI-001 15/15 và AI-002 17/17 tests pass; không có finding | Completed — Merged via PR #3 |
| AI-003 | Patent Draft Generation Contract v1.0.0 | PR [#5](https://github.com/nshaokiet/ai-ip-description-generator/pull/5), implementation `ae7e8fb573ea4681a9db1bafa711d19a3c598666`, merge commit `fb522bc5ecbb5ad66bab6226fa88ae51020cef52`, 20/09/2026; Gemini reviews PASS; 57/57 tests pass; không có finding hoặc required change | Completed — Merged via PR #5 |
| DOC-001 | Patent DOCX Template v1.0.0 | PR [#7](https://github.com/nshaokiet/ai-ip-description-generator/pull/7), implementation `d3f7c7d9596b77a39e9a56fcdf97c76cb972612a`, merge commit `d208a7925da844c5b43578bac8ebdbb1c5c6b5b8`, 20/09/2026; Human Visual QA và Gemini reviews PASS; 85/85 tests pass; không có finding hoặc required change | Completed — Merged via PR #7 |
| APP-001 | FastAPI Backend Skeleton and Secure Document Upload | Specification PR [#9](https://github.com/nshaokiet/ai-ip-description-generator/pull/9), merge `1bf957162eba78c069d3ba976af7fe1d174cab30`; implementation PR [#10](https://github.com/nshaokiet/ai-ip-description-generator/pull/10), head `bd39b9f7bdd9f7a1796d9a405e7998070e124e07`, merge `0df4814ff1eb8cd576566ac3dd403131feca3759`, 20/09/2026; Gemini PASS, 22/22 AC, Security/Scope PASS, 109/109 tests | Completed — Merged via PR #10 |
| APP-002 | Document Parsing & Evidence Source Units | PR [#12](https://github.com/nshaokiet/ai-ip-description-generator/pull/12), initial implementation `477b8fda6afbae0049d8d691c213dc6355ba67da`, remediation `8b6f909a0f5787d72c002e163395656a666c9b78`, merge `4a001d116cbf002bdd42a9151efbf3f308fce3e6`, 21/09/2026; initial Gemini `REQUEST CHANGES`, F-001/F-002 resolved, targeted `PASS`; 30/30 AC; 135 executed, 134 pass, 1 skip, 0 failure/error | Completed — Merged via PR #12 |
| AI-RUNTIME-001 | OpenAI Responses API + Structured Outputs Extraction Runtime | PR [#14](https://github.com/nshaokiet/ai-ip-description-generator/pull/14), initial implementation `e430584a0cc31d0ccc821eb2d21ad7a14548329a`, remediation `5247cbcbe591d8b29917d9982b9066e393901c7e`, merge `597f6c7b074eb2c5e445790b8c4f48f336f04da5`, 21/09/2026; Gemini implementation `PASS WITH NON-BLOCKING NOTES`, F-001 `MEDIUM` resolved, targeted remediation `PASS`; 32/32 AC; 201 executed, 200 pass, 1 skip | Completed — Merged via PR #14 |
| AI-RUNTIME-002 | OpenAI Responses API + Patent Draft Generation Runtime | PR [#16](https://github.com/nshaokiet/ai-ip-description-generator/pull/16), implementation head `a59ce0219d7039f24fa8c7bd71d4e9829dbbf612`, merge commit `978516a4f5caa90bbd2189668237c6e028597361`, 22/09/2026; independent review APPROVED; backend suite 240 pass, 2 skip, 1 warning; tests/draft 25 pass; live provider smoke NOT RUN — DEFERRED due to unavailable API funding | Completed — Merged via PR #16 |
| APP-003 | Internal Core Pipeline Orchestration and Offline E2E Harness | Specification v1.2.0 merged at `bfbcdc760916f497b603bcd49ce0150d6819d337`; implementation `3e7c2910695eed9e5ef1d7d0ff11f8f0e3ac6c38` merged at `b5a47f6030441b438e7e1745b75b05d8b345d6c0`; merge message records 32/32 AC verified and independent Antigravity `PASS`; exact underlying reviewer model/profile not evidenced | Completed — Merged; internal/synthetic-only, not production-ready |
| P0-005 | Frontend MVP | Final accepted SHA `43907213f14c8c55294f55af34afcc0cbcc9dc66`; independent review `ACCEPT`; logo asset, desktop visual, narrow visual, `npm run lint`, `npm run build`, `git diff --check` và remediation scope `PASS`; release-blocking findings `NONE` | CLOSED |
| P0-006 | Frontend/backend integration | Accepted implementation `0f1e94db438869a980db8a1cb1e06956de2d8d3e`; merge `3207479e5cca73da3e7facbc7c482d2ce5eba2b9`; independent Google Antigravity (Advanced Agentic Coding) `PASS`, AC-01…AC-17 `PASS`, findings `NONE`; targeted backend 17 pass, frontend lint/build PASS, Playwright 6 pass; Human accepted and approved merge | CLOSED / Completed — Merged |
| P0-007 | MVP End-to-End Validation & Stabilization | Approved spec v0.1.0 `f98cf600f47a6559175c10dc3498846a7ae4395b`; accepted implementation/handoff `bd43a7e9875537c4f5ebdee53626542a11500636`, final test-code `2638c620a36e6fb4016ed2efaeb788446a5b2eff`, merge `26b12450284b9331f79fbbffe3220d93e40c0916`; independent Google Antigravity (Advanced Agentic Coding) `PASS`, AC-01…AC-16 `PASS`, findings `NONE`; Human accepted review and approved merge; BLK-003 OPEN | CLOSED / COMPLETED — MERGED; synthetic/offline only, not production-ready |
| P0-008 | MVP Release & Handover Readiness | Approved spec v0.1.0 `52d3c62d3741e9e7abc98c2bf2b300b4885f316c`; reviewed implementation `956ba93048536d2a54d120752ade5540ecc0d901`, merge `e6b2f665f6334047ec420c49d2097732f2917354`; independent Google Antigravity / Gemini 1.5 Pro (Advanced Agentic Coding) PASS, findings NONE, AC-01…AC-16 PASS after Human AC-16 acceptance; BLK-003 OPEN | CLOSED / COMPLETED — MERGED; MVP HANDOVER READY — LOCAL/SYNTHETIC only |
| P0-009 | CI Foundation | Baseline `bf837ef10622160fc76f80227e23f81830d69f76`; original `8979c72145d95f4f539b40e9e59b2d8af2f59fab`; final accepted `ce9f723e143671d4917bf0bf5885772af3b00f7b`; PR #28 merge `1f1754607152053ed4788f7fd5208c782432a320`; Gemini 3.1 Pro High targeted PASS, F-01 RESOLVED, findings NONE remaining; Human merge approval GRANTED; PR CI `36396184226` and main CI `36397653688` SUCCESS | CLOSED / COMPLETED — MERGED; CI ACTIVE for offline regression only; BLK-003 OPEN |

APP-002 capability boundary: `Validated PDF/DOCX → deterministic text/table parsing → safe metadata registry + SHA-256 integrity verification → source units → evidence IDs/source locators → AI-002 Extraction Input Envelope`. AI-RUNTIME-001 tiếp nối bằng internal Responses API, provider schema, normalization và canonical/grounding validation tới validated analysis. AI-RUNTIME-002 tiếp nối bằng internal Responses API draft runtime từ validated analysis qua deterministic AI-003 envelope, provider adaptation, normalization, canonical draft validation và deterministic business/grounding validation tới validated Patent Description Draft JSON. Các task sau đó đã merge local orchestration/API, DOCX integration và P0-006 frontend; không suy rộng thành production auth/storage/deployment. Live provider smoke ghi nhận NOT RUN — DEFERRED due to unavailable API funding (bắt buộc chạy trước production deployment). BLK-003 vẫn OPEN; APP-003 governance reconciliation GOV-P0-006-01 đã RESOLVED.

## 9. In Progress

| Task ID | Công việc | Owner | Reviewer | Status | Evidence/Blocker |
|---|---|---|---|---|---|
| SPEC-004 | Đồng bộ Project Control Center sang Google Docs | Human / Product Owner | ChatGPT/Codex | `[CẦN XÁC NHẬN TRẠNG THÁI]` | Chưa có bằng chứng Google Doc/link |

## 10. Next Tasks

| Task ID | Task | Owner | Reviewer | Priority | Status | Dependency | Target date |
|---|---|---|---|---|---|---|---|
| EVAL-001 | Semantic Quality Evaluation — framework phase | GPT-6 Sol | Gemini 3.1 Pro High | Human-approved framework only | IMPLEMENTING — independent framework review pending; BLOCKED FOR PRODUCT-RUNTIME EVIDENCE | Frozen product baseline `37d42fc8b07003aa2a67f2d1d32e64e69eb0ddb5`; approved spec `67c8d71f79712ede8780babf890a79fcbfd2769e`; provider access not authorized | To be set by Human |

Mọi target date cụ thể cần được xếp trước deadline chung 02/10/2026 và do Human xác nhận.

GOV-P0-006-01 — RESOLVED: APP-003 implementation `3e7c2910695eed9e5ef1d7d0ff11f8f0e3ac6c38` đã merge vào `main` tại `b5a47f6030441b438e7e1745b75b05d8b345d6c0`; thông điệp merge ghi 32/32 AC verified và independent Antigravity `PASS`. Exact underlying reviewer model/profile và primary review report không được cung cấp. P0-003 DOCX integration merge `5cfb1b5d0377fcb4538a2bba0bbb48232001b123`; P0-004 local HTTP API merge `43737a79fcdb634a12a92752c767df9fbf98d1f3`. Reconciliation này sửa trạng thái lỗi thời được P0-006 audit nêu, không đổi APP-003 technical requirements hoặc P0-006 lifecycle. BLK-003 vẫn OPEN; không suy diễn production readiness/live-provider validation.

P0-006 specification review: v0.1.0 tại `9115c14e929a1f9796fd4622d0f0fddba84e58f1` được Gemini 3.8 Flash High đánh giá `PASS WITH HUMAN DECISIONS REQUIRED`, findings `NONE`. Human / Product Owner đã APPROVE HD-P0-006-01 đến HD-P0-006-07; Human Decision Gate `RESOLVED`. Specification v0.2.0 tại `5dfbbca9b66367a7930bd3892b8a0ea883781f31` nhận targeted re-review `PASS`, findings `NONE`, sau đó Human phê duyệt implementation. Independent implementation review của Google Antigravity (Advanced Agentic Coding) tại `0f1e94db438869a980db8a1cb1e06956de2d8d3e`: `PASS`, AC-01…AC-17 `PASS`, findings `NONE`; Human accepted review và approved merge tại `3207479e5cca73da3e7facbc7c482d2ce5eba2b9`. Underlying Gemini model/profile không được cung cấp.

## 11. Current Blockers

| Blocker ID | Blocker | Ảnh hưởng | Owner quyết định | Status |
|---|---|---|---|---|
| BLK-003 | Chưa chốt auth/private production storage/retention | Không được dùng dữ liệu nghiên cứu thật hoặc coi runtime là production-ready; live smoke nếu chạy chỉ được dùng synthetic data | Human / Product Owner | Open — production/real-data blocker |
| BLK-004 | Chưa chốt model, retrieval, retry, timeout, cost | Extraction Runtime v1 và Draft Runtime v1 đã khóa; task tương lai không được suy rộng | Human / Product Owner | Resolved for Extraction Runtime v1 (AI-RUNTIME-001) and Draft Runtime v1 (AI-RUNTIME-002) |
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
| ADR-010 | 21/09/2026 | OpenAI Responses API extraction với `gpt-5.6-sol`, provider adapter, canonical/grounding post-validation và `store=false` | Tạo internal fail-closed boundary mà không đổi AI-001/AI-002 | Raw canonical schema; provider schema copy; repair call; retrieval | Human / Product Owner | ACCEPTED — IMPLEMENTED — MERGED VIA PR #14 | `docs/decisions/ADR-010-openai-extraction-runtime-v1.md` |

ADR-001 đến ADR-010 đã được Human phê duyệt trong phạm vi từng decision record. `Accepted` không tự động cho phép implementation ngoài task được duyệt.

## 13. Current AI Assignments

| Task ID | Task | Owner | Reviewer | Status | Expected output |
|---|---|---|---|---|---|
| SPEC-001 | System Specification | ChatGPT/Codex | Gemini Pro + Human | Approved baseline | `docs/system-specification.md` 0.3.7; REV-001 CLOSED; factual status corrected |
| SPEC-002 | Project Context | ChatGPT/Codex | Gemini Pro + Human | Approved baseline | `PROJECT_CONTEXT.md` 0.4.10; REV-003 CLOSED |
| SPEC-003 | AGENTS.md | ChatGPT/Codex | Gemini Pro + Human | Approved baseline | `AGENTS.md` 0.3.1; REV-002 CLOSED; roles unchanged |
| SPEC-004 | Control Center source | ChatGPT/Codex | Human | Active | File hiện tại 0.3.23 |
| REVIEW-001 | Review Log | ChatGPT/Codex | Independent reviewers + Human | Active | `02_GEMINI_REVIEW_LOG.md` 0.3.12; REV-P0-009-IMPLEMENTATION CLOSED; historical review stages preserved |
| APP-001 | FastAPI Backend Skeleton and Secure Document Upload | ChatGPT/Codex | Gemini 3.1 Pro High + Human | Completed — Merged via PR #10 | Implementation head `bd39b9f7bdd9f7a1796d9a405e7998070e124e07`; merge `0df4814ff1eb8cd576566ac3dd403131feca3759`; 109/109 tests pass |
| APP-002 | Document Parsing & Evidence Source Units | ChatGPT/Codex | Gemini 3.1 Pro High + Human | Completed — Merged via PR #12 | Initial `477b8fda6afbae0049d8d691c213dc6355ba67da`; remediation `8b6f909a0f5787d72c002e163395656a666c9b78`; merge `4a001d116cbf002bdd42a9151efbf3f308fce3e6`; 30/30 AC; final Gemini PASS; 135 executed, 134 pass, 1 skip |
| AI-RUNTIME-001 | OpenAI Responses API + Structured Outputs Extraction Runtime | ChatGPT/Codex | Gemini 3.1 Pro High + Human | Completed — Merged via PR #14 | Initial `e430584a0cc31d0ccc821eb2d21ad7a14548329a`; remediation `5247cbcbe591d8b29917d9982b9066e393901c7e`; merge `597f6c7b074eb2c5e445790b8c4f48f336f04da5`; 32/32 AC; 201 executed, 200 pass, 1 skip; live smoke not run |
| AI-RUNTIME-002 | OpenAI Responses API + Patent Draft Generation Runtime | ChatGPT/Codex | Gemini 3.8 Flash High / Gemini 3.1 Pro High + Human | Completed — Merged via PR #16 | Implementation head `a59ce0219d7039f24fa8c7bd71d4e9829dbbf612`; merge commit `978516a4f5caa90bbd2189668237c6e028597361`; 240 backend pass, 2 skip, 1 warning; tests/draft 25 pass; live smoke deferred |
| APP-003 | Core Pipeline Orchestration & Offline E2E Harness | Codex implementation; specification owner ChatGPT/Codex | Specification: Gemini 3.1 Pro High + Human; implementation: Antigravity per merge message, exact underlying model/profile not evidenced | Completed — Merged | Specification v1.2.0 merge `bfbcdc760916f497b603bcd49ce0150d6819d337`; implementation `3e7c2910695eed9e5ef1d7d0ff11f8f0e3ac6c38`; implementation merge `b5a47f6030441b438e7e1745b75b05d8b345d6c0`; merge message: 32/32 AC, independent Antigravity PASS; BLK-003 OPEN |
| P0-005 | Frontend MVP | Codex | Independent review `ACCEPT`; exact reviewer profile not supplied in closeout instruction | CLOSED | Final accepted SHA `43907213f14c8c55294f55af34afcc0cbcc9dc66`; release-blocking findings `NONE` |
| P0-006 | Frontend/backend integration | Codex | Google Antigravity (Advanced Agentic Coding); underlying Gemini model/profile not evidenced | CLOSED / Completed — Merged | Accepted implementation `0f1e94db438869a980db8a1cb1e06956de2d8d3e`; merge `3207479e5cca73da3e7facbc7c482d2ce5eba2b9`; independent PASS, AC-01…AC-17 PASS, findings NONE; targeted backend 17 pass, frontend lint/build PASS, Playwright 6 pass; Human accepted/approved merge; BLK-003 remains OPEN; GOV-P0-006-01 resolved separately |
| P0-007 | MVP End-to-End Validation & Stabilization | Codex | Google Antigravity (Advanced Agentic Coding) implementation reviewer; underlying model not evidenced | CLOSED / COMPLETED — MERGED | Approved spec v0.1.0 `f98cf600f47a6559175c10dc3498846a7ae4395b`; accepted implementation/handoff `bd43a7e9875537c4f5ebdee53626542a11500636`; final test-code `2638c620a36e6fb4016ed2efaeb788446a5b2eff`; merge `26b12450284b9331f79fbbffe3220d93e40c0916`; independent AC-01…AC-16 PASS, findings NONE; lint/build PASS, Playwright 11 passed; historical backend 194 passed/1 skipped targeted and 380 passed/3 skipped full accepted without independent rerun; BLK-003 OPEN; live smoke deferred; no production readiness |
| P0-008 | MVP Release & Handover Readiness | Codex implementation | Specification: Google Antigravity (Advanced Agentic Coding); implementation: Google Antigravity / Gemini 1.5 Pro (Advanced Agentic Coding) | CLOSED / COMPLETED — MERGED; MVP HANDOVER READY — LOCAL/SYNTHETIC | Approved spec v0.1.0 `52d3c62d3741e9e7abc98c2bf2b300b4885f316c`; reviewed implementation `956ba93048536d2a54d120752ade5540ecc0d901`; independent implementation PASS/findings NONE; Human accepted handover and merge `e6b2f665f6334047ec420c49d2097732f2917354`; MCP reconciliation BLOCKED BY TOOL CAPABILITY under Human-approved non-blocking exception; BLK-003 OPEN |
| P0-009 | CI Foundation | GPT-6 Sol implementation role | Gemini 3.1 Pro High | CLOSED / COMPLETED — MERGED; CI ACTIVE | PR #28; baseline `bf837ef10622160fc76f80227e23f81830d69f76`; original `8979c72145d95f4f539b40e9e59b2d8af2f59fab`; accepted `ce9f723e143671d4917bf0bf5885772af3b00f7b`; merge `1f1754607152053ed4788f7fd5208c782432a320`; F-01 RESOLVED/new findings NONE; PR CI `36396184226` and main CI `36397653688` SUCCESS; BLK-003 OPEN |
| AI-001 | Output Schema v1.0.0 | ChatGPT/Codex | Gemini 3.1 Pro | Completed — Merged via PR #1 | Merge commit `49efead593437dfc5c88397ea6f335a2d4ff84d7`; Gemini review PASS; 15/15 tests pass; không có finding |
| AI-002 | Extraction Prompt v1.0.0 | ChatGPT/Codex | Gemini 3.1 Pro High | Completed — Merged via PR #3 | Merge commit `8f2b7082881961cc1a2cf7fa56ece81976759c7f`; implementation `f8772b228a23bf7cdec10fa0c463e6d1f672c341`; governance `9f2a78b1396cdadb747c263a2bbbbacb8d7f4292`; 15/15 regression và 17/17 AI-002 tests pass |
| AI-003 | Patent Draft Generation Contract v1.0.0 | ChatGPT/Codex | Gemini 3.1 Pro High | Completed — Merged via PR #5 | Implementation `ae7e8fb573ea4681a9db1bafa711d19a3c598666`; merge `fb522bc5ecbb5ad66bab6226fa88ae51020cef52`; 57/57 tests pass |
| DOC-001 | Patent DOCX Template v1.0.0 | ChatGPT/Codex | Gemini 3.1 Pro High + Human | Completed — Merged via PR #7 | Implementation `d3f7c7d9596b77a39e9a56fcdf97c76cb972612a`; merge `d208a7925da844c5b43578bac8ebdbb1c5c6b5b8`; Human Visual QA/Gemini reviews PASS; 85/85 tests pass |

## 14. ChatGPT/Codex Handoffs

The current P0-008 implementation handoff is in the evidence addendum of `docs/tasks/P0-008-mvp-release-handover-readiness.md` and the [runbook](MVP_HANDOVER_RUNBOOK.md). P0-007 post-merge closeout/handoff remains in section 16 of its task file; sections 14 and 15 preserve historical pre-review handoffs. The P0-006 and APP-003 handoffs below are historical records; their then-current next actions are superseded. The P0-006 `GOV-P0-006-01 OPEN` statement was true at that closeout, before the separate reconciliation.

```text
Task ID: P0-006
Agent: Codex
Reviewer: Google Antigravity (Advanced Agentic Coding); underlying Gemini model/profile not evidenced
Status: CLOSED / Completed — Merged; governance closeout branch awaiting Human merge
Version: Approved specification v0.2.0; accepted implementation SHA 0f1e94db438869a980db8a1cb1e06956de2d8d3e; implementation merge 3207479e5cca73da3e7facbc7c482d2ce5eba2b9
Work completed: Independent implementation review PASS for AC-01…AC-17, findings NONE; Human accepted review and approved merge to main. This closeout records governance only.
Files affected: docs/operations/02_GEMINI_REVIEW_LOG.md; docs/operations/01_PROJECT_CONTROL_CENTER.md; docs/tasks/P0-006-frontend-backend-integration.md; PROJECT_CONTEXT.md.
Evidence checked: Independent backend targeted 17 pass, frontend lint PASS, build PASS, Playwright 6 pass; reviewer modified no files; merge commit verified on main. No tests rerun for this documentation closeout.
Findings: NONE in independent implementation review.
Decisions: Human / Product Owner accepted the review and approved implementation merge to main.
Issues: BLK-003 OPEN; GOV-P0-006-01 OPEN; underlying Gemini model/profile and exact review date not evidenced.
Security impact: No new production/real-data authorization; local synthetic-only boundary remains.
Recommended next action: HUMAN MERGE CLOSEOUT branch docs/p0-006-post-merge-closeout.
```

Historical APP-003 governance handoff (completed before the P0-007 specification):

```text
Task ID: GOV-P0-006-01 / APP-003
Agent: Codex
Reviewer: Antigravity for APP-003 implementation per merge message; exact underlying model/profile not evidenced
Status: GOV-P0-006-01 RESOLVED; APP-003 Completed — Merged
Version: APP-003 Specification v1.2.0; governance evidence revision 1.2.1; Control Center 0.3.15
Work completed: Reconciled stale APP-003 status from verified implementation and merge commits; preserved P0-006 lifecycle and BLK-003.
Files affected: docs/tasks/APP-003-core-pipeline-orchestration.md; docs/operations/01_PROJECT_CONTROL_CENTER.md; docs/operations/02_GEMINI_REVIEW_LOG.md; PROJECT_CONTEXT.md.
Evidence checked: Implementation 3e7c2910695eed9e5ef1d7d0ff11f8f0e3ac6c38 is in merge b5a47f6030441b438e7e1745b75b05d8b345d6c0 on main; merge message reports 32/32 AC verified and independent Antigravity PASS.
Findings: Primary implementation review report and exact underlying reviewer model/profile not evidenced; no additional findings inferred.
Decisions: Resolve documentation-state discrepancy GOV-P0-006-01 only.
Issues: BLK-003 OPEN; live provider validation not evidenced.
Security impact: No production or real-data approval.
Recommended next action: HUMAN MERGE GOVERNANCE RECONCILIATION.
```

## 15. Latest Gemini Handoff

```text
Task ID: AI-RUNTIME-002
Agent: Gemini 3.8 Flash High
Reviewer: Human / Product Owner
Status: CLOSED — AI-RUNTIME-002 Completed — Merged via PR #16
Version: Implementation head a59ce0219d7039f24fa8c7bd71d4e9829dbbf612; resolved by merge commit 978516a4f5caa90bbd2189668237c6e028597361
Work completed: Checkpoint reviews (A through E) and final remediation review completed with verdict APPROVED; Human approved and merged PR #16.
Files affected: Review only; production artefacts not modified by reviewer.
Evidence checked: 240 backend pass, 2 skip, 1 warning; 25 tests/draft pass; git diff --check PASS.
Findings: Abstract-governance inconsistency plus F-D12/F-D13/F-D14 and test-import/environment notes resolved; F-D15 retained as a documented non-blocking NOTE; final independent review safe for merge.
Decisions: Recommendation APPROVE; Human / Product Owner approved and merged PR #16 on 22/09/2026.
Issues: Live provider smoke NOT RUN — DEFERRED due to unavailable API funding; pre-production live smoke gate preserved; BLK-003 remains open; core end-to-end pipeline not complete.
Security impact: Synthetic-only evidence; store=false; no credentials, PII or confidential paper data logged or committed.
Recommended next action: Post-merge governance closeout; await Human assignment for next milestone.
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
| 21/09/2026 | Governance/documentation closeout | 0.3.4 | Bảo toàn AI-RUNTIME-001 review lifecycle, ghi F-001 remediation, targeted PASS, Human merge PR #14 và đóng REV-AI-RUNTIME-001 | ChatGPT/Codex | AI-RUNTIME-001, REV-AI-RUNTIME-001, PR #14, merge `597f6c7b074eb2c5e445790b8c4f48f336f04da5` |
| 22/09/2026 | `backend/app/services/draft_*.py`, `backend/app/core/config.py`, `tests/draft/` | AI-RUNTIME-002 implementation | Internal OpenAI Responses API patent draft generation runtime merge qua PR #16 | ChatGPT/Codex | AI-RUNTIME-002, PR #16, merge `978516a4f5caa90bbd2189668237c6e028597361` |
| 22/09/2026 | Governance/documentation closeout | 0.3.5 | Ghi nhận AI-RUNTIME-002 post-merge closeout, đóng REV-AI-RUNTIME-002 | Gemini 3.8 Flash High | AI-RUNTIME-002, REV-AI-RUNTIME-002, PR #16 |
| 22/09/2026 | `docs/tasks/APP-003-core-pipeline-orchestration.md` | 1.2.0 | Làm cứng đặc tả APP-003 v1.2.0: helper `_cleanup_source` ngăn chặn mask lỗi, loại bỏ Python 3.14, tinh chỉnh AC-21 và AC-29 | Gemini 3.8 Flash High | APP-003, H-001, H-002, H-003 |
| 22/09/2026 | Governance/documentation closeout | 0.3.9 | Đóng vòng đời đặc tả APP-003 sau re-review PASS, Human phê duyệt v1.2.0, merge PR #18 tại bfbcdc7, đóng REV-APP-003; hoãn implementation đến 26/09/2026 cho Codex | Gemini 3.8 Flash High | APP-003, REV-APP-003, PR #18, merge commit `bfbcdc760916f497b603bcd49ce0150d6819d337` |
| 26/09/2026 | `docs/operations/01_PROJECT_CONTROL_CENTER.md` | 0.3.10 | Ghi P0-005 Frontend MVP `CLOSED` theo final accepted SHA và independent review evidence do Human cung cấp | Codex | P0-005, `43907213f14c8c55294f55af34afcc0cbcc9dc66` |
| 27/09/2026 | `docs/tasks/P0-006-frontend-backend-integration.md`; `docs/operations/01_PROJECT_CONTROL_CENTER.md` | 0.1.0; 0.3.11 | Tạo draft specification/audit P0-006, ghi mâu thuẫn APP-003 governance, chờ independent review và Human decisions | Codex | P0-006, GOV-P0-006-01 |
| 27/09/2026 | `docs/tasks/P0-006-frontend-backend-integration.md`; `docs/operations/01_PROJECT_CONTROL_CENTER.md` | 0.2.0; 0.3.12 | Ghi v0.1.0 independent review của Gemini 3.8 Flash High (PASS WITH HUMAN DECISIONS REQUIRED; findings NONE), bảy Human decisions APPROVED và v0.2.0 chờ targeted re-review | Codex | P0-006, HD-P0-006-01…07 |
| 27/09/2026 | P0-006 implementation and documentation handoff | Specification v0.2.0, evidence revision 0.2.1; Control Center 0.3.13 | Ghi targeted specification PASS, Human implementation approval, code/test SHA và offline regressions; chờ independent implementation review | Codex | P0-006, DEC-009; `8af6e499f22ecace4181f9422de525176c39aaf7` |
| 27/09/2026 | P0-006 post-merge governance closeout | Specification v0.2.0, evidence revision 0.2.2; Control Center 0.3.14; Review Log 0.3.6; Project Context 0.4.1 | Ghi independent review PASS, Human acceptance, implementation merge và CLOSED / Completed; không đổi code/test | Codex | P0-006, REV-P0-006-IMPLEMENTATION, DEC-010; merge `3207479e5cca73da3e7facbc7c482d2ce5eba2b9` |
| 27/09/2026 | APP-003 governance reconciliation | APP-003 specification v1.2.0, evidence revision 1.2.1; Control Center 0.3.15; Review Log 0.3.7; Project Context 0.4.2 | Sửa APP-003 implementation status theo Git merge; đóng GOV-P0-006-01; giữ BLK-003 OPEN và technical requirements nguyên trạng | Codex | APP-003, GOV-P0-006-01; implementation `3e7c2910695eed9e5ef1d7d0ff11f8f0e3ac6c38`, merge `b5a47f6030441b438e7e1745b75b05d8b345d6c0` |
| 27/09/2026 | `docs/tasks/P0-007-mvp-e2e-validation-stabilization.md` | Specification 0.1.0; Control Center 0.3.16; Project Context 0.4.3 | Define next synthetic/offline E2E validation task, reuse existing tests and identify only meaningful integration gaps; await independent specification review | Codex | P0-007; baseline `403deba9d33d1cc20c3d231bc08fa473420505ed`; BLK-003 OPEN |
| 27/09/2026 | P0-007 synthetic/offline implementation handoff | Specification v0.1.0, evidence addendum 0.1.1; Control Center 0.3.17; Review Log 0.3.8; Project Context 0.4.4 | Record spec review PASS/Human implementation approval, test-only changes, backend/frontend/browser/stability results and 16 AC self-checks; await independent implementation review | Codex | P0-007; code `2638c620a36e6fb4016ed2efaeb788446a5b2eff`; BLK-003 OPEN |
| 27/09/2026 | P0-007 post-merge governance closeout | Specification v0.1.0, evidence addendum 0.1.2; Control Center 0.3.18; Review Log 0.3.9; Project Context 0.4.5 | Record independent implementation PASS and Human-approved merge; close P0-007/REV-P0-007-IMPLEMENTATION without code/test or release change | Codex | P0-007; implementation `bd43a7e9875537c4f5ebdee53626542a11500636`; merge `26b12450284b9331f79fbbffe3220d93e40c0916`; BLK-003 OPEN |
| 28/09/2026 | `docs/tasks/P0-008-mvp-release-handover-readiness.md` | Specification v0.1.0; Control Center 0.3.19; Project Context 0.4.6 | Targeted repository audit, stale-current-state inventory, 16 objective AC/trace rows and local/synthetic handover design; await independent specification review, not implementation | Codex | P0-008; base `8142692c6e92670b4b09996d733f93c409e93e49`; BLK-003 OPEN |
| 28/09/2026 | P0-008 documentation/runbook and implementation handoff | Specification v0.1.0, evidence addendum 0.1.1; Control Center 0.3.20; Project Context 0.4.7; Review Log 0.3.10 | Reconcile current local status, record spec PASS/Human implementation approval/MCP exception, fresh isolated verification and pending independent implementation review | Codex | P0-008, REV-P0-008-SPECIFICATION; fresh verification `737edec7a134620285b368a9c57d08aa63829a0a`; BLK-003 OPEN |
| 28/09/2026 | P0-008 post-merge documentation closeout | Task evidence addendum 0.1.2; runbook 0.1.2; Control Center 0.3.21; Context 0.4.8; Review Log 0.3.11 | Record fixed-SHA independent implementation PASS, Human AC-16/handover acceptance and merge; no production approval | Codex | P0-008, REV-P0-008-IMPLEMENTATION, DEC-014; merge `e6b2f665f6334047ec420c49d2097732f2917354`; BLK-003 OPEN |
| 28/09/2026 | `.github/workflows/ci.yml`; `frontend/playwright.config.ts`; `docs/tasks/P0-009-ci-foundation.md` | P0-009 implementation; Control Center 0.3.22; Context 0.4.9 | Add offline CI gates and Human-approved interpreter override; record local evidence and pending independent review | Codex | P0-009, DEC-015; baseline `bf837ef10622160fc76f80227e23f81830d69f76` |
| 28/09/2026 | P0-009 post-merge documentation closeout | Task record 0.1.1; Control Center 0.3.23; Review Log 0.3.12; Context 0.4.10 | Record F-01 remediation/re-review, Human merge approval and successful PR/main CI; close P0-009 without product or release change | Codex | P0-009, REV-P0-009-IMPLEMENTATION, DEC-016; merge `1f1754607152053ed4788f7fd5208c782432a320`; BLK-003 OPEN |

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
| OpenAI extraction runtime | AI-RUNTIME-001 / spec 1.0.0 | Completed — Merged via PR #14; live provider smoke pending | ChatGPT/Codex | Gemini 3.1 Pro High + Human | 21/09/2026 |
| OpenAI draft runtime | AI-RUNTIME-002 / draft runtime v1 | Completed — Merged via PR #16; live provider smoke deferred | ChatGPT/Codex | Gemini 3.8 Flash High / Gemini 3.1 Pro High + Human | 22/09/2026 |

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
| Q-005 | Model/retrieval/retry/timeout/output budget là gì? | AI runtime | Cấu hình được Human phê duyệt | Schema/prompt/runtime tests | 22/09/2026 | Resolved for Extraction Runtime v1 (AI-RUNTIME-001: `gpt-5.6-sol`, timeout 180s, 48.000 tokens) and Draft Runtime v1 (AI-RUNTIME-002: `gpt-5.6-sol`, timeout 240s, 64.000 tokens); no retrieval, `store=false`; future runtimes remain separate |
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
| REV-AI-RUNTIME-001 | OpenAI extraction runtime, adapter, validators, tests and ADR-010 | Initial `e430584a0cc31d0ccc821eb2d21ad7a14548329a`; remediation `5247cbcbe591d8b29917d9982b9066e393901c7e`; resolved by merge `597f6c7b074eb2c5e445790b8c4f48f336f04da5` | Gemini 3.1 Pro High | CLOSED — PASS WITH NON-BLOCKING NOTES; F-001 RESOLVED; targeted PASS; merged via PR #14 | No |
| REV-AI-RUNTIME-002 | OpenAI draft generation runtime, provider schema, normalizer, validators, tests | Implementation head `a59ce0219d7039f24fa8c7bd71d4e9829dbbf612`; resolved by merge `978516a4f5caa90bbd2189668237c6e028597361` | Gemini 3.8 Flash High / Gemini 3.1 Pro High | CLOSED — APPROVED; merged via PR #16 | No |
| REV-APP-003 | `docs/tasks/APP-003-core-pipeline-orchestration.md` | 1.2.0 | Gemini 3.1 Pro High + Human | CLOSED — initial REQUEST CHANGES; remediation completed; independent re-review PASS; final hardening completed; targeted re-review PASS; Human approved Specification v1.2.0; merged via PR #18 | No |
| APP-003-IMPLEMENTATION-EVIDENCE | Core pipeline implementation merge message; not a new primary review record | Implementation `3e7c2910695eed9e5ef1d7d0ff11f8f0e3ac6c38`; merge `b5a47f6030441b438e7e1745b75b05d8b345d6c0` | Antigravity per merge message; exact underlying model/profile not evidenced | Merge message reports 32/32 AC verified and independent review PASS; primary review report not evidenced | No |
| REV-P0-006-IMPLEMENTATION | Frontend/backend integration implementation on `feat/p0-006-frontend-backend-integration` | Reviewed `0f1e94db438869a980db8a1cb1e06956de2d8d3e`; resolved by merge `3207479e5cca73da3e7facbc7c482d2ce5eba2b9` | Google Antigravity (Advanced Agentic Coding); underlying Gemini model/profile not evidenced | CLOSED — PASS; AC-01…AC-17 PASS; findings NONE; Human accepted review and approved merge | No |
| REV-P0-007-SPECIFICATION | P0-007 MVP E2E Validation & Stabilization specification | v0.1.0 at `f98cf600f47a6559175c10dc3498846a7ae4395b` | Google Antigravity (Advanced Agentic Coding); underlying model not evidenced | CLOSED — PASS; specification AC-01…AC-16 PASS; findings NONE; Human approved implementation | No |
| REV-P0-007-IMPLEMENTATION | P0-007 synthetic/offline test/harness implementation | Reviewed `bd43a7e9875537c4f5ebdee53626542a11500636`; final test-code `2638c620a36e6fb4016ed2efaeb788446a5b2eff`; resolved by merge `26b12450284b9331f79fbbffe3220d93e40c0916` | Google Antigravity (Advanced Agentic Coding); underlying model not evidenced | CLOSED — PASS; AC-01…AC-16 PASS; findings NONE; reviewer modified no files; Human accepted review and approved merge | No |
| REV-P0-008-SPECIFICATION | P0-008 MVP Release & Handover Readiness specification | v0.1.0 at `52d3c62d3741e9e7abc98c2bf2b300b4885f316c` | Google Antigravity (Advanced Agentic Coding); underlying model not evidenced | CLOSED — PASS; AC-01…AC-16 PASS; findings NONE; Human decisions required NONE; Human approved implementation | No |
| REV-P0-008-IMPLEMENTATION | P0-008 local/synthetic handover documentation and fresh evidence | Reviewed `956ba93048536d2a54d120752ade5540ecc0d901`; resolved by merge `e6b2f665f6334047ec420c49d2097732f2917354` | Google Antigravity; Gemini 1.5 Pro (Advanced Agentic Coding) | CLOSED — PASS; AC-01…AC-15 independent PASS, AC-16 completed by Human acceptance; findings NONE | No |

## 21. Recent Decisions

Human đã phê duyệt ADR-006 và Output Schema v1.0.0 cho AI-001, sau đó merge PR #1 ngày 19/09/2026. Human cũng đã phê duyệt AI-002/ADR-007, AI-003/ADR-008 và DOC-001/ADR-009 theo bằng chứng merge hiện có. Ngày 20/09/2026, Human phê duyệt SPEC-001/002/003 là baseline, accept ADR-001…005 và chốt upload APP-001. Ngày 21/09/2026, Human approve/merge APP-002 qua PR #12, sau đó phê duyệt AI-RUNTIME-001 Specification v1.0.0 và ADR-010: Responses API, `gpt-5.6-sol`, reasoning high, `store=false`, không retrieval, timeout 180, SDK retries 2 và 48.000 output tokens. Sau implementation review, F-001 remediation và targeted PASS, Human approve/merge AI-RUNTIME-001 qua PR #14 tại `597f6c7b074eb2c5e445790b8c4f48f336f04da5`. Ngày 22/09/2026, sau khi hoàn tất Checkpoints A-E, remediation đợt cuối và independent review APPROVED, Human / Product Owner đã approve và merge PR #16 cho AI-RUNTIME-002 tại merge commit `978516a4f5caa90bbd2189668237c6e028597361` (implementation head `a59ce0219d7039f24fa8c7bd71d4e9829dbbf612`), đồng thời miễn trừ synthetic live smoke call trước merge do chưa cấp kinh phí API (bắt buộc trước production deployment). Cũng trong ngày 22/09/2026, sau khi hoàn tất các vòng độc lập rà soát đặc tả APP-003 (remediation v1.1.0 và final hardening v1.2.0 cho H-001/H-002/H-003 đều PASS), Human / Product Owner đã chính thức phê duyệt APP-003 Specification v1.2.0 và merge PR #18 tại commit `bfbcdc760916f497b603bcd49ce0150d6819d337`, đồng thời hoãn triển khai kỹ thuật APP-003 đến 26/09/2026 cho Codex thực hiện sau khi quota reset. Các quyết định này không phê duyệt frontend, public analyze/draft endpoints, DOCX integration endpoint, database/auth, production storage hoặc deployment.

| Decision ID | Human decision | Trạng thái |
|---|---|---|
| DEC-001 | Phê duyệt SPEC-001/002/003 là baseline hiện hành (20/09/2026) | Recorded |
| DEC-002 | Accept nguyên trạng ADR-001…005 theo phạm vi từng ADR (20/09/2026) | Recorded |
| DEC-003 | Khóa upload/local single-tenant ephemeral scope, synthetic-only và retention tối đa 1 giờ cho APP-001 (20/09/2026) | Recorded and implemented in APP-001; merged via PR #10 |
| DEC-004 | Phê duyệt AI-RUNTIME-001 Specification v1.0.0 và runtime configuration (21/09/2026) | Recorded, implemented and merged via PR #14 |
| DEC-005 | Phê duyệt và merge PR #16 cho AI-RUNTIME-002 draft generation runtime; hoãn synthetic live smoke do chưa cấp kinh phí API (22/09/2026) | Recorded, implemented and merged via PR #16 |
| DEC-006 | Phê duyệt APP-003 Specification v1.2.0 và merge PR #18; hoãn implementation đến 26/09/2026 cho Codex thực hiện sau khi quota reset (22/09/2026) | Recorded, specification merged via PR #18 at `bfbcdc760916f497b603bcd49ce0150d6819d337` |
| DEC-007 | Đóng P0-005 Frontend MVP tại final accepted SHA `43907213f14c8c55294f55af34afcc0cbcc9dc66` sau independent review `ACCEPT`; release-blocking findings `NONE`; không merge `main` trong closeout này (26/09/2026) | Recorded; P0-005 CLOSED |
| DEC-008 | Human / Product Owner phê duyệt HD-P0-006-01…07 cho P0-006 specification sau Gemini 3.8 Flash High review v0.1.0 `PASS WITH HUMAN DECISIONS REQUIRED`, findings `NONE` (27/09/2026) | Recorded historical gate; decision gate RESOLVED; later review/implementation approval recorded in DEC-009 |
| DEC-009 | Gemini 3.8 Flash High targeted re-review P0-006 specification v0.2.0 at `5dfbbca9b66367a7930bd3892b8a0ea883781f31`: `PASS`, findings `NONE`; Human / Product Owner explicitly approved implementation (27/09/2026) | Recorded historical implementation gate; later independent review and Human merge approval recorded in DEC-010 |
| DEC-010 | Human / Product Owner accepted Google Antigravity (Advanced Agentic Coding) P0-006 independent implementation review `PASS`, findings `NONE`, and approved merge of `0f1e94db438869a980db8a1cb1e06956de2d8d3e` into `main` | Recorded; merge `3207479e5cca73da3e7facbc7c482d2ce5eba2b9`; P0-006 CLOSED / Completed; BLK-003 OPEN; GOV-P0-006-01 was OPEN at that closeout and is now RESOLVED separately |
| DEC-011 | Human / Product Owner approved P0-007 implementation after Google Antigravity (Advanced Agentic Coding) independent specification v0.1.0 `PASS`, AC-01…AC-16 `PASS`, findings `NONE`, Human decisions required `NONE` | Recorded; fixed specification `f98cf600f47a6559175c10dc3498846a7ae4395b`; implementation review and merge/release approvals are separate pending gates |
| DEC-012 | Human / Product Owner accepted Google Antigravity (Advanced Agentic Coding) P0-007 independent implementation review `PASS`, AC-01…AC-16 `PASS`, findings `NONE`, and approved merge of accepted implementation/handoff `bd43a7e9875537c4f5ebdee53626542a11500636` into `main` | Recorded; merge `26b12450284b9331f79fbbffe3220d93e40c0916`; P0-007 CLOSED / COMPLETED — MERGED; BLK-003 OPEN; no production/MVP-release approval |
| DEC-013 | Human / Product Owner approved P0-008 implementation after Google Antigravity (Advanced Agentic Coding) independent specification v0.1.0 PASS, AC-01…AC-16 PASS, findings NONE, Human decisions required NONE; Human also approved a non-blocking MCP reconciliation exception | Recorded at spec `52d3c62d3741e9e7abc98c2bf2b300b4885f316c`; MCP remains `Final hardening`/`PLANNED` with no metadata update/lease; implementation review, handover acceptance and production approval are separate future gates |
| DEC-014 | Human / Product Owner accepted P0-008 independent implementation review PASS/findings NONE, completed AC-16, granted `MVP HANDOVER READY — LOCAL/SYNTHETIC` classification and approved implementation merge/post-merge closeout | Reviewed `956ba93048536d2a54d120752ade5540ecc0d901`; merged at `e6b2f665f6334047ec420c49d2097732f2917354`; BLK-003 OPEN; no production/public/confidential-data approval or MCP reconciliation |
| DEC-015 | Human / Product Owner approved P0-009 offline CI design from reconciled main `bf837ef10622160fc76f80227e23f81830d69f76` and the narrow `PLAYWRIGHT_PYTHON` override in Playwright config | Local `.venv` default retained; CI uses setup-python 3.12 on PATH without repository `.venv`; no application/test-expectation change, provider calls, production approval or merge authorization |
| DEC-016 | Human / Product Owner approved F-01 test-helper interpreter-portability remediation, accepted Gemini 3.1 Pro High targeted PASS/F-01 RESOLVED and successful PR CI, and authorized PR #28 merge and post-merge closeout | Final accepted `ce9f723e143671d4917bf0bf5885772af3b00f7b`; normal merge `1f1754607152053ed4788f7fd5208c782432a320`; main CI `36397653688` SUCCESS; BLK-003 OPEN; no production/public/real-data approval |
| DEC-017 | Human / Product Owner accepted Gemini 3.1 Pro High EVAL-001 specification `PASS WITH HUMAN DECISIONS REQUIRED` (AC-01…AC-18 PASS, findings NONE) and approved framework-phase implementation with seven bounded decisions | Corpus >=6 / >=1 Vietnamese / >=2 domains; Section 10 thresholds unchanged; AI-assisted gold requires Human acceptance; provider access NOT AUTHORIZED, budget 0, repeated live runs NOT AUTHORIZED, sources manifest/local-only; product-runtime evidence blocked; no EVAL-001 completion or production approval |

## 22. Next Recommended Action

1. EVAL-001 — Draft PR #29 CI succeeded; obtain Gemini 3.1 Pro High independent framework implementation review at the final fixed SHA and Human corpus/gold acceptance separately. Actual product-runtime semantic evaluation remains blocked pending separate provider authorization/budget and cannot be called PASS or Completed.
2. Subsequent sequence: SEC-001 production security/BLK-003, a separate Human-approved deployment/staging task, then UX hardening if approved. MCP reconciliation remains BLOCKED BY TOOL CAPABILITY under the Human-approved non-blocking governance exception; no fabricated MCP state/lease.
3. BLK-003 remains OPEN and blocks production/real-data use; live-provider smoke remains UNVALIDATED / DEFERRED, public deployment NOT PERFORMED and production NOT APPROVED.

## 23. Last Updated

**28/09/2026 GMT+7**
