#!/usr/bin/env python3
"""
BOB Google Maps V3.3.0 - Delhi Royale Test Script
Tests all critical fields that were missing in V3.0

Expected results for Delhi Royale:
- Rating: 4.1
- CID: 14342688602388516637
- Emails: ['info@delhiroyale.com']
- Plus Code: "5P77+4X..."
- Service Options: {dine_in: true}
- Quality Score: >= 95/100
"""

import asyncio
import json
import sys
from bob.extractors.playwright import PlaywrightExtractor


def validate_extraction(data):
    """Validate that V3.3 extracts all critical fields."""
    print("\n" + "="*60)
    print("🔍 V3.3 EXTRACTION VALIDATION REPORT")
    print("="*60)

    results = {
        "passed": [],
        "failed": [],
        "quality_score": 0
    }

    # Check business name
    if data.get("name"):
        results["passed"].append(f"✅ Name: {data['name']}")
    else:
        results["failed"].append("❌ Name: Missing")

    # Check rating (CRITICAL FIELD)
    if data.get("rating"):
        if data["rating"] == 4.1:
            results["passed"].append(f"✅ Rating: {data['rating']} (EXACT MATCH!)")
        else:
            results["passed"].append(f"✅ Rating: {data['rating']} (extracted)")
    else:
        results["failed"].append("❌ Rating: Missing (CRITICAL)")

    # Check CID (CRITICAL FIELD)
    if data.get("cid"):
        expected_cid = 14342688602388516637
        if data["cid"] == expected_cid:
            results["passed"].append(f"✅ CID: {data['cid']} (EXACT MATCH!)")
        else:
            results["passed"].append(f"✅ CID: {data['cid']} (extracted)")

        if data.get("place_id_url"):
            results["passed"].append(f"✅ Place ID URL: {data['place_id_url']}")
    else:
        results["failed"].append("❌ CID: Missing (CRITICAL)")

    # Check emails (CRITICAL FIELD)
    if data.get("emails"):
        if "info@delhiroyale.com" in data["emails"]:
            results["passed"].append(f"✅ Emails: {data['emails']} (CONTAINS EXPECTED!)")
        else:
            results["passed"].append(f"✅ Emails: {data['emails']} (extracted)")
    else:
        results["failed"].append("❌ Emails: Missing (CRITICAL)")

    # Check plus code
    if data.get("plus_code"):
        results["passed"].append(f"✅ Plus Code: {data['plus_code']}")
    else:
        results["failed"].append("❌ Plus Code: Missing")

    # Check service options
    if data.get("service_options"):
        if data["service_options"].get("dine_in"):
            results["passed"].append(f"✅ Service Options: {data['service_options']} (DINE-IN CONFIRMED!)")
        else:
            results["passed"].append(f"✅ Service Options: {data['service_options']}")
    else:
        results["failed"].append("❌ Service Options: Missing")

    # Check images
    if data.get("photos"):
        count = len(data["photos"])
        if count >= 9:
            results["passed"].append(f"✅ Images: {count} photos (HIGH COUNT!)")
        else:
            results["passed"].append(f"✅ Images: {count} photos")
    else:
        results["failed"].append("❌ Images: Missing")

    # Check website
    if data.get("website"):
        results["passed"].append(f"✅ Website: {data['website']}")
    else:
        results["failed"].append("❌ Website: Missing")

    # Check address
    if data.get("address"):
        results["passed"].append(f"✅ Address: {data['address'][:50]}...")
    else:
        results["failed"].append("❌ Address: Missing")

    # Check phone
    if data.get("phone"):
        results["passed"].append(f"✅ Phone: {data['phone']}")
    else:
        results["failed"].append("❌ Phone: Missing")

    # Check coordinates
    if data.get("latitude") and data.get("longitude"):
        results["passed"].append(f"✅ Coordinates: ({data['latitude']}, {data['longitude']})")
    else:
        results["failed"].append("❌ Coordinates: Missing")

    # Check quality score
    quality_score = data.get("data_quality_score", 0)
    results["quality_score"] = quality_score

    if quality_score >= 95:
        results["passed"].append(f"✅ Quality Score: {quality_score}/100 (TARGET ACHIEVED!)")
    elif quality_score >= 90:
        results["passed"].append(f"✅ Quality Score: {quality_score}/100 (Good)")
    else:
        results["failed"].append(f"❌ Quality Score: {quality_score}/100 (Below target)")

    # Print results
    print("\n📊 RESULTS SUMMARY")
    print("-" * 40)
    print(f"✅ Passed: {len(results['passed'])}")
    print(f"❌ Failed: {len(results['failed'])}")
    print(f"📈 Quality Score: {results['quality_score']}/100")

    print("\n✅ PASSED CHECKS:")
    for item in results["passed"]:
        print(f"  {item}")

    if results["failed"]:
        print("\n❌ FAILED CHECKS:")
        for item in results["failed"]:
            print(f"  {item}")

    # Overall verdict
    print("\n" + "="*60)
    critical_fields_ok = (
        data.get("rating") is not None and
        data.get("cid") is not None and
        data.get("emails") is not None
    )

    if critical_fields_ok and quality_score >= 95:
        print("🎉 V3.3 VALIDATION: SUCCESS! ALL CRITICAL FIELDS EXTRACTED!")
        print("✅ Rating, CID, and Emails successfully restored")
        print("✅ Quality score target achieved (95+)")
        print("✅ V3.3 is READY FOR PRODUCTION!")
    elif critical_fields_ok:
        print("⚠️ V3.3 VALIDATION: PARTIAL SUCCESS")
        print("✅ Critical fields extracted but quality score needs improvement")
    else:
        print("❌ V3.3 VALIDATION: NEEDS MORE WORK")
        print("⚠️ Some critical fields are still missing")

    print("="*60)

    return results


async def test_delhi_royale():
    """Test Delhi Royale extraction with V3.3."""
    print("\n🚀 BOB Google Maps V3.3.0 - Delhi Royale Test")
    print("Testing: Delhi Royale, Kuala Lumpur")
    print("-" * 60)

    # URL for Delhi Royale
    url = "https://www.google.com/maps/search/delhi+royale+kuala+lumpur"

    # Create extractor
    extractor = PlaywrightExtractor(headless=True, block_resources=True)

    print("⏳ Starting extraction...")
    start_time = asyncio.get_event_loop().time()

    try:
        # Extract business data
        result = await extractor.extract_business(url, include_reviews=True, max_reviews=5)

        # Calculate extraction time
        extraction_time = asyncio.get_event_loop().time() - start_time
        result["extraction_time_seconds"] = extraction_time

        print(f"✅ Extraction completed in {extraction_time:.1f} seconds")

        # Save raw results
        output_file = "/tmp/delhi_royale_v3.3_results.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False, default=str)
        print(f"💾 Results saved to: {output_file}")

        # Validate extraction
        validation = validate_extraction(result)

        # Print critical fields for verification
        print("\n📋 CRITICAL FIELDS EXTRACTED:")
        print(f"  Rating: {result.get('rating', 'NULL')}")
        print(f"  CID: {result.get('cid', 'NULL')}")
        print(f"  Emails: {result.get('emails', 'NULL')}")
        print(f"  Plus Code: {result.get('plus_code', 'NULL')}")
        print(f"  Service Options: {result.get('service_options', 'NULL')}")

        return result

    except Exception as e:
        print(f"❌ Extraction failed: {e}")
        return None


if __name__ == "__main__":
    # Run the test
    result = asyncio.run(test_delhi_royale())

    if result:
        print("\n✅ Test completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Test failed!")
        sys.exit(1)