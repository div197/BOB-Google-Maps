#!/usr/bin/env python3
"""
Example: Extract Single Business

This example demonstrates how to extract complete business data
from a single Google Maps URL using BOB Google Maps.
"""

import sys
import os
import json

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.google_maps_extractor import GoogleMapsExtractor

def main():
    """Extract single business example."""
    print("🔱 BOB GOOGLE MAPS - Single Business Extraction Example")
    print("=" * 60)

    # Initialize extractor
    extractor = GoogleMapsExtractor(headless=True, optimize_for_speed=True)

    # Example URLs (replace with any Google Maps URL)
    example_urls = [
        "https://www.google.com/maps/place/Starbucks",
        "https://www.google.com/maps/search/restaurants",
        "https://www.google.com/maps/place/Empire+State+Building"
    ]

    for i, url in enumerate(example_urls[:1], 1):  # Test with first URL
        print(f"\n📍 Example {i}: {url}")
        print("-" * 40)

        try:
            # Extract complete business data
            result = extractor.extract_business(
                url,
                include_reviews=True,
                max_reviews=3
            )

            if result.get('success'):
                print("✅ EXTRACTION SUCCESSFUL!")
                print(f"📋 Business Name: {result.get('name', 'N/A')}")
                print(f"⭐ Rating: {result.get('rating', 'N/A')}")
                print(f"📍 Address: {result.get('address', 'N/A')}")
                print(f"📞 Phone: {result.get('phone', 'N/A')}")
                print(f"🌐 Website: {result.get('website', 'N/A')}")
                print(f"📸 Images Extracted: {result.get('image_count', 0)}")
                print(f"💬 Reviews Extracted: {len(result.get('reviews', []))}")

                if result.get('latitude') and result.get('longitude'):
                    print(f"🌍 Coordinates: {result['latitude']}, {result['longitude']}")

                # Save result
                output_file = f"single_business_result_{i}.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                print(f"💾 Full result saved: {output_file}")

                # Show revolutionary capability
                if result.get('image_count', 0) > 0:
                    print("\n🔥 REVOLUTIONARY ACHIEVEMENT:")
                    print(f"   - {result['image_count']} images extracted")
                    print("   - This is IMPOSSIBLE via Google Maps API!")
                    print("   - Saves $850-1,600 vs API costs")

            else:
                print("❌ EXTRACTION FAILED:")
                print(f"   Error: {result.get('error', 'Unknown error')}")

        except Exception as e:
            print(f"❌ Exception: {e}")

    print("\n🔱 Example completed! JAI SHREE KRISHNA! 🔱")

if __name__ == "__main__":
    main()