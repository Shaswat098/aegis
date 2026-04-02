from typing import Dict

LOCATION_MAP: Dict[str, int] = {
    "mumbai": 1,
    "delhi": 2,
    "chennai": 3,
    "bangalore": 4,
    "kolkata": 5,
}

def encode_location(location: str) -> int:

    location = location.strip().lower()

    return LOCATION_MAP.get(location, 0)