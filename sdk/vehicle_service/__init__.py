"""
Vehicle Service Python SDK
Generated from the Vehicle Service Collection

This SDK provides a Python client for interacting with the Vehicle Service API.
"""

from .client import VehicleServiceClient
from .models import Vehicle, VehicleCreate, VehicleUpdate
from .exceptions import VehicleServiceError, NotFoundError, ValidationError

__version__ = "1.0.0"
__all__ = [
    "VehicleServiceClient",
    "Vehicle",
    "VehicleCreate",
    "VehicleUpdate",
    "VehicleServiceError",
    "NotFoundError",
    "ValidationError",
]
