"""Define a 17track.net client."""
from typing import Optional
import warnings

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientError

from .errors import RequestError
from .profile import Profile
from .version import Version

# from .track import Track

DEFAULT_TIMEOUT: int = 10


class Client:  # pylint: disable=too-few-public-methods
    """Define the client."""

    def __init__(
        self,
        *,
        version: Version = Version.LEGACY,
        session: Optional[ClientSession] = None,
    ) -> None:
        """Initialize."""
        self._version: Version = version
        self._session: Optional[ClientSession] = session
        self._profile: Optional[Profile] = None

        # This is disabled until a workaround can be found:
        # self.track = Track(self._request)

    @property
    def profile(self):
        """Get the appropriate version profile."""
        if not self._profile:
            if self._version == Version.LEGACY:
                warnings.warn(
                    "Legacy API has been deprecated, please update to V1",
                    DeprecationWarning,
                    stacklevel=2,
                )
                from .legacy.profile import ProfileLegacy

                self._profile = ProfileLegacy(self._request)
            elif self._version == Version.V1:
                from .v1.profile import ProfileV1

                self._profile = ProfileV1(self._request)

        return self._profile

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

        assert session

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
