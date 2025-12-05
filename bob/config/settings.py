"""
BOB Google Maps v4.3.0 - Configuration Settings

Centralized configuration for all extraction operations.
Supports environment variables for Docker/production deployments.
"""

from dataclasses import dataclass, field
from typing import Optional, List
import os
from pathlib import Path


@dataclass
class ExtractorConfig:
    """Configuration for extraction engines."""

    # Browser settings
    headless: bool = True
    timeout: int = 60
    page_load_timeout: int = 90

    # Retry settings
    max_retries: int = 3
    retry_delay: int = 2

    # Stealth settings
    stealth_mode: bool = True
    user_agent: Optional[str] = None

    # Network settings
    intercept_network: bool = True
    block_resources: bool = True
    blocked_resource_types: List[str] = field(default_factory=lambda: ['image', 'stylesheet', 'font', 'media'])

    # Engine settings
    selenium_enabled: bool = True
    max_reviews: int = 10
    max_images: int = 20
    include_reviews: bool = True
    include_images: bool = True

    # Paths
    cache_dir: Path = field(default_factory=lambda: Path("./cache"))
    logs_dir: Path = field(default_factory=lambda: Path("./logs"))
    data_dir: Path = field(default_factory=lambda: Path("./data"))

    # Quality thresholds
    min_quality_score: int = 50

    @classmethod
    def from_env(cls):
        """Create configuration from environment variables."""
        return cls(
            headless=os.getenv('BOB_HEADLESS', 'true').lower() == 'true',
            timeout=int(os.getenv('BOB_TIMEOUT', '60')),
            max_retries=int(os.getenv('BOB_MAX_RETRIES', '3')),
            stealth_mode=os.getenv('BOB_STEALTH', 'true').lower() == 'true',
            intercept_network=os.getenv('BOB_INTERCEPT', 'true').lower() == 'true',
            block_resources=os.getenv('BOB_BLOCK_RESOURCES', 'true').lower() == 'true',
            max_reviews=int(os.getenv('BOB_MAX_REVIEWS', '10')),
            max_images=int(os.getenv('BOB_MAX_IMAGES', '20')),
            selenium_enabled=os.getenv('BOB_SELENIUM_ENABLED', 'true').lower() == 'true',
        )


@dataclass
class CacheConfig:
    """Configuration for caching system."""

    # Cache settings
    enabled: bool = True
    cache_db_path: str = "bob_cache_ultimate.db"
    expiration_hours: int = 24

    # Cache behavior
    auto_cleanup: bool = True
    cleanup_days: int = 7
    max_cache_size_mb: int = 500

    @classmethod
    def from_env(cls):
        """Create cache configuration from environment variables."""
        return cls(
            enabled=os.getenv('BOB_CACHE_ENABLED', 'true').lower() == 'true',
            cache_db_path=os.getenv('BOB_CACHE_PATH', 'bob_cache_ultimate.db'),
            expiration_hours=int(os.getenv('BOB_CACHE_HOURS', '24')),
            auto_cleanup=os.getenv('BOB_AUTO_CLEANUP', 'true').lower() == 'true',
            cleanup_days=int(os.getenv('BOB_CLEANUP_DAYS', '7')),
        )


@dataclass
class ParallelConfig:
    """Configuration for parallel processing."""

    # Parallel settings
    enabled: bool = True
    max_concurrent: int = 10
    context_pool_size: int = 5

    # Resource limits
    max_memory_mb: int = 2048
    max_cpu_percent: int = 80

    # Batch processing
    batch_size: int = 100
    checkpoint_interval: int = 10

    @classmethod
    def from_env(cls):
        """Create parallel configuration from environment variables."""
        return cls(
            enabled=os.getenv('BOB_PARALLEL_ENABLED', 'true').lower() == 'true',
            max_concurrent=int(os.getenv('BOB_MAX_CONCURRENT', '10')),
            context_pool_size=int(os.getenv('BOB_CONTEXT_POOL', '5')),
            max_memory_mb=int(os.getenv('BOB_MAX_MEMORY_MB', '2048')),
            batch_size=int(os.getenv('BOB_BATCH_SIZE', '100')),
        )


# Default configurations
DEFAULT_EXTRACTOR_CONFIG = ExtractorConfig()
DEFAULT_CACHE_CONFIG = CacheConfig()
DEFAULT_PARALLEL_CONFIG = ParallelConfig()
