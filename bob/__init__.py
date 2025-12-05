"""
BOB Google Maps v4.3.0 - Production-Grade Business Data Extraction

Extract comprehensive business data from Google Maps with 95%+ accuracy.

Key Features:
- 95%+ success rate on all business types
- Production-ready enterprise quality
- One-click setup (./setup.sh)
- Fast extraction (10-22 seconds per business)
- Memory efficient (<50MB peak)
- Multiple extraction engines (Playwright primary, Selenium fallback)
- Intelligent SQLite caching (1800x speedup)
- GPS coordinates, images, reviews, all contact details

Usage:
    from bob import HybridExtractorOptimized
    
    extractor = HybridExtractorOptimized()
    result = extractor.extract_business("Starbucks Times Square NYC")
    
    print(f"Name: {result.get('name')}")
    print(f"Phone: {result.get('phone')}")
    print(f"Rating: {result.get('rating')}")
    print(f"GPS: {result.get('latitude')}, {result.get('longitude')}")
"""

__version__ = '4.3.0'
__author__ = 'Divyanshu (Dhrishtadyumna)'
__license__ = 'MIT'

# Core extractors
from .extractors import PlaywrightExtractorOptimized

# Try to import optional extractors
try:
    from .extractors import SeleniumExtractorOptimized
except ImportError:
    SeleniumExtractorOptimized = None

try:
    from .extractors import HybridExtractorOptimized
except ImportError:
    HybridExtractorOptimized = None

# Data models
from .models.business import Business
from .models.review import Review
from .models.image import Image

# Cache management
from .cache import CacheManager

# Configuration
from .config import ExtractorConfig

__all__ = [
    # Extractors
    'PlaywrightExtractorOptimized',
    'SeleniumExtractorOptimized',
    'HybridExtractorOptimized',
    
    # Data models
    'Business',
    'Review',
    'Image',
    
    # Cache
    'CacheManager',
    
    # Configuration
    'ExtractorConfig',
    
    # Metadata
    '__version__',
    '__author__',
    '__license__'
]
