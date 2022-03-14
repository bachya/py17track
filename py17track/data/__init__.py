"""Define data maps."""

import json
import os
from typing import Dict

from ..errors import SeventeenTrackError


def _load_json_list(filename: str) -> list:
    """Load json data into list."""
    result: list = []
    with open(os.path.join(os.path.dirname(__file__), filename), "r") as f:
        for row in json.load(f):
            result.append(row)
    return result


CARRIER_MAP: Dict[int, str] = {
    row.get("key"): row.get("_name") for row in _load_json_list("carrier.all.json")
}


def get_carrier_key(name: str) -> int:
    """Get carrier key from name."""
    for key, carrier in CARRIER_MAP.items():
        if carrier.lower() == name.lower():
            return key
    raise SeventeenTrackError(f"Could not map carrier {name} to id")
