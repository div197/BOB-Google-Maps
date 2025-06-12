"""bob_api.services.interfaces

Service interfaces for BOB Google Maps API v0.6.0
Divine abstractions following Niṣkāma Karma Yoga principles.

Made with 🙏 for interconnected excellence
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, AsyncGenerator
from datetime import datetime

class ScrapingService(ABC):
    """Divine scraping service interface."""
    
    @abstractmethod
    async def scrape_url(
        self, 
        url: str, 
        extract_reviews: bool = True,
        max_reviews: Optional[int] = None,
        backend: str = "auto",
        timeout: int = 60,
        **kwargs
    ) -> Dict[str, Any]:
        """Scrape a single URL with divine precision."""
        pass
    
    @abstractmethod
    async def batch_scrape(
        self, 
        urls: List[str], 
        extract_reviews: bool = True,
        max_reviews: Optional[int] = None,
        backend: str = "auto",
        max_workers: int = 4,
        timeout: int = 60,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Batch scrape multiple URLs with divine efficiency."""
        pass
    
    @abstractmethod
    async def scrape_business_only(self, url: str, **kwargs) -> Dict[str, Any]:
        """Ultra-fast business-only extraction."""
        pass
    
    @abstractmethod
    async def validate_url(self, url: str) -> Dict[str, Any]:
        """Validate Google Maps URL."""
        pass
    
    @abstractmethod
    async def get_available_backends(self) -> Dict[str, Any]:
        """Get available scraping backends."""
        pass


class HealthService(ABC):
    """Divine health monitoring service interface."""
    
    @abstractmethod
    async def get_health_status(self) -> Dict[str, Any]:
        """Get comprehensive health status."""
        pass
    
    @abstractmethod
    async def get_simple_health(self) -> Dict[str, Any]:
        """Get simple health check."""
        pass
    
    @abstractmethod
    async def get_readiness_status(self) -> Dict[str, Any]:
        """Get readiness status for Kubernetes."""
        pass
    
    @abstractmethod
    async def get_liveness_status(self) -> Dict[str, Any]:
        """Get liveness status for Kubernetes."""
        pass
    
    @abstractmethod
    async def reset_health_monitors(self) -> Dict[str, Any]:
        """Reset all health monitors."""
        pass


class AnalyticsService(ABC):
    """Divine analytics service interface."""
    
    @abstractmethod
    async def analyze_business(self, business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze business data with divine insights."""
        pass
    
    @abstractmethod
    async def analyze_reviews(self, reviews: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze reviews with sentiment analysis."""
        pass
    
    @abstractmethod
    async def generate_market_insights(self, businesses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate market insights from multiple businesses."""
        pass
    
    @abstractmethod
    async def calculate_business_score(self, business_data: Dict[str, Any]) -> float:
        """Calculate overall business score."""
        pass


class MetricsService(ABC):
    """Divine metrics service interface."""
    
    @abstractmethod
    async def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics."""
        pass
    
    @abstractmethod
    async def get_system_metrics(self) -> Dict[str, Any]:
        """Get system resource metrics."""
        pass
    
    @abstractmethod
    async def get_scraping_metrics(self) -> Dict[str, Any]:
        """Get scraping-specific metrics."""
        pass
    
    @abstractmethod
    async def get_usage_statistics(self) -> Dict[str, Any]:
        """Get API usage statistics."""
        pass
    
    @abstractmethod
    async def record_request_metric(
        self, 
        endpoint: str, 
        response_time: float, 
        status_code: int,
        user_id: Optional[str] = None
    ) -> None:
        """Record a request metric."""
        pass


class JobService(ABC):
    """Divine job management service interface."""
    
    @abstractmethod
    async def create_job(self, job_type: str, payload: Dict[str, Any]) -> str:
        """Create a new background job."""
        pass
    
    @abstractmethod
    async def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """Get job status and progress."""
        pass
    
    @abstractmethod
    async def cancel_job(self, job_id: str) -> Dict[str, Any]:
        """Cancel a running job."""
        pass
    
    @abstractmethod
    async def get_job_result(self, job_id: str) -> Dict[str, Any]:
        """Get completed job result."""
        pass
    
    @abstractmethod
    async def list_jobs(self, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """List jobs for a user."""
        pass


class CacheService(ABC):
    """Divine caching service interface."""
    
    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        pass
    
    @abstractmethod
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache with optional TTL."""
        pass
    
    @abstractmethod
    async def delete(self, key: str) -> None:
        """Delete key from cache."""
        pass
    
    @abstractmethod
    async def clear_all(self) -> None:
        """Clear all cache entries."""
        pass
    
    @abstractmethod
    async def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        pass 