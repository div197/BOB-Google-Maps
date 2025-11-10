# API Reference - BOB Google Maps

Complete API documentation for all extractors and utilities.

## Core Extractors

### PlaywrightExtractorOptimized

Fast, JavaScript-enabled extraction engine.

```python
from bob import PlaywrightExtractorOptimized

extractor = PlaywrightExtractorOptimized(
    headless=True,              # Run browser in background
    timeout=30,                 # Timeout in seconds
    use_cache=True,             # Use SQLite cache
    memory_optimized=False      # Memory optimization mode
)

# Extract single business
result = extractor.extract_business(
    query,                      # Business name/location
    include_reviews=False,      # Include review data
    max_reviews=0              # Max reviews to fetch
)

# Check result
if result['success']:
    business = result['business']
    # Access fields: name, phone, address, rating, etc.
else:
    error = result['error']
    print(f"Extraction failed: {error}")
```

### SeleniumExtractorOptimized

Reliable fallback engine with undetected-chromedriver.

```python
from bob import SeleniumExtractorOptimized

extractor = SeleniumExtractorOptimized(
    headless=True,
    stealth_mode=True,          # Use undetected-chromedriver
    timeout=30
)

result = extractor.extract_business(query)
```

### HybridExtractorOptimized

Memory-optimized hybrid approach.

```python
from bob import HybridExtractorOptimized

extractor = HybridExtractorOptimized(
    memory_optimized=True,
    max_concurrent=1,
    cleanup_delay=3
)

result = extractor.extract_business(query)
```

## Business Data Model

### Business Object

```python
@dataclass
class Business:
    # Core Fields
    name: Optional[str]                 # Business name
    phone: Optional[str]                # Phone number
    address: Optional[str]              # Full address
    
    # Contact & Web
    emails: List[str]                   # Email addresses
    website: Optional[str]              # Website URL
    
    # Location
    latitude: Optional[float]           # GPS latitude
    longitude: Optional[float]          # GPS longitude
    plus_code: Optional[str]            # Google Plus Code
    
    # Business Info
    category: Optional[str]             # Business category
    rating: Optional[float]             # Star rating (0-5)
    review_count: Optional[int]         # Number of reviews
    
    # Operations
    hours: Optional[str]                # Operating hours
    current_status: Optional[str]       # Open/Closed status
    
    # Metadata
    data_quality_score: int             # Quality 0-100
    extraction_time_seconds: float      # Extraction duration
    extracted_at: datetime              # Extraction timestamp
    
    # Additional
    place_id: Optional[str]             # Google Place ID
    cid: Optional[int]                  # Business CID
    photos: List[str]                   # Photo URLs
    reviews: List[Review]               # Review objects
```

### Review Object

```python
@dataclass
class Review:
    reviewer: str                       # Reviewer name
    rating: str                         # Review rating
    text: str                           # Review text
    date: str                           # Review date
    review_index: int                   # Review position
```

## Batch Processing

### BatchProcessor

Process multiple businesses efficiently.

```python
from bob.utils.batch_processor import BatchProcessor

processor = BatchProcessor(
    headless=True,
    include_reviews=False,
    max_reviews=0,
    max_concurrent=5
)

# Process businesses
results = processor.process_batch_with_retry(
    businesses=['Business1', 'Business2', ...],
    max_retries=1,
    verbose=True
)

# Results is a list of extraction results
for result in results:
    if result['success']:
        print(f"✅ {result['business'].name}")
    else:
        print(f"❌ {result['error']}")
```

## Cache Management

### CacheManager

Manage SQLite cache for fast repeated queries.

```python
from bob.cache import CacheManager

cache = CacheManager()

# Get cached business
cached = cache.get_cached_business("Starbucks Times Square")

# Save to cache
cache.save_to_cache("Starbucks Times Square", business_data)

# Clear old cache entries (7+ days)
cache.cleanup(days=7)

# Get cache statistics
stats = cache.get_stats()
print(f"Cached businesses: {stats['total']}")
print(f"Cache size: {stats['size_mb']:.1f}MB")
```

## Data Export

### CSV Export

```python
import pandas as pd
from bob.utils.converters import to_dataframe

# Extract multiple businesses
results = [extractor.extract_business(q) for q in queries]

# Convert to DataFrame
df = to_dataframe(results)

# Export to CSV
df.to_csv('businesses.csv', index=False)
```

### JSON Export

```python
import json

# Single extraction
result = extractor.extract_business(query)

if result['success']:
    data = {
        'name': result['business'].name,
        'phone': result['business'].phone,
        'address': result['business'].address,
        'rating': result['business'].rating,
        'quality_score': result['business'].data_quality_score
    }
    
    with open('business.json', 'w') as f:
        json.dump(data, f, indent=2)
```

## Configuration

### ExtractorConfig

```python
from bob.config import ExtractorConfig

config = ExtractorConfig(
    headless=True,
    timeout=30,
    block_resources=True,
    disable_images=False,
    user_agent="Custom User Agent",
    proxy_config=None
)

extractor = PlaywrightExtractorOptimized(config=config)
```

## Utility Functions

### Place ID Utilities

```python
from bob.utils.place_id import extract_place_id, validate_place_id

# Extract place ID from URL
place_id = extract_place_id(google_maps_url)

# Validate place ID format
is_valid = validate_place_id(place_id)
```

### Image Processing

```python
from bob.utils.images import optimize_image, batch_download_images

# Download and optimize images
images = batch_download_images(urls, max_size_mb=5)
```

## Error Handling

```python
from bob.exceptions import ExtractionError, ConfigurationError

try:
    result = extractor.extract_business(query)
except ExtractionError as e:
    print(f"Extraction failed: {e}")
except ConfigurationError as e:
    print(f"Config error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Performance Tuning

### Optimize for Speed

```python
extractor = PlaywrightExtractorOptimized(
    headless=True,
    use_cache=True,             # Use cache for speed
    block_resources=True        # Block images/css/fonts
)
```

### Optimize for Accuracy

```python
extractor = PlaywrightExtractorOptimized(
    headless=False,             # Visual verification
    include_reviews=True,       # Get review data
    max_reviews=10              # Full review parsing
)
```

### Optimize for Memory

```python
extractor = HybridExtractorOptimized(
    memory_optimized=True,
    max_concurrent=1,
    cleanup_delay=3
)
```

## Statistics & Monitoring

```python
# Get extractor statistics
stats = extractor.get_stats()
print(f"Total extractions: {stats['total_extractions']}")
print(f"Success rate: {stats['success_rate']}%")
print(f"Average time: {stats['avg_time_seconds']:.1f}s")
print(f"Peak memory: {stats['peak_memory_mb']:.1f}MB")
```

## Examples

See `examples/` folder for complete working examples:
- `1_basic_extraction.py` - Single business extraction
- `2_batch_processing.py` - Processing multiple businesses
- `3_advanced_configuration.py` - Custom configuration
- `4_cache_management.py` - Cache operations
- `5_integration_with_crm.py` - CRM export

---

For more help, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md) or open an issue on GitHub.
