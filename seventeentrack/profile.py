"""Define interaction with a user profile."""
from abc import abstractmethod
from typing import Callable, Coroutine, Optional, Union


class Profile:  # pragma: no cover
    """Define a 17track.net profile manager."""

    def __init__(self, request: Callable[..., Coroutine]) -> None:
        """Initialize."""
        pass

    @abstractmethod
    async def packages(
        self,
        package_state: Union[int, str] = "",
        show_archived: bool = False,
        tz: str = "UTC",
    ) -> list:
        """Get the list of packages associated with the account."""
        pass

    @abstractmethod
    async def summary(self, show_archived: bool = False) -> dict:
        """Get a quick summary of how many packages are in an account."""
        pass

    @abstractmethod
    async def add_package(
        self, tracking_number: str, friendly_name: Optional[str] = None
    ):
        """Add a package by tracking number to the tracking list."""
        pass

    @abstractmethod
    async def add_package_with_carrier(
        self, tracking_number: str, carrier: str, friendly_name: Optional[str] = None
    ):
        """Add a package by tracking number with carrier to the tracking list."""
        pass

    @abstractmethod
    async def set_friendly_name(self, internal_id: str, friendly_name: str):
        """Set a friendly name to an already added tracking number.

        internal_id is not the tracking number, it's the ID of an existing package.
        """
        pass
