#!/usr/bin/env python3
"""
Example 2: Extraction with Reviews

Extract business data including customer reviews.
"""

import asyncio
from bob import PlaywrightExtractorOptimized


async def main():
    """Extract business with reviews."""
    
    print("🔱 BOB Google Maps v4.3.0 - With Reviews")
    print("=" * 60)
    
    extractor = PlaywrightExtractorOptimized(headless=True)
    
    query = "Taj Mahal Palace Mumbai"
    print(f"\n📍 Extracting: {query}")
    print("📝 Including reviews...")
    
    result = await extractor.extract_business_optimized(
        query,
        include_reviews=True,
        max_reviews=5  # Get up to 5 reviews
    )
    
    if result.get('success'):
        print("\n✅ Extraction Successful!")
        print("-" * 40)
        print(f"Name: {result.get('name')}")
        print(f"Rating: {result.get('rating')} ⭐ ({result.get('reviews_count', 0)} reviews)")
        print(f"Quality: {result.get('quality_score')}/100")
        
        # Display reviews if extracted
        reviews = result.get('reviews', [])
        if reviews:
            print(f"\n📝 Reviews ({len(reviews)} extracted):")
            for i, review in enumerate(reviews[:3], 1):
                if isinstance(review, dict):
                    author = review.get('author_name', 'Anonymous')
                    rating = review.get('rating', 'N/A')
                    text = review.get('text', '')[:100]
                    print(f"\n  {i}. {author} ({rating}⭐)")
                    print(f"     \"{text}...\"")
        else:
            print("\n📝 No reviews extracted")
    else:
        print(f"\n❌ Extraction failed")


if __name__ == "__main__":
    asyncio.run(main())
