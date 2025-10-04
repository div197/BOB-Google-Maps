"""
BOB Google Maps V3.0 - Configuration Unit Tests
Author: Divyanshu Singh Chouhan
Release: October 3, 2025

Real tests for configuration management.
"""

import pytest
import os
from bob_v3.config import ExtractorConfig, CacheConfig, ParallelConfig


class TestExtractorConfig:
    """Test suite for ExtractorConfig."""

    def test_default_config(self):
        """Test default configuration values."""
        config = ExtractorConfig()

        assert config.headless is True
        assert config.timeout == 60
        assert config.max_retries == 3
        assert config.stealth_mode is True
        assert config.intercept_network is True
        assert config.max_reviews == 10
        assert config.max_images == 20

    def test_custom_config(self):
        """Test custom configuration values."""
        config = ExtractorConfig(
            headless=False,
            timeout=30,
            max_retries=5,
            max_reviews=20
        )

        assert config.headless is False
        assert config.timeout == 30
        assert config.max_retries == 5
        assert config.max_reviews == 20

    def test_config_from_env(self):
        """Test creating config from environment variables."""
        # Set test environment variables
        os.environ['BOB_HEADLESS'] = 'false'
        os.environ['BOB_TIMEOUT'] = '90'
        os.environ['BOB_MAX_RETRIES'] = '5'

        config = ExtractorConfig.from_env()

        assert config.headless is False
        assert config.timeout == 90
        assert config.max_retries == 5

        # Cleanup
        del os.environ['BOB_HEADLESS']
        del os.environ['BOB_TIMEOUT']
        del os.environ['BOB_MAX_RETRIES']


class TestCacheConfig:
    """Test suite for CacheConfig."""

    def test_default_cache_config(self):
        """Test default cache configuration."""
        config = CacheConfig()

        assert config.enabled is True
        assert config.cache_db_path == "bob_cache_ultimate.db"
        assert config.expiration_hours == 24
        assert config.auto_cleanup is True

    def test_custom_cache_config(self):
        """Test custom cache configuration."""
        config = CacheConfig(
            enabled=False,
            cache_db_path="custom_cache.db",
            expiration_hours=48
        )

        assert config.enabled is False
        assert config.cache_db_path == "custom_cache.db"
        assert config.expiration_hours == 48

    def test_cache_config_from_env(self):
        """Test creating cache config from environment."""
        os.environ['BOB_CACHE_ENABLED'] = 'false'
        os.environ['BOB_CACHE_HOURS'] = '12'

        config = CacheConfig.from_env()

        assert config.enabled is False
        assert config.expiration_hours == 12

        # Cleanup
        del os.environ['BOB_CACHE_ENABLED']
        del os.environ['BOB_CACHE_HOURS']


class TestParallelConfig:
    """Test suite for ParallelConfig."""

    def test_default_parallel_config(self):
        """Test default parallel configuration."""
        config = ParallelConfig()

        assert config.enabled is True
        assert config.max_concurrent == 10
        assert config.context_pool_size == 5
        assert config.batch_size == 100

    def test_custom_parallel_config(self):
        """Test custom parallel configuration."""
        config = ParallelConfig(
            enabled=False,
            max_concurrent=5,
            batch_size=50
        )

        assert config.enabled is False
        assert config.max_concurrent == 5
        assert config.batch_size == 50

    def test_parallel_config_from_env(self):
        """Test creating parallel config from environment."""
        os.environ['BOB_MAX_CONCURRENT'] = '15'
        os.environ['BOB_BATCH_SIZE'] = '200'

        config = ParallelConfig.from_env()

        assert config.max_concurrent == 15
        assert config.batch_size == 200

        # Cleanup
        del os.environ['BOB_MAX_CONCURRENT']
        del os.environ['BOB_BATCH_SIZE']
