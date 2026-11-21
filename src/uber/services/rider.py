import logging
import math
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from uber.exceptions.rider import DuplicateRiderEmail, RiderNotFound
from uber.models.rider import Rider
from uber.repository.rider import RiderRepository
from uber.schemas.base import PaginatedResponse
from uber.schemas.rider import RequestRiderSchema, ResponseRiderSchema

logger = logging.getLogger(__name__)


class RiderService:
    def __init__(
        self,
        rider_repository: RiderRepository,
        session: AsyncSession,
    ) -> None:
        self.rider_repository = rider_repository
        self.session = session

    async def create_rider(
        self,
        rider_data: RequestRiderSchema,
    ) -> Rider:
        rider = Rider(**rider_data.model_dump())
        try:
            async with self.session.begin():
                created_rider = await self.rider_repository.create(rider)
        except IntegrityError as exc:
            if "uq_riders_email" in exc.orig.__cause__.constraint_name:  # type: ignore
                raise DuplicateRiderEmail(email=rider.email) from exc
            raise

        return created_rider

    async def get_rider(self, rider_id: UUID) -> Rider:
        retrieved_rider = await self.rider_repository.get_by_id(rider_id)
        if retrieved_rider is None:
            raise RiderNotFound(rider_id)
        return retrieved_rider

    async def get_all_riders_paginated(
        self,
        page_number: int,
        page_size: int,
    ) -> PaginatedResponse[ResponseRiderSchema]:
        total_riders = await self.rider_repository.count_all_riders()

        riders = await self.rider_repository.get_all_riders_paginated(
            page_number,
            page_size,
        )

        total_pages = math.ceil(total_riders / page_size)

        riders_schema = [ResponseRiderSchema.model_validate(rider) for rider in riders]

        return PaginatedResponse[ResponseRiderSchema](
            items=riders_schema,
            page_number=page_number,
            page_size=page_size,
            total_items=total_riders,
            total_pages=total_pages,
        )
