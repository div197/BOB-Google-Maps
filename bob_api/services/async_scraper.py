"""bob_api.services.async_scraper

Async Scraping Service for BOB Google Maps API v0.6.0
Divine scraping implementation following Niṣkāma Karma Yoga principles.

Made with 🙏 for interconnected excellence
"""

import asyncio
import time
from typing import Dict, Any, List, Optional
from urllib.parse import urlparse

from .interfaces import ScrapingService, HealthService, MetricsService, CacheService, AnalyticsService
from bob_core import GoogleMapsScraper, batch_scrape
from bob_core.url_validator import is_valid_google_maps_url


class AsyncScrapingService(ScrapingService):
    """Divine async scraping service implementation."""
    
    def __init__(
        self,
        health_service: Optional[HealthService] = None,
        metrics_service: Optional[MetricsService] = None,
        cache_service: Optional[CacheService] = None,
        analytics_service: Optional[AnalyticsService] = None
    ):
        self.health_service = health_service
        self.metrics_service = metrics_service
        self.cache_service = cache_service
        self.analytics_service = analytics_service
        self._scraper = None
        self._initialized = False
    
    async def initialize(self):
        """Initialize the scraping service."""
        if self._initialized:
            return
        
        # Initialize the core scraper
        self._scraper = GoogleMapsScraper()
        self._initialized = True
    
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
        start_time = time.time()
        
        try:
            # Validate URL
            if not is_valid_google_maps_url(url):
                raise ValueError(f"Invalid Google Maps URL: {url}")
            
            # Check cache first
            cache_key = f"scrape:{hash(url)}:{extract_reviews}:{max_reviews}:{backend}"
            if self.cache_service:
                cached_result = await self.cache_service.get(cache_key)
                if cached_result:
                    await self._record_metrics("cache_hit", time.time() - start_time, 200)
                    return cached_result
            
            # Perform scraping
            result = await asyncio.to_thread(
                self._scraper.scrape,
                url=url,
                extract_reviews=extract_reviews,
                max_reviews=max_reviews,
                backend=backend,
                timeout=timeout,
                **kwargs
            )
            
            # Enhance result with analytics
            if self.analytics_service and result.get('business'):
                analytics_result = await self.analytics_service.analyze_business(result['business'])
                result['analytics'] = analytics_result
            
            # Cache the result
            if self.cache_service and result.get('success'):
                await self.cache_service.set(cache_key, result, ttl=3600)  # 1 hour cache
            
            # Record metrics
            response_time = time.time() - start_time
            await self._record_metrics("scrape_single", response_time, 200 if result.get('success') else 500)
            
            return result
            
        except Exception as e:
            response_time = time.time() - start_time
            await self._record_metrics("scrape_single", response_time, 500)
            
            return {
                "success": False,
                "error": str(e),
                "url": url,
                "timestamp": time.time(),
                "response_time": response_time
            }
    
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
        start_time = time.time()
        
        try:
            # Validate all URLs
            invalid_urls = [url for url in urls if not is_valid_google_maps_url(url)]
            if invalid_urls:
                raise ValueError(f"Invalid Google Maps URLs: {invalid_urls}")
            
            # Check cache for each URL
            cached_results = {}
            urls_to_scrape = []
            
            if self.cache_service:
                for url in urls:
                    cache_key = f"scrape:{hash(url)}:{extract_reviews}:{max_reviews}:{backend}"
                    cached_result = await self.cache_service.get(cache_key)
                    if cached_result:
                        cached_results[url] = cached_result
                    else:
                        urls_to_scrape.append(url)
            else:
                urls_to_scrape = urls
            
            # Perform batch scraping for non-cached URLs
            scraped_results = []
            if urls_to_scrape:
                scraped_results = await asyncio.to_thread(
                    batch_scrape,
                    urls=urls_to_scrape,
                    extract_reviews=extract_reviews,
                    max_reviews=max_reviews,
                    backend=backend,
                    max_workers=max_workers,
                    timeout=timeout,
                    **kwargs
                )
            
            # Combine cached and scraped results
            all_results = []
            scraped_dict = {result.get('url'): result for result in scraped_results}
            
            for url in urls:
                if url in cached_results:
                    all_results.append(cached_results[url])
                elif url in scraped_dict:
                    result = scraped_dict[url]
                    
                    # Enhance with analytics
                    if self.analytics_service and result.get('business'):
                        analytics_result = await self.analytics_service.analyze_business(result['business'])
                        result['analytics'] = analytics_result
                    
                    # Cache the result
                    if self.cache_service and result.get('success'):
                        cache_key = f"scrape:{hash(url)}:{extract_reviews}:{max_reviews}:{backend}"
                        await self.cache_service.set(cache_key, result, ttl=3600)
                    
                    all_results.append(result)
                else:
                    # URL not found in results
                    all_results.append({
                        "success": False,
                        "error": "URL not processed",
                        "url": url,
                        "timestamp": time.time()
                    })
            
            # Generate market insights if analytics service is available
            if self.analytics_service:
                successful_businesses = [
                    result['business'] for result in all_results 
                    if result.get('success') and result.get('business')
                ]
                if successful_businesses:
                    market_insights = await self.analytics_service.generate_market_insights(successful_businesses)
                    # Add market insights to the first successful result
                    for result in all_results:
                        if result.get('success'):
                            result['market_insights'] = market_insights
                            break
            
            # Record metrics
            response_time = time.time() - start_time
            success_count = sum(1 for result in all_results if result.get('success'))
            await self._record_metrics("batch_scrape", response_time, 200, {
                "total_urls": len(urls),
                "successful": success_count,
                "cached": len(cached_results),
                "scraped": len(urls_to_scrape)
            })
            
            return all_results
            
        except Exception as e:
            response_time = time.time() - start_time
            await self._record_metrics("batch_scrape", response_time, 500)
            
            return [{
                "success": False,
                "error": str(e),
                "url": url,
                "timestamp": time.time(),
                "response_time": response_time
            } for url in urls]
    
    async def scrape_business_only(self, url: str, **kwargs) -> Dict[str, Any]:
        """Ultra-fast business-only extraction."""
        return await self.scrape_url(
            url=url,
            extract_reviews=False,
            max_reviews=0,
            **kwargs
        )
    
    async def validate_url(self, url: str) -> Dict[str, Any]:
        """Validate Google Maps URL."""
        try:
            is_valid = is_valid_google_maps_url(url)
            parsed = urlparse(url)
            
            return {
                "valid": is_valid,
                "url": url,
                "domain": parsed.netloc,
                "path": parsed.path,
                "query": parsed.query,
                "timestamp": time.time()
            }
        except Exception as e:
            return {
                "valid": False,
                "url": url,
                "error": str(e),
                "timestamp": time.time()
            }
    
    async def get_available_backends(self) -> Dict[str, Any]:
        """Get available scraping backends."""
        try:
            # Check which backends are available
            backends = {
                "selenium": True,  # Always available
                "playwright": False,  # Check if installed
                "auto": True  # Always available
            }
            
            try:
                import playwright
                backends["playwright"] = True
            except ImportError:
                pass
            
            return {
                "backends": backends,
                "default": "auto",
                "recommended": "playwright" if backends["playwright"] else "selenium",
                "timestamp": time.time()
            }
        except Exception as e:
            return {
                "backends": {"auto": True},
                "error": str(e),
                "timestamp": time.time()
            }
    
    async def _record_metrics(
        self, 
        operation: str, 
        response_time: float, 
        status_code: int,
        extra_data: Optional[Dict[str, Any]] = None
    ):
        """Record metrics for the operation."""
        if self.metrics_service:
            try:
                await self.metrics_service.record_request_metric(
                    endpoint=f"scraping.{operation}",
                    response_time=response_time,
                    status_code=status_code
                )
            except Exception:
                # Don't let metrics recording fail the main operation
                pass
    
    def is_healthy(self) -> bool:
        """Check if the service is healthy."""
        return self._initialized and self._scraper is not None
    
    async def shutdown(self):
        """Shutdown the service gracefully."""
        if self._scraper and hasattr(self._scraper, 'cleanup'):
            try:
                await asyncio.to_thread(self._scraper.cleanup)
            except Exception:
                pass
        
        self._initialized = False
        self._scraper = None 