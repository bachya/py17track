"""Define interaction with a user profile."""
import logging
from typing import Callable, Coroutine, List, Optional, Union

from ..data import get_carrier_key
from ..errors import InvalidTrackingNumberError
from ..package import PACKAGE_STATUS_MAP, Package
from ..profile import Profile

_LOGGER: logging.Logger = logging.getLogger(__name__)

V1_API_URL: str = "https://api.17track.net/track/v1"


class ProfileV1(Profile):
    """Define a 17track.net profile manager."""

    def __init__(self, request: Callable[..., Coroutine]) -> None:
        """Initialize."""
        self._request: Callable[..., Coroutine] = request
        self._api_token: Optional[str] = None

    def login(self, api_token: str) -> None:
        """Set api_token."""
        self._api_token = api_token

    async def packages(
        self,
        package_state: Union[int, str] = "",
        show_archived: bool = False,
        tz: str = "UTC",
    ) -> list:
        """Get the list of packages associated with the account."""
        track_list: dict = await self._get_track_list(
            package_state=package_state, show_archived=show_archived
        )
        tracking_request: list = []

        for t in track_list.get("data", {}).get("accepted", []):
            tracking_request.append({"number": t["number"], "carrier": t["w1"]})

        packages_resp: dict = await self._request(
            "post",
            V1_API_URL + "/gettrackinfo",
            headers={"17token": self._api_token},
            json=tracking_request,
        )

        _LOGGER.debug("Packages response: %s", packages_resp)

        packages: List[Package] = []
        for package in packages_resp.get("data", {}).get("accepted", []):
            track: dict = package.get("track", {})
            event: dict = track.get("z0", {})

            kwargs: dict = {
                "id": package.get("number"),
                "destination_country": track.get("c", 0),
                "info_text": event.get("z"),
                "location": " ".join([event.get("c", ""), event.get("d", "")]).strip(),
                "timestamp": event.get("a"),
                "tz": tz,
                "origin_country": track.get("b", 0),
                "status": track.get("e", 0),
                "tracking_info_language": track.get("ln1", "Unknown"),
            }
            packages.append(Package(package.get("number"), **kwargs))
        return packages

    async def summary(self, show_archived: bool = False) -> dict:
        """Get a quick summary of how many packages are in an account."""
        summary_resp: dict = await self._get_track_list(show_archived=show_archived)

        results: dict = {s: 0 for s in list(PACKAGE_STATUS_MAP.values())}
        results["Unknown"] = 0
        for kind in summary_resp.get("data", {}).get("accepted", []):
            key = PACKAGE_STATUS_MAP.get(kind["e"], "Unknown")
            value = 1
            results[key] = value if key not in results else results[key] + value
        return results

    async def _get_track_list(
        self,
        package_state: Union[int, str] = "",
        show_archived: bool = False,
    ) -> dict:
        """Get list of tracking numbers."""
        json: dict = {"package_state": package_state}
        if not show_archived:
            json["tracking_state"] = 1

        track_list: dict = await self._request(
            "post",
            V1_API_URL + "/gettracklist",
            headers={"17token": self._api_token},
            json=json,
        )

        _LOGGER.debug("Track List response: %s", track_list)
        return track_list

    async def add_package_with_carrier(
        self, tracking_number: str, carrier: str, friendly_name: Optional[str] = None
    ):
        """Add a package by tracking number to the tracking list."""
        json: dict = {"number": tracking_number}
        carrier_key: int = get_carrier_key(carrier)
        json["carrier"] = carrier_key
        # TODO map carrier name to code
        if friendly_name is not None:
            json["tag"] = friendly_name
        add_resp: dict = await self._request(
            "post",
            V1_API_URL + "/register",
            json=[json],
        )

        _LOGGER.debug("Add package response: %s", add_resp)

        rejected = add_resp.get("data", {}).get("rejected", [])
        if len(rejected) > 0:
            reason = rejected[0].get("error", {}).get("message", "Unknown")
            raise InvalidTrackingNumberError(f"{tracking_number} is invalid: {reason}")

    async def set_friendly_name(self, tracking_number: str, friendly_name: str):
        """Set a friendly name to an already added tracking number."""
        add_resp: dict = await self._request(
            "post",
            V1_API_URL + "/changeinfo",
            json={"number": tracking_number, "items": {"tag": friendly_name}},
        )

        _LOGGER.debug("Set friendly name response: %s", add_resp)

        rejected = add_resp.get("data", {}).get("rejected", [])
        if len(rejected) > 0:
            reason = rejected[0].get("error", {}).get("message", "Unknown")
            raise InvalidTrackingNumberError(f"{tracking_number} is invalid: {reason}")
