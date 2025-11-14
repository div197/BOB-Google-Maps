#!/usr/bin/env python3
"""
Example 4: Using the Cache System

This example demonstrates how to use BOB's intelligent caching
system to avoid re-extracting the same business.

Author: BOB Google Maps Team
Version: 4.2.0
"""

from bob import HybridExtractor
import time


def main():
    """Demonstrate cache usage for faster re-queries."""

    print("🔱 BOB Google Maps - Cache System Example")
    print("=" * 60)

    # Create extractor with cache enabled (default)
    extractor = HybridExtractor(
        use_cache=True,
        cache_expiration_hours=24  # Cache valid for 24 hours
    )

    business_query = "Starbucks Reserve Roastery Seattle"

    # First extraction (cold - no cache)
    print(f"\n🔵 FIRST EXTRACTION (Cold - No Cache)")
    print(f"{'─' * 60}")
    print(f"📍 Searching for: {business_query}")

    start_time = time.time()
    result1 = extractor.extract_business(business_query)
    time1 = time.time() - start_time

    if result1.get('success'):
        business1 = result1['business']
        print(f"✅ Success!")
        print(f"📛 Name: {business1.name}")
        print(f"⏱️ Extraction Time: {time1:.2f}s")
        print(f"💾 Cache Status: {result1.get('cache_status', 'unknown')}")

    # Second extraction (hot - from cache)
    print(f"\n🔴 SECOND EXTRACTION (Hot - From Cache)")
    print(f"{'─' * 60}")
    print(f"📍 Searching for: {business_query}")

    start_time = time.time()
    result2 = extractor.extract_business(business_query)
    time2 = time.time() - start_time

    if result2.get('success'):
        business2 = result2['business']
        print(f"✅ Success!")
        print(f"📛 Name: {business2.name}")
        print(f"⏱️ Extraction Time: {time2:.2f}s")
        print(f"💾 Cache Status: {result2.get('cache_status', 'unknown')}")

    # Performance comparison
    print(f"\n{'═' * 60}")
    print("📊 Performance Comparison")
    print(f"{'═' * 60}")
    print(f"🔵 Cold Extraction: {time1:.2f}s")
    print(f"🔴 Hot Extraction: {time2:.2f}s")
    if time1 > 0:
        speedup = time1 / time2
        print(f"⚡ Speedup: {speedup:.1f}x faster with cache!")
        print(f"💰 Time Saved: {time1 - time2:.2f}s")

    # Force fresh extraction (bypass cache)
    print(f"\n🟢 THIRD EXTRACTION (Force Fresh - Bypass Cache)")
    print(f"{'─' * 60}")

    start_time = time.time()
    result3 = extractor.extract_business(
        business_query,
        force_fresh=True  # Bypass cache
    )
    time3 = time.time() - start_time

    if result3.get('success'):
        print(f"✅ Success!")
        print(f"⏱️ Extraction Time: {time3:.2f}s")
        print(f"💾 Cache Status: Fresh (cache bypassed)")

    print(f"\n{'═' * 60}")
    print("✅ Cache demonstration completed!")
    print(f"\n💡 TIP: Cache location: bob_cache_ultimate.db")
    print(f"💡 TIP: Cache expires after 24 hours by default")


if __name__ == "__main__":
    main()
