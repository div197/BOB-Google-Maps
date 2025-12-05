#!/usr/bin/env python3#!/usr/bin/env python3

""""""

Example 1: Basic ExtractionExample 1: Basic Business Extraction



Extract a single business from Google Maps.This example demonstrates the simplest way to extract business data

"""from Google Maps using BOB Google Maps Extractor.



import asyncioAuthor: BOB Google Maps Team

from bob import PlaywrightExtractorOptimizedVersion: 4.2.0

"""



async def main():from bob import HybridExtractor

    """Extract a single business."""

    

    print("🔱 BOB Google Maps v4.3.0 - Basic Extraction")def main():

    print("=" * 60)    """Extract a single business with basic configuration."""

    

    # Create extractor    print("🔱 BOB Google Maps - Basic Extraction Example")

    extractor = PlaywrightExtractorOptimized(headless=True)    print("=" * 60)

    

    # Extract business    # Create extractor with default settings

    query = "Starbucks Times Square NYC"    extractor = HybridExtractor()

    print(f"\n📍 Extracting: {query}")

        # Extract a well-known business

    result = await extractor.extract_business_optimized(    business_query = "Starbucks Reserve Roastery Seattle"

        query,

        include_reviews=False,    print(f"\n📍 Searching for: {business_query}")

        max_reviews=0    print("⏳ Extracting data...")

    )

        # Perform extraction

    # Display results    result = extractor.extract_business(business_query)

    if result.get('success'):

        print("\n✅ Extraction Successful!")    # Check result

        print("-" * 40)    if result.get('success'):

        print(f"Name: {result.get('name')}")        business = result['business']

        print(f"Phone: {result.get('phone', 'N/A')}")

        print(f"Address: {result.get('address', 'N/A')}")        print("\n✅ Extraction Successful!")

        print(f"Website: {result.get('website', 'N/A')}")        print(f"{'─' * 60}")

        print(f"Rating: {result.get('rating')} ⭐")        print(f"📛 Name: {business.name}")

        print(f"Category: {result.get('category', 'N/A')}")        print(f"📞 Phone: {business.phone or 'N/A'}")

        print(f"GPS: {result.get('latitude')}, {result.get('longitude')}")        print(f"📧 Emails: {', '.join(business.emails) if business.emails else 'N/A'}")

        print(f"Quality: {result.get('quality_score')}/100")        print(f"🌐 Website: {business.website or 'N/A'}")

        print(f"Time: {result.get('extraction_time_seconds')}s")        print(f"📍 Address: {business.address or 'N/A'}")

    else:        print(f"⭐ Rating: {business.rating or 'N/A'} ({business.review_count or 0} reviews)")

        print(f"\n❌ Extraction failed: {result.get('error', 'Unknown error')}")        print(f"🏷️ Category: {business.category or 'N/A'}")

        print(f"📊 Quality Score: {business.data_quality_score}/100")

        print(f"⏱️ Extraction Time: {result.get('extraction_time_seconds', 0):.2f}s")

if __name__ == "__main__":        print(f"🔧 Method: {result.get('method', 'unknown')}")

    asyncio.run(main())

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
