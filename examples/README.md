# 📚 BOB Google Maps Examples

Usage examples for BOB Google Maps v4.3.0

## Available Examples

| # | File | Description |
|---|------|-------------|
| 1 | `01_basic_extraction.py` | Basic single business extraction |
| 2 | `02_with_reviews.py` | Extract with customer reviews |
| 3 | `03_with_cache.py` | Using HybridExtractor with caching |
| 4 | `04_export_json.py` | Export results to JSON |
| 5 | `05_batch_extraction.py` | Extract multiple businesses sequentially |
| 6 | `06_export_formats.py` | Export to CSV, SQLite, Excel |
| 7 | `07_city_extraction.py` | City-wide category extraction |
| 8 | `08_parallel_extraction.py` | Concurrent extraction for speed |

## Running Examples

```bash
# Activate environment
cd BOB-Google-Maps
source .venv/bin/activate

# Run any example
python examples/01_basic_extraction.py
python examples/05_batch_extraction.py
python examples/08_parallel_extraction.py
```

## Example Categories

### Basic (1-4)
- Single business extraction
- Review extraction
- Caching for repeat queries
- JSON output

### Advanced (5-8)
- Batch processing multiple businesses
- Multiple export formats (CSV, SQLite, Excel)
- City-wide extraction (all restaurants in a city)
- Parallel extraction for speed

## Quick Start

```python
import asyncio
from bob import PlaywrightExtractorOptimized

async def main():
    extractor = PlaywrightExtractorOptimized(headless=True)
    result = await extractor.extract_business_optimized("Starbucks NYC")
    
    if result['success']:
        print(f"Name: {result['name']}")
        print(f"Phone: {result['phone']}")
        print(f"Rating: {result['rating']}")

asyncio.run(main())
```

## Notes

- Examples create an `output/` directory for saved files
- Parallel extraction uses 2 browsers by default (safe)
- City extraction can take time for large categories
- All examples use `headless=True` by default
