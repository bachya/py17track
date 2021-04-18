# 📦 py17track: A Simple Python API for 17track.net

[![CI](https://github.com/bachya/py17track/workflows/CI/badge.svg)](https://github.com/bachya/py17track/actions)
[![PyPi](https://img.shields.io/pypi/v/py17track.svg)](https://pypi.python.org/pypi/py17track)
[![Version](https://img.shields.io/pypi/pyversions/py17track.svg)](https://pypi.python.org/pypi/py17track)
[![License](https://img.shields.io/pypi/l/py17track.svg)](https://github.com/bachya/py17track/blob/master/LICENSE)
[![Code Coverage](https://codecov.io/gh/bachya/py17track/branch/master/graph/badge.svg)](https://codecov.io/gh/bachya/py17track)
[![Maintainability](https://api.codeclimate.com/v1/badges/af60d65b69d416136fc9/maintainability)](https://codeclimate.com/github/bachya/py17track/maintainability)
[![Say Thanks](https://img.shields.io/badge/SayThanks-!-1EAEDB.svg)](https://saythanks.io/to/bachya)

`py17track` is a simple Python library to track packages in
[17track.net](http://www.17track.net/) accounts.

Since this is uses an unofficial API, there's no guarantee that 17track.net
will provide every field for every package, all the time. Additionally, this
API may stop working at any moment.

# Python Versions

`py17track` is currently supported on:

* Python 3.6
* Python 3.7
* Python 3.8
* Python 3.9

# Installation

```python
pip install py17track
```

# Usage

```python
import asyncio

from aiohttp import ClientSession

from py17track import Client


async def main() -> None:
    """Run!"""
    client = Client()

    # Login to 17track.net:
    await client.profile.login('<EMAIL>', '<PASSWORD>')

    # Get the account ID:
    client.profile.account_id
    # >>> 1234567890987654321

    # Get a summary of the user's packages:
    summary = await client.profile.summary()
    # >>> {'In Transit': 3, 'Expired': 3, ... }

    # Get all packages associated with a user's account:
    packages = await client.profile.packages()
    # >>> [py17track.package.Package(..), ...]
    
    # Add new packages by tracking number
    await client.profile.add_package('<TRACKING NUMBER>', '<FRIENDLY NAME>')


asyncio.run(main())
```

By default, the library creates a new connection to 17track with each coroutine. If you
are calling a large number of coroutines (or merely want to squeeze out every second of
runtime savings possible), an
[`aiohttp`](https://github.com/aio-libs/aiohttp) `ClientSession` can be used for connection
pooling:

```python
import asyncio

from aiohttp import ClientSession

from py17track import Client


async def main() -> None:
    """Run!"""
    async with ClientSession() as session:
        client = Client(session=session)

        # ...


asyncio.run(main())
```

Each `Package` object has the following info:

* `destination_country`: the country the package was shipped to
* `friendly_name`: the human-friendly name of the package
* `info`: a text description of the latest status
* `location`: the current location (if known)
* `timestamp`: the timestamp of the latest event
* `origin_country`: the country the package was shipped from
* `package_type`: the type of package (if known)
* `status`: the overall package status ("In Transit", "Delivered", etc.)
* `tracking_info_language`: the language of the tracking info
* `tracking_number`: the all-important tracking number

# Contributing

1. [Check for open features/bugs](https://github.com/bachya/py17track/issues)
  or [initiate a discussion on one](https://github.com/bachya/py17track/issues/new).
2. [Fork the repository](https://github.com/bachya/py17track/fork).
3. (_optional, but highly recommended_) Create a virtual environment: `python3 -m venv .venv`
4. (_optional, but highly recommended_) Enter the virtual environment: `source ./.venv/bin/activate`
5. Install the dev environment: `script/setup`
6. Code your new feature or bug fix.
7. Write tests that cover your new functionality.
8. Run tests and ensure 100% code coverage: `script/test`
9. Update `README.md` with any new documentation.
10. Add yourself to `AUTHORS.md`.
11. Submit a pull request!

