# 📍 IMPORT MAP - Current State
**Generated:** October 4, 2025 (Pre-Refactor)

## Purpose
Document all import paths before refactoring to ensure nothing breaks.

## Import Analysis

### BOB V3 Package Imports (`bob_v3/`)

#### `bob_v3/__init__.py` (BROKEN ❌)
```python
from .extractors import PlaywrightExtractor, SeleniumExtractor, HybridExtractor  # ❌ Doesn't exist
from .cache import CacheManager  # ❌ Doesn't exist
from .models import Business, Review, Image  # ✅ Works
```

**Status:** BROKEN - extractors and cache modules don't exist

#### `bob_v3/models/business.py` ✅
```python
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
```

**Status:** Good - standard library only

#### `bob_v3/models/review.py` ✅
```python
from dataclasses import dataclass
from typing import Optional
```

**Status:** Good - standard library only

#### `bob_v3/models/image.py` ✅
```python
from dataclasses import dataclass
from typing import Optional
```

**Status:** Good - standard library only

#### `bob_v3/config/settings.py` ✅
```python
from dataclasses import dataclass, field
from typing import Optional, List
import os
from pathlib import Path
```

**Status:** Good - standard library only

---

### Core Extractors (`src/core/`)

#### `src/core/hybrid_engine_ultimate.py` ⚠️
```python
import asyncio
from .cache_manager_ultimate import CacheManagerUltimate  # Relative
from .playwright_extractor_ultimate import PlaywrightExtractorUltimate  # Relative
from .google_maps_extractor_v2_ultimate import GoogleMapsExtractorV2Ultimate  # Relative
```

**Issues:**
- Relative imports (`.` notation)
- Works only when imported as `from core.`
- Class names have "Ultimate" suffix

#### `src/core/playwright_extractor_ultimate.py` ✅
```python
import asyncio
import re
import json
import time
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
from urllib.parse import unquote
```

**Status:** Good - no internal dependencies

#### `src/core/google_maps_extractor_v2_ultimate.py` ⚠️
```python
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# ... selenium imports
from .place_id_extractor import PlaceIDExtractor  # Relative
from .place_id_converter import enhance_place_id  # Relative
from .advanced_image_extractor import AdvancedImageExtractor  # Relative
```

**Issues:**
- Relative imports for utilities
- Depends on 3 utility modules

#### `src/core/cache_manager_ultimate.py` ✅
```python
import sqlite3
import json
import time
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
```

**Status:** Good - no internal dependencies

---

### CLI Files

#### `bob_maps_ultimate.py` ✅
```python
import sys
import os
import argparse
import json
import time

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from core.hybrid_engine_ultimate import HybridEngineUltimate  # Works via sys.path
```

**Status:** Works but uses sys.path hack

#### `bob_maps.py` (Legacy V1.0) ✅
```python
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from core.google_maps_extractor import GoogleMapsExtractor
```

**Status:** Legacy, works fine

---

### Test Files

#### `tests/conftest.py` ⚠️
```python
import pytest
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from bob_v3.config import ExtractorConfig, CacheConfig, ParallelConfig  # ✅ Works
```

**Issues:** Uses sys.path hack

#### `tests/unit/test_models.py` ✅
```python
import pytest
from datetime import datetime
from bob_v3.models import Business, Review, Image  # Works
```

**Status:** Good

#### `tests/unit/test_config.py` ✅
```python
import pytest
import os
from bob_v3.config import ExtractorConfig, CacheConfig, ParallelConfig  # Works
```

**Status:** Good

#### `tests/integration/test_cache_manager.py` ❌
```python
import pytest
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src" / "core"))

from cache_manager_ultimate import CacheManager  # ❌ Wrong - expects CacheManagerUltimate
from bob_v3.models import Business, Review
```

**Issues:**
- Wrong class name (CacheManager vs CacheManagerUltimate)
- sys.path hacks

#### `tests/e2e/test_real_extraction.py` ❌
```python
import pytest
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src" / "core"))

from hybrid_engine_ultimate import HybridExtractor  # ❌ Wrong - expects HybridEngineUltimate
```

**Issues:**
- Wrong class name
- sys.path hacks

---

## Summary

### ✅ Working Imports (7 files)
1. `bob_v3/models/business.py`
2. `bob_v3/models/review.py`
3. `bob_v3/models/image.py`
4. `bob_v3/config/settings.py`
5. `bob_maps_ultimate.py` (with sys.path hack)
6. `tests/unit/test_models.py`
7. `tests/unit/test_config.py`

### ❌ Broken Imports (4 files)
1. `bob_v3/__init__.py` - Tries to import non-existent modules
2. `tests/integration/test_cache_manager.py` - Wrong class name
3. `tests/e2e/test_real_extraction.py` - Wrong class name
4. Any code trying `from bob_v3 import PlaywrightExtractor`

### ⚠️ Problematic (Uses Hacks - 3 files)
1. `src/core/hybrid_engine_ultimate.py` - Relative imports
2. `src/core/google_maps_extractor_v2_ultimate.py` - Relative imports
3. `tests/conftest.py` - sys.path manipulation

---

## Fix Strategy

### Phase 2: Move extractors to proper locations
- `src/core/playwright_extractor_ultimate.py` → `bob_v3/extractors/playwright.py`
- `src/core/google_maps_extractor_v2_ultimate.py` → `bob_v3/extractors/selenium.py`
- `src/core/hybrid_engine_ultimate.py` → `bob_v3/extractors/hybrid.py`
- `src/core/cache_manager_ultimate.py` → `bob_v3/cache/manager.py`

### Phase 3: Update all imports to absolute
- Change `.cache_manager_ultimate` → `bob_v3.cache.manager`
- Change `.playwright_extractor_ultimate` → `bob_v3.extractors.playwright`
- Remove all sys.path hacks

### Phase 4: Rename classes
- `PlaywrightExtractorUltimate` → `PlaywrightExtractor`
- `GoogleMapsExtractorV2Ultimate` → `SeleniumExtractor`
- `HybridEngineUltimate` → `HybridExtractor`
- `CacheManagerUltimate` → `CacheManager`

---

**Next Steps:** Proceed with Step 4 (Dependency Analysis)
