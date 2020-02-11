"""Run an example script to quickly test a 17track.net account."""
import asyncio
import logging

from aiohttp import ClientSession

from py17track import Client
from py17track.errors import SeventeenTrackError

_LOGGER = logging.getLogger()


async def main() -> None:
    """Create the aiohttp session and run the example."""
    logging.basicConfig(level=logging.INFO)

    async with ClientSession() as websession:
        try:
            client = Client(websession)

            await client.profile.login("<EMAIL>", "<PASSWORD>")
            _LOGGER.info("Account ID: %s", client.profile.account_id)

            summary = await client.profile.summary()
            _LOGGER.info("Account Summary: %s", summary)

            packages = await client.profile.packages()
            _LOGGER.info("Package Summary: %s", packages)
        except SeventeenTrackError as err:
            print(err)


asyncio.get_event_loop().run_until_complete(main())
