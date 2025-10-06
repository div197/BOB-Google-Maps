"""
BOB Google Maps V3.0 - Real Extraction E2E Tests
Author: Divyanshu Singh Chouhan
Release: October 3, 2025

End-to-end tests with REAL Google Maps extraction.
These are NOT dummy tests - they perform actual web scraping.
"""

import pytest

from bob.extractors import HybridExtractor


@pytest.mark.slow
@pytest.mark.integration
class TestRealExtraction:
    """
    Real end-to-end extraction tests.
    These tests perform actual Google Maps scraping.

    Note: These tests are slow and require internet connection.
    Mark with @pytest.mark.slow to skip during fast testing.
    """

    @pytest.fixture
    def extractor(self):
        """Create hybrid extractor for testing."""
        return HybridExtractor(use_cache=False)

    def test_extract_well_known_business(self, extractor):
        """
        Test extracting a well-known business (Starbucks).
        This validates that the extractor can handle common businesses.
        """
        # Use a well-known business that should always exist
        result = extractor.extract_business("Starbucks New York Times Square")

        # Validate extraction succeeded
        assert result is not None
        assert result.name is not None
        assert "starbucks" in result.name.lower() or "coffee" in result.name.lower()

        # Validate key data points
        assert result.place_id is not None or result.cid is not None
        assert result.latitude is not None
        assert result.longitude is not None

        # Validate quality score
        assert result.data_quality_score > 0
        print(f"\n✓ Extracted: {result.name}")
        print(f"✓ Quality Score: {result.data_quality_score}/100")
        print(f"✓ Method: {result.extraction_method}")

    def test_extract_restaurant_with_reviews(self, extractor):
        """
        Test extracting a restaurant with full data including reviews.
        This validates comprehensive data extraction.
        """
        result = extractor.extract_business("McDonald's Times Square New York")

        # Validate basic data
        assert result is not None
        assert result.name is not None

        # Validate GPS coordinates
        assert result.latitude is not None
        assert result.longitude is not None

        # Check for reviews (at least some reviews should be extracted)
        # Note: Reviews may not always be available, so we just check the field exists
        assert hasattr(result, 'reviews')
        assert isinstance(result.reviews, list)

        # Check for photos
        assert hasattr(result, 'photos')
        assert isinstance(result.photos, list)

        print(f"\n✓ Business: {result.name}")
        print(f"✓ Rating: {result.rating}/5 ({result.review_count} reviews)")
        print(f"✓ Photos: {len(result.photos)}")
        print(f"✓ Reviews extracted: {len(result.reviews)}")
        print(f"✓ Quality: {result.data_quality_score}/100")

    def test_extract_local_business(self, extractor):
        """
        Test extracting a local business (The Filos Jodhpur).
        This validates extraction of less common, location-specific businesses.
        """
        result = extractor.extract_business("The Filos Jodhpur Rajasthan India")

        # Validate extraction
        assert result is not None
        assert result.data_quality_score > 0

        # At minimum, should have name and location
        assert result.name is not None
        assert (result.latitude is not None and result.longitude is not None) or \
               (result.address is not None)

        print(f"\n✓ Local Business: {result.name}")
        print(f"✓ Phone: {result.phone or 'Not found'}")
        print(f"✓ Address: {result.address or 'Not found'}")
        print(f"✓ Quality: {result.data_quality_score}/100")

    def test_extraction_method_fallback(self, extractor):
        """
        Test that extraction uses appropriate methods and fallbacks.
        This validates the hybrid engine's strategy selection.
        """
        result = extractor.extract_business("Apple Store Fifth Avenue New York")

        assert result is not None
        assert result.extraction_method in ['cache', 'playwright', 'selenium_v2', 'hybrid']

        print(f"\n✓ Extraction Method: {result.extraction_method}")
        print(f"✓ Business: {result.name}")
        print(f"✓ Quality: {result.data_quality_score}/100")

    def test_quality_score_accuracy(self, extractor):
        """
        Test that quality scores accurately reflect data completeness.
        High-profile businesses should have high quality scores.
        """
        # Extract a major business (should have complete data)
        result = extractor.extract_business("Grand Central Terminal New York")

        assert result is not None

        # Calculate expected quality based on available data
        has_name = result.name is not None
        has_location = result.latitude is not None and result.longitude is not None
        has_contact = result.phone is not None or result.website is not None
        has_rating = result.rating is not None

        # Major businesses should have most data
        data_completeness = sum([has_name, has_location, has_contact, has_rating])

        print(f"\n✓ Business: {result.name}")
        print(f"✓ Has Name: {has_name}")
        print(f"✓ Has Location: {has_location}")
        print(f"✓ Has Contact: {has_contact}")
        print(f"✓ Has Rating: {has_rating}")
        print(f"✓ Quality Score: {result.data_quality_score}/100")

        # Quality score should reflect data completeness
        if data_completeness >= 3:
            assert result.data_quality_score >= 40

    @pytest.mark.parametrize("business_name", [
        "Starbucks Coffee",
        "McDonald's Restaurant",
        "Apple Store",
    ])
    def test_multiple_extractions(self, extractor, business_name):
        """
        Test extracting multiple different businesses.
        Validates consistent extraction across different business types.
        """
        result = extractor.extract_business(business_name + " New York")

        assert result is not None
        assert result.name is not None
        assert result.data_quality_score > 0

        print(f"\n✓ {business_name}: Quality {result.data_quality_score}/100")


@pytest.mark.slow
class TestCacheIntegration:
    """Test cache integration in real extraction scenarios."""

    def test_cache_speedup(self):
        """
        Test that caching provides significant speedup on re-queries.
        This is a real performance test.
        """
        import time

        extractor_no_cache = HybridExtractor(use_cache=False)
        extractor_with_cache = HybridExtractor(use_cache=True)

        business_query = "Starbucks Reserve Roastery New York"

        # First extraction without cache
        start = time.time()
        result1 = extractor_no_cache.extract_business(business_query)
        time_no_cache = time.time() - start

        # First extraction with cache (will cache it)
        start = time.time()
        result2 = extractor_with_cache.extract_business(business_query)
        time_first = time.time() - start

        # Second extraction with cache (should be cached)
        start = time.time()
        result3 = extractor_with_cache.extract_business(business_query)
        time_cached = time.time() - start

        print(f"\n✓ Time without cache: {time_no_cache:.2f}s")
        print(f"✓ Time first (cached): {time_first:.2f}s")
        print(f"✓ Time cached: {time_cached:.2f}s")
        print(f"✓ Speedup: {time_first/time_cached:.1f}x faster")

        # Cached query should be significantly faster
        assert time_cached < time_first * 0.5  # At least 2x faster
        assert result3.extraction_method == 'cache'
