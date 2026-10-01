"""
Custom exceptions for the Vehicle Service SDK.
"""


class VehicleServiceError(Exception):
    """Base exception for all Vehicle Service SDK errors."""

    def __init__(self, message: str, status_code: int = None, response: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response

    def __str__(self):
        if self.status_code:
            return f"[HTTP {self.status_code}] {super().__str__()}"
        return super().__str__()


class NotFoundError(VehicleServiceError):
    """Raised when a requested vehicle resource is not found (HTTP 404)."""
    pass


class ValidationError(VehicleServiceError):
    """Raised when the request payload fails validation (HTTP 400/422)."""
    pass


class UnauthorizedError(VehicleServiceError):
    """Raised when the request is not authorized (HTTP 401)."""
    pass


class ServerError(VehicleServiceError):
    """Raised when the server returns a 5xx error."""
    pass
