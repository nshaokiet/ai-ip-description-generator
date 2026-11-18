# ADR-003 — Gemini Reviewer Role

## Metadata

| Thuộc tính | Giá trị |
|---|---|
| Status | Accepted |
| Date | 20/09/2026 |
| Decider | Human / Product Owner |
| Version | 0.1.0 — first explicit ADR version, 2026-11-18 addendum |

## Context

Dự án cần independent review tách khỏi implementation ownership và production runtime.

## Decision

Gemini Pro là Research Analyst, Independent Reviewer và QA Reviewer; không là production AI dependency, implementation owner hoặc actor tự sửa artefact production.

### Permanent reviewer-model selection — effective 2026-11-18

The original role decision above is preserved. Its model label is historical:
the standing authorized reviewer is now **Gemini 4 Argon (High)**, replacing
Gemini 3.8 Flash High under the [permanent Human decision](GOV-REVIEWER-002-permanent-reviewer-model.md).
This applies to all current/future independent Security and Quality reviews,
including PR #165, until a subsequent explicit Human decision supersedes it.
STRICT READ-ONLY, separate independent stream evidence, actual model/profile/
session ID/freshness, exact-HEAD CI/security gates and applicable Human merge
authorization remain mandatory. If unavailable, STOP and obtain explicit Human
authorization before substituting a model. No historical review is reattributed.

Version history: unversioned -> 0.1.0, 2026-11-18, Codex; append the approved
selection supersession while preserving the accepted role decision; Human
authorization recorded in GOV-REVIEWER-002. Breaking change: No product/API or
role-authority change.

## Alternatives considered

- Gemini vừa implement vừa review: giảm tính độc lập.
- Gemini là production runtime: mở rộng provider/scope chưa cần thiết.

## Consequences

- Kết quả Gemini chỉ được ghi vào Review Log sau khi review thực tế xảy ra và có bằng chứng.
- Recommendation của reviewer không thay Human approval.
- Review không tự thay đổi production artefact hoặc project state.
- Human / Product Owner giữ quyền quyết định cuối cùng.
