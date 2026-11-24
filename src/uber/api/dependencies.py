from collections.abc import AsyncGenerator
from typing import Annotated, cast

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from uber.database import Database
from uber.repository.driver import DriverRepository
from uber.repository.rider import RiderRepository
from uber.services.driver import DriverService
from uber.services.rider import RiderService


async def get_db(request: Request) -> Database:
    return cast(Database, request.app.state.database)


async def get_session(
    database: Annotated[Database, Depends(get_db)],
) -> AsyncGenerator[AsyncSession]:
    async for session in database.get_async_session():
        yield session


async def get_rider_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> RiderRepository:
    return RiderRepository(session)


async def get_driver_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> DriverRepository:
    return DriverRepository(session)


async def get_rider_service(
    rider_repository: Annotated[RiderRepository, Depends(get_rider_repository)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> RiderService:
    return RiderService(rider_repository, session)


async def get_driver_service(
    driver_repository: Annotated[DriverRepository, Depends(get_driver_repository)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> DriverService:
    return DriverService(driver_repository, session)
