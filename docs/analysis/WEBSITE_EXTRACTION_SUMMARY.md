# BOB-Google-Maps Website Extraction - Executive Summary

## Quick Reference

This document is a quick reference. For detailed analysis, see:
- **Full Architecture**: `BOB_WEBSITE_EXTRACTION_ARCHITECTURE.md` (26 KB)
- **Visual Diagrams**: `WEBSITE_EXTRACTION_VISUAL_MAP.txt` (41 KB)

---

## The Architecture in 30 Seconds

### Three-Tier System

```
TIER 1: HTML Selection (CSS Selector)
        a[data-item-id='authority'] → raw href attribute
        ↓
TIER 2: Intelligent Filtering (website_extractor.py)
        Filters Google URLs → Parses redirects → Validates business URLs
        ↓
TIER 3: Email Extraction (email_extractor.py)
        Safety gate → Fetch website → Regex extraction → Spam filter
```

---

## Six Extractors (Choose One)

| Extractor | File | Speed | Reliability | Recommendation |
|-----------|------|-------|-------------|-----------------|
| **PlaywrightOptimized** | playwright_optimized.py (477 L) | ⚡⚡⚡ Fast | 95% | **DEFAULT** |
| **SeleniumOptimized** | selenium_optimized.py (465 L) | ⚡⚡ Medium | 99% | Fallback |
| **HybridOptimized** | hybrid_optimized.py (281 L) | ⚡⚡ Medium | 99% | Auto-failover |
| Playwright (Legacy) | playwright.py (885 L) | ⚡⚡⚡ Fast | 95% | Full-featured |
| Selenium (Legacy) | selenium.py (849 L) | ⚡⚡ Medium | 99% | Full-featured |
| Hybrid (Legacy) | hybrid.py (203 L) | ⚡⚡ Medium | 99% | Legacy |

---

## File Map: Website/Email/Image Extraction

### Core Logic Files

1. **website_extractor.py** (277 lines) - PRIMARY
   - `extract_website_intelligent()` - Main filtering logic
   - `parse_google_redirect()` - Extracts real URL from Google redirect
   - `_is_valid_business_url()` - Blocks 45+ keyword patterns
   - `_extract_urls_from_patterns()` - Fallback pattern matching

2. **email_extractor.py** (148 lines) - DEPENDS ON WEBSITE
   - `extract_real_url_from_google_redirect()` - Parse Google redirects
   - `extract_emails_from_website()` - Main extraction (6 steps)

3. **image_extractor.py** (292 lines) - 6-PHASE STRATEGY
   - `extract_images_playwright()` - Async extraction
   - `extract_images_selenium()` - Fallback extraction
   - `is_valid_image_url()` - Filters non-business images
   - `convert_to_high_res()` - URL resolution upgrade

4. **images.py** (406 lines) - ADVANCED IMAGE EXTRACTOR
   - `AdvancedImageExtractor` class - 6-phase comprehensive extraction

### Extractor Files (Choose One)

| File | Lines | Purpose |
|------|-------|---------|
| playwright_optimized.py | 477 | Fast Playwright-based extraction |
| selenium_optimized.py | 465 | Reliable Selenium-based extraction |
| hybrid_optimized.py | 281 | Auto-selects best engine |
| playwright.py | 885 | Full-featured Playwright (legacy) |
| selenium.py | 849 | Full-featured Selenium (legacy) |
| hybrid.py | 203 | Hybrid orchestrator (legacy) |

---

## Website Extraction Flow (Step-by-Step)

### Step 1: Raw URL Collection (Tier 1)
```python
# CSS Selectors (try all 7):
selectors = [
    "a[data-item-id='authority']",      # PRIMARY
    "a[aria-label*='website']",         # SECONDARY
    "a[aria-label*='Website']",
    ".lVcKpb a[href*='http']",
    "a[href*='http']",
    "[data-item-id='website']",
    ".nVcWpd a[href]"
]

# Result: List of raw href values
available_urls = [
    "https://www.google.com/url?q=http://actual.com/",  # Google redirect
    "https://google.com/viewer/chooseprovider?mid=...",  # Provider chooser
    "http://actual.com/",                                # Real website
    ...
]
```

### Step 2: Intelligent Filtering (Tier 2)
```python
# extract_website_intelligent(page_text, available_urls)

# STEP 1: Filter Google URLs
for url in available_urls:
    if 'google.com' in url:
        if '/url?' in url or 'q=' in url:
            # Parse: https://google.com/url?q=http://actual.com/...
            # Result: http://actual.com/
            actual = parse_google_redirect(url)
        else:
            # Skip unrecognized Google format
            skip()
    elif _is_valid_business_url(url):
        # Check 45+ blocked keywords
        # Check URL structure
        add(url)

# STEP 2: Extract from page patterns
pattern_based = _extract_urls_from_patterns(page_text)
# Finds: "website: example.com", "visit example.com", direct URLs

# STEP 3: Score & Rank
# Priority: direct > pattern > redirect
return best_match
```

### Step 3: Email Extraction (Tier 3)
```python
# extract_emails_from_website(website_url)

# STEP 1: Parse Google redirect if present
real_url = extract_real_url_from_google_redirect(website_url)

# STEP 2: SAFETY GATE - Reject Google URLs
if 'google' in real_url.lower():
    return []  # Stop processing

# STEP 3-6: Extract emails from actual website
# Fetch website → Extract with regex → Spam filter
```

---

## Blocked Keywords (45+ Total)

### Google Internal URLs
- `google.com/viewer` - Provider chooser
- `google.com/aclk` - Google ads
- `/maps/reserve` - Maps booking
- `viewer/chooseprovider` - Provider selector
- `google.com/maps` - Maps domain

### Social Media
- facebook.com, instagram.com, twitter.com, youtube.com

### Booking Platforms
- zomato.com, swiggy.com, booking.com, tripadvisor, yelp.com, justdial, ubereats, doordash, grubhub

### Review Sites
- trustpilot, glassdoor, g2.com

### Invalid Formats
- @, mailto, localhost, 127.0.0.1, 192.168, 10.0

---

## Performance Breakdown

| Component | Time | Notes |
|-----------|------|-------|
| Navigate + load | 1-2s | Depends on network |
| CSS selector collection | <1s | Fast element queries |
| Website filtering | 1s | Google URL filtering + validation |
| Email extraction | 2-3s | HTTP fetch + regex |
| Image extraction | 8-15s | 6-phase strategy (longest) |
| Reviews extraction | 2-5s | Optional, per request |
| **Total** | **11-50s** | Varies by business type |

---

## Real-World Examples

### Example 1: Gypsy Vegetarian Restaurant (Jodhpur)
```
Raw URL collected: https://www.google.com/url?q=https://gypsyfoods.in/&opi=...
                   ↓
Parse Google redirect: https://gypsyfoods.in/
                   ↓
Validate: ✓ Not blocked, valid domain
                   ↓
Result: https://gypsyfoods.in/
                   ↓
Email extraction: ✓ Website valid, extract emails
Result: ["contact@gypsyfoods.in", ...]
```

### Example 2: Restaurant with Provider URL
```
Raw URL collected: https://google.com/viewer/chooseprovider?mid=/g/1td74zyg&...
                   ↓
Filter: ✗ 'google.com/viewer' is blocked
                   ↓
Fallback to pattern matching: ✗ No patterns found
                   ↓
Result: None
                   ↓
Email extraction: ✗ Cannot extract without website
Result: []
```

---

## Known Issues & Limitations

### Issue 1: Provider Chooser URLs
**Problem**: Some Google Maps listings return provider chooser URLs without parseable 'q=' parameter
**Affected URLs**: `https://google.com/viewer/chooseprovider?mid=...`
**Solution**: Fallback to pattern-based extraction from page text
**Workaround**: Manually inspect page for alternative website indicators

### Issue 2: Email Extraction Dependency
**By Design**: Email extraction ONLY works if website extraction succeeds
**Reason**: Safety gate prevents Google URL access
**Solution**: Fix website extraction first (Tier 2)

### Issue 3: Image Extraction Performance
**Problem**: 6-phase strategy takes 8-15 seconds
**Reason**: Gallery interaction + scroll + click operations
**Optimization**: Skip image extraction if not needed (`include_reviews=False`)

---

## Usage Examples

### Basic Website Extraction
```python
from bob import HybridExtractorOptimized

extractor = HybridExtractorOptimized()
result = extractor.extract_business("Gypsy Vegetarian Restaurant Jodhpur")

if result['success']:
    print(f"Website: {result.get('website')}")
    print(f"Emails: {result.get('emails', [])}")
```

### Fast Playwright Only
```python
from bob.extractors.playwright_optimized import PlaywrightExtractorOptimized

extractor = PlaywrightExtractorOptimized()
result = extractor.extract_business_optimized("Business Name")
```

### Reliable Selenium Fallback
```python
from bob.extractors.selenium_optimized import SeleniumExtractorOptimized

extractor = SeleniumExtractorOptimized()
result = extractor.extract_business_optimized("Business Name")
```

---

## Debugging

### Check What Website Was Extracted
```bash
python test_website_extraction_debug.py
```

This shows:
- Website URL returned
- Whether it's a Google URL
- Type of Google URL (if applicable)
- Actual URL if it's a redirect

### Manual Inspection
Check browser console to see:
1. Raw href values from CSS selectors
2. Page text content for pattern matching
3. Network requests to website domain

---

## Architecture Strengths

1. **Multi-layered**: Selector → Filtering → Validation → Email extraction
2. **Smart filtering**: 45+ blocked keywords prevent intermediary sites
3. **Fallback strategies**: Pattern matching if selectors fail
4. **Google redirect parsing**: Handles common Google URL format
5. **Safety gates**: Prevents invalid email extraction
6. **Highly optimized**: Multiple extractor variants for different needs

---

## Next Steps for Development

### To Improve Website Extraction:
1. Add support for additional Google redirect formats
2. Implement machine learning for URL confidence scoring
3. Cache known provider patterns for faster filtering
4. Add website title extraction as validation metric

### To Improve Email Extraction:
1. Add sitemap.xml parsing
2. Implement contact page detection
3. Add whois lookup for domain owner emails
4. Support for alternative contact methods (phone, form)

### To Improve Image Extraction:
1. Make gallery interaction optional
2. Add parallel phase execution
3. Implement smart scroll detection
4. Add image quality scoring

---

## Key Files You'll Need

### Must Know (Core Logic)
- `/Users/apple31/16 Nov 2025/BOB-Google-Maps/bob/utils/website_extractor.py`
- `/Users/apple31/16 Nov 2025/BOB-Google-Maps/bob/utils/email_extractor.py`
- `/Users/apple31/16 Nov 2025/BOB-Google-Maps/bob/extractors/playwright_optimized.py`
- `/Users/apple31/16 Nov 2025/BOB-Google-Maps/bob/extractors/selenium_optimized.py`

### Good to Know (Implementation Details)
- `/Users/apple31/16 Nov 2025/BOB-Google-Maps/bob/extractors/hybrid_optimized.py`
- `/Users/apple31/16 Nov 2025/BOB-Google-Maps/bob/utils/image_extractor.py`
- `/Users/apple31/16 Nov 2025/BOB-Google-Maps/bob/utils/images.py`

### For Testing
- `/Users/apple31/16 Nov 2025/BOB-Google-Maps/test_website_extraction_debug.py`
- `/Users/apple31/16 Nov 2025/BOB-Google-Maps/tests/realistic/`

---

## Document Files

1. **This file**: Quick reference and executive summary
2. **BOB_WEBSITE_EXTRACTION_ARCHITECTURE.md**: Complete technical architecture (26 KB)
3. **WEBSITE_EXTRACTION_VISUAL_MAP.txt**: Visual ASCII diagrams (41 KB)

---

**Version**: BOB-Google-Maps v4.2.1
**Last Updated**: November 15, 2025
**Author**: Comprehensive codebase exploration
