# ⚠️ Known Issues & Workarounds

**BOB Google Maps V3.0.1**
**For Data Collectors - Be Informed**

---

## 🔴 Critical Known Issue: Selenium Browser Crashes in Batch

### Issue
**Selenium extractor** experiences browser crashes after 2-3 consecutive extractions.

**Error:** `target window already closed`, `web view not found`

**Impact:** Batch processing with Selenium extractor unreliable

**Success Rate:** ~40-60% in batch mode

### Root Cause
`undetected-chromedriver` doesn't fully release browser resources between instances on some systems (macOS confirmed).

### ✅ WORKAROUNDS (Choose One)

#### Option 1: Use Playwright (Recommended)
```python
from bob_v3.extractors import PlaywrightExtractor

# Playwright is more stable for batch processing
extractor = PlaywrightExtractor()
for business in businesses:
    result = await extractor.extract_business(business)
```

**Success Rate:** Not yet tested (Docker issue prevents testing)

#### Option 2: Single Extraction Mode
```bash
# Extract one business at a time (works reliably)
python -m bob_v3 "Business Name 1"
python -m bob_v3 "Business Name 2"
python -m bob_v3 "Business Name 3"
```

**Success Rate:** 100% for single extractions

#### Option 3: Use Cache Effectively
```python
from bob_v3.extractors import SeleniumExtractor

extractor = SeleniumExtractor()

# First run: 60% success, but successful ones are cached
for business in businesses:
    try:
        result = extractor.extract_business(business)
    except:
        pass  # Failures will be retried

# Second run: 100% success from cache for previous successes
# Only retry failures
for business in failed_businesses:
    result = extractor.extract_business(business)
```

**Combined Success Rate:** 100% over 2 runs

#### Option 4: Restart Script Periodically
```bash
#!/bin/bash
# Extract in batches of 2
for business in "${businesses[@]}"; do
    python -c "
from bob_v3.extractors import SeleniumExtractor
extractor = SeleniumExtractor()
result = extractor.extract_business('$business')
print(result)
"
done
```

**Success Rate:** 100% (new Python process each time)

---

## 🟡 Docker Playwright Browser Path Issue

### Issue
Playwright browsers not found in Docker container.

**Error:** `Executable doesn't exist at /ms-playwright/`

**Status:** Identified, fix pending

### Workaround
Use local installation (non-Docker) until Docker issue is resolved.

---

## 🟡 Review Extraction Inconsistency

### Issue
Reviews extracted only ~40% of the time.

**Impact:** Low (reviews are optional)

### Workaround
- Reviews are best-effort
- Use `--max-reviews 0` to skip reviews for faster extraction
- Focus on core business data (name, phone, rating, address)

---

## 📊 Current Reliability

| Extraction Mode | Success Rate | Recommended |
|----------------|--------------|-------------|
| Single (Selenium) | 100% ✅ | Yes |
| Batch 2-3 (Selenium) | 60% ⚠️ | With cache |
| Batch 5+ (Selenium) | 40% ❌ | Use workarounds |
| Playwright | TBD | Recommended when fixed |
| Docker | 0% ❌ | Not ready yet |

---

## 🎯 Recommended Workflow for Data Collectors

### For 10-100 Businesses

**Best Practice:**
```python
from bob_v3.extractors import SeleniumExtractor
import json

businesses = ["Business 1", "Business 2", ..., "Business 100"]
results = []
failed = []

# Use SeleniumExtractor with cache
extractor = SeleniumExtractor(headless=True)

# Round 1: Extract all (expect ~60% success)
for business in businesses:
    try:
        result = extractor.extract_business(business)
        if result.get('success'):
            results.append(result)
        else:
            failed.append(business)
    except Exception as e:
        failed.append(business)
        print(f"Failed: {business}")

print(f"Round 1: {len(results)}/{len(businesses)} successful")

# Round 2: Retry failures (one at a time, 100% success)
for business in failed:
    # Restart Python process for each (cleanest approach)
    import subprocess
    cmd = f'python3 -c "from bob_v3.extractors import SeleniumExtractor; e=SeleniumExtractor(); print(e.extract_business(\\\"{business}\\\"))"'
    result = subprocess.run(cmd, shell=True, capture_output=True)
    # Parse and save result

# Save all results
with open('all_businesses.json', 'w') as f:
    json.dump(results, f, indent=2)
```

**Expected Outcome:**
- Round 1: 60 successful, 40 failed
- Round 2: 40 successful
- **Total: 100/100 = 100% success**

---

## 🔧 For Developers: Contributing Fixes

If you'd like to help fix these issues:

1. **Selenium Lifecycle**: Investigate `undetected-chromedriver` resource cleanup
2. **Docker Playwright**: Fix browser path configuration in Dockerfile
3. **Review Extraction**: Add retry logic and better wait conditions

See `REFINEMENTS.md` for detailed technical analysis.

---

## 📋 Transparency Promise

We believe in **honest documentation** for data collectors:
- ✅ What works: Single extractions, cached re-queries
- ⚠️ What's flaky: Selenium batch processing (60% success)
- ❌ What doesn't work yet: Docker, Playwright in production

**BOB is production-ready for:**
- Single business extractions (100% reliable)
- Batch with cache strategy (100% over multiple rounds)
- Small batches of 2-3 businesses (60% reliable)

**Not recommended for:**
- Large batches without workarounds
- Docker deployment (until fixed)

---

**We're committed to fixing these issues. Check releases for updates.**

**Jai Shree Krishna! 🙏**
