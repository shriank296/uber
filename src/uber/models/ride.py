from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Enum, Float, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID as PUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from uber.models.base import Base
from uber.models.driver import Driver
from uber.models.enums import RideStatus
from uber.models.mixin import TimeStampMixin
from uber.models.rider import Rider


class Ride(TimeStampMixin, Base):
    __tablename__ = "rides"
    id: Mapped[UUID] = mapped_column(
        PUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    rider_id: Mapped[UUID] = mapped_column(
        ForeignKey("riders.id"),
    )
    driver_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("drivers.id"),
    )
    pickup_latitude: Mapped[float] = mapped_column(Float)
    pickup_longitude: Mapped[float] = mapped_column(Float)
    drop_latitude: Mapped[float] = mapped_column(Float)
    drop_longitude: Mapped[float] = mapped_column(Float)
    status: Mapped[RideStatus] = mapped_column(
        Enum(
            RideStatus,
            name="ride_status",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        default=RideStatus.REQUESTED,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    rider: Mapped["Rider"] = relationship(back_populates="rides")
    driver: Mapped["Driver | None"] = relationship(back_populates="rides")
