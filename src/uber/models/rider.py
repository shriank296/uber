from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID as PUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from uber.models.base import Base
from uber.models.mixin import TimeStampMixin

if TYPE_CHECKING:
    from uber.models.ride import Ride


class Rider(TimeStampMixin, Base):
    __tablename__ = "riders"
    id: Mapped[UUID] = mapped_column(
        PUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    first_name: Mapped[str] = mapped_column(String(40))
    last_name: Mapped[str | None] = mapped_column(String(40))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    rides: Mapped[list["Ride"]] = relationship(back_populates="rider")
