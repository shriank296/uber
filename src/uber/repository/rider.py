import logging
from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from uber.models import Rider

logger = logging.getLogger(__name__)


class RiderRepository:
    """
    Rider Repository

    We do only flush, insert will execute and database value generated but transaction is not committed yet.
    Service layer should own the transaction and decide when to commit or rollback.
    """

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, rider_id: UUID) -> Rider | None:
        """Get a rider by primary key"""
        statement = select(Rider).where(Rider.id == rider_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def create(self, rider: Rider) -> Rider:
        """Create a rider"""
        self.session.add(rider)
        await self.session.flush()
        return rider

    async def get_all_riders_paginated(
        self, page_number: int, page_size: int
    ) -> Sequence[Rider]:
        """Get paginated riders."""
        statement = (
            select(Rider)
            .order_by(Rider.created_at, Rider.id)
            .offset((page_number - 1) * page_size)  # page number one-based.
            .limit(page_size)
        )
        result = await self.session.scalars(statement)
        return result.all()

    async def count_all_riders(self) -> int:
        """Get total number of riders"""
        statement = select(func.count()).select_from(Rider)
        result = await self.session.execute(statement)
        return result.scalar_one()
