import logging

from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, OperationalError

from uber.exceptions.base import AppException

logger = logging.getLogger(__name__)


async def app_exception_handler(
    request: Request,
    exc: AppException,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
            }
        },
    )


async def sqlalchemy_operational_error(
    request: Request,
    exc: OperationalError,
) -> JSONResponse:
    logger.exception(
        "Database operational error on %s %s",
        request.method,
        request.url.path,
    )
    return JSONResponse(
        status_code=503,
        content={
            "error": {
                "code": "DATABASE_UNAVAILABLE",
                "message": "The service is temporarily unavailable",
            }
        },
    )


async def sqlalchemy_integrity_error(
    request: Request,
    exc: IntegrityError,
) -> JSONResponse:
    logger.exception(
        "Database integrity error on %s %s",
        request.method,
        request.url.path,
    )
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTEGRITY_ERROR",
                "message": "The request could not be completed because data integrity constraint",
            }
        },
    )
