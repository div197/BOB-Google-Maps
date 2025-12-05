# API Reference - BOB Google Maps v4.3.0# API Reference - BOB Google Maps



Complete API documentation for BOB Google Maps extractors.Complete API documentation for all extractors and utilities.



## Quick Reference## Core Extractors



| Class | Type | Method | Use Case |### PlaywrightExtractorOptimized

|-------|------|--------|----------|

| `HybridExtractorOptimized` | Sync | `extract_business()` | **Recommended** - Caching + fallback |Fast, JavaScript-enabled extraction engine.

| `PlaywrightExtractorOptimized` | Async | `extract_business_optimized()` | Fast extraction |

| `SeleniumExtractorOptimized` | Sync | `extract_business_optimized()` | Fallback engine |```python

from bob import PlaywrightExtractorOptimized

---

extractor = PlaywrightExtractorOptimized(

## HybridExtractorOptimized (Recommended)    headless=True,              # Run browser in background

    timeout=30,                 # Timeout in seconds

The recommended extractor for most use cases. Provides caching and automatic fallback.    use_cache=True,             # Use SQLite cache

    memory_optimized=False      # Memory optimization mode

### Constructor)



```python# Extract single business

from bob import HybridExtractorOptimizedresult = extractor.extract_business(

    query,                      # Business name/location

extractor = HybridExtractorOptimized(    include_reviews=False,      # Include review data

    prefer_playwright=True,     # Use Playwright as primary engine    max_reviews=0              # Max reviews to fetch

    memory_optimized=True,      # Enable memory optimization)

    use_cache=True              # Enable SQLite caching

)# Check result

```if result['success']:

    business = result['business']

**Parameters:**    # Access fields: name, phone, address, rating, etc.

- `prefer_playwright` (bool): Use Playwright first, default `True`else:

- `memory_optimized` (bool): Enable memory optimization, default `True`    error = result['error']

- `use_cache` (bool): Enable SQLite caching, default `True`    print(f"Extraction failed: {error}")

```

### Methods

### SeleniumExtractorOptimized

#### `extract_business(url, include_reviews=True, max_reviews=10)`

Reliable fallback engine with undetected-chromedriver.

Extract a single business.

```python

```pythonfrom bob import SeleniumExtractorOptimized

result = extractor.extract_business(

    "Starbucks Times Square NYC",extractor = SeleniumExtractorOptimized(

    include_reviews=True,    headless=True,

    max_reviews=5    stealth_mode=True,          # Use undetected-chromedriver

)    timeout=30

```)



**Parameters:**result = extractor.extract_business(query)

- `url` (str): Business name or Google Maps URL```

- `include_reviews` (bool): Extract reviews, default `True`

- `max_reviews` (int): Maximum reviews to extract, default `10`### HybridExtractorOptimized



**Returns:** `dict` - Extraction result (see Result Structure below)Memory-optimized hybrid approach.



#### `extract_multiple(urls, include_reviews=True, max_reviews=10)````python

from bob import HybridExtractorOptimized

Extract multiple businesses.

extractor = HybridExtractorOptimized(

```python    memory_optimized=True,

results = extractor.extract_multiple(    max_concurrent=1,

    ["Starbucks NYC", "Apple Store NYC"],    cleanup_delay=3

    include_reviews=False)

)

```result = extractor.extract_business(query)

```

#### `get_stats()`

## Business Data Model

Get extraction statistics.

### Business Object

```python

stats = extractor.get_stats()```python

# {@dataclass

#     'total_requests': 5,class Business:

#     'playwright_success': 4,    # Core Fields

#     'selenium_success': 1,    name: Optional[str]                 # Business name

#     'failures': 0,    phone: Optional[str]                # Phone number

#     'cache_hits': 2    address: Optional[str]              # Full address

# }    

```    # Contact & Web

    emails: List[str]                   # Email addresses

---    website: Optional[str]              # Website URL

    

## PlaywrightExtractorOptimized    # Location

    latitude: Optional[float]           # GPS latitude

Fast, async extraction engine. Used internally by HybridExtractor.    longitude: Optional[float]          # GPS longitude

    plus_code: Optional[str]            # Google Plus Code

### Constructor    

    # Business Info

```python    category: Optional[str]             # Business category

from bob import PlaywrightExtractorOptimized    rating: Optional[float]             # Star rating (0-5)

    review_count: Optional[int]         # Number of reviews

extractor = PlaywrightExtractorOptimized(    

    headless=True,           # Run browser headlessly    # Operations

    memory_optimized=True    # Enable memory optimization    hours: Optional[str]                # Operating hours

)    current_status: Optional[str]       # Open/Closed status

```    

    # Metadata

### Methods    data_quality_score: int             # Quality 0-100

    extraction_time_seconds: float      # Extraction duration

#### `async extract_business_optimized(url, include_reviews=True, max_reviews=10)`    extracted_at: datetime              # Extraction timestamp

    

**Note:** This is an async method - use with `asyncio`.    # Additional

    place_id: Optional[str]             # Google Place ID

```python    cid: Optional[int]                  # Business CID

import asyncio    photos: List[str]                   # Photo URLs

from bob import PlaywrightExtractorOptimized    reviews: List[Review]               # Review objects

```

async def main():

    extractor = PlaywrightExtractorOptimized(headless=True)### Review Object

    

    result = await extractor.extract_business_optimized(```python

        "Starbucks Times Square NYC",@dataclass

        include_reviews=True,class Review:

        max_reviews=5    reviewer: str                       # Reviewer name

    )    rating: str                         # Review rating

        text: str                           # Review text

    if result['success']:    date: str                           # Review date

        print(f"Name: {result['name']}")    review_index: int                   # Review position

```

asyncio.run(main())

```## Batch Processing



**Parameters:**### BatchProcessor

- `url` (str): Business name or Google Maps URL

- `include_reviews` (bool): Extract reviews, default `True`Process multiple businesses efficiently.

- `max_reviews` (int): Maximum reviews, default `10`

```python

**Returns:** `dict` - Extraction resultfrom bob.utils.batch_processor import BatchProcessor



---processor = BatchProcessor(

    headless=True,

## SeleniumExtractorOptimized    include_reviews=False,

    max_reviews=0,

Fallback extraction engine using undetected-chromedriver.    max_concurrent=5

)

### Constructor

# Process businesses

```pythonresults = processor.process_batch_with_retry(

from bob import SeleniumExtractorOptimized    businesses=['Business1', 'Business2', ...],

    max_retries=1,

extractor = SeleniumExtractorOptimized(    verbose=True

    headless=True,           # Run browser headlessly)

    memory_optimized=True    # Enable memory optimization

)# Results is a list of extraction results

```for result in results:

    if result['success']:

### Methods        print(f"✅ {result['business'].name}")

    else:

#### `extract_business_optimized(url, include_reviews=True, max_reviews=3)`        print(f"❌ {result['error']}")

```

```python

result = extractor.extract_business_optimized(## Cache Management

    "Starbucks NYC",

    include_reviews=False### CacheManager

)

```Manage SQLite cache for fast repeated queries.



---```python

from bob.cache import CacheManager

## Result Structure

cache = CacheManager()

All extractors return a flat dictionary:

# Get cached business

```pythoncached = cache.get_cached_business("Starbucks Times Square")

{

    # Status# Save to cache

    'success': True,                    # bool - Extraction succeededcache.save_to_cache("Starbucks Times Square", business_data)

    

    # Core Data# Clear old cache entries (7+ days)

    'name': 'Starbucks',                # str - Business namecache.cleanup(days=7)

    'phone': '+1 212-221-7515',         # str - Phone number

    'address': '1500 Broadway...',      # str - Full address# Get cache statistics

    'website': 'https://...',           # str - Website URLstats = cache.get_stats()

    print(f"Cached businesses: {stats['total']}")

    # Business Infoprint(f"Cache size: {stats['size_mb']:.1f}MB")

    'rating': 4.0,                      # float - Star rating (0-5)```

    'reviews_count': 2847,              # int - Number of reviews

    'category': 'Coffee shop',          # str - Business category## Data Export

    

    # Location### CSV Export

    'latitude': 40.75664,               # float - GPS latitude

    'longitude': -73.9906636,           # float - GPS longitude```python

    import pandas as pd

    # Identifiersfrom bob.utils.converters import to_dataframe

    'place_id_hex': '...',              # str - Place ID (hex format)

    'cid': '...',                       # str - Customer ID# Extract multiple businesses

    results = [extractor.extract_business(q) for q in queries]

    # Rich Data

    'images': ['url1', 'url2', ...],    # list - Photo URLs (25-40)# Convert to DataFrame

    'photos': ['url1', 'url2', ...],    # list - Same as imagesdf = to_dataframe(results)

    'reviews': [...],                   # list - Review objects

    # Export to CSV

    # Metadatadf.to_csv('businesses.csv', index=False)

    'quality_score': 95,                # int - Quality score (0-100)```

    'extractor_version': 'Playwright v4.3.0',

    'extraction_time_seconds': 21.3     # float - Time taken### JSON Export

}

``````python

import json

### Error Result

# Single extraction

When extraction fails:result = extractor.extract_business(query)



```pythonif result['success']:

{    data = {

    'success': False,        'name': result['business'].name,

    'error': 'Error message',        'phone': result['business'].phone,

    'tried_methods': ['playwright', 'selenium']        'address': result['business'].address,

}        'rating': result['business'].rating,

```        'quality_score': result['business'].data_quality_score

    }

---    

    with open('business.json', 'w') as f:

## Data Models        json.dump(data, f, indent=2)

```

### Business

## Configuration

The `Business` dataclass (34 fields):

### ExtractorConfig

```python

from bob.models import Business```python

from bob.config import ExtractorConfig

@dataclass

class Business:config = ExtractorConfig(

    # Identification    headless=True,

    place_id: Optional[str]    timeout=30,

    cid: Optional[int]    block_resources=True,

        disable_images=False,

    # Core    user_agent="Custom User Agent",

    name: Optional[str]    proxy_config=None

    phone: Optional[str])

    address: Optional[str]

    emails: List[str]extractor = PlaywrightExtractorOptimized(config=config)

    ```

    # Location

    latitude: Optional[float]## Utility Functions

    longitude: Optional[float]

    plus_code: Optional[str]### Place ID Utilities

    

    # Business Info```python

    category: Optional[str]from bob.utils.place_id import extract_place_id, validate_place_id

    rating: Optional[float]

    review_count: Optional[int]# Extract place ID from URL

    website: Optional[str]place_id = extract_place_id(google_maps_url)

    hours: Optional[str]

    # Validate place ID format

    # Rich Datais_valid = validate_place_id(place_id)

    photos: List[str]```

    reviews: List[Any]

    ### Image Processing

    # Metadata

    data_quality_score: int```python

    extraction_method: strfrom bob.utils.images import optimize_image, batch_download_images

    extraction_time_seconds: Optional[float]

    extractor_version: str# Download and optimize images

```images = batch_download_images(urls, max_size_mb=5)

```

### Review

## Error Handling

```python

from bob.models import Review```python

from bob.exceptions import ExtractionError, ConfigurationError

@dataclass

class Review:try:

    author_name: Optional[str]    result = extractor.extract_business(query)

    author_url: Optional[str]except ExtractionError as e:

    rating: Optional[float]    print(f"Extraction failed: {e}")

    text: Optional[str]except ConfigurationError as e:

    time_description: Optional[str]    print(f"Config error: {e}")

    owner_response: Optional[str]except Exception as e:

```    print(f"Unexpected error: {e}")

```

---

## Performance Tuning

## Configuration

### Optimize for Speed

### Environment Variables

```python

```bashextractor = PlaywrightExtractorOptimized(

BOB_HEADLESS=true          # Run browsers headlessly    headless=True,

BOB_TIMEOUT=60             # Page timeout (seconds)    use_cache=True,             # Use cache for speed

BOB_MAX_RETRIES=3          # Retry attempts    block_resources=True        # Block images/css/fonts

BOB_SELENIUM_ENABLED=true  # Enable Selenium fallback)

``````



### ExtractorConfig### Optimize for Accuracy



```python```python

from bob.config import ExtractorConfig, DEFAULT_EXTRACTOR_CONFIGextractor = PlaywrightExtractorOptimized(

    headless=False,             # Visual verification

config = ExtractorConfig(    include_reviews=True,       # Get review data

    headless=True,    max_reviews=10              # Full review parsing

    timeout=60,)

    max_retries=3,```

    selenium_enabled=True

)### Optimize for Memory

```

```python

---extractor = HybridExtractorOptimized(

    memory_optimized=True,

## Caching    max_concurrent=1,

    cleanup_delay=3

The `HybridExtractorOptimized` uses SQLite caching:)

```

```python

# Enable caching## Statistics & Monitoring

extractor = HybridExtractorOptimized(use_cache=True)

```python

# First call: ~15 seconds (live extraction)# Get extractor statistics

result1 = extractor.extract_business("Starbucks NYC")stats = extractor.get_stats()

print(f"Total extractions: {stats['total_extractions']}")

# Second call: ~0.01 seconds (from cache)print(f"Success rate: {stats['success_rate']}%")

result2 = extractor.extract_business("Starbucks NYC")print(f"Average time: {stats['avg_time_seconds']:.1f}s")

```print(f"Peak memory: {stats['peak_memory_mb']:.1f}MB")

```

### Cache Location

## Examples

Default: `bob_cache_ultimate.db` in current directory

See `examples/` folder for complete working examples:

---- `1_basic_extraction.py` - Single business extraction

- `2_batch_processing.py` - Processing multiple businesses

## Error Handling- `3_advanced_configuration.py` - Custom configuration

- `4_cache_management.py` - Cache operations

```python- `5_integration_with_crm.py` - CRM export

from bob import HybridExtractorOptimized

from bob.exceptions import BOBException, ExtractionError---



extractor = HybridExtractorOptimized()For more help, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md) or open an issue on GitHub.


try:
    result = extractor.extract_business("Some Business")
    if not result['success']:
        print(f"Extraction failed: {result.get('error')}")
except ExtractionError as e:
    print(f"Extraction error: {e}")
except BOBException as e:
    print(f"BOB error: {e}")
```

---

**Version:** 4.3.0 | December 5, 2025
