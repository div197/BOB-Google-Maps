# Advanced Usage

## Rate Limiting

BOB includes sophisticated rate limiting to prevent overwhelming target servers:

```python
from bob_core.rate_limiter import AdaptiveRateLimiter, DomainRateLimiter

# Adaptive rate limiter adjusts based on response times
limiter = AdaptiveRateLimiter(
    initial_delay=1.0,
    min_delay=0.5,
    max_delay=10.0
)

# Use in scraping loop
for url in urls:
    limiter.wait()
    result = scraper.scrape(url)
    
    if result["success"]:
        limiter.report_success()
    else:
        limiter.report_error("timeout")
```

## Configuration Management

Persistent configuration for consistent behavior:

```python
from bob_core.config import load_config, update_config

# Load current config
config = load_config()

# Update settings
config = update_config(
    default_backend="playwright",
    default_workers=8,
    enable_sentiment=True
)
```

## Logging Configuration

Centralized logging for debugging and monitoring:

```python
from bob_core.logging_config import setup_logging, setup_scraper_logging

# Basic logging setup
logger = setup_logging(level="DEBUG", log_file="scraper.log")

# Scraping session logging
session_logger = setup_scraper_logging(
    output_dir="output",
    session_id="batch_001"
)
```

## Data Export Formats

Export scraped data to various formats:

```python
from bob_core.export import export_data

# Export to CSV with flattened structure
export_data(results, "output.csv", format="csv")

# Export to Excel with multiple sheets
export_data(results, "output.xlsx", format="excel", sheet_name="Businesses")

# Auto-detect format from extension
export_data(results, "output.json")  # JSON format
```

## Analytics and Business Intelligence

Extract insights from scraped data:

```python
from bob_core.analytics import BusinessAnalyzer, MarketAnalyzer, ReviewAnalyzer

# Single business analysis
analyzer = BusinessAnalyzer(business_data)
score = analyzer.overall_score()
print(f"Business grade: {score['grade']}")

# Market analysis for multiple businesses
market_analyzer = MarketAnalyzer(businesses_list)
opportunities = market_analyzer.market_opportunities()

# Review sentiment analysis
review_analyzer = ReviewAnalyzer(reviews)
sentiment = review_analyzer.sentiment_analysis()
```

## Backend Selection

Choose the optimal scraping backend:

```python
from bob_core.scraper import GoogleMapsScraper

# Auto-select best available backend
scraper = GoogleMapsScraper(backend="auto")

# Force specific backend
playwright_scraper = GoogleMapsScraper(backend="playwright")
selenium_scraper = GoogleMapsScraper(backend="selenium")
```

## Batch Processing with Progress Tracking

Process large datasets efficiently:

```python
from bob_core.batch import batch_scrape

urls = ["https://maps.google.com/?q=restaurant&hl=en", ...]

# Batch scrape with progress bar
results = batch_scrape(
    urls,
    max_workers=4,
    show_progress=True
)
```

## Error Handling and Retry Logic

Robust error handling for production use:

```python
from bob_core.models import ScrapeResult, ErrorLevel

def robust_scrape(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = scraper.scrape(url)
            if result["success"]:
                return result
        except Exception as e:
            if attempt == max_retries - 1:
                return {
                    "url": url,
                    "success": False,
                    "error_message": str(e),
                    "error_level": ErrorLevel.ERROR
                }
            time.sleep(2 ** attempt)  # Exponential backoff
```

## Custom Data Validation

Use Pydantic models for data validation:

```python
from bob_core.models import BusinessInfo, Review, ScrapeResult

# Validate business data
try:
    business = BusinessInfo(
        name="Test Restaurant",
        rating="4.5 stars",
        category="Restaurant"
    )
    print(f"Valid business: {business.name}")
except ValidationError as e:
    print(f"Validation error: {e}")
```

## Performance Optimization

Tips for optimal performance:

1. **Backend Selection**: Playwright is generally faster than Selenium
2. **Concurrency**: Start with 4 workers, adjust based on system performance
3. **Rate Limiting**: Use adaptive rate limiting for large-scale scraping
4. **Caching**: Cache results to avoid re-scraping the same URLs
5. **Monitoring**: Use logging to track performance and errors

## Production Deployment

Best practices for production use:

1. **Configuration**: Use environment variables for sensitive settings
2. **Logging**: Enable file logging with rotation
3. **Monitoring**: Track success rates and performance metrics
4. **Error Handling**: Implement comprehensive retry logic
5. **Rate Limiting**: Respect target server limits
6. **Data Storage**: Use appropriate storage backends for scale 