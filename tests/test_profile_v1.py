"""Define tests for the client object."""
import aiohttp
import pytest
from pytz import UTC, timezone

from py17track import Client, Version
from py17track.errors import (
    InvalidTrackingNumberError,
    RequestError,
    SeventeenTrackError,
)

from .common import TEST_TOKEN, load_fixture


@pytest.mark.asyncio
async def test_packages(aresponses):
    """Test getting packages."""
    aresponses.add(
        "api.17track.net",
        "/track/v1/gettracklist",
        "post",
        aresponses.Response(
            text=load_fixture("gettracklist_success_response.json"), status=200
        ),
    )
    aresponses.add(
        "api.17track.net",
        "/track/v1/gettrackinfo",
        "post",
        aresponses.Response(
            text=load_fixture("gettrackinfo_success_response.json"), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(version=Version.V1, session=session)
        client.profile.login(TEST_TOKEN)
        packages = await client.profile.packages()
        print(packages)
        assert len(packages) == 5
        assert packages[0].location == "Paris"
        assert packages[0].carrier == "Fedex"
        assert packages[0].origin_country == "United States"
        assert packages[1].location == "Spain"
        assert packages[2].location == "Milano Italy"
        assert packages[3].location == ""


@pytest.mark.asyncio
async def test_packages_with_unknown_state(aresponses):
    """Test getting packages."""
    aresponses.add(
        "api.17track.net",
        "/track/v1/gettracklist",
        "post",
        aresponses.Response(
            text=load_fixture("gettracklist_success_response.json"), status=200
        ),
    )
    aresponses.add(
        "api.17track.net",
        "/track/v1/gettrackinfo",
        "post",
        aresponses.Response(
            text=load_fixture("gettrackinfo_with_unknown_status_response.json"),
            status=200,
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(version=Version.V1, session=session)
        client.profile.login(TEST_TOKEN)
        packages = await client.profile.packages()
        assert len(packages) == 3
        assert packages[0].status == "Not Found"
        assert packages[1].status == "In Transit"
        assert packages[2].status == "Unknown"


@pytest.mark.asyncio
async def test_packages_default_timezone(aresponses):
    """Test getting packages with default timezone."""
    aresponses.add(
        "api.17track.net",
        "/track/v1/gettracklist",
        "post",
        aresponses.Response(
            text=load_fixture("gettracklist_success_response.json"), status=200
        ),
    )
    aresponses.add(
        "api.17track.net",
        "/track/v1/gettrackinfo",
        "post",
        aresponses.Response(
            text=load_fixture("gettrackinfo_success_response.json"), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(version=Version.V1, session=session)
        client.profile.login(TEST_TOKEN)
        packages = await client.profile.packages()
        assert len(packages) == 5
        assert packages[0].timestamp.isoformat() == "2022-03-08T14:11:00+00:00"
        assert packages[1].timestamp.isoformat() == "2022-03-08T02:36:00+00:00"
        assert packages[2].timestamp.isoformat() == "1970-01-01T00:00:00+00:00"


@pytest.mark.asyncio
async def test_packages_user_defined_timezone(aresponses):
    """Test getting packages with user-defined timezone."""
    aresponses.add(
        "api.17track.net",
        "/track/v1/gettracklist",
        "post",
        aresponses.Response(
            text=load_fixture("gettracklist_success_response.json"), status=200
        ),
    )
    aresponses.add(
        "api.17track.net",
        "/track/v1/gettrackinfo",
        "post",
        aresponses.Response(
            text=load_fixture("gettrackinfo_success_response.json"), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(version=Version.V1, session=session)
        client.profile.login(TEST_TOKEN)
        packages = await client.profile.packages(tz="Asia/Jakarta")
        assert len(packages) == 5
        assert packages[0].timestamp.isoformat() == "2022-03-08T07:11:00+00:00"
        assert packages[1].timestamp.isoformat() == "2022-03-07T19:36:00+00:00"
        assert packages[2].timestamp.isoformat() == "1970-01-01T00:00:00+00:00"


@pytest.mark.asyncio
async def test_summary(aresponses):
    """Test getting package summary."""
    aresponses.add(
        "api.17track.net",
        "/track/v1/gettracklist",
        "post",
        aresponses.Response(
            text=load_fixture("gettracklist_success_response.json"), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(version=Version.V1, session=session)
        client.profile.login(TEST_TOKEN)
        summary = await client.profile.summary()
        assert summary["Delivered"] == 1
        assert summary["Expired"] == 0
        assert summary["In Transit"] == 6
        assert summary["Not Found"] == 2
        assert summary["Ready to be Picked Up"] == 0
        assert summary["Returned"] == 0
        assert summary["Undelivered"] == 0
        assert summary["Unknown"] == 3


@pytest.mark.asyncio
async def test_add_new_package(aresponses):
    """Test adding a new package."""
    aresponses.add(
        "api.17track.net",
        "/track/v1/register",
        "post",
        aresponses.Response(
            text=load_fixture("register_success_response.json"), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Client(version=Version.V1, session=session)
        client.profile.login(TEST_TOKEN)
        await client.profile.add_package_with_carrier(
            "LP00432912409987", "FedEx", "Friendly name"
        )


@pytest.mark.asyncio
async def test_set_friendly_name(aresponses):
    """Test setting a friendly name."""
    aresponses.add(
        "api.17track.net",
        "/track/v1/changeinfo",
        "post",
        aresponses.Response(
            text=load_fixture("changeinfo_nonexistant_response.json"), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        with pytest.raises(InvalidTrackingNumberError):
            client = Client(version=Version.V1, session=session)
            client.profile.login(TEST_TOKEN)
            await client.profile.set_friendly_name(
                "1234567890987654321567", "Friendly name"
            )


@pytest.mark.asyncio
async def test_add_existing_package(aresponses):
    """Test adding an existing new package."""
    aresponses.add(
        "api.17track.net",
        "/track/v1/register",
        "post",
        aresponses.Response(
            text=load_fixture("register_existing_response.json"), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        with pytest.raises(InvalidTrackingNumberError):
            client = Client(version=Version.V1, session=session)
            client.profile.login(TEST_TOKEN)
            await client.profile.add_package("1234567890987654321")


@pytest.mark.asyncio
async def test_api_error(aresponses):
    """Test general API error."""
    aresponses.add(
        "api.17track.net",
        "/track/v1/register",
        "post",
        aresponses.Response(text=load_fixture("error_response.json"), status=401),
    )

    async with aiohttp.ClientSession() as session:
        with pytest.raises(RequestError):
            client = Client(version=Version.V1, session=session)
            client.profile.login(TEST_TOKEN)
            await client.profile.add_package("1234567890987654321")


@pytest.mark.asyncio
async def test_unknown_carrier_name(aresponses):
    """Test unknown carrier."""
    async with aiohttp.ClientSession() as session:
        with pytest.raises(SeventeenTrackError):
            client = Client(version=Version.V1, session=session)
            client.profile.login(TEST_TOKEN)
            await client.profile.add_package_with_carrier(
                "1234567890987654321", "Foobar"
            )
