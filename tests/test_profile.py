"""Define a set of client tests."""

# pylint: disable=wildcard-import,redefined-outer-name,unused-wildcard-import

import json

import pytest
import requests_mock

from py17track import Client
from py17track.exceptions import UnauthenticatedError
from py17track.profile import API_BUYER, API_USER
from tests.fixtures.profile import *  # noqa


def test_authentication_failure(authentication_failure, email, password):
    """Test failure in authentication."""
    with requests_mock.Mocker() as mock:
        mock.post(API_USER, text=json.dumps(authentication_failure))

        with pytest.raises(UnauthenticatedError) as exc:
            client = Client()
            client.profile.authenticate(email, password)
            assert 'Invalid' in str(exc)


def test_authentication_success(authentication_success, email, password):
    """Test success in authentication."""
    with requests_mock.Mocker() as mock:
        mock.post(API_USER, text=json.dumps(authentication_success))

        client = Client()
        client.profile.authenticate(email, password)

        assert True


def test_packages(authentication_success, email, password, packages,
                  tracking_number):
    """Test getting detail package info from an account."""
    with requests_mock.Mocker() as mock:
        mock.post(API_USER, text=json.dumps(authentication_success))
        mock.post(API_BUYER, text=json.dumps(packages))

        client = Client()
        client.profile.authenticate(email, password)
        packages = client.profile.packages()
        package = packages[0]

        assert package.tracking_number == tracking_number


def test_summary_unauthenticated(summary):
    """Test failure in authentication."""
    with requests_mock.Mocker() as mock:
        mock.post(API_BUYER, text=json.dumps(summary))

        with pytest.raises(UnauthenticatedError) as exc:
            client = Client()
            client.profile.summary()
            assert 'authenticate' in str(exc)


def test_summary(authentication_success, email, password, summary):
    """Test getting a package summary from an account."""
    with requests_mock.Mocker() as mock:
        mock.post(API_USER, text=json.dumps(authentication_success))
        mock.post(API_BUYER, text=json.dumps(summary))

        client = Client()
        client.profile.authenticate(email, password)
        summary_resp = client.profile.summary()

        assert summary_resp['Not Found'] == 2
        assert summary_resp['In Transit'] == 6
        assert summary_resp['Expired'] == 0
        assert summary_resp['Ready to be Picked Up'] == 0
        assert summary_resp['Undelivered'] == 0
        assert summary_resp['Delivered'] == 0
        assert summary_resp['Returned'] == 0
