import math
import os

import requests

from app.automation.exceptions import AutomationValidationError


def geocode_address(address: str) -> tuple[float, float]:
    """Return (latitude, longitude) for an address using Geoapify."""
    api_key = os.getenv("GEOAPIFY_API_KEY")
    if not api_key:
        raise AutomationValidationError(
            "Geocoding is not configured. Set GEOAPIFY_API_KEY."
        )

    try:
        response = requests.get(
            "https://api.geoapify.com/v1/geocode/autocomplete",
            params={"text": address, "apiKey": api_key},
            headers={"Accept": "application/json"},
            timeout=10,
        )
        response.raise_for_status()
        features = response.json().get("features", [])
    except (requests.RequestException, ValueError) as exc:
        raise AutomationValidationError(
            "Unable to geocode the address."
        ) from exc

    if not features:
        raise AutomationValidationError("No location was found for the address.")

    coordinates = features[0].get("geometry", {}).get("coordinates", [])
    if len(coordinates) < 2:
        raise AutomationValidationError("Geocoding returned invalid coordinates.")

    try:
        longitude, latitude = map(float, coordinates[:2])
    except (TypeError, ValueError) as exc:
        raise AutomationValidationError("Geocoding returned invalid coordinates.") from exc

    if (
        not math.isfinite(latitude)
        or not math.isfinite(longitude)
        or not -90 <= latitude <= 90
        or not -180 <= longitude <= 180
    ):
        raise AutomationValidationError("Geocoding returned out-of-range coordinates.")

    return latitude, longitude