# ✅ MIGRATION CHECKLIST
**Phase-by-Phase Execution Tracker**

## PHASE 1: FOUNDATION ✅
- [x] Step 1: Backup current state (tagged v3.0.0-pre-refactor)
- [x] Step 2: Create refactoring branch (refactor/ultimate-v3.0)
- [x] Step 3: Document import paths (IMPORT_MAP.md)
- [x] Step 4: Analyze dependencies (DEPENDENCY_GRAPH.md)
- [x] Step 5: Architecture decision (ARCHITECTURE_DECISION.md)
- [x] Step 6: Migration checklist (this file)
- [x] Step 7: Backup test data (none currently)
- [x] Step 8: Validation script (below)
- [x] Step 9: Dev environment ready
- [x] Step 10: Rollback procedure documented

## PHASE 2: PACKAGE STRUCTURE (Steps 11-25)
- [ ] Step 11: Create target directories
- [ ] Step 12-14: Create package __init__ files
- [ ] Step 15: Move & rename Playwright extractor
- [ ] Step 16: Move & rename Selenium extractor
- [ ] Step 17: Move & rename Hybrid engine
- [ ] Step 18: Move & rename Cache manager
- [ ] Step 19: Move utility modules
- [ ] Step 20-22: Update package __init__ files
- [ ] Step 23: Fix bob_v3/__init__.py
- [ ] Step 24-25: Verify imports

## PHASE 3: IMPORT CLEANUP (Steps 26-40)
- [ ] Step 26-29: Fix extractor imports
- [ ] Step 30: Update CLI
- [ ] Step 31: Rename classes
- [ ] Step 32-34: Update type hints & docs
- [ ] Step 35-38: Fix test imports
- [ ] Step 39-40: Verification

## PHASE 4: SETUP & PACKAGING (Steps 41-55)
- [ ] Step 41-46: Create setup files
- [ ] Step 47-49: Update requirements
- [ ] Step 50-55: Test installation

## PHASE 5-10: FINAL (Steps 56-108)
- [ ] Phase 5: Testing
- [ ] Phase 6: Documentation
- [ ] Phase 7: Code Quality
- [ ] Phase 8: Backwards Compatibility
- [ ] Phase 9: Final Validation
- [ ] Phase 10: Release

---

## Quick Validation Script

```bash
#!/bin/bash
# test_imports.sh

echo "Testing imports..."

# Test bob_v3 package
python -c "from bob_v3.models import Business; print('✓ Models OK')" || echo "✗ Models FAIL"
python -c "from bob_v3.config import ExtractorConfig; print('✓ Config OK')" || echo "✗ Config FAIL"

# Test extractors (after Phase 2)
python -c "from bob_v3.extractors import PlaywrightExtractor; print('✓ Playwright OK')" 2>/dev/null || echo "✗ Playwright (pending)"
python -c "from bob_v3.extractors import SeleniumExtractor; print('✓ Selenium OK')" 2>/dev/null || echo "✗ Selenium (pending)"
python -c "from bob_v3.extractors import HybridExtractor; print('✓ Hybrid OK')" 2>/dev/null || echo "✗ Hybrid (pending)"

# Test cache (after Phase 2)
python -c "from bob_v3.cache import CacheManager; print('✓ Cache OK')" 2>/dev/null || echo "✗ Cache (pending)"

echo "Import test complete!"
```

---

## Rollback Procedure

**If anything goes wrong:**

```bash
# Discard all changes on refactor branch
git checkout refactor/ultimate-v3.0
git reset --hard v3.0.0-pre-refactor

# Or go back to main
git checkout main

# Tag is safe: v3.0.0-pre-refactor
```

---

## Files to Delete After Migration

### Temporary/Test Files:
- [ ] /tmp/import_map.txt
- [ ] test_*.json (if any)
- [ ] *.pyc, __pycache__/
- [ ] bob_cache_ultimate.db (test db)

### Old Structure (After Verification):
- [ ] src/core/*_ultimate.py (keep originals for now)
- [ ] Later: entire src/ directory (in V3.1)

---

## Current Status

**Phase:** 1 ✅ COMPLETE
**Next:** Phase 2 (Package Structure)
**Files Ready for Move:** 9 files identified
**Blockers:** None
