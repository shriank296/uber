import logging
from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from uber.models import Driver
from uber.models.enums import DriverStatus

logger = logging.getLogger(__name__)


class DriverRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, driver_id: UUID) -> Driver | None:
        """Get a driver by primary key"""
        statement = select(Driver).where(Driver.id == driver_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def create(self, driver: Driver) -> Driver:
        """Create a driver"""
        self.session.add(driver)
        # We do only flush, insert will execute and database value generated but transaction is not committed yet. Service layer should own the transaction and decide when to commit or rollback.
        await self.session.flush()
        return driver

    async def get_available_drivers(self) -> Sequence[Driver]:
        """Get drivers whose status is avaialble"""
        statement = select(Driver).where(Driver.status == DriverStatus.AVAILABLE)
        return (await self.session.scalars(statement)).all()
