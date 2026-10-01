# Vehicle Service Python SDK

A Python client library generated from the **Vehicle Service Collection** in Postman.

## Installation

No external dependencies are required — the SDK uses Python's built-in `urllib` module.

Copy the `vehicle_service/` package into your project, or install it in development mode:

```bash
pip install -e .
```

## Quick Start

```python
from vehicle_service import VehicleServiceClient, VehicleCreate, VehicleUpdate

# Initialise the client
client = VehicleServiceClient(
    base_url="https://dceb2547-93d0-4c22-9722-112d408c5351.mock.pstmn.io"
)

# ── Get all vehicles ──────────────────────────────────────────────────
vehicles = client.get_all_vehicles()
for v in vehicles:
    print(v.id, v.nickName, v.make, v.model)

# ── Create a vehicle ──────────────────────────────────────────────────
new_vehicle = client.create_vehicle(VehicleCreate(
    nickName="The Lisa Marie",
    vin="4M2DV11W4RDJ53329",
    make="Mercury",
    model="Villager",
    year="1994",
    miles=159864,
))
print("Created:", new_vehicle.id)

# ── Retrieve a vehicle ────────────────────────────────────────────────
vehicle = client.retrieve_vehicle(vehicle_id=new_vehicle.id)
print("Retrieved:", vehicle.nickName)

# ── Update a vehicle ──────────────────────────────────────────────────
updated = client.update_vehicle(
    vehicle_id=new_vehicle.id,
    payload=VehicleUpdate(miles=160000),
)
print("Updated miles:", updated.miles)

# ── Delete a vehicle ──────────────────────────────────────────────────
client.delete_vehicle(vehicle_id=new_vehicle.id)
print("Deleted vehicle", new_vehicle.id)
```

## API Reference

### `VehicleServiceClient(base_url, api_key=None, timeout=30)`

| Parameter  | Type  | Description                                      |
|------------|-------|--------------------------------------------------|
| `base_url` | `str` | Base URL of the Vehicle Service API              |
| `api_key`  | `str` | Optional API key sent as `x-api-key` header      |
| `timeout`  | `int` | Request timeout in seconds (default `30`)        |

### Methods

| Method | HTTP | Endpoint | Description |
|--------|------|----------|-------------|
| `get_all_vehicles()` | `GET` | `/vehicles` | Return a list of all vehicles |
| `create_vehicle(payload)` | `POST` | `/vehicles` | Create a new vehicle |
| `retrieve_vehicle(vehicle_id)` | `GET` | `/vehicles/:id` | Retrieve a vehicle by ID |
| `update_vehicle(vehicle_id, payload)` | `PATCH` | `/vehicles/:id` | Partially update a vehicle |
| `delete_vehicle(vehicle_id)` | `DELETE` | `/vehicles/:id` | Delete a vehicle by ID |

### Models

#### `VehicleCreate`
| Field | Type | Required |
|-------|------|----------|
| `nickName` | `str` | ✅ |
| `vin` | `str` | ✅ |
| `make` | `str` | ✅ |
| `model` | `str` | ✅ |
| `year` | `str` | ✅ |
| `miles` | `int` | ✅ |

#### `VehicleUpdate`
All fields are optional — only the fields you provide will be sent.

| Field | Type |
|-------|------|
| `nickName` | `str` |
| `vin` | `str` |
| `make` | `str` |
| `model` | `str` |
| `year` | `str` |
| `miles` | `int` |

#### `Vehicle`
Returned by all read/write operations.

| Field | Type |
|-------|------|
| `id` | `int` |
| `nickName` | `str` |
| `vin` | `str` |
| `make` | `str` |
| `model` | `str` |
| `year` | `str` |
| `miles` | `int` |

### Exceptions

| Exception | HTTP Status | Description |
|-----------|-------------|-------------|
| `VehicleServiceError` | any | Base exception |
| `NotFoundError` | 404 | Vehicle not found |
| `ValidationError` | 400 / 422 | Invalid request payload |
| `UnauthorizedError` | 401 | Missing or invalid credentials |
| `ServerError` | 5xx | Server-side error |

## Error Handling

```python
from vehicle_service import VehicleServiceClient
from vehicle_service.exceptions import NotFoundError, ValidationError, VehicleServiceError

client = VehicleServiceClient(base_url="https://your-api-host.com")

try:
    vehicle = client.retrieve_vehicle(vehicle_id=999)
except NotFoundError as e:
    print(f"Vehicle not found: {e}")
except ValidationError as e:
    print(f"Bad request: {e}")
except VehicleServiceError as e:
    print(f"API error [{e.status_code}]: {e}")
```

## Source

Generated from the **Vehicle Service Collection** (ID: `cc0Aa128Fdd80e6823FBE9ff`) in Postman.
