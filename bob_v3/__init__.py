"""
BOB Google Maps V3.0.1 - Ultimate Edition
Revolutionary Google Maps Data Extraction Platform

Author: Divyanshu Singh Chouhan
Release: October 3, 2025
Version: 3.0.1 (Refactored)

Features:
- Dual-engine extraction (Playwright + Selenium)
- Intelligent SQLite caching
- Network API interception
- Parallel processing (10x faster)
- Auto-healing selectors
- 95%+ success rate
"""

__version__ = "3.0.1"
__author__ = "Divyanshu Singh Chouhan"
__release_date__ = "2025-10-03"
__license__ = "MIT"

# Core extractors
from .extractors import (
    PlaywrightExtractor,
    SeleniumExtractor,
    HybridExtractor
)

# Cache system
from .cache import CacheManager

# Data models
from .models import Business, Review, Image

# Configuration
from .config import ExtractorConfig, CacheConfig, ParallelConfig

__all__ = [
    # Extractors
    "PlaywrightExtractor",
    "SeleniumExtractor",
    "HybridExtractor",
    # Cache
    "CacheManager",
    # Models
    "Business",
    "Review",
    "Image",
    # Config
    "ExtractorConfig",
    "CacheConfig",
    "ParallelConfig",
]
