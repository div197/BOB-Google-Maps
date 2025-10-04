"""
BOB Google Maps V3.0 - Test Fixtures and Configuration
Author: Divyanshu Singh Chouhan
Release: October 3, 2025

Shared test fixtures and utilities.
"""

import pytest

from bob_v3.config import ExtractorConfig, CacheConfig, ParallelConfig


@pytest.fixture
def test_config():
    """Test configuration with conservative settings."""
    return ExtractorConfig(
        headless=True,
        timeout=30,
        max_retries=2,
        stealth_mode=True,
        intercept_network=True,
        block_resources=True,
        max_reviews=5,
        max_images=10,
        min_quality_score=40
    )


@pytest.fixture
def cache_config():
    """Test cache configuration."""
    return CacheConfig(
        enabled=True,
        cache_db_path="test_cache.db",
        expiration_hours=1,
        auto_cleanup=False
    )


@pytest.fixture
def parallel_config():
    """Test parallel configuration."""
    return ParallelConfig(
        enabled=True,
        max_concurrent=3,
        context_pool_size=2,
        batch_size=10
    )


@pytest.fixture
def real_business_urls():
    """Real Google Maps URLs for testing."""
    return {
        'starbucks': 'https://www.google.com/maps/place/Starbucks',
        'mcdonalds': 'https://www.google.com/maps/place/McDonald\'s',
        'apple_store': 'https://www.google.com/maps/place/Apple+Store',
    }


@pytest.fixture
def test_business_names():
    """Real business names for search testing."""
    return [
        "Starbucks Coffee New York",
        "The Filos Jodhpur",
        "ABC Steps Jodhpur"
    ]


@pytest.fixture
def expected_fields():
    """Expected fields in extracted business data."""
    return [
        'name',
        'place_id',
        'cid',
        'latitude',
        'longitude',
        'data_quality_score',
        'extraction_method'
    ]
