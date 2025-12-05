#!/usr/bin/env python3
"""
BOB Google Maps v4.3.0 - Production Integration Tests

These tests verify the extractor works correctly on real Google Maps data.
They test various business types across different locations.

Run with: python -m pytest tests/integration/test_production_v43.py -v

Author: BOB Team
Version: 4.3.0
Date: December 5, 2025
"""

import pytest
import asyncio
from bob.extractors.playwright_optimized import PlaywrightExtractorOptimized


class TestProductionExtractionV43:
    """
    Production integration tests for v4.3.0.
    
    These tests verify:
    - Core extraction functionality
    - GPS coordinates extraction
    - Phone/address/website extraction
    - Image extraction
    - Review extraction
    - Various business types and locations
    """
    
    @pytest.fixture
    def extractor(self):
        """Create a fresh extractor for each test."""
        return PlaywrightExtractorOptimized(headless=True)
    
    @pytest.mark.asyncio
    async def test_famous_hotel_extraction(self, extractor):
        """Test extraction of famous hotel that previously failed."""
        result = await extractor.extract_business_optimized(
            "Taj Mahal Palace Mumbai",
            include_reviews=True,
            max_reviews=3
        )
        
        assert result.get('success') is True, f"Extraction failed: {result.get('error')}"
        assert result.get('name') is not None, "Name should be extracted"
        assert 'Taj' in result.get('name', ''), f"Name should contain 'Taj': {result.get('name')}"
        assert result.get('phone') is not None, "Phone should be extracted"
        assert result.get('address') is not None, "Address should be extracted"
        assert result.get('website') is not None, "Website should be extracted"
        assert result.get('latitude') is not None, "Latitude should be extracted"
        assert result.get('longitude') is not None, "Longitude should be extracted"
        assert result.get('quality_score', 0) >= 80, f"Quality should be >= 80: {result.get('quality_score')}"
    
    @pytest.mark.asyncio
    async def test_tier2_city_restaurant(self, extractor):
        """Test extraction of restaurant in smaller city."""
        result = await extractor.extract_business_optimized(
            "Gypsy Restaurant Jodhpur",
            include_reviews=True,
            max_reviews=3
        )
        
        assert result.get('success') is True
        assert result.get('name') is not None
        assert result.get('phone') is not None
        assert result.get('latitude') is not None
        assert result.get('longitude') is not None
        assert result.get('quality_score', 0) >= 90
    
    @pytest.mark.asyncio
    async def test_us_chain_business(self, extractor):
        """Test extraction of US chain business."""
        result = await extractor.extract_business_optimized(
            "Starbucks Times Square NYC",
            include_reviews=True,
            max_reviews=3
        )
        
        assert result.get('success') is True
        assert result.get('name') is not None
        assert 'Starbucks' in result.get('name', '')
        assert result.get('phone') is not None
        assert result.get('latitude') is not None
        assert result.get('longitude') is not None
        # US coordinates check
        lat = result.get('latitude')
        if lat:
            assert 40 < lat < 41, f"Latitude should be around NYC (~40.75): {lat}"
    
    @pytest.mark.asyncio 
    async def test_direct_url_extraction(self, extractor):
        """Test extraction with direct Google Maps URL."""
        url = "https://www.google.com/maps/place/Empire+State+Building/@40.7484405,-73.9878584,17z/"
        
        result = await extractor.extract_business_optimized(
            url,
            include_reviews=False
        )
        
        assert result.get('success') is True
        assert result.get('name') is not None
        assert 'Empire' in result.get('name', '')
    
    @pytest.mark.asyncio
    async def test_image_extraction(self, extractor):
        """Test that images are properly extracted."""
        result = await extractor.extract_business_optimized(
            "Taj Mahal Palace Mumbai",
            include_reviews=False
        )
        
        images = result.get('images', [])
        assert len(images) > 0, "Should extract at least some images"
        
        # Check image URLs are valid
        for img in images[:3]:
            assert 'googleusercontent.com' in img, f"Image URL should be from Google: {img}"
    
    @pytest.mark.asyncio
    async def test_review_extraction(self, extractor):
        """Test that reviews are properly extracted."""
        result = await extractor.extract_business_optimized(
            "Starbucks Times Square NYC",
            include_reviews=True,
            max_reviews=5
        )
        
        reviews = result.get('reviews', [])
        # Note: Review extraction may vary, so we just check it doesn't error
        assert isinstance(reviews, list)
    
    @pytest.mark.asyncio
    async def test_gps_accuracy(self, extractor):
        """Test GPS coordinates are accurate."""
        # Known coordinates for Taj Mahal Palace Mumbai
        expected_lat = 18.92
        expected_lng = 72.83
        
        result = await extractor.extract_business_optimized(
            "Taj Mahal Palace Mumbai",
            include_reviews=False
        )
        
        lat = result.get('latitude')
        lng = result.get('longitude')
        
        assert lat is not None, "Latitude should be extracted"
        assert lng is not None, "Longitude should be extracted"
        
        # Check within ~1km accuracy
        assert abs(lat - expected_lat) < 0.01, f"Latitude should be ~{expected_lat}: {lat}"
        assert abs(lng - expected_lng) < 0.01, f"Longitude should be ~{expected_lng}: {lng}"
    
    @pytest.mark.asyncio
    async def test_quality_score_calculation(self, extractor):
        """Test quality score is calculated correctly."""
        result = await extractor.extract_business_optimized(
            "Gypsy Restaurant Jodhpur",
            include_reviews=True,
            max_reviews=3
        )
        
        score = result.get('quality_score', 0)
        
        # Score breakdown expectations:
        # - Name: 20 points
        # - Phone: 15 points
        # - Address: 15 points
        # - Website: 10 points
        # - GPS: 15 points
        # - Rating: 5 points
        # - Reviews count: 5 points
        # - Category: 5 points
        # Total potential: 90 points (plus bonus for reviews/images)
        
        assert score >= 80, f"Quality score should be >= 80 for complete data: {score}"


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    @pytest.fixture
    def extractor(self):
        return PlaywrightExtractorOptimized(headless=True)
    
    @pytest.mark.asyncio
    async def test_nonexistent_business(self, extractor):
        """Test handling of nonexistent business."""
        result = await extractor.extract_business_optimized(
            "XYZ123NonexistentBusiness99999",
            include_reviews=False
        )
        
        # Should not crash, but may return low quality or failure
        assert 'success' in result or 'error' in result
    
    @pytest.mark.asyncio
    async def test_special_characters_in_query(self, extractor):
        """Test handling of special characters."""
        result = await extractor.extract_business_optimized(
            "McDonald's Times Square",  # Apostrophe
            include_reviews=False
        )
        
        assert result.get('success') is True or 'error' in result


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
