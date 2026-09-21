"""FastAPI application factory for APP-001 and APP-002 local services."""

from __future__ import annotations

import logging
import uuid
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from backend.app.api.routes.documents import APIError, router as documents_router
from backend.app.api.routes.health import router as health_router
from backend.app.core.config import Settings
from backend.app.services.document_parsing import DocumentPreparationService
from backend.app.services.document_registry import DocumentRegistry
from backend.app.services.document_storage import DocumentStorage
from backend.app.services.document_validation import DocumentValidator


LOGGER = logging.getLogger(__name__)


def _correlation_id(request: Request) -> str:
    existing = getattr(request.state, "correlation_id", None)
    if existing:
        return existing
    generated = uuid.uuid4().hex
    request.state.correlation_id = generated
    return generated


def create_app(settings: Settings | None = None) -> FastAPI:
    runtime_settings = settings or Settings.from_environment()
    registry = DocumentRegistry()
    storage = DocumentStorage(
        runtime_settings.storage_root,
        ttl_seconds=runtime_settings.upload_ttl_seconds,
        max_upload_bytes=runtime_settings.max_upload_bytes,
        read_chunk_bytes=runtime_settings.read_chunk_bytes,
        on_removed=registry.remove,
    )
    validator = DocumentValidator(runtime_settings)
    preparation_service = DocumentPreparationService(
        storage,
        registry,
        max_source_unit_chars=runtime_settings.max_source_unit_chars,
    )

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        storage.sweep_expired()
        yield

    application = FastAPI(title="AI IP Generator Backend", lifespan=lifespan)
    application.state.settings = runtime_settings
    application.state.document_storage = storage
    application.state.document_validator = validator
    application.state.document_registry = registry
    application.state.document_preparation_service = preparation_service
    application.include_router(health_router)
    application.include_router(documents_router)

    @application.middleware("http")
    async def add_correlation_id(request: Request, call_next):
        correlation_id = _correlation_id(request)
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation_id
        return response

    @application.exception_handler(APIError)
    async def api_error_handler(request: Request, exc: APIError) -> JSONResponse:
        correlation_id = _correlation_id(request)
        LOGGER.info("upload_rejected code=%s correlation_id=%s", exc.code, correlation_id)
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.code,
                    "message": exc.safe_message,
                    "correlation_id": correlation_id,
                }
            },
        )

    @application.exception_handler(Exception)
    async def unexpected_error_handler(request: Request, _: Exception) -> JSONResponse:
        correlation_id = _correlation_id(request)
        LOGGER.error("unexpected_request_error correlation_id=%s", correlation_id)
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "internal_error",
                    "message": "The request could not be completed.",
                    "correlation_id": correlation_id,
                }
            },
        )

    return application


app = create_app()

