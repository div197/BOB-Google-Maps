"""
BOB Google Maps v4.3.0 - Configuration Module

Configuration management for BOB extractors.
Supports environment variables for Docker/production deployments.
"""

from .settings import (
    ExtractorConfig, 
    CacheConfig, 
    ParallelConfig,
    DEFAULT_EXTRACTOR_CONFIG,
    DEFAULT_CACHE_CONFIG,
    DEFAULT_PARALLEL_CONFIG
)

__all__ = [
    'ExtractorConfig', 
    'CacheConfig', 
    'ParallelConfig',
    'DEFAULT_EXTRACTOR_CONFIG',
    'DEFAULT_CACHE_CONFIG',
    'DEFAULT_PARALLEL_CONFIG'
]
