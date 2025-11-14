#!/usr/bin/env python3
"""
Example 2: Extract Business with Reviews

This example demonstrates how to extract business data including
customer reviews and ratings.

Author: BOB Google Maps Team
Version: 4.2.0
"""

from bob import HybridExtractor


def main():
    """Extract a business with customer reviews."""

    print("🔱 BOB Google Maps - Extract with Reviews")
    print("=" * 60)

    # Create extractor with review extraction enabled
    extractor = HybridExtractor()

    # Choose a business known for many reviews
    business_query = "Apple Fifth Avenue New York"

    print(f"\n📍 Searching for: {business_query}")
    print("⏳ Extracting data with reviews...")

    # Extract with reviews (max 10)
    result = extractor.extract_business(
        business_query,
        include_reviews=True,
        max_reviews=10
    )

    if result.get('success'):
        business = result['business']

        print("\n✅ Extraction Successful!")
        print(f"{'─' * 60}")
        print(f"📛 Name: {business.name}")
        print(f"⭐ Rating: {business.rating or 'N/A'} ({business.review_count or 0} reviews)")
        print(f"📍 Address: {business.address or 'N/A'}")

        # Display reviews
        if business.reviews:
            print(f"\n📝 Recent Reviews ({len(business.reviews)}):")
            print(f"{'─' * 60}")

            for idx, review in enumerate(business.reviews[:5], 1):
                print(f"\n{idx}. {review.reviewer}")
                print(f"   Rating: {'⭐' * int(float(review.rating))} ({review.rating})")
                print(f"   Date: {review.review_date}")
                print(f"   Review: {review.text[:150]}...")
                if review.photos:
                    print(f"   📸 Photos: {len(review.photos)}")

        else:
            print("\n⚠️ No reviews extracted")

        print(f"\n📊 Quality Score: {business.data_quality_score}/100")
        print(f"⏱️ Extraction Time: {result.get('extraction_time_seconds', 0):.2f}s")

    else:
        print("\n❌ Extraction Failed!")
        print(f"Error: {result.get('error', 'Unknown error')}")

    print(f"\n{'═' * 60}")
    print("✅ Example completed!")


if __name__ == "__main__":
    main()
