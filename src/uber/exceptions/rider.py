from uuid import UUID

from uber.exceptions.base import AppException


class RiderNotFound(AppException):
    def __init__(self, rider_id: UUID):
        self.rider_id = rider_id
        super().__init__(
            message="Rider not found",
            code="RIDER_NOT_FOUND",
            status_code=404,
        )


class DuplicateRiderEmail(AppException):
    def __init__(self, email: str):
        self.email = email
        super().__init__(
            message="Rider with this email id already exists",
            code="DUPLICATE_EMAIL",
            status_code=409,
        )
