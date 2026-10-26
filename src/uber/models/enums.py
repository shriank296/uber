from enum import StrEnum


class DriverStatus(StrEnum):
    AVAILABLE = "available"
    ON_TRIP = "on_trip"
    OFFLINE = "offline"


class RideStatus(StrEnum):
    REQUESTED = "requested"
    ACCEPTED = "accepted"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
