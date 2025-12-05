"""
Custom exception classes for BOB Google Maps Extractor.

This module defines a hierarchy of custom exceptions for better error handling
and debugging throughout the BOB Google Maps extraction system.

Version: 4.3.0
"""

from typing import Optional, Dict, Any


# ============================================================================
# BASE EXCEPTIONS
# ============================================================================

class BOBException(Exception):
    """
    Base exception class for all BOB Google Maps exceptions.

    All custom exceptions in the BOB system inherit from this class.
    """

    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        original_exception: Optional[Exception] = None
    ):
        """
        Initialize BOB exception.

        Args:
            message: Human-readable error message
            details: Additional context about the error
            original_exception: Original exception if this wraps another error
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}
        self.original_exception = original_exception

    def __str__(self) -> str:
        """Return formatted error message."""
        error_msg = self.message
        if self.details:
            error_msg += f" | Details: {self.details}"
        if self.original_exception:
            error_msg += f" | Original error: {str(self.original_exception)}"
        return error_msg


# ============================================================================
# EXTRACTION EXCEPTIONS
# ============================================================================

class ExtractionError(BOBException):
    """
    Base exception for all extraction-related errors.

    Raised when business data extraction fails.
    """
    pass


class ExtractionTimeout(ExtractionError):
    """
    Raised when extraction operation times out.

    Example:
        raise ExtractionTimeout(
            "Extraction timed out after 30 seconds",
            details={"business_name": "Example Corp", "timeout": 30}
        )
    """
    pass


class ExtractionValidationError(ExtractionError):
    """
    Raised when extracted data fails validation.

    Example:
        raise ExtractionValidationError(
            "Extracted business has no name or place_id",
            details={"data": extracted_data}
        )
    """
    pass


class NoResultsFound(ExtractionError):
    """
    Raised when no business results are found for a query.

    Example:
        raise NoResultsFound(
            "No businesses found for query",
            details={"query": "NonexistentBusiness12345"}
        )
    """
    pass


class MultipleResultsError(ExtractionError):
    """
    Raised when multiple businesses found but only one expected.

    Example:
        raise MultipleResultsError(
            "Found 5 businesses, expected 1",
            details={"count": 5, "query": "Generic Name"}
        )
    """
    pass


class PlaceIDError(ExtractionError):
    """
    Raised when Place ID extraction or validation fails.

    Example:
        raise PlaceIDError(
            "Invalid Place ID format",
            details={"place_id": "invalid_id"}
        )
    """
    pass


# ============================================================================
# BROWSER/ENGINE EXCEPTIONS
# ============================================================================

class BrowserError(BOBException):
    """
    Base exception for browser-related errors.

    Raised when browser automation fails.
    """
    pass


class BrowserLaunchError(BrowserError):
    """
    Raised when browser fails to launch.

    Example:
        raise BrowserLaunchError(
            "Failed to launch Chrome browser",
            details={"browser": "chrome", "headless": True}
        )
    """
    pass


class BrowserNavigationError(BrowserError):
    """
    Raised when browser navigation fails.

    Example:
        raise BrowserNavigationError(
            "Failed to navigate to Google Maps",
            details={"url": "https://maps.google.com"}
        )
    """
    pass


class ElementNotFoundError(BrowserError):
    """
    Raised when expected DOM element is not found.

    Example:
        raise ElementNotFoundError(
            "Business name element not found",
            details={"selector": ".business-name"}
        )
    """
    pass


class PageLoadError(BrowserError):
    """
    Raised when page fails to load properly.

    Example:
        raise PageLoadError(
            "Page load timeout after 30 seconds",
            details={"url": "https://maps.google.com", "timeout": 30}
        )
    """
    pass


# ============================================================================
# CACHE EXCEPTIONS
# ============================================================================

class CacheError(BOBException):
    """
    Base exception for cache-related errors.

    Raised when cache operations fail.
    """
    pass


class CacheDatabaseError(CacheError):
    """
    Raised when SQLite database operations fail.

    Example:
        raise CacheDatabaseError(
            "Failed to connect to cache database",
            details={"db_path": "/path/to/cache.db"}
        )
    """
    pass


class CacheCorruptionError(CacheError):
    """
    Raised when cache data appears corrupted.

    Example:
        raise CacheCorruptionError(
            "Cache entry has invalid JSON data",
            details={"place_id": "ChIJ..."}
        )
    """
    pass


class CacheWriteError(CacheError):
    """
    Raised when writing to cache fails.

    Example:
        raise CacheWriteError(
            "Failed to write business to cache",
            details={"business_name": "Example Corp"}
        )
    """
    pass


# ============================================================================
# CONFIGURATION EXCEPTIONS
# ============================================================================

class ConfigurationError(BOBException):
    """
    Base exception for configuration-related errors.

    Raised when configuration is invalid or missing.
    """
    pass


class InvalidConfigurationError(ConfigurationError):
    """
    Raised when configuration values are invalid.

    Example:
        raise InvalidConfigurationError(
            "Invalid timeout value",
            details={"timeout": -10, "expected": "positive integer"}
        )
    """
    pass


class MissingConfigurationError(ConfigurationError):
    """
    Raised when required configuration is missing.

    Example:
        raise MissingConfigurationError(
            "Required environment variable not set",
            details={"variable": "GOOGLE_MAPS_API_KEY"}
        )
    """
    pass


class ConfigurationFileError(ConfigurationError):
    """
    Raised when configuration file cannot be read or parsed.

    Example:
        raise ConfigurationFileError(
            "Failed to parse config.yaml",
            details={"file": "config.yaml"}
        )
    """
    pass


# ============================================================================
# DATA MODEL EXCEPTIONS
# ============================================================================

class DataModelError(BOBException):
    """
    Base exception for data model errors.

    Raised when data model operations fail.
    """
    pass


class InvalidBusinessDataError(DataModelError):
    """
    Raised when business data is invalid or incomplete.

    Example:
        raise InvalidBusinessDataError(
            "Business missing required fields",
            details={"missing": ["name", "place_id"]}
        )
    """
    pass


class DataConversionError(DataModelError):
    """
    Raised when data type conversion fails.

    Example:
        raise DataConversionError(
            "Failed to convert rating to float",
            details={"value": "not_a_number"}
        )
    """
    pass


class DataSerializationError(DataModelError):
    """
    Raised when data serialization fails.

    Example:
        raise DataSerializationError(
            "Failed to serialize business to JSON",
            details={"business_name": "Example Corp"}
        )
    """
    pass


# ============================================================================
# BATCH PROCESSING EXCEPTIONS
# ============================================================================

class BatchProcessingError(BOBException):
    """
    Base exception for batch processing errors.

    Raised when batch operations fail.
    """
    pass


class BatchValidationError(BatchProcessingError):
    """
    Raised when batch input validation fails.

    Example:
        raise BatchValidationError(
            "Invalid business queries in batch",
            details={"invalid_count": 5, "total": 100}
        )
    """
    pass


class BatchPartialFailureError(BatchProcessingError):
    """
    Raised when some businesses in batch fail extraction.

    Example:
        raise BatchPartialFailureError(
            "10 of 100 businesses failed extraction",
            details={"failed": 10, "succeeded": 90, "total": 100}
        )
    """
    pass


# ============================================================================
# NETWORK EXCEPTIONS
# ============================================================================

class NetworkError(BOBException):
    """
    Base exception for network-related errors.

    Raised when network operations fail.
    """
    pass


class ConnectionError(NetworkError):
    """
    Raised when network connection fails.

    Example:
        raise ConnectionError(
            "Failed to connect to Google Maps",
            details={"url": "https://maps.google.com"}
        )
    """
    pass


class RateLimitError(NetworkError):
    """
    Raised when rate limit is exceeded.

    Example:
        raise RateLimitError(
            "Google Maps rate limit exceeded",
            details={"retry_after": 60}
        )
    """
    pass


class ProxyError(NetworkError):
    """
    Raised when proxy connection fails.

    Example:
        raise ProxyError(
            "Failed to connect through proxy",
            details={"proxy": "http://proxy.example.com:8080"}
        )
    """
    pass


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def wrap_exception(
    original_exception: Exception,
    new_exception_class: type,
    message: str,
    details: Optional[Dict[str, Any]] = None
) -> BOBException:
    """
    Wrap an existing exception in a BOB exception.

    Args:
        original_exception: The original exception to wrap
        new_exception_class: The BOB exception class to use
        message: Human-readable error message
        details: Additional context

    Returns:
        New BOB exception wrapping the original

    Example:
        try:
            risky_operation()
        except ValueError as e:
            raise wrap_exception(
                e,
                ConfigurationError,
                "Invalid configuration value",
                {"key": "timeout"}
            )
    """
    return new_exception_class(
        message=message,
        details=details,
        original_exception=original_exception
    )


def is_bob_exception(exception: Exception) -> bool:
    """
    Check if an exception is a BOB exception.

    Args:
        exception: Exception to check

    Returns:
        True if exception is a BOB exception

    Example:
        try:
            extractor.extract_business("query")
        except Exception as e:
            if is_bob_exception(e):
                print(f"BOB Error: {e.message}")
            else:
                print(f"Unknown Error: {str(e)}")
    """
    return isinstance(exception, BOBException)


# ============================================================================
# EXCEPTION HIERARCHY DOCUMENTATION
# ============================================================================

"""
EXCEPTION HIERARCHY:

BOBException (Base)
├── ExtractionError
│   ├── ExtractionTimeout
│   ├── ExtractionValidationError
│   ├── NoResultsFound
│   ├── MultipleResultsError
│   └── PlaceIDError
├── BrowserError
│   ├── BrowserLaunchError
│   ├── BrowserNavigationError
│   ├── ElementNotFoundError
│   └── PageLoadError
├── CacheError
│   ├── CacheDatabaseError
│   ├── CacheCorruptionError
│   └── CacheWriteError
├── ConfigurationError
│   ├── InvalidConfigurationError
│   ├── MissingConfigurationError
│   └── ConfigurationFileError
├── DataModelError
│   ├── InvalidBusinessDataError
│   ├── DataConversionError
│   └── DataSerializationError
├── BatchProcessingError
│   ├── BatchValidationError
│   └── BatchPartialFailureError
└── NetworkError
    ├── ConnectionError
    ├── RateLimitError
    └── ProxyError

USAGE GUIDELINES:

1. Always use specific exceptions (leaf nodes) when possible
2. Use base exceptions (branch nodes) for catching broad categories
3. Include meaningful details dict with context
4. Wrap non-BOB exceptions using wrap_exception()
5. Log exceptions properly before raising

Example:
    try:
        browser.navigate(url)
    except TimeoutException as e:
        raise wrap_exception(
            e,
            BrowserNavigationError,
            f"Failed to navigate to {url}",
            {"url": url, "timeout": 30}
        )
"""
