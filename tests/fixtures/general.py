"""Define generic fixtures to use anywhere."""

import pytest


@pytest.fixture(scope='session')
def failure_one_package():
    """Return a failed response for one package."""
    return {
        "ret": 1,
        "msg": "Ok",
        "g": "89b4aae67c414a968142239d0716e1a0",
        "dat": []
    }


@pytest.fixture(scope='session')
def successful_one_package_1():
    """Return a successful response for one package."""
    return {
        "ret": 1,
        "msg": "Ok",
        "g": "89b4aae67c414a968142239d0716e1a0",
        "dat": [{
            "no": "12345ABCDEF",
            "delay": 0,
            "yt": None,
            "track": {
                "b": 1404,
                "c": 0,
                "e": 40,
                "f": 8,
                "w1": 14044,
                "w2": 0,
                "ln1": "en",
                "ln2": None,
                "is1": 1,
                "is2": 2,
                "ygt1": 0,
                "ygt2": 0,
                "ylt1": "2018-05-17 17:03:35",
                "ylt2": "2079-01-01 00:00:00",
                "hs": -2093193954,
                "yt": None,
                "z0": {
                    "a": "2018-05-02 16:03",
                    "b": None,
                    "c": "",
                    "d": "",
                    "z": "The item has been delivered successfully"
                },
                "z1": [{
                    "a": "2018-05-02 16:03",
                    "b": None,
                    "c": "",
                    "d": "",
                    "z": "The item has been delivered successfully"
                }, {
                    "a": "2018-05-02 09:21",
                    "b": None,
                    "c": "",
                    "d": "",
                    "z": "Receive item at delivery office (Inb)"
                }, {
                    "a": "2018-05-02 08:53",
                    "b": None,
                    "c": "",
                    "d": "",
                    "z": "Receive item at delivery office (Inb)"
                }, {
                    "a": "2018-05-01 11:30",
                    "b": None,
                    "c": "",
                    "d": "",
                    "z": "The item has been processed"
                }, {
                    "a": "2018-04-30 07:34",
                    "b": None,
                    "c": "",
                    "d": "",
                    "z": "The item has arrived in the country of destination"
                }, {
                    "a": "2018-04-30 07:29",
                    "b": None,
                    "c": "",
                    "d": "",
                    "z": "Consignment received at the PostNL Acceptance Centre"
                }, {
                    "a": "2018-04-27 04:07",
                    "b": None,
                    "c": "",
                    "d": "",
                    "z": "The item is ready for shipment"
                }, {
                    "a": "2018-04-25 03:55",
                    "b": None,
                    "c": "",
                    "d": "",
                    "z": "The item is pre-advised"
                }, {
                    "a": "2018-04-25 03:52",
                    "b": None,
                    "c": "",
                    "d": "",
                    "z": "The Item is at the shippers warehouse"
                }],
                "z2": [],
                "zex": {
                    "sa": False
                }
            }
        }]
    }


@pytest.fixture(scope='session')
def successful_one_package_2():
    """Return a successful response for one package."""
    return {
        "ret": 1,
        "msg": "Ok",
        "g": "89b4aae67c414a968142239d0716e1a0",
        "dat": [{
            "no": "12345ABCDEF",
            "delay": 0,
            "yt": None,
            "track": {
                "b": 1404,
                "c": 0,
                "e": 0,
                "f": 8,
                "w1": 14044,
                "w2": 0,
                "ln1": "en",
                "ln2": None,
                "is1": 1,
                "is2": 2,
                "ygt1": 0,
                "ygt2": 0,
                "ylt1": "2018-05-17 17:03:35",
                "ylt2": "2079-01-01 00:00:00",
                "hs": -2093193954,
                "yt": None,
                "z0": {
                    "a": "2018-05-02 16:03",
                    "b": None,
                    "c": "",
                    "d": "",
                    "z": "The item has been delivered successfully"
                },
                "z1": [{
                    "a": "2018-05-02 16:03",
                    "b": None,
                    "c": "",
                    "d": "",
                    "z": "The item has been delivered successfully"
                }, {
                    "a": "2018-05-02 09:21",
                    "b": None,
                    "c": "",
                    "d": "",
                    "z": "Receive item at delivery office (Inb)"
                }, {
                    "a": "2018-05-02 08:53",
                    "b": None,
                    "c": "",
                    "d": "",
                    "z": "Receive item at delivery office (Inb)"
                }, {
                    "a": "2018-05-01 11:30",
                    "b": None,
                    "c": "",
                    "d": "",
                    "z": "The item has been processed"
                }, {
                    "a": "2018-04-30 07:34",
                    "b": None,
                    "c": "",
                    "d": "",
                    "z": "The item has arrived in the country of destination"
                }, {
                    "a": "2018-04-30 07:29",
                    "b": None,
                    "c": "",
                    "d": "",
                    "z": "Consignment received at the PostNL Acceptance Centre"
                }, {
                    "a": "2018-04-27 04:07",
                    "b": None,
                    "c": "",
                    "d": "",
                    "z": "The item is ready for shipment"
                }, {
                    "a": "2018-04-25 03:55",
                    "b": None,
                    "c": "",
                    "d": "",
                    "z": "The item is pre-advised"
                }, {
                    "a": "2018-04-25 03:52",
                    "b": None,
                    "c": "",
                    "d": "",
                    "z": "The Item is at the shippers warehouse"
                }],
                "z2": [],
                "zex": {
                    "sa": False
                }
            }
        }]
    }


@pytest.fixture(scope='session')
def tracking_number():
    """Return a sample tracking number."""
    return '12345ABCDEF'
