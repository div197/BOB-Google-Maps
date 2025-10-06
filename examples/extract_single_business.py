#!/usr/bin/env python3
"""
Example: Extract Single Business

This example demonstrates how to extract complete business data
from a single Google Maps URL using BOB Google Maps 1.0.
"""

import json
from bob import HybridExtractor

def main():
    """Extract single business example."""
    print("🔱 BOB GOOGLE MAPS 1.0 - Single Business Extraction Example")
    print("=" * 60)

    # Initialize extractor
    extractor = HybridExtractor(headless=True)

    # Example URLs (replace with any Google Maps business URL)
    example_urls = [
        "https://www.google.com/maps/place/Starbucks+Reserve+Roastery",
        "https://www.google.com/maps/place/Empire+State+Building",
        "https://www.google.com/maps/place/The+Peninsula+Hotel"
    ]

    for i, url in enumerate(example_urls[:1], 1):  # Test with first URL
        print(f"\n📍 Example {i}: {url}")
        print("-" * 40)

        try:
            # Extract complete business data
            result = extractor.extract_business(
                url,
                include_reviews=True,
                max_reviews=5
            )

            business = result['business']

            print("✅ EXTRACTION SUCCESSFUL!")
            print(f"📋 Business Name: {business.name}")
            print(f"⭐ Rating: {business.rating or 'N/A'}")
            print(f"📍 Address: {business.address}")
            print(f"📞 Phone: {business.phone or 'N/A'}")
            print(f"🌐 Website: {business.website or 'N/A'}")
            print(f"🆔 CID: {business.cid or 'N/A'}")
            print(f"📧 Emails: {', '.join(business.emails) if business.emails else 'N/A'}")
            print(f"📸 Images: {len(business.images)}")
            print(f"💬 Reviews: {len(business.reviews)}")

            if business.latitude and business.longitude:
                print(f"🌍 Coordinates: {business.latitude}, {business.longitude}")

            if business.service_options:
                print(f"🍽️ Service: {', '.join([k for k, v in business.service_options.items() if v])}")

            # Quality score
            quality = business.calculate_quality_score()
            print(f"📊 Quality Score: {quality}/100")

            # Save result
            output_file = f"single_business_result_{i}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(business.to_dict(), f, indent=2, ensure_ascii=False)
            print(f"💾 Full result saved: {output_file}")

            # Show revolutionary capability
            if len(business.images) > 0:
                print("\n🔥 REVOLUTIONARY ACHIEVEMENT:")
                print(f"   - {len(business.images)} high-resolution images extracted")
                print("   - This is IMPOSSIBLE via Google Maps API!")
                print("   - Saves $850-1,600 vs API costs")

        except Exception as e:
            print(f"❌ Exception: {e}")
            import traceback
            traceback.print_exc()

    print("\n🔱 Example completed! JAI SHREE KRISHNA! 🔱")

if __name__ == "__main__":
    main()