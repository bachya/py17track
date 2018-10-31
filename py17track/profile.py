"""Define interaction with a user profile."""
import json
from typing import Coroutine, Callable, Union

from .package import PACKAGE_STATUS_MAP, Package

API_URL_BUYER = 'https://buyer.17track.net/orderapi/call'
API_URL_USER = 'https://user.17track.net/userapi/call'


class Profile:
    """Define a 17track.net profile manager."""

    def __init__(self, request: Callable[..., Coroutine]) -> None:
        """Initialize."""
        self._request = request

    async def login(self, email: str, password: str) -> bool:
        """Login to the profile."""
        login_resp = await self._request(
            'post',
            API_URL_USER,
            json={
                'version': '1.0',
                'method': 'Signin',
                'param': {
                    'Email': email,
                    'Password': password,
                    'CaptchaCode': ''
                },
                'sourcetype': 0
            })

        if login_resp.get('Code') != 0:
            return False

        return True

    async def packages(
            self, package_state: Union[int, str] = '',
            show_archived: bool = False) -> list:
        """Get the list of packages associated with the account."""
        packages_resp = await self._request(
            'post',
            API_URL_BUYER,
            json={
                'version': '1.0',
                'method': 'GetTrackInfoList',
                'param': {
                    'IsArchived': show_archived,
                    'Item': '',
                    'Page': 1,
                    'PerPage': 40,
                    'PackageState': package_state,
                    'Sequence': '0'
                },
                'sourcetype': 0
            })

        packages = []
        for package in packages_resp.get('Json', []):
            last_event = package.get('FLastEvent')
            if last_event:
                event = json.loads(last_event)
            else:
                event = {}

            kwargs = {
                'destination_country': package.get('FSecondCountry', 0),
                'info_text': event.get('z'),
                'location': event.get('c'),
                'origin_country': package.get('FFirstCountry', 0),
                'package_type': event.get('d') or 0,
                'status': package.get('FPackageState', 0)
            }
            packages.append(Package(package['FTrackNo'], **kwargs))
        return packages

    async def summary(self, show_archived: bool = False) -> dict:
        """Get a quick summary of how many packages are in an account."""
        summary_resp = await self._request(
            'post',
            API_URL_BUYER,
            json={
                'version': '1.0',
                'method': 'GetIndexData',
                'param': {
                    'IsArchived': show_archived
                },
                'sourcetype': 0
            })

        results = {}
        for kind in summary_resp.get('Json', {}).get('eitem', []):
            results[PACKAGE_STATUS_MAP[kind['e']]] = kind['ec']
        return results
