# Schema registry

Các schema production của dự án được lưu theo artefact và semantic version. Không chỉnh sửa một version đã phát hành để thay đổi contract; tạo thư mục version mới và cập nhật ADR/migration notes.

| Artefact | Version | Canonical path | Status |
|---|---|---|---|
| Invention Output | 1.0.0 | `schemas/invention-output/v1.0.0/invention-output.schema.json` | Completed — Merged via PR #1 |
| Patent Draft | 1.0.0 | `schemas/patent-draft/v1.0.0/patent-draft.schema.json` | Completed — Merged via PR #5 |

Hướng dẫn và field contract:

- [`invention-output/v1.0.0/README.md`](invention-output/v1.0.0/README.md)
- [`patent-draft/v1.0.0/README.md`](patent-draft/v1.0.0/README.md)
