# ADR-005 — Human Review Required

## Metadata

| Thuộc tính | Giá trị |
|---|---|
| Status | Accepted |
| Date | 20/09/2026 |
| Decider | Human / Product Owner |

## Context

Hệ thống xử lý nội dung nghiên cứu và tạo bản dự thảo liên quan SHTT, có rủi ro hallucination, thiếu evidence và hiểu nhầm pháp lý.

## Decision

Human review là bắt buộc trước mọi sử dụng quan trọng, export/release theo policy được duyệt hoặc mục đích SHTT/pháp lý. Output luôn là draft, không filing-ready, không phải tư vấn pháp lý hay kết luận patentability. Claims nằm ngoài MVP hiện hành. Human approval/audit state không được nhúng vào AI payload như trạng thái do model sinh.

## Alternatives considered

- Fully automated approval/export: rủi ro pháp lý và kỹ thuật không chấp nhận được.
- Human review tùy chọn: không đủ bảo vệ cho nội dung nhạy cảm.

## Consequences

- UI/runtime tương lai phải hiển thị disclaimer, evidence, missing/conflict/inference và review state.
- Reviewer AI không thể thay Human decision.
- Merge, production release và việc sử dụng dữ liệu thật cần Human decision có bằng chứng.
- APP-001 chỉ upload/validate; không tạo hoặc phê duyệt nội dung SHTT.
