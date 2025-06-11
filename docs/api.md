# Python API Reference

## Core Scraper

```python
from bob_core.scraper import GoogleMapsScraper

# Auto-select best backend (Playwright preferred)
scraper = GoogleMapsScraper()
result = scraper.scrape("https://maps.google.com/?q=restaurant&hl=en")

# Force specific backend
scraper = GoogleMapsScraper(backend="playwright")
scraper = GoogleMapsScraper(backend="selenium")
```

## Batch Processing

```python
from bob_core.batch import batch_scrape

urls = ["https://maps.google.com/?q=cafe&hl=en", ...]
results = batch_scrape(urls, max_workers=4, show_progress=True)
```

## Analytics

```python
from bob_core.analytics import BusinessAnalyzer, ReviewAnalyzer, MarketAnalyzer

# Single business analysis
analyzer = BusinessAnalyzer(scrape_result)
score = analyzer.overall_score()
print(f"Business grade: {score['grade']}")

# Review sentiment analysis
review_analyzer = ReviewAnalyzer(scrape_result["reviews"])
sentiment = review_analyzer.sentiment_analysis()
print(f"Overall sentiment: {sentiment['overall_sentiment']}")

# Market analysis across multiple businesses
market_analyzer = MarketAnalyzer(multiple_results)
opportunities = market_analyzer.market_opportunities()
```

## Data Models

```python
from bob_core.models import ScrapeResult, BusinessInfo, Review

# Validate scraped data
result = ScrapeResult(**raw_data)
print(f"Scraped {result.reviews_count} reviews")
``` 