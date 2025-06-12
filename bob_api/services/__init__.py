"""bob_api.services

Service layer for BOB Google Maps API v0.6.0
Divine service abstraction following Niṣkāma Karma Yoga principles.

Made with 🙏 for interconnected excellence
"""

from .interfaces import ScrapingService, HealthService, AnalyticsService, MetricsService
from .factory import ServiceFactory
from .async_scraper import AsyncScrapingService
from .health_service import HealthServiceImpl
from .analytics_service import AnalyticsServiceImpl
from .metrics_service import MetricsServiceImpl

__all__ = [
    "ScrapingService",
    "HealthService", 
    "AnalyticsService",
    "MetricsService",
    "ServiceFactory",
    "AsyncScrapingService",
    "HealthServiceImpl",
    "AnalyticsServiceImpl",
    "MetricsServiceImpl"
]

# Global service factory instance
_service_factory = None

async def get_service_factory() -> ServiceFactory:
    """Get the global service factory instance."""
    global _service_factory
    if _service_factory is None:
        _service_factory = ServiceFactory()
        await _service_factory.initialize()
    return _service_factory 