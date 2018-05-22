"""Define module exceptions."""


class HTTPError(Exception):
    """Define a generic HTTP error (i.e., a wrapper for Requests)."""
    pass


class InvalidTrackingNumberError(ValueError):
    """Define an error for an invalid tracking number."""
    pass
