"""Define interaction with a user profile."""
import json
import logging
from typing import Callable, Coroutine, List, Optional, Union

from ..errors import InvalidTrackingNumberError, RequestError
from ..package import PACKAGE_STATUS_MAP, Package
from ..profile import Profile

_LOGGER: logging.Logger = logging.getLogger(__name__)

API_URL_BUYER: str = "https://buyer.17track.net/orderapi/call"
API_URL_USER: str = "https://user.17track.net/userapi/call"


class ProfileLegacy(Profile):
    """Define a 17track.net profile manager."""

    def __init__(self, request: Callable[..., Coroutine]) -> None:
        """Initialize."""
        self._request: Callable[..., Coroutine] = request
        self.account_id: Optional[str] = None

    async def login(self, email: str, password: str) -> bool:
        """Login to the profile."""
        login_resp: dict = await self._request(
            "post",
            API_URL_USER,
            json={
                "version": "1.0",
                "method": "Signin",
                "param": {"Email": email, "Password": password, "CaptchaCode": ""},
                "sourcetype": 0,
            },
        )

        _LOGGER.debug("Login response: %s", login_resp)

        if login_resp.get("Code") != 0:
            return False

        self.account_id = login_resp["Json"]["gid"]

        return True

    async def packages(
        self,
        package_state: Union[int, str] = "",
        show_archived: bool = False,
        tz: str = "UTC",
    ) -> list:
        """Get the list of packages associated with the account."""
        packages_resp: dict = await self._request(
            "post",
            API_URL_BUYER,
            json={
                "version": "1.0",
                "method": "GetTrackInfoList",
                "param": {
                    "IsArchived": show_archived,
                    "Item": "",
                    "Page": 1,
                    "PerPage": 40,
                    "PackageState": package_state,
                    "Sequence": "0",
                },
                "sourcetype": 0,
            },
        )

        _LOGGER.debug("Packages response: %s", packages_resp)

        packages: List[Package] = []
        for package in packages_resp.get("Json", []):
            event: dict = {}
            last_event_raw: str = package.get("FLastEvent")
            if last_event_raw:
                event = json.loads(last_event_raw)

            kwargs: dict = {
                "id": package.get("FTrackInfoId"),
                "destination_country": package.get("FSecondCountry", 0),
                "friendly_name": package.get("FRemark"),
                "info_text": event.get("z"),
                "location": " ".join([event.get("c", ""), event.get("d", "")]).strip(),
                "timestamp": event.get("a"),
                "tz": tz,
                "origin_country": package.get("FFirstCountry", 0),
                "package_type": package.get("FTrackStateType", 0),
                "status": package.get("FPackageState", 0),
            }
            packages.append(Package(package["FTrackNo"], **kwargs))
        return packages

    async def summary(self, show_archived: bool = False) -> dict:
        """Get a quick summary of how many packages are in an account."""
        summary_resp: dict = await self._request(
            "post",
            API_URL_BUYER,
            json={
                "version": "1.0",
                "method": "GetIndexData",
                "param": {"IsArchived": show_archived},
                "sourcetype": 0,
            },
        )

        _LOGGER.debug("Summary response: %s", summary_resp)

        results: dict = {}
        for kind in summary_resp.get("Json", {}).get("eitem", []):
            key = PACKAGE_STATUS_MAP.get(kind["e"], "Unknown")
            value = kind["ec"]
            results[key] = value if key not in results else results[key] + value
        return results

    async def add_package(
        self, tracking_number: str, friendly_name: Optional[str] = None
    ):
        """Add a package by tracking number to the tracking list."""
        add_resp: dict = await self._request(
            "post",
            API_URL_BUYER,
            json={
                "version": "1.0",
                "method": "AddTrackNo",
                "param": {"TrackNos": [tracking_number]},
            },
        )

        _LOGGER.debug("Add package response: %s", add_resp)

        code = add_resp.get("Code")
        if code != 0:
            raise RequestError(f"Non-zero status code in response: {code}")

        if not friendly_name:
            return

        packages = await self.packages()
        try:
            new_package = next(
                p for p in packages if p.tracking_number == tracking_number
            )
        except StopIteration:
            raise InvalidTrackingNumberError(
                f"Recently added package not found by tracking number: {tracking_number}"
            )

        _LOGGER.debug("Found internal ID of recently added package: %s", new_package.id)

        await self.set_friendly_name(new_package.id, friendly_name)

    async def set_friendly_name(self, internal_id: str, friendly_name: str):
        """Set a friendly name to an already added tracking number.

        internal_id is not the tracking number, it's the ID of an existing package.
        """
        remark_resp: dict = await self._request(
            "post",
            API_URL_BUYER,
            json={
                "version": "1.0",
                "method": "SetTrackRemark",
                "param": {"TrackInfoId": internal_id, "Remark": friendly_name},
            },
        )

        _LOGGER.debug("Set friendly name response: %s", remark_resp)

        code = remark_resp.get("Code")
        if code != 0:
            raise RequestError(f"Non-zero status code in response: {code}")
