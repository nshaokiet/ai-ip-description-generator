# RESUME-FOUNDATION-001 — Quyết định tiếp tục sản phẩm web

Version: 1.0.1. Date: 05/11/2026, Asia/Saigon. Author: Codex.
Status: HUMAN DIRECTION RECORDED; documentary candidate, independent review PENDING.
Authorization reference: `RESUME-FOUNDATION-001`, Human direct instruction05/11/2026;
source retained privately, digest in public technical evidence. Later Human instruction
explicitly permits this public-safe projection and Draft PR after verification.
Workflow: V1, no V2 execution/enrollment asserted. Breaking change: No runtime change.

1.0.0→1.0.1: public-safe source/provenance wording; full original retained locally.

## Quyết định và phạm vi được phép

Sản phẩm đích là **website Next.js + FastAPI**: upload → xử lý nguồn → dựng bản
nháp → Human review/chỉnh sửa → validate → xuất bộ USPTO v2. Local/offline/synthetic
là môi trường và chế độ kiểm thử. MCP điều phối phát triển; không phải database
hồ sơ người dùng website. Human yêu cầu xác minh, sửa tài liệu/checkpoint, chuẩn
bị một task kế tiếp và Draft PR foundation; không thực thi toàn roadmap.

Chỉ dẫn này thay thế **khuyến nghị terminal-first cho increment sản phẩm kế tiếp**
tại [PRODUCT-001B v0.1.0, ff511e5](https://github.com/nshaokiet/ai-ip-description-generator/blob/ff511e5b4e384268224d586a8abd3cea11313655/docs/tasks/PRODUCT-001B-trusted-local-review-presenter.md).
Bản cũ được giữ [nguyên văn trong history](../tasks/history/PRODUCT-001B-trusted-local-review-presenter-v0.1.0.md).
Terminal có thể là công cụ phát triển; không còn là kết quả người dùng của B.
[B v0.2.0](../tasks/PRODUCT-001B-trusted-local-review-presenter.md) là contract web
đề xuất, chưa freeze, chưa triển khai, chưa được duyệt security policy.

## Ranh giới còn hiệu lực

- Dùng lại PRODUCT-001A/C1/P2; không tạo pipeline thứ hai hoặc gửi authority nội
  bộ cho browser. Server giữ source/owner/session/revision/review/manifest.
- B cần quyết định riêng trước khi thực thi session/auth/CSRF/owner policy. Việc
  ghi hướng web không tự cấp quyền đổi security/data policy theo AGENTS §19.
- [C2 REVISION-004](https://github.com/nshaokiet/ai-ip-description-generator/pull/146)
  vẫn là specification-only đã có Human architecture acceptance; không tự biến
  contract same-process thành browser authorization. B là increment riêng, không
  âm thầm sửa frozen C2 hoặc tuyên bố thực hiện đủ C2 pilot.
- C1/PRODUCT-001A và review/CI/security gates giữ nguyên. Foundation không merge
  hoặc đóng PR implementation, đổi settings, rerun workflow, deploy hoặc gọi AI.
- Provider/API budget USD 0; dữ liệu thật/chưa công bố không được dùng; EVAL-001
  PRODUCT_RUNTIME deferred, semantic acceptance NOT_DETERMINED; BLK-003 OPEN;
  production readiness NO. Bốn file đều là draft cần Human review.

## Xung đột và disposition có bằng chứng

| Nguồn | Quan sát / disposition |
|---|---|
| PROJECT_CONTEXT / system-specification / workflow và AGENTS lịch sử | Các mốc cũ giữ nguyên; trạng thái hiện hành đọc tại [Control Center](../operations/01_PROJECT_CONTROL_CENTER.md#resume-foundation-001-current-baseline). AGENTS vẫn là authority về quyền/gates. |
| AGENTS mô tả repository Private ngày 18/09 | API ngày 05/11 trả public; không suy ra quyền dùng dữ liệu mật, không thay visibility. Không có bằng chứng ở lượt này để kết luận có leak hay ai đổi visibility. |
| README cũ ghi C2 chưa có quyết định / CI chỉ lỗi quota | PR146 có architecture acceptance và attributed fixed-SHA PASS; required CI vẫn failure. Run148 upload thành công; run149 bị QA HTTP503. Sửa summary, không đổi lịch sử run. |
| Report PRODUCT-001A local | Giữ nguyên byte và attribution; TTL900 và severity Low trong report không thay code/advisory. [Reconciliation](../tasks/PRODUCT-001A-review-reconciliation.md) ghi correction riêng. |

Đây là record của chỉ dẫn Human và delta kế hoạch; không phải independent PASS,
implementation authorization cho task kế tiếp, semantic acceptance hay release.
