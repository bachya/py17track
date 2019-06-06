"""Define tests for the client object."""
# pylint: disable=redefined-outer-name,unused-import
import json

import aiohttp
import pytest

from py17track import Client

from .const import TEST_EMAIL, TEST_PASSWORD
from .fixtures.profile import *  # noqa


@pytest.mark.asyncio
async def test_login_failure(aresponses, authentication_failure_json, event_loop):
    """Test that a failed login returns the correct response."""
    aresponses.add(
        "user.17track.net",
        "/userapi/call",
        "post",
        aresponses.Response(text=json.dumps(authentication_failure_json), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = Client(websession)
        login_result = await client.profile.login(TEST_EMAIL, TEST_PASSWORD)

        assert login_result is False


@pytest.mark.asyncio
async def test_login_success(aresponses, authentication_success_json, event_loop):
    """Test that a successful login returns the correct response."""
    aresponses.add(
        "user.17track.net",
        "/userapi/call",
        "post",
        aresponses.Response(text=json.dumps(authentication_success_json), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = Client(websession)
        login_result = await client.profile.login(TEST_EMAIL, TEST_PASSWORD)

        assert login_result is True


@pytest.mark.asyncio
async def test_packages(
    aresponses, authentication_success_json, event_loop, packages_json
):
    """Test getting packages."""
    aresponses.add(
        "user.17track.net",
        "/userapi/call",
        "post",
        aresponses.Response(text=json.dumps(authentication_success_json), status=200),
    )
    aresponses.add(
        "buyer.17track.net",
        "/orderapi/call",
        "post",
        aresponses.Response(text=json.dumps(packages_json), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = Client(websession)
        await client.profile.login(TEST_EMAIL, TEST_PASSWORD)
        packages = await client.profile.packages()

        assert len(packages) == 2


@pytest.mark.asyncio
async def test_summary(
    aresponses, authentication_success_json, event_loop, summary_json
):
    """Test getting package summary."""
    aresponses.add(
        "user.17track.net",
        "/userapi/call",
        "post",
        aresponses.Response(text=json.dumps(authentication_success_json), status=200),
    )
    aresponses.add(
        "buyer.17track.net",
        "/orderapi/call",
        "post",
        aresponses.Response(text=json.dumps(summary_json), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = Client(websession)
        await client.profile.login(TEST_EMAIL, TEST_PASSWORD)
        summary = await client.profile.summary()

        assert summary["Delivered"] == 0
        assert summary["Expired"] == 0
        assert summary["In Transit"] == 6
        assert summary["Not Found"] == 2
        assert summary["Ready to be Picked Up"] == 0
        assert summary["Returned"] == 0
        assert summary["Undelivered"] == 0
