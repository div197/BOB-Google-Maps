#!/usr/bin/env python3
"""
Example 5: Batch Extraction

Extract multiple businesses in a single run with progress tracking.
"""

import asyncio
from bob import PlaywrightExtractorOptimized


async def main():
    """Extract multiple businesses."""
    
    print("🔱 BOB Google Maps v4.3.0 - Batch Extraction")
    print("=" * 60)
    
    # List of businesses to extract
    businesses = [
        "Taj Mahal Palace Mumbai",
        "India Gate Delhi",
        "Gateway of India Mumbai",
        "Hawa Mahal Jaipur",
        "Qutub Minar Delhi",
    ]
    
    extractor = PlaywrightExtractorOptimized(headless=True)
    results = []
    
    print(f"\n📋 Extracting {len(businesses)} businesses...\n")
    
    for i, query in enumerate(businesses, 1):
        print(f"[{i}/{len(businesses)}] {query}...")
        
        result = await extractor.extract_business_optimized(
            query,
            include_reviews=False  # Faster without reviews
        )
        
        if result.get('success'):
            results.append(result)
            print(f"   ✅ {result.get('name')} (Quality: {result.get('quality_score')}/100)")
        else:
            print(f"   ❌ Failed: {result.get('error', 'Unknown')[:50]}")
        
        # Small delay between extractions (be respectful)
        if i < len(businesses):
            await asyncio.sleep(2)
    
    # Summary
    print("\n" + "=" * 60)
    print(f"📊 BATCH COMPLETE")
    print(f"   Success: {len(results)}/{len(businesses)}")
    print(f"   Success Rate: {len(results)/len(businesses)*100:.0f}%")
    
    if results:
        avg_quality = sum(r.get('quality_score', 0) for r in results) / len(results)
        print(f"   Average Quality: {avg_quality:.0f}/100")
    
    return results


if __name__ == "__main__":
    results = asyncio.run(main())
