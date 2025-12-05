# Architecture Guide - BOB Google Maps v4.3.0# Architecture Guide - BOB Google Maps



## OverviewUnderstanding the system design and components.



BOB Google Maps uses a **hybrid extraction architecture** with Playwright as the primary engine and Selenium as fallback, backed by SQLite caching.## System Overview



```BOB Google Maps uses a **multi-engine extraction architecture** optimized for speed, reliability, and memory efficiency.

┌─────────────────────────────────────────────────┐

│              User Application                    │```

│  python -m bob "query"  OR  Python API          │┌─────────────────────────────────────────────────────┐

└────────────────────┬────────────────────────────┘│         User Application Layer                       │

                     ││  (Your Python code using BOB extractors)            │

┌────────────────────▼────────────────────────────┐└──────────────────┬──────────────────────────────────┘

│           HybridExtractorOptimized              │                   │

│  ┌─────────────────────────────────────────┐    │┌──────────────────▼──────────────────────────────────┐

│  │            Cache Check                   │    ││      Extraction Engine Layer (Choose One)            │

│  │  (SQLite: bob_cache_ultimate.db)        │    ││  ┌────────────────┬─────────────┬────────────────┐  │

│  └─────────────────────────────────────────┘    ││  │ Playwright     │ Selenium    │ Hybrid         │  │

│           │ miss           │ hit                ││  │ (Fast)         │ (Reliable)  │ (Balanced)     │  │

│           ▼                ▼                    ││  └────────────────┴─────────────┴────────────────┘  │

│  ┌────────────────┐  ┌─────────────┐           │└──────────────────┬──────────────────────────────────┘

│  │   Playwright   │  │ Return from │           │                   │

│  │   Extractor    │  │    cache    │           │┌──────────────────▼──────────────────────────────────┐

│  └────────┬───────┘  └─────────────┘           ││      Data Extraction & Processing                    │

│           │ fail                                ││  ├─ DOM Parsing & Extraction                        │

│           ▼                                     ││  ├─ Quality Score Calculation                       │

│  ┌────────────────┐                            ││  ├─ Error Handling & Fallbacks                      │

│  │    Selenium    │                            ││  └─ Data Validation                                 │

│  │    Fallback    │                            │└──────────────────┬──────────────────────────────────┘

│  └────────────────┘                            │                   │

└────────────────────┬────────────────────────────┘┌──────────────────▼──────────────────────────────────┐

                     ││      Support Systems                                 │

┌────────────────────▼────────────────────────────┐│  ┌──────────────┬──────────────┬──────────────────┐ │

│              Browser Layer                       ││  │ Cache System │ Config Mgmt   │ Logging/Monitor  │ │

│  • Chromium (Playwright/Selenium)               ││  │ (SQLite)     │ (YAML/Python) │ (Real-time)      │ │

│  • Headless mode                                ││  └──────────────┴──────────────┴──────────────────┘ │

│  • Resource blocking (images/fonts)             │└──────────────────┬──────────────────────────────────┘

└────────────────────┬────────────────────────────┘                   │

                     │┌──────────────────▼──────────────────────────────────┐

                     ▼│      Browser Layer (Chrome/Chromium)                │

              Google Maps│  ├─ Playwright or Selenium Driver                   │

```│  ├─ Resource Blocking (Ads/Tracking only)          │

│  └─ Network Interception                            │

## Core Components└──────────────────┬──────────────────────────────────┘

                   │

### 1. Extraction Engines         Google Maps API (Production)

```

| Engine | Type | Speed | Use Case |

|--------|------|-------|----------|## Component Architecture

| `PlaywrightExtractorOptimized` | Async | 10-22s | Primary extraction |

| `SeleniumExtractorOptimized` | Sync | 15-30s | Fallback |### 1. Extraction Engines

| `HybridExtractorOptimized` | Sync | 10-25s | **Recommended** - combines both |

#### PlaywrightExtractorOptimized (Recommended)

### 2. Cache System- **Speed:** 7-11 seconds per business

- **Memory:** <30MB per extraction

SQLite-based caching in `bob_cache_ultimate.db`:- **Advantages:** Fast, low memory, good data quality

- **Use Case:** Default choice for most applications

```

businesses table:#### SeleniumExtractorOptimized

  - place_id (PRIMARY KEY)- **Speed:** 8-15 seconds per business

  - name, phone, address, website- **Memory:** <40MB per extraction

  - latitude, longitude- **Advantages:** Reliable fallback, stealth mode

  - rating, review_count- **Use Case:** When Playwright fails, critical businesses

  - full_data (JSON blob)

  - extracted_at, updated_at#### HybridExtractorOptimized

```- **Speed:** 9-12 seconds per business

- **Memory:** <50MB per extraction

Cache provides **~1800x speedup** for repeat queries.- **Advantages:** Flexible, memory-conscious

- **Use Case:** Memory-constrained environments

### 3. Data Model

### 2. Data Models

The `Business` model has **34 fields**:

#### Business (108 Fields)

```python```

# Identification (7 fields)Core Fields (8):        place_id, cid, name, phone, address, emails, latitude, longitude

place_id, cid, place_id_original, place_id_confidence,Business Details (15):  category, rating, review_count, website, hours, price_range, etc.

place_id_format, is_real_cid, place_id_urlRich Data (25+):        photos, reviews, popular_times, social_media, menu_items

Metadata (12):          quality_score, extraction_time, extracted_at, etc.

# Core Info (4 fields)```

name, phone, address, emails

### 3. Cache System

# Location (3 fields)

latitude, longitude, plus_code**SQLite-based intelligent caching:**

- 1800x faster for repeated queries

# Business Details (7 fields)- Automatic expiration (configurable)

category, rating, review_count, website, hours,- Smart incremental updates

current_status, price_range- Efficient cleanup



# Service Options (1 field)### 4. Configuration Management

service_options  # dict: dine_in, takeout, delivery

```yaml

# Rich Data (5 fields)extraction:  # Extraction behavior

attributes, photos, reviews, popular_times, social_media, menu_itemsmemory:      # Memory optimization

browser:     # Browser settings

# Metadata (7 fields)cache:       # Cache configuration

extracted_at, data_quality_score, extraction_method,logging:     # Log settings

extraction_time_seconds, extractor_version, metadata```

```

## Data Flow

## Directory Structure

### Single Business Extraction

```

bob/```

├── __init__.py           # Package exports1. Query Input

├── __main__.py           # CLI entry point   └─> "Starbucks Times Square New York"

├── cli.py                # Command-line interface

├── exceptions.py         # Custom exceptions2. Cache Check

├── extractors/   ├─ Found → Return (0.1 seconds)

│   ├── __init__.py   └─ Not found → Continue

│   ├── playwright_optimized.py   # Primary engine

│   ├── selenium_optimized.py     # Fallback engine3. Browser Launch

│   └── hybrid_optimized.py       # Orchestrator   ├─ JavaScript enabled

├── models/   ├─ Minimal resource blocking

│   ├── __init__.py   └─ Navigate to Google Maps

│   ├── business.py       # Business dataclass (34 fields)

│   ├── review.py         # Review dataclass4. Search Execution

│   └── image.py          # Image dataclass   ├─ Input query

├── cache/   ├─ Wait for results

│   ├── __init__.py   └─ Parse results page

│   └── cache_manager.py  # SQLite cache

├── config/5. Business Link Discovery

│   ├── __init__.py   ├─ Find first result

│   └── settings.py       # Configuration   └─ Extract link/place_id

└── utils/

    ├── __init__.py6. Business Details Extraction

    ├── website_extractor.py   ├─ Extract name, phone, address

    ├── image_extractor.py   ├─ Extract rating, reviews

    └── email_extractor.py   ├─ Extract hours, website

```   └─ Extract additional fields



## Extraction Flow7. Quality Scoring

   ├─ Count extracted fields

### 1. URL Handling   ├─ Verify data validity

   └─ Calculate quality score 0-100

Input is converted to Google Maps search URL:

8. Cache Storage

```   └─ Save for future requests

"Starbucks Times Square NYC"

    ↓9. Return Results

https://www.google.com/maps/search/Starbucks+Times+Square+NYC?hl=en   └─> Business object with all data

``````



Key insight: Using `/search/` instead of `/place/` allows Google to redirect to the correct business page automatically.### Batch Processing Flow



### 2. Data Extraction```

Input: [Business1, Business2, ..., BusinessN]

JavaScript is executed in the browser to extract:       ↓

For Each Business:

1. **Name** - from `h1` element├─ Check Cache

2. **Phone** - from `button[data-item-id^='phone:']`├─ Extract (if not cached)

3. **Address** - from `button[data-item-id='address']`├─ Quality Check

4. **Website** - from `a[data-item-id='authority']`├─ Store Result

5. **Rating** - from review element└─ Rate Limit (pause between)

6. **GPS** - from URL parameters or page elements (3 fallback methods)       ↓

7. **Images** - from photo galleryOutput: Results array + statistics

```

### 3. Quality Scoring

## Quality Scoring Algorithm

Score calculated based on field completeness:

```python

```score = 0

Name:      15 pointsscore += 20 if name          # Essential field

Phone:     10 pointsscore += 15 if phone         # Contact info

Address:   10 pointsscore += 15 if address       # Location data

GPS:       15 pointsscore += 10 if rating        # Business metrics

Rating:     8 pointsscore += 10 if category      # Business type

Category:   7 pointsscore += 10 if website       # Web presence

Website:    8 pointsscore += 5  if emails        # Email contacts

Photos:    up to 10 pointsscore += 5  if hours         # Operating hours

Reviews:   up to 7 pointsscore += 5  if reviews       # Social proof

-----------------------score += 5  if photos        # Visual content

Maximum:  100 points

```return min(score, 100)

```

## Configuration

## Memory Management

Environment variables (optional):

### Optimization Strategies

```bash

BOB_HEADLESS=true          # Headless browser1. **Resource Blocking**

BOB_TIMEOUT=60             # Page timeout   - Block ads, tracking, analytics

BOB_MAX_RETRIES=3          # Retry attempts   - Allow Google Maps APIs only

BOB_SELENIUM_ENABLED=true  # Enable Selenium fallback   - Reduce page load size

```

2. **Incremental Loading**

## Performance Characteristics   - Load data as needed

   - Don't load full page DOM

| Metric | Value |   - Clean up after extraction

|--------|-------|

| First extraction | 10-22 seconds |3. **Process Cleanup**

| Cached extraction | ~10ms |   - Proper browser instance closure

| Memory usage | <50MB |   - Memory leak prevention

| Success rate | 95%+ |   - Garbage collection triggers

| Quality score | 90-100 avg |

### Memory Profile

---- **Base:** 26-27MB (just extractors)

- **Per Extraction:** 35-40MB peak

**v4.3.0** | December 5, 2025- **Peak Total:** 64MB across all operations


## Error Handling & Fallbacks

### Extraction Failure Handling

```
Browser Launch Failed
└─> Try alternative extractor (Selenium)
    └─> If fails → Return error result

DOM Elements Not Found
└─> Try alternate selectors (6 strategies)
    └─> If fails → Return partial data

Network Timeout
└─> Retry with exponential backoff
    └─> Max 3 attempts, then fail

Invalid Data
└─> Validate format
    └─> Return with quality score penalty
```

## Scalability

### Single Machine
- **Sequential Processing:** 1 business every 7.4 seconds = 486/day
- **Parallel Processing:** 3 concurrent = 1,458/day  
- **Batch Processing:** 110 businesses in 14.1 minutes

### Distributed Scaling
- Stateless design allows horizontal scaling
- Cache can be centralized (Redis)
- Each machine operates independently
- Database can handle millions of cached entries

## Performance Characteristics

### Speed
- Average: 7.4 seconds per business
- Range: 5-25 seconds (landmarks)
- Cache hit: 0.1 seconds

### Accuracy
- Success Rate: 100% on valid businesses
- Quality Score: 85.5/100 average (verified with 110 real businesses)
- Field Extraction: 80-100% per field

### Efficiency
- Memory: 64MB peak
- CPU: Moderate (browser rendering)
- Network: Minimal (selective blocking)

## Design Principles

### 1. Real Data First
- Extract actual data, not simulated
- Verify against source
- Honest metrics

### 2. Minimal Dependencies
- Core: Python + Playwright/Selenium
- Optional: Pandas for export
- No heavyweight frameworks

### 3. Flexibility
- Pluggable extractors
- Configurable behavior
- Custom data pipelines

### 4. Reliability
- Multiple fallbacks
- Robust error handling
- Graceful degradation

## Integration Points

### CRM Systems
- Salesforce
- HubSpot
- Pipedrive
- Custom REST APIs

### Data Warehouses
- PostgreSQL
- MongoDB
- Elasticsearch
- BigQuery

### Export Formats
- CSV
- JSON
- Excel
- Database

## Development Stack

### Core Technologies
- **Language:** Python 3.8+
- **Browser Automation:** Playwright / Selenium
- **Data:** SQLite cache, JSON export
- **Config:** YAML / Python

### Testing Infrastructure
- **Framework:** pytest
- **Coverage:** 95%+
- **CI/CD:** GitHub Actions

### Documentation
- **Markdown:** Complete API docs
- **Examples:** Working code samples
- **Guides:** User-facing tutorials

---

For detailed API documentation, see [API_REFERENCE.md](API_REFERENCE.md).
For troubleshooting, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).
