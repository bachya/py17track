"""Define interaction with a user profile."""
import json
import logging
from typing import Coroutine, Callable, Union

from .package import PACKAGE_STATUS_MAP, Package

_LOGGER = logging.getLogger(__name__)

API_URL_BUYER = 'https://buyer.17track.net/orderapi/call'
API_URL_USER = 'https://user.17track.net/userapi/call'


class Profile:
    """Define a 17track.net profile manager."""

    def __init__(self, request: Callable[..., Coroutine]) -> None:
        """Initialize."""
        self._request = request
        self.account_id = None

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

        _LOGGER.debug('Login response: %s', login_resp)

        if login_resp.get('Code') != 0:
            return False

        self.account_id = login_resp['Json']['gid']

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

        _LOGGER.debug('Packages response: %s', packages_resp)

        packages = []
        for package in packages_resp.get('Json', []):
            last_event = package.get('FLastEvent')
            if last_event:
                event = json.loads(last_event)
            else:
                event = {}

            kwargs = {
                'destination_country': package.get('FSecondCountry', 0),
                'friendly_name': package.get('FRemark'),
                'info_text': event.get('z'),
                'location': event.get('c'),
                'origin_country': package.get('FFirstCountry', 0),
                'package_type': package.get('FTrackStateType', 0),
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

        _LOGGER.debug('Summary response: %s', summary_resp)

        results = {}
        for kind in summary_resp.get('Json', {}).get('eitem', []):
            results[PACKAGE_STATUS_MAP[kind['e']]] = kind['ec']
        return results
