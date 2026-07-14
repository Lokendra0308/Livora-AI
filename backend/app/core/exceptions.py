"""
Application-wide exception types + FastAPI exception handlers.

Why: raising a generic Exception anywhere in the app produces an ugly
500 with no useful client-facing message. Instead, every domain error
subclasses NexusException with a machine-readable `code` and safe
`message`. main.py registers ONE handler that turns any NexusException
into a consistent JSON error envelope.
"""

import logging

from fastapi import Request, status
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class NexusException(Exception):
    """Base class for all application-raised errors."""

    status_code: int = status.HTTP_400_BAD_REQUEST
    code: str = "bad_request"

    def __init__(self, message: str, status_code: int | None = None):
        self.message = message
        if status_code:
            self.status_code = status_code
        super().__init__(message)


class NotFoundException(NexusException):
    status_code = status.HTTP_404_NOT_FOUND
    code = "not_found"


class UnauthorizedException(NexusException):
    status_code = status.HTTP_401_UNAUTHORIZED
    code = "unauthorized"


class ForbiddenException(NexusException):
    status_code = status.HTTP_403_FORBIDDEN
    code = "forbidden"


class ValidationException(NexusException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    code = "validation_error"


class AgentExecutionException(NexusException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    code = "agent_execution_error"


async def nexus_exception_handler(request: Request, exc: NexusException) -> JSONResponse:
    logger.warning("Handled error on %s %s: %s", request.method, request.url.path, exc.message)
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.code, "message": exc.message}},
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": {"code": "internal_error", "message": "An unexpected error occurred."}},
    )
