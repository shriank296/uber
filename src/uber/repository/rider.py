import logging
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from uber.models import Rider

logger = logging.getLogger(__name__)


class RiderRepository:
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
        # We do only flush, insert will execute and database value generated but transaction is not committed yet. Service layer should own the transaction and decide when to commit or rollback.
        await self.session.flush()
        return rider
