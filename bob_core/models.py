"""bob_core.models

Pydantic models for structured data validation and serialization.
"""
from __future__ import annotations

from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

try:
    from pydantic import BaseModel, Field, validator
except ImportError:
    # Fallback for environments without pydantic
    BaseModel = dict
    Field = lambda **kwargs: None
    validator = lambda *args, **kwargs: lambda f: f

__all__ = [
    "BusinessInfo",
    "Review", 
    "ScrapeResult",
    "BatchConfig",
    "ErrorLevel"
]


class ErrorLevel(str, Enum):
    """Error severity levels."""
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class BusinessInfo(BaseModel):
    """Business information extracted from Google Maps."""
    
    name: str = Field(default="Unknown", description="Business name")
    rating: str = Field(default="Unrated", description="Rating with stars")
    category: str = Field(default="Unknown", description="Business category")
    address: str = Field(default="Unknown", description="Full address")
    phone: str = Field(default="Unavailable", description="Phone number")
    website: str = Field(default="Unavailable", description="Website URL")
    coordinates: Optional[Dict[str, float]] = Field(default=None, description="Lat/lng")
    
    @validator("rating")
    def validate_rating(cls, v):
        """Ensure rating is reasonable."""
        if v and v != "Unrated":
            # Extract numeric rating if possible
            import re
            match = re.search(r'(\d+\.?\d*)', v)
            if match:
                rating_val = float(match.group(1))
                if not (0 <= rating_val <= 5):
                    return "Invalid rating"
        return v


class Review(BaseModel):
    """Individual review data."""
    
    username: str = Field(default="Anonymous", description="Reviewer username")
    content: str = Field(default="", description="Review text content")
    rating: str = Field(default="Unrated", description="Review rating")
    time: str = Field(default="", description="Review timestamp")
    helpful_count: Optional[int] = Field(default=None, description="Helpful votes")
    
    @validator("content")
    def validate_content_length(cls, v):
        """Ensure content isn't excessively long."""
        if len(v) > 10000:  # 10k char limit
            return v[:10000] + "..."
        return v


class ScrapeResult(BaseModel):
    """Complete scraping result for a single place."""
    
    url: str = Field(..., description="Original Google Maps URL")
    success: bool = Field(default=False, description="Whether scraping succeeded")
    error_code: int = Field(default=0, description="Error code (0 = success)")
    error_message: str = Field(default="", description="Error description")
    business_info: BusinessInfo = Field(default_factory=BusinessInfo)
    reviews: List[Review] = Field(default_factory=list, description="Extracted reviews")
    reviews_count: int = Field(default=0, description="Number of reviews found")
    scraped_at: Optional[datetime] = Field(default_factory=datetime.now)
    scrape_duration: Optional[float] = Field(default=None, description="Seconds taken")
    
    @validator("reviews_count", always=True)
    def sync_reviews_count(cls, v, values):
        """Ensure reviews_count matches actual reviews length."""
        if "reviews" in values:
            return len(values["reviews"])
        return v


class BatchConfig(BaseModel):
    """Configuration for batch scraping operations."""
    
    max_workers: int = Field(default=4, ge=1, le=20, description="Thread pool size")
    max_retries: int = Field(default=3, ge=0, le=10, description="Retry attempts")
    timeout: int = Field(default=300, ge=30, le=1800, description="Timeout per URL")
    headless: bool = Field(default=True, description="Run browser headless")
    show_progress: bool = Field(default=True, description="Show progress bar")
    output_format: str = Field(default="json", regex="^(json|csv|both)$")
    
    @validator("max_workers")
    def validate_workers(cls, v):
        """Reasonable worker limits."""
        if v > 10:
            import warnings
            warnings.warn("High worker count may trigger rate limiting")
        return v 