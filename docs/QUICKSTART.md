# Quick Start Guide - BOB Google Maps

Get started extracting business data in 5 minutes.

## Installation

```bash
git clone https://github.com/div197/bob-google-maps.git
cd bob-google-maps
python3 -m venv venv && source venv/bin/activate
pip install -e .
```

## Your First Extraction (30 seconds)

```python
from bob import PlaywrightExtractorOptimized

# Create extractor
extractor = PlaywrightExtractorOptimized()

# Extract business data
result = extractor.extract_business("Starbucks Times Square New York")

# Access the data
if result['success']:
    business = result['business']
    print(f"Name: {business.name}")
    print(f"Phone: {business.phone}")
    print(f"Address: {business.address}")
    print(f"Rating: {business.rating}")
    print(f"Quality: {business.data_quality_score}/100")
else:
    print(f"Error: {result['error']}")
```

## Common Use Cases

### 1. Batch Processing (50+ businesses)

```python
from bob.utils.batch_processor import BatchProcessor

processor = BatchProcessor(headless=True, max_concurrent=3)

businesses = [
    "Starbucks Times Square",
    "Apple Store Fifth Avenue",
    "Google NYC Office",
    # ... add more
]

results = processor.process_batch_with_retry(businesses, max_retries=1)
print(f"Processed {len(results)} businesses")
```

### 2. With Caching

```python
extractor = PlaywrightExtractorOptimized(use_cache=True)

# First run: extracts from Google Maps (10 seconds)
result1 = extractor.extract_business("Starbucks")

# Second run: returns from cache (0.1 seconds)
result2 = extractor.extract_business("Starbucks")
```

### 3. Export to CSV

```python
import pandas as pd

results = [
    extractor.extract_business(name)
    for name in ["Starbucks", "Apple", "Google"]
]

# Convert to DataFrame
data = []
for r in results:
    if r['success']:
        b = r['business']
        data.append({
            'name': b.name,
            'phone': b.phone,
            'address': b.address,
            'rating': b.rating
        })

df = pd.DataFrame(data)
df.to_csv('businesses.csv', index=False)
print("✅ Exported to businesses.csv")
```

### 4. With Error Handling

```python
from bob import PlaywrightExtractorOptimized

extractor = PlaywrightExtractorOptimized()

try:
    result = extractor.extract_business("Starbucks")
    
    if not result['success']:
        print(f"Extraction failed: {result['error']}")
    else:
        business = result['business']
        
        # Validate data quality
        if business.data_quality_score < 70:
            print("⚠️ Low quality data")
        else:
            print("✅ High quality data extracted")
            
except Exception as e:
    print(f"Error: {e}")
```

## Configuration Options

### Headless Mode
```python
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
