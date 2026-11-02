import pytest
from sqlalchemy import text

from uber.database import Database


@pytest.fixture
async def database(test_db_url):
    test_db = Database(test_db_url)
    try:
        yield test_db
    finally:
        await test_db.dispose()


async def test_db_connection_successful(database):
    session_generator = database.get_async_session()
    session = await anext(session_generator)
    try:
        result = await session.execute(text("SELECT 1"))
        assert result.scalar_one() == 1
    finally:
        await session_generator.aclose()
