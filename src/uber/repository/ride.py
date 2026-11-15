import logging
from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from uber.models import Ride
from uber.models.enums import RideStatus


class RideRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, ride_id: UUID) -> Ride | None:
        """Get a Ride by primary key"""
        statement = select(Ride).where(Ride.id == ride_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def create(self, ride: Ride) -> Ride:
        """Create a ride"""
        self.session.add(ride)
        # We do only flush, insert will execute and database value generated but transaction is not committed yet. Service layer should own the transaction and decide when to commit or rollback.
        await self.session.flush()
        return ride

    async def get_rides_by_rider(self, rider_id: UUID) -> Sequence[Ride]:
        """Get rides by rider"""
        statement = select(Ride).where(Ride.rider_id == rider_id)
        return (await self.session.scalars(statement)).all()
