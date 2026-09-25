# Tools / Công cụ nội bộ

Thư mục này chứa tooling hỗ trợ phát triển và điều phối dự án, không phải production application runtime.

## Nhiệm vụ / Responsibilities

| Folder / Thư mục | Nhiệm vụ |
|---|---|
| `project-orchestrator-mcp/` | MCP điều phối task, quota guard, task lease, checkpoint/handoff và phối hợp Codex/VS Code/Antigravity |

## Quy tắc

- Tooling không được tự merge `main`.
- Không tự kích hoạt quota reset hoặc paid API.
- Không chứa API key, token hoặc dữ liệu nghiên cứu bí mật.
- Production APP code chỉ được sửa trong task implementation đã phê duyệt.
