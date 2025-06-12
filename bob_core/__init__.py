"""bob_core

BOB Google Maps - Build Online Business toolkit
Made in India 🇮🇳, Made for the World 🌍

A comprehensive Google Maps scraping and business intelligence platform
following the principles of Niṣkāma Karma Yoga - selfless service with perfect execution.

Version 0.5.0 - Divine Perfection Release
- Enterprise-grade fault tolerance and self-healing
- Advanced performance monitoring and optimization
- Comprehensive error handling and recovery
- Adaptive timeout management and circuit breakers
- Memory management and connection pooling
- Graceful degradation and auto-recovery systems
"""

__version__ = "0.5.0"

# Core functionality
from .cli import main as _cli_main

# Enhanced fault tolerance and monitoring systems
from .circuit_breaker import CircuitBreaker, get_circuit_breaker
from .dead_letter_queue import DeadLetterQueue, get_global_dlq
from .graceful_degradation import GracefulDegradationManager, get_global_degradation_manager
from .auto_recovery import AutoRecoveryManager, get_global_recovery_manager
from .selector_healing import SelectorHealer, get_global_selector_healer
from .memory_management import MemoryManager, get_global_memory_manager
from .connection_pooling import ConnectionManager, get_global_connection_manager
from .performance_monitoring import PerformanceMonitor, get_global_performance_monitor

# Core scraping and data models
from .scraper import GoogleMapsScraper
from .models import BusinessInfo, Review, ScrapeResult, BatchConfig
from .error_codes import ErrorCodes, ErrorContext, BOBError

# Analytics and export
from .analytics import BusinessAnalyzer, ReviewAnalyzer, MarketAnalyzer
from .export import JSONExporter, CSVExporter, ExcelExporter

__all__ = [
    # Version
    "__version__",
    
    # Core functionality
    "GoogleMapsScraper",
    
    # Data models
    "BusinessInfo", "Review", "ScrapeResult", "BatchConfig",
    
    # Error handling
    "ErrorCodes", "ErrorContext", "BOBError",
    
    # Fault tolerance systems
    "CircuitBreaker", "get_circuit_breaker",
    "DeadLetterQueue", "get_global_dlq",
    "GracefulDegradationManager", "get_global_degradation_manager",
    "AutoRecoveryManager", "get_global_recovery_manager",
    "SelectorHealer", "get_global_selector_healer",
    "MemoryManager", "get_global_memory_manager",
    "ConnectionManager", "get_global_connection_manager",
    "PerformanceMonitor", "get_global_performance_monitor",
    
    # Analytics
    "BusinessAnalyzer", "ReviewAnalyzer", "MarketAnalyzer",
    
    # Export
    "JSONExporter", "CSVExporter", "ExcelExporter",
]

def cli():
    """Entry point for CLI."""
    return _cli_main()

# Initialize global systems for divine perfection
def initialize_divine_systems():
    """Initialize all fault tolerance and monitoring systems."""
    # Start performance monitoring
    perf_monitor = get_global_performance_monitor()
    perf_monitor.start_monitoring()
    
    # Initialize memory management
    memory_manager = get_global_memory_manager()
    memory_manager.start_monitoring()
    
    # Initialize auto-recovery
    recovery_manager = get_global_recovery_manager()
    recovery_manager.start_monitoring()
    
    return {
        "performance_monitor": perf_monitor,
        "memory_manager": memory_manager,
        "recovery_manager": recovery_manager,
        "circuit_breaker": get_circuit_breaker("global"),
        "dead_letter_queue": get_global_dlq(),
        "degradation_manager": get_global_degradation_manager(),
        "selector_healer": get_global_selector_healer(),
        "connection_manager": get_global_connection_manager()
    }

# Auto-initialize on import for seamless experience
_divine_systems = None

def get_divine_systems():
    """Get initialized divine systems."""
    global _divine_systems
    if _divine_systems is None:
        _divine_systems = initialize_divine_systems()
    return _divine_systems 