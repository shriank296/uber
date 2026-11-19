from collections.abc import Sequence
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class PaginatedResponse[T](BaseModel):
    items: Sequence[T]
    page_number: Annotated[int, Field(ge=1)]
    page_size: Annotated[int, Field(ge=1)]
    total_items: Annotated[int, Field(ge=0)]
    total_pages: Annotated[int, Field(ge=0)]

    model_config = ConfigDict(
        alias_generator=to_camel,
        serialize_by_alias=True,
        validate_by_name=True,
    )
