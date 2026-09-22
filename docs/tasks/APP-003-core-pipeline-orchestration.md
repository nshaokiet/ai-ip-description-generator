# APP-003 — Internal Core Pipeline Orchestration and Offline E2E Harness

## Metadata

| Thuộc tính | Giá trị |
|---|---|
| Task ID | APP-003 |
| Document title | APP-003 — Internal Core Pipeline Orchestration and Offline E2E Harness Specification |
| Specification version | 1.0.0 |
| Status | Specification — Awaiting Independent Review |
| Owner | ChatGPT/Codex |
| Author | Gemini 3.8 Flash High |
| Reviewer | Gemini 3.1 Pro High + Human / Product Owner |
| Human specification approval | Pending independent review |
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
```

Mục tiêu cốt lõi:
1. **Liên kết tuần tự, nhất quán và chặt chẽ:** Kết nối các tầng xử lý nội bộ mà không làm thay đổi hay làm sai lệch hợp đồng dữ liệu chuẩn (**canonical contracts**) của AI-001, AI-002, AI-003, APP-001, APP-002, AI-RUNTIME-001, và AI-RUNTIME-002.
2. **Fail-closed nghiêm ngặt:** Nếu bất kỳ bước nào trong chuỗi gặp lỗi (lỗi lookup, hết hạn, integrity, parser, runtime, validation, schema, grounding), pipeline phải dừng lại ngay lập tức và trả về lỗi an toàn có cấu trúc; tuyệt đối không thực thi các bước AI kế tiếp khi bước trước đó thất bại.
3. **Kiểm thử ngoại tuyến độc lập (Offline E2E Harness):** Hỗ trợ cơ chế Dependency Injection (hoặc test doubles) cho phép kiểm thử toàn bộ luồng điều phối nội bộ 100% offline, không phụ thuộc vào `OPENAI_API_KEY`, không gọi mạng và không tiêu tốn chi phí API.
4. **Giới hạn phạm vi rõ ràng:** APP-003 kết thúc tại **Validated Patent Description Draft JSON**. Không tích hợp xuất DOCX, không tạo public HTTP endpoint, và không đưa vào các hạ tầng ngoài phạm vi MVP.

---

## 2. Background & Lý do triển khai Internal Orchestration trước

Theo đặc tả kiến trúc tại [`docs/system-specification.md`](../system-specification.md), hệ thống dự kiến sẽ có các public API endpoints như `POST /api/documents/{id}/analyze` hoặc pipeline endpoint. Tuy nhiên:

1. **Rào cản BLK-003 vẫn đang mở:** Dự án chưa phê duyệt hạ tầng Authentication, Authorization, Tenant Isolation, Private Production Storage, và chính sách lưu trữ/xóa dữ liệu thực tế. Do đó, việc mở ra public HTTP pipeline endpoint tại thời điểm này là chưa an toàn và thiếu nền tảng quản trị truy cập.
2. **Đảm bảo tính toàn vẹn nghiệp vụ nội bộ:** Trước khi giải quyết các vấn đề về HTTP routing, background worker, hay database session, cần phải chứng minh bằng kiểm thử tự động rằng chuỗi liên kết các module nghiệp vụ nội bộ hoạt động chính xác, dữ liệu chuyển giao giữa các module không bị mất mát hay biến dạng, và cơ chế dọn dẹp bộ nhớ/tài nguyên hoạt động tin cậy.
3. **Tách biệt mối quan tâm (Separation of Concerns):** APP-003 tập trung thiết lập ranh giới điều phối dịch vụ nội bộ (service layer boundary), định nghĩa rõ thứ tự thực thi, cách bắt và bọc lỗi (error wrapping), cũng như vòng đời tài nguyên đĩa của tài liệu nguồn.

---

## 3. Scope Boundaries

### 3.1 In Scope

- Xây dựng module điều phối nội bộ `backend/app/services/core_pipeline.py` với lớp `CorePipelineOrchestrator`.
- Nhận diện và phối hợp tuần tự 3 giai đoạn chính từ một tài liệu đã upload:
  - **Giai đoạn 1 (Preparation):** `DocumentPreparationService.prepare_extraction_input(document_id)` sinh `ExtractionInputEnvelope`.
  - **Giai đoạn 2 (Extraction):** `OpenAIExtractionRuntime.run_extraction(envelope)` sinh validated `Structured Invention Analysis`.
  - **Giai đoạn 3 (Draft Generation):** `OpenAIDraftRuntime.run_draft_generation(source_analysis, selected_title_candidate_id)` sinh validated `Patent Description Draft JSON`.
- Hỗ trợ tham số tùy chọn `selected_title_candidate_id: str | None = None` để truyền lựa chọn tiêu đề của tác giả vào giai đoạn soạn thảo.
- Quản lý vòng đời tài liệu nguồn trên đĩa: cung cấp cờ tùy chọn `cleanup_source: bool = False` cho phép dọn dẹp file tạm và bản ghi registry qua `DocumentStorage.delete(document_id)` sau khi hoàn tất hoặc khi có lỗi.
- Định nghĩa kiểu kết quả chuẩn `PipelineResult` chứa `analysis: dict[str, Any]`, `draft: dict[str, Any]`, và `metadata: PipelineMetadata` (chứa thời gian thực thi từng chặng, correlation ID, document ID).
- Định nghĩa phân loại lỗi điều phối `PipelineOrchestrationError` an toàn, xác định rõ chặng thất bại (`stage`), mã lỗi (`code`), thông điệp an toàn (`safe_message`) và xâu chuỗi ngoại lệ gốc (`from exc`).
- Thiết kế Dependency Injection cho các service con (`preparation_service`, `extraction_runtime`, `draft_runtime`) để phục vụ mock / fake trong kiểm thử.
- Ghi log vận hành an toàn (chỉ log metadata, timing, IDs; không log văn bản thô, prompt, payload, hoặc secret).
- Xây dựng bộ kiểm thử tích hợp ngoại tuyến `tests/backend/test_core_pipeline_e2e_offline.py` bao phủ toàn diện các kịch bản thành công và thất bại.

### 3.2 Out of Scope (Các hạng mục không triển khai)

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
| **Registry** | `backend/app/services/document_registry.py` | `DocumentRegistry.get(doc_id)`<br>`DocumentRegistry.remove(doc_id)` | `document_id: str` | `DocumentRecord \| None`<br>`bool` | Không |
| **Preparation** | `backend/app/services/document_parsing.py` | `DocumentPreparationService.prepare_extraction_input(doc_id)` | `document_id: str` | `ExtractionInputEnvelope` | `DocumentPreparationError` (`document_unknown`, `document_expired_or_missing`, `parse_failed`, `no_extractable_text`) |
| **Extraction Runtime** | `backend/app/services/extraction_runtime.py` | `OpenAIExtractionRuntime.run_extraction(envelope, correlation_id=...)` | `ExtractionInputEnvelope` | `ExtractionRuntimeResult` (`analysis`, `runtime`) | `ExtractionRuntimeError` (`provider_error`, `provider_timeout`, `schema_validation_failed`, `grounding_validation_failed`, ...) |
| **Draft Runtime** | `backend/app/services/draft_runtime.py` | `OpenAIDraftRuntime.run_draft_generation(source_analysis, selected_title_candidate_id=...)` | `source_analysis: dict`, `selected_title_candidate_id: str \| None` | `DraftRuntimeResult` (`draft`, `runtime`) | `DraftRuntimeError` (`provider_error`, `draft_schema_validation_failed`, `source_analysis_invalid`, `word_count_exceeded`, ...) |

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

from backend.app.core.config import Settings
from backend.app.schemas.analysis_input import ExtractionInputEnvelope
from backend.app.services.document_parsing import (
    DocumentPreparationError,
    DocumentPreparationService,
)
from backend.app.services.document_registry import DocumentRegistry
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

Nhằm phục vụ kiểm thử đơn vị và E2E không phụ thuộc mạng, orchestrator sử dụng duck-typing hoặc protocols rõ ràng:

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
    duration_ms: int
    status: str  # "completed"
    provider_request_id: str | None = None
    usage: dict[str, int] | None = None

@dataclass(frozen=True, slots=True)
class PipelineMetadata:
    document_id: str
    correlation_id: str
    total_duration_ms: int
    stages: tuple[PipelineStageMetadata, ...]
    source_cleanup_performed: bool

@dataclass(frozen=True, slots=True)
class PipelineResult:
    analysis: dict[str, Any]
    draft: dict[str, Any]
    metadata: PipelineMetadata
```

### 5.4 Error Model

Nhằm tránh tạo ra các lớp lỗi trừu tượng dư thừa, APP-003 giới thiệu một lớp lỗi duy nhất ở tầng điều phối:

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

- `stage`: Nhận diện chính xác giai đoạn phát sinh lỗi: `"lookup"`, `"preparation"`, `"extraction"`, `"draft_generation"`.
- `code`: Giữ nguyên mã lỗi chuẩn từ service con (`DocumentPreparationError.code`, `ExtractionRuntimeError.code`, `DraftRuntimeError.code`).
- `paths`: Bảo toàn JSON Pointer paths nếu lỗi xuất phát từ schema/business validation.
- Chaining: Mọi lỗi từ service con đều được liên kết bằng `raise PipelineOrchestrationError(...) from exc`.

---

## 6. Component Sequence & Step-by-Step Execution

Luồng thực thi bên trong `CorePipelineOrchestrator.run_pipeline()` tuân thủ nghiêm ngặt 5 bước tuần tự:

```
[Start]
   │
   ▼
[Step 1: Correlation & Document Lookup]
   │── Document ID invalid or not in Registry? ──► [Fail: stage='lookup', code='document_unknown']
   ▼
[Step 2: Document Preparation (APP-002)]
   │── File missing, SHA mismatch, or parser error? ──► [Fail: stage='preparation', code=exc.code]
   ▼
[Step 3: Extraction Runtime (AI-RUNTIME-001)]
   │── Provider timeout, refusal, schema, or grounding error? ──► [Fail: stage='extraction', code=exc.code]
   ▼
[Step 4: Draft Generation Runtime (AI-RUNTIME-002)]
   │── Schema invalid, word count exceeded, or business error? ──► [Fail: stage='draft_generation', code=exc.code]
   ▼
[Step 5: Resource Lifecycle & Result Assembly]
   │── (Optional: cleanup source if requested)
   ▼
[Return PipelineResult]
```

### Chi tiết các bước thực hiện:

1. **Khởi tạo và đối chiếu thông tin (Lookup & Initialization):**
   - Tạo mới `correlation_id` nếu caller không cung cấp: `uuid.uuid4().hex`.
   - Kiểm tra định dạng `document_id`. Đối chiếu trong `DocumentRegistry.get(document_id)`.
   - Nếu không tìm thấy, raise `PipelineOrchestrationError(stage="lookup", code="document_unknown", ...)`.

2. **Chuẩn bị dữ liệu tài liệu (Document Preparation - APP-002):**
   - Bắt đầu đo thời gian chặng `preparation`.
   - Gọi `self.preparation_service.prepare_extraction_input(document_id)`.
   - APP-002 thực hiện mở lease trên storage, kiểm tra tính toàn vẹn SHA-256, parse PDF/DOCX, sinh source units và trả về `ExtractionInputEnvelope`.
   - Nếu phát sinh `DocumentPreparationError`, bắt ngoại lệ, ghi log lỗi an toàn, thực hiện dọn dẹp (nếu bật cleanup) và raise `PipelineOrchestrationError(stage="preparation", code=exc.code, ...) from exc`.

3. **Trích xuất thông tin sáng chế (Extraction Runtime - AI-RUNTIME-001):**
   - Bắt đầu đo thời gian chặng `extraction`.
   - Gọi `self.extraction_runtime.run_extraction(envelope, correlation_id=correlation_id)`.
   - Service thực hiện chuyển đổi provider schema, gọi mô hình (hoặc fake), normalize, kiểm tra canonical schema và grounding validation.
   - Nhận về `ExtractionRuntimeResult` chứa `analysis` hợp lệ và `runtime` metadata.
   - Nếu phát sinh `ExtractionRuntimeError`, bắt ngoại lệ, ghi log lỗi, dọn dẹp (nếu bật cleanup) và raise `PipelineOrchestrationError(stage="extraction", code=exc.code, paths=exc.paths, ...) from exc`.
   - **Quy tắc bất biến:** Tuyệt đối KHÔNG gọi chặng draft nếu chặng extraction gặp bất kỳ lỗi nào.

4. **Soạn thảo mô tả bằng sáng chế (Draft Generation Runtime - AI-RUNTIME-002):**
   - Bắt đầu đo thời gian chặng `draft_generation`.
   - Gọi `self.draft_runtime.run_draft_generation(source_analysis=extraction_result.analysis, selected_title_candidate_id=selected_title_candidate_id)`.
   - Service tạo `AI-003 Draft Input Envelope`, sinh draft provider schema, gọi mô hình (hoặc fake), normalize, kiểm tra canonical draft schema và business rules (word count, legal assertions, grounding links).
   - Nhận về `DraftRuntimeResult` chứa `draft` hợp lệ và `runtime` metadata.
   - Nếu phát sinh `DraftRuntimeError`, bắt ngoại lệ, ghi log lỗi, dọn dẹp (nếu bật cleanup) và raise `PipelineOrchestrationError(stage="draft_generation", code=exc.code, paths=exc.paths, ...) from exc`.

5. **Dọn dẹp tài nguyên & Đóng gói kết quả (Cleanup & Result Assembly):**
   - Nếu tham số `cleanup_source=True`, gọi `self.storage.delete(document_id)` để xóa file đĩa và loại bỏ metadata khỏi registry.
   - Nếu quá trình xóa trả về `False` (do file đã bị xóa hoặc đang có lease khác), chỉ ghi log cảnh báo mức `WARNING` mà không làm thay đổi trạng thái thành công của pipeline.
   - Tổng hợp `PipelineStageMetadata` cho từng chặng (thời gian, status, provider_request_id, token usage).
   - Đóng gói và trả về đối tượng `PipelineResult`.

---

## 7. Storage Lifecycle & Cleanup Rules

APP-003 tôn trọng và phối hợp chặt chẽ với cơ chế lưu trữ của APP-001/APP-002:

1. **Thời điểm tài liệu sẵn sàng:** File upload và bản ghi metadata trở nên sẵn sàng ngay sau khi endpoint `POST /api/documents` (APP-001) hoàn tất xác thực ban đầu.
2. **Quyền đọc file:** `DocumentPreparationService` (APP-002) là thành phần duy nhất đọc trực tiếp file từ đĩa, và việc này bắt buộc phải diễn ra bên trong khối `with storage.lease(document_id):`.
3. **Độc lập sau bước Preparation:** Sau khi `ExtractionInputEnvelope` được tạo thành công ở Bước 2, toàn bộ nội dung cần thiết đã được nạp vào bộ nhớ dưới dạng các `SourceUnit`. Cả AI-RUNTIME-001 và AI-RUNTIME-002 đều không cần truy cập lại file trên đĩa.
4. **Chính sách dọn dẹp (Cleanup Policy):**
   - **Mặc định:** `cleanup_source=False` (giữ nguyên file cho đến khi TTL 1 giờ tự động quét dọn hoặc caller chủ động xóa).
   - **Khi bật `cleanup_source=True`:**
     - Nếu pipeline thành công: File đĩa và registry entry được dọn dẹp tại Bước 5.
     - Nếu pipeline thất bại ở bất kỳ chặng nào: Khối `finally` hoặc error handler sẽ thực hiện dọn dẹp đĩa để tránh rò rỉ dung lượng.
5. **Xử lý lỗi cleanup:** Lỗi khi xóa file đĩa (ví dụ lỗi OS file lock trên Windows) không được làm gián đoạn hay ghi đè lỗi nghiệp vụ chính đang được ném ra.
6. **Không lưu trữ vĩnh viễn:** Tuyệt đối không lưu trữ tài liệu nghiên cứu vô thời hạn. Bộ quét TTL (`DocumentStorage.sweep_expired()`) tiếp tục là chốt chặn an toàn cho mọi tài liệu tồn tại quá 60 phút.

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
- `document_id` (mã băm ngẫu nhiên 32 ký tự)
- Tên chặng thực thi: `stage="preparation"`, `stage="extraction"`, `stage="draft_generation"`
- Trạng thái chặng: `status="started"`, `status="completed"`, `status="failed"`
- Thời gian thực thi chặng: `duration_ms`
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
| **AC-01** | Khởi tạo Orchestrator thành công với cấu hình chuẩn | Unit Test | Đối tượng khởi tạo đầy đủ dependencies | `CorePipelineOrchestrator` instantiated |
| **AC-02** | Thành công trọn vẹn luồng PDF với Fake Runtimes | Offline E2E Test | Trả về `PipelineResult` đầy đủ `analysis`, `draft`, và `metadata` | 3 chặng hoàn tất, status="completed" |
| **AC-03** | Thành công trọn vẹn luồng DOCX với Fake Runtimes | Offline E2E Test | Trả về `PipelineResult` chính xác từ file DOCX hợp lệ | 3 chặng hoàn tất, dữ liệu nhất quán |
| **AC-04** | Thứ tự thực thi các chặng tuân thủ nghiêm ngặt | Mock/Spy Test | Thứ tự gọi chính xác: Preparation → Extraction → Draft | Thứ tự calls được ghi lại khớp 100% |
| **AC-05** | Dữ liệu `ExtractionInputEnvelope` được chuyển giao chính xác | Contract Test | Envelope từ Preparation được truyền nguyên vẹn vào Extraction | `envelope.document_metadata.sha256` khớp |
| **AC-06** | Dữ liệu `analysis` được chuyển giao chính xác vào Draft | Contract Test | `analysis` từ Extraction được truyền nguyên vẹn vào Draft | `source_analysis` nhận được khớp chính xác |
| **AC-07** | Tham số `selected_title_candidate_id` được truyền chính xác | Feature Test | Giá trị ID tiêu đề được chuyển vào Draft Runtime | `draft_runtime.invocations` ghi nhận đúng ID |
| **AC-08** | Lỗi không tìm thấy Document ID fail-closed an toàn | Error Test | Ném `PipelineOrchestrationError` (stage="lookup", code="document_unknown") | Không gọi preparation hay AI runtimes |
| **AC-09** | Tài liệu hết hạn hoặc bị xóa trên đĩa fail-closed | Error Test | Ném `PipelineOrchestrationError` (stage="preparation", code="document_expired_or_missing") | Không gọi AI runtimes |
| **AC-10** | Lỗi sai lệch SHA-256 (integrity check) fail-closed | Error Test | Ném `PipelineOrchestrationError` (stage="preparation", code="parse_failed") | Không gọi AI runtimes |
| **AC-11** | Tài liệu không có chữ (no extractable text) fail-closed | Error Test | Ném `PipelineOrchestrationError` (stage="preparation", code="no_extractable_text") | Không gọi AI runtimes |
| **AC-12** | Lỗi Extraction Provider (timeout/error) fail-closed | Error Test | Ném `PipelineOrchestrationError` (stage="extraction", code="provider_timeout") | Draft Runtime KHÔNG ĐƯỢC GỌI |
| **AC-13** | Lỗi Extraction Canonical Schema Validation fail-closed | Error Test | Ném `PipelineOrchestrationError` (stage="extraction", code="schema_validation_failed") | Draft Runtime KHÔNG ĐƯỢC GỌI |
| **AC-14** | Lỗi Extraction Grounding Validation fail-closed | Error Test | Ném `PipelineOrchestrationError` (stage="extraction", code="grounding_validation_failed") | Draft Runtime KHÔNG ĐƯỢC GỌI |
| **AC-15** | Lỗi Draft Provider (connection/error) fail-closed | Error Test | Ném `PipelineOrchestrationError` (stage="draft_generation", code="provider_connection") | Pipeline báo lỗi, không trả kết quả draft |
| **AC-16** | Lỗi Draft Canonical Schema Validation fail-closed | Error Test | Ném `PipelineOrchestrationError` (stage="draft_generation", code="draft_schema_validation_failed") | Pipeline báo lỗi |
| **AC-17** | Lỗi Draft Business Validation (word count, legal) fail-closed | Error Test | Ném `PipelineOrchestrationError` (stage="draft_generation", code="word_count_exceeded") | Pipeline báo lỗi |
| **AC-18** | Dọn dẹp tài nguyên khi bật `cleanup_source=True` (thành công) | Lifecycle Test | File trên đĩa bị xóa, registry entry bị loại bỏ | `storage.path_for(doc_id).exists() == False` |
| **AC-19** | Dọn dẹp tài nguyên khi bật `cleanup_source=True` (thất bại) | Lifecycle Test | File bị xóa ngay cả khi pipeline gặp lỗi ở giữa chặng | File được xóa an toàn trong error handler |
| **AC-20** | Giữ lại tài nguyên khi `cleanup_source=False` (mặc định) | Lifecycle Test | File trên đĩa và registry entry vẫn tồn tại | File tiếp tục sẵn sàng cho kiểm tra |
| **AC-21** | Lỗi khi cleanup không làm đè lỗi chính hay làm hỏng payload | Robustness Test | Quá trình xóa gặp OSError vẫn bảo toàn kết quả hoặc exception gốc | Log WARNING xuất hiện, không raise lỗi xóa |
| **AC-22** | Không gọi mạng bên ngoài trong default test suite | Network Guard | Chạy toàn bộ test suite khi ngắt mạng hoặc không có API key | Toàn bộ offline test suite PASS |
| **AC-23** | Không yêu cầu `OPENAI_API_KEY` trong môi trường test | Config Guard | Chạy test khi `$env:OPENAI_API_KEY=""` | Toàn bộ offline test suite PASS |
| **AC-24** | Số lần gọi Fake Extraction Runtime hoàn toàn tất định | Determinism Test | Chính xác 1 lần gọi cho mỗi pipeline run hợp lệ | `len(fake_extraction.invocations) == 1` |
| **AC-25** | Số lần gọi Fake Draft Runtime hoàn toàn tất định | Determinism Test | Chính xác 1 lần gọi cho mỗi pipeline run hợp lệ | `len(fake_draft.invocations) == 1` |
| **AC-26** | Tính tất định qua các lần chạy lặp lại | Determinism Test | Cùng một input cho ra kết quả metadata và cấu trúc giống hệt nhau | Kết quả 2 lần chạy độc lập tương đương |
| **AC-27** | Bảo vệ quyền riêng tư trong log và thông điệp lỗi | Privacy Guard | Error message và log không chứa raw text, prompts, hay secrets | Scan log output không có dữ liệu nhạy cảm |
| **AC-28** | Không làm biến dạng hay trôi hợp đồng của AI-001/AI-002/AI-003 | Contract Guard | Dữ liệu output tuân thủ 100% JSON Schema Draft 2020-12 | Canonical validators kiểm tra đều PASS |
| **AC-29** | Không có Public HTTP Endpoint nào được tạo ra | Scope Guard | Kiểm tra routing table của FastAPI app | Chỉ có `GET /health` và `POST /api/documents` |
| **AC-30** | Không thêm thư viện phụ thuộc mới | Dependency Guard | `requirements.txt` không thay đổi; `pip check` PASS | Không thêm package ngoài |
| **AC-31** | Không thay đổi chính sách mô hình AI | Policy Guard | Giữ nguyên `gpt-5.6-sol`, reasoning `high`, `store=False` | Settings không bị thay đổi |
| **AC-32** | Bộ kiểm thử hồi quy hiện có tiếp tục PASS 100% | Regression Test | Chạy toàn bộ test suites hiện tại của repository | Tất cả test hiện có đều PASS, 0 fail |

---

## 12. Proposed Implementation Files

Khi bước vào Phase Implementation (nhiệm vụ kỹ thuật tương lai được Human phê duyệt), các file dự kiến được tạo hoặc cập nhật gồm:

1. **Production Code:**
   - `backend/app/services/core_pipeline.py`: Chứa `CorePipelineOrchestrator`, `PipelineResult`, `PipelineMetadata`, `PipelineStageMetadata`, và `PipelineOrchestrationError`.
2. **Test Suites:**
   - `tests/backend/test_core_pipeline.py`: Unit tests cho orchestrator logic, error wrapping, và lifecycle.
   - `tests/backend/test_core_pipeline_e2e_offline.py`: E2E integration tests với synthetic fixtures, PDF/DOCX input thực tế trên đĩa, kết hợp fake runtimes.
3. **Application Registration (chỉ cho internal DI nếu cần):**
   - Cập nhật nhẹ `backend/app/main.py` để gắn `core_pipeline_orchestrator` vào `app.state` (nếu cần thiết cho backend factory).

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
.\.venv\Scripts\python.exe -m unittest discover -s tests/backend -p "test_*.py" -v

# 6. Kiểm tra tính toàn vẹn phụ thuộc
.\.venv\Scripts\python.exe -m pip check

# 7. Kiểm tra định dạng và khoảng trắng
git diff --check
```

---

## 14. Risks & Mitigations

| Rủi ro | Mức độ | Biện pháp giảm thiểu |
|---|---|---|
| **Rò rỉ dữ liệu nghiên cứu chưa công bố** | Critical | Chỉ dùng synthetic fixtures cho testing; không log payload, prompt, hay text; BLK-003 vẫn mở ngăn chặn production usage. |
| **Xung đột bộ nhớ / Disk lock trên Windows** | Medium | Sử dụng `storage.lease()` chuẩn; xử lý ngoại lệ unlinking an toàn trong khối `finally`. |
| **Lệch pha dữ liệu giữa Extraction và Draft** | High | Tận dụng chính xác `build_draft_input_envelope` và các validator chuẩn đã được kiểm chứng của AI-RUNTIME-002. |
| **Vô tình kích hoạt gọi API tốn phí** | High | Default E2E harness sử dụng Fake Runtimes; live smoke test được tách biệt hoàn toàn và yêu cầu cờ môi trường riêng. |

---

## 15. Human Decisions

| Quyết định | Trạng thái hiện tại | Ghi chú |
|---|---|---|
| **Scope & Boundaries của APP-003** | Khuyến nghị phê duyệt theo đặc tả này | Dừng lại ở Validated Draft JSON; không mở public endpoint, không render DOCX. |
| **Chính sách dọn dẹp file nguồn** | Khuyến nghị `cleanup_source: bool = False` mặc định | Caller có thể chủ động kích hoạt dọn dẹp; TTL 1 giờ tự động quét dọn bảo vệ hệ thống. |
| **Quyết định kiến trúc mới** | Không yêu cầu ADR mới | Kế thừa trọn vẹn ADR-001 đến ADR-010. |

---

## 16. Definition of Done (DoD) cho Specification

Đặc tả APP-003 được coi là hoàn tất khi:
- [x] Tài liệu đặc tả `docs/tasks/APP-003-core-pipeline-orchestration.md` được tạo đầy đủ các mục theo yêu cầu.
- [x] Không sửa đổi bất kỳ file mã nguồn backend, schema, prompt, fixture, template, hay test nào.
- [x] Trạng thái nhiệm vụ được cập nhật chính xác trong tài liệu quản trị: `Specification — Awaiting Independent Review`.
- [x] Không tuyên bố Phase 1, Phase 2, hay MVP hoàn thành.
- [x] `git diff --check` đạt kết quả sạch (clean).
- [x] Nhánh `docs/app-003-core-pipeline-orchestration-spec` được push lên remote repository.

---

## 17. Handoff Expectations

```text
Task ID: APP-003
Agent: Gemini 3.8 Flash High
Reviewer: Gemini 3.1 Pro High + Human / Product Owner
Status: Specification — Awaiting Independent Review
Version: Specification 1.0.0
Work completed: Created full task specification for APP-003 internal core pipeline orchestration and offline E2E harness; defined sequence, interfaces, error taxonomy, lifecycle, dependency injection, logging, and 32 acceptance criteria.
Files affected: docs/tasks/APP-003-core-pipeline-orchestration.md (new); docs/operations/01_PROJECT_CONTROL_CENTER.md; PROJECT_CONTEXT.md; README.md.
Evidence checked: Git branch, status, diff check PASS; zero production code or schemas modified.
Findings: None; fully consistent with ADR-001 through ADR-010 and prior components.
Decisions: Human review and approval of APP-003 specification required before implementation task is assigned.
Issues: BLK-003 remains open; live provider smoke remains deferred due to lack of API funding.
Security impact: Synthetic-only testing design; no credentials, PII or research content exposed.
Recommended next action: Independent read-only specification review by Gemini 3.1 Pro High before any implementation begins.
```
