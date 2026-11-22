# AI-IP — Yêu cầu sản phẩm và quy trình mục tiêu

| Trường | Giá trị |
|---|---|
| ID / version / date | REALIGN-001-REQ / 1.0.1 / 22/11/2026, Asia/Saigon |
| Owner | Nguyễn Song Hào Kiệt — Independent Developer |
| Status | Yêu cầu từ Owner; cập nhật repository chờ review/CI/integration |
| Scope / authority | Tài liệu theo Master Project Realignment ngày 21/11/2026; không đổi runtime hoặc quyền merge |

AI-IP Description Generator là sản phẩm phát triển độc lập: website Next.js + FastAPI hỗ trợ chuyển một bài báo PDF/DOCX thành bản thảo **Nonprovisional Utility Patent** có căn cứ để chuyên viên/đại diện sáng chế rà soát. Đây là mục tiêu, không phải tuyên bố mọi chức năng đã hoạt động. Xem [audit và roadmap](PRODUCT_DIRECTION_20261121.md).

Thông tin công khai về chủ dự án chỉ dùng tên, **Independent Developer** và sản phẩm phát triển độc lập. Không công bố thông tin nghề nghiệp riêng tư, quan hệ cơ quan hoặc nguồn giao nhiệm vụ. Không suy luận quyền sở hữu pháp lý đối với sản phẩm.

## Hai mục tiêu cốt lõi

1. **Standardized Patent Drafting:** một quy trình chuyển paper thành bản thảo có cấu trúc, source evidence và điểm kiểm tra của chuyên viên.
2. **U.S. Patent Application Preparation:** tạo nền tảng cho chuyên viên/đại diện sáng chế tiếp tục chuẩn bị hồ sơ; không tự nộp, không chứng nhận filing-ready hoặc patentability.

## Phạm vi

- Một bài báo cho một hồ sơ; không bắt buộc tải thêm tài liệu. Chuyên viên quyết định dừng/tiếp tục khi thiếu thông tin.
- Utility Patent / Nonprovisional Utility Patent Application drafting: specification, supported independent/dependent Claims, Abstract, hình vẽ, review/edit/QA và export.
- Chưa gồm provisional/design/plant patent, tự nộp đơn/thanh toán, thủ tục sau export, bảo đảm cấp bằng, quản lý IP doanh nghiệp hoặc tự chia paper thành nhiều hồ sơ.
- Reuse module hiện có. Local/offline/synthetic là chế độ phát triển/kiểm thử; MCP điều phối development, không phải database hồ sơ website.

Bằng chứng kỹ thuật dùng cho invention description/Claims phải từ bài báo đã tải. Prior Art phục vụ so sánh, không tự bổ sung invention fact, thông số hoặc kết quả không có trong nguồn.

## Quy trình mục tiêu

| Bước | Hành vi và điều kiện nghiệm thu mục tiêu |
|---|---|
| 1. Document Intake | PDF/DOCX, source ID/locator; text, hình/sơ đồ/biểu đồ, bảng, công thức, thông số, phương pháp, kết quả. Hiện parser mới bao phủ text/table, không được tuyên bố đã đọc image pixels hoặc công thức đầy đủ. |
| 2. Research Analysis | Nhận diện vấn đề, giải pháp, đặc điểm kỹ thuật, Claims support và phần thiếu. Đánh giá khả năng drafting, không kết luận patentability; chuyên viên được stop/continue có cảnh báo. |
| 3. Confidentiality | Intake/phân tích ban đầu ở môi trường được phép. **Phân loại và xác nhận trước mọi lần truyền ra ngoài**, kể cả AI analysis bước 2 và search query. Upload không phải consent gửi API. Lưu người xác nhận, thời điểm, phạm vi dữ liệu, evidence nếu có; kiểm tra lại khi thay đổi/thu hồi. |
| 4. Prior Art Search | Bắt buộc có bước tra cứu trước drafting; ưu tiên nguồn miễn phí hợp pháp, query không lộ giải pháp mật. Lưu nguồn/ngày/query được phép/tài liệu/tương đồng/khác biệt/giới hạn. Cho nhập thủ công có dẫn chứng. Không đủ: `Prior Art Search Incomplete`; chỉ tiếp tục với quyết định chuyên viên và cảnh báo. Không bypass im lặng hoặc suy tính mới chắc chắn. |
| 5. Patent Draft | Title, Technical Field, Background, Summary, Brief Description of Drawings, Detailed Description, Embodiments, Claims, Abstract và drawings theo applicability. Không bịa dữ liệu/kết quả/chi tiết kỹ thuật. |
| 6. Claims | Independent/dependent draft Claims; từng element có evidence trang/đoạn/bảng/hình và khớp description. Sửa trực tiếp/AI từng Claim; thiếu support bị flag/refuse. Giữ product runtime OFF tới gate riêng. |
| 7. Figure Redrawing | Bảo toàn topology, nhãn, số liệu và ý nghĩa; liên kết hình gốc–bản vẽ–description, Figure numbers/reference numerals. Chưa chứng minh fidelity: `REVIEW_REQUIRED`, không xuất như hình đã hợp lệ. |
| 8. Editing | Direct edit và chat theo section/Claim/figure; lưu actor/time/reason/before-after versions. Không ghi đè approved version; thay đổi làm mất hiệu lực review liên quan. |
| 9. QA | Tám lớp: structure/format, scientific accuracy, Claims support/consistency, figure fidelity, traceability, unsupported content, contradictions, missing information. Chỉ tự sửa format/lỗi xác minh chắc chắn; thay đổi nghiêm trọng Claims/thông số/hình cần chuyên viên xác nhận. Có báo cáo QA. |
| 10. Human Review & Export | `Draft → Under Review → Revision Required → Under Review`, hoặc Admin duyệt `Approved for Export`. Member trong quyền hồ sơ được xuất DRAFT dù thiếu thông tin, kèm cảnh báo/phần thiếu và quyết định tiếp tục của chuyên viên. Quyền hồ sơ, đúng revision, file integrity và confidentiality vẫn bắt buộc; quyền xuất nháp không phải bypass security hoặc giả support cho Claims. Approved là phê duyệt nội bộ, không phải chấp thuận pháp lý USPTO. |

## Tài liệu đầu ra và kiểu trình bày

| Loại | Nội dung mục tiêu | Hiện trạng |
|---|---|---|
| Patent Draft | Bản thảo DRAFT, marker tham chiếu phần thiếu | Renderer synthetic DOCX/PDF có sẵn |
| Annotated Draft | Ghi chú đúng vị trí: nguồn, Claims cần kiểm tra, thiếu/chưa xác minh/cảnh báo | Có review projections, chưa có annotated export hoàn chỉnh |
| Analysis Report | Analysis, Claims basis, Prior Art/limits, figures, missing, QA, việc cần xác nhận | Validation reports nội bộ có sẵn, chưa đủ report nghiệp vụ |

DOCX/PDF theo khả năng thích hợp. Chọn tiếng Việt nội bộ hoặc tiếng Anh hướng tới USPTO; kiểm tra bảo toàn thuật ngữ/số liệu/phạm vi Claims khi dịch. Chưa có nghiệm thu bilingual drafting.

**USPTO Application Draft** là mặc định mục tiêu; **Reference Patent Style** là tùy chọn, cùng nội dung khoa học. `B2_REFERENCE_PREVIEW.*` hiện là legacy technical filename, không phải biểu mẫu USPTO. US11367264B2 và US11044591B2 chỉ dùng cấu trúc/văn phong, Claims/Abstract/hình; không copy nội dung hoặc giả lập patent/application number, grant date, metadata cấp bằng. [Corpus và nguồn USPTO/MPEP](../references/P2-001-uspto-reference-corpus.md).

Mục hành chính chỉ `NOT_APPLICABLE` khi có căn cứ; chưa biết phải `MISSING`/cảnh báo. Technical Field/Embodiments có thể là subsection, không phải mọi heading là yêu cầu pháp lý độc lập. Thay executable template/schema cần version/compatibility/review riêng.

## Người dùng, hồ sơ và phiên bản

| Vai trò | Quyền mục tiêu |
|---|---|
| Admin | Quản lý tài khoản/cấu hình/toàn bộ hồ sơ/quyền; duyệt `Approved for Export` |
| Member | Intake/workflow/edit/Claims/export nháp, quản lý hồ sơ được cấp quyền |

Nhóm nội bộ, không public registration. Server kiểm quyền từng hồ sơ/mutation/download; local S1 pairing chưa phải Admin/Member RBAC.

Mỗi hồ sơ lưu source, analysis, Prior Art evidence, draft, figures, Claims, QA, revisions, export history và confidentiality consent. V1/V2/V3 có Human/AI actor, thời điểm, diff/lý do, before/after; đặc biệt trace Claims/hình/thông số. Approved version bất biến; revision mới cần review mới. Storage/backup/retention/deletion dùng stack hiện có, phải qua security decision trước nghiên cứu thật.

## Kinh phí, kiểm thử, deployment và authority

| Mức | Evidence |
|---|---|
| LEVEL 1 — OFFLINE / MOCK VERIFIED | Fixture/mock chứng minh hợp đồng và workflow kỹ thuật, không chứng minh AI thật |
| LEVEL 2 — LOCAL AI EXPERIMENTAL | Chỉ thử miễn phí nếu phần cứng phù hợp; báo model/config/chất lượng/giới hạn riêng; không là dependency bắt buộc |
| LEVEL 3 — REAL AI API VALIDATED | Sau approval provider/model/budget/data/bounded calls; đo scientific/Claims/figure/source fidelity và Human acceptance |

USD 0 hiện hành. Phát triển website/backend/documents/templates/database/validation/Prior Art/auth/audit/export/mock/interfaces/tests theo gap/gates. Không tự đăng ký dịch vụ trả phí, billing, gọi paid API, mua phần cứng hoặc truyền nghiên cứu mật ra ngoài. CI chỉ synthetic/public được phép. Không suy model entitlement từ tên model trong code hoặc tài khoản ChatGPT.

Development trong scope được tự thực hiện; staging chỉ miễn phí, phù hợp governance, dữ liệu mẫu/public được phép. Production luôn cần Owner approval; không tự công khai website/tạo signup/chuyển dữ liệu nội bộ lên hạ tầng mới. REALIGN-001 không deploy.

Owner directive ngày 21/11 thay đề xuất hoãn Prior Art/internal users: Prior Art thuộc P0, Admin/Member/persistence thuộc P1, confidentiality là P0 trước egress. Giữ schema/runtime/evidence lịch sử, không hồi tố approval PR cũ.

**Thuật ngữ điều hành theo instruction ngày22/11/2026:** Phase0 minimal preflight → Phase1 đối chiếu/cập nhật định hướng → Phase2 repository reality check → Phase3 gap analysis/roadmap. Nếu Phase1 chưa tích hợp, chỉ dùng ngoại lệ Owner cho phép kiểm kê read-only sau khi định hướng đã được cập nhật/đối chiếu; ghi rõ branch candidate, không gọi Phase1 Completed hoặc bắt đầu feature development.

PR168 là governance proposal NOT_EFFECTIVE, không là điều kiện để làm read-only inventory hoặc task đã được Human cho phép riêng theo V1. Không coi proposal là standing approval cho backlog. Các nhãn cũ “Phase1B/governance → Phase2 free development → Phase3 paid API” chỉ nói về proposal phát triển tương lai, không phải ba giai đoạn của lượt kiểm kê này. Runtime task tiếp theo vẫn cần ID/scope/AC/authorization theo governance hiện hành; production/paid/real-data/Claims activation cần gate riêng.

Changelog: new 1.0.0, 21/11/2026, Codex, REALIGN-001; Owner-directed product scope delta Yes; executable API/schema/template change No.

Changelog1.0.0→1.0.1,22/11/2026,Codex: hai objectives, thuật ngữ Phase0–3 theo Owner, draft-export/security separation; không đổi runtime/governance authority.
