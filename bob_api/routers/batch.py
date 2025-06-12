"""bob_api.routers.batch

Batch processing endpoints for BOB Google Maps API v0.6.0
High-performance parallel scraping with divine efficiency.

Made with 🙏 following Niṣkāma Karma Yoga principles
"""

import time
import logging
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends

from bob_core.batch import batch_scrape
from ..models import BatchScrapeRequest, BatchScrapeResponse, ScrapeResponse
from ..auth import verify_api_key

logger = logging.getLogger("bob_api.batch")
router = APIRouter()


@router.post("/batch", response_model=BatchScrapeResponse)
async def batch_scrape_urls(
    request: BatchScrapeRequest,
    background_tasks: BackgroundTasks,
    api_key: Optional[str] = Depends(verify_api_key)
):
    """
    ⚡ Batch scrape multiple Google Maps URLs
    
    **Features:**
    - 🚀 Parallel processing (up to 10 workers)
    - 📊 Progress tracking
    - 🛡️ Individual error handling
    - 📈 Comprehensive analytics
    
    **Perfect for:**
    - Business directory creation
    - Market research
    - Competitor analysis
    - Lead generation
    
    **Example:**
    ```python
    {
        "urls": [
            "https://maps.google.com/?q=restaurant+paris&hl=en",
            "https://maps.google.com/?q=cafe+london&hl=en"
        ],
        "extract_reviews": false,
        "max_workers": 4
    }
    ```
    """
    start_time = time.time()
    
    try:
        logger.info(f"🕉️ Starting batch scrape for {len(request.urls)} URLs")
        
        # Convert URLs to strings
        url_strings = [str(url) for url in request.urls]
        
        # Perform batch scraping
        results = batch_scrape(
            url_strings,
            extract_reviews=request.extract_reviews,
            max_reviews=request.max_reviews,
            backend=request.backend.value,
            max_workers=request.max_workers,
            timeout=request.timeout,
            show_progress=False  # Disable console progress for API
        )
        
        total_processing_time = time.time() - start_time
        
        # Convert results to API models
        api_results = []
        successful_count = 0
        failed_count = 0
        
        for result in results:
            # Convert to ScrapeResponse model
            scrape_response = ScrapeResponse(
                success=result.get("success", False),
                url=result.get("url", ""),
                business_info=result.get("business_info"),
                reviews=result.get("reviews", []),
                reviews_count=len(result.get("reviews", [])),
                processing_time=result.get("processing_time", 0.0),
                backend_used=result.get("backend_used", request.backend.value),
                error_message=result.get("error_message")
            )
            
            api_results.append(scrape_response)
            
            if scrape_response.success:
                successful_count += 1
            else:
                failed_count += 1
        
        # Calculate average time per URL
        avg_time = total_processing_time / len(request.urls) if request.urls else 0
        
        # Create batch response
        batch_response = BatchScrapeResponse(
            success=successful_count > 0,
            total_urls=len(request.urls),
            successful_urls=successful_count,
            failed_urls=failed_count,
            results=api_results,
            total_processing_time=total_processing_time,
            average_time_per_url=avg_time,
            backend_used=request.backend.value
        )
        
        # Log results
        logger.info(
            f"✅ Batch scrape completed - "
            f"{successful_count}/{len(request.urls)} successful - "
            f"{total_processing_time:.2f}s total - "
            f"{avg_time:.2f}s avg"
        )
        
        return batch_response
        
    except Exception as e:
        total_processing_time = time.time() - start_time
        error_message = f"Batch scraping failed: {str(e)}"
        
        logger.error(f"💥 Batch scrape error: {error_message}")
        
        return BatchScrapeResponse(
            success=False,
            total_urls=len(request.urls),
            successful_urls=0,
            failed_urls=len(request.urls),
            results=[],
            total_processing_time=total_processing_time,
            average_time_per_url=0.0,
            backend_used=request.backend.value
        )


@router.post("/batch/business-only", response_model=BatchScrapeResponse)
async def batch_scrape_business_only(
    request: BatchScrapeRequest,
    api_key: Optional[str] = Depends(verify_api_key)
):
    """
    🚀 Ultra-fast batch business-only extraction
    
    **3.18x faster than full extraction**
    
    Perfect for:
    - 📋 Business directories
    - 📞 Contact lists
    - 🏢 Market research
    - ⚡ High-volume processing
    
    **No reviews extracted** - Maximum speed optimization
    """
    # Force business-only mode
    request.extract_reviews = False
    request.max_reviews = 0
    request.include_analytics = False
    
    return await batch_scrape_urls(request, BackgroundTasks(), api_key)


@router.get("/batch/limits")
async def get_batch_limits():
    """
    📊 Get batch processing limits and recommendations
    
    Returns current limits and performance guidelines.
    """
    return {
        "max_urls_per_batch": 100,
        "max_workers": 10,
        "recommended_workers": 4,
        "timeout_range": {
            "min": 10,
            "max": 300,
            "recommended": 60
        },
        "performance_tips": [
            "Use business-only mode for 3.18x speed improvement",
            "Start with 4 workers and adjust based on performance",
            "Consider splitting large batches into smaller chunks",
            "Monitor rate limits to avoid blocking"
        ],
        "estimated_times": {
            "business_only": "15-25 seconds per URL",
            "with_reviews": "45-90 seconds per URL",
            "parallel_speedup": "Near-linear with worker count"
        }
    } 