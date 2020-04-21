"""Define a 17track.net client."""
from typing import Optional

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientError

from .errors import RequestError
from .profile import Profile

# from .track import Track

DEFAULT_TIMEOUT: int = 10


class Client:  # pylint: disable=too-few-public-methods
    """Define the client."""

    def __init__(self, *, session: Optional[ClientSession] = None) -> None:
        """Initialize."""
        self._session: ClientSession = session

        self.profile: Profile = Profile(self._request)
        # This is disabled until a workaround can be found:
        # self.track = Track(self._request)

    async def _request(
        self,
        method: str,
        url: str,
        *,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        json: Optional[dict] = None,
    ) -> dict:
        """Make a request against the RainMachine device."""
        use_running_session = self._session and not self._session.closed

        if use_running_session:
            session = self._session
        else:
            session = ClientSession(timeout=ClientTimeout(total=DEFAULT_TIMEOUT))

        try:
            async with session.request(
                method, url, headers=headers, params=params, json=json
            ) as resp:
                resp.raise_for_status()
                data: dict = await resp.json(content_type=None)
                return data
        except ClientError as err:
            raise RequestError(f"Error requesting data from {url}: {err}")
        finally:
            if not use_running_session:
                await session.close()
