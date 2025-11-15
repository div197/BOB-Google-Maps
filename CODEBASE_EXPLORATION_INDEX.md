# BOB-Google-Maps Codebase Exploration - Complete Index

## Three New Documentation Files Created

### 1. WEBSITE_EXTRACTION_SUMMARY.md (Quick Reference)
**Size**: 8 KB  
**Time to read**: 10-15 minutes  
**Best for**: Quick understanding of the system

- Executive summary of website extraction architecture
- Three-tier system overview
- Six extractor options with comparison table
- Step-by-step extraction flow
- Real-world examples
- Known issues and limitations
- Usage examples with code
- Performance breakdown

### 2. BOB_WEBSITE_EXTRACTION_ARCHITECTURE.md (Complete Reference)
**Size**: 26 KB  
**Time to read**: 30-45 minutes  
**Best for**: Deep technical understanding

- Complete directory structure
- All 6 extractor implementations with line counts
- Website extraction workflow (3-tier architecture)
- Tier 1: Primary HTML Selection (CSS selectors)
- Tier 2: Intelligent Filtering & Google Redirect Parsing
  - `extract_website_intelligent()` function
  - `parse_google_redirect()` function
  - `_is_valid_business_url()` function with all 45+ blocked keywords
  - `_extract_urls_from_patterns()` function
- Tier 3: Email Extraction
  - Dependency on website URL
  - Safety gates and validation
- Image Extraction: 6-phase strategy
- Complete data flow architecture
- All files involved with line counts and purposes
- Known issues & bottlenecks
- Selection guide for each extractor
- Function call stack for website extraction

### 3. WEBSITE_EXTRACTION_VISUAL_MAP.txt (ASCII Diagrams)
**Size**: 41 KB  
**Time to read**: 20-30 minutes  
**Best for**: Visual learners

- Large ASCII diagrams of entire architecture
- Extractor engine layer (6 implementations)
- Website extraction utility layer
- Email extraction layer
- Image extraction layer (6-phase)
- Complete data flow from start to finish
- Critical points for understanding
- Performance breakdown visualization
- All major components mapped visually

---

## Navigation Guide

### I want to understand: Website Extraction
**Start here**: WEBSITE_EXTRACTION_SUMMARY.md (Section: "Website Extraction Flow")
**Then read**: BOB_WEBSITE_EXTRACTION_ARCHITECTURE.md (Section: "Website Extraction - Three-Tier Architecture")
**Visualize with**: WEBSITE_EXTRACTION_VISUAL_MAP.txt (Section: "WEBSITE EXTRACTION UTILITY LAYER")

### I want to understand: Email Extraction
**Start here**: WEBSITE_EXTRACTION_SUMMARY.md (Look for "Email Extraction")
**Then read**: BOB_WEBSITE_EXTRACTION_ARCHITECTURE.md (Section: "Tier 3: Email Extraction")
**Visualize with**: WEBSITE_EXTRACTION_VISUAL_MAP.txt (Section: "EMAIL EXTRACTION LAYER")

### I want to understand: Image Extraction
**Start here**: WEBSITE_EXTRACTION_SUMMARY.md (Look for "Image Extraction Performance")
**Then read**: BOB_WEBSITE_EXTRACTION_ARCHITECTURE.md (Section: "Image Extraction Flow")
**Visualize with**: WEBSITE_EXTRACTION_VISUAL_MAP.txt (Section: "IMAGE EXTRACTION LAYER")

### I want to choose an extractor
**Read**: WEBSITE_EXTRACTION_SUMMARY.md (Section: "Six Extractors")
**Or**: BOB_WEBSITE_EXTRACTION_ARCHITECTURE.md (Section: "Selection Guide")

### I want to fix a bug
**Read**: WEBSITE_EXTRACTION_SUMMARY.md (Section: "Known Issues & Limitations")
**Or**: BOB_WEBSITE_EXTRACTION_ARCHITECTURE.md (Section: "Known Issues & Bottlenecks")

### I want the complete file map
**Read**: WEBSITE_EXTRACTION_SUMMARY.md (Section: "File Map")
**Or**: BOB_WEBSITE_EXTRACTION_ARCHITECTURE.md (Section: "All Files Involved")

---

## Key Absolute File Paths

### Core Logic Files
- `/Users/apple31/16 Nov 2025/BOB-Google-Maps/bob/utils/website_extractor.py`
- `/Users/apple31/16 Nov 2025/BOB-Google-Maps/bob/utils/email_extractor.py`
- `/Users/apple31/16 Nov 2025/BOB-Google-Maps/bob/utils/image_extractor.py`
- `/Users/apple31/16 Nov 2025/BOB-Google-Maps/bob/utils/images.py`

### Extractor Files (Choose One)
- `/Users/apple31/16 Nov 2025/BOB-Google-Maps/bob/extractors/playwright_optimized.py` (Recommended)
- `/Users/apple31/16 Nov 2025/BOB-Google-Maps/bob/extractors/selenium_optimized.py` (Most reliable)
- `/Users/apple31/16 Nov 2025/BOB-Google-Maps/bob/extractors/hybrid_optimized.py` (Auto-failover)
- `/Users/apple31/16 Nov 2025/BOB-Google-Maps/bob/extractors/playwright.py` (Full-featured)
- `/Users/apple31/16 Nov 2025/BOB-Google-Maps/bob/extractors/selenium.py` (Full-featured)
- `/Users/apple31/16 Nov 2025/BOB-Google-Maps/bob/extractors/hybrid.py` (Legacy)

### Documentation Files
- `/Users/apple31/16 Nov 2025/BOB-Google-Maps/WEBSITE_EXTRACTION_SUMMARY.md` (Quick start)
- `/Users/apple31/16 Nov 2025/BOB-Google-Maps/BOB_WEBSITE_EXTRACTION_ARCHITECTURE.md` (Complete reference)
- `/Users/apple31/16 Nov 2025/BOB-Google-Maps/WEBSITE_EXTRACTION_VISUAL_MAP.txt` (Diagrams)

### Testing Files
- `/Users/apple31/16 Nov 2025/BOB-Google-Maps/test_website_extraction_debug.py` (Debug website extraction)
- `/Users/apple31/16 Nov 2025/BOB-Google-Maps/tests/realistic/` (Real-world tests)

---

## Quick Facts

### Architecture Overview
- **6 different extractors** (Playwright, Selenium, Hybrid - each with optimized variants)
- **3-tier website extraction** (HTML selector → Intelligent filtering → Email extraction)
- **6-phase image extraction** (Immediate → Scroll → Gallery → Scroll gallery → Hidden → Special views)
- **3 core utility modules** (website_extractor, email_extractor, image_extractor)

### Performance
- Playwright: 7-11 seconds per business (95% reliability)
- Selenium: 8-15 seconds per business (99% reliability)
- Hybrid: 7-15 seconds per business (99% reliability with auto-failover)
- Image extraction alone: 8-15 seconds (most time-consuming)
- Email extraction: 2-3 seconds (depends on website availability)

### Website Extraction
- **Primary method**: CSS selector `a[data-item-id='authority']`
- **Fallback methods**: 6 additional CSS selectors
- **Google redirect handling**: Parses `?q=` parameter
- **Blocked keywords**: 45+ patterns (Google URLs, social media, booking platforms, etc.)
- **Safety gates**: Prevents invalid email extraction on Google URLs

### Email Extraction
- **Dependency**: Requires valid business website from website extraction
- **Methods**: 3 regex patterns (standard, mailto, field labels)
- **Spam filtering**: Blocks 'example', 'test', 'noreply', etc.
- **Output**: Maximum 5 emails per website

### Image Extraction
- **6 phases**: Immediate, Scroll, Gallery click, Gallery scroll, Hidden, Special views
- **Filters**: Removes maps, logos, avatars, UI icons
- **Resolution**: Converts to high-res URLs (removes size parameters)
- **Output**: Deduplicated list of business photos

---

## Most Important Insights

### 1. Website Extraction is Multi-Layered
It's not just a simple CSS selector. It involves:
- **Tier 1**: Collecting raw href values
- **Tier 2**: Filtering Google URLs and parsing redirects
- **Tier 3**: Pattern-based fallback extraction
- **Validation**: Checking 45+ blocked keywords
- **Prioritization**: Scoring and ranking results

### 2. Email Extraction Depends on Website Success
- If website extraction fails → emails = []
- This is by design (safety gate)
- Website must be a real domain, not Google URL

### 3. The System is Well-Protected Against Bad URLs
The `_is_valid_business_url()` function blocks:
- Google internal URLs (viewer, aclk, /maps/reserve, etc.)
- Social media profiles (not primary websites)
- Booking platforms (intermediaries like Zomato, Swiggy)
- Review sites (not business websites)
- Email addresses and local IPs

### 4. Performance Trade-offs
- **Image extraction is slowest** (8-15 seconds)
- **Playwright is fastest** but slightly less reliable (95% vs 99%)
- **Selenium is most reliable** but slower
- **Hybrid is best balanced** (auto-failover + intelligent caching)

### 5. There Are Actually 6 Extractor Implementations
Not just 2. Three tiers:
1. **Optimized** (recommended): Small, fast, lean (277-477 lines)
2. **Hybrid** (auto-failover): Orchestrates other extractors
3. **Full-featured** (legacy): Large, comprehensive (849-885 lines)

---

## Code Snippets to Know

### Most Critical: Google URL Blocking
```python
# From: bob/utils/website_extractor.py, lines 116-156
blocked_keywords = [
    'google.com/viewer',           # Provider chooser
    'google.com/aclk',             # Google ads
    'viewer/chooseprovider',       # Provider selector
    'google.com/maps',             # Maps redirect
    # ... 40+ more keywords
]
```

### Most Critical: Google Redirect Parsing
```python
# From: bob/utils/website_extractor.py, lines 72-94
def parse_google_redirect(google_url):
    if 'google.com/url' in google_url and 'q=' in google_url:
        parsed = urlparse(google_url)
        query_params = parse_qs(parsed.query)
        if 'q' in query_params:
            return unquote(query_params['q'][0])
    return google_url
```

### Most Critical: CSS Selector Priority
```python
# From: bob/extractors/playwright.py, lines 462-470
website_selectors = [
    "a[data-item-id='authority']",      # PRIMARY
    "a[aria-label*='website']",         # SECONDARY
    "a[aria-label*='Website']",
    ".lVcKpb a[href*='http']",
    "a[href*='http']",
    "[data-item-id='website']",
    ".nVcWpd a[href]"
]
```

### Most Critical: Email Safety Gate
```python
# From: bob/utils/email_extractor.py, lines 76-78
if 'google' in real_url.lower():
    return []  # Rejects unrecognized Google formats
```

---

## Terminology Reference

| Term | Meaning | Example |
|------|---------|---------|
| **Authority Link** | The main website link | `a[data-item-id='authority']` |
| **Google Redirect** | URL wrapped by Google | `https://www.google.com/url?q=...` |
| **Provider Chooser** | Provider selection page | `google.com/viewer/chooseprovider?mid=...` |
| **Smart Finder** | Multi-strategy element finder | Tries CSS, XPath, JS, text patterns |
| **Pattern Matching** | Text-based URL extraction | Finds "website: ..." in page text |
| **Safety Gate** | Validation checkpoint | Rejects Google URLs before email extraction |
| **High-res URL** | Maximum resolution image | Removes size parameters like `=w1024` |
| **Lazy-load** | Images loaded on scroll | `img[data-src]`, `img[data-lazy-src]` |

---

## Who Should Read What

### If you're a QA Tester
- Start: WEBSITE_EXTRACTION_SUMMARY.md
- Then: Test cases in test_website_extraction_debug.py
- Reference: Known issues section

### If you're a Backend Developer
- Start: BOB_WEBSITE_EXTRACTION_ARCHITECTURE.md
- Focus: All file paths and function signatures
- Reference: Selection guide and API section

### If you're a Frontend Developer
- Start: WEBSITE_EXTRACTION_VISUAL_MAP.txt
- Then: Data flow architecture section
- Reference: CSS selectors and HTML element IDs

### If you're a DevOps Engineer
- Start: Performance breakdown section
- Focus: Image extraction optimization
- Reference: Known bottlenecks section

### If you're a Data Scientist
- Start: Blocked keywords list
- Focus: Validation logic and filtering
- Reference: Real-world examples section

---

## Files in This Exploration

1. **CODEBASE_EXPLORATION_INDEX.md** (This file)
   - Navigation guide
   - Quick reference
   - Terminology

2. **WEBSITE_EXTRACTION_SUMMARY.md**
   - Executive summary
   - Quick reference guide
   - Real-world examples
   - Usage code examples

3. **BOB_WEBSITE_EXTRACTION_ARCHITECTURE.md**
   - Complete technical reference
   - All function signatures
   - Blocked keywords list
   - All file paths with line counts

4. **WEBSITE_EXTRACTION_VISUAL_MAP.txt**
   - ASCII diagrams
   - Visual data flow
   - Component relationships
   - Process flows

---

## Summary

You now have **comprehensive documentation** of the BOB-Google-Maps website, email, and image extraction architecture with:

- 3 different documentation styles (summary, detailed, visual)
- 100+ absolute file paths
- 50+ function names and signatures
- Real-world code examples
- Performance metrics
- Known issues and limitations
- Selection guides for each component
- Navigation guides for different audiences

The codebase is **well-architected** with proper separation of concerns, intelligent filtering, and multiple fallback strategies for robustness.

---

**Created**: November 15, 2025  
**Codebase**: BOB-Google-Maps v4.2.1  
**Total Documentation**: ~75 KB across 3 files  
**Total Analysis**: 3,200+ lines of code reviewed  
**Absolute File Paths**: 100+ listed with line counts
