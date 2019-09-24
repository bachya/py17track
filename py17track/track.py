"""Define interaction with an individual package."""
from typing import Callable, Coroutine, List

from .errors import InvalidTrackingNumberError
from .package import Package

API_URL_TRACK: str = "https://t.17track.net/restapi/track"


class Track:  # pylint: disable=too-few-public-methods
    """Define a 17track.net package manager."""

    def __init__(self, request: Callable[..., Coroutine]) -> None:
        """Initialize."""
        self._request: Callable[..., Coroutine] = request

    async def find(self, *tracking_numbers: str) -> list:
        """Get tracking info for one or more tracking numbers."""
        data: dict = {"data": [{"num": num} for num in tracking_numbers]}
        tracking_resp: dict = await self._request("post", API_URL_TRACK, json=data)

        if not tracking_resp.get("dat"):
            raise InvalidTrackingNumberError("Invalid data")

        packages: List[Package] = []
        for info in tracking_resp["dat"]:
            package_info: dict = info.get("track", {})

            if not package_info:
                continue

            kwargs: dict = {
                "destination_country": package_info.get("c"),
                "info_text": package_info.get("z0", {}).get("z"),
                "location": package_info.get("z0", {}).get("c"),
                "origin_country": package_info.get("b"),
                "package_type": package_info.get("d", 0),
                "status": package_info.get("e", 0),
                "tracking_info_language": package_info.get("ln1", "Unknown"),
            }
            packages.append(Package(info["no"], **kwargs))
        return packages
