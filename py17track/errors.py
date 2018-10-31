"""Define module exceptions."""


class SeventeenTrackError(Exception):
    """Define a base error."""

    pass


class InvalidTrackingNumberError(SeventeenTrackError):
    """Define an error for an invalid tracking number."""

    pass


class RequestError(SeventeenTrackError):
    """Define an error for HTTP request errors."""

    pass
