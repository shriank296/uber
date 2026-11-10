from contextlib import asynccontextmanager

from fastapi import FastAPI

from uber.database import Database
from uber.settings import AppSettings


def create_app(settings: AppSettings):

    @asynccontextmanager
    async def lifespan(app: FastAPI):
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

    return app
