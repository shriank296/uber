from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from tests.factories.rider import RiderFactory
from uber.models.rider import Rider
from uber.repository.rider import RiderRepository


@pytest.fixture
def rider_repository(session: AsyncSession) -> RiderRepository:
    return RiderRepository(session)


async def test_get_by_id_returns_when_rider_exists(
    session: AsyncSession, rider_repository: RiderRepository
) -> None:
    rider = RiderFactory.build()

    session.add(rider)
    await session.flush()

    result = await rider_repository.get_by_id(rider_id=rider.id)

    assert result is not None
    assert result.id == rider.id


async def test_get_by_id_returns_none_when_not_exists(
    session: AsyncSession, rider_repository: RiderRepository
) -> None:
    rider = RiderFactory.build()

    session.add(rider)
    await session.flush()

    test_id = uuid4()

    result = await rider_repository.get_by_id(rider_id=test_id)

    assert result is None


async def test_create_rider_success(
    session: AsyncSession, rider_repository: RiderRepository
) -> None:
    rider = RiderFactory.build()
    result = await rider_repository.create(rider)
    row_returned = await session.get(Rider, result.id)
    assert row_returned is not None
    assert result is row_returned
