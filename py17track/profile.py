"""Define interaction with a user profile."""
from typing import Callable, Coroutine, Optional, Union


class Profile:
    """Define a 17track.net profile manager."""

    def __init__(self, request: Callable[..., Coroutine]) -> None:
        """Initialize."""
        pass

    def login(self, api_token: str) -> None:
        pass

    async def login(self, email: str, password: str) -> bool:
        """Login to the profile."""
        pass

    async def packages(
        self,
        package_state: Union[int, str] = "",
        show_archived: bool = False,
        tz: str = "UTC",
    ) -> list:
        """Get the list of packages associated with the account."""
        pass

    async def summary(self, show_archived: bool = False) -> dict:
        """Get a quick summary of how many packages are in an account."""
        pass

    async def add_package(
        self, tracking_number: str, friendly_name: Optional[str] = None
    ):
        pass

    async def set_friendly_name(self, internal_id: str, friendly_name: str):
        """Set a friendly name to an already added tracking number.

        internal_id is not the tracking number, it's the ID of an existing package.
        """
        pass
