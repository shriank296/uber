from collections.abc import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from alembic.config import Config
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from testcontainers.community.postgres import PostgresContainer

from alembic import command
from uber.api.dependencies import get_session
from uber.database import Database
from uber.main import create_app
from uber.settings import AppSettings


@pytest.fixture(scope="session")
def test_db_url() -> Generator[str]:

    def run_alembic_migrations(container_db_url: str) -> None:
        alembic_cfg = Config("alembic.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", container_db_url)
        command.upgrade(alembic_cfg, "head")

    with PostgresContainer("postgres:latest", driver="asyncpg") as postgres:
        db_url = postgres.get_connection_url()
        run_alembic_migrations(db_url.replace("asyncpg", "psycopg"))
        yield db_url


@pytest.fixture(scope="session")
def test_settings(test_db_url: str) -> AppSettings:
    return AppSettings(
        database_url=test_db_url,
        project_name="Uber Test",
        migration_database_url=test_db_url.replace("+asyncpg", "+psycopg"),
    )


@pytest_asyncio.fixture
async def database(test_db_url: str) -> AsyncGenerator[Database]:
    test_db = Database(test_db_url)
    try:
        yield test_db
    finally:
        await test_db.dispose()


@pytest_asyncio.fixture
async def session(database: Database) -> AsyncGenerator[AsyncSession]:
    async for db_session in database.get_async_session():
        yield db_session


@pytest.fixture
def test_client(test_settings: AppSettings) -> Generator[TestClient]:
    app = create_app(settings=test_settings)
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
