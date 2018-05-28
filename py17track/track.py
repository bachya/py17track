"""Define an 17track.com profile manager."""
from requests import Session

from py17track.api import BaseAPI
from py17track.exceptions import InvalidTrackingNumberError
from py17track.package import Package

API_TRACK = 'https://t.17track.net/restapi/track'


class AdHocTracker(BaseAPI):  # pylint: disable=too-few-public-methods
    """Define a 17track.net profile manager."""

    def __init__(self, session: Session) -> None:
        """Initialize."""
        self.authenticated = False
        super().__init__(session)

    def find(self, *tracking_numbers: str) -> list:
        """Get tracking info for one or more tracking numbers."""
        data = {'data': [{'num': num} for num in tracking_numbers]}
        resp = self.post(API_TRACK, json=data)
        json = resp.json()

        if not json.get('dat'):
            raise InvalidTrackingNumberError('Invalid data')

        packages = []
        for info in json['dat']:
            resp_data = info.get('track', {})

            if not resp_data:
                raise InvalidTrackingNumberError()

            kwargs = {
                'destination_country': resp_data.get('c'),
                'info_text': resp_data.get('z0', {}).get('z'),
                'location': resp_data.get('z0', {}).get('c'),
                'origin_country': resp_data.get('b'),
                'package_type': resp_data.get('d', 0),
                'status': resp_data.get('e', 0),
                'tracking_info_language': resp_data.get('ln1', 'Unknown')
            }
            packages.append(Package(info['no'], **kwargs))
        return packages
