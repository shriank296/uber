from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from uber.models.enums import DriverStatus


class BaseDriver(BaseModel):
    first_name: Annotated[str, Field(min_length=1, max_length=100)]
    last_name: Annotated[str | None, Field(min_length=1, max_length=100)] = None
    status: DriverStatus
    latitude: Annotated[float, Field(ge=-90.0, le=90.0, allow_inf_nan=False)]
    longitude: Annotated[float, Field(ge=-180.0, le=180.0, allow_inf_nan=False)]

    model_config = ConfigDict(
        alias_generator=to_camel,
        validate_by_name=True,
        extra="forbid",
    )


class RequestDriverSchema(BaseDriver):
    pass


class ResponseDriverSchema(BaseDriver):
    id: UUID
    model_config = ConfigDict(
        serialize_by_alias=True,
        from_attributes=True,
    )
