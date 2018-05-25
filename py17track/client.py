"""Define an 17track.com client."""

from requests import Session

from .api import BaseAPI
from .profile import ProfileManager
from .track import AdHocTracker


class Client(BaseAPI):  # pylint: disable=too-few-public-methods
    """Define a 17track.net client."""

    def __init__(self) -> None:
        """Initialize."""
        self.session = Session()
        super().__init__(self.session)

        self.profile = ProfileManager(self.session)
        self.track = AdHocTracker(self.session)
