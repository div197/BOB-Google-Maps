"""bob_api.models

Pydantic models for BOB Google Maps API v0.6.0
Enterprise-grade data validation and serialization.

Made with 🙏 following Niṣkāma Karma Yoga principles
"""

from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, HttpUrl, field_validator
import time

__all__ = [
    "ScrapeRequest", "ScrapeResponse", "BatchScrapeRequest", "BatchScrapeResponse",
    "HealthResponse", "MetricsResponse", "ErrorResponse", "BackendType",
    "BusinessInfo", "Review", "Analytics", "JobStatus", "JobResponse", "APIResponse"
]


class APIResponse(BaseModel):
    """Generic API response model."""
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Response message")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")
    timestamp: float = Field(default_factory=time.time, description="Response timestamp")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "success": True,
                "message": "Operation completed successfully",
                "data": {"result": "example_data"},
                "timestamp": 1703123456.789
            }
        }
    }


class BackendType(str, Enum):
    """Scraping backend types."""
    AUTO = "auto"
    SELENIUM = "selenium"
    PLAYWRIGHT = "playwright"


class JobStatus(str, Enum):
    """Job status types."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class BusinessInfo(BaseModel):
    """Business information model."""
    name: str = Field(..., description="Business name")
    rating: Optional[str] = Field(None, description="Business rating")
    category: Optional[str] = Field(None, description="Business category")
    address: Optional[str] = Field(None, description="Business address")
    phone: Optional[str] = Field(None, description="Phone number")
    website: Optional[str] = Field(None, description="Website URL")
    hours: Optional[Dict[str, str]] = Field(None, description="Operating hours")
    price_range: Optional[str] = Field(None, description="Price range")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Café de Flore",
                "rating": "4.2 stars",
                "category": "Café",
                "address": "172 Boulevard Saint-Germain, 75006 Paris, France",
                "phone": "+33 1 45 48 55 26",
                "website": "https://cafedeflore.fr",
                "hours": {"Monday": "7:30 AM–1:30 AM", "Tuesday": "7:30 AM–1:30 AM"},
                "price_range": "€€"
            }
        }
    }


class Review(BaseModel):
    """Review model."""
    author: str = Field(..., description="Review author name")
    rating: Optional[str] = Field(None, description="Review rating")
    text: Optional[str] = Field(None, description="Review text")
    date: Optional[str] = Field(None, description="Review date")
    helpful_count: Optional[int] = Field(None, description="Helpful votes count")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "author": "John Smith",
                "rating": "5 stars",
                "text": "Amazing coffee and atmosphere! Highly recommended.",
                "date": "2 months ago",
                "helpful_count": 12
            }
        }
    }


class Analytics(BaseModel):
    """Analytics model."""
    overall_score: Optional[float] = Field(None, description="Overall business score")
    sentiment_score: Optional[float] = Field(None, description="Review sentiment score")
    review_count: Optional[int] = Field(None, description="Total review count")
    average_rating: Optional[float] = Field(None, description="Average rating")
    category_insights: Optional[Dict[str, Any]] = Field(None, description="Category insights")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "overall_score": 8.5,
                "sentiment_score": 0.75,
                "review_count": 1247,
                "average_rating": 4.2,
                "category_insights": {"popular_times": "Evening", "busy_level": "High"}
            }
        }
    }


class ScrapeRequest(BaseModel):
    """Request model for single URL scraping."""
    url: HttpUrl = Field(..., description="Google Maps URL to scrape")
    extract_reviews: bool = Field(True, description="Whether to extract reviews")
    max_reviews: Optional[int] = Field(None, ge=0, le=1000, description="Maximum reviews to extract")
    backend: BackendType = Field(BackendType.AUTO, description="Scraping backend to use")
    timeout: Optional[int] = Field(60, ge=10, le=300, description="Timeout in seconds")
    include_analytics: bool = Field(False, description="Include analytics in response")
    
    @field_validator('url')
    @classmethod
    def validate_google_maps_url(cls, v):
        """Validate that URL is a Google Maps URL."""
        url_str = str(v)
        if not any(domain in url_str for domain in ['maps.google.com', 'google.com/maps']):
            raise ValueError('URL must be a Google Maps URL')
        return v
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "url": "https://maps.google.com/?q=restaurant+paris&hl=en",
                "extract_reviews": True,
                "max_reviews": 50,
                "backend": "auto",
                "timeout": 60,
                "include_analytics": True
            }
        }
    }


class ScrapeResponse(BaseModel):
    """Response model for single URL scraping."""
    success: bool = Field(..., description="Whether scraping was successful")
    url: str = Field(..., description="Original URL")
    business_info: Optional[BusinessInfo] = Field(None, description="Business information")
    reviews: Optional[List[Review]] = Field(None, description="Reviews list")
    reviews_count: Optional[int] = Field(None, description="Total reviews extracted")
    analytics: Optional[Analytics] = Field(None, description="Analytics data")
    processing_time: float = Field(..., description="Processing time in seconds")
    backend_used: str = Field(..., description="Backend used for scraping")
    timestamp: float = Field(default_factory=time.time, description="Response timestamp")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "success": True,
                "url": "https://maps.google.com/?q=restaurant+paris&hl=en",
                "business_info": {
                    "name": "Café de Flore",
                    "rating": "4.2 stars",
                    "category": "Café"
                },
                "reviews": [
                    {
                        "author": "John Smith",
                        "rating": "5 stars",
                        "text": "Amazing coffee!"
                    }
                ],
                "reviews_count": 1,
                "processing_time": 18.5,
                "backend_used": "playwright",
                "timestamp": 1703123456.789
            }
        }
    }


class BatchScrapeRequest(BaseModel):
    """Request model for batch scraping."""
    urls: List[HttpUrl] = Field(..., min_length=1, max_length=100, description="List of Google Maps URLs")
    extract_reviews: bool = Field(True, description="Whether to extract reviews")
    max_reviews: Optional[int] = Field(None, ge=0, le=1000, description="Maximum reviews per URL")
    backend: BackendType = Field(BackendType.AUTO, description="Scraping backend to use")
    max_workers: int = Field(4, ge=1, le=10, description="Number of parallel workers")
    timeout: Optional[int] = Field(60, ge=10, le=300, description="Timeout per URL in seconds")
    include_analytics: bool = Field(False, description="Include analytics in responses")
    
    @field_validator('urls')
    @classmethod
    def validate_google_maps_urls(cls, v):
        """Validate that all URLs are Google Maps URLs."""
        for url in v:
            url_str = str(url)
            if not any(domain in url_str for domain in ['maps.google.com', 'google.com/maps']):
                raise ValueError(f'All URLs must be Google Maps URLs: {url_str}')
        return v
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "urls": [
                    "https://maps.google.com/?q=restaurant+paris&hl=en",
                    "https://maps.google.com/?q=cafe+london&hl=en"
                ],
                "extract_reviews": False,
                "max_reviews": 10,
                "backend": "auto",
                "max_workers": 4,
                "timeout": 60,
                "include_analytics": False
            }
        }
    }


class BatchScrapeResponse(BaseModel):
    """Response model for batch scraping."""
    success: bool = Field(..., description="Whether batch operation was successful")
    total_urls: int = Field(..., description="Total URLs processed")
    successful_urls: int = Field(..., description="Successfully processed URLs")
    failed_urls: int = Field(..., description="Failed URLs")
    results: List[ScrapeResponse] = Field(..., description="Individual scraping results")
    total_processing_time: float = Field(..., description="Total processing time in seconds")
    average_time_per_url: float = Field(..., description="Average time per URL")
    backend_used: str = Field(..., description="Backend used for scraping")
    timestamp: float = Field(default_factory=time.time, description="Response timestamp")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "success": True,
                "total_urls": 2,
                "successful_urls": 2,
                "failed_urls": 0,
                "results": [
                    {
                        "success": True,
                        "url": "https://maps.google.com/?q=restaurant+paris&hl=en",
                        "business_info": {"name": "Café de Flore"},
                        "processing_time": 18.5
                    }
                ],
                "total_processing_time": 37.2,
                "average_time_per_url": 18.6,
                "backend_used": "playwright",
                "timestamp": 1703123456.789
            }
        }
    }


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="Overall health status")
    timestamp: float = Field(default_factory=time.time, description="Health check timestamp")
    version: str = Field(..., description="API version")
    uptime: float = Field(..., description="Uptime in seconds")
    checks: Dict[str, Dict[str, Any]] = Field(..., description="Individual health checks")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "healthy",
                "timestamp": 1703123456.789,
                "version": "0.6.0",
                "uptime": 3600.0,
                "checks": {
                    "database": {"status": "healthy", "response_time": 0.05},
                    "scraper": {"status": "healthy", "backend": "playwright"}
                }
            }
        }
    }


class MetricsResponse(BaseModel):
    """Metrics response model."""
    timestamp: float = Field(default_factory=time.time, description="Metrics timestamp")
    performance: Dict[str, Any] = Field(..., description="Performance metrics")
    usage: Dict[str, Any] = Field(..., description="Usage statistics")
    errors: Dict[str, Any] = Field(..., description="Error statistics")
    system: Dict[str, Any] = Field(..., description="System metrics")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "timestamp": 1703123456.789,
                "performance": {
                    "average_response_time": 18.5,
                    "requests_per_minute": 12.3,
                    "success_rate": 0.95
                },
                "usage": {
                    "total_requests": 1247,
                    "business_only_requests": 892,
                    "full_extraction_requests": 355
                },
                "errors": {
                    "total_errors": 23,
                    "timeout_errors": 12,
                    "parsing_errors": 11
                },
                "system": {
                    "cpu_usage": 45.2,
                    "memory_usage": 67.8,
                    "disk_usage": 23.1
                }
            }
        }
    }


class ErrorResponse(BaseModel):
    """Error response model."""
    error: bool = Field(True, description="Error flag")
    message: str = Field(..., description="Error message")
    status_code: int = Field(..., description="HTTP status code")
    timestamp: float = Field(default_factory=time.time, description="Error timestamp")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "error": True,
                "message": "Invalid Google Maps URL provided",
                "status_code": 400,
                "timestamp": 1703123456.789,
                "details": {
                    "field": "url",
                    "provided_value": "https://example.com"
                }
            }
        }
    }


class JobResponse(BaseModel):
    """Async job response model."""
    job_id: str = Field(..., description="Unique job identifier")
    status: JobStatus = Field(..., description="Job status")
    created_at: float = Field(default_factory=time.time, description="Job creation timestamp")
    started_at: Optional[float] = Field(None, description="Job start timestamp")
    completed_at: Optional[float] = Field(None, description="Job completion timestamp")
    progress: float = Field(0.0, ge=0.0, le=1.0, description="Job progress (0.0 to 1.0)")
    result: Optional[Union[ScrapeResponse, BatchScrapeResponse]] = Field(None, description="Job result")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "job_id": "job_123456789",
                "status": "running",
                "created_at": 1703123456.789,
                "started_at": 1703123457.123,
                "progress": 0.65,
                "result": None
            }
        }
    } 