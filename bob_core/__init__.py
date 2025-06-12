"""BOB Google Maps v0.6.0

Enterprise-grade Google Maps scraper with divine thermodynamics system.
Following Niṣkāma Karma Yoga principles - Selfless Excellence.

🔱 Made in India 🇮🇳, Made for the World 🌍
"""

__version__ = "0.6.0"
__author__ = "Divyanshu Singh Chouhan"
__email__ = "divyanshu@abcsteps.com"

# Main interfaces - Primary user-facing classes
from .scraper import BOBScraper, GoogleMapsScraper
from .analytics import BusinessAnalytics, BusinessAnalyzer

# Core functionality
from .business_parser import BusinessParser
from .review_parser import ReviewParser
from .models import BusinessInfo, Review, ScrapeResult

# Fault tolerance and reliability
from .circuit_breaker import CircuitBreaker, get_circuit_breaker

# Batch processing
from .batch import batch_scrape, async_batch_scrape

__all__ = [
    # Main interfaces
    "BOBScraper",
    "GoogleMapsScraper", 
    "BusinessAnalytics",
    "BusinessAnalyzer",
    
    # Core functionality
    "BusinessParser",
    "ReviewParser",
    "BusinessInfo",
    "Review", 
    "ScrapeResult",
    
    # Fault tolerance
    "CircuitBreaker",
    "get_circuit_breaker",
    
    # Batch processing
    "batch_scrape",
    "async_batch_scrape",
    
    # Metadata
    "__version__",
    "__author__",
    "__email__"
] 