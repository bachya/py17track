"""Define a set of client tests."""

# pylint: disable=wildcard-import,redefined-outer-name,unused-wildcard-import

import pytest
import requests_mock

from py17track import Client
from py17track.exceptions import HTTPError
from py17track.track import API_TRACK
from tests.fixtures.track import *  # noqa


def test_exception(tracking_number):
    """Test what happens when some HTTP error occurs."""
    with requests_mock.Mocker() as mock:
        mock.post(API_TRACK, status_code=404)

        with pytest.raises(HTTPError) as exc:
            client = Client()
            client.track.find(tracking_number)
            assert '404' in str(exc)
