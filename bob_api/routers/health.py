"""bob_api.routers.health

Health monitoring endpoints for BOB Google Maps API v0.6.0
Comprehensive system health checks with divine monitoring.

Made with 🙏 following Niṣkāma Karma Yoga principles
"""

import time
import psutil
from typing import Dict, Any

from fastapi import APIRouter
from bob_core.health_check import get_global_health_monitor
from ..models import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    🏥 Comprehensive health check
    
    Returns detailed system health information including:
    - Overall status
    - Individual component health
    - System metrics
    - Uptime information
    """
    health_monitor = get_global_health_monitor()
    
    # Get health status
    health_status = health_monitor.get_health_status()
    
    # System metrics
    system_metrics = {
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent,
        "load_average": psutil.getloadavg() if hasattr(psutil, 'getloadavg') else None
    }
    
    # Combine all checks
    all_checks = {
        "system": {
            "status": "healthy" if system_metrics["cpu_percent"] < 90 else "warning",
            "metrics": system_metrics
        }
    }
    all_checks.update(health_status.get("checks", {}))
    
    return HealthResponse(
        status=health_status.get("status", "unknown"),
        version="0.6.0",
        uptime=time.time() - health_monitor.start_time,
        checks=all_checks
    )


@router.get("/health/simple")
async def simple_health():
    """
    ✅ Simple health check for load balancers
    
    Returns minimal response for basic health monitoring.
    """
    return {"status": "ok", "timestamp": time.time()}


@router.get("/health/ready")
async def readiness_check():
    """
    🚀 Readiness check for Kubernetes
    
    Checks if the service is ready to accept traffic.
    """
    health_monitor = get_global_health_monitor()
    health_status = health_monitor.get_health_status()
    
    if health_status.get("status") in ["healthy", "warning"]:
        return {"ready": True, "status": health_status.get("status")}
    else:
        return {"ready": False, "status": health_status.get("status")}, 503


@router.get("/health/live")
async def liveness_check():
    """
    💓 Liveness check for Kubernetes
    
    Checks if the service is alive and should not be restarted.
    """
    # Basic liveness - if we can respond, we're alive
    return {"alive": True, "timestamp": time.time()} 