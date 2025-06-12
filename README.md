# BOB Google Maps v0.5.0

*Build Online Business – Made in 🇮🇳, Made for the World*

BOB Google Maps is an **enterprise-grade**, open-source (MIT) Google Maps scraper that transforms raw location data into actionable business intelligence. Powered by principles of **Niṣkāma Karma Yoga** (selfless, excellence-first action), BOB delivers production-ready performance with zero compromises.

## 🚀 What's New in v0.5.0

- **⚡ Business-Only Mode**: 3.18x faster extraction for business directories
- **🛡️ Enterprise Fault Tolerance**: Circuit breakers, auto-recovery, graceful degradation
- **🎭 Dual Backend Support**: Selenium (reliable) + Playwright (fast)
- **📊 Advanced Analytics**: Market analysis, sentiment scoring, opportunity detection
- **🔧 Production Ready**: Health monitoring, performance tracking, memory management
- **📈 Scalable Architecture**: Batch processing, connection pooling, dead letter queues

## 🎯 Key Features

### **Lightning-Fast Extraction**
- **Business-Only Mode**: Extract just business info in ~18s (vs 56s full)
- **Smart Review Limiting**: Configure max reviews for optimal performance
- **Dual Backend**: Selenium (stable) + Playwright (3x faster for some operations)

### **Enterprise-Grade Reliability**
- **Circuit Breakers**: Auto-failover when services degrade
- **Auto-Recovery**: Self-healing from temporary failures
- **Graceful Degradation**: Partial data when full extraction fails
- **Health Monitoring**: Real-time system status and metrics

### **Business Intelligence**
- **Market Analysis**: Category trends, competitive landscape
- **Sentiment Analysis**: Review sentiment scoring with TextBlob
- **Opportunity Detection**: Identify market gaps and high-potential areas
- **Export Formats**: JSON, CSV with flattened data structures

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/div197/BOB-Google-Maps.git
cd BOB-Google-Maps

# Install dependencies
pip install -r requirements.txt

# Install Playwright (optional, for faster extraction)
pip install playwright
playwright install chromium
```

### Basic Usage

```python
import bob_core

# Quick business-only extraction (3x faster)
scraper = bob_core.GoogleMapsScraper(extract_reviews=False)
result = scraper.scrape("https://maps.google.com/?q=restaurant&hl=en")
print(f"Business: {result['business_info']['name']}")

# Full extraction with reviews
scraper = bob_core.GoogleMapsScraper(extract_reviews=True)
result = scraper.scrape("https://maps.google.com/?q=restaurant&hl=en")
print(f"Reviews: {result['reviews_count']}")

# Limited reviews for faster processing
scraper = bob_core.GoogleMapsScraper(max_reviews=10)
result = scraper.scrape("https://maps.google.com/?q=restaurant&hl=en")

# Dedicated business-only method
scraper = bob_core.GoogleMapsScraper()
result = scraper.scrape_business_only("https://maps.google.com/?q=restaurant&hl=en")
```

### Command Line Interface

```bash
# Business-only extraction (fastest)
python -m bob_core.cli single "https://maps.google.com/?q=restaurant&hl=en" --business-only

# Full extraction with Playwright backend
python -m bob_core.cli single "https://maps.google.com/?q=restaurant&hl=en" --backend playwright

# Batch processing from file
python -m bob_core.cli batch urls.txt --workers 4 --business-only

# Health check
python -m bob_core.health_cli status

# Circuit breaker status
python -m bob_core.health_cli circuits
```

### Batch Processing

```python
from bob_core.batch import batch_scrape

urls = [
    "https://maps.google.com/?q=restaurant+paris&hl=en",
    "https://maps.google.com/?q=cafe+london&hl=en"
]

# Business-only batch (fastest for directories)
results = batch_scrape(urls, extract_reviews=False, max_workers=4)

# Limited reviews batch
results = batch_scrape(urls, max_reviews=5, max_workers=2)

# Full extraction batch
results = batch_scrape(urls, extract_reviews=True, max_workers=2)
```

### Analytics & Business Intelligence

```python
from bob_core.analytics import MarketAnalyzer, BusinessAnalyzer
from bob_core.export import export_data

# Analyze market trends
analyzer = MarketAnalyzer(results)
market_analysis = analyzer.category_analysis()
opportunities = analyzer.market_opportunities()

# Individual business analysis
business_analyzer = BusinessAnalyzer(single_result)
score = business_analyzer.overall_score()

# Export results
export_data(results, "market_data.json", format="json")
export_data(results, "market_data.csv", format="csv")
```

## 📊 Performance Benchmarks

| Mode | Time | Reviews | Use Case |
|------|------|---------|----------|
| **Business-Only** | ~18s | 0 | Business directories, contact lists |
| **Limited (10 reviews)** | ~20s | 10 | Quick sentiment check |
| **Full Extraction** | ~56s | 250+ | Comprehensive analysis |

**Speed Improvements:**
- Business-only: **3.18x faster** than full extraction
- Playwright backend: **1.5x faster** than Selenium
- Smart review limiting: **2.8x faster** for partial data

## 🛡️ Enterprise Features

### Fault Tolerance
```python
# Circuit breaker configuration
scraper = bob_core.GoogleMapsScraper()
cb = bob_core.get_circuit_breaker("my_scraper", failure_threshold=5)

# Health monitoring
health = bob_core.get_global_health_monitor()
status = health.get_system_status()

# Memory management
memory_manager = bob_core.get_global_memory_manager()
stats = memory_manager.get_comprehensive_stats()
```

### Performance Monitoring
```python
# Performance tracking
perf_monitor = bob_core.get_global_performance_monitor()
metrics = perf_monitor.get_current_metrics()

# Dead letter queue for failed requests
dlq = bob_core.get_global_dlq()
failed_requests = dlq.get_failed_requests()
```

## 🏗️ Architecture

```text
bob_core/
├── scraper.py              # Main scraper interface
├── playwright_backend.py   # Playwright implementation
├── business_parser.py      # Business info extraction
├── review_parser.py        # Review extraction
├── analytics.py            # Business intelligence
├── circuit_breaker.py      # Fault tolerance
├── memory_management.py    # Resource optimization
├── performance_monitoring.py # Metrics & profiling
├── health_check.py         # System monitoring
├── graceful_degradation.py # Partial failure handling
├── auto_recovery.py        # Self-healing capabilities
├── dead_letter_queue.py    # Failed request handling
├── retry_strategy.py       # Smart retry logic
├── selector_healing.py     # DOM selector adaptation
├── data_quality.py         # Data validation & cleaning
├── connection_pooling.py   # Resource pooling
├── export.py               # Data export utilities
├── batch.py                # Batch processing
├── cli.py                  # Command line interface
├── health_cli.py           # Health monitoring CLI
└── models.py               # Pydantic data models
```

## 🔧 Configuration

### Backend Selection
```python
# Auto-select best backend
scraper = bob_core.GoogleMapsScraper(backend="auto")

# Force Selenium (most reliable)
scraper = bob_core.GoogleMapsScraper(backend="selenium")

# Force Playwright (fastest)
scraper = bob_core.GoogleMapsScraper(backend="playwright")
```

### Extraction Options
```python
# Business-only (fastest)
scraper = bob_core.GoogleMapsScraper(extract_reviews=False)

# Limited reviews
scraper = bob_core.GoogleMapsScraper(max_reviews=10)

# Full extraction
scraper = bob_core.GoogleMapsScraper(extract_reviews=True)
```

### Timeout & Performance
```python
# Custom timeout
scraper = bob_core.GoogleMapsScraper(timeout=60)

# Headless mode (default)
scraper = bob_core.GoogleMapsScraper(headless=True)

# Visible browser (debugging)
scraper = bob_core.GoogleMapsScraper(headless=False)
```

## 📈 Use Cases

### 1. Business Directory Creation
```python
# Extract business info only for maximum speed
scraper = bob_core.GoogleMapsScraper(extract_reviews=False)
results = batch_scrape(restaurant_urls, extract_reviews=False)
export_data(results, "restaurant_directory.csv")
```

### 2. Market Research
```python
# Full extraction with analytics
scraper = bob_core.GoogleMapsScraper(extract_reviews=True)
results = batch_scrape(competitor_urls)
analyzer = MarketAnalyzer(results)
opportunities = analyzer.market_opportunities()
```

### 3. Sentiment Analysis
```python
# Limited reviews for sentiment check
scraper = bob_core.GoogleMapsScraper(max_reviews=20)
results = batch_scrape(business_urls, max_reviews=20)
for result in results:
    sentiment = ReviewAnalyzer(result['reviews']).sentiment_analysis()
```

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Test specific functionality
python -m pytest tests/test_circuit_breaker.py -v

# Health check
python -m bob_core.health_cli status

# Performance test
python -c "
import bob_core
scraper = bob_core.GoogleMapsScraper(extract_reviews=False)
result = scraper.scrape('https://maps.google.com/?q=restaurant&hl=en')
print(f'Business-only test: {result[\"success\"]}')
"
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Clone and setup
git clone https://github.com/div197/BOB-Google-Maps.git
cd BOB-Google-Maps
pip install -r requirements.txt

# Run tests
python -m pytest tests/ -v

# Check health
python -m bob_core.health_cli status
```

## 📄 License

MIT © 2025 Divyanshu Singh Chouhan (<divyanshu@abcsteps.com>)

## 🙏 Philosophy

Built following **Niṣkāma Karma Yoga** principles:
- **Excellence without attachment** to results
- **Service-oriented** development
- **Zero-compromise** quality standards
- **Community-first** approach

---

> **Status: Production Ready v0.5.0**  
> Enterprise-grade Google Maps scraper with business-only extraction, fault tolerance, and comprehensive analytics. Battle-tested with real-world data.

**Made with 🙏 in India for the World** 