"""Define an 17track.com profile manager."""
import json
from typing import Union

from requests import Session

from py17track.api import BaseAPI
from py17track.exceptions import UnauthenticatedError
from py17track.package import PACKAGE_STATUS_MAP, Package

API_BUYER = 'https://buyer.17track.net/orderapi/call'
API_USER = 'https://user.17track.net/userapi/call'


def requires_authentication(function):
    """Define a check for authentication"""

    def decorator(self, *args, **kwargs):
        """ Decorate! """
        if not self.authenticated:
            raise UnauthenticatedError('You need to authenticate first!')
        else:
            return function(self, *args, **kwargs)

    return decorator


class ProfileManager(BaseAPI):  # pylint: disable=too-few-public-methods
    """Define a 17track.net profile manager."""

    def __init__(self, session: Session) -> None:
        """Initialize."""
        self.authenticated = False
        super().__init__(session)

    def authenticate(self, email: str, password: str) -> None:
        """Authenticate an account."""
        resp = self.post(
            'https://user.17track.net/userapi/call',
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

        if resp.json()['Code'] != 0:
            raise UnauthenticatedError('Invalid username/password')

        self.authenticated = True

    @requires_authentication
    def packages(self,
                 package_state: Union[int, str] = '',
                 show_archived: bool = False) -> list:
        """Get detailed information on packages in an account."""
        resp = self.post(
            API_BUYER,
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

        packages = []  # type: ignore
        for package in resp.json().get('Json', []):
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

    @requires_authentication
    def summary(self, show_archived: bool = False) -> dict:
        """Get a quick summary of how many packages are in an account."""
        resp = self.post(
            API_BUYER,
            json={
                'version': '1.0',
                'method': 'GetIndexData',
                'param': {
                    'IsArchived': show_archived
                },
                'sourcetype': 0
            })

        results = {}
        for kind in resp.json().get('Json', {}).get('eitem', []):
            results[PACKAGE_STATUS_MAP[kind['e']]] = kind['ec']
        return results
