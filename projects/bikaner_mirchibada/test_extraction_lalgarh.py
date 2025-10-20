#!/usr/bin/env python3
"""
🔱 BOB Google Maps - Bikaner Project
Test Extraction: Lalgarh Palace Bikaner

Purpose: Test the extraction system with real business data
Business: Lalgarh Palace Hotel, Bikaner
Status: FIRST TEST RUN

Created: October 20, 2025
"""

import sys
import json
import time
from pathlib import Path

# Add BOB to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from bob.extractors.hybrid_optimized import HybridExtractorOptimized


def test_extraction():
    """Test extraction of Lalgarh Palace Bikaner"""

    print("\n" + "="*80)
    print("🏨 LALGARH PALACE BIKANER - EXTRACTION TEST")
    print("="*80)
    print()

    # Business to extract
    business_query = "Lalgarh Palace Bikaner"

    print(f"📍 Business: {business_query}")
    print(f"📌 Location: Bikaner, Rajasthan, India")
    print()

    # Create extractor
    print("🔱 Initializing BOB Extractor (Nishkaam Karma Yoga Optimized)...")
    extractor = HybridExtractorOptimized(
        prefer_playwright=True,
        memory_optimized=True
    )

    # Start extraction
    print("\n⚡ Starting extraction...")
    print("-" * 80)

    start_time = time.time()

    try:
        result = extractor.extract_business(
            business_query,
            include_reviews=True,
            max_reviews=10
        )

        extraction_time = time.time() - start_time

        print("-" * 80)
        print(f"\n✅ Extraction completed in {extraction_time:.2f} seconds")

        # Display results
        if result.get('success'):
            business = result.get('business')

            print("\n" + "="*80)
            print("📊 EXTRACTION RESULTS")
            print("="*80)
            print()

            # Basic Info
            print("🏢 BASIC INFORMATION:")
            print(f"   Name: {business.get('name', 'N/A')}")
            print(f"   Category: {business.get('category', 'N/A')}")
            print(f"   Address: {business.get('address', 'N/A')}")
            print()

            # Contact
            print("📞 CONTACT INFORMATION:")
            print(f"   Phone: {business.get('phone', 'N/A')}")
            print(f"   Website: {business.get('website', 'N/A')}")
            print(f"   Emails: {business.get('emails', [])}")
            print()

            # Location
            print("📍 LOCATION:")
            print(f"   Latitude: {business.get('latitude', 'N/A')}")
            print(f"   Longitude: {business.get('longitude', 'N/A')}")
            print(f"   Plus Code: {business.get('plus_code', 'N/A')}")
            print()

            # Business Details
            print("⭐ BUSINESS DETAILS:")
            print(f"   Rating: {business.get('rating', 'N/A')}/5.0")
            print(f"   Reviews: {business.get('review_count', 'N/A')}")
            print(f"   Hours: {business.get('hours', 'N/A')}")
            print(f"   Price Range: {business.get('price_range', 'N/A')}")
            print()

            # Identifiers
            print("🆔 IDENTIFIERS:")
            print(f"   Place ID: {business.get('place_id', 'N/A')}")
            print(f"   CID: {business.get('cid', 'N/A')}")
            print(f"   Place ID Confidence: {business.get('place_id_confidence', 'N/A')}")
            print()

            # Rich Data
            print("📸 RICH DATA:")
            photos = business.get('photos', [])
            print(f"   Photos: {len(photos)} extracted")
            if photos:
                print(f"      First photo: {photos[0][:60]}...")

            reviews = business.get('reviews', [])
            print(f"   Reviews: {len(reviews)} extracted")
            if reviews:
                print(f"      First review by: {reviews[0].get('reviewer_name', 'Anonymous')}")
            print()

            # Metadata
            print("📊 METADATA:")
            print(f"   Quality Score: {business.get('data_quality_score', 'N/A')}/100")
            print(f"   Extraction Method: {business.get('extraction_method', 'N/A')}")
            print(f"   Extractor Version: {business.get('extractor_version', 'N/A')}")
            print()

            # Save to JSON
            output_path = Path(__file__).parent / "data" / "lalgarh_palace_bikaner.json"
            with open(output_path, 'w') as f:
                json.dump(result, f, indent=2, default=str)

            print(f"💾 Result saved to: {output_path}")
            print()

            # Assessment
            print("="*80)
            print("✅ ASSESSMENT")
            print("="*80)
            quality_score = business.get('data_quality_score', 0)

            if quality_score >= 80:
                assessment = "EXCELLENT - High quality data extraction"
            elif quality_score >= 70:
                assessment = "GOOD - Acceptable data quality"
            elif quality_score >= 60:
                assessment = "FAIR - Basic data extracted"
            else:
                assessment = "POOR - Limited data available"

            print(f"   Quality: {assessment}")
            print(f"   Fields Extracted: {quality_score}%")
            print()

        else:
            print("\n❌ EXTRACTION FAILED")
            print(f"   Error: {result.get('error', 'Unknown error')}")
            print()

    except Exception as e:
        print(f"\n❌ EXCEPTION OCCURRED:")
        print(f"   {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()

    print("\n" + "="*80)
    print("🔱 TEST COMPLETE")
    print("="*80)
    print()


if __name__ == "__main__":
    test_extraction()
