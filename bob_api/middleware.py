"""bob_api.middleware

Middleware components for BOB Google Maps API v0.6.0
Rate limiting, logging, and security with divine protection.

Made with 🙏 following Niṣkāma Karma Yoga principles
"""

import time
import logging
from typing import Dict, Any
from collections import defaultdict, deque
from datetime import datetime, timedelta

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from .config import get_settings

settings = get_settings()
logger = logging.getLogger("bob_api.middleware")


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware with sliding window algorithm.
    
    Implements per-IP rate limiting with configurable limits.
    """
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.requests: Dict[str, deque] = defaultdict(deque)
        self.max_requests = settings.RATE_LIMIT_REQUESTS
        self.window_seconds = settings.RATE_LIMIT_WINDOW
    
    async def dispatch(self, request: Request, call_next):
        """Process request with rate limiting."""
        client_ip = self._get_client_ip(request)
        current_time = time.time()
        
        # Clean old requests
        self._clean_old_requests(client_ip, current_time)
        
        # Check rate limit
        if len(self.requests[client_ip]) >= self.max_requests:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            return JSONResponse(
                status_code=429,
                content={
                    "error": True,
                    "message": "Rate limit exceeded",
                    "limit": self.max_requests,
                    "window": self.window_seconds,
                    "retry_after": self.window_seconds
                },
                headers={"Retry-After": str(self.window_seconds)}
            )
        
        # Add current request
        self.requests[client_ip].append(current_time)
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers
        remaining = max(0, self.max_requests - len(self.requests[client_ip]))
        response.headers["X-RateLimit-Limit"] = str(self.max_requests)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(int(current_time + self.window_seconds))
        
        return response
    
    def _get_client_ip(self, request: Request) -> str:
        """Get client IP address from request."""
        # Check for forwarded headers (behind proxy)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # Fallback to direct connection
        return request.client.host if request.client else "unknown"
    
    def _clean_old_requests(self, client_ip: str, current_time: float):
        """Remove requests outside the time window."""
        cutoff_time = current_time - self.window_seconds
        
        while (self.requests[client_ip] and 
               self.requests[client_ip][0] < cutoff_time):
            self.requests[client_ip].popleft()


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Comprehensive request/response logging middleware.
    
    Logs all API requests with timing and status information.
    """
    
    async def dispatch(self, request: Request, call_next):
        """Process request with logging."""
        start_time = time.time()
        client_ip = self._get_client_ip(request)
        
        # Log request
        logger.info(
            f"🌐 {request.method} {request.url.path} - "
            f"IP: {client_ip} - "
            f"User-Agent: {request.headers.get('User-Agent', 'Unknown')}"
        )
        
        # Process request
        try:
            response = await call_next(request)
            processing_time = time.time() - start_time
            
            # Log response
            logger.info(
                f"✅ {request.method} {request.url.path} - "
                f"Status: {response.status_code} - "
                f"Time: {processing_time:.3f}s - "
                f"IP: {client_ip}"
            )
            
            # Add timing header
            response.headers["X-Process-Time"] = f"{processing_time:.3f}"
            
            return response
            
        except Exception as e:
            processing_time = time.time() - start_time
            
            # Log error
            logger.error(
                f"❌ {request.method} {request.url.path} - "
                f"Error: {str(e)} - "
                f"Time: {processing_time:.3f}s - "
                f"IP: {client_ip}"
            )
            
            # Re-raise exception
            raise
    
    def _get_client_ip(self, request: Request) -> str:
        """Get client IP address from request."""
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        return request.client.host if request.client else "unknown"


class SecurityMiddleware(BaseHTTPMiddleware):
    """
    Security headers and protection middleware.
    
    Adds security headers and basic protection measures.
    """
    
    async def dispatch(self, request: Request, call_next):
        """Process request with security measures."""
        # Process request
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        
        # Add API identification
        response.headers["X-API-Version"] = settings.VERSION
        response.headers["X-Powered-By"] = "BOB Google Maps API"
        
        # HSTS for HTTPS
        if request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        return response


class MetricsMiddleware(BaseHTTPMiddleware):
    """
    Metrics collection middleware.
    
    Collects performance and usage metrics for monitoring.
    """
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.request_count = defaultdict(int)
        self.response_times = defaultdict(list)
        self.error_count = defaultdict(int)
        self.start_time = time.time()
    
    async def dispatch(self, request: Request, call_next):
        """Process request with metrics collection."""
        start_time = time.time()
        endpoint = f"{request.method} {request.url.path}"
        
        # Increment request count
        self.request_count[endpoint] += 1
        self.request_count["total"] += 1
        
        try:
            # Process request
            response = await call_next(request)
            processing_time = time.time() - start_time
            
            # Record response time
            self.response_times[endpoint].append(processing_time)
            self.response_times["total"].append(processing_time)
            
            # Keep only last 1000 response times per endpoint
            if len(self.response_times[endpoint]) > 1000:
                self.response_times[endpoint] = self.response_times[endpoint][-1000:]
            
            return response
            
        except Exception as e:
            # Record error
            self.error_count[endpoint] += 1
            self.error_count["total"] += 1
            
            # Re-raise exception
            raise
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get collected metrics."""
        uptime = time.time() - self.start_time
        
        metrics = {
            "uptime_seconds": uptime,
            "total_requests": self.request_count.get("total", 0),
            "total_errors": self.error_count.get("total", 0),
            "endpoints": {}
        }
        
        # Calculate average response times
        for endpoint, times in self.response_times.items():
            if times:
                metrics["endpoints"][endpoint] = {
                    "request_count": self.request_count.get(endpoint, 0),
                    "error_count": self.error_count.get(endpoint, 0),
                    "avg_response_time": sum(times) / len(times),
                    "min_response_time": min(times),
                    "max_response_time": max(times)
                }
        
        return metrics


# Global metrics instance
metrics_middleware = None


def get_metrics_middleware() -> MetricsMiddleware:
    """Get global metrics middleware instance."""
    global metrics_middleware
    if metrics_middleware is None:
        metrics_middleware = MetricsMiddleware(None)
    return metrics_middleware 