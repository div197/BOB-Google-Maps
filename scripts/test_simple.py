#!/usr/bin/env python3
"""Simple test script for BOB extraction"""

import sys

print("🔍 Testing BOB V3.0.1...")

# Test 1: Imports
print("\n1️⃣ Testing imports...")
try:
    from bob_v3.extractors import SeleniumExtractor
    print("✅ Imports successful")
except Exception as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

# Test 2: Selenium Extractor (simpler, no async)
print("\n2️⃣ Testing Selenium extractor...")
try:
    print("Creating Selenium extractor...")
    extractor = SeleniumExtractor(headless=True, stealth_mode=True)
    print("✅ Extractor created")

    print("Starting extraction (this may take 30-60 seconds)...")
    result = extractor.extract_business("Starbucks New York", max_reviews=2)

    if result.get('success'):
        print(f"✅ SUCCESS!")
        print(f"   Name: {result.get('name', 'N/A')}")
        print(f"   Phone: {result.get('phone', 'N/A')}")
        print(f"   Rating: {result.get('rating', 'N/A')}")
    else:
        print(f"❌ Extraction failed: {result.get('error', 'Unknown error')}")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✅ All tests passed!")
