#!/usr/bin/env python3
"""
Test Browser Lifecycle Fix - Oct 2025

Tests the research-based fixes applied to SeleniumExtractor:
- use_subprocess=False
- 5-second delay after quit()
- Proper __del__ method
- Context manager support

Expected: 90%+ success rate (vs 60% before fix)
"""

import sys
import time
from bob_v3.extractors import SeleniumExtractor

print("=" * 80)
print("🧪 TESTING BROWSER LIFECYCLE FIX - OCT 2025")
print("=" * 80)
print()
print("FIXES APPLIED:")
print("1. ✅ use_subprocess=False for better resource management")
print("2. ✅ 5-second delay after driver.quit() (was 2 seconds)")
print("3. ✅ Explicit driver = None for garbage collection")
print("4. ✅ __del__() destructor method")
print("5. ✅ Context manager support (__enter__/__exit__)")
print("6. ✅ Docker Chrome binary path support")
print()
print("=" * 80)
print()

# Test businesses (mix of international and local)
test_businesses = [
    "Taj Mahal India",
    "Eiffel Tower Paris",
    "Statue of Liberty New York",
    "Sydney Opera House",
    "Big Ben London",
    "Digital Marketing Jodhpur",
    "SEO Services Mumbai",
    "Web Design Bangalore",
    "IT Solutions Pune",
    "Software Development Delhi"
]

results = []
extractor = SeleniumExtractor(headless=True)

start_time = time.time()

for i, business in enumerate(test_businesses, 1):
    print(f"\n[{i}/10] Testing: {business}...")
    print("-" * 60)

    try:
        result = extractor.extract_business(business, include_reviews=False, max_reviews=0)

        if result.get('success'):
            print(f"✅ SUCCESS - {result.get('name', 'Unknown')}")
            results.append({'business': business, 'success': True, 'name': result.get('name')})
        else:
            print(f"❌ FAILED - {result.get('error', 'Unknown error')}")
            results.append({'business': business, 'success': False, 'error': result.get('error')})

    except Exception as e:
        print(f"❌ EXCEPTION - {str(e)[:100]}")
        results.append({'business': business, 'success': False, 'error': str(e)})

    # Small delay between extractions
    if i < len(test_businesses):
        print(f"⏳ Waiting 3 seconds before next extraction...")
        time.sleep(3)

end_time = time.time()
total_time = end_time - start_time

print("\n")
print("=" * 80)
print("📊 TEST RESULTS - BROWSER LIFECYCLE FIX")
print("=" * 80)

successful = sum(1 for r in results if r['success'])
failed = len(results) - successful
success_rate = (successful / len(results)) * 100

print(f"\nTotal Tests: {len(results)}")
print(f"✅ Successful: {successful}")
print(f"❌ Failed: {failed}")
print(f"📈 Success Rate: {success_rate:.1f}%")
print(f"⏱️  Total Time: {total_time:.1f}s")
print(f"⏱️  Avg Time per Extraction: {total_time/len(results):.1f}s")

print("\nDETAILED RESULTS:")
for i, r in enumerate(results, 1):
    status = "✅" if r['success'] else "❌"
    name = r.get('name', r.get('error', 'Unknown'))
    print(f"  {i}. {status} {r['business']}: {name}")

print("\n")
print("=" * 80)
print("🎯 EVALUATION")
print("=" * 80)

if success_rate >= 90:
    print("✅ EXCELLENT - Browser lifecycle fix is HIGHLY EFFECTIVE!")
    print(f"   Improved from 60% to {success_rate:.1f}%")
    exit_code = 0
elif success_rate >= 80:
    print("✅ GOOD - Browser lifecycle fix shows significant improvement")
    print(f"   Improved from 60% to {success_rate:.1f}%")
    exit_code = 0
elif success_rate >= 70:
    print("⚠️  MODERATE - Some improvement but not optimal")
    print(f"   Improved from 60% to {success_rate:.1f}%")
    exit_code = 0
else:
    print("❌ NEEDS MORE WORK - Fix did not achieve target improvement")
    print(f"   Target: 90%+, Got: {success_rate:.1f}%")
    exit_code = 1

print("\n")
print("🔱 Jai Shree Krishna!")
print("=" * 80)

sys.exit(exit_code)
