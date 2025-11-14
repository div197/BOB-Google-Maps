#!/usr/bin/env python3
"""
Async Jodhpur Validation Test - Using Playwright with async/await

Tests BOB extraction with 10 Jodhpur businesses
"""

import json
import sys
import asyncio
from datetime import datetime

sys.path.insert(0, '/home/user/BOB-Google-Maps')

async def test_extraction_async():
    """Test extraction with Playwright async."""

    print("🔱 BOB VALIDATION TEST - JODHPUR RESTAURANTS")
    print("=" * 70)

    # Direct import
    from bob.extractors.playwright import PlaywrightExtractor
    print("✅ Playwright extractor imported")

    # Businesses to test
    businesses = [
        "Gypsy Vegetarian Restaurant Jodhpur",
        "Jharokha Restaurant Jodhpur",
        "Indique Restaurant Jodhpur",
        "Pillars Restaurant Jodhpur",
        "Janta Sweet House Jodhpur",
        "Omelette Shop Jodhpur",
        "Cafe Mehran Jodhpur",
        "Hanwant Mahal Restaurant Jodhpur",
        "Darikhana Restaurant Jodhpur",
        "The Spice Court Jodhpur"
    ]

    print(f"\n📋 Testing {len(businesses)} businesses from Jodhpur\n")

    # Initialize
    print("🔧 Initializing Playwright...")
    extractor = PlaywrightExtractor(headless=True)
    print("✅ Ready\n")

    # Extract
    results = []
    successful = 0

    for idx, query in enumerate(businesses, 1):
        print(f"{idx}/10: {query[:40]}...")

        try:
            start = datetime.now()
            result = await extractor.extract_business(query)
            time_taken = (datetime.now() - start).total_seconds()

            if result.get('success'):
                business = result.get('business', {})
                successful += 1

                name = business.get('name', 'N/A')
                phone = business.get('phone', 'N/A')
                rating = business.get('rating', 'N/A')
                quality = business.get('data_quality_score', 0)

                print(f"  ✅ {name[:40]}")
                print(f"     📞 {phone} | ⭐ {rating} | 📊 {quality}/100 | ⏱️ {time_taken:.1f}s")

                results.append({
                    'query': query,
                    'success': True,
                    'name': name,
                    'phone': phone,
                    'rating': rating,
                    'quality': quality,
                    'time': time_taken
                })
            else:
                error = result.get('error', 'Unknown')
                print(f"  ❌ Failed: {error[:60]}")
                results.append({
                    'query': query,
                    'success': False,
                    'error': error
                })

        except Exception as e:
            print(f"  ❌ Exception: {str(e)[:60]}")
            results.append({
                'query': query,
                'success': False,
                'error': str(e)
            })

    # Summary
    print("\n" + "=" * 70)
    print("📊 RESULTS")
    print("=" * 70)
    print(f"✅ Successful: {successful}/10 ({successful*10}%)")
    print(f"❌ Failed: {10-successful}/10")

    if successful > 0:
        avg_quality = sum(r.get('quality', 0) for r in results if r.get('success')) / successful
        avg_time = sum(r.get('time', 0) for r in results if r.get('success')) / successful
        print(f"📊 Avg Quality: {avg_quality:.1f}/100")
        print(f"⏱️ Avg Time: {avg_time:.1f}s")

    # Save
    with open('jodhpur_test_results.json', 'w') as f:
        json.dump({
            'test_date': datetime.now().isoformat(),
            'location': 'Jodhpur, Rajasthan, India',
            'keyword': 'restaurants',
            'total': 10,
            'successful': successful,
            'failed': 10-successful,
            'success_rate': successful*10,
            'results': results
        }, f, indent=2, default=str)
    print(f"\n💾 Saved: jodhpur_test_results.json")

    # Verdict
    print("\n" + "=" * 70)
    if successful >= 8:
        print("🎉 TEST PASSED! (≥80% success)")
    elif successful >= 6:
        print("⚠️ TEST PARTIAL (60-79% success)")
    else:
        print("❌ TEST FAILED (<60% success)")
    print("=" * 70)

    return successful, results


if __name__ == "__main__":
    successful, results = asyncio.run(test_extraction_async())
