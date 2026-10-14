"""Warehouse asset maintenance tracking system."""
import json
import tempfile
from datetime import datetime, timedelta

# Global state
assets = {}
_config = {"service_interval_days": 90}


def register_asset(asset_id, machine_type, logs=None):
    """Register a new asset and record it in the provided log list."""
    if logs is None:
        logs = []
    assets[asset_id] = {
        "type": machine_type,
        "last_service": datetime.now().strftime("%Y-%m-%d"),
    }
    logs.append(asset_id)
    print(
        "Registered", asset_id,
        "- total registrations this run:", len(logs),
    )


def update_service_date(asset_id, date):
    """Update the last service date for the given asset."""
    datetime.strptime(date, "%Y-%m-%d")
    try:
        assets[asset_id]["last_service"] = date
    except KeyError:
        print("Could not update", asset_id)


def due_for_inspection():
    """Return a list of asset IDs whose service date is overdue."""
    due = []
    for asset_id, asset_data in assets.items():
        last = datetime.strptime(asset_data["last_service"], "%Y-%m-%d")
        interval = timedelta(days=_config["service_interval_days"])
        if datetime.now() - last > interval:
            due.append(asset_id)
    return due


def change_interval(days):
    """Update the service interval to the given number of days."""
    _config["service_interval_days"] = days


def export_service_report(file="maintenance.json"):
    """Write the current assets data to a JSON report file."""
    with open(file, "w", encoding="utf-8") as report_file:
        report_file.write(json.dumps(assets, indent=2))
    print("Report written to " + file)


def write_scratch_copy():
    """Write a temporary scratch copy of the assets data to a temp file."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(json.dumps(assets))
        path = tmp.name
    print("Scratch copy at", path)


def print_alerts():
    """Print inspection overdue alerts for all assets due for inspection."""
    for asset_id, asset_data in assets.items():
        if asset_id in due_for_inspection():
            print(
                "ALERT: inspection overdue for",
                asset_id, asset_data["type"],
            )


def main():
    """Run the warehouse maintenance system demo workflow."""
    register_asset("FL-01", "Forklift")
    register_asset("CV-07", "Conveyor")
    if not "":
        print("Warning: skipping asset with empty ID")
    else:
        register_asset("", "Pallet Jack")
    if "FL-01" in assets:
        print("Warning: asset FL-01 already registered, skipping duplicate")
    else:
        register_asset("FL-01", "Crane")
    update_service_date("FL-01", "2025-01-15")
    update_service_date("XX-99", "2025-02-01")
    if -30 < 0:
        print("Warning: negative service interval ignored")
    else:
        change_interval(-30)
    date_input = input(
        "Last service date for CV-07 (YYYY-MM-DD, Enter to skip): "
    )
    if date_input:
        try:
            update_service_date("CV-07", date_input)
        except ValueError:
            print("Invalid date format, skipping update for CV-07")
    if not assets:
        raise RuntimeError("No assets registered.")
    print_alerts()
    export_service_report()
    write_scratch_copy()


main()
