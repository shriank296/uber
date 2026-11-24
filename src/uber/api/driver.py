from collections.abc import Sequence
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from uber.api.dependencies import get_driver_service
from uber.models.enums import DriverStatus
from uber.schemas.driver import RequestDriverSchema, ResponseDriverSchema
from uber.services.driver import DriverService

driver_router = APIRouter(prefix="/drivers", tags=["Drivers"])


@driver_router.post(
    "/",
    response_model=ResponseDriverSchema,
    summary="Register a driver",
    description="Registers a new driver in the system.",
    status_code=status.HTTP_201_CREATED,
)
async def create_rider(
    driver_input: RequestDriverSchema,
    driver_service: Annotated[DriverService, Depends(get_driver_service)],
) -> ResponseDriverSchema:
    driver = await driver_service.create_driver(driver_input)
    return ResponseDriverSchema.model_validate(driver)


@driver_router.get(
    "/available",
    response_model=Sequence[ResponseDriverSchema],
    summary="Get available drivers",
    description="Retrieve available drivers",
)
async def get_available_drivers(
    driver_service: Annotated[DriverService, Depends(get_driver_service)],
) -> Sequence[ResponseDriverSchema]:
    return await driver_service.get_available_drivers()


@driver_router.get(
    "/{driver_id}",
    response_model=ResponseDriverSchema,
    summary="Get a driver",
    description="Retrieve a driver with primary key",
)
async def get_driver(
    driver_id: UUID,
    driver_service: Annotated[DriverService, Depends(get_driver_service)],
) -> ResponseDriverSchema:
    driver = await driver_service.get_driver(driver_id)
    return ResponseDriverSchema.model_validate(driver)


@driver_router.patch(
    "/{driver_id}/status",
    response_model=ResponseDriverSchema,
    summary="Update driver status",
    description="Update driver with given status",
)
async def update_status(
    driver_id: UUID,
    status: DriverStatus,
    driver_service: Annotated[DriverService, Depends(get_driver_service)],
) -> ResponseDriverSchema:
    driver = await driver_service.update_driver_status(driver_id, status)
    return ResponseDriverSchema.model_validate(driver)
