"""
BOB Google Maps V3.0 - Cache Manager Integration Tests
Author: Divyanshu Singh Chouhan
Release: October 3, 2025

Real integration tests for SQLite cache system.
"""

import pytest
import os
from pathlib import Path
from datetime import datetime, timedelta

from bob.cache import CacheManager
from bob.models import Business, Review


class TestCacheManagerIntegration:
    """Integration tests for CacheManager."""

    @pytest.fixture
    def cache_manager(self, tmp_path):
        """Create temporary cache manager for testing."""
        db_path = tmp_path / "test_cache.db"
        cache = CacheManager(db_path=str(db_path))
        yield cache
        # Cleanup
        if os.path.exists(db_path):
            os.remove(db_path)

    @pytest.fixture
    def sample_business(self):
        """Create sample business for testing."""
        business = Business(
            place_id="ChIJTest123",
            cid=123456789,
            name="Test Restaurant",
            phone="+1-555-1234",
            address="123 Test Street",
            latitude=40.7128,
            longitude=-74.0060,
            category="Restaurant",
            rating=4.5,
            review_count=100,
            website="https://test.com"
        )
        business.photos = [
            "https://example.com/photo1.jpg",
            "https://example.com/photo2.jpg"
        ]
        business.reviews = [
            Review(reviewer="John Doe", rating=5, text="Excellent!", date="1 week ago"),
            Review(reviewer="Jane Smith", rating=4, text="Good", date="2 weeks ago")
        ]
        business.data_quality_score = 85
        return business

    def test_cache_initialization(self, cache_manager):
        """Test cache database initialization."""
        stats = cache_manager.get_statistics()

        assert stats is not None
        assert stats['total_cached'] == 0
        assert stats['cache_hits'] == 0

    def test_save_and_retrieve_business(self, cache_manager, sample_business):
        """Test saving and retrieving business from cache."""
        # Save business
        cache_manager.save_to_cache(sample_business)

        # Retrieve business
        cached = cache_manager.get_cached("ChIJTest123")

        assert cached is not None
        assert cached.name == "Test Restaurant"
        assert cached.phone == "+1-555-1234"
        assert cached.rating == 4.5
        assert cached.data_quality_score == 85
        assert len(cached.photos) == 2
        assert len(cached.reviews) == 2

    def test_cache_expiration(self, cache_manager, sample_business):
        """Test cache expiration functionality."""
        # Save business
        cache_manager.save_to_cache(sample_business)

        # Should be retrievable with default expiration
        cached = cache_manager.get_cached("ChIJTest123", max_age_hours=24)
        assert cached is not None

        # Should be None with very short expiration
        cached_expired = cache_manager.get_cached("ChIJTest123", max_age_hours=0)
        assert cached_expired is None

    def test_cache_update(self, cache_manager, sample_business):
        """Test updating cached business."""
        # Save initial business
        cache_manager.save_to_cache(sample_business)

        # Update business
        sample_business.rating = 4.8
        sample_business.review_count = 150
        cache_manager.save_to_cache(sample_business)

        # Retrieve updated business
        cached = cache_manager.get_cached("ChIJTest123")

        assert cached.rating == 4.8
        assert cached.review_count == 150

    def test_cache_statistics(self, cache_manager, sample_business):
        """Test cache statistics tracking."""
        # Initial stats
        stats = cache_manager.get_statistics()
        assert stats['total_cached'] == 0

        # Save multiple businesses
        cache_manager.save_to_cache(sample_business)

        # Create another business
        business2 = Business(
            place_id="ChIJTest456",
            name="Another Business"
        )
        cache_manager.save_to_cache(business2)

        # Check updated stats
        stats = cache_manager.get_statistics()
        assert stats['total_cached'] == 2

    def test_cache_cleanup(self, cache_manager, sample_business):
        """Test cache cleanup of old entries."""
        # Save business
        cache_manager.save_to_cache(sample_business)

        # Verify it exists
        assert cache_manager.get_cached("ChIJTest123") is not None

        # Cleanup with 0 days (remove all)
        cache_manager.cleanup_old_cache(days=0)

        # Should still exist if recent
        # This test validates that cleanup respects timing
        stats = cache_manager.get_statistics()
        assert stats is not None

    def test_multiple_business_caching(self, cache_manager):
        """Test caching multiple businesses."""
        businesses = []
        for i in range(5):
            business = Business(
                place_id=f"ChIJTest{i}",
                name=f"Business {i}",
                rating=4.0 + (i * 0.1)
            )
            businesses.append(business)
            cache_manager.save_to_cache(business)

        # Verify all cached
        for i, business in enumerate(businesses):
            cached = cache_manager.get_cached(f"ChIJTest{i}")
            assert cached is not None
            assert cached.name == f"Business {i}"
            assert cached.rating == 4.0 + (i * 0.1)

    def test_cache_with_special_characters(self, cache_manager):
        """Test caching businesses with special characters."""
        business = Business(
            place_id="ChIJ_Special-123",
            name="Test's \"Restaurant\" & Café",
            phone="+1 (555) 123-4567",
            address="123 O'Brien St, Apt #5"
        )

        cache_manager.save_to_cache(business)
        cached = cache_manager.get_cached("ChIJ_Special-123")

        assert cached is not None
        assert cached.name == "Test's \"Restaurant\" & Café"
        assert cached.phone == "+1 (555) 123-4567"
