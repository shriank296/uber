import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from tests.factories.rider import RiderFactory
from uber.models.rider import Rider
from uber.repository.ride import RideRepository


@pytest.fixture
def ride_repository(session: AsyncSession) -> RideRepository:
    return RideRepository(session)


@pytest_asyncio.fixture
async def create_rider(session: AsyncSession) -> Rider:
    rider = RiderFactory.build()
    async with session.begin() as test_session:
        test_session.add(rider)
        await session.flush()
    return rider
