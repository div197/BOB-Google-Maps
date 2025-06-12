"""bob_api.routers.metrics

Performance metrics endpoints for BOB Google Maps API v0.6.0
Real-time monitoring and analytics with divine insights.

Made with 🙏 following Niṣkāma Karma Yoga principles
"""

import time
import psutil
from typing import Optional

from fastapi import APIRouter, Depends

from bob_core.performance_monitoring import get_global_performance_monitor
from ..models import MetricsResponse
from ..auth import verify_api_key
from ..middleware import get_metrics_middleware

router = APIRouter()


@router.get("/metrics", response_model=MetricsResponse)
async def get_metrics(api_key: Optional[str] = Depends(verify_api_key)):
    """
    📊 Get comprehensive performance metrics
    
    Returns detailed performance, usage, and system metrics.
    """
    performance_monitor = get_global_performance_monitor()
    metrics_middleware = get_metrics_middleware()
    
    # Get performance metrics
    perf_metrics = performance_monitor.get_metrics()
    
    # Get middleware metrics
    middleware_metrics = metrics_middleware.get_metrics()
    
    # System metrics
    system_metrics = {
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent,
        "network_io": dict(psutil.net_io_counters()._asdict()) if psutil.net_io_counters() else {},
        "process_count": len(psutil.pids())
    }
    
    # Usage statistics
    usage_stats = {
        "total_requests": middleware_metrics.get("total_requests", 0),
        "total_errors": middleware_metrics.get("total_errors", 0),
        "uptime_seconds": middleware_metrics.get("uptime_seconds", 0),
        "requests_per_minute": _calculate_rpm(middleware_metrics),
        "success_rate": _calculate_success_rate(middleware_metrics)
    }
    
    # Error statistics
    error_stats = {
        "total_errors": middleware_metrics.get("total_errors", 0),
        "error_rate": _calculate_error_rate(middleware_metrics),
        "common_errors": _get_common_errors(middleware_metrics)
    }
    
    return MetricsResponse(
        performance=perf_metrics,
        usage=usage_stats,
        errors=error_stats,
        system=system_metrics
    )


@router.get("/metrics/performance")
async def get_performance_metrics(api_key: Optional[str] = Depends(verify_api_key)):
    """
    ⚡ Get performance-specific metrics
    
    Returns response times, throughput, and performance indicators.
    """
    performance_monitor = get_global_performance_monitor()
    metrics_middleware = get_metrics_middleware()
    
    perf_data = performance_monitor.get_metrics()
    middleware_data = metrics_middleware.get_metrics()
    
    # Calculate performance indicators
    endpoints = middleware_data.get("endpoints", {})
    
    performance_summary = {
        "overall": {
            "avg_response_time": _calculate_avg_response_time(endpoints),
            "requests_per_second": _calculate_rps(middleware_data),
            "p95_response_time": _calculate_percentile(endpoints, 95),
            "p99_response_time": _calculate_percentile(endpoints, 99)
        },
        "endpoints": {}
    }
    
    # Per-endpoint performance
    for endpoint, data in endpoints.items():
        if endpoint != "total":
            performance_summary["endpoints"][endpoint] = {
                "avg_response_time": data.get("avg_response_time", 0),
                "min_response_time": data.get("min_response_time", 0),
                "max_response_time": data.get("max_response_time", 0),
                "request_count": data.get("request_count", 0),
                "error_count": data.get("error_count", 0),
                "success_rate": _calculate_endpoint_success_rate(data)
            }
    
    return performance_summary


@router.get("/metrics/system")
async def get_system_metrics(api_key: Optional[str] = Depends(verify_api_key)):
    """
    🖥️ Get system resource metrics
    
    Returns CPU, memory, disk, and network usage.
    """
    # CPU metrics
    cpu_metrics = {
        "usage_percent": psutil.cpu_percent(interval=1),
        "count": psutil.cpu_count(),
        "load_average": psutil.getloadavg() if hasattr(psutil, 'getloadavg') else None
    }
    
    # Memory metrics
    memory = psutil.virtual_memory()
    memory_metrics = {
        "total": memory.total,
        "available": memory.available,
        "used": memory.used,
        "usage_percent": memory.percent
    }
    
    # Disk metrics
    disk = psutil.disk_usage('/')
    disk_metrics = {
        "total": disk.total,
        "used": disk.used,
        "free": disk.free,
        "usage_percent": (disk.used / disk.total) * 100
    }
    
    # Network metrics
    network = psutil.net_io_counters()
    network_metrics = {
        "bytes_sent": network.bytes_sent,
        "bytes_recv": network.bytes_recv,
        "packets_sent": network.packets_sent,
        "packets_recv": network.packets_recv
    } if network else {}
    
    return {
        "cpu": cpu_metrics,
        "memory": memory_metrics,
        "disk": disk_metrics,
        "network": network_metrics,
        "timestamp": time.time()
    }


@router.get("/metrics/scraping")
async def get_scraping_metrics(api_key: Optional[str] = Depends(verify_api_key)):
    """
    🔍 Get scraping-specific metrics
    
    Returns scraping performance, success rates, and backend usage.
    """
    performance_monitor = get_global_performance_monitor()
    metrics = performance_monitor.get_metrics()
    
    # Extract scraping-specific metrics
    scraping_metrics = {
        "total_scrapes": 0,
        "successful_scrapes": 0,
        "failed_scrapes": 0,
        "avg_scrape_time": 0,
        "backend_usage": {
            "selenium": 0,
            "playwright": 0
        },
        "extraction_modes": {
            "business_only": 0,
            "full_extraction": 0
        }
    }
    
    # TODO: Implement detailed scraping metrics collection
    # This would require integration with the scraping components
    
    return scraping_metrics


# Helper functions
def _calculate_rpm(metrics: dict) -> float:
    """Calculate requests per minute."""
    total_requests = metrics.get("total_requests", 0)
    uptime_seconds = metrics.get("uptime_seconds", 1)
    uptime_minutes = uptime_seconds / 60
    return total_requests / uptime_minutes if uptime_minutes > 0 else 0


def _calculate_rps(metrics: dict) -> float:
    """Calculate requests per second."""
    total_requests = metrics.get("total_requests", 0)
    uptime_seconds = metrics.get("uptime_seconds", 1)
    return total_requests / uptime_seconds if uptime_seconds > 0 else 0


def _calculate_success_rate(metrics: dict) -> float:
    """Calculate overall success rate."""
    total_requests = metrics.get("total_requests", 0)
    total_errors = metrics.get("total_errors", 0)
    if total_requests == 0:
        return 1.0
    return (total_requests - total_errors) / total_requests


def _calculate_error_rate(metrics: dict) -> float:
    """Calculate error rate."""
    total_requests = metrics.get("total_requests", 0)
    total_errors = metrics.get("total_errors", 0)
    if total_requests == 0:
        return 0.0
    return total_errors / total_requests


def _calculate_avg_response_time(endpoints: dict) -> float:
    """Calculate average response time across all endpoints."""
    total_time = 0
    total_requests = 0
    
    for endpoint, data in endpoints.items():
        if endpoint != "total" and "avg_response_time" in data:
            requests = data.get("request_count", 0)
            avg_time = data.get("avg_response_time", 0)
            total_time += avg_time * requests
            total_requests += requests
    
    return total_time / total_requests if total_requests > 0 else 0


def _calculate_percentile(endpoints: dict, percentile: int) -> float:
    """Calculate response time percentile (simplified)."""
    # This is a simplified implementation
    # In production, you'd want to maintain actual response time distributions
    times = []
    for endpoint, data in endpoints.items():
        if endpoint != "total" and "max_response_time" in data:
            times.append(data.get("max_response_time", 0))
    
    if not times:
        return 0
    
    times.sort()
    index = int((percentile / 100) * len(times))
    return times[min(index, len(times) - 1)]


def _calculate_endpoint_success_rate(data: dict) -> float:
    """Calculate success rate for a specific endpoint."""
    requests = data.get("request_count", 0)
    errors = data.get("error_count", 0)
    if requests == 0:
        return 1.0
    return (requests - errors) / requests


def _get_common_errors(metrics: dict) -> list:
    """Get list of common errors."""
    # TODO: Implement error categorization and tracking
    return [
        {"type": "timeout", "count": 0},
        {"type": "parsing_error", "count": 0},
        {"type": "network_error", "count": 0}
    ] 