from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Enum, Float, String
from sqlalchemy.dialects.postgresql import UUID as PUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from uber.models.base import Base
from uber.models.enums import DriverStatus
from uber.models.mixin import TimeStampMixin

if TYPE_CHECKING:
    from uber.models.ride import Ride


class Driver(TimeStampMixin, Base):
    __tablename__ = "drivers"
    id: Mapped[UUID] = mapped_column(
        PUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    first_name: Mapped[str] = mapped_column(String(40))
    last_name: Mapped[str | None] = mapped_column(String(40))
    status: Mapped[DriverStatus] = mapped_column(
        Enum(
            DriverStatus,
            name="driver_status",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
    )
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    rides: Mapped[list["Ride"]] = relationship(back_populates="driver")
