from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.exc import IntegrityError, OperationalError

from uber.api.rider import rider_router
from uber.database import Database
from uber.exceptions.base import AppException
from uber.exceptions.exception_handlers import (
    app_exception_handler,
    sqlalchemy_integrity_error,
    sqlalchemy_operational_error,
)
from uber.settings import AppSettings, get_app_settings


def create_app(settings: AppSettings) -> FastAPI:

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
        database = Database(settings.database_url)
        app.state.database = database
        try:
            yield
        finally:
            await database.dispose()

    app = FastAPI(
        title=settings.project_name,
        lifespan=lifespan,
    )
    app.add_exception_handler(AppException, app_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(OperationalError, sqlalchemy_operational_error)  # type: ignore[arg-type]
    app.add_exception_handler(IntegrityError, sqlalchemy_integrity_error)  # type: ignore[arg-type]

    app.include_router(rider_router)

    return app


def create_app_from_settings() -> FastAPI:
    settings = get_app_settings()
    return create_app(settings)
