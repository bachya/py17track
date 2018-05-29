"""Define an 17track.com client."""

from requests import Session

from .profile import ProfileManager
from .track import AdHocTracker


class Client(object):  # pylint: disable=too-few-public-methods
    """Define a 17track.net client."""

    def __init__(self) -> None:
        """Initialize."""
        session = Session()

        self.profile = ProfileManager(session)
        self.track = AdHocTracker(session)
