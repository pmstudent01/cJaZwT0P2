"""
Vehicle Service CLI Application
================================
A beginner-friendly command-line app for managing vehicles
via the Vehicle Service API.

Usage:
    python run.py

Environment Variables:
    BASE_URL  — Override the default API base URL.
                Default: https://dceb2547-93d0-4c22-9722-112d408c5351.mock.pstmn.io
"""

import os
import sys

# ---------------------------------------------------------------------------
# Make sure the local SDK is importable regardless of where the script runs.
# ---------------------------------------------------------------------------
_SDK_PATH = os.path.join(os.path.dirname(__file__), "..", "sdk")
sys.path.insert(0, os.path.abspath(_SDK_PATH))

from vehicle_service import VehicleServiceClient, VehicleCreate, VehicleUpdate
from vehicle_service.exceptions import (
    VehicleServiceError,
    NotFoundError,
    ValidationError,
    UnauthorizedError,
    ServerError,
)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
DEFAULT_BASE_URL = "https://dceb2547-93d0-4c22-9722-112d408c5351.mock.pstmn.io"
BASE_URL = os.environ.get("BASE_URL", DEFAULT_BASE_URL)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

DIVIDER = "-" * 50


def print_divider():
    print(DIVIDER)


def print_vehicle(vehicle):
    """Pretty-print a single Vehicle object."""
    print_divider()
    print(f"  ID       : {vehicle.id}")
    print(f"  Nickname : {vehicle.nickName}")
    print(f"  VIN      : {vehicle.vin}")
    print(f"  Make     : {vehicle.make}")
    print(f"  Model    : {vehicle.model}")
    print(f"  Year     : {vehicle.year}")
    print(f"  Miles    : {vehicle.miles}")
    print_divider()


def prompt(label, required=True, default=None):
    """
    Prompt the user for input.

    Args:
        label    : The field name shown to the user.
        required : If True, keep asking until a non-empty value is entered.
        default  : Optional default value shown in brackets.

    Returns:
        The user's input string, or the default if nothing was entered.
    """
    hint = f" [{default}]" if default is not None else ""
    while True:
        value = input(f"  {label}{hint}: ").strip()
        if value:
            return value
        if default is not None:
            return default
        if not required:
            return None
        print(f"  ⚠  '{label}' is required. Please enter a value.")


def handle_error(err):
    """Print a friendly error message for known SDK exceptions."""
    if isinstance(err, NotFoundError):
        print(f"\n  ❌  Not found: {err}")
    elif isinstance(err, ValidationError):
        print(f"\n  ❌  Validation error: {err}")
    elif isinstance(err, UnauthorizedError):
        print(f"\n  ❌  Unauthorized: {err}")
    elif isinstance(err, ServerError):
        print(f"\n  ❌  Server error: {err}")
    elif isinstance(err, VehicleServiceError):
        print(f"\n  ❌  API error: {err}")
    else:
        print(f"\n  ❌  Unexpected error: {err}")


# ---------------------------------------------------------------------------
# CRUD operations
# ---------------------------------------------------------------------------

def list_vehicles(client):
    """Fetch and display all vehicles."""
    print("\n📋  Fetching all vehicles...\n")
    try:
        vehicles = client.get_all_vehicles()
        if not vehicles:
            print("  (No vehicles found)")
            return
        print(f"  Found {len(vehicles)} vehicle(s):\n")
        for v in vehicles:
            print_vehicle(v)
    except VehicleServiceError as err:
        handle_error(err)


def get_vehicle(client):
    """Fetch and display a single vehicle by ID."""
    print("\n🔍  Get Vehicle by ID\n")
    vehicle_id = prompt("Vehicle ID")
    try:
        vehicle = client.retrieve_vehicle(vehicle_id)
        print("\n  Vehicle details:")
        print_vehicle(vehicle)
    except VehicleServiceError as err:
        handle_error(err)


def create_vehicle(client):
    """Prompt for all fields and create a new vehicle."""
    print("\n➕  Create a New Vehicle\n")
    print("  Please enter the details for the new vehicle:")
    print()

    nick_name = prompt("Nickname")
    vin       = prompt("VIN")
    make      = prompt("Make")
    model     = prompt("Model")
    year      = prompt("Year")
    miles     = prompt("Miles")

    new_vehicle = VehicleCreate(
        nickName=nick_name,
        vin=vin,
        make=make,
        model=model,
        year=year,
        miles=miles,
    )

    try:
        created = client.create_vehicle(new_vehicle)
        print("\n  ✅  Vehicle created successfully!")
        print_vehicle(created)
    except VehicleServiceError as err:
        handle_error(err)


def update_vehicle(client):
    """Prompt for an ID and any fields to update, then send the update."""
    print("\n✏️   Update a Vehicle\n")
    vehicle_id = prompt("Vehicle ID to update")

    print("\n  Enter new values (press Enter to skip a field and keep its current value):\n")

    nick_name = prompt("Nickname", required=False)
    vin       = prompt("VIN",      required=False)
    make      = prompt("Make",     required=False)
    model     = prompt("Model",    required=False)
    year      = prompt("Year",     required=False)
    miles     = prompt("Miles",    required=False)

    # Build the update payload with only the fields the user provided.
    update_data = {}
    if nick_name: update_data["nickName"] = nick_name
    if vin:       update_data["vin"]      = vin
    if make:      update_data["make"]     = make
    if model:     update_data["model"]    = model
    if year:      update_data["year"]     = year
    if miles:     update_data["miles"]    = miles

    if not update_data:
        print("\n  ℹ️   No fields entered — nothing to update.")
        return

    vehicle_update = VehicleUpdate(**update_data)

    try:
        updated = client.update_vehicle(vehicle_id, vehicle_update)
        print("\n  ✅  Vehicle updated successfully!")
        print_vehicle(updated)
    except VehicleServiceError as err:
        handle_error(err)


def delete_vehicle(client):
    """Prompt for an ID and delete the vehicle."""
    print("\n🗑️   Delete a Vehicle\n")
    vehicle_id = prompt("Vehicle ID to delete")

    confirm = input(f"\n  Are you sure you want to delete vehicle '{vehicle_id}'? (yes/no): ").strip().lower()
    if confirm not in ("yes", "y"):
        print("  Deletion cancelled.")
        return

    try:
        client.delete_vehicle(vehicle_id)
        print(f"\n  ✅  Vehicle '{vehicle_id}' deleted successfully.")
    except VehicleServiceError as err:
        handle_error(err)


# ---------------------------------------------------------------------------
# Menu
# ---------------------------------------------------------------------------

MENU = """
╔══════════════════════════════════════╗
║     🚗  Vehicle Service Manager      ║
╠══════════════════════════════════════╣
║  1. List all vehicles                ║
║  2. Get a vehicle by ID              ║
║  3. Create a new vehicle             ║
║  4. Update a vehicle                 ║
║  5. Delete a vehicle                 ║
║  6. Exit                             ║
╚══════════════════════════════════════╝
"""

ACTIONS = {
    "1": list_vehicles,
    "2": get_vehicle,
    "3": create_vehicle,
    "4": update_vehicle,
    "5": delete_vehicle,
}


def main():
    """Main entry point — initialise the client and run the interactive menu."""
    print(f"\n  Connecting to: {BASE_URL}\n")
    client = VehicleServiceClient(base_url=BASE_URL)

    while True:
        print(MENU)
        choice = input("  Enter your choice (1-6): ").strip()

        if choice == "6":
            print("\n  👋  Goodbye!\n")
            break
        elif choice in ACTIONS:
            ACTIONS[choice](client)
        else:
            print("\n  ⚠️   Invalid choice. Please enter a number between 1 and 6.")

        input("\n  Press Enter to return to the menu...")


if __name__ == "__main__":
    main()
