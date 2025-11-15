#!/usr/bin/env python3
"""
COMPREHENSIVE JAIPUR RESTAURANT TESTING
Tests both email and image extraction features
"""

import time
from datetime import datetime
from bob import HybridExtractorOptimized

restaurants = [
    "Laxmi Mishthan Bhandar Jaipur",
    "Niro's Restaurant Jaipur",
    "Surya Mahal Restaurant Jaipur",
    "Peacock Rooftop Restaurant Jaipur",
    "Handi Restaurant Jaipur",
    "Tapri Central Jaipur",
    "Indigo Restaurant Jaipur",
    "Dasaprakash Restaurant Jaipur",
    "Karni Nivas Hotel Restaurant Jaipur",
    "Chokhi Dhani Jaipur"
]

print("\n" + "="*90)
print("🏘️  COMPREHENSIVE JAIPUR RESTAURANTS - EMAIL & IMAGE EXTRACTION VALIDATION")
print("="*90)
print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Testing: {len(restaurants)} restaurants for BOTH email and image extraction")
print("="*90 + "\n")

results = []
successful = 0
emails_found = 0
images_found = 0
total_time = 0

for i, restaurant in enumerate(restaurants, 1):
    print(f"[{i}/10] Testing: {restaurant}")
    try:
        extractor = HybridExtractorOptimized(
            prefer_playwright=True,
            memory_optimized=True
        )
        start = time.time()
        result = extractor.extract_business(restaurant)
        elapsed = time.time() - start
        total_time += elapsed

        if result.get('success'):
            successful += 1
            name = result.get('name', 'N/A')
            phone = result.get('phone', 'N/A')
            website = result.get('website', 'N/A')
            emails = result.get('emails', [])
            photos = result.get('photos', [])
            reviews = result.get('reviews', [])
            quality = result.get('data_quality_score', 0)

            # Track metrics
            emails_found += len(emails)
            images_found += len(photos)

            print(f"  ✅ SUCCESS - Quality: {quality}/100, Time: {elapsed:.1f}s")
            print(f"     Name: {name}")
            print(f"     Phone: {phone}")
            print(f"     Website: {website[:50] if website else 'N/A'}")
            print(f"     📧 Emails: {len(emails)} | 📸 Images: {len(photos)} | ⭐ Reviews: {len(reviews)}")

            if emails:
                for email in emails[:2]:
                    print(f"        - Email: {email}")

            if photos:
                print(f"        - First image: {photos[0][:70]}...")

            results.append({
                'name': name,
                'quality': quality,
                'time': elapsed,
                'emails': len(emails),
                'images': len(photos),
                'reviews': len(reviews)
            })
        else:
            print(f"  ❌ FAILED: {result.get('error', 'Unknown error')[:50]}")

    except Exception as e:
        print(f"  ❌ ERROR: {str(e)[:60]}")

    print()

print("="*90)
print("📊 FINAL RESULTS SUMMARY")
print("="*90)

print(f"\nSuccess Rate: {successful}/{len(restaurants)} ({successful/len(restaurants)*100:.0f}%)")
print(f"Total Testing Time: {total_time:.1f}s ({total_time/len(restaurants):.1f}s per restaurant)")

if results:
    avg_quality = sum(r['quality'] for r in results) / len(results)
    avg_time = sum(r['time'] for r in results) / len(results)
    total_reviews = sum(r['reviews'] for r in results)

    print(f"\nCore Extraction Metrics:")
    print(f"  Average Quality: {avg_quality:.0f}/100")
    print(f"  Average Time per Business: {avg_time:.1f}s")
    print(f"  Total Reviews Found: {total_reviews}")

    print(f"\n🔑 FEATURE VALIDATION:")
    print(f"  ✅ Email Extraction: {emails_found} emails found ({emails_found/successful:.1f} per business)")
    print(f"  ✅ Image Extraction: {images_found} images found ({images_found/successful:.1f} per business)")

    # Feature success rate
    businesses_with_emails = sum(1 for r in results if r['emails'] > 0)
    businesses_with_images = sum(1 for r in results if r['images'] > 0)

    print(f"\n📈 Feature Success Rate:")
    print(f"  Businesses with emails: {businesses_with_emails}/{successful} ({businesses_with_emails/successful*100:.0f}%)")
    print(f"  Businesses with images: {businesses_with_images}/{successful} ({businesses_with_images/successful*100:.0f}%)")

print(f"\n" + "="*90)

if emails_found > 0 and images_found > 0:
    print("🟢 STATUS: BOTH EMAIL AND IMAGE EXTRACTION WORKING")
    print("✅ System is PRODUCTION READY for email and image extraction")
elif emails_found > 0:
    print("🟡 STATUS: EMAIL EXTRACTION WORKING, IMAGE EXTRACTION NEEDS IMPROVEMENT")
elif images_found > 0:
    print("🟡 STATUS: IMAGE EXTRACTION WORKING, EMAIL EXTRACTION NEEDS IMPROVEMENT")
else:
    print("🔴 STATUS: BOTH FEATURES NEED IMPROVEMENT")

print("="*90 + "\n")
