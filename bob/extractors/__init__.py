"""
BOB Google Maps - Extraction Engines

Three optimized extractors for different use cases:
- PlaywrightExtractorOptimized: Fast, recommended default (7-11s per business)
- SeleniumExtractorOptimized: Reliable fallback (8-15s per business)
- HybridExtractorOptimized: Memory-optimized (9-12s per business)
"""

# Import Playwright extractors (no external dependencies)
from .playwright_optimized import PlaywrightExtractorOptimized

__all__ = ['PlaywrightExtractorOptimized']

# Try to import Selenium extractors (requires undetected-chromedriver)
try:
    from .selenium_optimized import SeleniumExtractorOptimized
    __all__.append('SeleniumExtractorOptimized')
except ImportError:
    pass

# Try to import Hybrid extractors
try:
    from .hybrid_optimized import HybridExtractorOptimized
    __all__.append('HybridExtractorOptimized')
except ImportError:
    pass

# Legacy imports for backwards compatibility
try:
    from .playwright import PlaywrightExtractor
    __all__.append('PlaywrightExtractor')
except ImportError:
    pass

try:
    from .selenium import SeleniumExtractor
    __all__.append('SeleniumExtractor')
except ImportError:
    pass

try:
    from .hybrid import HybridExtractor
    __all__.append('HybridExtractor')
except ImportError:
    pass
