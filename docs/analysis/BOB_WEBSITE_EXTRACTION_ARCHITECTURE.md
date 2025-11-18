# BOB-Google-Maps Website Extraction Architecture - Complete Analysis

## Executive Summary

The website extraction flow in BOB-Google-Maps is a **multi-layered system** with:
- **6 different extractor implementations** (Playwright, Selenium, Hybrid - each with optimized variants)
- **2 specialized utility modules** (website_extractor.py and email_extractor.py)
- **3-tier extraction strategy**: Primary HTML selector → Fallback strategies → Intelligent filtering
- **Known issue**: Raw `href` values from Google Maps sometimes return provider URLs instead of actual business websites

---

## Directory Structure

```
/Users/apple31/16 Nov 2025/BOB-Google-Maps/
├── bob/                                    # Main package
│   ├── extractors/                         # 6 different extractor engines
│   │   ├── playwright.py                   # Original Playwright (885 lines) - FULL-FEATURED
│   │   ├── playwright_optimized.py         # Optimized variant (477 lines)
│   │   ├── selenium.py                     # Original Selenium V2 (849 lines) - MOST RELIABLE
│   │   ├── selenium_optimized.py           # Optimized variant (465 lines)
│   │   ├── hybrid.py                       # Hybrid orchestrator (203 lines)
│   │   ├── hybrid_optimized.py             # Memory-optimized (281 lines)
│   │   └── __init__.py                     # Module exports
│   │
│   ├── utils/                              # Specialized extraction utilities
│   │   ├── website_extractor.py            # PRIMARY WEBSITE EXTRACTION LOGIC
│   │   ├── email_extractor.py              # EMAIL EXTRACTION (depends on website)
│   │   ├── image_extractor.py              # IMAGE EXTRACTION (6-phase strategy)
│   │   ├── images.py                       # AdvancedImageExtractor class
│   │   ├── place_id.py                     # Place ID/CID extraction
│   │   └── ...
│   │
│   ├── models/                             # Data structures
│   │   ├── business.py                     # Business data model (108 fields)
│   │   ├── review.py                       # Review model
│   │   └── image.py                        # Image model
│   │
│   ├── cache/                              # SQLite caching system
│   │   └── cache_manager.py
│   │
│   ├── config/                             # Configuration management
│   │   └── settings.py
│   │
│   └── __init__.py                         # Main package exports
│
└── [test files and examples]
```

---

## Website Extraction Workflow

### Level 1: Entry Points (6 Extractors)

All extractors follow the same general flow:
1. Navigate to Google Maps listing
2. Extract website using primary method
3. Email extraction depends on website URL
4. Return combined result

#### **Primary Extractors (In Recommended Order)**

| Extractor | File | Lines | Speed | Reliability | Use Case |
|-----------|------|-------|-------|-------------|----------|
| PlaywrightExtractorOptimized | playwright_optimized.py | 477 | ⚡⚡⚡ Fast | 95% | Default choice |
| SeleniumExtractorOptimized | selenium_optimized.py | 465 | ⚡⚡ Medium | 99% | Fallback when Playwright fails |
| HybridExtractorOptimized | hybrid_optimized.py | 281 | ⚡⚡ Medium | 99% | Auto-selects best engine |
| PlaywrightExtractor (Legacy) | playwright.py | 885 | ⚡⚡⚡ Fast | 95% | Full-featured version |
| SeleniumExtractor (Legacy) | selenium.py | 849 | ⚡⚡ Medium | 99% | Legacy version |
| HybridExtractor (Legacy) | hybrid.py | 203 | ⚡⚡ Medium | 99% | Legacy hybrid |

---

## Website Extraction - Three-Tier Architecture

### Tier 1: Primary HTML Selection

**File**: `/Users/apple31/16 Nov 2025/BOB-Google-Maps/bob/extractors/playwright.py` (Lines 454-500)
**File**: `/Users/apple31/16 Nov 2025/BOB-Google-Maps/bob/extractors/selenium.py` (Lines 619-638)

#### Playwright Extraction (playwright.py)
```python
# Lines 462-470: Define CSS selectors for website element
website_selectors = [
    "a[data-item-id='authority']",      # PRIMARY - Main website link
    "a[aria-label*='website']",         # SECONDARY - Aria-labeled links
    "a[aria-label*='Website']",         # Case variant
    ".lVcKpb a[href*='http']",          # Container-based selector
    "a[href*='http']",                  # Generic fallback
    "[data-item-id='website']",         # Alternative attribute
    ".nVcWpd a[href]",                  # Class-based selector
]

# Lines 472-480: Collect all URLs from matching selectors
available_urls = []
for selector in website_selectors:
    try:
        elements = await page.query_selector_all(selector)
        for elem in elements:
            href = await elem.get_attribute("href")
            if href and not href.startswith("javascript:"):
                available_urls.append(href)  # Raw href values
    except:
        continue

# Lines 488-495: Pass to intelligent extractor for filtering
website = extract_website_intelligent(page_content, available_urls)
if website:
    data["website"] = website
```

#### Selenium Extraction (selenium.py)
```python
# Lines 619-623: Define selector configuration
"website": {
    "selectors": ["[data-item-id='authority']", "[aria-label*='Website']"],
    "xpath": ["//a[contains(@aria-label, 'Website')]"],
    "text": None
}

# Lines 648-658: Smart multi-strategy finder extracts website
result = smart_finder.find_with_strategies(
    "website",
    config["selectors"],
    config.get("xpath"),
    config.get("text")
)
```

**Critical Issue Identified**: 
- The HTML selector `a[data-item-id='authority']` extracts the raw `href` attribute
- This href sometimes points to Google redirect URLs or provider chooser URLs
- **Raw example**: `https://www.google.com/url?q=...` or `https://google.com/viewer/chooseprovider?mid=...`

---

### Tier 2: Intelligent Filtering & Google Redirect Parsing

**File**: `/Users/apple31/16 Nov 2025/BOB-Google-Maps/bob/utils/website_extractor.py` (Lines 16-209)

This is where the main website extraction logic resides.

#### Function: `extract_website_intelligent()` (Lines 16-69)

```python
def extract_website_intelligent(page_text: str, available_urls: list) -> Optional[str]:
    """
    Smart website extraction using "indie hacker" methodology.
    
    Strategy:
    1. Filter out Google internal URLs
    2. Look for patterns like "website:", "visit:", "contact"
    3. Validate URLs for business legitimacy
    4. Prefer actual domains over Google URLs
    """
    
    filtered_urls = []
    
    # STEP 1: Filter URLs (Lines 36-54)
    for url in available_urls:
        if 'google.com' in url.lower():
            # Check if it's a redirect we can parse
            if '/url?' in url or 'q=' in url:
                actual = parse_google_redirect(url)  # Parse redirect
                if actual and 'google.com' not in actual.lower():
                    filtered_urls.append(('redirect', actual))
            # Skip provider chooser URLs, Maps URLs, etc
            continue
        
        # Keep non-Google URLs
        if _is_valid_business_url(url):
            filtered_urls.append(('direct', url))
    
    # STEP 2: Extract URLs from page text patterns (Lines 56-60)
    pattern_based_urls = _extract_urls_from_patterns(page_text)
    for url in pattern_based_urls:
        if url not in [u[1] for u in filtered_urls]:
            filtered_urls.append(('pattern', url))
    
    # STEP 3: Score and select best URL (Lines 62-68)
    if filtered_urls:
        priority_order = {'direct': 0, 'pattern': 1, 'redirect': 2}
        filtered_urls.sort(key=lambda x: priority_order.get(x[0], 99))
        return filtered_urls[0][1]
    
    return None
```

#### Function: `parse_google_redirect()` (Lines 72-94)

Extracts actual URL from Google redirect format:

```python
def parse_google_redirect(google_url: str) -> Optional[str]:
    """
    Parse Google redirect URL to extract actual website.
    
    Example:
    Input:  https://www.google.com/url?q=http://www.business.com/&opi=...
    Output: http://www.business.com/
    """
    if 'google.com/url' not in google_url or 'q=' not in google_url:
        return google_url
    
    parsed = urlparse(google_url)
    query_params = parse_qs(parsed.query)
    
    if 'q' in query_params and query_params['q']:
        real_url = query_params['q'][0]
        real_url = unquote(real_url)
        return real_url
    
    return google_url
```

#### Function: `_is_valid_business_url()` (Lines 97-173)

**Critical: This is the main filter that blocks problematic URLs**

```python
def _is_valid_business_url(url: str) -> bool:
    """
    Check if URL looks like a legitimate business website.
    
    Filters out:
    - Google Maps/internal URLs
    - Facebook/Instagram profiles
    - Booking platforms (Zomato, Swiggy, etc)
    - Maps/review sites
    """
    
    url_lower = url.lower()
    
    # BLOCKED KEYWORDS (Lines 116-156)
    blocked_keywords = [
        # Google internal URLs - CRITICAL FILTER
        'google.com/viewer',           # Provider chooser
        'google.com/aclk',             # Google ads
        '/maps/reserve',               # Maps booking
        '/maps/place',                 # Maps place redirect
        '/viewer/choose',              # Viewer choice page
        'viewer/chooseprovider',       # Provider selector
        'maps.google',                 # Maps domain
        'google.com/maps',             # Maps redirect
        'maps-booking',                # Maps booking
        
        # Social media (not primary business website)
        'facebook.com',
        'instagram.com',
        'twitter.com',
        'youtube.com',
        
        # Booking platforms
        'zomato.com',
        'swiggy.com',
        'booking.com',
        'tripadvisor',
        'yelp.com',
        'justdial',
        'urban piper',
        'deliveroo',
        'ubereats',
        'doordash',
        'grubhub',
        
        # Review sites
        'trustpilot',
        'glassdoor',
        'g2.com',
        
        # Invalid formats
        '@',
        'mailto',
        'localhost',
        '127.0.0.1',
        '192.168',
        '10.0',
    ]
    
    for keyword in blocked_keywords:
        if keyword in url_lower:
            return False
    
    # Validation check
    try:
        parsed = urlparse(url)
        if not parsed.netloc:
            return False
        if parsed.scheme not in ('http', 'https', ''):
            return False
        return True
    except:
        return False
```

#### Function: `_extract_urls_from_patterns()` (Lines 176-208)

**Fallback method: Extract URLs from page text patterns**

```python
def _extract_urls_from_patterns(text: str) -> list:
    """
    Extract URLs from page text using patterns like:
    - "website: www.example.com"
    - "visit: example.com"
    - "contact: www.example.com"
    - Direct URLs in text
    """
    
    urls = []
    
    # Pattern 1: "website:", "visit:", "web:", "contact us at:" with domain
    pattern1 = r'(?:website|visit|web|contact us at|our site|home page|homepage)[\s:]*(?:www\.)?([a-zA-Z0-9]...'
    matches = re.finditer(pattern1, text, re.IGNORECASE)
    # Extract and validate domains
    
    # Pattern 2: Direct URLs in text
    url_pattern = r'https?://(?:www\.)?([a-zA-Z0-9]...'
    matches = re.finditer(url_pattern, text)
    # Extract and validate URLs
    
    return urls
```

---

### Tier 3: Email Extraction (Depends on Website)

**File**: `/Users/apple31/16 Nov 2025/BOB-Google-Maps/bob/utils/email_extractor.py` (Lines 14-147)

Email extraction depends entirely on having a valid business website URL.

#### Function: `extract_real_url_from_google_redirect()` (Lines 14-47)

```python
def extract_real_url_from_google_redirect(google_redirect_url):
    """
    Parse Google redirect URL to get actual website URL.
    
    Examples:
    - Input:  https://www.google.com/url?q=http://www.lallgarhpalace.com/&opi=...
    - Output: http://www.lallgarhpalace.com/
    
    - Input:  https://www.google.com/viewer/chooseprovider?mid=/g/1td74zyg&g2lbs=...
    - Output: None (unrecognized Google format)
    """
    if not google_redirect_url:
        return None
    
    try:
        if 'google.com/url' in google_redirect_url and 'q=' in google_redirect_url:
            parsed = urlparse(google_redirect_url)
            query_params = parse_qs(parsed.query)
            if 'q' in query_params and query_params['q']:
                real_url = query_params['q'][0]
                real_url = unquote(real_url)
                return real_url
        return google_redirect_url
    except:
        return google_redirect_url
```

#### Function: `extract_emails_from_website()` (Lines 50-147)

**Critical Safety Feature**: Rejects Google URLs before attempting extraction

```python
def extract_emails_from_website(website_url, timeout=10):
    """
    Extract emails from business website.
    
    Process:
    1. Parse Google redirects if present
    2. Validate URL format
    3. Skip if still a Google URL (SAFETY GATE)
    4. Fetch website content
    5. Search for emails with multiple regex patterns
    6. Filter out spam/fake emails
    """
    
    if not website_url:
        return []
    
    emails = []
    
    # STEP 1: Parse Google redirect
    real_url = extract_real_url_from_google_redirect(website_url)
    
    # STEP 2: SAFETY GATE - Skip if still a Google URL
    if 'google' in real_url.lower():
        return []  # Designed to reject unrecognized Google formats
    
    # STEP 3-6: Extract emails from actual website
    # [fetch content, apply regex patterns, filter spam emails]
```

---

## Image Extraction Flow

**Files**: 
- `/Users/apple31/16 Nov 2025/BOB-Google-Maps/bob/utils/image_extractor.py` (292 lines)
- `/Users/apple31/16 Nov 2025/BOB-Google-Maps/bob/utils/images.py` (406 lines)

### 6-Phase Extraction Strategy

```
Phase 1: Extract immediate images (visible on page load)
    ↓
Phase 2: Scroll to load lazy-loaded images
    ↓
Phase 3: Click on main photo gallery
    ↓
Phase 4: Scroll through gallery
    ↓
Phase 5: Extract hidden/offscreen images
    ↓
Phase 6: Extract special views (Street View, 360°)
```

### Key Functions

#### `is_valid_image_url()` (image_extractor.py:17-48)
Filters out non-business images (maps, logos, avatars).

#### `convert_to_high_res()` (image_extractor.py:51-76)
Converts image URLs to maximum resolution.

#### `extract_images_playwright()` (image_extractor.py:141-246)
Async image extraction using Playwright.

#### `extract_images_selenium()` (image_extractor.py:249-291)
Fallback to AdvancedImageExtractor for Selenium.

---

## Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ENTRY: HybridExtractor                   │
│         (orchestrates Playwright + Selenium fallback)       │
└──────────────────────────┬──────────────────────────────────┘
                           │
        ┌──────────────────┴──────────────────┐
        │                                     │
    ┌───▼──────────────┐         ┌──────────▼────────┐
    │ Playwright Fast  │         │  Selenium Reliable │
    │  (7-11 seconds)  │         │  (8-15 seconds)    │
    └───┬──────────────┘         └──────────┬────────┘
        │                                   │
        │ Navigate to Google Maps listing   │
        │                                   │
        ├──────────────────────────────────┤
        │
        │ CSS Selectors: a[data-item-id='authority']
        │              + 6 other selectors
        │                              ↓
        │                  ┌──────────────────────────┐
        │                  │ Raw href values collected │
        │                  │ (may be Google URLs)     │
        │                  └────────┬─────────────────┘
        │                           │
        │                           ▼
        │        ┌──────────────────────────────────┐
        │        │   website_extractor.py           │
        │        │   extract_website_intelligent()  │
        │        │                                  │
        │        │ 1. Filter Google URLs            │
        │        │ 2. Parse Google redirects        │
        │        │ 3. Validate business URLs        │
        │        │ 4. Extract from page patterns    │
        │        │ 5. Score and rank URLs           │
        │        └────────┬─────────────────────────┘
        │                 │
        │                 ▼
        │        ┌──────────────────────────────┐
        │        │  Actual Business Website     │
        │        │  (gypsyfoods.in, example.com)│
        │        └────────┬──────────────────────┘
        │                 │
        │                 ├─────────────────────┐
        │                 │                     │
        │                 ▼                     ▼
        │    ┌───────────────────────┐  ┌─────────────────┐
        │    │ email_extractor.py    │  │ Image Extraction│
        │    │ extract_emails...()   │  │ (6-phase)       │
        │    │                       │  │                 │
        │    │ 1. Parse redirects    │  │ Phase 1-6:      │
        │    │ 2. Safety gate (reject│  │ Multiple        │
        │    │    Google URLs)       │  │ strategies      │
        │    │ 3. Fetch website      │  │                 │
        │    │ 4. Regex extraction   │  │                 │
        │    │ 5. Spam filtering     │  └─────────────────┘
        │    └───────────┬───────────┘
        │                │
        │    ┌───────────▼──────────┐
        │    │  Extracted Emails    │
        │    │ [contact@domain.com] │
        │    └──────────────────────┘
        │
        │ Extract Reviews
        │ Extract Place ID/CID
        │ Extract GPS Coordinates
        │ Calculate Quality Score
        │                           
        └──────────────────────────┐
                                   │
                                   ▼
                        ┌──────────────────────┐
                        │  Return Result Dict  │
                        │  {                   │
                        │    name,             │
                        │    phone,            │
                        │    website,          │
                        │    emails,           │
                        │    photos,           │
                        │    reviews,          │
                        │    rating,           │
                        │    address,          │
                        │    ...108+ fields    │
                        │  }                   │
                        └──────────────────────┘
```

---

## All Files Involved in Website/Email/Image Extraction

### Primary Extraction Files

| File | Lines | Purpose | Key Functions |
|------|-------|---------|----------------|
| `bob/extractors/playwright.py` | 885 | Playwright-based extraction | `extract_business()`, `_extract_data_playwright()` (Lines 454-500 for website) |
| `bob/extractors/selenium.py` | 849 | Selenium-based extraction | `extract_business()`, `_extract_business_data_ultimate()` (Lines 619-638 for website) |
| `bob/extractors/hybrid.py` | 203 | Orchestrates Playwright + Selenium | `extract_business()` (Lines 48-143) |
| `bob/extractors/playwright_optimized.py` | 477 | Fast Playwright variant | `extract_business_optimized()` |
| `bob/extractors/selenium_optimized.py` | 465 | Fast Selenium variant | `extract_business_optimized()` |
| `bob/extractors/hybrid_optimized.py` | 281 | Memory-optimized hybrid | `extract_business()` |

### Utility Files (Core Logic)

| File | Lines | Purpose | Key Functions |
|------|-------|---------|----------------|
| `bob/utils/website_extractor.py` | 277 | PRIMARY website extraction logic | `extract_website_intelligent()`, `parse_google_redirect()`, `_is_valid_business_url()`, `_extract_urls_from_patterns()` |
| `bob/utils/email_extractor.py` | 148 | Email extraction from website | `extract_real_url_from_google_redirect()`, `extract_emails_from_website()` |
| `bob/utils/image_extractor.py` | 292 | Image extraction strategies | `extract_images_playwright()`, `extract_images_selenium()`, `is_valid_image_url()` |
| `bob/utils/images.py` | 406 | Advanced image extractor | `AdvancedImageExtractor` class (6-phase extraction) |
| `bob/utils/place_id.py` | ? | Place ID/CID extraction | `PlaceIDExtractor` |
| `bob/utils/converters.py` | ? | Data format conversion | Format conversion utilities |

### Data Model Files

| File | Purpose |
|------|---------|
| `bob/models/business.py` | 108-field Business model |
| `bob/models/review.py` | Review data model |
| `bob/models/image.py` | Image metadata model |

### Cache & Config

| File | Purpose |
|------|---------|
| `bob/cache/cache_manager.py` | SQLite caching system |
| `bob/config/settings.py` | Configuration management |

---

## Known Issues & Bottlenecks

### Issue 1: Google Redirect URLs Not Always Parsed
**Location**: `website_extractor.py` Lines 42-50

**Problem**: 
```python
if 'google.com' in url.lower():
    if '/url?' in url or 'q=' in url:
        actual = parse_google_redirect(url)  # Works
        if actual and 'google.com' not in actual.lower():
            filtered_urls.append(('redirect', actual))
    # Skip provider chooser URLs
    continue
```

**Issue**: Provider chooser URLs like `https://google.com/viewer/chooseprovider?mid=...` don't contain `/url?` or `q=`, so they're skipped entirely (no fallback).

---

### Issue 2: Email Extraction Safety Gate
**Location**: `email_extractor.py` Lines 76-78

**Design Choice** (intentional):
```python
# SAFETY GATE - Skip if still a Google URL
if 'google' in real_url.lower():
    return []  # Rejects unrecognized Google formats
```

This is **by design** - if website extraction fails to get a real URL, emails won't be extracted.

---

### Issue 3: Image Extraction Overhead
**Location**: `images.py` - 6-phase strategy

**Performance Impact**:
- Phase 1: Immediate images (fast)
- Phase 2: Scroll loading (adds 2-3 seconds)
- Phase 3: Click gallery (adds 4-5 seconds)
- Phase 4-6: Additional phases (adds 2-3 seconds more)

Total image extraction: **8-15 seconds** out of total **11-50 seconds** for business extraction.

---

## Selection Guide: Which Extractor to Use?

### For Website Extraction Specifically

1. **Best Performance**: `PlaywrightExtractorOptimized`
   - Files: `playwright_optimized.py` (477 lines)
   - Speed: 7-11 seconds per business
   - Reliability: 95%

2. **Most Reliable**: `SeleniumExtractorOptimized` 
   - Files: `selenium_optimized.py` (465 lines)
   - Speed: 8-15 seconds per business
   - Reliability: 99%

3. **Auto-Failover**: `HybridExtractorOptimized`
   - Files: `hybrid_optimized.py` (281 lines)
   - Tries Playwright first, falls back to Selenium
   - Speed: 7-15 seconds (depends on which succeeds)
   - Reliability: 99%

### Function Call Stack for Website Extraction

```
User Code
    ↓
HybridExtractorOptimized.extract_business()
    ↓
[Cache check] → [Playwright attempt] → [Selenium fallback]
    ↓
PlaywrightExtractorOptimized/SeleniumExtractorOptimized.extract_business_optimized()
    ↓
_extract_data_playwright() / _extract_business_data_ultimate()
    ↓
Smart selector collection (multiple CSS selectors)
    ↓
bob.utils.website_extractor.extract_website_intelligent()
    ↓
_is_valid_business_url() [filter blocked keywords]
_extract_urls_from_patterns() [fallback extraction]
parse_google_redirect() [parse Google URLs]
    ↓
Return valid business website URL
    ↓
[IF website found] → email_extractor.extract_emails_from_website()
                     → returns email list
[IF website NOT found] → emails = [] (empty)
```

---

## Testing & Validation

### Debug File
- `/Users/apple31/16 Nov 2025/BOB-Google-Maps/test_website_extraction_debug.py`

Shows what website is being extracted and whether it's a Google URL or real business website.

### Real-World Test Cases
- Gypsy Vegetarian Restaurant, Jodhpur: Should extract `gypsyfoods.in`
- Lalgarh Palace: Should extract `lallgarhpalace.com`
- Architecture firms in Dubai: Should extract actual firm websites

---

## Summary: Website Extraction Architecture

### The Three-Tier System

1. **Tier 1 (HTML Extraction)**: 
   - Primary selector: `a[data-item-id='authority']`
   - 6 fallback selectors
   - Collects raw href values from Google Maps HTML

2. **Tier 2 (Intelligent Filtering)**:
   - `extract_website_intelligent()` function
   - Filters Google URLs
   - Parses Google redirects
   - Validates business URLs
   - Extracts from page text patterns
   - Scores and ranks results

3. **Tier 3 (Email Extraction)**:
   - Depends on Tier 2 output
   - Additional Google redirect parsing
   - Safety gate rejects Google URLs
   - Fetches website and extracts emails

### Key Takeaway

The system is **well-designed** with proper filtering and fallbacks. The issue with provider URLs is due to Google Maps returning them in certain cases, and they're properly blocked by the intelligent filtering system.

