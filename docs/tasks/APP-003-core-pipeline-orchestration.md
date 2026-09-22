# APP-003 — Internal Core Pipeline Orchestration and Offline E2E Harness

## Metadata

| Thuộc tính | Giá trị |
|---|---|
| Task ID | APP-003 |
| Document title | APP-003 — Internal Core Pipeline Orchestration and Offline E2E Harness Specification |
| Specification version | 1.1.0 |
| Status | Specification — Remediated — Awaiting Independent Re-review |
| Owner | ChatGPT/Codex |
| Author | Gemini 3.8 Flash High |
| Reviewer | Gemini 3.1 Pro High + Human / Product Owner |
| Human specification approval | Pending independent re-review |
| Baseline commit | `59bfe67583040319a7a0c2aa156db31bab382737` |
| Branch | `docs/app-003-core-pipeline-orchestration-spec` |
| Prepared date | 22/09/2026 |
| Target completion | Internal baseline before 02/10/2026 |
| Related tasks | APP-001, APP-002, AI-RUNTIME-001, AI-RUNTIME-002, DOC-001 |
| Applicable ADRs | ADR-001, ADR-002, ADR-003, ADR-004, ADR-005, ADR-006, ADR-007, ADR-008, ADR-010 |
| Blocker status | BLK-003 remains OPEN; synthetic-only and internal local development |

---

## 1. Objective

Triển khai dịch vụ điều phối pipeline nội bộ (**Internal Core Pipeline Orchestration**) và bộ kiểm thử tích hợp đầu-cuối ngoại tuyến (**Offline E2E Harness**) để kết nối các thành phần đã hoàn tất và đã merge vào repository thành một luồng xử lý hoàn chỉnh duy nhất:

```text
Validated Document (APP-001 upload & storage)
→ APP-002 deterministic parsing & evidence preparation
→ AI-002 Extraction Input Envelope
→ AI-RUNTIME-001 extraction runtime (OpenAI Responses API)
→ Validated AI-001 Structured Invention Analysis
→ Deterministic AI-003 Draft Input Envelope
→ AI-RUNTIME-002 draft generation runtime (OpenAI Responses API)
→ Validated Patent Description Draft JSON
→ Mandatory best-effort source cleanup (APP-001 contract)
```

Mục tiêu cốt lõi:
1. **Liên kết tuần tự, nhất quán và chặt chẽ:** Kết nối các tầng xử lý nội bộ mà không làm thay đổi hay làm sai lệch hợp đồng dữ liệu chuẩn (**canonical contracts**) của AI-001, AI-002, AI-003, APP-001, APP-002, AI-RUNTIME-001, và AI-RUNTIME-002.
2. **Fail-closed nghiêm ngặt:** Nếu bất kỳ bước nào trong chuỗi gặp lỗi (hết hạn, integrity, parser, runtime, validation, schema, grounding), pipeline phải dừng lại ngay lập tức và trả về lỗi an toàn có cấu trúc; tuyệt đối không thực thi các bước AI kế tiếp khi bước trước đó thất bại. Mọi lần chạy gặp lỗi đều cố gắng dọn dẹp file nguồn trên đĩa nếu tồn tại.
3. **Thực thi bắt buộc chính sách dọn dẹp nguồn APP-001:** Tuân thủ tuyệt đối hợp đồng lưu trữ của APP-001 ("file chỉ tồn tại cho pipeline/rendering cục bộ; xóa ngay sau khi downstream processing kết thúc"). Orchestrator bắt buộc thực hiện best-effort cleanup sau khi hoàn tất pipeline (thành công hoặc thất bại), không cung cấp cờ tùy chọn giữ file cho caller.
4. **Kiểm thử ngoại tuyến độc lập (Offline E2E Harness):** Hỗ trợ cơ chế Dependency Injection (qua typing Protocols) cho phép kiểm thử toàn bộ luồng điều phối nội bộ 100% offline, không phụ thuộc vào `OPENAI_API_KEY`, không gọi mạng và không tiêu tốn chi phí API.
5. **Giới hạn phạm vi rõ ràng:** APP-003 kết thúc tại **Validated Patent Description Draft JSON**. Không tích hợp xuất DOCX, không tạo public HTTP endpoint, và không đưa vào các hạ tầng ngoài phạm vi MVP.

---

## 2. Background & Lý do triển khai Internal Orchestration trước

Theo đặc tả kiến trúc tại [`docs/system-specification.md`](../system-specification.md), hệ thống dự kiến sẽ có các public API endpoints như `POST /api/documents/{id}/analyze` hoặc pipeline endpoint. Tuy nhiên:

1. **Rào cản BLK-003 vẫn đang mở:** Dự án chưa phê duyệt hạ tầng Authentication, Authorization, Tenant Isolation, Private Production Storage, và chính sách lưu trữ/xóa dữ liệu thực tế. Do đó, việc mở ra public HTTP pipeline endpoint tại thời điểm này là chưa an toàn và thiếu nền tảng quản trị truy cập.
2. **Đảm bảo tính toàn vẹn nghiệp vụ nội bộ:** Trước khi giải quyết các vấn đề về HTTP routing, background worker, hay database session, cần phải chứng minh bằng kiểm thử tự động rằng chuỗi liên kết các module nghiệp vụ nội bộ hoạt động chính xác, dữ liệu chuyển giao giữa các module không bị mất mát hay biến dạng, và cơ chế dọn dẹp bộ nhớ/tài nguyên hoạt động tin cậy.
3. **Tách biệt mối quan tâm (Separation of Concerns):** APP-003 tập trung thiết lập ranh giới điều phối dịch vụ nội bộ (service layer boundary), định nghĩa rõ thứ tự thực thi, cách bắt và bọc lỗi (error wrapping), cũng như quản trị vòng đời tài nguyên đĩa của tài liệu nguồn theo đúng hợp đồng APP-001.

---

## 3. Scope Boundaries

### 3.1 In Scope

- Xây dựng module điều phối nội bộ `backend/app/services/core_pipeline.py` với lớp `CorePipelineOrchestrator`.
- Nhận diện và phối hợp tuần tự 3 giai đoạn chính từ một tài liệu đã upload:
  - **Giai đoạn 1 (Preparation):** `DocumentPreparationService.prepare_extraction_input(document_id)` sinh `ExtractionInputEnvelope`. (Giai đoạn này sở hữu hoàn toàn việc lookup registry, mở lease, kiểm tra SHA-256 integrity, và parse PDF/DOCX).
  - **Giai đoạn 2 (Extraction):** `OpenAIExtractionRuntime.run_extraction(envelope)` sinh validated `Structured Invention Analysis`.
  - **Giai đoạn 3 (Draft Generation):** `OpenAIDraftRuntime.run_draft_generation(source_analysis, selected_title_candidate_id)` sinh validated `Patent Description Draft JSON`.
- Hỗ trợ tham số tùy chọn `selected_title_candidate_id: str | None = None` để truyền lựa chọn tiêu đề của tác giả vào giai đoạn soạn thảo.
- Hỗ trợ tham số tùy chọn `correlation_id: str | None = None` để cho phép caller truyền ID theo dõi hoặc tự sinh ngẫu nhiên nếu không có.
- **Bắt buộc dọn dẹp tài nguyên nguồn (Mandatory Best-Effort Source Cleanup):** Sau khi hoàn tất pipeline (thành công hoặc thất bại), orchestrator luôn thực hiện dọn dẹp file tạm trên đĩa qua `DocumentStorage.delete(document_id)`. Trong cấu hình ứng dụng chuẩn APP-001 (`on_removed=registry.remove`), việc xóa file thành công trên storage cũng tự động gỡ bỏ metadata khỏi registry.
- Định nghĩa kiểu kết quả chuẩn `PipelineResult` chứa `analysis: dict[str, Any]`, `draft: dict[str, Any]`, và `metadata: PipelineMetadata`.
- `PipelineMetadata` ghi nhận:
  - `document_id`: mã định danh UUID4 hex mờ 32 ký tự (`opaque 32-character UUID4 hex identifier`).
  - `correlation_id`: mã tương quan theo dõi.
  - `total_duration_ms`: tổng thời gian thực thi đo lường được (dữ liệu viễn thám / runtime observability).
  - `stages`: danh sách `PipelineStageMetadata` ghi nhận tên chặng, thời lượng, trạng thái, và provider request ID (nếu có).
  - `source_cleanup_performed: bool`: cờ phản ánh chính xác kết quả dọn dẹp (`True` nếu `DocumentStorage.delete` thành công; `False` nếu dọn dẹp thất bại/chưa xác nhận, kèm cảnh báo log và TTL 1 giờ làm chốt chặn an toàn).
- Định nghĩa phân loại lỗi điều phối `PipelineOrchestrationError` an toàn với 3 chặng chính: `"preparation"`, `"extraction"`, `"draft_generation"`. Bảo toàn mã lỗi chuẩn (`code`), thông điệp an toàn (`safe_message`), đường dẫn JSON Pointer (`paths`) và xâu chuỗi ngoại lệ gốc (`from exc`).
- Thiết kế Dependency Injection qua `typing.Protocol` cho các service con (`preparation_service`, `extraction_runtime`, `draft_runtime`) để phục vụ mock / fake trong kiểm thử.
- Ghi log vận hành an toàn (chỉ log metadata, timing, IDs; không log văn bản thô, prompt, payload, hoặc secret).
- Xây dựng bộ kiểm thử tích hợp ngoại tuyến `tests/backend/test_core_pipeline_e2e_offline.py` và kiểm thử đơn vị `tests/backend/test_core_pipeline.py` bao phủ toàn diện các kịch bản thành công và thất bại.

### 3.2 Out of Scope (Các hạng mục không triển khai)

- **Không cho phép tắt dọn dẹp nguồn (No Caller Source Retention):** Không cung cấp tham số `cleanup_source: bool = False` hay bất kỳ cơ chế nào cho phép caller bỏ qua việc dọn dẹp nguồn bắt buộc của APP-001.
- **Không tạo Public HTTP Endpoint:** Không tạo route mới tại `/api/documents/{id}/analyze`, `/api/documents/{id}/draft`, hay `/api/pipeline`.
- **Không tích hợp DOCX Rendering:** Không gọi `render_patent_docx_v1` hay sinh file DOCX trong APP-003.
- **Không bổ sung hạ tầng hàng đợi/worker:** Không dùng Celery, RQ, Redis, Kafka, hay async background job queue.
- **Không tích hợp Database:** Không dùng Supabase, PostgreSQL, SQLite, hay ORM persistence.
- **Không triển khai Auth/Tenant:** Không có JWT, API keys, user roles, hay multi-tenant storage (chờ giải quyết BLK-003).
- **Không có Frontend UI:** Không xây dựng giao diện người dùng Next.js hay web interface.
- **Không thay đổi AI Contracts:** Tuyệt đối không thay đổi JSON Schemas (`schemas/invention-output/`, `schemas/patent-draft/`) hay Prompts (`prompts/extraction/`, `prompts/draft-generation/`).
- **Không thay đổi Runtime Provider Policy:** Giữ nguyên cấu hình `gpt-5.6-sol`, reasoning `high`, `store=False`, không retrieval, timeout 180s cho extraction và 240s cho draft.
- **Không có Claims / Legal Advice:** Không sinh Claims, Draft Claims hay đánh giá khả năng cấp bằng sáng chế.
- **Không gọi Live API trong default test suite:** Bộ test mặc định tuyệt đối không yêu cầu `OPENAI_API_KEY` hay kết nối mạng.

---

## 4. Current Architecture Boundary & Existing Interfaces

Dựa trên việc kiểm tra trực tiếp mã nguồn trong repository, các interface hiện hành được cấu trúc như sau:

| Thành phần | File nguồn | Interface chính | Kiểu Input | Kiểu Output | Ngoại lệ chính |
|---|---|---|---|---|---|
| **Storage** | `backend/app/services/document_storage.py` | `DocumentStorage.lease(doc_id)`<br>`DocumentStorage.delete(doc_id)` | `document_id: str` | `Path` (context manager)<br>`bool` | `ValueError` (nếu ID không hợp lệ) |
| **Preparation** | `backend/app/services/document_parsing.py` | `DocumentPreparationService.prepare_extraction_input(doc_id)` | `document_id: str` | `ExtractionInputEnvelope` | `DocumentPreparationError` (`document_unknown`, `document_expired_or_missing`, `parse_failed`, `no_extractable_text`) |
| **Extraction Runtime** | `backend/app/services/extraction_runtime.py` | `OpenAIExtractionRuntime.run_extraction(envelope, correlation_id=...)` | `ExtractionInputEnvelope` | `ExtractionRuntimeResult` (`analysis`, `runtime`) | `ExtractionRuntimeError` (`provider_error`, `provider_timeout`, `schema_validation_failed`, `grounding_validation_failed`, ...) |
| **Draft Runtime** | `backend/app/services/draft_runtime.py` | `OpenAIDraftRuntime.run_draft_generation(source_analysis, selected_title_candidate_id=...)` | `source_analysis: dict`, `selected_title_candidate_id: str \| None` | `DraftRuntimeResult` (`draft`, `runtime`) | `DraftRuntimeError` (`provider_error`, `draft_schema_validation_failed`, `source_analysis_invalid`, `word_count_exceeded`, ...) |

> [!NOTE]
> Trong mô hình ứng dụng chuẩn APP-001 (`backend/app/main.py`), `DocumentStorage` được khởi tạo với tham số `on_removed=registry.remove`. Do đó, khi `DocumentStorage.delete(document_id)` xóa file thành công, bản ghi registry tương ứng cũng tự động được gỡ bỏ mà không cần orchestrator phải quản lý thêm một vòng đời registry độc lập.
>
> Ngoài ra, `DocumentPreparationService.prepare_extraction_input(document_id)` đã bao hàm toàn bộ việc kiểm tra đăng ký tài liệu (`registry.get`), mở lease, kiểm tra tồn tại của file trên đĩa, đối chiếu giá trị toàn vẹn SHA-256 (nếu không khớp sẽ raise `parse_failed`), và phân tích cú pháp. Do đó, orchestrator không thực hiện kiểm tra `DocumentRegistry.get` trùng lặp trước khi gọi `prepare_extraction_input`.

---

## 5. Proposed Orchestration Contract

### 5.1 Orchestrator Class Structure

Module đề xuất: `backend/app/services/core_pipeline.py`

```python
"""Internal Core Pipeline Orchestration Service for APP-003."""

from __future__ import annotations

import logging
import time
import uuid
from dataclasses import dataclass
from typing import Any, Protocol

from backend.app.schemas.analysis_input import ExtractionInputEnvelope
from backend.app.services.document_parsing import (
    DocumentPreparationError,
    DocumentPreparationService,
)
from backend.app.services.document_storage import DocumentStorage
from backend.app.services.draft_runtime import (
    DraftRuntimeError,
    DraftRuntimeResult,
    OpenAIDraftRuntime,
)
from backend.app.services.extraction_runtime import (
    ExtractionRuntimeError,
    ExtractionRuntimeResult,
    OpenAIExtractionRuntime,
)
```

### 5.2 Dependency Protocols (for Clean Injection & Mocking)

Nhằm phục vụ kiểm thử đơn vị và E2E không phụ thuộc mạng, orchestrator sử dụng protocols rõ ràng:

```python
class PreparationServiceProtocol(Protocol):
    def prepare_extraction_input(self, document_id: str) -> ExtractionInputEnvelope: ...

class ExtractionRuntimeProtocol(Protocol):
    def run_extraction(
        self,
        envelope: ExtractionInputEnvelope,
        *,
        correlation_id: str | None = None,
    ) -> ExtractionRuntimeResult: ...

class DraftRuntimeProtocol(Protocol):
    def run_draft_generation(
        self,
        source_analysis: dict[str, Any],
        selected_title_candidate_id: str | None = None,
    ) -> DraftRuntimeResult: ...
```

### 5.3 Data Types & Result Models

```python
@dataclass(frozen=True, slots=True)
class PipelineStageMetadata:
    stage: str  # "preparation" | "extraction" | "draft_generation"
    duration_ms: int  # Runtime observability telemetry
    status: str  # "completed"
    provider_request_id: str | None = None  # None for preparation; provider ID for extraction/draft
    usage: dict[str, int] | None = None

@dataclass(frozen=True, slots=True)
class PipelineMetadata:
    document_id: str  # Opaque 32-character UUID4 hex identifier
    correlation_id: str
    total_duration_ms: int  # Runtime observability telemetry
    stages: tuple[PipelineStageMetadata, ...]
    source_cleanup_performed: bool  # True if storage.delete succeeded; False if failed/unconfirmed

@dataclass(frozen=True, slots=True)
class PipelineResult:
    analysis: dict[str, Any]
    draft: dict[str, Any]
    metadata: PipelineMetadata
```

### 5.4 Error Model

Nhằm tránh tạo ra các lớp lỗi trừu tượng dư thừa, APP-003 định nghĩa một lớp lỗi duy nhất ở tầng điều phối:

```python
class PipelineOrchestrationError(RuntimeError):
    """Raised when any stage of the internal core pipeline fails."""

    def __init__(
        self,
        stage: str,
        code: str,
        message: str,
        *,
        document_id: str,
        correlation_id: str,
        paths: tuple[str, ...] = (),
    ) -> None:
        super().__init__(message)
        self.stage = stage
        self.code = code
        self.safe_message = message
        self.document_id = document_id
        self.correlation_id = correlation_id
        self.paths = paths
```

- `stage`: Nhận diện chính xác giai đoạn phát sinh lỗi: `"preparation"`, `"extraction"`, `"draft_generation"`.
- `code`: Giữ nguyên mã lỗi chuẩn từ service con (`DocumentPreparationError.code`, `ExtractionRuntimeError.code`, `DraftRuntimeError.code`).
- `paths`: Bảo toàn JSON Pointer paths nếu lỗi xuất phát từ schema/business validation.
- Chaining: Mọi lỗi từ service con đều được liên kết bằng `raise PipelineOrchestrationError(...) from exc`.

### 5.5 Orchestrator Interface

```python
class CorePipelineOrchestrator:
    """Internal sequential orchestrator coordinating preparation, extraction, draft, and cleanup."""

    def __init__(
        self,
        storage: DocumentStorage,
        preparation_service: PreparationServiceProtocol,
        extraction_runtime: ExtractionRuntimeProtocol,
        draft_runtime: DraftRuntimeProtocol,
    ) -> None:
        self.storage = storage
        self.preparation_service = preparation_service
        self.extraction_runtime = extraction_runtime
        self.draft_runtime = draft_runtime

    def run_pipeline(
        self,
        document_id: str,
        *,
        selected_title_candidate_id: str | None = None,
        correlation_id: str | None = None,
    ) -> PipelineResult:
        ...
```

---

## 6. Component Sequence & Step-by-Step Execution

Luồng thực thi bên trong `CorePipelineOrchestrator.run_pipeline()` tuân thủ nghiêm ngặt chuỗi tuần tự và cơ chế fail-closed:

```text
[Start]
   │
   ▼
[Stage 1: Document Preparation (APP-002)]
   │── Document unknown, missing, SHA mismatch, or parse error? ──► [Fail: stage='preparation', code=exc.code] (Cleanup attempt)
   ▼
[Stage 2: Extraction Runtime (AI-RUNTIME-001)]
   │── Provider timeout, refusal, schema, or grounding error? ──► [Fail: stage='extraction', code=exc.code] (Cleanup attempt)
   ▼
[Stage 3: Draft Generation Runtime (AI-RUNTIME-002)]
   │── Schema invalid, word count exceeded, or business error? ──► [Fail: stage='draft_generation', code=exc.code] (Cleanup attempt)
   ▼
[Mandatory Best-Effort Source Cleanup & Result Assembly]
   │── Execute DocumentStorage.delete(document_id)
   │── If False: log warning, source_cleanup_performed=False, TTL fallback
   │── If True: source_cleanup_performed=True
   ▼
[Return PipelineResult]
```

### Chi tiết các bước thực hiện:

1. **Khởi tạo và Chuẩn bị dữ liệu tài liệu (Stage 1: Preparation - APP-002):**
   - Xác định `correlation_id`: nếu caller không cung cấp, sinh mới bằng `uuid.uuid4().hex`.
   - Bắt đầu đo thời gian chặng `preparation`.
   - Gọi `self.preparation_service.prepare_extraction_input(document_id)`.
   - `DocumentPreparationService` tự quản lý việc kiểm tra sự tồn tại trong registry (`document_unknown`), mở lease, kiểm tra file trên đĩa (`document_expired_or_missing`), kiểm tra tính toàn vẹn SHA-256 (`parse_failed`), parse nội dung, và kiểm tra văn bản trích xuất được (`no_extractable_text`).
   - Nếu phát sinh `DocumentPreparationError`, bắt ngoại lệ, cố gắng thực hiện dọn dẹp file nguồn qua `self.storage.delete(document_id)`, ghi log lỗi an toàn, và raise `PipelineOrchestrationError(stage="preparation", code=exc.code, document_id=document_id, correlation_id=correlation_id) from exc`.
   - Kết thúc chặng preparation thành công, nhận về đối tượng `ExtractionInputEnvelope`.

2. **Trích xuất thông tin sáng chế (Stage 2: Extraction - AI-RUNTIME-001):**
   - Bắt đầu đo thời gian chặng `extraction`.
   - Gọi `self.extraction_runtime.run_extraction(envelope, correlation_id=correlation_id)`.
   - Service thực hiện chuyển đổi provider schema, gọi mô hình (hoặc fake), normalize, kiểm tra canonical schema và grounding validation.
   - Nhận về `ExtractionRuntimeResult` chứa `analysis` hợp lệ và `runtime` metadata.
   - Nếu phát sinh `ExtractionRuntimeError`, bắt ngoại lệ, thực hiện dọn dẹp file nguồn qua `self.storage.delete(document_id)`, ghi log lỗi, và raise `PipelineOrchestrationError(stage="extraction", code=exc.code, document_id=document_id, correlation_id=correlation_id, paths=exc.paths) from exc`.
   - **Quy tắc bất biến:** Tuyệt đối KHÔNG gọi chặng draft nếu chặng extraction gặp bất kỳ lỗi nào.

3. **Soạn thảo mô tả bằng sáng chế (Stage 3: Draft Generation - AI-RUNTIME-002):**
   - Bắt đầu đo thời gian chặng `draft_generation`.
   - Gọi `self.draft_runtime.run_draft_generation(source_analysis=extraction_result.analysis, selected_title_candidate_id=selected_title_candidate_id)`.
   - Service tạo `AI-003 Draft Input Envelope`, sinh draft provider schema, gọi mô hình (hoặc fake), normalize, kiểm tra canonical draft schema và business rules.
   - Nhận về `DraftRuntimeResult` chứa `draft` hợp lệ và `runtime` metadata.
   - Nếu phát sinh `DraftRuntimeError`, bắt ngoại lệ, thực hiện dọn dẹp file nguồn qua `self.storage.delete(document_id)`, ghi log lỗi, và raise `PipelineOrchestrationError(stage="draft_generation", code=exc.code, document_id=document_id, correlation_id=correlation_id, paths=exc.paths) from exc`.

4. **Dọn dẹp tài nguyên bắt buộc & Đóng gói kết quả (Mandatory Source Cleanup & Result Assembly):**
   - Luôn thực hiện gọi `cleanup_ok = self.storage.delete(document_id)`.
   - Nếu `cleanup_ok` là `True`: ghi nhận `source_cleanup_performed = True`.
   - Nếu `cleanup_ok` là `False` (do file đã bị xóa, đang có active lease khác, hoặc lỗi I/O đĩa): ghi log cảnh báo mức `WARNING` (`document_cleanup_failed document_id=%s`), ghi nhận `source_cleanup_performed = False`. Quá trình dọn dẹp thất bại KHÔNG làm hỏng hay thay đổi trạng thái thành công của kết quả nghiệp vụ đã hoàn tất; cơ chế quét dọn TTL 1 giờ tự động của APP-001 tiếp tục là chốt chặn an toàn dự phòng.
   - Tổng hợp `PipelineStageMetadata` cho từng chặng (thời gian, status, provider_request_id, token usage).
   - Đóng gói và trả về đối tượng `PipelineResult`.

---

## 7. Storage Lifecycle & Mandatory Cleanup Rules

APP-003 tuân thủ và đồng bộ tuyệt đối với hợp đồng quản lý lưu trữ của APP-001:

1. **Thời điểm tài liệu sẵn sàng:** File upload và bản ghi metadata trở nên sẵn sàng ngay sau khi endpoint `POST /api/documents` (APP-001) hoàn tất xác thực ban đầu.
2. **Quyền đọc file:** `DocumentPreparationService` (APP-002) là thành phần duy nhất đọc trực tiếp file từ đĩa, và việc này bắt buộc phải diễn ra bên trong khối `with storage.lease(document_id):`.
3. **Độc lập sau bước Preparation:** Sau khi `ExtractionInputEnvelope` được tạo thành công ở Giai đoạn 1, toàn bộ nội dung cần thiết đã được nạp vào bộ nhớ dưới dạng các `SourceUnit`. Cả AI-RUNTIME-001 và AI-RUNTIME-002 đều không cần truy cập lại file trên đĩa.
4. **Chính sách dọn dẹp bắt buộc (Mandatory Source Cleanup Policy):**
   - Theo đặc tả hợp đồng APP-001: *"file chỉ tồn tại cho pipeline/rendering cục bộ; xóa ngay sau khi downstream processing kết thúc."*
   - Do đó, APP-003 bắt buộc kích hoạt dọn dẹp file nguồn ngay sau khi quá trình điều phối kết thúc, không cho phép caller can thiệp giữ lại tài liệu.
   - **Khi pipeline thành công:** File đĩa được dọn dẹp ngay tại Bước 4.
   - **Khi pipeline thất bại:** File đĩa được dọn dẹp ngay trong khối xử lý lỗi của chặng tương ứng.
5. **Xử lý sự cố dọn dẹp (Cleanup Failure Semantics):**
   - Nếu pipeline thành công nhưng việc dọn dẹp file đĩa thất bại: bảo toàn kết quả nghiệp vụ `analysis` và `draft`, ghi log cảnh báo an toàn, ghi nhận `source_cleanup_performed = False`, và để cơ chế TTL sweep dọn dẹp sau.
   - Nếu pipeline thất bại và việc dọn dẹp file cũng thất bại: bảo toàn ngoại lệ nghiệp vụ gốc (`PipelineOrchestrationError`), không thay thế bằng lỗi dọn dẹp, ghi log cảnh báo an toàn, và để TTL sweep dọn dẹp sau.
6. **Cơ chế Registry Cleanup liên kết:** Trong mô hình chuẩn của ứng dụng (`backend/app/main.py`), `DocumentStorage` được khởi tạo với `on_removed=registry.remove`. Do đó, mỗi khi `DocumentStorage.delete` xóa file thành công, bản ghi registry cũng đồng thời được dọn dẹp.
7. **Không lưu trữ vĩnh viễn:** Tuyệt đối không lưu trữ tài liệu nghiên cứu vô thời hạn. Bộ quét TTL (`DocumentStorage.sweep_expired()`) tiếp tục là chốt chặn an toàn cho mọi tài liệu tồn tại quá 60 phút.

---

## 8. Retry & Provider Policy

1. **Không có Retry ở tầng Orchestrator:** `CorePipelineOrchestrator` không tự động retry bất kỳ lệnh gọi mô hình hay parsing nào. Mọi lỗi đều fail-closed ngay lập tức.
2. **Bảo toàn cơ chế Retry của Provider:** Cơ chế retry duy nhất được phép là retry ở tầng transport do OpenAI SDK quản lý (`max_retries=2`), đã được đóng gói bên trong AI-RUNTIME-001 và AI-RUNTIME-002.
3. **Không dùng Repair Prompts:** Không gọi prompt sửa lỗi, không gọi fallback model, không tự ý nới lỏng schema.

---

## 9. Logging & Privacy Rules

Nhằm tuân thủ nguyên tắc bảo mật và quản trị dữ liệu nghiên cứu chưa công bố:

### Dữ liệu ĐƯỢC PHÉP log:
- `correlation_id`
- `document_id`: mã định danh UUID4 hex mờ 32 ký tự (`opaque 32-character UUID4 hex identifier`)
- Tên chặng thực thi: `stage="preparation"`, `stage="extraction"`, `stage="draft_generation"`
- Trạng thái chặng: `status="started"`, `status="completed"`, `status="failed"`
- Thời gian thực thi chặng: `duration_ms` (telemetry)
- Mã lỗi an toàn: `code` (ví dụ: `document_unknown`, `schema_validation_failed`)
- Provider request ID (ví dụ: `resp_12345`)
- Token usage metadata: `input_tokens`, `output_tokens`, `total_tokens`

### Dữ liệu TUYỆT ĐỐI KHÔNG ĐƯỢC log:
- Nội dung văn bản thô của bài báo nghiên cứu.
- Trích đoạn bằng chứng (`evidence excerpt`).
- Toàn văn `ExtractionInputEnvelope` hay `source_units`.
- Toàn văn kết quả `Structured Invention Analysis` hay `Patent Description Draft`.
- Nội dung câu lệnh nhắc (`prompt`).
- Request / Response payload thô từ OpenAI Responses API.
- Khóa bảo mật (`OPENAI_API_KEY`), Bearer token, Header authorization.
- Đường dẫn tuyệt đối của hệ thống file cục bộ.
- Dấu vết stack trace chứa nội dung chuỗi trích dẫn tài liệu.

---

## 10. Offline E2E Harness Strategy & Test Doubles

Để đảm bảo khả năng kiểm thử toàn diện, lặp lại được, chạy nhanh và độc lập với API key, một bộ test harness chuyên dụng sẽ được xây dựng tại `tests/backend/test_core_pipeline_e2e_offline.py`.

### 10.1 Fake Runtimes Architecture

Mở rộng từ mẫu `FakeResponses` và `FakeClient` hiện có trong `tests/backend/runtime_test_support.py`:

```python
class FakeExtractionRuntime:
    """Deterministic, configurable fake extraction runtime for offline E2E tests."""
    def __init__(
        self,
        analysis_result: dict[str, Any] | None = None,
        error: Exception | None = None,
    ) -> None:
        self.analysis_result = analysis_result
        self.error = error
        self.invocations: list[ExtractionInputEnvelope] = []

    def run_extraction(
        self,
        envelope: ExtractionInputEnvelope,
        *,
        correlation_id: str | None = None,
    ) -> ExtractionRuntimeResult:
        self.invocations.append(envelope)
        if self.error is not None:
            raise self.error
        return ExtractionRuntimeResult(
            analysis=self.analysis_result or {},
            runtime=ExtractionRuntimeMetadata(
                provider="fake_openai",
                model="gpt-5.6-sol",
                request_id="fake_req_extract_001",
                status="completed",
                duration_ms=15,
                usage={"input_tokens": 100, "output_tokens": 200, "total_tokens": 300},
            ),
        )

class FakeDraftRuntime:
    """Deterministic, configurable fake draft runtime for offline E2E tests."""
    def __init__(
        self,
        draft_result: dict[str, Any] | None = None,
        error: Exception | None = None,
    ) -> None:
        self.draft_result = draft_result
        self.error = error
        self.invocations: list[tuple[dict[str, Any], str | None]] = []

    def run_draft_generation(
        self,
        source_analysis: dict[str, Any],
        selected_title_candidate_id: str | None = None,
    ) -> DraftRuntimeResult:
        self.invocations.append((source_analysis, selected_title_candidate_id))
        if self.error is not None:
            raise self.error
        return DraftRuntimeResult(
            draft=self.draft_result or {},
            runtime=DraftRuntimeMetadata(
                provider="fake_openai",
                model="gpt-5.6-sol",
                request_id="fake_req_draft_001",
                status="completed",
                duration_ms=25,
                usage={"input_tokens": 200, "output_tokens": 400, "total_tokens": 600},
            ),
        )
```

---

## 11. Acceptance Criteria Matrix

| AC ID | Yêu cầu kiểm chứng | Phương pháp kiểm chứng | Kết quả kỳ vọng | Bằng chứng kiểm thử |
|---|---|---|---|---|
| **AC-01** | Khởi tạo Orchestrator thành công với cấu hình chuẩn | Unit Test | Đối tượng khởi tạo đầy đủ dependencies mà không đòi hỏi DocumentRegistry trực tiếp | `CorePipelineOrchestrator` instantiated |
| **AC-02** | Thành công trọn vẹn luồng PDF với Fake Runtimes | Offline E2E Test | Trả về `PipelineResult` đầy đủ `analysis`, `draft`, và `metadata`; `source_cleanup_performed=True` | 3 chặng hoàn tất, status="completed" |
| **AC-03** | Thành công trọn vẹn luồng DOCX với Fake Runtimes | Offline E2E Test | Trả về `PipelineResult` chính xác từ file DOCX hợp lệ; file đĩa được dọn dẹp | 3 chặng hoàn tất, dữ liệu nhất quán |
| **AC-04** | Thứ tự thực thi các chặng tuân thủ nghiêm ngặt | Mock/Spy Test | Thứ tự gọi chính xác: Preparation → Extraction → Draft → Cleanup | Thứ tự calls được ghi lại khớp 100% |
| **AC-05** | Dữ liệu `ExtractionInputEnvelope` được chuyển giao chính xác | Contract Test | Envelope từ Preparation được truyền nguyên vẹn vào Extraction | `envelope.document_metadata.sha256` khớp |
| **AC-06** | Dữ liệu `analysis` được chuyển giao chính xác vào Draft | Contract Test | `analysis` từ Extraction được truyền nguyên vẹn vào Draft | `source_analysis` nhận được khớp chính xác |
| **AC-07** | Tham số `selected_title_candidate_id` được truyền chính xác | Feature Test | Giá trị ID tiêu đề được chuyển vào Draft Runtime | `draft_runtime.invocations` ghi nhận đúng ID |
| **AC-08** | Lỗi tài liệu chưa đăng ký hoặc không tìm thấy fail-closed an toàn | Error Test | Ném `PipelineOrchestrationError` (stage="preparation", code="document_unknown") | Không gọi AI runtimes |
| **AC-09** | Tài liệu hết hạn hoặc bị xóa trên đĩa fail-closed | Error Test | Ném `PipelineOrchestrationError` (stage="preparation", code="document_expired_or_missing") | Không gọi AI runtimes |
| **AC-10** | Lỗi sai lệch SHA-256 (integrity check) fail-closed | Error Test | Ném `PipelineOrchestrationError` (stage="preparation", code="parse_failed") | Không gọi AI runtimes |
| **AC-11** | Tài liệu không có chữ (no extractable text) fail-closed | Error Test | Ném `PipelineOrchestrationError` (stage="preparation", code="no_extractable_text") | Không gọi AI runtimes |
| **AC-12** | Lỗi Extraction Provider (timeout/error) fail-closed | Error Test | Ném `PipelineOrchestrationError` (stage="extraction", code="provider_timeout") | Draft Runtime KHÔNG ĐƯỢC GỌI |
| **AC-13** | Lỗi Extraction Canonical Schema Validation fail-closed | Error Test | Ném `PipelineOrchestrationError` (stage="extraction", code="schema_validation_failed") | Draft Runtime KHÔNG ĐƯỢC GỌI |
| **AC-14** | Lỗi Extraction Grounding Validation fail-closed | Error Test | Ném `PipelineOrchestrationError` (stage="extraction", code="grounding_validation_failed") | Draft Runtime KHÔNG ĐƯỢC GỌI |
| **AC-15** | Lỗi Draft Provider (connection/error) fail-closed | Error Test | Ném `PipelineOrchestrationError` (stage="draft_generation", code="provider_connection") | Pipeline báo lỗi, không trả kết quả draft |
| **AC-16** | Lỗi Draft Canonical Schema Validation fail-closed | Error Test | Ném `PipelineOrchestrationError` (stage="draft_generation", code="draft_schema_validation_failed") | Pipeline báo lỗi |
| **AC-17** | Lỗi Draft Business Validation (word count, legal) fail-closed | Error Test | Ném `PipelineOrchestrationError` (stage="draft_generation", code="word_count_exceeded") | Pipeline báo lỗi |
| **AC-18** | Bắt buộc dọn dẹp tài nguyên sau khi pipeline hoàn tất thành công | Lifecycle Test | File trên đĩa bị xóa sau khi hoàn tất; `source_cleanup_performed=True` | `storage.path_for(doc_id).exists() == False` |
| **AC-19** | Bắt buộc dọn dẹp tài nguyên khi pipeline thất bại ở bất kỳ chặng nào | Lifecycle Test | File bị xóa ngay cả khi pipeline gặp lỗi ở giữa chặng | File được xóa an toàn trong error handler |
| **AC-20** | Ràng buộc hợp đồng: Caller không thể vô hiệu hóa dọn dẹp nguồn APP-001 | Contract Guard | Không có tham số `cleanup_source` hay switch bỏ qua dọn dẹp trong interface orchestrator | Chữ ký phương thức `run_pipeline` không có cờ bỏ qua cleanup |
| **AC-21** | Lỗi khi cleanup không làm đè lỗi chính hay làm hỏng payload thành công | Robustness Test | `storage.delete` gặp lỗi hoặc trả `False` vẫn bảo toàn kết quả; `source_cleanup_performed=False` | Log WARNING xuất hiện, không ném lỗi xóa file |
| **AC-22** | Không gọi mạng bên ngoài trong default test suite | Network Guard | Chạy toàn bộ test suite khi ngắt mạng hoặc không có API key | Toàn bộ offline test suite PASS |
| **AC-23** | Không yêu cầu `OPENAI_API_KEY` trong môi trường test | Config Guard | Chạy test khi `$env:OPENAI_API_KEY=""` | Toàn bộ offline test suite PASS |
| **AC-24** | Số lần gọi Fake Extraction Runtime hoàn toàn tất định | Determinism Test | Chính xác 1 lần gọi cho mỗi pipeline run hợp lệ | `len(fake_extraction.invocations) == 1` |
| **AC-25** | Số lần gọi Fake Draft Runtime hoàn toàn tất định | Determinism Test | Chính xác 1 lần gọi cho mỗi pipeline run hợp lệ | `len(fake_draft.invocations) == 1` |
| **AC-26** | Tính tất định của luồng điều phối nghiệp vụ và bàn giao dữ liệu | Determinism Test | Với input cố định và fake runtimes tất định, thứ tự gọi, số lần gọi, envelope, analysis và draft payload là giống hệt nhau qua các lần chạy lặp lại; các trường dữ liệu viễn thám thời gian (`duration_ms`, `total_duration_ms`) và ID sinh ngẫu nhiên (`correlation_id`, `provider_request_id`) được loại trừ rõ ràng khỏi phép so sánh bằng nhau tuyệt đối | So sánh cấu trúc và nội dung nghiệp vụ PASS |
| **AC-27** | Bảo vệ quyền riêng tư trong log và thông điệp lỗi | Privacy Guard | Error message và log không chứa raw text, prompts, hay secrets | Scan log output không có dữ liệu nhạy cảm |
| **AC-28** | Không làm biến dạng hay trôi hợp đồng của AI-001/AI-002/AI-003 | Contract Guard | Dữ liệu output tuân thủ 100% JSON Schema Draft 2020-12 | Canonical validators kiểm tra đều PASS |
| **AC-29** | Không có Public HTTP Endpoint nào được tạo ra | Scope Guard | Kiểm tra routing table của FastAPI app | Chỉ có `GET /health` và `POST /api/documents` |
| **AC-30** | Không thêm thư viện phụ thuộc mới | Dependency Guard | `requirements.txt` không thay đổi; `pip check` PASS | Không thêm package ngoài |
| **AC-31** | Không thay đổi chính sách mô hình AI | Policy Guard | Giữ nguyên `gpt-5.6-sol`, reasoning `high`, `store=False` | Settings không bị thay đổi |
| **AC-32** | Không phát sinh lỗi hoặc hỏng hóc hồi quy bất thường trong các bộ kiểm thử hiện có | Regression Test | Chạy toàn bộ test suites hiện tại của repository; zero unexpected failures/errors; chỉ cho phép các intentional skips đã được ghi nhận trước đó | Regression suites PASS |

---

## 12. Proposed Implementation Files

Khi bước vào Phase Implementation (nhiệm vụ kỹ thuật tương lai được Human phê duyệt), các file dự kiến được tạo hoặc cập nhật gồm:

1. **Production Code:**
   - `backend/app/services/core_pipeline.py`: Chứa `CorePipelineOrchestrator`, `PipelineResult`, `PipelineMetadata`, `PipelineStageMetadata`, và `PipelineOrchestrationError`.
2. **Test Suites:**
   - `tests/backend/test_core_pipeline.py`: Unit tests cho orchestrator logic, error wrapping, và mandatory cleanup lifecycle.
   - `tests/backend/test_core_pipeline_e2e_offline.py`: E2E integration tests với synthetic fixtures, PDF/DOCX input thực tế trên đĩa, kết hợp fake runtimes.

*(Lưu ý: Không thay đổi `backend/app/main.py` trong APP-003 vì không có public HTTP endpoint mới; việc tích hợp ứng dụng ở tầng HTTP thuộc về task được Human phê duyệt riêng trong tương lai).*

---

## 13. Regression Validation Plan

Trong giai đoạn implementation tiếp theo, agent thực hiện bắt buộc phải chạy kế hoạch kiểm thử tự động sau:

```powershell
$env:PYTHONDONTWRITEBYTECODE="1"

# 1. Toàn bộ test suite schema hiện có
.\.venv\Scripts\python.exe -m unittest discover -s tests/schema -p "test_*.py" -v

# 2. Toàn bộ test suite prompt hiện có
.\.venv\Scripts\python.exe -m unittest discover -s tests/prompt -p "test_*.py" -v

# 3. Toàn bộ test suite draft contract hiện có
.\.venv\Scripts\python.exe -m unittest discover -s tests/draft -p "test_*.py" -v

# 4. Toàn bộ test suite docx template hiện có
.\.venv\Scripts\python.exe -m unittest discover -s tests/docx -p "test_*.py" -v

# 5. Toàn bộ backend test suite (bao gồm APP-001, APP-002, AI-RUNTIME-001, AI-RUNTIME-002 và APP-003 mới)
C:\Python314\python.exe -m pytest tests/backend/

# 6. Kiểm tra tính toàn vẹn phụ thuộc
.\.venv\Scripts\python.exe -m pip check

# 7. Kiểm tra định dạng và khoảng trắng
git diff --check
```

---

## 14. Risks & Mitigations

| Rủi ro | Mức độ | Biện pháp giảm thiểu |
|---|---|---|
| **Rò rỉ dữ liệu nghiên cứu chưa công bố** | Critical | Chỉ dùng synthetic fixtures cho testing; bắt buộc dọn dẹp file nguồn ngay sau khi chạy; không log payload, prompt, hay text; BLK-003 vẫn mở ngăn chặn production usage. |
| **Xung đột bộ nhớ / Disk lock trên Windows** | Medium | Sử dụng `storage.lease()` chuẩn trong APP-002; bắt buộc gọi `storage.delete()` sau khi lease đã giải phóng; xử lý an toàn lỗi I/O để bảo toàn kết quả và để TTL sweep dọn dẹp sau. |
| **Lệch pha dữ liệu giữa Extraction và Draft** | High | Tận dụng chính xác `build_draft_input_envelope` và các validator chuẩn đã được kiểm chứng của AI-RUNTIME-002. |
| **Vô tình kích hoạt gọi API tốn phí** | High | Default E2E harness sử dụng Fake Runtimes; live smoke test được tách biệt hoàn toàn và yêu cầu cờ môi trường riêng. |

---

## 15. Human Decisions

| Quyết định | Trạng thái hiện tại | Ghi chú |
|---|---|---|
| **Scope & Boundaries của APP-003** | Khuyến nghị phê duyệt theo đặc tả remediated này | Dừng lại ở Validated Draft JSON; không mở public endpoint, không render DOCX, dọn dẹp file nguồn bắt buộc theo APP-001. |
| **Chính sách dọn dẹp file nguồn** | Đã định đoạt bởi hợp đồng APP-001 | Bắt buộc dọn dẹp sau khi pipeline kết thúc; không cần Human decision mới. |
| **Quyết định kiến trúc mới** | Không yêu cầu ADR mới | Kế thừa trọn vẹn ADR-001 đến ADR-010. |
| **Phê duyệt đặc tả sau Re-review** | Chờ Human / Product Owner quyết định | Yêu cầu kết quả independent re-review từ Gemini 3.1 Pro High trước khi Human phê duyệt. |

---

## 16. Definition of Done (DoD) cho Specification

Đặc tả APP-003 được coi là hoàn tất khi:
- [x] Tài liệu đặc tả `docs/tasks/APP-003-core-pipeline-orchestration.md` được remediate đầy đủ các phát hiện review.
- [x] Xung đột chính sách dọn dẹp nguồn được giải quyết triệt để, đồng bộ với APP-001 (mandatory cleanup, không có `cleanup_source` parameter).
- [x] Tính tất định trong AC-26 được chuẩn hóa cho dữ liệu nghiệp vụ, loại trừ dữ liệu viễn thám thời gian.
- [x] Loại bỏ đề xuất sửa đổi không cần thiết đối với `backend/app/main.py`.
- [x] Không sửa đổi bất kỳ file mã nguồn backend, schema, prompt, fixture, template, hay test nào.
- [x] Trạng thái nhiệm vụ được cập nhật chính xác trong tài liệu quản trị: `Specification — Remediated — Awaiting Independent Re-review`.
- [x] Không tuyên bố Phase 1, Phase 2, hay MVP hoàn thành.
- [x] `git diff --check` đạt kết quả sạch (clean).
- [x] Nhánh `docs/app-003-core-pipeline-orchestration-spec` được push lên remote repository.

---

## 17. Handoff Expectations

```text
Task ID: APP-003
Agent: Gemini 3.8 Flash High
Reviewer: Gemini 3.1 Pro High + Human / Product Owner
Status: Specification — Remediated — Awaiting Independent Re-review
Version: Specification 1.1.0
Work completed: Remediated APP-003 core pipeline orchestration specification after independent review: aligned source cleanup contract with APP-001 (mandatory cleanup, removed cleanup_source parameter), removed redundant registry lookup, refined determinism contract (AC-26) to exclude volatile observability telemetry, corrected document_id terminology to opaque 32-character UUID4 hex, refined regression contract (AC-32), and removed speculative main.py modification.
Files affected: docs/tasks/APP-003-core-pipeline-orchestration.md; docs/operations/01_PROJECT_CONTROL_CENTER.md; PROJECT_CONTEXT.md; README.md.
Evidence checked: Git branch, status, diff check PASS; zero production code, tests, or schemas modified.
Findings: All findings from independent review addressed; fully consistent with APP-001/002, ADR-001 through ADR-010.
Decisions: Human specification approval pending independent re-review by Gemini 3.1 Pro High.
Issues: BLK-003 remains open; live provider smoke remains deferred due to lack of API funding.
Security impact: Mandatory cleanup mitigates disk retention risk; no credentials, PII or research content exposed.
Recommended next action: Independent re-review by Gemini 3.1 Pro High before Human approval and implementation scheduling.
```
