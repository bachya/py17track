"""Define an 17track.com client."""

from py17track.api import BaseAPI
from py17track.package import Package


class Client(BaseAPI):  # pylint: disable=too-few-public-methods
    """Define a 17track.net client."""

    def track(self, *tracking_numbers: str) -> list:
        """Get tracking info for one or more tracking numbers."""
        data = {'data': [{'num': num} for num in tracking_numbers]}
        resp = self.post('track', json=data).json()

        if not resp.get('dat'):
            raise ValueError('Invalid data for package')

        return [Package(i) for i in resp['dat']]
