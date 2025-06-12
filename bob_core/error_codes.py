"""bob_core.error_codes

Enhanced error code system with hierarchical categorization and rich context.
Implements comprehensive error handling following Niṣkāma Karma Yoga principles.
"""

from enum import IntEnum
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
import traceback
import logging

__all__ = ["ErrorCodes", "ErrorContext", "ErrorManager", "BOBError"]


class ErrorCodes(IntEnum):
    """Hierarchical error codes for BOB Google Maps."""
    
    # Success
    SUCCESS = 0
    
    # Browser/Driver Errors (1000-1099)
    BROWSER_INIT_FAILED = 1001
    BROWSER_CRASHED = 1002
    BROWSER_TIMEOUT = 1003
    WEBDRIVER_NOT_FOUND = 1004
    WEBDRIVER_VERSION_MISMATCH = 1005
    PLAYWRIGHT_NOT_AVAILABLE = 1006
    BROWSER_MEMORY_ERROR = 1007
    
    # Network/URL Errors (1100-1199)
    URL_LOAD_FAILED = 1101
    NETWORK_TIMEOUT = 1102
    CONNECTION_REFUSED = 1103
    DNS_RESOLUTION_FAILED = 1104
    SSL_CERTIFICATE_ERROR = 1105
    HTTP_ERROR_4XX = 1106
    HTTP_ERROR_5XX = 1107
    RATE_LIMITED = 1108
    
    # Parsing/Extraction Errors (1200-1299)
    BUSINESS_INFO_EXTRACTION_FAILED = 1201
    REVIEWS_BUTTON_NOT_FOUND = 1202
    REVIEWS_SCROLL_FAILED = 1203
    REVIEWS_EXTRACTION_FAILED = 1204
    COORDINATES_EXTRACTION_FAILED = 1205
    SELECTOR_NOT_FOUND = 1206
    ELEMENT_NOT_FOUND = 1207
    ELEMENT_NOT_CLICKABLE = 1208
    ELEMENT_STALE = 1209
    
    # Data Processing Errors (1300-1399)
    DATA_VALIDATION_FAILED = 1301
    DATA_SERIALIZATION_FAILED = 1302
    DATA_CORRUPTION = 1303
    DUPLICATE_DATA = 1304
    MISSING_REQUIRED_FIELD = 1305
    INVALID_DATA_FORMAT = 1306
    DATA_SIZE_EXCEEDED = 1307
    
    # File/Storage Errors (1400-1499)
    FILE_NOT_FOUND = 1401
    FILE_PERMISSION_DENIED = 1402
    DISK_SPACE_FULL = 1403
    CSV_SAVE_FAILED = 1404
    JSON_SAVE_FAILED = 1405
    EXCEL_SAVE_FAILED = 1406
    DATABASE_CONNECTION_FAILED = 1407
    DATABASE_QUERY_FAILED = 1408
    
    # Configuration Errors (1500-1599)
    CONFIG_FILE_NOT_FOUND = 1501
    CONFIG_PARSE_ERROR = 1502
    INVALID_CONFIG_VALUE = 1503
    MISSING_CONFIG_KEY = 1504
    CONFIG_VALIDATION_FAILED = 1505
    
    # System/Resource Errors (1600-1699)
    MEMORY_EXHAUSTED = 1601
    CPU_OVERLOAD = 1602
    DISK_FULL = 1603
    SYSTEM_RESOURCE_UNAVAILABLE = 1604
    PERMISSION_DENIED = 1605
    
    # Circuit Breaker/Resilience Errors (1700-1799)
    CIRCUIT_BREAKER_OPEN = 1701
    MAX_RETRIES_EXCEEDED = 1702
    TIMEOUT_EXCEEDED = 1703
    HEALTH_CHECK_FAILED = 1704
    SERVICE_UNAVAILABLE = 1705
    
    # Analytics/Processing Errors (1800-1899)
    SENTIMENT_ANALYSIS_FAILED = 1801
    KEYWORD_EXTRACTION_FAILED = 1802
    ANALYTICS_COMPUTATION_FAILED = 1803
    TEXTBLOB_NOT_AVAILABLE = 1804
    
    # Generic/Unexpected Errors (1900-1999)
    UNEXPECTED_ERROR = 1999
    
    @classmethod
    def get_category(cls, error_code: int) -> str:
        """Get error category based on error code."""
        if error_code == 0:
            return "success"
        elif 1000 <= error_code < 1100:
            return "browser"
        elif 1100 <= error_code < 1200:
            return "network"
        elif 1200 <= error_code < 1300:
            return "parsing"
        elif 1300 <= error_code < 1400:
            return "data"
        elif 1400 <= error_code < 1500:
            return "storage"
        elif 1500 <= error_code < 1600:
            return "config"
        elif 1600 <= error_code < 1700:
            return "system"
        elif 1700 <= error_code < 1800:
            return "resilience"
        elif 1800 <= error_code < 1900:
            return "analytics"
        else:
            return "unknown"
    
    @classmethod
    def get_severity(cls, error_code: int) -> str:
        """Get error severity level."""
        if error_code == 0:
            return "success"
        elif error_code in [cls.RATE_LIMITED, cls.CIRCUIT_BREAKER_OPEN]:
            return "warning"
        elif error_code in [cls.BROWSER_CRASHED, cls.MEMORY_EXHAUSTED, cls.DISK_FULL]:
            return "critical"
        else:
            return "error"


@dataclass
class ErrorContext:
    """Rich error context with debugging information."""
    
    error_code: int
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    category: str = field(init=False)
    severity: str = field(init=False)
    
    # Context information
    url: Optional[str] = None
    component: Optional[str] = None
    operation: Optional[str] = None
    user_agent: Optional[str] = None
    
    # Technical details
    exception_type: Optional[str] = None
    stack_trace: Optional[str] = None
    system_info: Dict[str, Any] = field(default_factory=dict)
    
    # Recovery information
    retry_count: int = 0
    max_retries: int = 3
    recovery_suggestions: List[str] = field(default_factory=list)
    
    # Additional metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Set derived fields after initialization."""
        self.category = ErrorCodes.get_category(self.error_code)
        self.severity = ErrorCodes.get_severity(self.error_code)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "error_code": self.error_code,
            "message": self.message,
            "timestamp": self.timestamp.isoformat(),
            "category": self.category,
            "severity": self.severity,
            "url": self.url,
            "component": self.component,
            "operation": self.operation,
            "user_agent": self.user_agent,
            "exception_type": self.exception_type,
            "stack_trace": self.stack_trace,
            "system_info": self.system_info,
            "retry_count": self.retry_count,
            "max_retries": self.max_retries,
            "recovery_suggestions": self.recovery_suggestions,
            "metadata": self.metadata
        }
    
    def add_recovery_suggestion(self, suggestion: str) -> None:
        """Add a recovery suggestion."""
        if suggestion not in self.recovery_suggestions:
            self.recovery_suggestions.append(suggestion)
    
    def can_retry(self) -> bool:
        """Check if operation can be retried."""
        return self.retry_count < self.max_retries and self.severity != "critical"


class BOBError(Exception):
    """Base exception class for BOB Google Maps with rich error context."""
    
    def __init__(self, 
                 error_code: int,
                 message: str,
                 **context_kwargs):
        super().__init__(message)
        self.context = ErrorContext(
            error_code=error_code,
            message=message,
            **context_kwargs
        )
        
        # Capture stack trace
        self.context.stack_trace = traceback.format_exc()
        
        # Set exception type
        self.context.exception_type = self.__class__.__name__
    
    def __str__(self) -> str:
        return f"[{self.context.error_code}] {self.context.message}"
    
    def __repr__(self) -> str:
        return f"BOBError(error_code={self.context.error_code}, message='{self.context.message}')"


class ErrorManager:
    """Central error management system for tracking and analyzing errors."""
    
    def __init__(self):
        self.error_history: List[ErrorContext] = []
        self.error_patterns: Dict[int, int] = {}  # error_code -> count
        self.recovery_stats: Dict[str, Dict[str, int]] = {}
        self._logger = logging.getLogger("bob_core.error_manager")
        self._max_history = 1000
    
    def record_error(self, error_context: ErrorContext) -> None:
        """Record an error for tracking and analysis."""
        # Add to history
        self.error_history.append(error_context)
        
        # Limit history size
        if len(self.error_history) > self._max_history:
            self.error_history = self.error_history[-self._max_history:]
        
        # Update patterns
        self.error_patterns[error_context.error_code] = (
            self.error_patterns.get(error_context.error_code, 0) + 1
        )
        
        # Update recovery stats
        category = error_context.category
        if category not in self.recovery_stats:
            self.recovery_stats[category] = {"total": 0, "recovered": 0}
        
        self.recovery_stats[category]["total"] += 1
        
        # Log the error
        self._logger.error(
            f"Error recorded: [{error_context.error_code}] {error_context.message} "
            f"(Category: {error_context.category}, Severity: {error_context.severity})"
        )
    
    def record_recovery(self, error_context: ErrorContext) -> None:
        """Record a successful recovery from an error."""
        category = error_context.category
        if category in self.recovery_stats:
            self.recovery_stats[category]["recovered"] += 1
        
        self._logger.info(f"Recovery recorded for error {error_context.error_code}")
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """Get comprehensive error statistics."""
        total_errors = len(self.error_history)
        
        if total_errors == 0:
            return {"total_errors": 0, "categories": {}, "patterns": {}}
        
        # Category breakdown
        category_stats = {}
        for error in self.error_history:
            cat = error.category
            if cat not in category_stats:
                category_stats[cat] = {"count": 0, "severity_breakdown": {}}
            
            category_stats[cat]["count"] += 1
            severity = error.severity
            category_stats[cat]["severity_breakdown"][severity] = (
                category_stats[cat]["severity_breakdown"].get(severity, 0) + 1
            )
        
        # Most common errors
        top_errors = sorted(
            self.error_patterns.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:10]
        
        # Recovery rates
        recovery_rates = {}
        for category, stats in self.recovery_stats.items():
            if stats["total"] > 0:
                recovery_rates[category] = stats["recovered"] / stats["total"]
        
        return {
            "total_errors": total_errors,
            "categories": category_stats,
            "top_errors": [{"error_code": code, "count": count} for code, count in top_errors],
            "recovery_rates": recovery_rates,
            "recent_errors": [
                error.to_dict() for error in self.error_history[-10:]
            ]
        }
    
    def get_recovery_suggestions(self, error_code: int) -> List[str]:
        """Get recovery suggestions for a specific error code."""
        suggestions = []
        
        # Generic suggestions based on category
        category = ErrorCodes.get_category(error_code)
        
        if category == "browser":
            suggestions.extend([
                "Restart the browser",
                "Update ChromeDriver/WebDriver",
                "Check browser installation",
                "Try different browser options"
            ])
        elif category == "network":
            suggestions.extend([
                "Check internet connection",
                "Retry with exponential backoff",
                "Use different proxy/VPN",
                "Verify URL accessibility"
            ])
        elif category == "parsing":
            suggestions.extend([
                "Update CSS selectors",
                "Wait for page to load completely",
                "Check if page structure changed",
                "Try alternative parsing strategy"
            ])
        elif category == "data":
            suggestions.extend([
                "Validate input data",
                "Check data format requirements",
                "Clean and normalize data",
                "Implement data validation"
            ])
        elif category == "storage":
            suggestions.extend([
                "Check disk space",
                "Verify file permissions",
                "Use alternative storage location",
                "Implement data compression"
            ])
        elif category == "system":
            suggestions.extend([
                "Free up system resources",
                "Restart the application",
                "Check system requirements",
                "Monitor resource usage"
            ])
        
        # Specific suggestions for common errors
        if error_code == ErrorCodes.RATE_LIMITED:
            suggestions.extend([
                "Implement exponential backoff",
                "Reduce request frequency",
                "Use multiple IP addresses",
                "Respect robots.txt"
            ])
        elif error_code == ErrorCodes.CIRCUIT_BREAKER_OPEN:
            suggestions.extend([
                "Wait for circuit breaker to reset",
                "Check service health",
                "Use fallback mechanism",
                "Implement graceful degradation"
            ])
        
        return suggestions
    
    def clear_history(self) -> None:
        """Clear error history and statistics."""
        self.error_history.clear()
        self.error_patterns.clear()
        self.recovery_stats.clear()
        self._logger.info("Error history cleared")


# Global error manager instance
_global_error_manager: Optional[ErrorManager] = None


def get_error_manager() -> ErrorManager:
    """Get the global error manager instance."""
    global _global_error_manager
    if _global_error_manager is None:
        _global_error_manager = ErrorManager()
    return _global_error_manager


def create_error_context(error_code: int, 
                        message: str,
                        **kwargs) -> ErrorContext:
    """Factory function to create error context with recovery suggestions."""
    context = ErrorContext(error_code=error_code, message=message, **kwargs)
    
    # Add recovery suggestions
    suggestions = get_error_manager().get_recovery_suggestions(error_code)
    context.recovery_suggestions.extend(suggestions)
    
    return context


def handle_error(error_code: int,
                message: str,
                raise_exception: bool = True,
                **context_kwargs) -> ErrorContext:
    """Central error handling function."""
    context = create_error_context(error_code, message, **context_kwargs)
    
    # Record the error
    get_error_manager().record_error(context)
    
    if raise_exception:
        raise BOBError(error_code, message, **context_kwargs)
    
    return context 