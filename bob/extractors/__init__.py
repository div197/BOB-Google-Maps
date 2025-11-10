"""
BOB Google Maps - Extraction Engines

Three optimized extractors for different use cases:
- PlaywrightExtractorOptimized: Fast, recommended default (7-11s per business)
- SeleniumExtractorOptimized: Reliable fallback (8-15s per business)
- HybridExtractorOptimized: Memory-optimized (9-12s per business)
"""

from .playwright_optimized import PlaywrightExtractorOptimized
from .selenium_optimized import SeleniumExtractorOptimized
from .hybrid_optimized import HybridExtractorOptimized

__all__ = [
    'PlaywrightExtractorOptimized',
    'SeleniumExtractorOptimized',
    'HybridExtractorOptimized'
]

# Legacy imports for backwards compatibility
try:
    from .playwright import PlaywrightExtractor
    from .selenium import SeleniumExtractor
    from .hybrid import HybridExtractor
except ImportError:
    pass
