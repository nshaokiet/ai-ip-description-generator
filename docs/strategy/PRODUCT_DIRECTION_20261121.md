# REALIGN-001 — Repository audit, gap analysis và roadmap

| Trường | Giá trị |
|---|---|
| Document / version | PRODUCT-DIRECTION-20261121 / 0.2.1 |
| Date / owner | 22/11/2026 Asia/Saigon / Nguyễn Song Hào Kiệt — Independent Developer |
| Status | Phase 1 documentation candidate; independent Security/Quality PENDING; không phải closeout |
| Audit baseline | main `6bb947c1cf67bcfb3ffc935b3a3fafcafb87f0af`; tree `aaece7b6128648deae0ebb2b60749f786cb0ca8f` |
| Candidate / authority | Draft PR167, `docs/product-direction-20261121-web-api-ready`; Master Project Realignment directive, 21/11/2026 |
| Boundary | USD 0; không provider invocation, nghiên cứu thật, Claims activation, deployment hoặc merge |

## A. Repository Reality Check

GitHub API xác nhận repository PUBLIC, default branch `main`; branch protection của main chưa bật ở lúc đọc. Không vì vậy mà miễn gate dự án. Checkout mới sạch, đúng SHA. Đã kiểm source tree, README/PROJECT_CONTEXT/AGENTS/system spec/workflow, decisions/tasks, schema/prompt, corpus/maps/templates, backend/frontend/tests, CI và render.yaml. Static audit cùng targeted offline checks không phải full acceptance/penetration test.

Main [CI43357769931](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/43357769931): COMPLETED/SUCCESS trên đúng SHA, cả `mcp-tests` và `build-and-test` SUCCESS. Run ngày 13/11 không phải dependency audit mới ngày 21/11; không suy graph hiện vẫn sạch vulnerability.

| Open PR | HEAD lúc audit | Trạng thái / next action |
|---|---|---|
| [#165](https://github.com/nshaokiet/ai-ip-description-generator/pull/165) | `4186b7afd4845497decc041f3016968fada2c754` | [CI44905331090](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/44905331090) SUCCESS. Implementer đã sửa dynamic-directory finding, independent verification PENDING; hai Security/Quality review mới, historical authorization provenance disposition và Human merge authorization còn thiếu. OPEN/DRAFT. |
| [#166](https://github.com/nshaokiet/ai-ip-description-generator/pull/166) | `37e9344465e5bc052bb02e9da60c23d67e7f62de` | Reviewer policy + metadata-validator correction; [CI44889601897](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/44889601897) FAILURE tại dependency audit. Direct Owner Argon choice có hiệu lực model selection, không phải PASS/merge authority. |
| [#164](https://github.com/nshaokiet/ai-ip-description-generator/pull/164) | `f08b071ee76468f01ad20bfa917d1b6360e5b453` | S2-A default-OFF bridge chưa có trên main; [CI44230339727](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/44230339727) FAILURE theo PR receipt. Windows proof không thay Linux browser proof/reviews. |
| [#167](https://github.com/nshaokiet/ai-ip-description-generator/pull/167) | audit-start `67dd983f6f84390169468f1a729d8a3e2f45bca7` | Existing strategy PR đang được mở rộng; old-head [CI44903839302](https://github.com/nshaokiet/ai-ip-description-generator/actions/runs/44903839302) FAILURE tại security graph. Không dùng làm kết quả HEAD mới. |
| #152/#150/#148/#146/#144/#143/#140 | OPEN/DRAFT, legacy | Giữ nguyên; #148 diagnostic DO NOT MERGE. Đối chiếu supersession với main/#153/#154/#155/#156 trước quyết định riêng; không tự đóng hoặc merge. |

**11 open Draft PRs** lúc đọc. Sáu open issues: [#160](https://github.com/nshaokiet/ai-ip-description-generator/issues/160) MCP input/resource planning; [#131](https://github.com/nshaokiet/ai-ip-description-generator/issues/131) PREAPI; [#126](https://github.com/nshaokiet/ai-ip-description-generator/issues/126) unknown-task; [#121](https://github.com/nshaokiet/ai-ip-description-generator/issues/121) API-v2 spec; [#113](https://github.com/nshaokiet/ai-ip-description-generator/issues/113) old reviewer policy; [#111](https://github.com/nshaokiet/ai-ip-description-generator/issues/111) offline orchestration. Open issue không chứng minh code chưa merge.

Không có tool Project Orchestrator/Antigravity/Gemini execution trong phiên này: MCP state/lease **NOT VERIFIED**, independent reviews **NOT RUN**. Requested reviewer theo direct Owner decision: **Gemini 4 Argon (High), Antigravity STRICT READ-ONLY**, actual profile/model/session/reuse phải được ghi; Security/Quality độc lập. #166 vẫn pending integration.

`render.yaml` cấu hình public synthetic demo và `checksPass`; repository config không phải live Render readback. Không đổi Render, không khẳng định live auto-deploy OFF. Trước merge phải xác minh platform để tránh deployment ngoài quyền.

## B. Product Alignment

Giữ website Next.js + FastAPI, parsing/reconstruction/Claims/renderer; không có căn cứ xây lại hoặc tạo CLI product thứ hai. Đề xuất 0.1.0 chỉ nhắm mock E2E rồi chờ API đã thiếu Prior Art/confidentiality/internal group/ba loại output. [Yêu cầu Owner mới](AIIP_PRODUCT_REQUIREMENTS.md) thay ưu tiên đó. `API_READY_SYNTHETIC` chỉ là mốc kỹ thuật.

README được bỏ nhận diện tổ chức, ghi sản phẩm độc lập. **UI còn legacy logo/attribution** ở `frontend/src/app/page.tsx`, `frontend/src/lib/uiPreferences.tsx`; xử lý P0-ID sau gates, không đổi UI trong Phase 1. Không công bố lại tên tổ chức/nghề nghiệp riêng tư hoặc phán quyết ownership. Không xóa history/evidence.

## C. Feature Gap Matrix

Status áp dụng đúng phạm vi mỗi dòng: `Implemented & Verified` cần test thực của scope; `Offline/Mock Verified` chỉ synthetic; `API-Ready` chỉ interfaces/preflight, không live acceptance; `Deprecated` chỉ proposal bị Owner thay thế. Effort S/M/L tương đối, không phải cam kết thời gian. USD 0 là chi phí dự kiến với stack hiện có, không gồm vận hành production.

| Requirement | Current implementation / status | Missing functionality / proposed action | Priority | Dependency | Cost / effort / API | Risk / testing |
|---|---|---|---|---|---|---|---|
| Independent identity | Docs Partial; UI legacy attribution | P0-ID: chỉnh UI identity, regression layout | P0 | Phase 1/1B | 0 / S / no | Sai attribution; string/UI checks |
| PDF/DOCX intake | Offline/Mock Verified: validation/parsing text PDF + DOCX text/table | Nối browser v2; giữ 10 MiB/text-PDF 50-page constraints; scanned/OCR chưa có | P0 | S1/S2-A acceptance, fixture admission | 0 / M / no | File/path/parser abuse; reject/locator tests |
| Full scientific input | Partially Implemented: TEXT/TABLE source units | Inventory image/formula/chart assets, không coi text extraction là full multimodal | P0 | Intake/evidence model | 0 / L / no infrastructure API | Mất số liệu/ý nghĩa; source/asset comparison |
| Scientific analysis | Offline/Mock Verified reconstruction/specification; live Blocked | Adequacy/missing view, Human stop/continue | P0 | Grounding/browser | 0 / M / mock now | Hallucination; sparse/refusal/contradictions |
| Confidentiality | Not Implemented consent workflow; defaults/tripwire có | Classification, bounded consent/revocation/query preview trước egress | P0 | Existing session/custody | 0 / M / no | Bí quyết lộ; denied/stale/revoked-scope tests |
| Prior Art | Not Implemented per-paper; corpus chỉ reference | Manual evidence source/date/query/similarity/difference/limits; mandatory record hoặc explicit incomplete continuation | P0 | Confidentiality/revision | 0 / M / no; manual first | Query leak/fake citations; no-search/incomplete/refusal |
| Patent specification | Offline/Mock Verified P2-002/003/005; API adapters có | Browser drafting sau confidentiality/Prior Art records, reuse pipeline | P0 | #164/S2 + prior steps | 0 / M / mock | Unsupported facts; source/manifest/revision checks |
| Claims | Implemented but Disabled in product; standalone + synthetic SYSTEM/APPARATUS positives | Trace/refusal UI trước; activation/family expansion qua gate riêng | P0 | Source/spec/authority | 0 / L / validation no API | Unsupported elements/overbreadth; OFF/support tests |
| Figures | Not Implemented redraw; metadata/references có | Asset map/deterministic redraw/reference numerals/fidelity approval | P0 | Asset/source locators | 0 / L / infrastructure no API | Sai topology/values; original/redraw compare; flag uncertainty |
| Editing | Partially Implemented v1 `draftRevisions.ts`, UI, C1 revisions | Nối source-bound v2 edit/revalidation, chat interfaces/mock | P0 | Custody/browser/version design | 0 / M / mock | Stale edits/reviews; optimistic revision tests |
| QA | Offline/Mock Verified schema/grounding/business/layout/support checks | Tổng hợp tám lớp; scientific/figure semantic review còn thủ công; serious edit confirmation | P0 | Validators/figures | 0 / M / real AI later | False PASS; unsupported/contradiction/missing tests |
| Review/export states | Partially Implemented C1 ack + four synthetic exports | Four business states, Admin-only final approval, Member DRAFT export mọi trạng thái có warnings | P0 behavior; P1 RBAC | State/identity contract | 0 / M / no | Escalation/stale approval; incomplete draft tests |
| Three outputs | Patent Draft Offline/Mock Verified; Annotated/Analysis export Not Implemented | Reuse renderer/projections, position notes + separate report, DOCX/PDF matrix | P0 | QA/Prior Art/export | 0 / M / no | Citation/private-note leak; integrity/content tests |
| Vietnamese/English | UI toggle có; drafting Partially Implemented | Output language + terminology/values/Claims equivalence | P1 | Canonical content | 0 / M / mock; real AI later | Scope drift; bilingual review |
| Internal Admin/Member | Local S1 pairing Implemented & Verified within its scope; RBAC Not Implemented | No public signup, server case permissions/Admin approval | P1 before team use | Auth/data policy | 0 / L / no | Cross-user read/write/download; role matrix tests |
| Cases/version/audit | Partial ephemeral custody + in-memory UI revisions | Durable records/immutable approved versions, actor/time/reason/export history, restore/retention | P1 before real data | Access/private storage decision | 0 / L / no | Loss/exposure; isolation/restore/delete tests |
| Provider interfaces | API-Ready extraction/draft adapters + offline preflight | Entitlement UNVERIFIED; live spend enforcement NOT_IMPLEMENTED; live semantic Blocked | P0 before paid pilot | Funding/data authorization | 0 prep / M; paid runtime gated | Spend/secrets; no-client tripwires/future caps |
| Old defer-all proposal | Deprecated as current target | Preserve v0.1.0 in Git history; follow new requirements | P0 docs | Owner directive | 0 / S / no | Stale instructions; consistency/link checks |

## D. Updated Roadmap

Mỗi dòng là scope riêng; không triển khai toàn bộ roadmap một lần. Nhãn Phase2free-development cũ không phải inventory Phase2 của lượt22/11. Inventory read-only được Owner cho phép nếu Phase1 integration bị chặn; implementation task cần authority V1 hoặc governance168 thực sự được chấp thuận. Không hỏi lại yêu cầu đã chốt; chỉ xác định quyết định kỹ thuật/bảo mật còn thiếu trước task phụ thuộc.

| Order / task | Lý do / đầu ra tối thiểu | Dependency / exit |
|---|---|---|
| 0 — REALIGN-001 | Audit/docs/roadmap nhất quán, public-safe, tách target/runtime | PR167 new-head checks/reviews và merge/platform authority hiện hành |
| 1 — GOV-AUTONOMY-001 | PR governance riêng để Owner duyệt một lần; không tự merge | Human approval/integration, phối hợp #166; giữ independent/CI/security gates |
| P0-ID | UI đúng sản phẩm độc lập | Task-specific V1 scope/approval hoặc governance thực sự có hiệu lực; scoped UI diff/checks, giữ history |
| P0-CONF | Consent/egress gate, upload không đồng nghĩa API consent | Reuse S1/custody; default-deny, revoke/stale tests |
| P0-PRIOR | **Task nghiệp vụ giá trị cao nhất tiếp theo:** manual Prior Art trước drafting | P0-CONF/revision; evidence/explicit incomplete continuation; không cần search API |
| P0-WEB | Nối browser intake → analysis → confidentiality → Prior Art → review/edit → export | #165 → #164 fresh accepted dependencies; đối chiếu D01–D07/fixture decisions chưa giải quyết |
| P0-ASSETS / P0-FIG | Giữ image/chart/formula/source map, redraw có fidelity | Supported subset trước; không đoán geometry/data; uncertain output flagged |
| P0-CLAIM-QA | Support/refusal/trace UI; tám lớp QA và serious-change confirmation | Product Claims OFF tới gate/semantic approval riêng |
| P0-OUTPUT | Patent Draft + Annotated Draft + Analysis Report | Reuse renderer, version-bound content/warnings; fixtures từng loại |
| P1-ACCESS / P1-CASE | Admin/Member, persistent private cases, durable versions/audit/exports | Trước team/real-data use; storage/retention/backup/security decisions |
| P1-LANG / P1-OPS | VI/EN equivalence, vận hành/restore/security acceptance | Canonical content/roles, no Claims scope drift |
| P2-SEARCH | Automated lawful free search sau manual workflow | Source availability/terms/confidentiality; giữ manual fallback |
| P2-LOCAL-AI | Free local model experiment nếu phù hợp | Chưa có hardware telemetry máy Owner; chưa cài/thử model; không dependency bắt buộc |
| P2-ADVANCED | Redraw nâng cao/OCR/input mở rộng/tối ưu có bằng chứng | Không làm chậm P0/P1; không mặc định SaaS/RAG/vector DB/rewrite |

**API_READY_SYNTHETIC:** hai technical contents khác nhau (text PDF và DOCX), browser-to-export, source/consent/Prior Art records, negative/refusal tests, no-provider tripwires và artifact fidelity trong scope đã duyệt. **INTERNAL_GROUP_READY:** thêm P1 RBAC/persistence/audit/retention/security acceptance. Cả hai không bằng LEVEL 3 hoặc production approval.

## E. GitHub Evidence và validation boundary

Phase 1 chỉ Markdown, không code/schema/template/dependencies/fixture/gold/CI/render.yaml. Branch/final HEAD/TREE/changed paths/local checks/new CI được ghi ở PR167 sau commit; không nhúng SHA tương lai của chính commit. Independent Security/Quality PENDING, self-check không thay reviewer. Không ghi Completed/MERGED trước gate.

Corpus đã đối chiếu grant PDFs gốc qua Google Patents và USPTO/MPEP ngày 21/11: maps/counts/independent Claims/figure labels phù hợp ở phạm vi quan sát; tests giữ nguyên. Repository chưa pin binary/hash PDF gốc; không claim corpus binary reproducibility.

## F. Funding-Dependent Backlog

| Component | Chuẩn bị hiện có | Chờ gì / chưa xác minh |
|---|---|---|
| Extraction/draft | OpenAI adapters, prompts/schemas, timeout/retry/output caps, offline preflight | Account/model entitlement, funding/data/call authorization; live chưa chạy |
| Live spend guard | Checklists và test tripwires | Hard live USD/token/request enforcement NOT_IMPLEMENTED; phải kiểm trước activation |
| Scientific/Claims acceptance | Evaluator + gold 6 cases/154 items, synthetic authority/refusal tests | Bounded live outputs + Human IP review; EVAL-001 PRODUCT_RUNTIME NOT_DETERMINED |
| Chat edits/translation | Source/version primitives; target đã mô tả | Chat/prompt integration chưa đầy đủ; interfaces/mock làm được miễn phí |
| AI image/redraw | Metadata/figure references | Chưa có validated vision/redraw pipeline; API không tự chứng minh fidelity |

Prior Art thủ công/auth/RBAC/database/version/audit/export **không bị chặn vì thiếu API**. Không dùng thiếu kinh phí để bỏ qua gap miễn phí.

## G. Next Development Task

Scope nhỏ **P0-CONF rồi P0-PRIOR**; implementation chỉ khi có task-specific V1 authorization và prerequisites hoặc governance168 đã thực sự có hiệu lực. P0-PRIOR dùng manual source/date/query/evidence/limits, buộc có record hoặc `Prior Art Search Incomplete` + actor decision trước drafting; không kết luận tính mới/gọi search provider. Reuse custody revision binding, không external service mới.

Changelog 0.1.0 → 0.2.0, 21/11/2026, Codex: Owner-directed expanded gap/roadmap, sửa #165 snapshot, supersede defer Prior Art/internal users. Product planning delta Yes; runtime breaking change No; history/reviews giữ nguyên.

Direction checkpoint22/11/2026: tiếp tục167; Phase0preflight→Phase1direction→Phase2inventory→Phase3plan. Đây là alignment checkpoint trước inventory mới; Phase1 integration vẫn PENDING, không feature development, PR168NOT_EFFECTIVE.

Changelog0.2.0→0.2.1,22/11/2026,Codex: pre-inventory direction/phase reconciliation, no runtime change.
