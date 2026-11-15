from typing import Annotated

from fastapi import APIRouter, Depends, status

from uber.api.dependencies import get_rider_service
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
):
    rider = await rider_service.create_rider(rider_input)
    return ResponseRiderSchema.model_validate(rider)
