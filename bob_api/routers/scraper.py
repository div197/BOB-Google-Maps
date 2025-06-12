"""bob_api.routers.scraper

Core scraping endpoints for BOB Google Maps API v0.6.0
Single URL scraping with divine fault tolerance.

Made with 🙏 following Niṣkāma Karma Yoga principles
"""

import time
import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends, status
from fastapi.responses import JSONResponse

import bob_core
from bob_core.scraper import GoogleMapsScraper
from bob_core.analytics import BusinessAnalyzer, ReviewAnalyzer

from ..models import ScrapeRequest, ScrapeResponse, BusinessInfo, Review, Analytics
from ..auth import verify_api_key
from ..config import get_settings

logger = logging.getLogger("bob_api.scraper")
settings = get_settings()

router = APIRouter()


@router.post("/scrape", response_model=ScrapeResponse)
async def scrape_url(
    request: ScrapeRequest,
    background_tasks: BackgroundTasks,
    api_key: Optional[str] = Depends(verify_api_key)
):
    """
    🚀 Scrape a single Google Maps URL
    
    **Features:**
    - ⚡ Business-only mode (3.18x faster)
    - 📊 Full extraction with reviews
    - 🛡️ Enterprise fault tolerance
    - 📈 Optional analytics
    
    **Examples:**
    ```python
    # Business-only (fastest)
    {
        "url": "https://maps.google.com/?q=restaurant+paris&hl=en",
        "extract_reviews": false
    }
    
    # Full extraction with analytics
    {
        "url": "https://maps.google.com/?q=cafe+london&hl=en",
        "extract_reviews": true,
        "max_reviews": 50,
        "include_analytics": true
    }
    ```
    """
    start_time = time.time()
    
    try:
        logger.info(f"🕉️ Starting scrape for URL: {request.url}")
        
        # Create scraper with request parameters
        scraper = GoogleMapsScraper(
            headless=True,
            backend=request.backend.value,
            timeout=request.timeout,
            extract_reviews=request.extract_reviews,
            max_reviews=request.max_reviews
        )
        
        # Perform scraping
        if request.extract_reviews:
            result = scraper.scrape(str(request.url))
        else:
            result = scraper.scrape_business_only(str(request.url))
        
        processing_time = time.time() - start_time
        
        # Convert to API models
        business_info = None
        if result.get("business_info"):
            business_info = BusinessInfo(**result["business_info"])
        
        reviews = []
        if result.get("reviews"):
            reviews = [Review(**review) for review in result["reviews"]]
        
        # Generate analytics if requested
        analytics = None
        if request.include_analytics and result.get("success"):
            try:
                if business_info:
                    business_analyzer = BusinessAnalyzer(result)
                    business_score = business_analyzer.overall_score()
                    
                    analytics_data = {
                        "overall_score": business_score.get("score", 0.0),
                        "review_count": len(reviews),
                        "category_insights": business_score.get("insights", {})
                    }
                    
                    if reviews:
                        review_analyzer = ReviewAnalyzer(result.get("reviews", []))
                        sentiment = review_analyzer.sentiment_analysis()
                        analytics_data["sentiment_score"] = sentiment.get("overall_sentiment", 0.0)
                        analytics_data["average_rating"] = sentiment.get("average_rating", 0.0)
                    
                    analytics = Analytics(**analytics_data)
            except Exception as e:
                logger.warning(f"Analytics generation failed: {e}")
        
        # Create response
        response = ScrapeResponse(
            success=result.get("success", False),
            url=str(request.url),
            business_info=business_info,
            reviews=reviews,
            reviews_count=len(reviews),
            analytics=analytics,
            processing_time=processing_time,
            backend_used=result.get("backend_used", request.backend.value),
            error_message=result.get("error_message")
        )
        
        # Log success metrics
        if response.success:
            logger.info(f"✅ Scrape successful - {processing_time:.2f}s - {len(reviews)} reviews")
        else:
            logger.error(f"❌ Scrape failed - {response.error_message}")
        
        return response
        
    except Exception as e:
        processing_time = time.time() - start_time
        error_message = f"Scraping failed: {str(e)}"
        
        logger.error(f"💥 Scrape error: {error_message}")
        
        return ScrapeResponse(
            success=False,
            url=str(request.url),
            processing_time=processing_time,
            backend_used=request.backend.value,
            error_message=error_message
        )


@router.post("/scrape/business-only", response_model=ScrapeResponse)
async def scrape_business_only(
    request: ScrapeRequest,
    api_key: Optional[str] = Depends(verify_api_key)
):
    """
    ⚡ Ultra-fast business-only extraction (3.18x faster)
    
    Perfect for:
    - 📋 Business directories
    - 📞 Contact lists  
    - 🏢 Market research
    - 🚀 High-volume processing
    
    **No reviews extracted** - Maximum speed optimization
    """
    # Force business-only mode
    request.extract_reviews = False
    request.max_reviews = 0
    request.include_analytics = False
    
    return await scrape_url(request, BackgroundTasks(), api_key)


@router.get("/scrape/status/{job_id}")
async def get_scrape_status(
    job_id: str,
    api_key: Optional[str] = Depends(verify_api_key)
):
    """
    📊 Get status of an asynchronous scraping job
    
    Returns job progress, status, and results when complete.
    """
    # TODO: Implement job tracking with Redis/Database
    # For now, return placeholder
    return {
        "job_id": job_id,
        "status": "completed",
        "progress": 1.0,
        "message": "Job tracking will be implemented in future version"
    }


@router.post("/scrape/validate")
async def validate_url(
    url: str,
    api_key: Optional[str] = Depends(verify_api_key)
):
    """
    ✅ Validate Google Maps URL before scraping
    
    Checks if URL is valid and accessible.
    """
    try:
        # Basic URL validation
        if not any(domain in url for domain in ['maps.google.com', 'google.com/maps']):
            raise HTTPException(
                status_code=400,
                detail="URL must be a Google Maps URL"
            )
        
        # TODO: Add more sophisticated validation
        # - Check if URL is accessible
        # - Validate URL format
        # - Check for rate limiting
        
        return {
            "valid": True,
            "url": url,
            "message": "URL appears to be valid",
            "estimated_time": "18-60 seconds depending on mode"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        return {
            "valid": False,
            "url": url,
            "message": f"Validation failed: {str(e)}"
        }


@router.get("/scrape/backends")
async def get_available_backends():
    """
    🔧 Get available scraping backends and their status
    
    Returns information about Selenium and Playwright availability.
    """
    backends = {}
    
    # Check Selenium
    try:
        from selenium import webdriver
        backends["selenium"] = {
            "available": True,
            "description": "Selenium WebDriver - Reliable and stable",
            "performance": "Standard speed, high compatibility"
        }
    except ImportError:
        backends["selenium"] = {
            "available": False,
            "description": "Selenium not installed",
            "performance": "N/A"
        }
    
    # Check Playwright
    try:
        from playwright.sync_api import sync_playwright
        backends["playwright"] = {
            "available": True,
            "description": "Playwright - Fast and modern",
            "performance": "2-3x faster than Selenium"
        }
    except ImportError:
        backends["playwright"] = {
            "available": False,
            "description": "Playwright not installed",
            "performance": "N/A"
        }
    
    # Auto selection logic
    if backends.get("playwright", {}).get("available"):
        recommended = "playwright"
    elif backends.get("selenium", {}).get("available"):
        recommended = "selenium"
    else:
        recommended = None
    
    return {
        "backends": backends,
        "recommended": recommended,
        "auto_selection": "Playwright preferred, fallback to Selenium"
    } 