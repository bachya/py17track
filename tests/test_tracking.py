"""Define a set of client tests."""

# pylint: disable=wildcard-import,redefined-outer-name,unused-wildcard-import

import json

import pytest
import requests_mock

from py17track import Client
from py17track.track import API_TRACK
from tests.fixtures.track import *  # noqa


def test_track_failure(failure_one_package, tracking_number):
    """Test failure of one tracking number."""
    with requests_mock.Mocker() as mock:
        mock.post(API_TRACK, text=json.dumps(failure_one_package))

        with pytest.raises(ValueError) as exc:
            client = Client()
            client.track.find(tracking_number)
            assert 'Invalid data' in str(exc)


def test_track_success(successful_one_package_1, tracking_number):
    """Test success of one tracking number."""
    with requests_mock.Mocker() as mock:
        mock.post(API_TRACK, text=json.dumps(successful_one_package_1))

        client = Client()
        packages = client.track.find(tracking_number)

        assert len(packages) == 1
        assert packages[0].tracking_number == tracking_number


def test_track_success_2(successful_one_package_2, tracking_number):
    """Test success of one tracking number with unknown destination."""
    with requests_mock.Mocker() as mock:
        mock.post(API_TRACK, text=json.dumps(successful_one_package_2))

        client = Client()
        packages = client.track.find(tracking_number)

        assert len(packages) == 1
        assert packages[0].tracking_number == tracking_number
        assert packages[0].destination_country == 'Unknown'
