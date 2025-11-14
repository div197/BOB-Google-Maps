#!/usr/bin/env python3
"""
Example 1: Basic Business Extraction

This example demonstrates the simplest way to extract business data
from Google Maps using BOB Google Maps Extractor.

Author: BOB Google Maps Team
Version: 4.2.0
"""

from bob import HybridExtractor


def main():
    """Extract a single business with basic configuration."""

    print("🔱 BOB Google Maps - Basic Extraction Example")
    print("=" * 60)

    # Create extractor with default settings
    extractor = HybridExtractor()

    # Extract a well-known business
    business_query = "Starbucks Reserve Roastery Seattle"

    print(f"\n📍 Searching for: {business_query}")
    print("⏳ Extracting data...")

    # Perform extraction
    result = extractor.extract_business(business_query)

    # Check result
    if result.get('success'):
        business = result['business']

        print("\n✅ Extraction Successful!")
        print(f"{'─' * 60}")
        print(f"📛 Name: {business.name}")
        print(f"📞 Phone: {business.phone or 'N/A'}")
        print(f"📧 Emails: {', '.join(business.emails) if business.emails else 'N/A'}")
        print(f"🌐 Website: {business.website or 'N/A'}")
        print(f"📍 Address: {business.address or 'N/A'}")
        print(f"⭐ Rating: {business.rating or 'N/A'} ({business.review_count or 0} reviews)")
        print(f"🏷️ Category: {business.category or 'N/A'}")
        print(f"📊 Quality Score: {business.data_quality_score}/100")
        print(f"⏱️ Extraction Time: {result.get('extraction_time_seconds', 0):.2f}s")
        print(f"🔧 Method: {result.get('method', 'unknown')}")

        # Show coordinates if available
        if business.latitude and business.longitude:
            print(f"🗺️ Coordinates: {business.latitude}, {business.longitude}")

        # Show place ID info
        if business.place_id:
            print(f"🆔 Place ID: {business.place_id}")
        if business.cid:
            print(f"🔢 CID: {business.cid}")

    else:
        print("\n❌ Extraction Failed!")
        print(f"Error: {result.get('error', 'Unknown error')}")
        print(f"Tried methods: {result.get('tried_methods', [])}")

    print(f"\n{'═' * 60}")
    print("✅ Example completed!")


if __name__ == "__main__":
    main()
