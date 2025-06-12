"""bob_api.services.metrics_service

Metrics Service for BOB Google Maps API v0.6.0
Divine metrics implementation following Niṣkāma Karma Yoga principles.

Made with 🙏 for interconnected excellence
"""

import asyncio
import time
import psutil
from typing import Dict, Any, Optional, List
from collections import defaultdict, deque
from datetime import datetime, timedelta

from .interfaces import MetricsService, CacheService
from bob_core import get_global_performance_monitor


class MetricsServiceImpl(MetricsService):
    """Divine metrics service implementation."""
    
    def __init__(self, cache_service: Optional[CacheService] = None):
        self.cache_service = cache_service
        self._performance_monitor = None
        self._initialized = False
        self._startup_time = time.time()
        
        # In-memory metrics storage
        self._request_metrics = deque(maxlen=10000)  # Last 10k requests
        self._system_metrics_history = deque(maxlen=1440)  # 24 hours of minute-by-minute data
        self._endpoint_stats = defaultdict(lambda: {
            'count': 0,
            'total_time': 0,
            'errors': 0,
            'last_request': None
        })
        
        # Background task for system metrics collection
        self._metrics_task = None
    
    async def initialize(self):
        """Initialize the metrics service."""
        if self._initialized:
            return
        
        # Get the global performance monitor from BOB Core
        self._performance_monitor = get_global_performance_monitor()
        
        # Start background metrics collection
        self._metrics_task = asyncio.create_task(self._collect_system_metrics_loop())
        
        self._initialized = True
    
    async def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics."""
        try:
            # Get core performance metrics
            core_metrics = self._performance_monitor.get_metrics() if self._performance_monitor else {}
            
            # Calculate API-specific metrics
            api_metrics = await self._calculate_api_metrics()
            
            # Get recent system metrics
            recent_system = self._system_metrics_history[-1] if self._system_metrics_history else {}
            
            return {
                "timestamp": time.time(),
                "uptime": time.time() - self._startup_time,
                "core": core_metrics,
                "api": api_metrics,
                "system": recent_system,
                "summary": await self._generate_performance_summary(api_metrics, recent_system)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": time.time()
            }
    
    async def get_system_metrics(self) -> Dict[str, Any]:
        """Get system resource metrics."""
        try:
            # Current system metrics
            current_metrics = await self._collect_current_system_metrics()
            
            # Historical data
            historical_data = list(self._system_metrics_history)[-60:]  # Last hour
            
            # Calculate trends
            trends = await self._calculate_system_trends(historical_data)
            
            return {
                "current": current_metrics,
                "historical": historical_data,
                "trends": trends,
                "timestamp": time.time()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": time.time()
            }
    
    async def get_scraping_metrics(self) -> Dict[str, Any]:
        """Get scraping-specific metrics."""
        try:
            # Filter scraping-related requests
            scraping_requests = [
                req for req in self._request_metrics 
                if 'scraping' in req.get('endpoint', '')
            ]
            
            if not scraping_requests:
                return {
                    "total_scrapes": 0,
                    "success_rate": 0,
                    "average_response_time": 0,
                    "scraping_trends": []
                }
            
            # Calculate scraping metrics
            total_scrapes = len(scraping_requests)
            successful_scrapes = sum(1 for req in scraping_requests if req.get('status_code', 0) < 400)
            success_rate = successful_scrapes / total_scrapes if total_scrapes > 0 else 0
            
            response_times = [req.get('response_time', 0) for req in scraping_requests]
            avg_response_time = sum(response_times) / len(response_times) if response_times else 0
            
            return {
                "total_scrapes": total_scrapes,
                "successful_scrapes": successful_scrapes,
                "success_rate": success_rate,
                "average_response_time": avg_response_time,
                "timestamp": time.time()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": time.time()
            }
    
    async def get_usage_statistics(self) -> Dict[str, Any]:
        """Get API usage statistics."""
        try:
            # Endpoint usage
            endpoint_usage = {}
            for endpoint, stats in self._endpoint_stats.items():
                endpoint_usage[endpoint] = {
                    'total_requests': stats['count'],
                    'average_response_time': stats['total_time'] / stats['count'] if stats['count'] > 0 else 0,
                    'error_rate': stats['errors'] / stats['count'] if stats['count'] > 0 else 0,
                    'last_request': stats['last_request']
                }
            
            return {
                "total_requests": len(self._request_metrics),
                "endpoint_usage": endpoint_usage,
                "timestamp": time.time()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": time.time()
            }
    
    async def record_request_metric(
        self, 
        endpoint: str, 
        response_time: float, 
        status_code: int,
        user_id: Optional[str] = None
    ) -> None:
        """Record a request metric."""
        try:
            metric = {
                'endpoint': endpoint,
                'response_time': response_time,
                'status_code': status_code,
                'user_id': user_id,
                'timestamp': time.time()
            }
            
            # Add to request metrics
            self._request_metrics.append(metric)
            
            # Update endpoint stats
            stats = self._endpoint_stats[endpoint]
            stats['count'] += 1
            stats['total_time'] += response_time
            if status_code >= 400:
                stats['errors'] += 1
            stats['last_request'] = time.time()
                
        except Exception:
            # Don't let metrics recording fail the main operation
            pass
    
    async def _collect_system_metrics_loop(self):
        """Background loop to collect system metrics."""
        while self._initialized:
            try:
                metrics = await self._collect_current_system_metrics()
                self._system_metrics_history.append(metrics)
                
                # Sleep for 1 minute
                await asyncio.sleep(60)
                
            except asyncio.CancelledError:
                break
            except Exception:
                # Continue on error
                await asyncio.sleep(60)
    
    async def _collect_current_system_metrics(self) -> Dict[str, Any]:
        """Collect current system metrics."""
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory metrics
            memory = psutil.virtual_memory()
            
            return {
                "timestamp": time.time(),
                "cpu": {
                    "percent": cpu_percent,
                    "count": psutil.cpu_count()
                },
                "memory": {
                    "total": memory.total,
                    "available": memory.available,
                    "percent": memory.percent,
                    "used": memory.used
                }
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "timestamp": time.time()
            }
    
    async def _calculate_api_metrics(self) -> Dict[str, Any]:
        """Calculate API-specific metrics."""
        if not self._request_metrics:
            return {
                "total_requests": 0,
                "average_response_time": 0,
                "error_rate": 0,
                "requests_per_minute": 0
            }
        
        total_requests = len(self._request_metrics)
        response_times = [req.get('response_time', 0) for req in self._request_metrics]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        errors = sum(1 for req in self._request_metrics if req.get('status_code', 0) >= 400)
        error_rate = errors / total_requests if total_requests > 0 else 0
        
        # Calculate requests per minute (last 5 minutes)
        five_minutes_ago = time.time() - 300
        recent_requests = sum(1 for req in self._request_metrics if req.get('timestamp', 0) > five_minutes_ago)
        requests_per_minute = recent_requests / 5
        
        return {
            "total_requests": total_requests,
            "average_response_time": avg_response_time,
            "error_rate": error_rate,
            "requests_per_minute": requests_per_minute
        }
    
    async def _calculate_system_trends(self, historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate system resource trends."""
        if len(historical_data) < 2:
            return {}
        
        # Extract time series data
        cpu_data = [d.get('cpu', {}).get('percent', 0) for d in historical_data]
        memory_data = [d.get('memory', {}).get('percent', 0) for d in historical_data]
        
        return {
            "cpu_average": sum(cpu_data) / len(cpu_data) if cpu_data else 0,
            "memory_average": sum(memory_data) / len(memory_data) if memory_data else 0
        }
    
    async def _generate_performance_summary(self, api_metrics: Dict[str, Any], system_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Generate performance summary."""
        summary = {
            "status": "healthy",
            "issues": [],
            "recommendations": []
        }
        
        # Check API performance
        if api_metrics.get('error_rate', 0) > 0.05:  # 5% error rate
            summary["status"] = "degraded"
            summary["issues"].append("High error rate detected")
            summary["recommendations"].append("Investigate failing requests")
        
        if api_metrics.get('average_response_time', 0) > 10:  # 10 seconds
            summary["status"] = "degraded"
            summary["issues"].append("Slow response times")
            summary["recommendations"].append("Optimize scraping performance")
        
        return summary
    
    def is_healthy(self) -> bool:
        """Check if the service is healthy."""
        return self._initialized and self._performance_monitor is not None
    
    async def shutdown(self):
        """Shutdown the service gracefully."""
        if self._metrics_task:
            self._metrics_task.cancel()
            try:
                await self._metrics_task
            except asyncio.CancelledError:
                pass
        
        self._initialized = False
        self._performance_monitor = None 