# 🔱 BOB Google Maps - Usage Examples

This directory contains comprehensive examples demonstrating how to use BOB Google Maps Extractor for various use cases.

## 📚 Available Examples

### Example 1: Basic Extraction
**File:** `01_basic_extraction.py`
**Description:** Simplest way to extract a single business
**Key Features:**
- Basic HybridExtractor usage
- Single business extraction
- Display all extracted fields
- Success/failure handling

**Run:**
```bash
python examples/01_basic_extraction.py
```

**What You'll Learn:**
- How to create an extractor
- How to extract a business
- How to access extracted data
- How to check extraction status

---

### Example 2: Extract with Reviews
**File:** `02_with_reviews.py`
**Description:** Extract business data including customer reviews
**Key Features:**
- Review extraction
- Reviewer information
- Rating and review text
- Review photos

**Run:**
```bash
python examples/02_with_reviews.py
```

**What You'll Learn:**
- How to enable review extraction
- How to limit number of reviews
- How to access review data
- How to display review information

---

### Example 3: Batch Extraction
**File:** `03_batch_extraction.py`
**Description:** Extract multiple businesses efficiently
**Key Features:**
- Batch processing
- Concurrent extraction
- Progress tracking
- Results aggregation
- JSON export

**Run:**
```bash
python examples/03_batch_extraction.py
```

**What You'll Learn:**
- How to use BatchProcessor
- How to process multiple businesses
- How to handle batch results
- How to export batch data
- Performance optimization

---

### Example 4: Using Cache
**File:** `04_using_cache.py`
**Description:** Leverage intelligent caching for faster re-queries
**Key Features:**
- Cache hit vs miss comparison
- Performance benchmarking
- Force fresh extraction
- Cache bypass

**Run:**
```bash
python examples/04_using_cache.py
```

**What You'll Learn:**
- How caching works
- Performance improvement with cache
- How to bypass cache
- When to use cache

---

### Example 5: Export Formats
**File:** `05_export_formats.py`
**Description:** Export data to various formats (JSON, CSV, CRM)
**Key Features:**
- JSON export (detailed)
- CSV export (basic)
- CRM format export (HubSpot style)
- Multiple export formats

**Run:**
```bash
python examples/05_export_formats.py
```

**What You'll Learn:**
- How to export to JSON
- How to export to CSV
- How to create CRM-friendly formats
- How to structure export data

---

### Example 6: Engine Selection
**File:** `06_engine_selection.py`
**Description:** Compare Playwright, Selenium, and Hybrid engines
**Key Features:**
- Engine comparison
- Performance benchmarking
- Quality comparison
- Recommendation system

**Run:**
```bash
python examples/06_engine_selection.py
```

**What You'll Learn:**
- Differences between engines
- When to use each engine
- Performance trade-offs
- Best practices for engine selection

---

## 🚀 Quick Start

### Prerequisites

1. **Install BOB Google Maps:**
   ```bash
   pip install -e .
   ```

2. **Verify Installation:**
   ```bash
   python -c "from bob import HybridExtractor; print('✅ BOB installed successfully!')"
   ```

### Running Examples

All examples can be run directly from the command line:

```bash
# Run basic example
python examples/01_basic_extraction.py

# Run batch example
python examples/03_batch_extraction.py

# Run all examples
for example in examples/*.py; do python "$example"; done
```

---

## 📋 Example Use Cases

### Use Case 1: Lead Generation for Sales
**Recommended Examples:** 3 (Batch), 5 (Export)
**Scenario:** Extract 100+ businesses for sales outreach
**Workflow:**
1. Use batch extraction with list of businesses
2. Export to CSV for CRM import
3. Use email extraction for outreach

---

### Use Case 2: Competitive Analysis
**Recommended Examples:** 2 (Reviews), 4 (Cache), 5 (Export)
**Scenario:** Analyze competitors including reviews
**Workflow:**
1. Extract competitor data with reviews
2. Use cache for repeated analysis
3. Export to JSON for detailed analysis

---

### Use Case 3: Market Research
**Recommended Examples:** 3 (Batch), 6 (Engines)
**Scenario:** Research businesses in specific category/location
**Workflow:**
1. Use batch processing for multiple businesses
2. Select appropriate engine based on scale
3. Aggregate data for insights

---

### Use Case 4: Data Enrichment
**Recommended Examples:** 1 (Basic), 5 (Export)
**Scenario:** Enrich existing business database
**Workflow:**
1. Extract individual businesses
2. Export in CRM-friendly format
3. Import to existing database

---

## 🎯 Best Practices

### Performance Optimization

1. **Use Cache Effectively:**
   ```python
   extractor = HybridExtractor(
       use_cache=True,
       cache_expiration_hours=24
   )
   ```

2. **Batch Processing:**
   ```python
   processor = BatchProcessor(
       max_concurrent=5,  # Adjust based on system
       headless=True      # Faster in headless mode
   )
   ```

3. **Resource Management:**
   ```python
   # Use context manager for automatic cleanup
   with HybridExtractor() as extractor:
       result = extractor.extract_business("query")
   ```

### Error Handling

```python
try:
    result = extractor.extract_business("Business Name")
    if not result.get('success'):
        print(f"Extraction failed: {result.get('error')}")
except Exception as e:
    print(f"Unexpected error: {str(e)}")
```

### Data Validation

```python
business = result.get('business')
if business:
    # Validate critical fields
    has_contact = business.phone or business.emails or business.website
    has_location = business.latitude and business.longitude
    quality_threshold = business.data_quality_score >= 70

    if not has_contact:
        print("⚠️ Warning: No contact information found")
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```bash
# Browser Configuration
BOB_HEADLESS=true
CHROME_BIN=/usr/bin/google-chrome

# Cache Configuration
BOB_CACHE_PATH=./bob_cache_ultimate.db
BOB_CACHE_EXPIRY_HOURS=24

# Performance Settings
BOB_TIMEOUT=30
BOB_MAX_CONCURRENT=10
```

### Configuration File

Modify `config.yaml` for advanced settings:

```yaml
extraction:
  default_engine: "hybrid"
  include_reviews: false
  max_reviews: 10
  timeout: 30

cache:
  enabled: true
  expiration_hours: 24
  max_size_mb: 500

logging:
  level: "INFO"
  file: "logs/bob.log"
```

---

## 📊 Example Output

### Successful Extraction
```
🔱 BOB Google Maps - Basic Extraction Example
============================================================

📍 Searching for: Starbucks Reserve Roastery Seattle
⏳ Extracting data...

✅ Extraction Successful!
────────────────────────────────────────────────────────────
📛 Name: Starbucks Reserve Roastery
📞 Phone: (206) 624-0173
📧 Emails: contact@starbucks.com
🌐 Website: https://www.starbucksreserve.com
📍 Address: 1124 Pike St, Seattle, WA 98101
⭐ Rating: 4.5 (2,847 reviews)
🏷️ Category: Coffee roastery
📊 Quality Score: 94/100
⏱️ Extraction Time: 12.34s
🔧 Method: playwright
🗺️ Coordinates: 47.6101, -122.3331
🆔 Place ID: ChIJNU...
```

---

## 🆘 Troubleshooting

### Common Issues

**1. Import Error:**
```bash
# Solution: Install BOB package
pip install -e .
```

**2. Browser Not Found:**
```bash
# Solution: Install Chrome/Chromium
# Ubuntu/Debian:
sudo apt install chromium-browser

# macOS:
brew install chromium
```

**3. Extraction Timeout:**
```python
# Solution: Increase timeout
extractor = HybridExtractor(timeout=60)
```

**4. No Results Found:**
```python
# Solution: Try different query formats
queries = [
    "Starbucks Seattle",
    "Starbucks, Seattle, WA",
    "Starbucks Reserve Roastery Seattle"
]
```

---

## 📚 Additional Resources

- **Main Documentation:** [CLAUDE.md](../CLAUDE.md)
- **API Reference:** [docs/technical/](../docs/technical/)
- **Troubleshooting Guide:** [docs/guides/](../docs/guides/)
- **Contributing:** [CONTRIBUTING.md](../CONTRIBUTING.md)

---

## 💡 Tips & Tricks

### Tip 1: Query Optimization
```python
# ❌ Too generic
"Starbucks"

# ✅ Specific with location
"Starbucks Reserve Roastery Seattle"

# ✅ Include address for uniqueness
"Starbucks, 1124 Pike St, Seattle"
```

### Tip 2: Performance Monitoring
```python
import time

start = time.time()
result = extractor.extract_business("query")
print(f"Time taken: {time.time() - start:.2f}s")
```

### Tip 3: Quality Filtering
```python
# Filter by quality score
results = batch_process(queries)
high_quality = [
    r for r in results
    if r.get('business', {}).get('data_quality_score', 0) >= 80
]
```

---

## 🎓 Learning Path

**Beginner:** Start with Examples 1, 2
**Intermediate:** Examples 3, 4, 5
**Advanced:** Example 6, Custom implementations

---

## 🔄 Contributing

Found a useful example to add? See [CONTRIBUTING.md](../CONTRIBUTING.md)

---

## 📄 License

BOB Google Maps is released under the MIT License. See [LICENSE](../LICENSE) for details.

---

**🔱 JAI SHREE KRISHNA!**
*Built with Nishkaam Karma Yoga principles - Selfless action for maximum efficiency*

---

**Version:** 4.2.0
**Last Updated:** November 14, 2025
**Status:** Production-Ready ✅
