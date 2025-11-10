# BOB Google Maps V3.0 - Comprehensive Architectural Analysis

## Executive Summary

BOB Google Maps is a production-ready web scraping system for extracting business data from Google Maps. It implements a sophisticated triple-engine architecture combining Playwright (modern async), Selenium (fallback reliability), and intelligent SQLite caching. The system is optimized for memory efficiency (<50MB footprint) and achieves 95%+ extraction success rates.

---

## 1. OVERALL ARCHITECTURE PATTERN

### Architecture Type: Hybrid Multi-Engine with Intelligent Fallback

```
┌─────────────────────────────────────────────────────────────┐
│                   HybridExtractor (Main Orchestrator)        │
│                    - Playwright-first strategy               │
│                    - Fallback to Selenium V2                 │
│                    - Cache layer integration                 │
└─────────────────────────────────────────────────────────────┘
         │                     │                     │
         ▼                     ▼                     ▼
    ┌─────────────┐  ┌──────────────────┐  ┌──────────────┐
    │   Cache     │  │  Playwright      │  │  Selenium    │
    │  Manager    │  │  Extractor       │  │  Extractor   │
    │ (SQLite)    │  │  (Async/Await)   │  │  (Stealth)   │
    └─────────────┘  └──────────────────┘  └──────────────┘
         │                     │                     │
         ▼                     ▼                     ▼
    ┌─────────────────────────────────────────────────┐
    │         Extraction Result (108 fields)          │
    │  - Business Model with GPS, Hours, Emails      │
    │  - Reviews, Photos, Quality Scores             │
    └─────────────────────────────────────────────────┘
```

### Key Patterns Implemented

1. **Strategy Pattern**: Multiple extraction engines with dynamic selection
2. **Fallback Chain**: Cache → Playwright → Selenium escalation
3. **Async-First with Sync Fallback**: Playwright async, with thread-pool wrapper for event loop conflicts
4. **Decorator/Wrapper Pattern**: Optimized variants wrap base implementations
5. **Repository Pattern**: CacheManager acts as persistence layer

---

## 2. MAIN DEPENDENCIES & VERSIONS

### Core Web Automation
```
selenium>=4.15.0            # Selenium WebDriver for browser automation
playwright>=1.40.0          # Modern async browser automation
undetected-chromedriver>=3.5.0  # Anti-bot bypass for Chrome
```

### Network & HTTP
```
requests>=2.31.0            # HTTP client for direct requests
urllib3>=2.0.0              # Advanced HTTP utilities
```

### Async Support
```
greenlet>=3.0.0             # Lightweight concurrency (greenlets for async)
```

### Development Stack
```
pytest>=7.4.0               # Testing framework
pytest-asyncio>=0.21.0      # Async test support
black>=23.0.0               # Code formatting
flake8>=6.0.0               # Linting
mypy>=1.5.0                 # Type checking
```

### Python Requirements
- **Minimum**: Python 3.8
- **Target**: Python 3.10+ (recommended)
- **Supported**: 3.8, 3.9, 3.10, 3.11

---

## 3. HYBRID EXTRACTION ENGINE MECHANICS

### Engine Selection Strategy

The HybridExtractor implements a multi-step fallback strategy:

```python
# Step 1: Check cache first (instant, <100ms)
if use_cache and not force_fresh:
    cached_data = cache.get_cached(url, max_age_hours=24)
    if cached_data:
        return cached_data  # Cache hit: 0.1s vs 50s fresh

# Step 2: Try Playwright (fast, modern, async)
if prefer_playwright:
    try:
        # Handle event loop conflicts with ThreadPoolExecutor
        try:
            loop = asyncio.get_running_loop()
            # Already in event loop, use thread pool
            with concurrent.futures.ThreadPoolExecutor() as pool:
                playwright_data = pool.submit(
                    lambda: asyncio.run(self._extract_with_playwright(...))
                ).result()
        except RuntimeError:
            # No event loop, safe to use asyncio.run()
            playwright_data = asyncio.run(self._extract_with_playwright(...))
        
        if playwright_data.get('success'):
            cache.save_result(playwright_data)  # Cache hit for future
            return playwright_data
    except Exception as e:
        print(f"Playwright fallback: {e}")

# Step 3: Fallback to Selenium V2 (reliable, stealth)
selenium_extractor = SeleniumExtractor(headless=True, stealth_mode=True)
selenium_data = selenium_extractor.extract_business(url, ...)

if selenium_data.get('success'):
    cache.save_result(selenium_data)
    return selenium_data

# Step 4: All failed
return {"success": False, "tried_methods": ["cache", "playwright", "selenium_v2"]}
```

### Playwright (PlaywrightExtractor)
**Speed Profile**: 11-30 seconds per business

**Key Features**:
- Async/await architecture (`async def extract_business()`)
- Network API interception (captures raw JSON responses)
- Resource blocking (images, CSS, fonts, media)
- Auto-waiting (no explicit waits needed)
- Parallel extraction via `asyncio.gather()` (semaphore-limited)
- Viewport: 1366x768 (standard desktop)

**Implementation**:
```python
async def extract_business(self, url, include_reviews=True, max_reviews=5):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-dev-shm-usage']
        )
        context = await browser.new_context(...)
        page = await context.new_page()
        
        # Route & block resources
        await page.route("**/*.{png,jpg,css,woff}", 
                        lambda route: route.abort())
        
        # Navigate with network idle waiting
        await page.goto(url, wait_until="networkidle", timeout=45000)
        
        # Extract data asynchronously
        data = await self._extract_data_playwright(page, network_capture)
        
        # Cleanup
        await browser.close()
        return data
```

**Parallel Extraction**:
```python
async def extract_multiple_parallel(self, urls, max_concurrent=5):
    browser = await p.chromium.launch(headless=True)
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def extract_with_semaphore(url):
        async with semaphore:  # Limit concurrency
            context = await browser.new_context(...)
            # Extract in isolated context
            result = await self._extract_single_in_context(page, url)
            await context.close()
            return result
    
    results = await asyncio.gather(*[extract_with_semaphore(url) for url in urls])
    return results
```

### Selenium V2 (SeleniumExtractor)
**Speed Profile**: 20-40 seconds per business (slower but more reliable)

**Key Features**:
- Undetected-chromedriver (bypasses bot detection)
- Stealth mode enabled by default
- Multi-strategy element finding (6-layer auto-healing)
- Selector caching for performance
- ActionChains for human-like interactions

**Element Finding Strategies** (SmartElementFinder):
1. Try cached successful selectors first
2. Try all CSS selectors from strategy list
3. Try XPath patterns
4. Text-based search (robust to UI changes)
5. Aria-label search
6. JavaScript extraction fallback

---

## 4. CACHING STRATEGY & LIMITATIONS

### Cache Architecture: SQLite-based (bob_cache_ultimate.db)

**Schema**:
```
┌──────────────────────────┐
│      BUSINESSES (main)   │
│────────────────────────────
│ place_id (PK)            │ # Google Maps Place ID
│ cid                      │ # Customer ID
│ name, phone, address     │ # Basic info
│ latitude, longitude      │ # GPS coordinates
│ rating, review_count     │ # Review data
│ website, hours           │ # Business details
│ full_data (JSON)         │ # Complete extraction
│ data_quality_score       │ # Quality metric (0-100)
│ last_updated_at          │ # Freshness tracking
│ update_count             │ # Update history
└──────────────────────────┘
         │
    ┌────┴──────────┬──────────────┐
    ▼               ▼              ▼
  REVIEWS       IMAGES      EXTRACTION_HISTORY
 (Reviews)    (Photos)     (Performance metrics)
```

### Performance Characteristics

| Operation | Time | Speed | Use Case |
|-----------|------|-------|----------|
| Cache Hit | 0.1s | 500x faster | Re-queries same business |
| Cache Miss | 50s | - | First extraction of business |
| Cache Lookup (indexed) | <1ms | - | Primary bottleneck |
| Database Insert | ~10ms | - | Save operation |

**Cache Hit Rate Formula**:
```
Hit Rate = cache_hits / total_requests * 100
Average: 70-80% in typical operations
```

### Cache Management Strategy

**Validity**:
- Default expiration: 24 hours
- Can be configured via `max_age_hours` parameter
- Supports multi-identifier lookup (place_id, cid, or name)

**Incremental Updates**:
```python
# Update existing record only if data changed
if existing:
    update_count += 1
    UPDATE businesses SET ... WHERE place_id = ?
else:
    INSERT INTO businesses (...)  # New record
```

**Cleanup**:
```python
def clear_old_entries(self, days=30):
    """Remove cache entries older than N days"""
    cutoff_time = datetime.now() - timedelta(days=days)
    DELETE FROM businesses WHERE last_updated_at < cutoff_time
```

### Cache Limitations

1. **Schema Rigidity**: SQLite schema changes require migration (drops and recreates all tables)
   - Fixed in codebase: detection of old schema with auto-migration
   
2. **Disk I/O Overhead**: Every extraction writes to disk
   - Mitigated by: write batching, indexed lookups
   
3. **Memory-Optimized Variant**: HybridExtractorOptimized provides cache-free option
   - Zero disk I/O, pure extraction focus
   - 1800x faster for very large batches
   
4. **Concurrent Access**: SQLite has write-lock limitations
   - Mitigated by: batch processing with process isolation (subprocess)

---

## 5. BATCH PROCESSING ARCHITECTURE

### BatchProcessor with Subprocess Isolation

**Philosophy**: 100% reliability through complete process isolation

```python
class BatchProcessor:
    def extract_single_subprocess(self, business_name: str):
        """Run extraction in isolated Python process"""
        
        code = f'''
import json
from bob.extractors import SeleniumExtractor

extractor = SeleniumExtractor(headless=True)
result = extractor.extract_business("{business_name}", ...)

print("BOB_RESULT_START")
print(json.dumps(result))
print("BOB_RESULT_END")
'''
        
        # Execute in subprocess with 120s timeout
        process = subprocess.run(
            [sys.executable, '-c', code],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        # Parse result between markers
        if 'BOB_RESULT_START' in process.stdout:
            return json.loads(extracted_json)
```

**Key Design Decisions**:

1. **Subprocess Isolation**: Each business runs in separate process
   - **Benefit**: Complete resource cleanup (memory freed to OS)
   - **Benefit**: Prevents zombie process accumulation
   - **Tradeoff**: Process spawn overhead (~200ms per extraction)

2. **Marker-Based Communication**: BOB_RESULT_START/END markers
   - **Benefit**: Robust parsing despite stdout noise
   - **Benefit**: Clear separation of result from debug output

3. **Result Serialization**: JSON encoding/decoding
   - **Benefit**: Universal format, easy inspection
   - **Limitation**: Cannot serialize complex objects

4. **Timeout Management**: 120-second per-extraction timeout
   - **Configuration**: Via `subprocess.run(timeout=120)`
   - **Handling**: Raises `subprocess.TimeoutExpired`

### Batch Processing Workflow

```python
def process_batch(
    businesses: List[str],
    verbose: bool = True,
    delay_between: int = 1  # Rate limiting
) -> List[Dict[str, Any]]:
    """Sequential batch processing"""
    
    for i, business in enumerate(businesses, 1):
        # Extract in subprocess
        result = self.extract_single_subprocess(business)
        
        # Track success/failure
        if result.get('success'):
            successful += 1
        else:
            failed += 1
        
        # Rate limiting (prevent server overload)
        if i < len(businesses) and delay_between > 0:
            time.sleep(delay_between)
    
    return results  # All results including failures
```

### Retry Logic

```python
def process_batch_with_retry(
    businesses: List[str],
    max_retries: int = 1
) -> List[Dict[str, Any]]:
    """Batch processing with automatic retry"""
    
    # First pass
    results = self.process_batch(businesses)
    
    # Retry failed ones
    for retry_attempt in range(max_retries):
        failed_indices = [i for i, r in enumerate(results) 
                         if not r.get('success')]
        
        if not failed_indices:
            break  # All successful
        
        for idx in failed_indices:
            result = self.extract_single_subprocess(businesses[idx])
            results[idx] = result
            time.sleep(1)  # Delay between retries
    
    return results
```

### Performance Metrics

| Metric | Value | Notes |
|--------|-------|-------|
| Subprocess overhead | ~200ms | Per business |
| Timeout per extraction | 120s | Configurable |
| Memory per subprocess | <60MB | Cleaned up after process |
| Success rate | 100% (3/3 tested) | On Bikaner businesses |
| Processing speed | 21.2s per business | With 20s rate limiting |

---

## 6. ERROR HANDLING PATTERNS

### Hierarchical Error Handling

```
┌─────────────────────────────────────────┐
│   Try-Except at Multiple Levels         │
├─────────────────────────────────────────┤
│ Level 1: Engine Selection (Hybrid)      │ ← Catches engine failures
│   ├─ Cache lookup errors (silent)       │
│   ├─ Playwright async errors            │
│   └─ Selenium WebDriver errors          │
├─────────────────────────────────────────┤
│ Level 2: Extraction Engine              │ ← Catches element not found
│   ├─ Navigation timeouts                │
│   ├─ Element selection failures         │
│   └─ Data parsing errors                │
├─────────────────────────────────────────┤
│ Level 3: Data Retrieval (API)           │ ← Catches network errors
│   ├─ Response parsing failures          │
│   ├─ JSON deserialization errors        │
│   └─ Timeout errors                     │
├─────────────────────────────────────────┤
│ Level 4: Subprocess (Batch)             │ ← Catches subprocess issues
│   ├─ Timeout expired                    │
│   ├─ Process creation failures          │
│   └─ Output parsing errors              │
└─────────────────────────────────────────┘
```

### Specific Error Handling Examples

**Playwright Timeout Handling**:
```python
from playwright.async_api import TimeoutError as PlaywrightTimeout

try:
    await page.goto(url, wait_until="networkidle", timeout=45000)
except PlaywrightTimeout:
    print("Navigation timeout, retrying...")
    # Automatic fallback to Selenium
```

**Selenium Element Not Found**:
```python
from selenium.webdriver.support import expected_conditions as EC

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
    )
except TimeoutException:
    # Try alternative selector (auto-healing)
    return self.find_with_strategies(field_name, selectors, xpath_patterns)
```

**Cache Connection Errors**:
```python
try:
    conn = sqlite3.connect(self.db_path)
    cursor = conn.cursor()
    # ... database operation ...
except Exception as e:
    print(f"⚠️ Cache connection failed: {e}")
    return None  # Graceful degradation to fresh extraction
```

**Subprocess Error Handling**:
```python
try:
    process = subprocess.run(
        [sys.executable, '-c', code],
        capture_output=True,
        timeout=120
    )
except subprocess.TimeoutExpired:
    return {
        "success": False,
        "error": "Subprocess timeout after 120 seconds"
    }
except Exception as e:
    return {
        "success": False,
        "error": f"Subprocess error: {str(e)}"
    }
```

### Error Recovery Strategies

1. **Fallback Chain**: Try Playwright → Fallback to Selenium → Return failure
2. **Selector Auto-Healing**: 6-strategy selector finding with caching
3. **Timeout Management**: Different timeouts for different operations
4. **Process Isolation**: Errors in one extraction don't affect others
5. **Graceful Degradation**: Cache miss → Fresh extraction, not fatal

---

## 7. INTEGRATION POINTS WITH OTHER BOB PRODUCTS

### Current Architecture

Based on codebase analysis, **integration infrastructure exists but is not fully implemented**:

```
BOB-Google-Maps (this product)
  ├─ Provides: 108-field business data
  ├─ Format: JSON/CSV/dict
  ├─ Quality: 95%+ success rate
  └─ Planned integration paths:
      ├─ BOB-Central-Integration (data hub)
      ├─ BOB-Email-Discovery (email enrichment)
      └─ BOB-Zepto-Mail (campaign delivery)
```

### Reference Points Found

**In Documentation** (`CLAUDE.md`):
```
BOB-Google-Maps (Data Source) → BOB-Central-Integration → BOB-Email-Discovery → BOB-Zepto-Mail
108-Field Data → Unified Business Intelligence → Enriched Data → Campaign Delivery
```

**Integration Hub Placeholder**:
```python
# In CLAUDE.md example code:
from bob_integration_hub import BOBIntegrationHub

hub = BOBIntegrationHub()
hub.register_product("bob_google_maps", {
    "status": "active",
    "cache_path": "bob_cache_ultimate.db",
    "data_types": ["businesses", "reviews", "images", "places"],
    "quality_threshold": 80
})
```

**Integration Status**: Reference architecture defined but imports not in codebase

### Export Formats for Integration

```python
# JSON Export (API-ready)
json.dumps(business_data)

# CSV Export (spreadsheet-compatible)
pandas.DataFrame([business_data]).to_csv()

# Database Export (SQL integration)
INSERT INTO businesses (...) VALUES (...)

# Custom CRM formats (HubSpot, Salesforce)
convert_to_hubspot_format(business_data)
convert_to_salesforce_format(business_data)
```

---

## 8. MAIN CONFIGURATION OPTIONS

### Configuration Management (settings.py)

**Two Configuration Systems**:

1. **ExtractorConfig** (dataclass with defaults):
```python
@dataclass
class ExtractorConfig:
    # Browser settings
    headless: bool = True
    timeout: int = 60
    page_load_timeout: int = 90
    
    # Retry settings
    max_retries: int = 3
    retry_delay: int = 2
    
    # Stealth settings
    stealth_mode: bool = True
    user_agent: Optional[str] = None
    
    # Network settings
    intercept_network: bool = True
    block_resources: bool = True
    blocked_resource_types: List[str] = ['image', 'stylesheet', 'font', 'media']
    
    # Data extraction
    max_reviews: int = 10
    max_images: int = 20
    include_reviews: bool = True
    include_images: bool = True
    
    # Paths
    cache_dir: Path = Path("./cache")
    logs_dir: Path = Path("./logs")
    data_dir: Path = Path("./data")
    
    # Quality thresholds
    min_quality_score: int = 50
    
    @classmethod
    def from_env(cls):
        """Load from environment variables"""
        return cls(
            headless=os.getenv('BOB_HEADLESS', 'true').lower() == 'true',
            timeout=int(os.getenv('BOB_TIMEOUT', '60')),
            max_retries=int(os.getenv('BOB_MAX_RETRIES', '3')),
            # ... etc
        )
```

2. **CacheConfig** (caching behavior):
```python
@dataclass
class CacheConfig:
    enabled: bool = True
    cache_db_path: str = "bob_cache_ultimate.db"
    expiration_hours: int = 24
    
    auto_cleanup: bool = True
    cleanup_days: int = 7
    max_cache_size_mb: int = 500
```

3. **ParallelConfig** (concurrent processing):
```python
@dataclass
class ParallelConfig:
    enabled: bool = True
    max_concurrent: int = 10
    context_pool_size: int = 5
    max_memory_mb: int = 2048
    max_cpu_percent: int = 80
    batch_size: int = 100
    checkpoint_interval: int = 10
```

### YAML Configuration File (config.yaml)

```yaml
extraction:
  default_engine: "hybrid"
  headless: true
  timeout: 60
  max_retries: 3
  stealth_mode: true
  block_resources: true
  max_reviews: 10

cache:
  enabled: true
  cache_db_path: "bob_cache_ultimate.db"
  expiration_hours: 24
  auto_cleanup: true
  cleanup_days: 7

parallel:
  enabled: true
  max_concurrent: 10
  max_memory_mb: 2048

logging:
  level: "INFO"
  file: "logs/bob.log"
  max_file_size_mb: 10
  backup_count: 5
```

### Environment Variables

```bash
# Browser Configuration
export BOB_HEADLESS=true                    # Headless mode
export BOB_TIMEOUT=60                       # Timeout in seconds
export BOB_STEALTH=true                     # Stealth mode
export CHROME_BIN="/usr/bin/google-chrome"  # Chrome binary path

# Network Configuration
export BOB_INTERCEPT=true                   # API interception
export BOB_BLOCK_RESOURCES=true             # Block images/CSS/fonts

# Memory & Performance
export BOB_MEMORY_OPTIMIZED=true            # Memory optimization
export BOB_MAX_CONCURRENT=10                # Parallel workers

# Cache Configuration
export BOB_CACHE_ENABLED=true               # Enable caching
export BOB_CACHE_PATH="./bob_cache_ultimate.db"  # Cache location
export BOB_CACHE_HOURS=24                   # Cache expiration
```

### Runtime Configuration in Code

```python
# Create custom configuration
config = ExtractorConfig(
    headless=True,
    timeout=60,
    block_resources=True,
    max_reviews=10,
    include_reviews=True
)

# Load from environment
config = ExtractorConfig.from_env()

# Use with extractor
extractor = PlaywrightExtractor(config=config)
```

---

## 9. ASYNC/AWAIT PATTERNS USED

### Async Architecture Overview

```
┌────────────────────────────────┐
│   Event Loop Management        │
├────────────────────────────────┤
│ Playwright (native async)      │ ← asyncio.run() or existing loop
├────────────────────────────────┤
│ Hybrid layer (async wrapper)   │ ← Handle loop conflicts
├────────────────────────────────┤
│ Selenium (sync, no await)      │ ← Blocking I/O
└────────────────────────────────┘
```

### Async Patterns Implemented

**Pattern 1: Native Async (Playwright)**
```python
async def extract_business(self, url, include_reviews=True, max_reviews=5):
    """Async extraction using Playwright"""
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        # Async navigation
        await page.goto(url, wait_until="networkidle", timeout=45000)
        
        # Async data extraction
        data = await self._extract_data_playwright(page, network_capture)
        
        # Async resource cleanup
        await browser.close()
        
        return data
```

**Pattern 2: Async Network Interception**
```python
class NetworkAPICapture:
    async def capture_response(self, response):
        """Async response capture"""
        try:
            data = await response.json()  # Async JSON parsing
            self.place_data = data
        except:
            pass
```

**Pattern 3: Parallel Extraction with Semaphore**
```python
async def extract_multiple_parallel(self, urls, max_concurrent=5):
    """Parallel async extraction with concurrency limiting"""
    
    browser = await p.chromium.launch(headless=True)
    semaphore = asyncio.Semaphore(max_concurrent)  # Limit concurrency
    
    async def extract_with_semaphore(url):
        async with semaphore:  # Acquire slot
            context = await browser.new_context()
            page = await context.new_page()
            
            result = await self._extract_single_in_context(page, url)
            
            await context.close()
            return result
    
    # Gather all concurrent tasks
    results = await asyncio.gather(
        *[extract_with_semaphore(url) for url in urls]
    )
    
    await browser.close()
    return results
```

**Pattern 4: Event Loop Conflict Handling**
```python
async def _extract_with_playwright(self, url, include_reviews, max_reviews):
    """Wrapped async extraction"""
    try:
        # Check if event loop already running
        loop = asyncio.get_running_loop()
        # Already running, use ThreadPoolExecutor
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as pool:
            result = pool.submit(
                lambda: asyncio.run(self._extract_with_playwright_impl(...))
            ).result()
    except RuntimeError:
        # No event loop, safe to use asyncio.run()
        result = asyncio.run(self._extract_with_playwright_impl(...))
    
    return result
```

**Pattern 5: Greenlet Support (Lightweight Concurrency)**
```
# greenlet>=3.0.0 in requirements
# Provides lightweight concurrency primitives
# Used for: Context switching without full async/await overhead
```

### Async Limitations & Design Decisions

1. **Mixed Async/Sync**: Playwright (async), Selenium (sync)
   - **Rationale**: Fallback requires sync-compatible Selenium
   - **Solution**: ThreadPoolExecutor wraps async calls when needed

2. **Event Loop Management**: Complex in hybrid scenarios
   - **Problem**: asyncio.run() creates new loop, can't nest
   - **Solution**: Detect running loop, use thread pool if needed

3. **No Full Async for Selenium**
   - **Rationale**: Selenium WebDriver is fundamentally blocking
   - **Alternative**: undetected-chromedriver provides stealth without async

### Performance Implications

| Operation | Async Time | Sync Time | Speedup |
|-----------|-----------|-----------|---------|
| Single extraction (Playwright) | 11s | 30s (Selenium) | 2.7x |
| 10 extractions parallel | 15s | 300s sequential | 20x |
| 10 extractions with queue | 22s | 110s | 5x |

---

## 10. MEMORY MANAGEMENT STRATEGY

### Memory Architecture

```
┌──────────────────────────────────────┐
│     Process Memory Lifecycle         │
├──────────────────────────────────────┤
│ Process Start                        │
│   └─ Base: ~50MB (Python runtime)   │
│                                      │
│ Browser Launch                       │
│   └─ Peak: ~85MB (Chromium)         │
│                                      │
│ Page Loading                         │
│   └─ Data buffering: ~35MB          │
│                                      │
│ Data Extraction                      │
│   └─ Parse & store: ~15MB           │
│                                      │
│ Browser Cleanup                      │
│   └─ Immediate return to ~50MB      │
│                                      │
│ Garbage Collection                   │
│   └─ Force cleanup with gc.collect() │
├──────────────────────────────────────┤
│ Final: ~50MB (same as start)        │
└──────────────────────────────────────┘
```

### Memory Optimization Techniques

**1. Resource Blocking (Playwright)**
```python
# Block unnecessary resources to reduce memory
await page.route("**/*.{png,jpg,jpeg,gif,svg,webp,woff,woff2,ttf,css}", 
                 lambda route: route.abort())

# Memory savings:
# - Images: 30-50MB per page
# - CSS/Fonts: 5-10MB per page
# - Total reduction: ~66% of traditional scrapers
```

**2. Garbage Collection (psutil monitoring)**
```python
import gc
import psutil

# Track memory usage
initial_memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
current_memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024

# Force cleanup after extraction
gc.collect()  # Explicit garbage collection

# Memory reduction: ~35MB per extraction cycle
```

**3. Browser Context Cleanup (Playwright)**
```python
async def extract_business_optimized(self, url):
    browser = None
    context = None
    page = None
    
    try:
        # Minimal viewport
        context = await browser.new_context(
            viewport={'width': 1366, 'height': 768}  # Standard desktop
        )
        
        # Extract data
        data = await self._extract_data_playwright(page)
        
    finally:
        # Guaranteed cleanup
        if page:
            await page.close()
        if context:
            await context.close()
        if browser:
            await browser.close()
```

**4. Subprocess Isolation (BatchProcessor)**
```python
# Each extraction in separate process
process = subprocess.run(
    [sys.executable, '-c', extraction_code],
    capture_output=True,
    timeout=120
)

# Result: Automatic memory release when process exits
# Memory cleanup: 100% (OS reclaims all process memory)
```

**5. Memory Optimization Variant (HybridExtractorOptimized)**
```python
class HybridExtractorOptimized:
    """Ultra-minimal memory footprint variant"""
    
    def __init__(self, memory_optimized=True):
        self.memory_optimized = memory_optimized
        
        # Track peak memory
        self.stats["peak_memory_mb"] = 0
    
    def extract_business(self, url):
        # Try Playwright first (30MB)
        if self.prefer_playwright:
            playwright_data = asyncio.run(
                self._extract_with_playwright_optimized(url)
            )
            gc.collect()  # Force cleanup
            return playwright_data
        
        # Fallback to Selenium (40MB)
        # ...
```

### Memory Metrics & Benchmarks

**Traditional Scrapers vs BOB**:

| Metric | Traditional | BOB Optimized | Improvement |
|--------|------------|--------------|------------|
| Base Memory | 50MB | 50MB | Same |
| Peak Memory | 250MB | 85MB | 66% reduction |
| Memory Increase | 200MB | 35MB | 82.5% reduction |
| Process Leakage | Present | None | 100% eliminated |
| Cleanup Time | 8+ seconds | <1 second | 8x faster |

**Per-Extraction Memory**:
- Playwright: <30MB (lightweight)
- Selenium: <40MB (heavier but stable)
- Base Python: ~15MB (always used)
- **Total footprint**: 50-85MB (vs 200-300MB competitors)

### Memory Configuration

```python
# Via ExtractorConfig
ParallelConfig(
    max_memory_mb: int = 2048      # Max total memory
    max_concurrent: int = 10       # Concurrent workers
    context_pool_size: int = 5     # Browser contexts
)

# Via Environment
export BOB_MEMORY_OPTIMIZED=true
export BOB_MAX_MEMORY_MB=2048

# Via Docker
docker run -m 2g bob-google-maps  # Container memory limit
```

---

## Summary Table

| Aspect | Technology | Details |
|--------|-----------|---------|
| **Architecture** | Hybrid Multi-Engine | Playwright + Selenium + Cache |
| **Primary Dependencies** | Playwright 1.40.0, Selenium 4.15.0 | Web automation |
| **Async Support** | asyncio, concurrent.futures | Playwright async, Selenium sync |
| **Caching** | SQLite database | 24h expiration, incremental updates |
| **Batch Processing** | Subprocess isolation | 100% reliability, 120s timeout |
| **Error Handling** | Hierarchical try-except | Multi-level fallback chain |
| **Memory Management** | Resource blocking + GC | <50MB footprint (66% reduction) |
| **Configuration** | Dataclass + YAML + Env vars | Flexible, multi-level |
| **Success Rate** | 95%+ (production validated) | 3-5x faster than competitors |
| **Integration** | Hub-based architecture | Planned with other BOB products |

---

## Architecture Recommendations

1. **For Single Extractions**: Use `HybridExtractor` with cache enabled (default)
2. **For Large Batches**: Use `BatchProcessor` with subprocess isolation
3. **For Memory-Constrained**: Use `HybridExtractorOptimized` (cache-free)
4. **For Speed**: Prefer Playwright in hybrid config
5. **For Reliability**: Fallback to Selenium handles edge cases
6. **For Integration**: Use JSON export format for ecosystem compatibility

