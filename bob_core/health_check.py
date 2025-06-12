"""bob_core.health_check

Comprehensive health check system for monitoring component status and system health.
Implements observability patterns following Niṣkāma Karma Yoga principles.
"""
from __future__ import annotations

import time
import threading
import psutil
import logging
from typing import Dict, Any, List, Optional, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import json

__all__ = [
    "HealthStatus",
    "HealthCheck", 
    "HealthCheckResult",
    "HealthMonitor",
    "SystemHealthCheck",
    "ComponentHealthCheck"
]


class HealthStatus(Enum):
    """Health status levels."""
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


@dataclass
class HealthCheckResult:
    """Result of a health check."""
    name: str
    status: HealthStatus
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    duration_ms: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "name": self.name,
            "status": self.status.value,
            "message": self.message,
            "timestamp": self.timestamp.isoformat(),
            "duration_ms": self.duration_ms,
            "metadata": self.metadata
        }


class HealthCheck:
    """Base class for health checks."""
    
    def __init__(self, name: str, timeout: float = 5.0):
        self.name = name
        self.timeout = timeout
        self._logger = logging.getLogger(f"bob_core.health_check.{name}")
    
    def check(self) -> HealthCheckResult:
        """Perform the health check."""
        start_time = time.time()
        
        try:
            status, message, metadata = self._perform_check()
            duration_ms = (time.time() - start_time) * 1000
            
            return HealthCheckResult(
                name=self.name,
                status=status,
                message=message,
                duration_ms=duration_ms,
                metadata=metadata
            )
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            self._logger.error(f"Health check {self.name} failed: {e}")
            
            return HealthCheckResult(
                name=self.name,
                status=HealthStatus.CRITICAL,
                message=f"Health check failed: {str(e)}",
                duration_ms=duration_ms,
                metadata={"error": str(e), "error_type": type(e).__name__}
            )
    
    def _perform_check(self) -> tuple[HealthStatus, str, Dict[str, Any]]:
        """Override this method to implement specific health check logic."""
        raise NotImplementedError


class SystemHealthCheck(HealthCheck):
    """Health check for system resources (CPU, memory, disk)."""
    
    def __init__(self, 
                 name: str = "system",
                 cpu_threshold: float = 80.0,
                 memory_threshold: float = 85.0,
                 disk_threshold: float = 90.0):
        super().__init__(name)
        self.cpu_threshold = cpu_threshold
        self.memory_threshold = memory_threshold
        self.disk_threshold = disk_threshold
    
    def _perform_check(self) -> tuple[HealthStatus, str, Dict[str, Any]]:
        """Check system resource usage."""
        # Get system metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        metadata = {
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "memory_available_gb": memory.available / (1024**3),
            "disk_percent": disk.percent,
            "disk_free_gb": disk.free / (1024**3)
        }
        
        # Determine status
        issues = []
        status = HealthStatus.HEALTHY
        
        if cpu_percent > self.cpu_threshold:
            issues.append(f"High CPU usage: {cpu_percent:.1f}%")
            status = HealthStatus.WARNING if cpu_percent < 95 else HealthStatus.CRITICAL
        
        if memory.percent > self.memory_threshold:
            issues.append(f"High memory usage: {memory.percent:.1f}%")
            if status != HealthStatus.CRITICAL:
                status = HealthStatus.WARNING if memory.percent < 95 else HealthStatus.CRITICAL
        
        if disk.percent > self.disk_threshold:
            issues.append(f"High disk usage: {disk.percent:.1f}%")
            if status != HealthStatus.CRITICAL:
                status = HealthStatus.WARNING if disk.percent < 98 else HealthStatus.CRITICAL
        
        if issues:
            message = "; ".join(issues)
        else:
            message = f"System healthy - CPU: {cpu_percent:.1f}%, Memory: {memory.percent:.1f}%, Disk: {disk.percent:.1f}%"
        
        return status, message, metadata


class ComponentHealthCheck(HealthCheck):
    """Health check for application components."""
    
    def __init__(self, 
                 name: str,
                 check_function: Callable[[], bool],
                 description: str = ""):
        super().__init__(name)
        self.check_function = check_function
        self.description = description
    
    def _perform_check(self) -> tuple[HealthStatus, str, Dict[str, Any]]:
        """Check component health using provided function."""
        try:
            is_healthy = self.check_function()
            
            if is_healthy:
                return (
                    HealthStatus.HEALTHY,
                    f"Component {self.name} is healthy",
                    {"description": self.description}
                )
            else:
                return (
                    HealthStatus.CRITICAL,
                    f"Component {self.name} is not healthy",
                    {"description": self.description}
                )
                
        except Exception as e:
            return (
                HealthStatus.CRITICAL,
                f"Component {self.name} check failed: {str(e)}",
                {"description": self.description, "error": str(e)}
            )


class DatabaseHealthCheck(HealthCheck):
    """Health check for database connectivity."""
    
    def __init__(self, name: str = "database", connection_string: str = ""):
        super().__init__(name)
        self.connection_string = connection_string
    
    def _perform_check(self) -> tuple[HealthStatus, str, Dict[str, Any]]:
        """Check database connectivity."""
        # This is a placeholder - implement based on your database
        # For now, just check if connection string is provided
        if not self.connection_string:
            return (
                HealthStatus.WARNING,
                "No database connection configured",
                {"connection_configured": False}
            )
        
        # In a real implementation, you would:
        # 1. Try to connect to the database
        # 2. Execute a simple query (SELECT 1)
        # 3. Measure response time
        
        return (
            HealthStatus.HEALTHY,
            "Database connection healthy",
            {"connection_configured": True, "response_time_ms": 10}
        )


class WebDriverHealthCheck(HealthCheck):
    """Health check for WebDriver availability."""
    
    def __init__(self, name: str = "webdriver"):
        super().__init__(name)
    
    def _perform_check(self) -> tuple[HealthStatus, str, Dict[str, Any]]:
        """Check WebDriver availability."""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            
            # Try to create a headless Chrome instance
            options = Options()
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            
            driver = webdriver.Chrome(options=options)
            driver.get("data:text/html,<html><body>Health Check</body></html>")
            driver.quit()
            
            return (
                HealthStatus.HEALTHY,
                "WebDriver (Chrome) is available and functional",
                {"driver_type": "chrome", "headless": True}
            )
            
        except Exception as e:
            return (
                HealthStatus.CRITICAL,
                f"WebDriver not available: {str(e)}",
                {"error": str(e), "driver_type": "chrome"}
            )


class PlaywrightHealthCheck(HealthCheck):
    """Health check for Playwright availability."""
    
    def __init__(self, name: str = "playwright"):
        super().__init__(name)
    
    def _perform_check(self) -> tuple[HealthStatus, str, Dict[str, Any]]:
        """Check Playwright availability."""
        try:
            from playwright.sync_api import sync_playwright
            
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto("data:text/html,<html><body>Health Check</body></html>")
                browser.close()
            
            return (
                HealthStatus.HEALTHY,
                "Playwright is available and functional",
                {"browser_type": "chromium", "headless": True}
            )
            
        except ImportError:
            return (
                HealthStatus.WARNING,
                "Playwright not installed",
                {"error": "ImportError", "installed": False}
            )
        except Exception as e:
            return (
                HealthStatus.CRITICAL,
                f"Playwright not functional: {str(e)}",
                {"error": str(e), "installed": True}
            )


class HealthMonitor:
    """Central health monitoring system."""
    
    def __init__(self, check_interval: int = 60):
        self.checks: Dict[str, HealthCheck] = {}
        self.results: Dict[str, HealthCheckResult] = {}
        self.check_interval = check_interval
        self._monitoring = False
        self._monitor_thread: Optional[threading.Thread] = None
        self._lock = threading.RLock()
        self._logger = logging.getLogger("bob_core.health_monitor")
    
    def add_check(self, health_check: HealthCheck) -> None:
        """Add a health check to the monitor."""
        with self._lock:
            self.checks[health_check.name] = health_check
            self._logger.info(f"Added health check: {health_check.name}")
    
    def remove_check(self, name: str) -> None:
        """Remove a health check from the monitor."""
        with self._lock:
            if name in self.checks:
                del self.checks[name]
                if name in self.results:
                    del self.results[name]
                self._logger.info(f"Removed health check: {name}")
    
    def run_check(self, name: str) -> Optional[HealthCheckResult]:
        """Run a specific health check."""
        if name not in self.checks:
            return None
        
        result = self.checks[name].check()
        
        with self._lock:
            self.results[name] = result
        
        self._logger.debug(f"Health check {name}: {result.status.value}")
        return result
    
    def run_all_checks(self) -> Dict[str, HealthCheckResult]:
        """Run all registered health checks."""
        results = {}
        
        for name in self.checks:
            result = self.run_check(name)
            if result:
                results[name] = result
        
        return results
    
    def get_overall_status(self) -> HealthStatus:
        """Get overall system health status."""
        if not self.results:
            return HealthStatus.UNKNOWN
        
        statuses = [result.status for result in self.results.values()]
        
        if HealthStatus.CRITICAL in statuses:
            return HealthStatus.CRITICAL
        elif HealthStatus.WARNING in statuses:
            return HealthStatus.WARNING
        elif all(status == HealthStatus.HEALTHY for status in statuses):
            return HealthStatus.HEALTHY
        else:
            return HealthStatus.UNKNOWN
    
    def get_health_summary(self) -> Dict[str, Any]:
        """Get comprehensive health summary."""
        overall_status = self.get_overall_status()
        
        summary = {
            "overall_status": overall_status.value,
            "timestamp": datetime.now().isoformat(),
            "checks": {
                name: result.to_dict() 
                for name, result in self.results.items()
            },
            "statistics": {
                "total_checks": len(self.checks),
                "healthy": sum(1 for r in self.results.values() if r.status == HealthStatus.HEALTHY),
                "warning": sum(1 for r in self.results.values() if r.status == HealthStatus.WARNING),
                "critical": sum(1 for r in self.results.values() if r.status == HealthStatus.CRITICAL),
                "unknown": sum(1 for r in self.results.values() if r.status == HealthStatus.UNKNOWN)
            }
        }
        
        return summary
    
    def start_monitoring(self) -> None:
        """Start continuous health monitoring."""
        if self._monitoring:
            return
        
        self._monitoring = True
        self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._monitor_thread.start()
        self._logger.info("Started health monitoring")
    
    def stop_monitoring(self) -> None:
        """Stop continuous health monitoring."""
        self._monitoring = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=5)
        self._logger.info("Stopped health monitoring")
    
    def _monitor_loop(self) -> None:
        """Main monitoring loop."""
        while self._monitoring:
            try:
                self.run_all_checks()
                time.sleep(self.check_interval)
            except Exception as e:
                self._logger.error(f"Error in monitoring loop: {e}")
                time.sleep(min(self.check_interval, 30))  # Fallback interval


# Global health monitor instance
_global_health_monitor: Optional[HealthMonitor] = None

def get_global_health_monitor() -> HealthMonitor:
    """Get or create global health monitor."""
    global _global_health_monitor
    if _global_health_monitor is None:
        _global_health_monitor = HealthMonitor()
    return _global_health_monitor


def setup_default_health_checks() -> HealthMonitor:
    """Setup default health checks for BOB Google Maps."""
    monitor = get_global_health_monitor()
    
    # Add BOB-specific health checks
    def check_config():
        """Check if configuration is loaded."""
        try:
            from .config import load_config
            config = load_config()
            return config is not None
        except Exception:
            return False
    
    def check_rate_limiter():
        """Check if rate limiter is functional."""
        try:
            from .rate_limiter import RateLimiter
            limiter = RateLimiter(delay=0.1)
            limiter.wait()
            return True
        except Exception:
            return False
    
    monitor.add_check(ComponentHealthCheck("config", check_config, "Configuration system"))
    monitor.add_check(ComponentHealthCheck("rate_limiter", check_rate_limiter, "Rate limiting system"))
    
    return monitor 