# Tools / Công cụ nội bộ

Thư mục này chứa tooling hỗ trợ phát triển và điều phối dự án, không phải production application runtime.

## Nhiệm vụ / Responsibilities

| Folder / Thư mục | Nhiệm vụ |
|---|---|
| `project-orchestrator-mcp/` | MCP điều phối task, quota guard, task lease, checkpoint/handoff và phối hợp Codex/VS Code/Antigravity |
| `local_dev.py` | Launcher stdlib cho backend + frontend local, readiness và shutdown cây tiến trình do launcher sở hữu |
| `offline_benchmark.py` | P1-005 deterministic offline benchmark cho validation, parsing, structured validation, DOCX export và local browser workflow |

## Offline performance baseline

Với Python/frontend dependencies đã cài và frontend đã build, chạy complete synthetic/offline baseline từ repository root:

```powershell
python tools/offline_benchmark.py --profile baseline --warmups 1 --samples 5 --output artifacts/p1-005-offline-baseline.json
```

JSON chứa environment/workload metadata, raw samples, median và nearest-rank p95. CI chỉ kiểm tra correctness; không áp absolute timing threshold trên shared runner. Live flags luôn bị khóa `0 / 0`, `OPENAI_API_KEY` bị loại khỏi browser subprocess và browser chặn non-loopback traffic.

## Quy tắc

- Tooling không được tự merge `main`.
- Không tự kích hoạt quota reset hoặc paid API.
- Không chứa API key, token hoặc dữ liệu nghiên cứu bí mật.
- Production APP code chỉ được sửa trong task implementation đã phê duyệt.
