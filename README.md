# 📦 py17track: A Simple Python API for 17track.net

[![Travis CI](https://travis-ci.org/bachya/py17track.svg?branch=master)](https://travis-ci.org/bachya/py17track)
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

* Python 3.5
* Python 3.6
* Python 3.7

However, running the test suite currently requires Python 3.6 or higher; tests
run on Python 3.5 will fail.

# Installation

```python
pip install py17track
```

# Usage

`py17track` starts within an
[aiohttp](https://aiohttp.readthedocs.io/en/stable/) `ClientSession`:

```python
import asyncio

from aiohttp import ClientSession

from py17track import Client


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as websession:
      # YOUR CODE HERE


asyncio.get_event_loop().run_until_complete(main())
```

Create a client then get to it:

```python
import asyncio

from aiohttp import ClientSession

from py17track import Client


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as websession:
      client = Client(websession)

      # Login to 17track.net:
      await client.profile.login('<EMAIL>', '<PASSWORD>')

      # Get a summary of the user's packages:
      summary = await client.profile.summary()
      # >>> {'In Transit': 3, 'Expired': 3, ... }

      # Get all packages associated with a user's account:
      packages = await client.profile.packages()
      # >>> [py17track.package.Package(..), ...]


asyncio.get_event_loop().run_until_complete(main())
```

Each `Package` object has the following info:

* :code:`destination_country`: the country the package was shipped to
* :code:`info`: a text description of the latest status
* :code:`location`: the current location (if known)
* :code:`origin_country`: the country the package was shipped from
* :code:`package_type`: the type of package (if known)
* :code:`status`: the overall package status ("In Transit", "Delivered", etc.)
* :code:`tracking_info_language`: the language of the tracking info
* :code:`tracking_number`: the all-important tracking number

# Contributing

1. [Check for open features/bugs](https://github.com/bachya/py17track/issues)
  or [initiate a discussion on one](https://github.com/bachya/py17track/issues/new).
2. [Fork the repository](https://github.com/bachya/py17track/fork).
3. Install the dev environment: `make init`.
4. Enter the virtual environment: `pipenv shell`
5. Code your new feature or bug fix.
6. Write a test that covers your new functionality.
7. Update `README.md` with any new documentation.
8. Run tests and ensure 100% code coverage: `make coverage`
9. Ensure you have no linting errors: `make lint`
10. Ensure you have no typed your code correctly: `make typing`
11. Add yourself to `AUTHORS.md`.
12. Submit a pull request!
