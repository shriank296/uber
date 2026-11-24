from collections.abc import Sequence
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from uber.exceptions.driver import DriverNotFound
from uber.models.driver import Driver
from uber.models.enums import DriverStatus
from uber.repository.driver import DriverRepository
from uber.schemas.driver import RequestDriverSchema, ResponseDriverSchema


class DriverService:
    def __init__(
        self,
        driver_repository: DriverRepository,
        session: AsyncSession,
    ) -> None:
        self.driver_repository = driver_repository
        self.session = session

    async def create_driver(
        self,
        driver_data: RequestDriverSchema,
    ) -> Driver:
        driver = Driver(**driver_data.model_dump())
        async with self.session.begin():
            created_driver = await self.driver_repository.create(driver)
        return created_driver

    async def get_driver(self, driver_id: UUID) -> ResponseDriverSchema:
        retrieved_driver = await self.driver_repository.get_by_id(driver_id)
        if retrieved_driver is None:
            raise DriverNotFound(driver_id)
        return ResponseDriverSchema.model_validate(retrieved_driver)

    async def get_available_drivers(self) -> Sequence[ResponseDriverSchema]:
        available_drivers = await self.driver_repository.get_available_drivers()
        if available_drivers is None:
            return []
        return [
            ResponseDriverSchema.model_validate(available_driver)
            for available_driver in available_drivers
        ]

    async def update_driver_status(
        self, driver_id: UUID, status: DriverStatus
    ) -> ResponseDriverSchema:
        async with self.session.begin():
            updated_driver = await self.driver_repository.update_status(
                driver_id, status
            )
            if updated_driver is None:
                raise DriverNotFound(driver_id=driver_id)
            response = ResponseDriverSchema.model_validate(updated_driver)
        return response
