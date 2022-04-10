"""Run an example script to quickly test a 17track.net account."""
import asyncio
import logging

from aiohttp import ClientSession

from seventeentrack import Client
from seventeentrack.errors import SeventeenTrackError

_LOGGER = logging.getLogger()


async def main() -> None:
    """Create the aiohttp session and run the example."""
    logging.basicConfig(level=logging.INFO)

    async with ClientSession() as session:
        try:
            client = Client(session=session)

            await client.profile.login("<EMAIL>", "<PASSWORD>")
            _LOGGER.info("Account ID: %s", client.profile.account_id)

            # await client.profile.add_package("<TRACKING NUMBER>", "<FRIENDLY NAME>")

            summary = await client.profile.summary()
            _LOGGER.info("Account Summary: %s", summary)

            packages = await client.profile.packages()
            _LOGGER.info("Package Summary: %s", packages)
        except SeventeenTrackError as err:
            print(err)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
