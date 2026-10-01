"""
Main client for the Vehicle Service SDK.

Generated from the Vehicle Service Collection.
Base URL: {{baseUrl}}/vehicles
"""

import json
from typing import List, Optional
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode

from .models import Vehicle, VehicleCreate, VehicleUpdate
from .exceptions import (
    VehicleServiceError,
    NotFoundError,
    ValidationError,
    UnauthorizedError,
    ServerError,
)


class VehicleServiceClient:
    """
    Python client for the Vehicle Service API.

    Usage:
        client = VehicleServiceClient(base_url="https://your-api-host.com")

        # Get all vehicles
        vehicles = client.get_all_vehicles()

        # Create a vehicle
        new_vehicle = client.create_vehicle(VehicleCreate(
            nickName="The Lisa Marie",
            vin="4M2DV11W4RDJ53329",
            make="Mercury",
            model="Villager",
            year="1994",
            miles=159864,
        ))

        # Retrieve a vehicle by ID
        vehicle = client.retrieve_vehicle(vehicle_id=1)

        # Update a vehicle
        updated = client.update_vehicle(vehicle_id=1, payload=VehicleUpdate(miles=160000))

        # Delete a vehicle
        client.delete_vehicle(vehicle_id=1)
    """

    def __init__(self, base_url: str, api_key: str = None, timeout: int = 30):
        """
        Initialize the VehicleServiceClient.

        Args:
            base_url: The base URL of the Vehicle Service API
                      (e.g. "https://dceb2547-93d0-4c22-9722-112d408c5351.mock.pstmn.io").
            api_key:  Optional API key sent as the 'x-api-key' header.
            timeout:  Request timeout in seconds (default: 30).
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_headers(self, extra: dict = None) -> dict:
        headers = {"Accept": "application/json"}
        if self.api_key:
            headers["x-api-key"] = self.api_key
        if extra:
            headers.update(extra)
        return headers

    def _handle_error(self, error: HTTPError) -> None:
        body = {}
        try:
            body = json.loads(error.read().decode("utf-8"))
        except Exception:
            pass

        status = error.code
        message = body.get("message", str(error.reason))

        if status == 400:
            raise ValidationError(message, status_code=status, response=body)
        elif status == 401:
            raise UnauthorizedError(message, status_code=status, response=body)
        elif status == 404:
            raise NotFoundError(message, status_code=status, response=body)
        elif status == 422:
            raise ValidationError(message, status_code=status, response=body)
        elif status >= 500:
            raise ServerError(message, status_code=status, response=body)
        else:
            raise VehicleServiceError(message, status_code=status, response=body)

    def _request(self, method: str, path: str, body: dict = None) -> dict:
        url = f"{self.base_url}{path}"
        data = None
        headers = self._build_headers()

        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"

        req = Request(url, data=data, headers=headers, method=method)
        try:
            with urlopen(req, timeout=self.timeout) as response:
                raw = response.read().decode("utf-8")
                if raw:
                    return json.loads(raw)
                return {}
        except HTTPError as e:
            self._handle_error(e)
        except URLError as e:
            raise VehicleServiceError(f"Connection error: {e.reason}")

    # ------------------------------------------------------------------
    # API methods
    # ------------------------------------------------------------------

    def get_all_vehicles(self) -> List[Vehicle]:
        """
        GET /vehicles
        Retrieve a list of all vehicles.

        Returns:
            A list of Vehicle objects.

        Raises:
            VehicleServiceError: On any API or network error.
        """
        response = self._request("GET", "/vehicles")
        if isinstance(response, list):
            return [Vehicle.from_dict(item) for item in response]
        # Some APIs wrap the list in a key
        items = response.get("vehicles", response.get("data", [response]))
        return [Vehicle.from_dict(item) for item in items]

    def create_vehicle(self, payload: VehicleCreate) -> Vehicle:
        """
        POST /vehicles
        Create a new vehicle.

        Args:
            payload: A VehicleCreate object with the vehicle details.

        Returns:
            The created Vehicle object.

        Raises:
            ValidationError: If the payload is invalid (HTTP 400/422).
            VehicleServiceError: On any other API or network error.
        """
        response = self._request("POST", "/vehicles", body=payload.to_dict())
        return Vehicle.from_dict(response)

    def retrieve_vehicle(self, vehicle_id: int) -> Vehicle:
        """
        GET /vehicles/:id
        Retrieve a single vehicle by its ID.

        Args:
            vehicle_id: The integer ID of the vehicle.

        Returns:
            The Vehicle object.

        Raises:
            NotFoundError: If no vehicle with the given ID exists (HTTP 404).
            VehicleServiceError: On any other API or network error.
        """
        response = self._request("GET", f"/vehicles/{vehicle_id}")
        return Vehicle.from_dict(response)

    def update_vehicle(self, vehicle_id: int, payload: VehicleUpdate) -> Vehicle:
        """
        PATCH /vehicles/:id
        Partially update an existing vehicle.

        Args:
            vehicle_id: The integer ID of the vehicle to update.
            payload:    A VehicleUpdate object with the fields to change.

        Returns:
            The updated Vehicle object.

        Raises:
            NotFoundError:   If no vehicle with the given ID exists (HTTP 404).
            ValidationError: If the payload is invalid (HTTP 400/422).
            VehicleServiceError: On any other API or network error.
        """
        response = self._request("PATCH", f"/vehicles/{vehicle_id}", body=payload.to_dict())
        return Vehicle.from_dict(response)

    def delete_vehicle(self, vehicle_id: int) -> None:
        """
        DELETE /vehicles/:id
        Delete a vehicle by its ID.

        Args:
            vehicle_id: The integer ID of the vehicle to delete.

        Returns:
            None (HTTP 204 No Content on success).

        Raises:
            NotFoundError: If no vehicle with the given ID exists (HTTP 404).
            VehicleServiceError: On any other API or network error.
        """
        self._request("DELETE", f"/vehicles/{vehicle_id}")
