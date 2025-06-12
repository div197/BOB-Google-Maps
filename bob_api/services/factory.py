"""bob_api.services.factory

Service Factory for BOB Google Maps API v0.6.0
Divine dependency injection following Niṣkāma Karma Yoga principles.

Made with 🙏 for interconnected excellence
"""

import asyncio
from typing import Dict, Any, Optional, Type
from functools import lru_cache

from .interfaces import (
    ScrapingService, HealthService, AnalyticsService, 
    MetricsService, JobService, CacheService
)
from .async_scraper import AsyncScrapingService
from .health_service import HealthServiceImpl
from .analytics_service import AnalyticsServiceImpl
from .metrics_service import MetricsServiceImpl
from .job_service import JobServiceImpl
from .cache_service import CacheServiceImpl

from ..config import get_settings


class ServiceFactory:
    """Divine service factory for dependency injection."""
    
    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._settings = get_settings()
        self._initialized = False
    
    async def initialize(self):
        """Initialize all services with divine coordination."""
        if self._initialized:
            return
        
        # Initialize services in proper order
        await self._initialize_cache_service()
        await self._initialize_metrics_service()
        await self._initialize_health_service()
        await self._initialize_analytics_service()
        await self._initialize_scraping_service()
        await self._initialize_job_service()
        
        self._initialized = True
    
    async def _initialize_cache_service(self):
        """Initialize cache service."""
        cache_service = CacheServiceImpl(
            redis_url=self._settings.REDIS_URL,
            default_ttl=3600  # 1 hour default
        )
        await cache_service.initialize()
        self._services['cache'] = cache_service
    
    async def _initialize_metrics_service(self):
        """Initialize metrics service."""
        metrics_service = MetricsServiceImpl(
            cache_service=self._services.get('cache')
        )
        await metrics_service.initialize()
        self._services['metrics'] = metrics_service
    
    async def _initialize_health_service(self):
        """Initialize health service."""
        health_service = HealthServiceImpl(
            metrics_service=self._services.get('metrics'),
            cache_service=self._services.get('cache')
        )
        await health_service.initialize()
        self._services['health'] = health_service
    
    async def _initialize_analytics_service(self):
        """Initialize analytics service."""
        analytics_service = AnalyticsServiceImpl(
            cache_service=self._services.get('cache'),
            metrics_service=self._services.get('metrics')
        )
        await analytics_service.initialize()
        self._services['analytics'] = analytics_service
    
    async def _initialize_scraping_service(self):
        """Initialize scraping service."""
        scraping_service = AsyncScrapingService(
            health_service=self._services.get('health'),
            metrics_service=self._services.get('metrics'),
            cache_service=self._services.get('cache'),
            analytics_service=self._services.get('analytics')
        )
        await scraping_service.initialize()
        self._services['scraping'] = scraping_service
    
    async def _initialize_job_service(self):
        """Initialize job service."""
        job_service = JobServiceImpl(
            scraping_service=self._services.get('scraping'),
            cache_service=self._services.get('cache'),
            metrics_service=self._services.get('metrics')
        )
        await job_service.initialize()
        self._services['job'] = job_service
    
    def get_scraping_service(self) -> ScrapingService:
        """Get scraping service instance."""
        if not self._initialized:
            raise RuntimeError("ServiceFactory not initialized. Call initialize() first.")
        return self._services['scraping']
    
    def get_health_service(self) -> HealthService:
        """Get health service instance."""
        if not self._initialized:
            raise RuntimeError("ServiceFactory not initialized. Call initialize() first.")
        return self._services['health']
    
    def get_analytics_service(self) -> AnalyticsService:
        """Get analytics service instance."""
        if not self._initialized:
            raise RuntimeError("ServiceFactory not initialized. Call initialize() first.")
        return self._services['analytics']
    
    def get_metrics_service(self) -> MetricsService:
        """Get metrics service instance."""
        if not self._initialized:
            raise RuntimeError("ServiceFactory not initialized. Call initialize() first.")
        return self._services['metrics']
    
    def get_job_service(self) -> JobService:
        """Get job service instance."""
        if not self._initialized:
            raise RuntimeError("ServiceFactory not initialized. Call initialize() first.")
        return self._services['job']
    
    def get_cache_service(self) -> CacheService:
        """Get cache service instance."""
        if not self._initialized:
            raise RuntimeError("ServiceFactory not initialized. Call initialize() first.")
        return self._services['cache']
    
    async def shutdown(self):
        """Gracefully shutdown all services."""
        shutdown_tasks = []
        
        for service_name, service in self._services.items():
            if hasattr(service, 'shutdown'):
                shutdown_tasks.append(service.shutdown())
        
        if shutdown_tasks:
            await asyncio.gather(*shutdown_tasks, return_exceptions=True)
        
        self._services.clear()
        self._initialized = False
    
    def get_service_status(self) -> Dict[str, Any]:
        """Get status of all services."""
        return {
            "initialized": self._initialized,
            "services": {
                name: {
                    "type": type(service).__name__,
                    "status": "active" if hasattr(service, 'is_healthy') and service.is_healthy() else "unknown"
                }
                for name, service in self._services.items()
            }
        }


# Global factory instance
_factory: Optional[ServiceFactory] = None
_factory_lock = asyncio.Lock()


async def get_service_factory() -> ServiceFactory:
    """Get the global service factory instance."""
    global _factory
    
    async with _factory_lock:
        if _factory is None:
            _factory = ServiceFactory()
            await _factory.initialize()
    
    return _factory


async def shutdown_service_factory():
    """Shutdown the global service factory."""
    global _factory
    
    async with _factory_lock:
        if _factory is not None:
            await _factory.shutdown()
            _factory = None 