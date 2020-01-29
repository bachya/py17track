"""Define tests for the client object."""
import aiohttp
import pytest
from py17track import Client
from py17track.errors import RequestError


@pytest.mark.asyncio
async def test_bad_request(aresponses):
    """Test that a failed login returns the correct response."""
    aresponses.add(
        "random.domain", "/no/good", "get", aresponses.Response(text="", status=404)
    )

    with pytest.raises(RequestError):
        async with aiohttp.ClientSession() as websession:
            client = Client(websession)
            await client._request("get", "https://random.domain/no/good")
