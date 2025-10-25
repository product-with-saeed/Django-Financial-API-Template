"""
Custom throttling classes for the Financial API.
Defines rate limiting for transaction-related API requests.
"""

from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class TransactionUserThrottle(UserRateThrottle):
    """
    Custom throttle for authenticated users.

    Limits transaction-related API requests to prevent abuse.
    Default rate: 500 requests per day.

    Attributes:
        rate: The throttle rate in format "num_requests/period".

    Examples:
        >>> throttle = TransactionUserThrottle()
        >>> throttle.rate
        '500/day'
    """

    rate: str = "500/day"


class TransactionAnonThrottle(AnonRateThrottle):
    """
    Custom throttle for anonymous users.

    Limits transaction-related API requests for unauthenticated users.
    Default rate: 5 requests per minute.

    Attributes:
        rate: The throttle rate in format "num_requests/period".

    Examples:
        >>> throttle = TransactionAnonThrottle()
        >>> throttle.rate
        '5/minute'
    """

    rate: str = "5/minute"
