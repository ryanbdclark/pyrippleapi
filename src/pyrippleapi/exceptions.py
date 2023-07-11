class RippleError(Exception):
    """Generic exception"""


class RippleConnectionError(RippleError):
    """When a connection error occurs"""

class RippleDevicesError(RippleError):
    """When there are no generation assets"""

class RippleAuthenticationError(RippleError):
    """When an authentication token is invalid"""