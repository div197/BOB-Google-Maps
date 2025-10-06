# 🏗️ ARCHITECTURE DECISION RECORD
**Date:** October 4, 2025
**Status:** ✅ APPROVED
**Deciders:** Divyanshu Singh Chouhan (Author), Claude Code (Technical Analysis)

---

## Context

BOB V3.0 has extractors in `src/core/` but package structure expects them in `bob_v3/extractors/`. This causes broken imports and prevents pip installation.

---

## Decision

**APPROVED: Option A - Move Everything to bob_v3/***

### Final Structure:
```
bob_v3/
├── __init__.py              # Clean package exports
├── cli.py                   # Moved from bob_maps_ultimate.py
├── extractors/
│   ├── __init__.py
│   ├── playwright.py        # Moved from src/core/playwright_extractor_ultimate.py
│   ├── selenium.py          # Moved from src/core/google_maps_extractor_v2_ultimate.py
│   └── hybrid.py            # Moved from src/core/hybrid_engine_ultimate.py
├── cache/
│   ├── __init__.py
│   └── manager.py           # Moved from src/core/cache_manager_ultimate.py
├── utils/
│   ├── __init__.py
│   ├── place_id.py          # Moved from src/core/place_id_extractor.py
│   ├── converters.py        # Moved from src/core/place_id_converter.py
│   └── images.py            # Moved from src/core/advanced_image_extractor.py
├── models/                  # Already exists ✅
│   ├── __init__.py
│   ├── business.py
│   ├── review.py
│   └── image.py
└── config/                  # Already exists ✅
    ├── __init__.py
    └── settings.py
```

---

## Rationale

### ✅ Advantages of Option A:

1. **Standard Python Package Structure**
   - Follows Python packaging conventions
   - Pip installable
   - Clean imports: `from bob_v3.extractors import PlaywrightExtractor`

2. **No sys.path Hacks**
   - Absolute imports throughout
   - Works in any environment
   - No path manipulation needed

3. **Clear Namespace**
   - `bob_v3` is the single source
   - No confusion about location
   - IDE autocomplete works perfectly

4. **Maintainability**
   - Easier for new contributors
   - Standard Python practices
   - Better tooling support

5. **Distribution Ready**
   - Can create wheel/sdist
   - PyPI publishable
   - Docker friendly

---

## Alternatives Considered

### ❌ Option B: Keep in src/core with Wrappers
**Rejected because:**
- Confusing dual structure
- Import complexity
- Not Pythonic
- Harder to maintain

### ❌ Option C: Symlinks
**Rejected because:**
- Windows compatibility issues
- Git doesn't track symlink content
- Confusing for contributors

---

## Class Naming Decision

**DECISION: Remove "Ultimate" Suffix**

### Renaming:
| Old Name | New Name |
|----------|----------|
| `PlaywrightExtractorUltimate` | `PlaywrightExtractor` |
| `GoogleMapsExtractorV2Ultimate` | `SeleniumExtractor` |
| `HybridEngineUltimate` | `HybridExtractor` |
| `CacheManagerUltimate` | `CacheManager` |

### Rationale:
- Cleaner, more professional names
- "Ultimate" is marketing, not technical
- Shorter import statements
- Standard Python naming

---

## Legacy Code Handling

### src/core/ Directory
**DECISION: Keep for now, mark deprecated**

**Rationale:**
- bob_maps.py (V1.0) still uses it
- Gradual deprecation
- Backwards compatibility

**Action:**
- Add deprecation warnings
- Document migration path
- Remove in V4.0

### bob_maps.py (V1.0 CLI)
**DECISION: Keep as legacy wrapper**

**Rationale:**
- Some users may depend on it
- Easy migration path
- No harm in keeping

---

## Import Strategy

### From Relative to Absolute:

**Before:**
```python
from .cache_manager_ultimate import CacheManagerUltimate
from .playwright_extractor_ultimate import PlaywrightExtractorUltimate
```

**After:**
```python
from bob_v3.cache import CacheManager
from bob_v3.extractors import PlaywrightExtractor
```

---

## Entry Points

### Package Entry Point:
```python
# bob_v3/__main__.py
from bob_v3.cli import main

if __name__ == "__main__":
    main()
```

### Console Script (setup.py):
```python
entry_points={
    'console_scripts': [
        'bob-maps=bob_v3.cli:main',
    ],
}
```

**Usage:**
```bash
# Module execution
python -m bob_v3 --help

# Console script (after pip install)
bob-maps --help
```

---

## Migration Checklist

- [ ] Create bob_v3/extractors/, bob_v3/cache/, bob_v3/utils/
- [ ] Move files (follow dependency order)
- [ ] Rename classes (remove Ultimate)
- [ ] Update imports (relative → absolute)
- [ ] Fix bob_v3/__init__.py
- [ ] Update CLI
- [ ] Fix tests
- [ ] Add setup.py/pyproject.toml
- [ ] Create __main__.py
- [ ] Test pip install
- [ ] Update docs

---

## Success Criteria

✅ All of these must work:

```bash
# Import test
python -c "from bob_v3 import PlaywrightExtractor; print('Success')"

# Pip install test
pip install -e .
python -c "import bob_v3; print(bob_v3.__version__)"

# CLI test
bob-maps --version

# Module test
python -m bob_v3 --help

# Test suite
pytest tests/ -v
```

---

## Risks & Mitigation

### Risk 1: Breaking Changes
**Mitigation:**
- Keep old code with deprecation warnings
- Provide migration guide
- Semantic versioning (3.0.0 → 3.0.1)

### Risk 2: Import Errors During Migration
**Mitigation:**
- Follow strict dependency order
- Test after each file move
- Git tags for rollback

### Risk 3: Test Failures
**Mitigation:**
- Fix imports in parallel with moves
- Run tests frequently
- Keep sys.path hacks temporarily if needed

---

## Timeline

**Estimated:** 4-6 hours
**Started:** October 4, 2025
**Target Completion:** Same day

**Phases:**
- Foundation: 30 mins (Steps 1-10) ✅ In Progress
- Package Structure: 1 hour (Steps 11-25)
- Import Cleanup: 1.5 hours (Steps 26-40)
- Setup & Packaging: 1 hour (Steps 41-55)
- Testing: 1 hour (Steps 56-70)
- Final: 1 hour (Steps 71-108)

---

## Approval

**Decision:** ✅ APPROVED
**Date:** October 4, 2025
**Next Step:** Execute Phase 2 (Package Structure)

---

**Jai Shree Krishna! 🙏**
*This architecture will serve BOB well for years to come.*
