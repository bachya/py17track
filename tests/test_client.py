"""Define tests for the client object."""
# pylint: disable=redefined-outer-name,unused-import
import aiohttp
import pytest

from py17track import Client
from py17track.errors import RequestError


@pytest.mark.asyncio
async def test_bad_request(aresponses, event_loop):
    """Test that a failed login returns the correct response."""
    aresponses.add(
        'random.domain', '/no/good', 'get',
        aresponses.Response(
            text='', status=404))

    with pytest.raises(RequestError):
        async with aiohttp.ClientSession(loop=event_loop) as websession:
            client = Client(websession)
            await client._request('get', 'https://random.domain/no/good')
