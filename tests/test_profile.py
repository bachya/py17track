"""Define tests for the client object."""
import aiohttp
import pytest

from py17track import Client

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
        assert len(packages) == 2


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
