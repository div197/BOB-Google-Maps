#!/bin/bash
# BOB V3.0 - Import Validation Script
# Tests that all imports work correctly

echo "🔍 BOB V3.0 Import Validation"
echo "=============================="
echo ""

# Test current working imports
echo "📦 Testing current package..."
python3 -c "from bob_v3.models import Business; print('  ✅ Models: Business')" || echo "  ❌ Models FAILED"
python3 -c "from bob_v3.models import Review; print('  ✅ Models: Review')" || echo "  ❌ Review FAILED"
python3 -c "from bob_v3.models import Image; print('  ✅ Models: Image')" || echo "  ❌ Image FAILED"
python3 -c "from bob_v3.config import ExtractorConfig; print('  ✅ Config: ExtractorConfig')" || echo "  ❌ Config FAILED"

echo ""
echo "🔧 Testing extractors (after Phase 2)..."
python3 -c "from bob_v3.extractors import PlaywrightExtractor; print('  ✅ PlaywrightExtractor')" 2>/dev/null || echo "  ⏳ PlaywrightExtractor (pending)"
python3 -c "from bob_v3.extractors import SeleniumExtractor; print('  ✅ SeleniumExtractor')" 2>/dev/null || echo "  ⏳ SeleniumExtractor (pending)"
python3 -c "from bob_v3.extractors import HybridExtractor; print('  ✅ HybridExtractor')" 2>/dev/null || echo "  ⏳ HybridExtractor (pending)"

echo ""
echo "💾 Testing cache (after Phase 2)..."
python3 -c "from bob_v3.cache import CacheManager; print('  ✅ CacheManager')" 2>/dev/null || echo "  ⏳ CacheManager (pending)"

echo ""
echo "🎯 Testing package root import..."
python3 -c "import bob_v3; print('  ✅ bob_v3 package imports'); print(f'  Version: {bob_v3.__version__}')" 2>/dev/null || echo "  ⏳ Package import (pending)"

echo ""
echo "=============================="
echo "Validation complete!"
