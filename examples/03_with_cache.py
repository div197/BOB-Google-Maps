#!/usr/bin/env python3
"""
Example 3: Using the Hybrid Extractor with Caching

The HybridExtractorOptimized is the recommended engine for most use cases.
It provides caching for fast repeat queries.
"""

from bob import HybridExtractorOptimized
import time


def main():
    """Demonstrate caching with HybridExtractor."""
    
    print("🔱 BOB Google Maps v4.3.0 - Hybrid Extractor with Cache")
    print("=" * 60)
    
    # Create extractor with caching enabled
    extractor = HybridExtractorOptimized(
        use_cache=True,
        prefer_playwright=True
    )
    
    query = "Empire State Building NYC"
    
    # First extraction - from live source
    print(f"\n📍 First extraction: {query}")
    print("⏳ Fetching from Google Maps...")
    
    start = time.time()
    result1 = extractor.extract_business(query, include_reviews=False)
    time1 = time.time() - start
    
    if result1.get('success'):
        print(f"✅ Success in {time1:.2f}s")
        print(f"   Name: {result1.get('name')}")
        print(f"   Quality: {result1.get('quality_score')}/100")
    
    # Second extraction - from cache
    print(f"\n📍 Second extraction (same query)")
    print("⏳ Should be from cache...")
    
    start = time.time()
    result2 = extractor.extract_business(query, include_reviews=False)
    time2 = time.time() - start
    
    if result2.get('success'):
        print(f"✅ Success in {time2:.4f}s")
        print(f"   Name: {result2.get('name')}")
    
    # Show speedup
    if time1 > 0 and time2 > 0:
        speedup = time1 / time2
        print(f"\n🚀 Cache speedup: {speedup:.0f}x faster!")


if __name__ == "__main__":
    main()
