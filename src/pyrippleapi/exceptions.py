class RippleError(Exception):
    """Generic exception"""


class RippleConnectionError(RippleError):
    """When a connection error occurs"""
