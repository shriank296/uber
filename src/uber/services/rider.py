import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from uber.exceptions.rider import DuplicateRiderEmail
from uber.models.rider import Rider
from uber.repository.rider import RiderRepository
from uber.schemas.rider import RequestRiderSchema

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
            if "uq_riders_email" in exc.orig.__cause__.constraint_name:
                raise DuplicateRiderEmail(email=rider.email) from exc
            raise

        return created_rider
