"""
BOB Google Maps v4.3.0 - Extraction Engines

Production-grade extractors for Google Maps data extraction.

Recommended Usage:
    from bob.extractors import HybridExtractorOptimized
    
    extractor = HybridExtractorOptimized()
    result = extractor.extract_business("Business Name")

Available Extractors:
- PlaywrightExtractorOptimized: Primary engine (10-22s per business)
- SeleniumExtractorOptimized: Fallback engine (15-30s per business)  
- HybridExtractorOptimized: Smart orchestrator with caching
"""

# Primary extractor (always available)
from .playwright_optimized import PlaywrightExtractorOptimized

__all__ = ['PlaywrightExtractorOptimized']

# Hybrid extractor (recommended for production)
try:
    from .hybrid_optimized import HybridExtractorOptimized
    __all__.append('HybridExtractorOptimized')
except ImportError:
    HybridExtractorOptimized = None

# Selenium fallback (optional)
try:
    from .selenium_optimized import SeleniumExtractorOptimized
    __all__.append('SeleniumExtractorOptimized')
except ImportError:
    SeleniumExtractorOptimized = None

# Legacy imports for backwards compatibility (deprecated)
try:
    from .hybrid import HybridExtractor
    __all__.append('HybridExtractor')
except ImportError:
    HybridExtractor = None
