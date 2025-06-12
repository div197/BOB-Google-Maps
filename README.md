# BOB Google Maps v0.5.0

<div align="center">

![BOB Google Maps Banner](https://img.shields.io/badge/BOB-Google%20Maps-blue?style=for-the-badge&logo=googlemaps&logoColor=white)

*Build Online Business – Made in 🇮🇳, Made for the World*

[![Production Ready](https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=for-the-badge)](https://github.com/div197/BOB-Google-Maps)
[![Version](https://img.shields.io/badge/Version-0.5.0-blue?style=for-the-badge)](https://github.com/div197/BOB-Google-Maps/releases)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](https://github.com/div197/BOB-Google-Maps/blob/main/LICENSE)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Selenium](https://img.shields.io/badge/Selenium-Latest-green?style=flat-square&logo=selenium&logoColor=white)](https://selenium.dev)
[![Playwright](https://img.shields.io/badge/Playwright-Latest-orange?style=flat-square&logo=playwright&logoColor=white)](https://playwright.dev)
[![Tests](https://img.shields.io/badge/Tests-23%20Passing-brightgreen?style=flat-square&logo=pytest&logoColor=white)](https://github.com/div197/BOB-Google-Maps/actions)

[![Performance](https://img.shields.io/badge/Performance-3.18x%20Faster-red?style=flat-square&logo=speedtest&logoColor=white)](https://github.com/div197/BOB-Google-Maps)
[![Enterprise](https://img.shields.io/badge/Enterprise-Grade-purple?style=flat-square&logo=enterprise&logoColor=white)](https://github.com/div197/BOB-Google-Maps)
[![Fault Tolerance](https://img.shields.io/badge/Fault-Tolerant-orange?style=flat-square&logo=shield&logoColor=white)](https://github.com/div197/BOB-Google-Maps)

</div>

---

## 🌟 Overview

BOB Google Maps is an **enterprise-grade**, open-source Google Maps scraper that transforms raw location data into actionable business intelligence. Powered by principles of **Niṣkāma Karma Yoga** (selfless, excellence-first action), BOB delivers production-ready performance with zero compromises.

<div align="center">

### 🚀 **3.18x Faster Business-Only Extraction**
*From 56 seconds to 18 seconds – Revolutionary speed for business directories*

</div>

## ✨ What's New in v0.5.0

<table>
<tr>
<td width="50%">

### ⚡ **Lightning-Fast Extraction**
- **Business-Only Mode**: 3.18x faster than full extraction
- **Smart Review Limiting**: Configure max reviews for optimal performance
- **Dual Backend**: Selenium (stable) + Playwright (3x faster)

### 🛡️ **Enterprise Reliability**
- **Circuit Breakers**: Auto-failover when services degrade
- **Auto-Recovery**: Self-healing from temporary failures
- **Graceful Degradation**: Partial data when full extraction fails
- **Health Monitoring**: Real-time system status and metrics

</td>
<td width="50%">

### 📊 **Business Intelligence**
- **Market Analysis**: Category trends, competitive landscape
- **Sentiment Analysis**: Review sentiment scoring with TextBlob
- **Opportunity Detection**: Identify market gaps and high-potential areas
- **Export Formats**: JSON, CSV with flattened data structures

### 🔧 **Production Features**
- **Memory Management**: Automatic garbage collection
- **Performance Monitoring**: Real-time metrics collection
- **Dead Letter Queue**: Failed request handling
- **Connection Pooling**: Resource optimization

</td>
</tr>
</table>

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

# 🚀 Quick business-only extraction (3x faster)
scraper = bob_core.GoogleMapsScraper(extract_reviews=False)
result = scraper.scrape("https://maps.google.com/?q=restaurant&hl=en")
print(f"Business: {result['business_info']['name']}")

# 📊 Full extraction with reviews
scraper = bob_core.GoogleMapsScraper(extract_reviews=True)
result = scraper.scrape("https://maps.google.com/?q=restaurant&hl=en")
print(f"Reviews: {result['reviews_count']}")

# ⚖️ Limited reviews for faster processing
scraper = bob_core.GoogleMapsScraper(max_reviews=10)
result = scraper.scrape("https://maps.google.com/?q=restaurant&hl=en")

# 🎯 Dedicated business-only method
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

## 📊 Performance Benchmarks

<div align="center">

| Mode | Time | Reviews | Use Case | Speed Gain |
|------|------|---------|----------|------------|
| **🚀 Business-Only** | ~18s | 0 | Business directories, contact lists | **3.18x faster** |
| **⚖️ Limited (10 reviews)** | ~20s | 10 | Quick sentiment check | **2.8x faster** |
| **📊 Full Extraction** | ~56s | 250+ | Comprehensive analysis | *Baseline* |

</div>

### 🎯 Real-World Performance Results
- **Business-only**: 17.71s (0 reviews) ⚡
- **Limited reviews**: 20.24s (10 reviews) ⚖️
- **Full extraction**: 56.37s (254 reviews) 📊
- **Time saved**: 38.65s (68.6% reduction) 🎉

## 🏗️ Architecture

<div align="center">

```mermaid
graph TB
    A[GoogleMapsScraper] --> B[Backend Selection]
    B --> C[Selenium Backend]
    B --> D[Playwright Backend]
    
    C --> E[Business Parser]
    D --> E
    E --> F[Review Parser]
    
    G[Fault Tolerance] --> H[Circuit Breaker]
    G --> I[Auto Recovery]
    G --> J[Health Monitor]
    
    K[Performance] --> L[Memory Manager]
    K --> M[Performance Monitor]
    K --> N[Connection Pool]
    
    E --> O[Analytics Engine]
    F --> O
    O --> P[Export System]
```

</div>

### Core Components

```text
bob_core/
├── 🎯 scraper.py              # Main scraper interface
├── 🎭 playwright_backend.py   # Playwright implementation  
├── 🏢 business_parser.py      # Business info extraction
├── 📝 review_parser.py        # Review extraction
├── 📊 analytics.py            # Business intelligence
├── 🛡️ circuit_breaker.py      # Fault tolerance
├── 🧠 memory_management.py    # Resource optimization
├── 📈 performance_monitoring.py # Metrics & profiling
├── 🏥 health_check.py         # System monitoring
├── 🔄 batch.py                # Batch processing
├── 💻 cli.py                  # Command line interface
└── 📋 models.py               # Pydantic data models
```

## 🎯 Use Cases

<table>
<tr>
<td width="33%">

### 🏢 **Business Directories**
```python
# Lightning-fast directory creation
scraper = bob_core.GoogleMapsScraper(
    extract_reviews=False
)
results = batch_scrape(
    restaurant_urls, 
    extract_reviews=False
)
export_data(results, "directory.csv")
```

</td>
<td width="33%">

### 📊 **Market Research**
```python
# Comprehensive market analysis
scraper = bob_core.GoogleMapsScraper(
    extract_reviews=True
)
results = batch_scrape(competitor_urls)
analyzer = MarketAnalyzer(results)
opportunities = analyzer.market_opportunities()
```

</td>
<td width="33%">

### 💭 **Sentiment Analysis**
```python
# Quick sentiment insights
scraper = bob_core.GoogleMapsScraper(
    max_reviews=20
)
results = batch_scrape(
    business_urls, 
    max_reviews=20
)
for result in results:
    sentiment = ReviewAnalyzer(
        result['reviews']
    ).sentiment_analysis()
```

</td>
</tr>
</table>

## 🛡️ Enterprise Features

### Fault Tolerance System
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

## 🔧 Configuration Options

### Backend Selection
```python
# Auto-select best backend
scraper = bob_core.GoogleMapsScraper(backend="auto")

# Force Selenium (most reliable)
scraper = bob_core.GoogleMapsScraper(backend="selenium")

# Force Playwright (fastest)
scraper = bob_core.GoogleMapsScraper(backend="playwright")
```

### Extraction Modes
```python
# 🚀 Business-only (fastest)
scraper = bob_core.GoogleMapsScraper(extract_reviews=False)

# ⚖️ Limited reviews (balanced)
scraper = bob_core.GoogleMapsScraper(max_reviews=10)

# 📊 Full extraction (comprehensive)
scraper = bob_core.GoogleMapsScraper(extract_reviews=True)
```

## 🧪 Testing & Quality

<div align="center">

[![Tests](https://img.shields.io/badge/Unit%20Tests-23%20Passing-brightgreen?style=for-the-badge&logo=pytest)](https://github.com/div197/BOB-Google-Maps/actions)
[![Coverage](https://img.shields.io/badge/Coverage-85%25-green?style=for-the-badge&logo=codecov)](https://github.com/div197/BOB-Google-Maps)
[![Quality](https://img.shields.io/badge/Code%20Quality-A+-blue?style=for-the-badge&logo=codeclimate)](https://github.com/div197/BOB-Google-Maps)

</div>

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

## 🗺️ Roadmap

### ✅ v0.5.0 (Current - Production Ready)
- Business-only extraction (3.18x faster)
- Enterprise fault tolerance system
- Advanced performance monitoring
- Dual backend support (Selenium + Playwright)

### 🔮 v0.6.0 (Coming Soon)
- 🐳 **Docker Support**: Containerized deployment
- 🤖 **AI Integration**: LLM-powered data analysis
- 🚀 **FastAPI Server**: REST API endpoints
- 🔌 **MCP Protocol**: Model Context Protocol support

### 🌟 v0.7.0 (Future)
- 📱 **Mobile Support**: React Native app
- 🌐 **Web Dashboard**: Real-time monitoring UI
- 🔗 **Third-party Integrations**: CRM, Analytics platforms
- 🎯 **Advanced ML**: Predictive analytics

## 📄 License

MIT © 2025 [Divyanshu Singh Chouhan](https://github.com/div197) (<divyanshu@abcsteps.com>)

## 🙏 Philosophy

<div align="center">

Built following **Niṣkāma Karma Yoga** principles:

**Excellence without attachment** • **Service-oriented development** • **Zero-compromise quality** • **Community-first approach**

</div>

---

<div align="center">

### 🌟 **Status: Production Ready v0.5.0**

*Enterprise-grade Google Maps scraper with business-only extraction, fault tolerance, and comprehensive analytics. Battle-tested with real-world data.*

[![GitHub stars](https://img.shields.io/github/stars/div197/BOB-Google-Maps?style=social)](https://github.com/div197/BOB-Google-Maps/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/div197/BOB-Google-Maps?style=social)](https://github.com/div197/BOB-Google-Maps/network/members)
[![GitHub issues](https://img.shields.io/github/issues/div197/BOB-Google-Maps)](https://github.com/div197/BOB-Google-Maps/issues)

**Made with 🙏 in India for the World**

</div> 