"""
Data models for the Vehicle Service SDK.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Vehicle:
    """Represents a vehicle resource returned by the API."""

    id: Optional[int] = None
    nickName: Optional[str] = None
    vin: Optional[str] = None
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[str] = None
    miles: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Vehicle":
        """Create a Vehicle instance from a dictionary."""
        return cls(
            id=data.get("id"),
            nickName=data.get("nickName"),
            vin=data.get("vin"),
            make=data.get("make"),
            model=data.get("model"),
            year=data.get("year"),
            miles=data.get("miles"),
        )

    def to_dict(self) -> dict:
        """Convert the Vehicle instance to a dictionary."""
        return {k: v for k, v in self.__dict__.items() if v is not None}


@dataclass
class VehicleCreate:
    """Payload for creating a new vehicle."""

    nickName: str
    vin: str
    make: str
    model: str
    year: str
    miles: int

    def to_dict(self) -> dict:
        """Convert the VehicleCreate instance to a dictionary."""
        return {
            "nickName": self.nickName,
            "vin": self.vin,
            "make": self.make,
            "model": self.model,
            "year": self.year,
            "miles": self.miles,
        }


@dataclass
class VehicleUpdate:
    """Payload for updating an existing vehicle (all fields optional)."""

    nickName: Optional[str] = None
    vin: Optional[str] = None
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[str] = None
    miles: Optional[int] = None

    def to_dict(self) -> dict:
        """Convert the VehicleUpdate instance to a dictionary, omitting None values."""
        return {k: v for k, v in self.__dict__.items() if v is not None}
