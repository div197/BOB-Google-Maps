"""bob_api.main

Main FastAPI application for BOB Google Maps v0.6.0
Enterprise-grade REST API with divine fault tolerance and monitoring.

Made with 🙏 following Niṣkāma Karma Yoga principles
"""

import time
import logging
from contextlib import asynccontextmanager
from typing import Dict, Any, List, Optional

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
import uvicorn

# BOB Core imports
import bob_core
from bob_core.scraper import GoogleMapsScraper
from bob_core.batch import batch_scrape
from bob_core.health_check import get_global_health_monitor
from bob_core.performance_monitoring import get_global_performance_monitor
from bob_core.circuit_breaker import get_circuit_breaker
from bob_core.graceful_degradation import get_global_degradation_manager

# API models and routers
from .models import (
    ScrapeRequest, ScrapeResponse, BatchScrapeRequest, BatchScrapeResponse,
    HealthResponse, MetricsResponse, ErrorResponse
)
from .routers import (
    scraper, batch, health, metrics, admin, zeroth_law, thermodynamics
)
from .middleware import RateLimitMiddleware, LoggingMiddleware, SecurityMiddleware
from .auth import get_current_user, verify_api_key
from .config import get_settings

# Import new divine routers
try:
    from .routers import zeroth_law, thermodynamics
    THERMODYNAMICS_AVAILABLE = True
except ImportError:
    THERMODYNAMICS_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bob_api")

# Global settings
settings = get_settings()

# Initialize divine systems
health_monitor = get_global_health_monitor()
performance_monitor = get_global_performance_monitor()
degradation_manager = get_global_degradation_manager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    # Startup
    logger.info("🕉️ BOB API v0.6.0 - Divine Service Starting...")
    logger.info("🙏 Following Niṣkāma Karma Yoga principles")
    
    # Initialize divine systems
    health_monitor.start_monitoring()
    performance_monitor.start_monitoring()
    
    # Warm up scrapers
    try:
        scraper = GoogleMapsScraper(headless=True)
        logger.info("✅ Scraper systems initialized")
    except Exception as e:
        logger.error(f"❌ Scraper initialization failed: {e}")
    
    logger.info("🚀 BOB API ready to serve humanity!")
    
    yield
    
    # Shutdown
    logger.info("🙏 BOB API gracefully shutting down...")
    health_monitor.stop_monitoring()
    performance_monitor.stop_monitoring()
    logger.info("✅ Divine service completed")


# Create FastAPI app
app = FastAPI(
    title="BOB Google Maps API",
    description="""
    🕉️ **BOB Google Maps v0.6.0** - Enterprise-grade Google Maps scraping API
    
    Built with divine architecture following **Niṣkāma Karma Yoga** principles.
    
    ## Features
    
    * 🚀 **Ultra-fast business-only extraction** (3.18x faster)
    * 📊 **Comprehensive data extraction** with reviews and analytics
    * ⚡ **Batch processing** with parallel execution
    * 🛡️ **Enterprise fault tolerance** with circuit breakers
    * 📈 **Real-time monitoring** and health checks
    * 🔄 **Auto-recovery** and graceful degradation
    * 🐳 **Production-ready** Docker deployment
    * 🌐 **Multi-cloud** deployment support
    
    ## Quick Start
    
    ```python
    import requests
    
    # Business-only extraction (fastest)
    response = requests.post("/api/v1/scrape", json={
        "url": "https://maps.google.com/?q=restaurant+paris&hl=en",
        "extract_reviews": false
    })
    
    # Full extraction with reviews
    response = requests.post("/api/v1/scrape", json={
        "url": "https://maps.google.com/?q=restaurant+paris&hl=en",
        "extract_reviews": true,
        "max_reviews": 50
    })
    ```
    
    Made with 🙏 for the global community
    """,
    version="0.6.0",
    contact={
        "name": "Divyanshu Singh Chouhan",
        "email": "divyanshu@abcsteps.com",
        "url": "https://github.com/div197/BOB-Google-Maps"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    },
    openapi_tags=[
        {
            "name": "scraper",
            "description": "Core scraping operations"
        },
        {
            "name": "batch",
            "description": "Batch processing operations"
        },
        {
            "name": "health",
            "description": "Health monitoring and status"
        },
        {
            "name": "metrics",
            "description": "Performance metrics and analytics"
        },
        {
            "name": "admin",
            "description": "Administrative operations"
        },
        {
            "name": "Zeroth Law",
            "description": "🔱 Thermal equilibrium and system balance"
        },
        {
            "name": "Thermodynamics", 
            "description": "🕉️ Divine thermodynamic laws and optimization"
        }
    ],
    lifespan=lifespan,
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
    openapi_url="/openapi.json" if settings.ENVIRONMENT != "production" else None
)

# Security
security = HTTPBearer(auto_error=False)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

# Add custom middleware
app.add_middleware(SecurityMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimitMiddleware)


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=True,
            message=exc.detail,
            status_code=exc.status_code,
            timestamp=time.time()
        ).dict()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error=True,
            message="Internal server error",
            status_code=500,
            timestamp=time.time()
        ).dict()
    )


# Root endpoint
@app.get("/", include_in_schema=False)
async def root():
    """Root endpoint - redirect to docs."""
    return RedirectResponse(url="/docs")


@app.get("/api", include_in_schema=False)
async def api_root():
    """API root endpoint."""
    return {
        "message": "🕉️ BOB Google Maps API v0.6.0",
        "description": "Enterprise-grade Google Maps scraping service",
        "version": "0.6.0",
        "docs": "/docs",
        "health": "/api/v1/health",
        "philosophy": "Made with 🙏 following Niṣkāma Karma Yoga principles"
    }


# Include all routers
app.include_router(scraper.router)
app.include_router(batch.router)
app.include_router(health.router)
app.include_router(metrics.router)
app.include_router(admin.router)
app.include_router(zeroth_law.router)
app.include_router(thermodynamics.router)


# Custom OpenAPI
def custom_openapi():
    """Custom OpenAPI schema."""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="BOB Google Maps API",
        version="0.6.0",
        description=app.description,
        routes=app.routes,
    )
    
    # Add custom security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        },
        "ApiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key"
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# Development server
if __name__ == "__main__":
    uvicorn.run(
        "bob_api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 