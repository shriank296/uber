from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from tests.factories.ride import RideFactory
from tests.factories.rider import RiderFactory
from uber.models.ride import Ride
from uber.repository.ride import RideRepository


async def test_get_by_id_returns_when_ride_exists(
    session: AsyncSession, ride_repository: RideRepository
) -> None:
    ride = RideFactory.build()

    session.add(ride)
    await session.flush()

    result = await ride_repository.get_by_id(ride_id=ride.id)

    assert result is not None
    assert result.id == ride.id


async def test_create_rider_success(
    session: AsyncSession, ride_repository: RideRepository
) -> None:
    ride = RideFactory.build()
    result = await ride_repository.create(ride)
    row_returned = await session.get(Ride, result.id)
    assert row_returned is not None
    assert result is row_returned


async def test_get_rides_by_rider(
    session: AsyncSession, ride_repository: RideRepository
) -> None:
    rider = RiderFactory.build()
    rides = RideFactory.build_batch(3, rider=rider)
    other_ride = RideFactory.build()

    session.add_all([*rides, other_ride])
    await session.flush()

    result = await ride_repository.get_rides_by_rider(rider.id)

    assert len(result) == 3
    assert {ride.id for ride in rides} == {ride.id for ride in result}


async def test_get_rides_by_rider_returns_empty_list(
    session: AsyncSession, ride_repository: RideRepository
) -> None:

    result = await ride_repository.get_rides_by_rider(uuid4())

    assert result == []
