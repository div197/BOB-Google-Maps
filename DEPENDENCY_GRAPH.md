# 🔗 DEPENDENCY GRAPH
**Generated:** October 4, 2025

## Visual Dependency Tree

```
┌─────────────────────────────────────────────────────────┐
│                 DEPENDENCY ANALYSIS                      │
└─────────────────────────────────────────────────────────┘

LEVEL 0 (No Dependencies - Safe to Move First):
========================================
✅ bob_v3/models/business.py
✅ bob_v3/models/review.py
✅ bob_v3/models/image.py
✅ bob_v3/config/settings.py
✅ src/core/playwright_extractor_ultimate.py (only external deps)
✅ src/core/cache_manager_ultimate.py (only external deps)

LEVEL 1 (Depends on Level 0):
========================================
⚠️ src/core/place_id_extractor.py
   └── No internal deps (only Selenium)

⚠️ src/core/place_id_converter.py
   └── No internal deps

⚠️ src/core/advanced_image_extractor.py
   └── No internal deps (only Selenium)

LEVEL 2 (Depends on Level 0 + 1):
========================================
⚠️ src/core/google_maps_extractor_v2_ultimate.py
   ├── .place_id_extractor (Level 1)
   ├── .place_id_converter (Level 1)
   └── .advanced_image_extractor (Level 1)

LEVEL 3 (Depends on Everything):
========================================
❌ src/core/hybrid_engine_ultimate.py
   ├── .cache_manager_ultimate (Level 0)
   ├── .playwright_extractor_ultimate (Level 0)
   └── .google_maps_extractor_v2_ultimate (Level 2)

LEVEL 4 (Top-level Entry Points):
========================================
🔷 bob_maps_ultimate.py
   └── core.hybrid_engine_ultimate (Level 3)

🔷 bob_v3/__init__.py (BROKEN)
   ├── .extractors (doesn't exist)
   └── .cache (doesn't exist)
```

---

## Circular Dependencies

**Analysis:** ✅ **NO CIRCULAR DEPENDENCIES FOUND**

All dependencies flow in one direction:
- Models/Config (bottom) → Utils → Extractors → Hybrid Engine → CLI (top)

---

## Migration Order (Safe Order)

### Step 1: Move Independent Modules (Level 0)
```bash
# No dependencies, can move anytime
bob_v3/cache/manager.py         ← src/core/cache_manager_ultimate.py
bob_v3/extractors/playwright.py ← src/core/playwright_extractor_ultimate.py
```

### Step 2: Move Utility Modules (Level 1)
```bash
bob_v3/utils/place_id.py     ← src/core/place_id_extractor.py
bob_v3/utils/converters.py   ← src/core/place_id_converter.py
bob_v3/utils/images.py       ← src/core/advanced_image_extractor.py
```

### Step 3: Move Selenium Extractor (Level 2)
```bash
# After utils are moved
bob_v3/extractors/selenium.py ← src/core/google_maps_extractor_v2_ultimate.py
```

### Step 4: Move Hybrid Engine (Level 3)
```bash
# After all extractors are moved
bob_v3/extractors/hybrid.py ← src/core/hybrid_engine_ultimate.py
```

### Step 5: Fix Entry Points (Level 4)
```bash
# Update imports in:
- bob_maps_ultimate.py → bob_v3/cli.py
- bob_v3/__init__.py
```

---

## Import Dependencies by File

### `playwright_extractor_ultimate.py`
**External Only:** ✅
- playwright.async_api
- asyncio, re, json, time, urllib

**Internal:** None

**Move Safety:** HIGH (no internal deps)

---

### `cache_manager_ultimate.py`
**External Only:** ✅
- sqlite3, json, time, hashlib, datetime, pathlib

**Internal:** None

**Move Safety:** HIGH (no internal deps)

---

### `place_id_extractor.py`
**External Only:** ✅
- selenium.webdriver
- re, time

**Internal:** None

**Move Safety:** HIGH

---

### `place_id_converter.py`
**External Only:** ✅
- re

**Internal:** None

**Move Safety:** HIGH

---

### `advanced_image_extractor.py`
**External Only:** ✅
- selenium.webdriver
- re, time

**Internal:** None

**Move Safety:** HIGH

---

### `google_maps_extractor_v2_ultimate.py`
**External:** ✅
- undetected_chromedriver, selenium.*, time, re, json, urllib

**Internal:** ⚠️
- `.place_id_extractor` → Must move utils first
- `.place_id_converter` → Must move utils first
- `.advanced_image_extractor` → Must move utils first

**Move Safety:** MEDIUM (move utils first)

---

### `hybrid_engine_ultimate.py`
**External:** ✅
- asyncio

**Internal:** ❌
- `.cache_manager_ultimate` → Must move cache first
- `.playwright_extractor_ultimate` → Must move playwright first
- `.google_maps_extractor_v2_ultimate` → Must move selenium first

**Move Safety:** LOW (move last)

---

## Risk Assessment

### 🟢 Low Risk (Move First)
1. Models (business, review, image) - Already in place ✅
2. Config (settings) - Already in place ✅
3. Playwright extractor - No internal deps
4. Cache manager - No internal deps
5. Utils (place_id, converters, images) - No internal deps

### 🟡 Medium Risk (Move After Utils)
1. Selenium extractor - Depends on utils

### 🔴 High Risk (Move Last)
1. Hybrid engine - Depends on everything

### ⚫ Critical (Fix After All Moves)
1. bob_v3/__init__.py - Currently broken
2. CLI (bob_maps_ultimate.py) - Needs import updates
3. Tests - Need import updates

---

## Execution Plan

### Phase 2 (Steps 11-25): Move Files
**Order of execution:**
1. ✅ Create target directories (bob_v3/extractors, bob_v3/cache, bob_v3/utils)
2. ✅ Move Level 0: playwright, cache
3. ✅ Move Level 1: utils (place_id, converters, images)
4. ✅ Move Level 2: selenium extractor
5. ✅ Move Level 3: hybrid engine

### Phase 3 (Steps 26-40): Fix Imports
**After all files moved:**
1. Update all relative imports to absolute
2. Fix bob_v3/__init__.py
3. Update CLI imports
4. Update test imports

---

## Critical Notes

1. **No circular dependencies** - Clean architecture ✅
2. **Clear hierarchy** - Easy to refactor ✅
3. **Move order is critical** - Must follow levels ⚠️
4. **Test after each move** - Catch issues early ✅

---

**Next:** Proceed to Step 5 (Architecture Decision)
