
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from tests.factories.driver import DriverFactory
from uber.models.enums import DriverStatus
from uber.repository.driver import DriverRepository


@pytest.fixture
def driver_repository(session: AsyncSession) -> DriverRepository:
    return DriverRepository(session)


async def test_get_by_id_returns_when_driver_exists(
    session: AsyncSession, driver_repository: DriverRepository
) -> None:
    driver = DriverFactory.build()

    session.add(driver)
    await session.flush()

    result = await driver_repository.get_by_id(driver_id=driver.id)

    assert result is not None
    assert result.id == driver.id


async def test_get_all_available_drivers(
    session: AsyncSession, driver_repository: DriverRepository
) -> None:
    available_drivers = DriverFactory.build_batch(5, status=DriverStatus.AVAILABLE)
    offline_drivers = DriverFactory.build_batch(5, status=DriverStatus.OFFLINE)

    session.add_all(available_drivers + offline_drivers)
    await session.flush()

    result = await driver_repository.get_available_drivers()

    assert len(result) == 5
    assert all(driver.status == DriverStatus.AVAILABLE for driver in result)
