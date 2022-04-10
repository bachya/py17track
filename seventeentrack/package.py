"""Define a simple structure for a package."""
from datetime import datetime
from typing import Optional

import attr
from pytz import UTC, timezone

from .data import CARRIER_MAP, COUNTRY_MAP, PACKAGE_STATUS_MAP, PACKAGE_TYPE_MAP


@attr.s(
    frozen=True
)  # pylint: disable=too-few-public-methods,too-many-instance-attributes
class Package:
    """Define a package object."""

    tracking_number: str = attr.ib()
    carrier: Optional[int] = attr.ib(default=0)
    destination_country: int = attr.ib(default=0)
    id: Optional[str] = attr.ib(default=None)
    friendly_name: Optional[str] = attr.ib(default=None)
    info_text: Optional[str] = attr.ib(default=None)
    location: str = attr.ib(default="")
    timestamp: str = attr.ib(default="")
    origin_country: int = attr.ib(default=0)
    package_type: int = attr.ib(default=0)
    status: int = attr.ib(default=0)
    tracking_info_language: str = attr.ib(default="Unknown")
    tz: str = attr.ib(default="UTC")

    def __attrs_post_init__(self):
        """Do some post-init processing."""
        object.__setattr__(
            self, "destination_country", COUNTRY_MAP.get(self.origin_country, "Unknown")
        )
        object.__setattr__(
            self, "origin_country", COUNTRY_MAP.get(self.origin_country, "Unknown")
        )
        object.__setattr__(self, "package_type", PACKAGE_TYPE_MAP[self.package_type])
        object.__setattr__(
            self, "status", PACKAGE_STATUS_MAP.get(self.status, "Unknown")
        )
        object.__setattr__(self, "carrier", CARRIER_MAP.get(self.carrier, "Unknown"))

        if self.timestamp is not None:
            tz = timezone(self.tz)
            try:
                timestamp = tz.localize(
                    datetime.strptime(self.timestamp, "%Y-%m-%d %H:%M")
                )
            except ValueError:
                try:
                    timestamp = tz.localize(
                        datetime.strptime(self.timestamp, "%Y-%m-%d %H:%M:%S")
                    )
                except ValueError:
                    timestamp = datetime(1970, 1, 1, tzinfo=UTC)

            if self.tz != "UTC":
                timestamp = timestamp.astimezone(UTC)

            object.__setattr__(self, "timestamp", timestamp)
