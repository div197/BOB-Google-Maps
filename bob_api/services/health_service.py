"""bob_api.services.health_service

Health Service for BOB Google Maps API v0.6.0
Divine health monitoring following Niṣkāma Karma Yoga principles.

Made with 🙏 for interconnected excellence
"""

import asyncio
import time
import psutil
from typing import Dict, Any, Optional

from .interfaces import HealthService, MetricsService, CacheService
from bob_core import get_global_health_monitor


class HealthServiceImpl(HealthService):
    """Divine health service implementation."""
    
    def __init__(
        self,
        metrics_service: Optional[MetricsService] = None,
        cache_service: Optional[CacheService] = None
    ):
        self.metrics_service = metrics_service
        self.cache_service = cache_service
        self._health_monitor = None
        self._initialized = False
        self._startup_time = time.time()
    
    async def initialize(self):
        """Initialize the health service."""
        if self._initialized:
            return
        
        # Get the global health monitor from BOB Core
        self._health_monitor = get_global_health_monitor()
        self._initialized = True
    
    async def get_health_status(self) -> Dict[str, Any]:
        """Get comprehensive health status."""
        try:
            # Get core health status
            core_health = self._health_monitor.get_health_status() if self._health_monitor else {}
            
            # Get system metrics
            system_metrics = await self._get_system_metrics()
            
            # Get service health
            service_health = await self._get_service_health()
            
            # Calculate overall health
            overall_healthy = (
                core_health.get('healthy', False) and
                system_metrics.get('healthy', False) and
                service_health.get('healthy', False)
            )
            
            return {
                "healthy": overall_healthy,
                "timestamp": time.time(),
                "uptime": time.time() - self._startup_time,
                "core": core_health,
                "system": system_metrics,
                "services": service_health,
                "version": "0.6.0",
                "environment": "production"
            }
            
        except Exception as e:
            return {
                "healthy": False,
                "error": str(e),
                "timestamp": time.time(),
                "uptime": time.time() - self._startup_time
            }
    
    async def get_simple_health(self) -> Dict[str, Any]:
        """Get simple health check."""
        try:
            is_healthy = self._health_monitor.is_healthy() if self._health_monitor else True
            
            return {
                "status": "healthy" if is_healthy else "unhealthy",
                "timestamp": time.time(),
                "uptime": time.time() - self._startup_time
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": time.time()
            }
    
    async def get_readiness_status(self) -> Dict[str, Any]:
        """Get readiness status for Kubernetes."""
        try:
            # Check if all critical services are ready
            ready = (
                self._initialized and
                (self._health_monitor is not None) and
                (self.cache_service is None or await self._check_cache_ready()) and
                (self.metrics_service is None or await self._check_metrics_ready())
            )
            
            return {
                "ready": ready,
                "timestamp": time.time(),
                "checks": {
                    "initialized": self._initialized,
                    "health_monitor": self._health_monitor is not None,
                    "cache_service": await self._check_cache_ready() if self.cache_service else True,
                    "metrics_service": await self._check_metrics_ready() if self.metrics_service else True
                }
            }
            
        except Exception as e:
            return {
                "ready": False,
                "error": str(e),
                "timestamp": time.time()
            }
    
    async def get_liveness_status(self) -> Dict[str, Any]:
        """Get liveness status for Kubernetes."""
        try:
            # Basic liveness check - service is running
            alive = self._initialized and (time.time() - self._startup_time) > 0
            
            return {
                "alive": alive,
                "timestamp": time.time(),
                "uptime": time.time() - self._startup_time,
                "pid": psutil.Process().pid
            }
            
        except Exception as e:
            return {
                "alive": False,
                "error": str(e),
                "timestamp": time.time()
            }
    
    async def reset_health_monitors(self) -> Dict[str, Any]:
        """Reset all health monitors."""
        try:
            if self._health_monitor and hasattr(self._health_monitor, 'reset'):
                self._health_monitor.reset()
            
            return {
                "success": True,
                "message": "Health monitors reset successfully",
                "timestamp": time.time()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": time.time()
            }
    
    async def _get_system_metrics(self) -> Dict[str, Any]:
        """Get system resource metrics."""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            
            # Disk usage
            disk = psutil.disk_usage('/')
            
            # Network stats
            network = psutil.net_io_counters()
            
            # Process info
            process = psutil.Process()
            
            healthy = (
                cpu_percent < 90 and
                memory.percent < 90 and
                disk.percent < 90
            )
            
            return {
                "healthy": healthy,
                "cpu": {
                    "percent": cpu_percent,
                    "count": psutil.cpu_count()
                },
                "memory": {
                    "total": memory.total,
                    "available": memory.available,
                    "percent": memory.percent,
                    "used": memory.used
                },
                "disk": {
                    "total": disk.total,
                    "used": disk.used,
                    "free": disk.free,
                    "percent": disk.percent
                },
                "network": {
                    "bytes_sent": network.bytes_sent,
                    "bytes_recv": network.bytes_recv,
                    "packets_sent": network.packets_sent,
                    "packets_recv": network.packets_recv
                },
                "process": {
                    "pid": process.pid,
                    "memory_percent": process.memory_percent(),
                    "cpu_percent": process.cpu_percent(),
                    "num_threads": process.num_threads(),
                    "create_time": process.create_time()
                }
            }
            
        except Exception as e:
            return {
                "healthy": False,
                "error": str(e)
            }
    
    async def _get_service_health(self) -> Dict[str, Any]:
        """Get health status of dependent services."""
        try:
            services = {}
            
            # Check cache service
            if self.cache_service:
                try:
                    cache_stats = await self.cache_service.get_cache_stats()
                    services["cache"] = {
                        "healthy": True,
                        "stats": cache_stats
                    }
                except Exception as e:
                    services["cache"] = {
                        "healthy": False,
                        "error": str(e)
                    }
            
            # Check metrics service
            if self.metrics_service:
                try:
                    metrics_stats = await self.metrics_service.get_system_metrics()
                    services["metrics"] = {
                        "healthy": True,
                        "stats": metrics_stats
                    }
                except Exception as e:
                    services["metrics"] = {
                        "healthy": False,
                        "error": str(e)
                    }
            
            # Overall service health
            all_healthy = all(
                service.get("healthy", False) 
                for service in services.values()
            )
            
            return {
                "healthy": all_healthy,
                "services": services
            }
            
        except Exception as e:
            return {
                "healthy": False,
                "error": str(e)
            }
    
    async def _check_cache_ready(self) -> bool:
        """Check if cache service is ready."""
        if not self.cache_service:
            return True
        
        try:
            # Try a simple cache operation
            await self.cache_service.set("health_check", "ok", ttl=1)
            result = await self.cache_service.get("health_check")
            await self.cache_service.delete("health_check")
            return result == "ok"
        except Exception:
            return False
    
    async def _check_metrics_ready(self) -> bool:
        """Check if metrics service is ready."""
        if not self.metrics_service:
            return True
        
        try:
            # Try to get metrics
            await self.metrics_service.get_system_metrics()
            return True
        except Exception:
            return False
    
    def is_healthy(self) -> bool:
        """Check if the service is healthy."""
        return self._initialized and self._health_monitor is not None
    
    async def shutdown(self):
        """Shutdown the service gracefully."""
        self._initialized = False
        self._health_monitor = None 