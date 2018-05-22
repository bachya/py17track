"""Define an 17track.com client."""

from py17track.api import BaseAPI
from py17track.exceptions import InvalidTrackingNumberError
from py17track.package import Package


class Client(BaseAPI):  # pylint: disable=too-few-public-methods
    """Define a 17track.net client."""

    def track(self, *tracking_numbers: str) -> dict:
        """Get tracking info for one or more tracking numbers."""
        data = {'data': [{'num': num} for num in tracking_numbers]}
        resp = self.post('track', json=data).json()

        if not resp.get('dat'):
            raise InvalidTrackingNumberError('Invalid data')

        packages = {}
        for info in resp['dat']:
            package = Package(info)
            packages[package.tracking_number] = package
        return packages
