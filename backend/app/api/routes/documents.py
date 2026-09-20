"""Secure single-document upload endpoint."""

from __future__ import annotations

from fastapi import APIRouter, Request
from starlette.datastructures import UploadFile
from starlette.exceptions import HTTPException as StarletteHTTPException

from backend.app.services.document_storage import EmptyUploadError, UploadTooLargeError
from backend.app.services.document_validation import DocumentValidationError, sanitize_filename


router = APIRouter(prefix="/api")


class APIError(Exception):
    def __init__(self, status_code: int, code: str, message: str) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.safe_message = message


def _validation_status(code: str) -> int:
    if code in {"unsupported_extension", "format_mismatch"}:
        return 415
    return 422


@router.post("/documents", status_code=201)
async def upload_document(request: Request) -> dict[str, object]:
    settings = request.app.state.settings
    storage = request.app.state.document_storage
    validator = request.app.state.document_validator
    storage.sweep_expired()

    try:
        form_context = request.form(
            max_files=10,
            max_fields=10,
            max_part_size=settings.max_upload_bytes + settings.read_chunk_bytes,
        )
        async with form_context as form:
            items = list(form.multi_items())
            file_items = [(key, value) for key, value in items if isinstance(value, UploadFile)]
            if len(file_items) != 1:
                raise APIError(400, "single_file_required", "Exactly one file must be uploaded.")
            if len(items) != 1 or file_items[0][0] != "file":
                raise APIError(400, "invalid_multipart_fields", "Only the multipart field 'file' is accepted.")
            upload = file_items[0][1]
            document_id = storage.allocate_id()
            try:
                path, size_bytes = await storage.stream_to_disk(upload, document_id)
                result = validator.validate(
                    path,
                    filename=upload.filename,
                    declared_mime=upload.content_type,
                )
            except UploadTooLargeError as exc:
                raise APIError(413, "file_too_large", "The file exceeds the 10 MiB limit.") from exc
            except EmptyUploadError as exc:
                raise APIError(400, "empty_file", "The uploaded file is empty.") from exc
            except DocumentValidationError as exc:
                storage.delete(document_id)
                raise APIError(_validation_status(exc.code), exc.code, exc.safe_message) from exc
            except Exception:
                storage.delete(document_id)
                raise

            response: dict[str, object] = {
                "document_id": document_id,
                "original_filename": sanitize_filename(upload.filename),
                "media_type": result.media_type,
                "size_bytes": size_bytes,
                "validation_status": "validated",
            }
            if result.page_count is not None:
                response["page_count"] = result.page_count
            return response
    except APIError:
        raise
    except StarletteHTTPException as exc:
        raise APIError(400, "malformed_multipart", "The multipart request is malformed.") from exc
