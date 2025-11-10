# Troubleshooting Guide - BOB Google Maps

Solutions for common issues and problems.

## Installation Issues

### Python Version Error
**Problem:** `python: command not found` or version mismatch

**Solution:**
```bash
# Check Python version
python3 --version

# Must be 3.8 or higher
# macOS: brew install python@3.10
# Linux: sudo apt install python3.10
# Windows: Download from python.org
```

### Chrome/Chromium Not Found
**Problem:** `Chromium executable not found`

**Solution:**
```bash
# macOS
brew install chromium

# Linux
sudo apt install chromium-browser

# Windows
Download from: https://www.chromium.org/

# Set CHROME_BIN environment variable
export CHROME_BIN=/path/to/chrome
```

### Module Not Found
**Problem:** `ModuleNotFoundError: No module named 'bob'`

**Solution:**
```bash
# Install in development mode
pip install -e .

# Verify installation
python -c "import bob; print('✅ Ready!')"
```

## Extraction Issues

### No Business Found
**Problem:** "No business link found" error

**Solution:**
- Try alternative search query
- Add location details (city, state)
- Search for well-known chains/businesses
- Some businesses may not have Google Maps listings

### Timeout Errors
**Problem:** "Extraction timed out after 30 seconds"

**Solution:**
```python
# Increase timeout
extractor = PlaywrightExtractorOptimized(timeout=60)

# Or use memory-optimized version
from bob import HybridExtractorOptimized
extractor = HybridExtractorOptimized()
```

### Low Quality Scores
**Problem:** Quality score below 70/100

**Possible Causes:**
- Incomplete Google Maps listing
- Missing contact information
- Business name variation
- No reviews/ratings yet

**Solution:**
- Accept partial data (quality score shows completeness)
- Try manual verification
- Use alternative search

### Empty Fields
**Problem:** Some fields return `None`

**Normal Behavior:** Not all fields available for every business
- Phone: 81% of businesses
- Email: ~20% of businesses  
- Hours: ~90% of businesses

**Check:**
```python
if result['success']:
    b = result['business']
    if b.phone:
        print(f"Phone: {b.phone}")
    else:
        print("Phone not available for this business")
```

## Performance Issues

### Out of Memory
**Problem:** Memory usage exceeds available RAM

**Solution:**
```python
# Use memory-optimized extractor
from bob import HybridExtractorOptimized

extractor = HybridExtractorOptimized(
    memory_optimized=True,
    max_concurrent=1
)
```

### Slow Extraction
**Problem:** Taking longer than expected

**Solutions:**
```python
# 1. Use cache for repeated queries
extractor = PlaywrightExtractorOptimized(use_cache=True)

# 2. Disable reviews (faster extraction)
result = extractor.extract_business(query, include_reviews=False)

# 3. Block images for faster loading
from bob.config import ExtractorConfig
config = ExtractorConfig(disable_images=True)
```

### High CPU Usage
**Problem:** Extraction using too much CPU

**Causes:**
- Browser rendering overhead
- Multiple concurrent extractions
- Image loading/processing

**Solution:**
- Reduce max_concurrent to 1
- Run during off-peak hours
- Use headless mode (reduces UI rendering)

## Cache Issues

### Cache Database Corrupted
**Problem:** `sqlite3.DatabaseError: database disk image is malformed`

**Solution:**
```bash
# Delete corrupted cache
rm bob_cache_ultimate.db

# Recreate cache on next extraction
python -c "from bob import PlaywrightExtractorOptimized; e = PlaywrightExtractorOptimized(); e.extract_business('Test')"
```

### Cache Not Working
**Problem:** Cache seems ineffective

**Solution:**
```python
# Verify cache is enabled
extractor = PlaywrightExtractorOptimized(use_cache=True)

# Check cache statistics
from bob.cache import CacheManager
cache = CacheManager()
stats = cache.get_stats()
print(f"Cached businesses: {stats['total']}")
```

### Clear Cache
**Solution:**
```python
from bob.cache import CacheManager

cache = CacheManager()
cache.cleanup(days=0)  # Clear all
cache.cleanup(days=7)  # Clear 7+ days old
```

## Docker Issues

### Container Memory
**Problem:** Docker container out of memory

**Solution:**
```bash
# Increase Docker memory limit
docker run -m 4g bob-google-maps

# Or use docker-compose.yml
version: '3'
services:
  bob:
    build: .
    mem_limit: 4g
```

### Port Binding
**Problem:** `Port already in use`

**Solution:**
```bash
# Use different port
docker run -p 8080:8000 bob-google-maps

# Or find and kill process
lsof -i :8000
kill -9 <PID>
```

## Authentication Issues

### Browser Security
**Problem:** `ERR_BLOCKED_BY_CLIENT` errors

**Solution:**
```python
# Use --disable-web-security flag (already enabled in V4.2)
# This allows Google Maps APIs to work properly
```

## Data Quality Issues

### Inconsistent Results
**Problem:** Same business returns different data each time

**Causes:**
- Google Maps changes data
- Different language/region settings
- Cache stale data

**Solution:**
```python
# Force fresh extraction (bypass cache)
result = extractor.extract_business(query, force_fresh=True)

# Clear cache for this business
cache.clear_specific(query)
```

### Missing Consistency
**Problem:** Phone number present one time, absent another

**Normal:** Google Maps data changes, some fields not always available

**Best Practice:** Check field existence before using
```python
if business.phone:
    use_phone(business.phone)
else:
    print("Phone not available")
```

## Debugging

### Enable Verbose Logging
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('bob')

# Now see detailed extraction logs
```

### Visual Debugging
```python
# Watch browser extraction in real-time
extractor = PlaywrightExtractorOptimized(headless=False)
result = extractor.extract_business(query)
```

### Test Extraction
```python
from bob import PlaywrightExtractorOptimized

def test_extraction():
    extractor = PlaywrightExtractorOptimized()
    result = extractor.extract_business("Starbucks")
    
    assert result['success'], "Extraction failed"
    assert result['business'].name, "Missing name"
    assert result['business'].data_quality_score > 70, "Low quality"
    
    print("✅ Extraction working properly")

test_extraction()
```

## Getting Help

1. **Check Documentation:**
   - [QUICKSTART.md](QUICKSTART.md) - Basic usage
   - [API_REFERENCE.md](API_REFERENCE.md) - Complete API
   - [ARCHITECTURE.md](ARCHITECTURE.md) - System design

2. **Common Issues:**
   - Search existing GitHub issues
   - Check examples/ folder for working code

3. **Report New Issues:**
   - Open GitHub issue with:
     - Error message (exact)
     - Code snippet (minimal)
     - Environment (Python version, OS)
     - Expected vs actual behavior

## System Requirements Verification

```bash
# Check everything
python -c "
import sys
print(f'Python: {sys.version}')
print(f'Platform: {sys.platform}')

try:
    import playwright
    print('✅ Playwright installed')
except:
    print('❌ Playwright missing')

try:
    import bob
    print('✅ BOB installed')
except:
    print('❌ BOB missing')
"
```

---

Still having issues? Check [CONTRIBUTING.md](../CONTRIBUTING.md) for how to get support.
