# Quick Start Guide - BOB Google Maps v4.3.0# Quick Start Guide - BOB Google Maps



Get extracting in 2 minutes.Get started extracting business data in 5 minutes.



## Installation## Installation



### Option 1: One-Click Setup (Recommended)```bash

git clone https://github.com/div197/bob-google-maps.git

```bashcd bob-google-maps

git clone https://github.com/div197/BOB-Google-Maps.gitpython3 -m venv venv && source venv/bin/activate

cd BOB-Google-Mapspip install -e .

chmod +x setup.sh && ./setup.sh```

source .venv/bin/activate

```## Your First Extraction (30 seconds)



### Option 2: Manual Setup```python

from bob import PlaywrightExtractorOptimized

```bash

git clone https://github.com/div197/BOB-Google-Maps.git# Create extractor

cd BOB-Google-Mapsextractor = PlaywrightExtractorOptimized()

python3 -m venv .venv

source .venv/bin/activate# Extract business data

pip install -r requirements.txtresult = extractor.extract_business("Starbucks Times Square New York")

playwright install chromium

```# Access the data

if result['success']:

## First Extraction    business = result['business']

    print(f"Name: {business.name}")

### Command Line (Fastest)    print(f"Phone: {business.phone}")

    print(f"Address: {business.address}")

```bash    print(f"Rating: {business.rating}")

python -m bob "Starbucks Times Square NYC"    print(f"Quality: {business.data_quality_score}/100")

```else:

    print(f"Error: {result['error']}")

### Python - Hybrid Extractor (Recommended)```



```python## Common Use Cases

from bob import HybridExtractorOptimized

### 1. Batch Processing (50+ businesses)

extractor = HybridExtractorOptimized(use_cache=True)

result = extractor.extract_business("Starbucks Times Square NYC")```python

from bob.utils.batch_processor import BatchProcessor

if result['success']:

    print(f"Name: {result['name']}")processor = BatchProcessor(headless=True, max_concurrent=3)

    print(f"Phone: {result['phone']}")

    print(f"Address: {result['address']}")businesses = [

    print(f"Rating: {result['rating']}")    "Starbucks Times Square",

    print(f"Quality: {result['quality_score']}/100")    "Apple Store Fifth Avenue",

```    "Google NYC Office",

    # ... add more

### Python - Async Playwright]



```pythonresults = processor.process_batch_with_retry(businesses, max_retries=1)

import asyncioprint(f"Processed {len(results)} businesses")

from bob import PlaywrightExtractorOptimized```



async def main():### 2. With Caching

    extractor = PlaywrightExtractorOptimized(headless=True)

    result = await extractor.extract_business_optimized(```python

        "Starbucks Times Square NYC",extractor = PlaywrightExtractorOptimized(use_cache=True)

        include_reviews=False

    )# First run: extracts from Google Maps (10 seconds)

    print(f"Name: {result['name']}")result1 = extractor.extract_business("Starbucks")



asyncio.run(main())# Second run: returns from cache (0.1 seconds)

```result2 = extractor.extract_business("Starbucks")

```

## Understanding Results

### 3. Export to CSV

Results are flat dictionaries:

```python

```pythonimport pandas as pd

result = {

    'success': True,results = [

    'name': 'Starbucks',    extractor.extract_business(name)

    'phone': '+1 212-221-7515',    for name in ["Starbucks", "Apple", "Google"]

    'address': '1500 Broadway, New York, NY 10036',]

    'website': 'https://starbucks.com/...',

    'rating': 4.0,# Convert to DataFrame

    'reviews_count': 2847,data = []

    'category': 'Coffee shop',for r in results:

    'latitude': 40.75664,    if r['success']:

    'longitude': -73.9906636,        b = r['business']

    'quality_score': 95,        data.append({

    'extraction_time_seconds': 21.3            'name': b.name,

}            'phone': b.phone,

```            'address': b.address,

            'rating': b.rating

Access fields directly: `result['name']`, `result['phone']`, etc.        })



## Common Tasksdf = pd.DataFrame(data)

df.to_csv('businesses.csv', index=False)

### Save to JSONprint("✅ Exported to businesses.csv")

```

```bash

python -m bob "Empire State Building" --output result.json### 4. With Error Handling

```

```python

### Skip Cache (Fresh Extraction)from bob import PlaywrightExtractorOptimized



```bashextractor = PlaywrightExtractorOptimized()

python -m bob "Some Business" --fresh

```try:

    result = extractor.extract_business("Starbucks")

### With Reviews    

    if not result['success']:

```python        print(f"Extraction failed: {result['error']}")

result = extractor.extract_business(    else:

    "Taj Mahal Palace Mumbai",        business = result['business']

    include_reviews=True,        

    max_reviews=10        # Validate data quality

)        if business.data_quality_score < 70:

reviews = result.get('reviews', [])            print("⚠️ Low quality data")

```        else:

            print("✅ High quality data extracted")

## Next Steps            

except Exception as e:

- [API Reference](API_REFERENCE.md) - Full API documentation    print(f"Error: {e}")

- [Examples](../examples/) - Working code examples```

- [Architecture](ARCHITECTURE.md) - How it works

## Configuration Options

---

### Headless Mode

**v4.3.0** | December 5, 2025```python

# Run browser in background (faster)
extractor = PlaywrightExtractorOptimized(headless=True)

# Run browser visibly (debugging)
extractor = PlaywrightExtractorOptimized(headless=False)
```

### Memory Optimization
```python
# Use memory-optimized version
from bob import HybridExtractorOptimized

extractor = HybridExtractorOptimized(
    memory_optimized=True,
    max_concurrent=1
)
```

### Custom Timeouts
```python
extractor = PlaywrightExtractorOptimized(timeout=60)
```

## Data Fields Available

Every extraction provides:

```python
business.name           # Business name
business.phone          # Phone number
business.address        # Full address
business.rating         # Star rating (0-5)
business.review_count   # Number of reviews
business.website        # Website URL
business.category       # Business category
business.emails         # Email addresses
business.latitude       # GPS latitude
business.longitude      # GPS longitude
business.data_quality_score  # Quality score (0-100)
```

## Testing Your Setup

```python
from bob import PlaywrightExtractorOptimized

def test_setup():
    """Verify installation works correctly"""
    extractor = PlaywrightExtractorOptimized()
    
    # Test real extraction
    result = extractor.extract_business("Google New York")
    
    assert result['success'], "Extraction failed"
    assert result['business'].name, "No business name"
    assert result['business'].data_quality_score > 70, "Low quality"
    
    print("✅ All tests passed - System ready!")

if __name__ == "__main__":
    test_setup()
```

## Troubleshooting

### "Chrome not found"
```bash
# macOS
brew install chromium

# Linux
sudo apt install chromium-browser
```

### "Timeout" errors
Increase timeout and retry:
```python
extractor = PlaywrightExtractorOptimized(timeout=60)
result = extractor.extract_business(query)
```

### "No business link found"
Some businesses don't have direct Google Maps links. Try alternative searches.

## Next Steps

- **Full API Reference:** See [API_REFERENCE.md](API_REFERENCE.md)
- **Architecture:** See [ARCHITECTURE.md](ARCHITECTURE.md)
- **Examples:** See [../examples/](../examples/)
- **Issues:** Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

## Real-World Performance

Tested with 110 businesses across 10 US cities:
- **Success Rate:** 100%
- **Average Quality:** 85.5/100
- **Average Speed:** 7.4 seconds/business
- **Memory Usage:** 64MB peak

---

**You're ready!** Start extracting business data now.
