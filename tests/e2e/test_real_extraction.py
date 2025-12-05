#!/usr/bin/env python3
"""
BOB Google Maps v4.3.0 - E2E Real Extraction Tests

End-to-end tests with REAL Google Maps extraction.
These perform actual web scraping - slow but validates real functionality.

Run with: pytest tests/e2e/ -v -m slow

Author: BOB Team
Version: 4.3.0
"""

import pytest
import asyncio
from bob.extractors.playwright_optimized import PlaywrightExtractorOptimized


@pytest.mark.slow
@pytest.mark.e2e
class TestRealExtraction:
    """
    Real end-to-end extraction tests.
    
    These tests perform actual Google Maps scraping.
    Note: They are slow and require internet connection.
    """
    
    @pytest.fixture
    def extractor(self):
        """Create extractor for testing."""
        return PlaywrightExtractorOptimized(headless=True)
    
    @pytest.mark.asyncio
    async def test_extract_starbucks(self, extractor):
        """Test extracting Starbucks (well-known business)."""
        result = await extractor.extract_business_optimized(
            "Starbucks Times Square NYC",
            include_reviews=False
        )
        
        assert result is not None
        assert result.get('success') is True
        assert result.get('name') is not None
        assert 'Starbucks' in result.get('name', '') or 'Coffee' in result.get('category', '')
    
    @pytest.mark.asyncio
    async def test_extract_with_gps(self, extractor):
        """Test that GPS coordinates are extracted."""
        result = await extractor.extract_business_optimized(
            "Empire State Building NYC",
            include_reviews=False
        )
        
        assert result.get('success') is True
        assert result.get('latitude') is not None
        assert result.get('longitude') is not None
        
        # Verify coordinates are in valid range (NYC area)
        lat = result.get('latitude')
        lng = result.get('longitude')
        assert 40.0 < lat < 41.0, f"Latitude {lat} not in NYC range"
        assert -74.5 < lng < -73.5, f"Longitude {lng} not in NYC range"
    
    @pytest.mark.asyncio
    async def test_extract_with_reviews(self, extractor):
        """Test that reviews are extracted."""
        result = await extractor.extract_business_optimized(
            "Taj Mahal Palace Mumbai",
            include_reviews=True,
            max_reviews=3
        )
        
        assert result.get('success') is True
        assert result.get('reviews') is not None
        # Reviews may be empty if hotel has restricted reviews
        if result.get('reviews'):
            assert len(result.get('reviews')) <= 3
    
    @pytest.mark.asyncio
    async def test_extract_restaurant(self, extractor):
        """Test extracting a restaurant."""
        result = await extractor.extract_business_optimized(
            "The Bombay Canteen Mumbai",
            include_reviews=False
        )
        
        assert result.get('success') is True
        assert result.get('name') is not None
        assert result.get('address') is not None
    
    @pytest.mark.asyncio
    async def test_quality_score(self, extractor):
        """Test that quality score is calculated."""
        result = await extractor.extract_business_optimized(
            "Google NYC Office",
            include_reviews=False
        )
        
        assert result.get('success') is True
        assert result.get('quality_score') is not None
        assert 0 <= result.get('quality_score', 0) <= 100
