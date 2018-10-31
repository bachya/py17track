py17track: A Simple Python API for 17track.net
================================================

.. image:: https://travis-ci.org/bachya/py17track.svg?branch=master
  :target: https://travis-ci.org/bachya/py17track

.. image:: https://img.shields.io/pypi/v/py17track.svg
  :target: https://pypi.python.org/pypi/py17track

.. image:: https://img.shields.io/pypi/pyversions/py17track.svg
  :target: https://pypi.python.org/pypi/py17track

.. image:: https://img.shields.io/pypi/l/py17track.svg
  :target: https://github.com/bachya/py17track/blob/master/LICENSE

.. image:: https://codecov.io/gh/bachya/py17track/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/bachya/py17track

.. image:: https://api.codeclimate.com/v1/badges/af60d65b69d416136fc9/maintainability
  :target: https://codeclimate.com/github/bachya/py17track

.. image:: https://img.shields.io/badge/SayThanks-!-1EAEDB.svg
  :target: https://saythanks.io/to/bachya

py17track is a simple Python library to track pacakges via
`17track.net <http://www.17track.net/>`_.

Installation
============

.. code-block:: bash

  $ pip install py17track

Usage
=====

Tracking individual packages via tracking number is easy!

.. code-block:: python

  from py17track import Client

  client = Client()

  # Use as many tracking numbers as you'd like:
  packages = client.track.find('12345ABCDE', '78901FGHIJ')
  # >>> {Package(...), Package(...)}

Each `Package` object has the following info:

* :code:`destination_country`: the country the package was shipped to
* :code:`info`: a text description of the latest status
* :code:`location`: the current location (if known)
* :code:`origin_country`: the country the package was shipped from
* :code:`package_type`: the type of package (if known)
* :code:`status`: the overall package status ("In Transit", "Delivered", etc.)
* :code:`tracking_info_language`: the language of the tracking info
* :code:`tracking_number`: the all-important tracking number

Since this is uses an unofficial API, there's no guarantee that 17track.net
will provide every field for every package, all the time.

If you have a 17track.net account, you can also find packages associated with
that account:

.. code-block:: python

  from py17track import Client

  client = Client()

  client.profile.authenticate('<EMAIL ADDRESS>', '<PASSWORD>')
  client.profile.packages()
  # >>> {Package(...), Package(...), Package(...), Package(...)}


Contributing
============

#. `Check for open features/bugs <https://github.com/bachya/py17track/issues>`_
   or `initiate a discussion on one <https://github.com/bachya/py17track/issues/new>`_.
#. `Fork the repository <https://github.com/bachya/py17track/fork>`_.
#. Install the dev environment: :code:`make init`.
#. Enter the virtual environment: :code:`pipenv shell`
#. Code your new feature or bug fix.
#. Write a test that covers your new functionality.
#. Run tests: :code:`make test`
#. Add yourself to AUTHORS.rst.
#. Submit a pull request!
