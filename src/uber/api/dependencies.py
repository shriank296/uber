from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from uber.database import Database
from uber.repository.ride import RideRepository
from uber.services.rider import RiderService


async def get_db(request: Request):
    return request.app.state.database


async def get_session(database: Annotated[Database, Depends(get_db)]):
    async for session in database.get_async_session():
        yield session


async def get_rider_repository(session: Annotated[AsyncSession, Depends(get_session)]):
    return RideRepository(session)


async def get_rider_service(
    rider_repository: Annotated[RideRepository, Depends(get_rider_repository)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    return RiderService(rider_repository, session)
