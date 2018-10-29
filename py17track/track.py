"""Define interaction with an individual package."""
from typing import Callable, Coroutine

from .errors import InvalidTrackingNumberError
from .package import Package

API_URL_TRACK = 'https://t.17track.net/restapi/track'


class Track:  # pylint: disable=too-few-public-methods
    """Define a 17track.net package manager."""

    def __init__(self, request: Callable[..., Coroutine]) -> None:
        """Initialize."""
        self._request = request

    async def find(self, *tracking_numbers: str) -> list:
        """Get tracking info for one or more tracking numbers."""
        data = {'data': [{'num': num} for num in tracking_numbers]}
        tracking_resp = await self._request('post', API_URL_TRACK, json=data)

        print(tracking_resp)

        if not tracking_resp.get('dat'):
            raise InvalidTrackingNumberError('Invalid data')

        packages = []
        for info in tracking_resp['dat']:
            package_info = info.get('track', {})

            if not package_info:
                continue

            kwargs = {
                'destination_country': package_info.get('c'),
                'info_text': package_info.get('z0', {}).get('z'),
                'location': package_info.get('z0', {}).get('c'),
                'origin_country': package_info.get('b'),
                'package_type': package_info.get('d', 0),
                'status': package_info.get('e', 0),
                'tracking_info_language': package_info.get('ln1', 'Unknown')
            }
            packages.append(Package(info['no'], **kwargs))
        return packages
