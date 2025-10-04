"""
BOB Google Maps V3.0 - Ultimate Edition
Revolutionary Google Maps Data Extraction Platform

Author: Divyanshu Singh Chouhan
Release: October 3, 2025
Version: 3.0.0

Features:
- Dual-engine extraction (Playwright + Selenium)
- Intelligent SQLite caching
- Network API interception
- Parallel processing (10x faster)
- Auto-healing selectors
- 95%+ success rate
"""

__version__ = "3.0.0"
__author__ = "Divyanshu Singh Chouhan"
__release_date__ = "2025-10-03"
__license__ = "MIT"

from .extractors import (
    PlaywrightExtractor,
    SeleniumExtractor,
    HybridExtractor
)
from .cache import CacheManager
from .models import Business, Review, Image

__all__ = [
    "PlaywrightExtractor",
    "SeleniumExtractor",
    "HybridExtractor",
    "CacheManager",
    "Business",
    "Review",
    "Image",
]
