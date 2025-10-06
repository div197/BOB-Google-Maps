#!/usr/bin/env python3
"""
BOB Google Maps V3.0.1 - Comprehensive Testing Suite
Tests real extraction with multiple businesses
"""

import json
import time
from datetime import datetime
from bob_v3.extractors import HybridExtractor, SeleniumExtractor

# Test businesses (diverse locations and types)
TEST_BUSINESSES = [
    {
        "name": "Taj Mahal, Agra",
        "url": "https://www.google.com/maps/place/Taj+Mahal/@27.1751448,78.0399535,17z",
        "expected": {"name_contains": "Taj Mahal", "rating_min": 4.0}
    },
    {
        "name": "Starbucks Reserve Roastery New York",
        "url": "https://www.google.com/maps/place/Starbucks+Reserve+Roastery+New+York/@40.7410065,-73.9896868,17z",
        "expected": {"name_contains": "Starbucks", "rating_min": 4.0}
    },
    {
        "name": "Apple Park Visitor Center",
        "url": "https://www.google.com/maps/place/Apple+Park+Visitor+Center/@37.3309332,-122.0114831,17z",
        "expected": {"name_contains": "Apple", "rating_min": 4.0}
    },
    {
        "name": "The Louvre Museum Paris",
        "url": "https://www.google.com/maps/place/Louvre+Museum/@48.8606111,2.337644,17z",
        "expected": {"name_contains": "Louvre", "rating_min": 4.0}
    },
    {
        "name": "Sydney Opera House",
        "url": "https://www.google.com/maps/place/Sydney+Opera+House/@-33.8567844,151.213108,17z",
        "expected": {"name_contains": "Opera", "rating_min": 4.0}
    }
]

def run_comprehensive_test():
    """Run comprehensive extraction tests"""

    print("=" * 80)
    print("🔱 BOB V3.0.1 - COMPREHENSIVE EXTRACTION TEST")
    print("=" * 80)
    print(f"📅 Test Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 Total Test Cases: {len(TEST_BUSINESSES)}")
    print("=" * 80)
    print()

    results = []
    extractor = SeleniumExtractor(headless=True, stealth_mode=True)

    for idx, test_case in enumerate(TEST_BUSINESSES, 1):
        print(f"\n{'=' * 80}")
        print(f"TEST {idx}/{len(TEST_BUSINESSES)}: {test_case['name']}")
        print(f"{'=' * 80}")

        start_time = time.time()

        try:
            print(f"🔍 Extracting: {test_case['url']}")
            result = extractor.extract_business(
                test_case['url'],
                include_reviews=True,
                max_reviews=3
            )

            elapsed = time.time() - start_time

            # Validate result
            success = result.get('success', False)
            extracted_name = result.get('name', '')
            rating = result.get('rating', 0)

            # Check expectations
            name_match = test_case['expected']['name_contains'].lower() in extracted_name.lower() if extracted_name else False
            rating_ok = rating >= test_case['expected']['rating_min'] if rating else False

            test_result = {
                "test_case": test_case['name'],
                "success": success,
                "name": extracted_name,
                "phone": result.get('phone', 'N/A'),
                "rating": rating,
                "review_count": result.get('review_count', 0),
                "place_id": result.get('place_id', 'N/A'),
                "cid": result.get('cid', 'N/A'),
                "image_count": len(result.get('photos', [])),
                "review_count_extracted": len(result.get('reviews', [])),
                "elapsed_time": f"{elapsed:.2f}s",
                "quality_score": result.get('data_quality_score', 0),
                "validation": {
                    "name_match": name_match,
                    "rating_ok": rating_ok,
                    "overall_pass": success and name_match and rating_ok
                }
            }

            results.append(test_result)

            # Print results
            print(f"\n📊 RESULTS:")
            print(f"   Success: {'✅' if success else '❌'}")
            print(f"   Name: {extracted_name}")
            print(f"   Phone: {result.get('phone', 'N/A')}")
            print(f"   Rating: {rating}/5 ({result.get('review_count', 0)} reviews)")
            print(f"   Place ID: {result.get('place_id', 'N/A')[:50]}...")
            print(f"   CID: {result.get('cid', 'N/A')}")
            print(f"   Images: {len(result.get('photos', []))}")
            print(f"   Reviews Extracted: {len(result.get('reviews', []))}")
            print(f"   Quality Score: {result.get('data_quality_score', 0)}/100")
            print(f"   Time: {elapsed:.2f}s")
            print(f"\n   VALIDATION:")
            print(f"   - Name Match: {'✅' if name_match else '❌'}")
            print(f"   - Rating OK: {'✅' if rating_ok else '❌'}")
            print(f"   - Overall: {'✅ PASS' if test_result['validation']['overall_pass'] else '❌ FAIL'}")

        except Exception as e:
            print(f"❌ ERROR: {e}")
            results.append({
                "test_case": test_case['name'],
                "success": False,
                "error": str(e),
                "elapsed_time": f"{time.time() - start_time:.2f}s"
            })

    # Summary
    print(f"\n\n{'=' * 80}")
    print("📊 TEST SUMMARY")
    print(f"{'=' * 80}")

    total = len(results)
    passed = sum(1 for r in results if r.get('validation', {}).get('overall_pass', False))
    failed = total - passed

    print(f"\nTotal Tests: {total}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"Success Rate: {(passed/total*100):.1f}%")

    # Average metrics
    avg_quality = sum(r.get('quality_score', 0) for r in results) / total
    avg_time = sum(float(r.get('elapsed_time', '0s').replace('s', '')) for r in results) / total

    print(f"\nAverage Quality Score: {avg_quality:.1f}/100")
    print(f"Average Extraction Time: {avg_time:.2f}s")

    # Save results
    output_file = f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total": total,
                "passed": passed,
                "failed": failed,
                "success_rate": f"{(passed/total*100):.1f}%",
                "avg_quality_score": f"{avg_quality:.1f}",
                "avg_extraction_time": f"{avg_time:.2f}s"
            },
            "results": results
        }, f, indent=2)

    print(f"\n📄 Detailed results saved: {output_file}")
    print(f"\n🔱 Jai Shree Krishna!")
    print("=" * 80)

if __name__ == "__main__":
    run_comprehensive_test()
