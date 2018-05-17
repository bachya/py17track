"""Define a set of base API tests."""

# pylint: disable=wildcard-import,redefined-outer-name,unused-wildcard-import

import json

import pytest
import requests_mock

from py17track import Client
from py17track.api import API_BASE
from py17track.exceptions import HTTPError
from tests.fixtures.general import *  # noqa


def test_one_failure(failure_one_package, tracking_number):
    """Test successful receipt of one package."""
    with requests_mock.Mocker() as mock:
        mock.post(
            '{0}/track'.format(API_BASE), text=json.dumps(failure_one_package))

        with pytest.raises(ValueError) as exc:
            client = Client()
            client.track(tracking_number)
            assert 'Invalid data' in str(exc)


def test_one_successful_1(successful_one_package_1, tracking_number):
    """Test successful receipt of one package."""
    with requests_mock.Mocker() as mock:
        mock.post(
            '{0}/track'.format(API_BASE),
            text=json.dumps(successful_one_package_1))

        client = Client()
        packages = client.track(tracking_number)

        assert len(packages) == 1
        assert packages[0].tracking_number == tracking_number
        assert packages[0].destination_country == packages[0].origin_country


def test_one_successful_2(successful_one_package_2, tracking_number):
    """Test successful receipt of one package."""
    with requests_mock.Mocker() as mock:
        mock.post(
            '{0}/track'.format(API_BASE),
            text=json.dumps(successful_one_package_2))

        client = Client()
        packages = client.track(tracking_number)

        assert len(packages) == 1
        assert packages[0].tracking_number == tracking_number
        assert packages[0].destination_country == 'Unknown'


def test_exception(tracking_number):
    """Test what happens when some HTTP error occurs."""
    with requests_mock.Mocker() as mock:
        mock.post('{0}/track'.format(API_BASE), status_code=404)

        with pytest.raises(HTTPError) as exc:
            client = Client()
            client.track(tracking_number)
            assert '404' in str(exc)
