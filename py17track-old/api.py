"""Define a base object for interacting with 17track.net."""

from urllib.parse import urlparse

import requests

from py17track.exceptions import HTTPError

HEADER_ACCEPT = '*/*'
HEADER_USER_AGENT = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36')


class BaseAPI(object):
    """Define a class that represents an API request."""

    def __init__(self, session=None):
        """Initialize."""
        self.full_url = None
        self.session = session if session else requests.Session()

    def request(self, method_type, url, **kwargs):
        """Define a generic request."""
        url_pieces = urlparse(url)
        host = url_pieces.netloc
        origin = '{0}://{1}'.format(url_pieces.scheme, host)
        referrer = '{0}/en'.format(origin)

        kwargs.setdefault('headers', {})
        kwargs['headers'].setdefault('Accept', HEADER_ACCEPT)
        kwargs['headers'].setdefault('Host', host)
        kwargs['headers'].setdefault('Origin', origin)
        kwargs['headers'].setdefault('Referrer', referrer)
        kwargs['headers'].setdefault('User-Agent', HEADER_USER_AGENT)

        method = getattr(self.session, method_type)
        resp = method(url, **kwargs)

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
