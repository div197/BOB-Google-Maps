#!/usr/bin/env python3
"""
Test V3.3 with multiple different business types
"""

import asyncio
import json
import time
from bob.extractors.playwright import PlaywrightExtractor

async def test_multiple_businesses():
    """Test different business types to validate V3.3 robustness"""

    test_businesses = [
        {
            "name": "Starbucks Times Square New York",
            "type": "Coffee Shop",
            "expected_fields": ["rating", "service_options", "hours"]
        },
        {
            "name": "Walmart Supercenter Los Angeles",
            "type": "Retail Store",
            "expected_fields": ["rating", "hours", "phone"]
        },
        {
            "name": "Four Seasons Hotel Tokyo",
            "type": "Hotel",
            "expected_fields": ["rating", "website", "phone"]
        }
    ]

    results = []
    print("\n" + "="*60)
    print("🎯 BOB V3.3 MULTI-BUSINESS TYPE TESTING")
    print("="*60)

    extractor = PlaywrightExtractor(headless=True)

    for business in test_businesses:
        print(f"\n📍 Testing: {business['name']}")
        print(f"   Type: {business['type']}")
        print("-" * 40)

        start_time = time.time()

        try:
            result = await extractor.extract_business(business['name'])
            extraction_time = time.time() - start_time

            # Validate critical V3.3 fields
            validation = {
                "business": business['name'],
                "type": business['type'],
                "extraction_time": round(extraction_time, 1),
                "success": True,
                "fields_extracted": {
                    "name": result.get('name', 'N/A'),
                    "rating": result.get('rating', 'N/A'),
                    "cid": result.get('cid', 'N/A'),
                    "emails": len(result.get('emails', [])),
                    "plus_code": bool(result.get('plus_code')),
                    "service_options": bool(result.get('service_options')),
                    "photos": len(result.get('photos', [])),
                    "quality_score": result.get('data_quality_score', 0)
                }
            }

            # Check critical fields
            critical_fields_ok = all([
                result.get('name'),
                result.get('rating') is not None,
                result.get('cid') is not None
            ])

            if critical_fields_ok:
                print(f"   ✅ SUCCESS - {extraction_time:.1f}s")
                print(f"   📊 Rating: {result.get('rating', 'N/A')}")
                print(f"   🆔 CID: {result.get('cid', 'N/A')}")
                print(f"   📧 Emails: {len(result.get('emails', []))}")
                print(f"   📸 Photos: {len(result.get('photos', []))}")
                print(f"   💯 Quality: {result.get('data_quality_score', 0)}/100")
            else:
                print(f"   ⚠️ PARTIAL SUCCESS - Some fields missing")
                validation["success"] = False

            results.append(validation)

        except Exception as e:
            print(f"   ❌ ERROR: {str(e)}")
            results.append({
                "business": business['name'],
                "type": business['type'],
                "success": False,
                "error": str(e)
            })

    await extractor.close()

    # Summary Report
    print("\n" + "="*60)
    print("📊 TESTING SUMMARY REPORT")
    print("="*60)

    successful = sum(1 for r in results if r.get("success"))
    total = len(results)

    print(f"\n✅ Success Rate: {successful}/{total} ({(successful/total*100):.0f}%)")
    print(f"⏱️ Average Time: {sum(r.get('extraction_time', 0) for r in results if 'extraction_time' in r) / len([r for r in results if 'extraction_time' in r]):.1f}s")

    print("\n📋 Detailed Results:")
    for r in results:
        status = "✅" if r.get("success") else "❌"
        print(f"\n{status} {r['business']} ({r['type']})")
        if r.get("success") and "fields_extracted" in r:
            fields = r["fields_extracted"]
            print(f"   - Rating: {fields['rating']}")
            print(f"   - CID: {fields['cid']}")
            print(f"   - Emails: {fields['emails']}")
            print(f"   - Photos: {fields['photos']}")
            print(f"   - Quality: {fields['quality_score']}/100")

    # Save results
    output_file = "/tmp/v3.3_multi_business_test_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n💾 Results saved to: {output_file}")

    # Final verdict
    if successful == total:
        print("\n" + "="*60)
        print("🎉 V3.3 VALIDATION: COMPLETE SUCCESS!")
        print("All business types extracted successfully with critical fields")
        print("="*60)
    elif successful > 0:
        print("\n" + "="*60)
        print("⚠️ V3.3 VALIDATION: PARTIAL SUCCESS")
        print(f"{successful}/{total} businesses extracted successfully")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("❌ V3.3 VALIDATION: FAILED")
        print("Critical issues detected - needs investigation")
        print("="*60)

    return results

if __name__ == "__main__":
    results = asyncio.run(test_multiple_businesses())