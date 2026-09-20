# ADR-004 — GitHub Technical Source of Truth

## Metadata

| Thuộc tính | Giá trị |
|---|---|
| Status | Accepted |
| Date | 20/09/2026 |
| Decider | Human / Product Owner |

## Context

Dự án có repository GitHub, tài liệu vận hành có thể được chia sẻ qua Google Drive và research notes trong NotebookLM. Cần một nguồn kỹ thuật duy nhất có version history.

## Decision

GitHub repository Private `ai-ip-description-generator` là Technical Source of Truth cho source code, schema, prompt, template, tests và governance Markdown, bao gồm ADR/tài liệu kỹ thuật.

## Alternatives considered

- Google Drive là technical source: thiếu diff/branch/test traceability.
- NotebookLM là source: là research workspace, không phải production governance.

## Consequences

- Bản sao Google Docs chỉ là communication bridge và không ghi đè Git.
- Mọi kết luận triển khai/release phải trỏ về file, commit, PR hoặc test evidence trong repository.
