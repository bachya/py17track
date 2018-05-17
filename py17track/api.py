"""Define a base object for interacting with 17track.net."""

import requests

from py17track.exceptions import HTTPError

API_BASE = 'https://t.17track.net/restapi'


class BaseAPI(object):
    """Define a class that represents an API request."""

    def __init__(self):
        """Initialize."""
        self.full_url = None
        self.session = requests.Session()

    def request(self, method_type, url, **kwargs):
        """Define a generic request."""
        self.full_url = '{0}/{1}'.format(API_BASE, url)
        method = getattr(self.session, method_type)
        resp = method(self.full_url, **kwargs)

        # I don't think it's good form to make end users of py17track have to
        # explicitly catch exceptions from a sub-library, so here, I wrap the
        # Requests HTTPError in my own:
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as exc_info:
            raise HTTPError(str(exc_info)) from None

        return resp

    def post(self, url, **kwargs):
        """Define a generic POST request."""
        return self.request('post', url, **kwargs)
