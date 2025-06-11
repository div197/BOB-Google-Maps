"""Tests for Pydantic models."""

import pytest
from bob_core.models import BusinessInfo, Review, ScrapeResult, BatchConfig


def test_business_info_validation():
    """Test BusinessInfo model validation."""
    # Valid data
    info = BusinessInfo(
        name="Test Business",
        rating="4.5 stars",
        category="Restaurant"
    )
    assert info.name == "Test Business"
    assert info.rating == "4.5 stars"
    
    # Default values
    info_defaults = BusinessInfo()
    assert info_defaults.name == "Unknown"
    assert info_defaults.phone == "Unavailable"


def test_review_validation():
    """Test Review model validation."""
    review = Review(
        username="John Doe",
        content="Great place!",
        rating="5 stars"
    )
    assert review.username == "John Doe"
    assert review.content == "Great place!"
    
    # Test content length validation
    long_content = "x" * 15000
    review_long = Review(content=long_content)
    assert len(review_long.content) <= 10003  # 10000 + "..."


def test_scrape_result():
    """Test ScrapeResult model."""
    result = ScrapeResult(
        url="https://example.com",
        success=True,
        business_info=BusinessInfo(name="Test"),
        reviews=[Review(content="Good")]
    )
    
    assert result.url == "https://example.com"
    assert result.success is True
    assert result.reviews_count == 1  # Auto-synced


def test_batch_config_validation():
    """Test BatchConfig validation."""
    config = BatchConfig(max_workers=5, timeout=120)
    assert config.max_workers == 5
    assert config.timeout == 120
    
    # Test validation limits
    with pytest.raises(ValueError):
        BatchConfig(max_workers=0)  # Below minimum
    
    with pytest.raises(ValueError):
        BatchConfig(output_format="invalid")  # Invalid format 