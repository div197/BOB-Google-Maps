#!/usr/bin/env python3
"""
Real-World Validation Test: Extract 10 Businesses from Jodhpur

This script tests the complete BOB extraction system with real businesses
from Jodhpur, Rajasthan to verify production readiness.

Author: BOB Google Maps Team
Date: November 14, 2025
"""

import json
import sys
from datetime import datetime

# Add current directory to path
sys.path.insert(0, '/home/user/BOB-Google-Maps')

def test_jodhpur_extraction():
    """Extract 10 businesses from Jodhpur for validation."""

    print("🔱 BOB GOOGLE MAPS - REAL-WORLD VALIDATION TEST")
    print("=" * 70)
    print("Location: Jodhpur, Rajasthan, India")
    print("Target: 10 businesses")
    print("Keyword: restaurants jodhpur")
    print("=" * 70)
    print()

    # Import BOB (with error handling for optional dependencies)
    try:
        from bob.extractors.playwright import PlaywrightExtractor
        print("✅ BOB Playwright extractor imported successfully")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Attempting fallback...")
        try:
            from bob.extractors.selenium import SeleniumExtractor
            print("✅ Using Selenium extractor as fallback")
        except ImportError as e2:
            print(f"❌ All extractors failed: {e2}")
            return

    # List of Jodhpur businesses to extract
    jodhpur_businesses = [
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

    print(f"📋 Target Businesses:")
    for idx, business in enumerate(jodhpur_businesses, 1):
        print(f"   {idx}. {business}")
    print()

    # Initialize extractor
    print("🔧 Initializing extractor...")
    try:
        extractor = PlaywrightExtractor(headless=True)
        print("✅ Playwright extractor initialized")
    except Exception as e:
        print(f"⚠️ Playwright failed: {e}")
        print("Trying Selenium...")
        try:
            extractor = SeleniumExtractor(headless=True)
            print("✅ Selenium extractor initialized")
        except Exception as e2:
            print(f"❌ All extractors failed: {e2}")
            return

    print()
    print("🚀 Starting extraction...")
    print("=" * 70)

    results = []
    successful = 0
    failed = 0
    total_time = 0

    for idx, business_query in enumerate(jodhpur_businesses, 1):
        print(f"\n{idx}/10: {business_query}")
        print("-" * 70)

        try:
            start_time = datetime.now()
            result = extractor.extract_business(business_query)
            extraction_time = (datetime.now() - start_time).total_seconds()
            total_time += extraction_time

            if result.get('success'):
                business = result.get('business')
                successful += 1

                print(f"✅ SUCCESS")
                print(f"   Name: {business.get('name', 'N/A')}")
                print(f"   Phone: {business.get('phone', 'N/A')}")
                print(f"   Rating: {business.get('rating', 'N/A')}")
                print(f"   Address: {business.get('address', 'N/A')[:60]}...")
                print(f"   Quality: {business.get('data_quality_score', 0)}/100")
                print(f"   Time: {extraction_time:.2f}s")

                # Store result
                results.append({
                    'query': business_query,
                    'success': True,
                    'name': business.get('name'),
                    'phone': business.get('phone'),
                    'rating': business.get('rating'),
                    'address': business.get('address'),
                    'quality_score': business.get('data_quality_score'),
                    'extraction_time': extraction_time
                })
            else:
                failed += 1
                error = result.get('error', 'Unknown error')
                print(f"❌ FAILED: {error}")
                print(f"   Time: {extraction_time:.2f}s")

                results.append({
                    'query': business_query,
                    'success': False,
                    'error': error,
                    'extraction_time': extraction_time
                })

        except Exception as e:
            failed += 1
            print(f"❌ EXCEPTION: {str(e)}")
            results.append({
                'query': business_query,
                'success': False,
                'error': str(e)
            })

    # Summary
    print()
    print("=" * 70)
    print("📊 VALIDATION TEST SUMMARY")
    print("=" * 70)
    print(f"✅ Successful: {successful}/10")
    print(f"❌ Failed: {failed}/10")
    print(f"📈 Success Rate: {(successful/10)*100:.1f}%")
    print(f"⏱️ Total Time: {total_time:.2f}s")
    print(f"⏱️ Average Time: {total_time/10:.2f}s per business")

    if successful > 0:
        avg_quality = sum(r.get('quality_score', 0) for r in results if r.get('success')) / successful
        print(f"📊 Average Quality Score: {avg_quality:.1f}/100")

    # Save results
    output_file = 'jodhpur_validation_test.json'
    with open(output_file, 'w') as f:
        json.dump({
            'test_date': datetime.now().isoformat(),
            'location': 'Jodhpur, Rajasthan, India',
            'total_businesses': 10,
            'successful': successful,
            'failed': failed,
            'success_rate': (successful/10)*100,
            'total_time': total_time,
            'average_time': total_time/10,
            'results': results
        }, f, indent=2, default=str)

    print(f"\n💾 Results saved to: {output_file}")

    print()
    print("=" * 70)
    if successful >= 8:
        print("🎉 VALIDATION TEST PASSED! (≥80% success rate)")
    elif successful >= 6:
        print("⚠️ VALIDATION TEST PARTIAL (60-79% success rate)")
    else:
        print("❌ VALIDATION TEST FAILED (<60% success rate)")
    print("=" * 70)


if __name__ == "__main__":
    test_jodhpur_extraction()
