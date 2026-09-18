# ĐẶC TẢ HỆ THỐNG
## AI Intellectual Property Description Generator

**Phiên bản:** 0.1  
**Trạng thái:** Draft / MVP Specification  
**Mục tiêu:** Đặc tả hệ thống AI hỗ trợ chuyển đổi bài báo nghiên cứu khoa học thành bản mô tả SHTT / bản mô tả sáng chế có cấu trúc để người dùng rà soát và xuất tài liệu.

---

# 1. Tổng quan hệ thống

## 1.1. Bài toán

Người dùng cung cấp một bài báo nghiên cứu khoa học ở định dạng PDF hoặc DOCX. Hệ thống sử dụng AI để:

1. Đọc và phân tích nội dung tài liệu.
2. Trích xuất thông tin kỹ thuật quan trọng.
3. Xác định các yếu tố có liên quan đến sáng chế / giải pháp kỹ thuật.
4. Chuẩn hóa thông tin thành cấu trúc dữ liệu cố định.
5. Sinh bản nháp mô tả SHTT theo mẫu đã cấu hình.
6. Cho phép người dùng rà soát, chỉnh sửa và xuất file DOCX.

Hệ thống là công cụ **hỗ trợ soạn thảo**, không thay thế việc thẩm định pháp lý, đánh giá khả năng bảo hộ hoặc tư vấn chuyên môn của chuyên gia SHTT.

## 1.2. Mục tiêu

Xây dựng một nền tảng có khả năng thực hiện luồng:

```text
Bài báo nghiên cứu
        ↓
Upload tài liệu
        ↓
AI phân tích
        ↓
Trích xuất thông tin kỹ thuật
        ↓
Chuẩn hóa dữ liệu
        ↓
Sinh bản mô tả SHTT
        ↓
Người dùng rà soát
        ↓
Xuất DOCX
```

## 1.3. Phạm vi MVP

MVP tập trung vào một luồng xử lý đơn giản:

- 01 tài liệu đầu vào cho mỗi lần phân tích.
- Hỗ trợ PDF và DOCX.
- AI xử lý nội dung tài liệu.
- Trả về dữ liệu có cấu trúc.
- Sinh bản nháp mô tả SHTT.
- Cho phép xem trước và chỉnh sửa.
- Xuất file DOCX.

Các chức năng nâng cao như quản lý người dùng, lịch sử phiên bản, tìm kiếm prior art quy mô lớn, billing và collaboration được để cho giai đoạn sau.

---

# 2. Đối tượng sử dụng

## 2.1. Người dùng chính

- Cán bộ nghiên cứu.
- Giảng viên / nhà khoa học.
- Nhân sự phụ trách SHTT.
- Chuyên viên chuyển giao công nghệ.
- Quản trị viên dự án nghiên cứu.

## 2.2. Vai trò trong MVP

### User

Có thể:

- Upload tài liệu.
- Bắt đầu phân tích.
- Xem kết quả AI.
- Chỉnh sửa nội dung.
- Xuất DOCX.

### Admin

Chưa bắt buộc ở MVP.

Có thể bổ sung ở giai đoạn sau để:

- Quản lý người dùng.
- Quản lý template.
- Quản lý prompt.
- Theo dõi usage.
- Xem log hệ thống.

---

# 3. Yêu cầu chức năng

## FR-01. Upload tài liệu

Hệ thống phải cho phép người dùng tải lên:

- PDF.
- DOCX.

### Điều kiện

- Kiểm tra định dạng file.
- Kiểm tra kích thước file.
- Từ chối file không hợp lệ.
- Không cho phép thực thi file từ phía server.

---

## FR-02. Đọc và xử lý nội dung tài liệu

Hệ thống phải có khả năng:

- Đọc text trong tài liệu.
- Gửi tài liệu hoặc nội dung đã trích xuất cho AI.
- Xử lý tài liệu có nhiều trang.
- Giữ lại metadata cần thiết nếu có.

---

## FR-03. Phân tích nội dung bằng AI

AI phải trích xuất tối thiểu các nhóm thông tin:

- Tên nghiên cứu.
- Lĩnh vực kỹ thuật.
- Vấn đề kỹ thuật đang tồn tại.
- Mục tiêu nghiên cứu.
- Giải pháp / phương pháp được đề xuất.
- Thành phần hoặc bước xử lý chính.
- Dữ liệu thực nghiệm / cách triển khai.
- Kết quả kỹ thuật.
- Ưu điểm kỹ thuật.
- Điểm khác biệt hoặc yếu tố có thể xem xét là mới.
- Thông tin còn thiếu.
- Nội dung cần chuyên gia xác minh.

---

## FR-04. Structured Output

Kết quả AI phải được trả về theo một schema xác định trước.

Ví dụ:

```json
{
  "invention_title": "",
  "technical_field": "",
  "background": "",
  "technical_problem": "",
  "technical_objective": "",
  "technical_solution": "",
  "components_or_steps": [],
  "novel_features": [],
  "technical_effects": [],
  "advantages": [],
  "embodiments": [],
  "supporting_evidence": [],
  "missing_information": [],
  "review_flags": []
}
```

Hệ thống không nên sử dụng free-form text làm dữ liệu trung gian chính.

---

## FR-05. Phát hiện thông tin không đủ cơ sở

Hệ thống phải có cơ chế đánh dấu:

- Thông tin không xuất hiện trong tài liệu nguồn.
- Thông tin AI suy luận nhưng không có bằng chứng rõ ràng.
- Nội dung thiếu dữ kiện.
- Thuật ngữ cần xác minh.
- Điểm cần chuyên gia SHTT đánh giá.

Không được tự động coi nội dung AI suy luận là sự thật.

---

## FR-06. Sinh bản mô tả SHTT

Từ structured output, hệ thống phải sinh bản nháp theo cấu trúc đã cấu hình.

Các mục có thể bao gồm:

1. Tên sáng chế.
2. Lĩnh vực kỹ thuật.
3. Tình trạng kỹ thuật.
4. Vấn đề kỹ thuật.
5. Mục đích / nhiệm vụ của sáng chế.
6. Bản chất kỹ thuật.
7. Mô tả chi tiết.
8. Ví dụ thực hiện.
9. Hiệu quả kỹ thuật.
10. Nội dung phục vụ cho việc xây dựng yêu cầu bảo hộ.

Cấu trúc cuối cùng sẽ được điều chỉnh theo template chính thức mà dự án sử dụng.

---

## FR-07. Human Review

Hệ thống phải cho phép người dùng:

- Xem từng trường nội dung.
- Sửa nội dung do AI tạo.
- Xác nhận hoặc bỏ qua cảnh báo.
- Nhập bổ sung thông tin còn thiếu.
- Sinh lại một phần nội dung nếu cần.

---

## FR-08. Export DOCX

Hệ thống phải cho phép:

- Mapping dữ liệu vào template DOCX.
- Sinh file DOCX có thể chỉnh sửa.
- Giữ định dạng theo template.
- Tải file về sau khi hoàn tất.

Thư viện dự kiến:

```text
docxtpl
```

---

## FR-09. Lưu trữ dữ liệu

Trong MVP có thể chưa bắt buộc.

Nếu bật Supabase, hệ thống có thể lưu:

- Project.
- Tên file.
- Thời điểm tạo.
- Structured output.
- Bản nháp đã chỉnh sửa.
- Phiên bản prompt.
- Phiên bản schema.
- Đường dẫn file đầu ra.

---

# 4. Yêu cầu phi chức năng

## NFR-01. Bảo mật

- API key phải nằm ở backend.
- Không hard-code secret trong source code.
- Không expose OpenAI API key ra frontend.
- Sử dụng biến môi trường.
- Không commit file `.env`.

---

## NFR-02. Riêng tư dữ liệu

Tài liệu nghiên cứu có thể chứa thông tin chưa công bố.

Hệ thống cần:

- Hạn chế lưu file lâu hơn mức cần thiết.
- Cho phép xóa file tạm.
- Không dùng tài liệu của người dùng làm dữ liệu công khai.
- Tách rõ dữ liệu người dùng và log kỹ thuật.

---

## NFR-03. Khả năng truy vết

Mỗi kết quả AI nên có khả năng lưu:

- Prompt version.
- Schema version.
- Model.
- Thời gian xử lý.
- Source document.
- Các cảnh báo liên quan.

---

## NFR-04. Khả năng bảo trì

Hệ thống cần tách biệt:

- Frontend.
- Backend.
- Prompt.
- Schema.
- Template.
- Logic export.

Việc thay đổi prompt không nên yêu cầu viết lại frontend.

---

## NFR-05. Khả năng mở rộng

Kiến trúc phải cho phép bổ sung:

- Nhiều tài liệu đầu vào.
- File Search.
- Database.
- Authentication.
- Version history.
- Prior-art reference.
- Collaboration.
- Multi-language.

---

## NFR-06. Hiệu năng

Mục tiêu MVP:

- Upload file phản hồi ngay.
- Hiển thị trạng thái processing.
- Không khóa UI trong quá trình AI xử lý.
- Có timeout và xử lý lỗi.
- Có thông báo rõ ràng khi API thất bại.

---

# 5. Kiến trúc đề xuất

## 5.1. Tổng quan

```text
┌──────────────────────────────┐
│          Frontend            │
│      Next.js + TypeScript    │
└──────────────┬───────────────┘
               │ HTTPS / API
               ▼
┌──────────────────────────────┐
│           Backend            │
│       FastAPI + Python       │
│                              │
│ - File validation            │
│ - AI orchestration           │
│ - Schema validation          │
│ - Prompt management          │
│ - DOCX generation            │
└───────┬──────────────┬───────┘
        │              │
        ▼              ▼
┌───────────────┐  ┌──────────────┐
│  OpenAI API   │  │   docxtpl    │
│ Responses API │  │ DOCX Export  │
└───────┬───────┘  └──────────────┘
        │
        ▼
┌──────────────────────────────┐
│ Supabase (optional / MVP+)   │
│ PostgreSQL + storage         │
└──────────────────────────────┘
```

---

# 6. Công nghệ sử dụng

| Thành phần | Công nghệ |
|---|---|
| Frontend | Next.js |
| Frontend language | TypeScript |
| Backend | FastAPI |
| Backend language | Python |
| AI | OpenAI Responses API |
| Output schema | Structured Outputs / JSON Schema |
| Retrieval | OpenAI File Search, nếu cần |
| Database | Supabase / PostgreSQL |
| DOCX generation | docxtpl |
| Frontend hosting | Vercel |
| Backend hosting | Railway |
| Version control | GitHub |

---

# 7. Luồng xử lý chi tiết

## Bước 1 — Upload

Frontend gửi file đến backend.

```text
POST /api/documents
```

Backend:

- Validate extension.
- Validate MIME type.
- Validate size.
- Tạo processing ID.

---

## Bước 2 — AI Analysis

Backend gọi AI service.

```text
Document
   ↓
Extraction Prompt
   ↓
Structured Output
```

Output phải tuân thủ JSON schema.

---

## Bước 3 — Validation

Backend kiểm tra:

- Đủ field bắt buộc.
- Đúng datatype.
- Không lỗi parse.
- Có missing information.
- Có review flag.

---

## Bước 4 — Draft Generation

Structured data được đưa vào prompt sinh từng section.

```text
Structured JSON
      ↓
Section Generator
      ↓
Draft Description
```

---

## Bước 5 — User Review

Frontend hiển thị:

- Nội dung AI.
- Cảnh báo.
- Trường thiếu.
- Nguồn hỗ trợ nếu có.

Người dùng chỉnh sửa trước khi export.

---

## Bước 6 — Export

```text
Reviewed Data
      ↓
docxtpl
      ↓
Template
      ↓
output.docx
```

---

# 8. API dự kiến

## POST /api/documents

Upload tài liệu.

### Response

```json
{
  "document_id": "uuid",
  "filename": "research-paper.pdf",
  "status": "uploaded"
}
```

---

## POST /api/documents/{id}/analyze

Bắt đầu AI analysis.

### Response

```json
{
  "document_id": "uuid",
  "status": "processing"
}
```

---

## GET /api/documents/{id}/analysis

Lấy structured output.

### Response

```json
{
  "status": "completed",
  "analysis": {
    "invention_title": "",
    "technical_field": "",
    "technical_problem": "",
    "technical_solution": ""
  }
}
```

---

## PUT /api/documents/{id}/draft

Lưu nội dung sau khi user chỉnh sửa.

---

## POST /api/documents/{id}/export

Sinh file DOCX.

---

# 9. Cấu trúc backend dự kiến

```text
backend/
│
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   ├── documents.py
│   │   └── export.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   │
│   ├── schemas/
│   │   ├── analysis.py
│   │   └── document.py
│   │
│   ├── services/
│   │   ├── openai_service.py
│   │   ├── analysis_service.py
│   │   └── document_service.py
│   │
│   └── exporters/
│       └── docx_exporter.py
│
└── tests/
```

---

# 10. Cấu trúc frontend dự kiến

```text
frontend/
│
├── app/
│   ├── page.tsx
│   ├── upload/
│   ├── analysis/
│   └── review/
│
├── components/
│   ├── UploadBox.tsx
│   ├── ProcessingStatus.tsx
│   ├── AnalysisForm.tsx
│   └── ExportButton.tsx
│
└── lib/
    └── api.ts
```

---

# 11. Quản lý Prompt

Prompt được lưu riêng trong thư mục:

```text
prompts/
├── v1/
│   ├── extraction.md
│   ├── invention-analysis.md
│   ├── draft-generation.md
│   └── validation.md
└── README.md
```

Mỗi prompt nên có:

- Version.
- Mục tiêu.
- Input.
- Expected output.
- Constraints.
- Evaluation notes.

---

# 12. Error Handling

Hệ thống cần xử lý tối thiểu:

| Mã | Trường hợp |
|---|---|
| 400 | File không hợp lệ |
| 413 | File quá lớn |
| 422 | Structured output không hợp lệ |
| 429 | API rate limit |
| 500 | Lỗi server |
| 502 | Lỗi từ AI provider |
| 504 | Timeout |

Frontend phải hiển thị thông báo dễ hiểu cho người dùng.

---

# 13. Logging

Backend cần log:

- Request ID.
- Document ID.
- Processing stage.
- Thời gian xử lý.
- Model.
- Prompt version.
- Schema version.
- Error.

Không log:

- API key.
- Token bí mật.
- Nội dung nhạy cảm không cần thiết.

---

# 14. Kiểm thử

## 14.1. Functional Test

- Upload PDF hợp lệ.
- Upload DOCX hợp lệ.
- Từ chối file sai định dạng.
- AI trả structured output.
- Export DOCX thành công.

## 14.2. AI Evaluation

Đánh giá:

- Độ đầy đủ.
- Độ chính xác so với tài liệu nguồn.
- Tỷ lệ hallucination.
- Khả năng phát hiện missing information.
- Độ ổn định giữa các lần chạy.
- Chất lượng mapping sang template.

## 14.3. Regression Test

Chuẩn bị một tập bài báo cố định để test khi:

- Đổi prompt.
- Đổi schema.
- Đổi model.
- Đổi template.

---

# 15. Tiêu chí hoàn thành MVP

MVP được xem là hoàn thành khi đáp ứng được toàn bộ luồng sau:

```text
User upload PDF/DOCX
        ↓
System accepts file
        ↓
AI extracts structured technical data
        ↓
System generates IP description draft
        ↓
User can review/edit
        ↓
System exports valid DOCX
```

Các tiêu chí tối thiểu:

- Upload hoạt động.
- AI integration hoạt động.
- Structured output parse được.
- Có cơ chế đánh dấu nội dung thiếu / cần review.
- Có preview.
- Có export DOCX.
- Không lộ API key.
- Có test với ít nhất một bộ tài liệu mẫu.

---

# 16. Ngoài phạm vi MVP

Các chức năng chưa bắt buộc:

- Automatic patentability conclusion.
- Legal opinion.
- Freedom-to-operate analysis.
- Automated prior-art decision.
- Multi-user collaboration.
- Billing.
- Enterprise SSO.
- Full patent database search.
- Automatic filing to patent offices.

---

# 17. Roadmap đề xuất

## Phase 1 — Foundation

- Hoàn thiện đặc tả.
- Chốt output schema.
- Chốt template.
- Khởi tạo frontend.
- Khởi tạo backend.

## Phase 2 — AI Pipeline

- Upload.
- OpenAI integration.
- Structured Outputs.
- Validation.
- Prompt v1.

## Phase 3 — Draft Generator

- Mapping nội dung.
- Review UI.
- DOCX generation.

## Phase 4 — Evaluation

- Test nhiều bài báo.
- Đánh giá hallucination.
- Chỉnh prompt.
- Chỉnh schema.

## Phase 5 — Deployment

- Vercel.
- Railway.
- Supabase nếu cần lưu trữ.

---

# 18. Kết luận

Kiến trúc ưu tiên nguyên tắc:

```text
Source Document
      ↓
Structured Extraction
      ↓
Validation
      ↓
Human Review
      ↓
Controlled Document Generation
```

Mục tiêu của hệ thống không phải là để AI tự động đưa ra kết luận pháp lý, mà là giảm thời gian chuyển đổi nội dung nghiên cứu thành một bản nháp SHTT có cấu trúc, có khả năng truy vết và thuận tiện cho chuyên gia tiếp tục xử lý.
