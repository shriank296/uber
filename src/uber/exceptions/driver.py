from uuid import UUID

from uber.exceptions.base import AppException


class DriverNotFound(AppException):
    def __init__(self, driver_id: UUID) -> None:
        self.driver_id = driver_id
        super().__init__(
            message="Driver not found",
            code="DRIVER_NOT_FOUND",
            status_code=404,
        )


class DriverAlreadyOnTrip(AppException):
    def __init__(self, driver_id: UUID) -> None:
        self.driver_id = driver_id
        super().__init__(
            message="Driver is already on a trip",
            code="DRIVER_ALREADY_ON_TRIP",
            status_code=409,
        )


class NoAvailableDriversFound(AppException):
    def __init__(self) -> None:
        super().__init__(
            message="No drivers are available",
            code="AVAILABLE_DRIVER_NOT_FOUND",
            status_code=404,
        )
