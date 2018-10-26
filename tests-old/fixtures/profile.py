"""Define generic fixtures to use anywhere."""

import pytest


@pytest.fixture(scope='session')
def authentication_failure():
    """Return a failed authentication response."""
    return {"Code": -6, "Message": "You haven't logged in for a long time."}


@pytest.fixture(scope='session')
def authentication_success():
    """Return a failed authentication response."""
    return {
        "Json": {
            "FUserRole": 4,
            "FNickname": "John Doe",
            "FEmail": "john.doe@company.com",
            "FLanguage": "en",
            "FCountry": 100,
            "FPhoto": 10001,
            "gid": "1234567890987654321"
        },
        "Code": 0
    }


@pytest.fixture(scope='session')
def email():
    """Return a dummy email."""
    return 'person@company.com'


@pytest.fixture(scope='session')
def packages():
    """Return package info from an account."""
    return {
        "pageInfo": {
            "Page": 1,
            "PerPage": 40,
            "TotalCount": 1
        },
        "Json": [{
            "FTrackInfoId": "1234567890987654321",
            "FTrackNo": "1234567890987654321",
            "FFirstCarrier": 0,
            "FFirstCarrierSource": 2,
            "FSecondCarrier": 0,
            "FSecondCarrierSource": 2,
            "FLastEvent": "{\"a\":\"2018-04-23 12:02\",\"b\":null,\"c\":\"\",\"d\":\"\",\"z\":\"Arrival at Destination Post\"}",
            "FIsArchived": False,
            "FRemark": "",
            "FTrackStateType": 0,
            "FCreateTime": "2018-05-04 20:22:13"
        }, {
            "FTrackInfoId": "1234567890987654321",
            "FTrackNo": "1234567890987654321",
            "FFirstCarrier": 0,
            "FFirstCarrierSource": 2,
            "FSecondCarrier": 0,
            "FSecondCarrierSource": 2,
            "FLastEvent": "",
            "FIsArchived": False,
            "FRemark": "",
            "FTrackStateType": 0,
            "FCreateTime": "2018-05-04 20:22:13"
        }]
    }


@pytest.fixture(scope='session')
def password():
    """Return a dummy password."""
    return '12345'


@pytest.fixture(scope='session')
def summary():
    """Return a summary of packages in a profile."""
    return {
        "Json": {
            "utn": {
                "cnum": "40",
                "unum": "9",
                "inum": "1",
                "anum": 22
            },
            "eitem": [{
                "e": 10,
                "ec": 6
            }, {
                "e": 0,
                "ec": 2
            }, {
                "e": 20,
                "ec": 0
            }, {
                "e": 30,
                "ec": 0
            }, {
                "e": 35,
                "ec": 0
            }, {
                "e": 40,
                "ec": 0
            }, {
                "e": 50,
                "ec": 0
            }]
        },
        "Code": 0
    }


@pytest.fixture(scope='session')
def tracking_number():
    """Return a dummy tracking number."""
    return '1234567890987654321'
