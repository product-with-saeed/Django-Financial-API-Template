from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class TransactionUserThrottle(UserRateThrottle):
    """
    Custom throttle for authenticated users.
    Limits transaction-related API requests.
    """

    rate = "500/day"


class TransactionAnonThrottle(AnonRateThrottle):
    """
    Custom throttle for anonymous users.
    """

    rate = "5/minute"
