from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class Database:
    def __init__(
        self,
        database_url: str,
        engine_kwargs: dict[str, Any] | None = None,
    ) -> None:
        self._async_engine: AsyncEngine = create_async_engine(
            database_url,
            **(engine_kwargs or {}),
        )

        self._async_session_factory = async_sessionmaker(
            bind=self._async_engine,
            autoflush=True,
            expire_on_commit=False,
        )

    async def get_async_session(self) -> AsyncGenerator[AsyncSession]:
        async with self._async_session_factory() as session:
            yield session

    async def dispose(self) -> None:
        await self._async_engine.dispose()
