"""bob_core.error_codes

Standardized error codes used across BOB Google Maps modules.
"""

from enum import IntEnum

__all__ = ["ErrorCodes"]

class ErrorCodes(IntEnum):
    SUCCESS = 0
    BROWSER_INIT_FAILED = 1001
    URL_LOAD_FAILED = 1002
    BUSINESS_INFO_EXTRACTION_FAILED = 1003
    REVIEWS_BUTTON_NOT_FOUND = 1004
    REVIEWS_SCROLL_FAILED = 1005
    REVIEWS_EXTRACTION_FAILED = 1006
    COORDINATES_EXTRACTION_FAILED = 1007
    CSV_SAVE_FAILED = 1008
    NETWORK_TIMEOUT = 1009
    ELEMENT_NOT_FOUND = 1010
    UNEXPECTED_ERROR = 1999 