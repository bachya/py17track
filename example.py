"""Run an example script to quickly test any SimpliSafe system."""
import asyncio

from aiohttp import ClientSession

from py17track import Client
from py17track.errors import SeventeenTrackError


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as websession:
        try:
            client = Client(websession)
            await client.profile.login('<EMAIL>', '<PASSWORD>')

            print('Account ID: {0}'.format(client.profile.account_id))

            print()
            print('Getting account summary...')
            summary = await client.profile.summary()
            print(summary)

            print()
            print('Getting all account packages...')
            packages = await client.profile.packages()
            print(packages)
        except SeventeenTrackError as err:
            print(err)


asyncio.get_event_loop().run_until_complete(main())
