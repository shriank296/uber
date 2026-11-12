from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def test_db_connection_successful(session: AsyncSession) -> None:
    result = await session.execute(text("SELECT 1"))
    assert result.scalar_one() == 1
