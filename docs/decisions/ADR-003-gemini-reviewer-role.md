# ADR-003 — Gemini Reviewer Role

## Metadata

| Thuộc tính | Giá trị |
|---|---|
| Status | Accepted |
| Date | 20/09/2026 |
| Decider | Human / Product Owner |

## Context

Dự án cần independent review tách khỏi implementation ownership và production runtime.

## Decision

Gemini Pro là Research Analyst, Independent Reviewer và QA Reviewer; không là production AI dependency, implementation owner hoặc actor tự sửa artefact production.

## Alternatives considered

- Gemini vừa implement vừa review: giảm tính độc lập.
- Gemini là production runtime: mở rộng provider/scope chưa cần thiết.

## Consequences

- Kết quả Gemini chỉ được ghi vào Review Log sau khi review thực tế xảy ra và có bằng chứng.
- Recommendation của reviewer không thay Human approval.
- Review không tự thay đổi production artefact hoặc project state.
- Human / Product Owner giữ quyền quyết định cuối cùng.
