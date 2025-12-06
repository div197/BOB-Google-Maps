#!/usr/bin/env python3
"""
Example 8: Parallel Extraction

Extract multiple businesses concurrently for faster batch processing.

⚠️ Use responsibly! Parallel extraction:
- Uses more memory (~50MB per browser)
- May trigger rate limiting if too aggressive
- Default is 2 parallel browsers (safe)
"""

import asyncio
from bob.utils.parallel_extractor import ParallelExtractor, ParallelConfig


async def main():
    """Demo parallel extraction."""
    
    print("🔱 BOB Google Maps v4.3.0 - Parallel Extraction")
    print("=" * 60)
    
    # Businesses to extract
    businesses = [
        "Starbucks Times Square NYC",
        "Apple Store Fifth Avenue NYC",
        "Empire State Building NYC",
        "Grand Central Terminal NYC",
    ]
    
    # Configure parallel extraction
    config = ParallelConfig(
        max_concurrent=2,           # 2 parallel browsers (safe default)
        delay_between_starts=3.0,   # 3 seconds between starting each browser
        memory_limit_percent=80,    # Stop if memory > 80%
        include_reviews=False,      # Faster without reviews
        headless=True
    )
    
    # Create extractor and run
    extractor = ParallelExtractor(config)
    results = await extractor.extract_batch(businesses)
    
    # Show successful results
    print("\n📋 Extracted Businesses:")
    for r in results:
        if r.get('success'):
            print(f"   • {r.get('name')}")
            print(f"     Rating: {r.get('rating')}⭐")
            print(f"     Phone: {r.get('phone', 'N/A')}")
            print(f"     Quality: {r.get('quality_score')}/100")
            print()
    
    # Calculate statistics
    successful = [r for r in results if r.get('success')]
    if successful:
        avg_quality = sum(r.get('quality_score', 0) for r in successful) / len(successful)
        print(f"📊 Average Quality: {avg_quality:.0f}/100")
    
    return results


if __name__ == "__main__":
    asyncio.run(main())
