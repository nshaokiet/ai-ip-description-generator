# Folder Structure / Bản đồ thư mục Anh–Việt

> Mục tiêu: giúp Human và agent hiểu ngay mỗi thư mục dùng để làm gì mà không đổi các technical path đã được code/tests/imports sử dụng.

## Quy ước đặt tên

Các **physical folder paths vẫn giữ tên kỹ thuật tiếng Anh** để tránh phá Python imports, test paths, IDE/MCP config và tài liệu canonical. Mỗi folder có **display name Anh / Việt** và trách nhiệm rõ ràng trong README của chính folder đó.

| Path | English name | Tên tiếng Việt | Nhiệm vụ chính |
|---|---|---|---|
| `backend/` | Backend | Xử lý máy chủ | Upload, parsing, storage tạm, AI runtimes, validation, grounding |
| `frontend/` | Frontend | Giao diện người dùng | Upload UI, progress, review/edit, export trigger |
| `prompts/` | Prompts | Câu lệnh AI | Prompt production có version và contract AI |
| `schemas/` | Schemas | Lược đồ dữ liệu | JSON Schema production và data contracts |
| `templates/` | Templates | Mẫu tài liệu | DOCX templates, manifests và field mappings |
| `tests/` | Tests | Kiểm thử | Unit/integration/regression, fixtures synthetic, offline/live separation |
| `docs/` | Documentation | Tài liệu dự án | Specification, ADR, task specs, operations, archive |
| `tools/` | Tools | Công cụ nội bộ | MCP/orchestration và developer tooling |
| `.github/` | GitHub configuration | Cấu hình GitHub | PR template và GitHub-native repository configuration |

## Nhóm nhiệm vụ / Responsibility groups

1. **Application / Ứng dụng:** `backend/`, `frontend/`
2. **AI Contracts / Hợp đồng AI:** `prompts/`, `schemas/`
3. **Document Output / Đầu ra tài liệu:** `templates/`
4. **Quality / Chất lượng:** `tests/`
5. **Governance & Knowledge / Quản trị & tri thức:** `docs/`
6. **Developer Tooling / Công cụ phát triển:** `tools/`, `.github/`

## Tại sao không đổi tên path vật lý sang song ngữ?

Các path như `backend`, `tests`, `schemas`, `prompts` đang được import hoặc tham chiếu trực tiếp trong Python, tests, docs và MCP/IDE config. Đổi path vật lý chỉ để hiển thị sẽ tạo refactor lớn và có nguy cơ phá build/test. Vì vậy repository dùng **technical path ổn định + bilingual display name**.
