from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from uber.api.dependencies import get_rider_service
from uber.schemas.base import PaginatedResponse
from uber.schemas.rider import RequestRiderSchema, ResponseRiderSchema
from uber.services.rider import RiderService

rider_router = APIRouter(prefix="/riders", tags=["Riders"])


@rider_router.post(
    "/",
    response_model=ResponseRiderSchema,
    summary="Create a rider",
    description="Registers a new rider in the system.",
    status_code=status.HTTP_201_CREATED,
)
async def create_rider(
    rider_input: RequestRiderSchema,
    rider_service: Annotated[RiderService, Depends(get_rider_service)],
) -> ResponseRiderSchema:
    rider = await rider_service.create_rider(rider_input)
    return ResponseRiderSchema.model_validate(rider)


@rider_router.get(
    "/{rider_id}",
    response_model=ResponseRiderSchema,
    summary="Get a rider",
    description="Retrieve a rider with primary key",
)
async def get_rider(
    rider_id: UUID,
    rider_service: Annotated[RiderService, Depends(get_rider_service)],
) -> ResponseRiderSchema:
    return await rider_service.get_rider(rider_id)


@rider_router.get(
    "/",
    response_model=PaginatedResponse[ResponseRiderSchema],
    summary="Get all riders.",
    description="Paginated endpoints to get all riders.",
)
async def get_riders_paginated(
    rider_service: Annotated[RiderService, Depends(get_rider_service)],
    page_number: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
) -> PaginatedResponse[ResponseRiderSchema]:
    return await rider_service.get_all_riders_paginated(
        page_number=page_number, page_size=page_size
    )
