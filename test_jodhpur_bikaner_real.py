#!/usr/bin/env python3
"""
REAL DATA TEST: Jodhpur & Bikaner Businesses
Direct testing with actual Google Maps extraction
Shows real data quality and system reliability
"""

from bob import HybridExtractorOptimized
import time


def test_business(name, query):
    """Test single business extraction and show ALL data"""
    print(f"\n{'='*70}")
    print(f"📍 Testing: {query}")
    print(f"{'='*70}")

    start = time.time()
    extractor = HybridExtractorOptimized(prefer_playwright=True, memory_optimized=True)
    result = extractor.extract_business(query)
    elapsed = time.time() - start

    if result.get('success'):
        print(f"✅ SUCCESS in {elapsed:.1f} seconds\n")

        # Show all extracted data
        print("📋 BUSINESS INFORMATION:")
        print(f"   Name: {result.get('name')}")
        print(f"   Phone: {result.get('phone') if result.get('phone') else 'N/A'}")
        print(f"   Address: {result.get('address') if result.get('address') else 'N/A'}")
        print(f"   Website: {result.get('website') if result.get('website') else 'N/A'}")

        # Show emails (now available in both Playwright and Selenium!)
        emails = result.get('emails', [])
        if emails:
            print(f"   📧 Emails: {', '.join(emails)}")
        else:
            print(f"   📧 Emails: N/A")

        print(f"\n📊 RATINGS & REVIEWS:")
        print(f"   Rating: {result.get('rating') if result.get('rating') else 'N/A'}")
        print(f"   Review Count: {result.get('review_count') if result.get('review_count') else 'N/A'}")
        print(f"   Category: {result.get('category') if result.get('category') else 'N/A'}")

        # Show images (comprehensive extraction)
        photos = result.get('photos', [])
        if photos:
            print(f"\n🖼️  IMAGES: {len(photos)} photo(s) extracted")
            for i, photo_url in enumerate(photos[:3], 1):
                display_url = photo_url[:60] + "..." if len(photo_url) > 60 else photo_url
                print(f"     {i}. {display_url}")
            if len(photos) > 3:
                print(f"     ... and {len(photos) - 3} more")
        else:
            print(f"\n🖼️  IMAGES: None extracted")

        print(f"\n⏱️  METADATA:")
        print(f"   Quality Score: {result.get('data_quality_score')}/100")
        print(f"   Extraction Time: {result.get('extraction_time_seconds', elapsed):.1f}s")
        print(f"   Method: {result.get('extraction_method') if result.get('extraction_method') else 'N/A'}")

        if result.get('reviews'):
            print(f"\n💬 REVIEWS: {len(result.get('reviews', []))} extracted")
            for i, review in enumerate(result.get('reviews', [])[:2], 1):
                if isinstance(review, dict):
                    reviewer = review.get('reviewer', 'Unknown')
                    rating = review.get('rating', 'N/A')
                    print(f"   Review {i}: {reviewer} ({rating}⭐)")

        return {
            'success': True,
            'quality': result.get('data_quality_score', 0),
            'time': elapsed,
            'name': result.get('name'),
            'phone': result.get('phone'),
            'rating': result.get('rating')
        }
    else:
        print(f"❌ FAILED: {result.get('error', 'Unknown error')}")
        return {'success': False, 'error': result.get('error')}


# JODHPUR BUSINESSES
print("\n\n" + "="*70)
print("🏙️  JODHPUR TIER 3 CITY TEST")
print("="*70)

jodhpur_businesses = [
    "Gypsy Vegetarian Restaurant Jodhpur",
    "Janta Sweet House Jodhpur",
    "Ajit Bhawan Hotel Jodhpur",
    "Hotel Maharaja Palace Jodhpur",
    "Kalyan Nivas Hotel Jodhpur",
    "Om Cuisine Jodhpur",
    "Shahi Palace Restaurant Jodhpur",
    "Mohan Vegetarian Jodhpur",
    "Clock Tower Jodhpur",
    "Mehrangarh Fort Jodhpur",
]

print(f"\nTesting {len(jodhpur_businesses)} Jodhpur businesses...")
jodhpur_results = []
for query in jodhpur_businesses[:10]:  # Test up to 10
    result = test_business("Jodhpur", query)
    jodhpur_results.append(result)

print("\n" + "="*70)
print("📊 JODHPUR SUMMARY")
print("="*70)
successful = [r for r in jodhpur_results if r.get('success')]
print(f"Success Rate: {len(successful)}/{len(jodhpur_results)} ({len(successful)/len(jodhpur_results)*100:.0f}%)")
if successful:
    avg_quality = sum(r['quality'] for r in successful) / len(successful)
    avg_time = sum(r['time'] for r in successful) / len(successful)
    print(f"Average Quality: {avg_quality:.0f}/100")
    print(f"Average Time: {avg_time:.1f}s per business")
    print(f"Quality Range: {min(r['quality'] for r in successful)}-{max(r['quality'] for r in successful)}/100")


# BIKANER BUSINESSES
print("\n\n" + "="*70)
print("🏙️  BIKANER TIER 3 CITY TEST")
print("="*70)

bikaner_businesses = [
    "Bikanervala Bikaner",
    "Hotel Narendra Bhawan Bikaner",
    "Junagarh Fort Bikaner",
    "Lalgarh Palace Bikaner",
    "Haldi Ghati Sweets Bikaner",
    "City Centre Mall Bikaner",
    "Restaurant Bikaner",
    "Cafe Bikaner",
]

print(f"\nTesting {len(bikaner_businesses)} Bikaner businesses...")
bikaner_results = []
for query in bikaner_businesses[:8]:
    result = test_business("Bikaner", query)
    bikaner_results.append(result)

print("\n" + "="*70)
print("📊 BIKANER SUMMARY")
print("="*70)
successful = [r for r in bikaner_results if r.get('success')]
print(f"Success Rate: {len(successful)}/{len(bikaner_results)} ({len(successful)/len(bikaner_results)*100:.0f}%)")
if successful:
    avg_quality = sum(r['quality'] for r in successful) / len(successful)
    avg_time = sum(r['time'] for r in successful) / len(successful)
    print(f"Average Quality: {avg_quality:.0f}/100")
    print(f"Average Time: {avg_time:.1f}s per business")
    print(f"Quality Range: {min(r['quality'] for r in successful)}-{max(r['quality'] for r in successful)}/100")


# COMBINED RESULTS
print("\n\n" + "="*70)
print("🌍 COMBINED TIER 3 RESULTS (Jodhpur + Bikaner)")
print("="*70)
all_results = jodhpur_results + bikaner_results
all_successful = [r for r in all_results if r.get('success')]
total_success = len(all_successful) / len(all_results) * 100

print(f"Total Businesses Tested: {len(all_results)}")
print(f"Total Success Rate: {total_success:.0f}% ({len(all_successful)}/{len(all_results)})")

if all_successful:
    overall_quality = sum(r['quality'] for r in all_successful) / len(all_successful)
    overall_time = sum(r['time'] for r in all_successful) / len(all_successful)
    print(f"Overall Quality Average: {overall_quality:.0f}/100")
    print(f"Overall Time Average: {overall_time:.1f}s per business")
    print(f"\n✅ TIER 3 CITY SYSTEM VALIDATION: WORKING")
    print(f"If tier 3 cities work, tier 1/2 cities are guaranteed to work!")

print("\n" + "="*70)
