# Templates / Mẫu tài liệu

**Nhiệm vụ / Responsibilities**

- Lưu template DOCX versioned dùng cho output generation.
- Lưu manifest/mapping giữa draft JSON và tài liệu xuất.
- Chỉ chứa template/cấu hình sinh tài liệu; không chứa tài liệu nghiên cứu thật.

---

This directory stores document templates used for output generation.

Current contents:

- Canonical Patent DOCX Template v1.0.0 at `patent-docx/v1.0.0/patent-description-template.docx`.
- Versioned manifest and mapping from Patent Draft Generation Contract v1.0.0.
- Deterministic offline renderer at `tests/docx/render_patent_docx_v1.py`.

DOC-001 status: **Completed — Merged via PR #7**. Human Visual QA, Gemini independent review, and targeted governance review passed with no findings or required changes; 85/85 tests passed. Implementation commit: `d3f7c7d9596b77a39e9a56fcdf97c76cb972612a`; merge commit: `d208a7925da844c5b43578bac8ebdbb1c5c6b5b8`.

Generated review documents belong under the Git-ignored `generated/patent-docx/v1.0.0/` path and must not be committed.

Do not commit confidential source documents unless repository access and data-handling requirements explicitly allow it.
