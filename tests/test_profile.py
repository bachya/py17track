"""Define tests for the client object."""
from datetime import datetime

import aiohttp
import pytest
from pytz import UTC, timezone

from py17track import Client
from py17track.errors import InvalidTrackingNumberError, RequestError

from .common import TEST_EMAIL, TEST_PASSWORD, load_fixture


@pytest.mark.asyncio
async def test_login_failure(aresponses):
    """Test that a failed login returns the correct response."""
    aresponses.add(
        "user.17track.net",
        "/userapi/call",
        "post",
        aresponses.Response(
            text=load_fixture("authentication_failure_response.json"), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(session=session)
        login_result = await client.profile.login(TEST_EMAIL, TEST_PASSWORD)
        assert login_result is False


@pytest.mark.asyncio
async def test_login_success(aresponses):
    """Test that a successful login returns the correct response."""
    aresponses.add(
        "user.17track.net",
        "/userapi/call",
        "post",
        aresponses.Response(
            text=load_fixture("authentication_success_response.json"), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(session=session)
        login_result = await client.profile.login(TEST_EMAIL, TEST_PASSWORD)
        assert login_result is True


@pytest.mark.asyncio
async def test_no_explicit_session(aresponses):
    """Test not providing an explicit aiohttp ClientSession."""
    aresponses.add(
        "user.17track.net",
        "/userapi/call",
        "post",
        aresponses.Response(
            text=load_fixture("authentication_success_response.json"), status=200
        ),
    )

    client = Client()
    login_result = await client.profile.login(TEST_EMAIL, TEST_PASSWORD)
    assert login_result is True


@pytest.mark.asyncio
async def test_packages(aresponses):
    """Test getting packages."""
    aresponses.add(
        "user.17track.net",
        "/userapi/call",
        "post",
        aresponses.Response(
            text=load_fixture("authentication_success_response.json"), status=200
        ),
    )
    aresponses.add(
        "buyer.17track.net",
        "/orderapi/call",
        "post",
        aresponses.Response(text=load_fixture("packages_response.json"), status=200),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(session=session)
        await client.profile.login(TEST_EMAIL, TEST_PASSWORD)
        packages = await client.profile.packages()
        assert len(packages) == 5
        assert packages[0].location == "Paris"
        assert packages[1].location == "Spain"
        assert packages[2].location == "Milano Italy"
        assert packages[3].location == ""


@pytest.mark.asyncio
async def test_packages_default_timezone(aresponses):
    """Test getting packages with default timezone."""
    aresponses.add(
        "user.17track.net",
        "/userapi/call",
        "post",
        aresponses.Response(
            text=load_fixture("authentication_success_response.json"), status=200
        ),
    )
    aresponses.add(
        "buyer.17track.net",
        "/orderapi/call",
        "post",
        aresponses.Response(text=load_fixture("packages_response.json"), status=200),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(session=session)
        await client.profile.login(TEST_EMAIL, TEST_PASSWORD)
        packages = await client.profile.packages()
        assert len(packages) == 5
        assert packages[0].timestamp.isoformat() == "2018-04-23T12:02:00+00:00"
        assert packages[1].timestamp.isoformat() == "2019-02-26T01:05:34+00:00"
        assert packages[2].timestamp.isoformat() == "1970-01-01T00:00:00+00:00"


@pytest.mark.asyncio
async def test_packages_user_defined_timezone(aresponses):
    """Test getting packages with user-defined timezone."""
    aresponses.add(
        "user.17track.net",
        "/userapi/call",
        "post",
        aresponses.Response(
            text=load_fixture("authentication_success_response.json"), status=200
        ),
    )
    aresponses.add(
        "buyer.17track.net",
        "/orderapi/call",
        "post",
        aresponses.Response(text=load_fixture("packages_response.json"), status=200),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(session=session)
        await client.profile.login(TEST_EMAIL, TEST_PASSWORD)
        packages = await client.profile.packages(tz="Asia/Jakarta")
        assert len(packages) == 5
        assert packages[0].timestamp.isoformat() == "2018-04-23T05:02:00+00:00"
        assert packages[1].timestamp.isoformat() == "2019-02-25T18:05:34+00:00"
        assert packages[2].timestamp.isoformat() == "1970-01-01T00:00:00+00:00"


@pytest.mark.asyncio
async def test_summary(aresponses):
    """Test getting package summary."""
    aresponses.add(
        "user.17track.net",
        "/userapi/call",
        "post",
        aresponses.Response(
            text=load_fixture("authentication_success_response.json"), status=200
        ),
    )
    aresponses.add(
        "buyer.17track.net",
        "/orderapi/call",
        "post",
        aresponses.Response(text=load_fixture("summary_response.json"), status=200),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(session=session)
        await client.profile.login(TEST_EMAIL, TEST_PASSWORD)
        summary = await client.profile.summary()
        assert summary["Delivered"] == 0
        assert summary["Expired"] == 0
        assert summary["In Transit"] == 6
        assert summary["Not Found"] == 2
        assert summary["Ready to be Picked Up"] == 0
        assert summary["Returned"] == 0
        assert summary["Undelivered"] == 0


@pytest.mark.asyncio
async def test_add_new_package(aresponses):
    """Test adding a new package."""
    aresponses.add(
        "user.17track.net",
        "/userapi/call",
        "post",
        aresponses.Response(
            text=load_fixture("authentication_success_response.json"), status=200
        ),
    )
    aresponses.add(
        "buyer.17track.net",
        "/orderapi/call",
        "post",
        aresponses.Response(text=load_fixture("add_package_response.json"), status=200),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(session=session)
        await client.profile.login(TEST_EMAIL, TEST_PASSWORD)
        await client.profile.add_package("LP00432912409987")


@pytest.mark.asyncio
async def test_add_new_package_with_friendly_name(aresponses):
    """Test adding a new package with friendly name."""
    aresponses.add(
        "user.17track.net",
        "/userapi/call",
        "post",
        aresponses.Response(
            text=load_fixture("authentication_success_response.json"), status=200
        ),
    )
    aresponses.add(
        "buyer.17track.net",
        "/orderapi/call",
        "post",
        aresponses.Response(text=load_fixture("add_package_response.json"), status=200),
    )
    aresponses.add(
        "buyer.17track.net",
        "/orderapi/call",
        "post",
        aresponses.Response(text=load_fixture("packages_response.json"), status=200),
    )
    aresponses.add(
        "buyer.17track.net",
        "/orderapi/call",
        "post",
        aresponses.Response(
            text=load_fixture("set_friendly_name_response.json"), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(session=session)
        await client.profile.login(TEST_EMAIL, TEST_PASSWORD)
        await client.profile.add_package("1234567890987654321", "Friendly name")


@pytest.mark.asyncio
async def test_add_new_package_with_friendly_name_not_found(aresponses):
    """Test adding a new package with friendly name but package not found after adding it."""
    aresponses.add(
        "user.17track.net",
        "/userapi/call",
        "post",
        aresponses.Response(
            text=load_fixture("authentication_success_response.json"), status=200
        ),
    )
    aresponses.add(
        "buyer.17track.net",
        "/orderapi/call",
        "post",
        aresponses.Response(text=load_fixture("add_package_response.json"), status=200),
    )
    aresponses.add(
        "buyer.17track.net",
        "/orderapi/call",
        "post",
        aresponses.Response(text=load_fixture("packages_response.json"), status=200),
    )
    aresponses.add(
        "buyer.17track.net",
        "/orderapi/call",
        "post",
        aresponses.Response(
            text=load_fixture("set_friendly_name_response.json"), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        with pytest.raises(InvalidTrackingNumberError):
            client = Client(session=session)
            await client.profile.login(TEST_EMAIL, TEST_PASSWORD)
            await client.profile.add_package("1234567890987654321567", "Friendly name")


@pytest.mark.asyncio
async def test_add_new_package_with_friendly_name_error_response(aresponses):
    """Test adding a new package with friendly name but setting the name fails."""
    aresponses.add(
        "user.17track.net",
        "/userapi/call",
        "post",
        aresponses.Response(
            text=load_fixture("authentication_success_response.json"), status=200
        ),
    )
    aresponses.add(
        "buyer.17track.net",
        "/orderapi/call",
        "post",
        aresponses.Response(text=load_fixture("add_package_response.json"), status=200),
    )
    aresponses.add(
        "buyer.17track.net",
        "/orderapi/call",
        "post",
        aresponses.Response(text=load_fixture("packages_response.json"), status=200),
    )
    aresponses.add(
        "buyer.17track.net",
        "/orderapi/call",
        "post",
        aresponses.Response(
            text=load_fixture("set_friendly_name_failure_response.json"), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        with pytest.raises(RequestError):
            client = Client(session=session)
            await client.profile.login(TEST_EMAIL, TEST_PASSWORD)
            await client.profile.add_package("1234567890987654321", "Friendly name")


@pytest.mark.asyncio
async def test_add_existing_package(aresponses):
    """Test adding an existing new package."""
    aresponses.add(
        "user.17track.net",
        "/userapi/call",
        "post",
        aresponses.Response(
            text=load_fixture("authentication_success_response.json"), status=200
        ),
    )
    aresponses.add(
        "buyer.17track.net",
        "/orderapi/call",
        "post",
        aresponses.Response(
            text=load_fixture("add_package_existing_response.json"), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        with pytest.raises(RequestError):
            client = Client(session=session)
            await client.profile.login(TEST_EMAIL, TEST_PASSWORD)
            await client.profile.add_package("1234567890987654321")
