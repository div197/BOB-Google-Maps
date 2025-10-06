#!/usr/bin/env python3
"""
BOB V3.0.1 - Realistic Batch Extraction Test
Scenario: Extract website design companies in Jodhpur
"""

import json
import time
from datetime import datetime
from bob_v3.extractors import SeleniumExtractor
import os

# Realistic test: Website design companies in Jodhpur
# Using Google Maps search results format
TEST_BUSINESSES = [
    "Website Design Company Jodhpur",
    "Web Development Jodhpur",
    "Digital Marketing Agency Jodhpur",
    "SEO Services Jodhpur",
    "App Development Jodhpur",
    "Graphic Design Jodhpur",
    "IT Company Jodhpur",
    "Software Company Jodhpur",
    "E-commerce Development Jodhpur",
    "Creative Agency Jodhpur"
]

def run_realistic_batch_test():
    """Run realistic batch extraction test"""

    print("=" * 80)
    print("🔱 BOB V3.0.1 - REALISTIC BATCH EXTRACTION TEST")
    print("=" * 80)
    print(f"📅 Test Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 Scenario: Website Design Companies in Jodhpur")
    print(f"📊 Total Queries: {len(TEST_BUSINESSES)}")
    print("=" * 80)
    print()

    results = []
    extractor = SeleniumExtractor(headless=True, stealth_mode=True)

    start_time_total = time.time()

    for idx, query in enumerate(TEST_BUSINESSES, 1):
        print(f"\n{'=' * 80}")
        print(f"EXTRACTION {idx}/{len(TEST_BUSINESSES)}: {query}")
        print(f"{'=' * 80}")

        start_time = time.time()

        try:
            print(f"🔍 Searching: {query}")
            result = extractor.extract_business(
                query,
                include_reviews=True,
                max_reviews=3
            )

            elapsed = time.time() - start_time

            # Extract key data
            success = result.get('success', False)
            name = result.get('name', 'N/A')
            phone = result.get('phone', 'N/A')
            rating = result.get('rating', 0)

            extraction_result = {
                "query": query,
                "success": success,
                "name": name,
                "phone": phone,
                "address": result.get('address', 'N/A'),
                "rating": rating,
                "review_count": result.get('review_count', 0),
                "website": result.get('website', 'N/A'),
                "place_id": result.get('place_id', 'N/A'),
                "cid": result.get('cid', 'N/A'),
                "category": result.get('category', 'N/A'),
                "images_count": len(result.get('photos', [])),
                "reviews_extracted": len(result.get('reviews', [])),
                "elapsed_time": f"{elapsed:.2f}s",
                "quality_score": result.get('data_quality_score', 0)
            }

            results.append(extraction_result)

            # Print results
            print(f"\n📊 RESULTS:")
            print(f"   Success: {'✅' if success else '❌'}")
            print(f"   Name: {name}")
            print(f"   Phone: {phone}")
            print(f"   Address: {result.get('address', 'N/A')[:60]}...")
            print(f"   Rating: {rating}/5")
            print(f"   Website: {result.get('website', 'N/A')}")
            print(f"   Category: {result.get('category', 'N/A')}")
            print(f"   Quality Score: {result.get('data_quality_score', 0)}/100")
            print(f"   Time: {elapsed:.2f}s")

        except Exception as e:
            print(f"❌ ERROR: {e}")
            results.append({
                "query": query,
                "success": False,
                "error": str(e),
                "elapsed_time": f"{time.time() - start_time:.2f}s"
            })

    # Total time
    total_elapsed = time.time() - start_time_total

    # Summary
    print(f"\n\n{'=' * 80}")
    print("📊 BATCH EXTRACTION SUMMARY")
    print(f"{'=' * 80}")

    total = len(results)
    successful = sum(1 for r in results if r.get('success', False))
    failed = total - successful

    print(f"\nTotal Extractions: {total}")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"Success Rate: {(successful/total*100):.1f}%")
    print(f"Total Time: {total_elapsed:.2f}s")
    print(f"Average Time/Business: {(total_elapsed/total):.2f}s")

    # Data completeness
    if successful > 0:
        avg_quality = sum(r.get('quality_score', 0) for r in results if r.get('success')) / successful
        print(f"Average Quality Score: {avg_quality:.1f}/100")

        # Field availability
        with_phone = sum(1 for r in results if r.get('success') and r.get('phone') != 'N/A')
        with_website = sum(1 for r in results if r.get('success') and r.get('website') != 'N/A')
        with_address = sum(1 for r in results if r.get('success') and r.get('address') != 'N/A')

        print(f"\n📈 Data Availability:")
        print(f"   Phone Numbers: {with_phone}/{successful} ({(with_phone/successful*100):.1f}%)")
        print(f"   Websites: {with_website}/{successful} ({(with_website/successful*100):.1f}%)")
        print(f"   Addresses: {with_address}/{successful} ({(with_address/successful*100):.1f}%)")

    # Save results
    output_file = f"batch_test_jodhpur_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump({
            "scenario": "Website Design Companies - Jodhpur",
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total": total,
                "successful": successful,
                "failed": failed,
                "success_rate": f"{(successful/total*100):.1f}%",
                "total_time": f"{total_elapsed:.2f}s",
                "avg_time": f"{(total_elapsed/total):.2f}s",
                "avg_quality_score": f"{avg_quality:.1f}" if successful > 0 else "N/A"
            },
            "results": results
        }, f, indent=2)

    print(f"\n📄 Results saved: {output_file}")

    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    if successful < total:
        print(f"   - {failed} extractions failed - consider retry mechanism")
    if total_elapsed/total > 60:
        print(f"   - Average time >60s - enable parallel processing for faster results")
    else:
        print(f"   - Extraction speed is good (~{total_elapsed/total:.1f}s per business)")

    print(f"\n🔱 Jai Shree Krishna!")
    print("=" * 80)

if __name__ == "__main__":
    run_realistic_batch_test()
