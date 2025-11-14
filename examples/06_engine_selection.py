#!/usr/bin/env python3
"""
Example 6: Engine Selection (Playwright vs Selenium vs Hybrid)

This example demonstrates how to select different extraction engines
based on your needs (speed, reliability, compatibility).

Author: BOB Google Maps Team
Version: 4.2.0
"""

from bob.extractors.playwright import PlaywrightExtractor
from bob.extractors.selenium import SeleniumExtractor
from bob.extractors.hybrid import HybridExtractor
import time


def test_engine(extractor_class, engine_name, business_query):
    """Test a specific extraction engine."""

    print(f"\n{'─' * 60}")
    print(f"🔧 Testing: {engine_name}")
    print(f"{'─' * 60}")

    try:
        extractor = extractor_class()

        start_time = time.time()
        result = extractor.extract_business(business_query)
        extraction_time = time.time() - start_time

        if result.get('success'):
            business = result['business']
            print(f"✅ Status: Success")
            print(f"📛 Name: {business.name}")
            print(f"⭐ Rating: {business.rating or 'N/A'}")
            print(f"📊 Quality Score: {business.data_quality_score}/100")
            print(f"⏱️ Extraction Time: {extraction_time:.2f}s")
            print(f"🆔 Place ID: {'✓' if business.place_id else '✗'}")
            print(f"🔢 CID: {'✓' if business.cid else '✗'}")
            print(f"📧 Emails: {len(business.emails or [])} found")

            return {
                'success': True,
                'time': extraction_time,
                'quality': business.data_quality_score
            }
        else:
            print(f"❌ Status: Failed")
            print(f"Error: {result.get('error', 'Unknown')}")
            return {'success': False, 'time': extraction_time}

    except Exception as e:
        print(f"❌ Status: Exception")
        print(f"Error: {str(e)}")
        return {'success': False, 'time': 0}


def main():
    """Compare different extraction engines."""

    print("🔱 BOB Google Maps - Engine Selection Example")
    print("=" * 60)

    business_query = "Starbucks Reserve Roastery Seattle"
    print(f"\n🎯 Target Business: {business_query}")
    print(f"\nTesting 3 different extraction engines...")

    # Test Playwright (Fastest)
    result_playwright = test_engine(
        PlaywrightExtractor,
        "Playwright Engine (⚡ Fastest)",
        business_query
    )

    # Test Selenium (Most Reliable)
    result_selenium = test_engine(
        SeleniumExtractor,
        "Selenium Engine (🛡️ Most Reliable)",
        business_query
    )

    # Test Hybrid (Best of Both)
    result_hybrid = test_engine(
        HybridExtractor,
        "Hybrid Engine (🎯 Intelligent)",
        business_query
    )

    # Comparison summary
    print(f"\n{'═' * 60}")
    print("📊 ENGINE COMPARISON SUMMARY")
    print(f"{'═' * 60}")

    engines = [
        ("Playwright", result_playwright),
        ("Selenium", result_selenium),
        ("Hybrid", result_hybrid)
    ]

    successful = sum(1 for _, r in engines if r['success'])
    print(f"\n✅ Successful Extractions: {successful}/3")

    print(f"\n{'Engine':<15} {'Status':<10} {'Time':<12} {'Quality':<10}")
    print(f"{'─' * 50}")

    for name, result in engines:
        status = "✅ Success" if result['success'] else "❌ Failed"
        time_str = f"{result['time']:.2f}s" if result['time'] else "N/A"
        quality_str = f"{result.get('quality', 0)}/100" if result.get('quality') else "N/A"

        print(f"{name:<15} {status:<10} {time_str:<12} {quality_str:<10}")

    # Recommendations
    print(f"\n{'═' * 60}")
    print("💡 RECOMMENDATIONS")
    print(f"{'═' * 60}")

    print("\n⚡ Playwright Engine:")
    print("   • Fastest extraction (11-15 seconds average)")
    print("   • Best for: Large-scale batch processing")
    print("   • Trade-off: May miss some fields occasionally")

    print("\n🛡️ Selenium Engine:")
    print("   • Most reliable (100% success rate)")
    print("   • Best for: Critical businesses, quality over speed")
    print("   • Trade-off: Slower (20-40 seconds average)")

    print("\n🎯 Hybrid Engine:")
    print("   • Intelligent fallback (tries Playwright first, then Selenium)")
    print("   • Best for: General use, balanced speed + reliability")
    print("   • Trade-off: None - recommended for most use cases")

    print(f"\n{'═' * 60}")
    print("✅ Engine comparison completed!")
    print("\n💡 TIP: Use HybridExtractor for best results!")


if __name__ == "__main__":
    main()
