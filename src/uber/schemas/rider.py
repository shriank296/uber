from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pydantic.alias_generators import to_camel


class BaseRider(BaseModel):
    first_name: Annotated[str, Field(min_length=1, max_length=100)]
    last_name: Annotated[str | None, Field(min_length=1, max_length=100)] = None
    email: EmailStr

    model_config = ConfigDict(
        alias_generator=to_camel,
        validate_by_name=True,
        extra="forbid",
    )


class RequestRiderSchema(BaseRider):
    pass


class ResponseRiderSchema(BaseRider):
    id: UUID
    model_config = ConfigDict(
        serialize_by_alias=True,
        from_attributes=True,
    )
