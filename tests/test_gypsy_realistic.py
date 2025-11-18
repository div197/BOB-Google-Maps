#!/usr/bin/env python3
"""
HIGHLY REALISTIC TEST - GYPSY RESTAURANT JODHPUR
Known: website=gypsyfoods.in, email=gypsyfoodservices@gmail.com
"""

import time
from datetime import datetime
from bob import HybridExtractorOptimized

print("\n" + "="*90)
print("🔥 HIGHLY REALISTIC TEST - GYPSY RESTAURANT JODHPUR")
print("="*90)
print(f"Test Start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("\nKnown Information:")
print("  - Website: gypsyfoods.in")
print("  - Email: gypsyfoodservices@gmail.com")
print("="*90 + "\n")

extractor = HybridExtractorOptimized(
    prefer_playwright=True,
    memory_optimized=False
)

start = time.time()
result = extractor.extract_business("Gypsy Vegetarian Restaurant Jodhpur")
elapsed = time.time() - start

print("\n" + "="*90)
print("📊 EXTRACTION RESULTS")
print("="*90 + "\n")

if result.get('success'):
    print("✅ Extraction Status: SUCCESS\n")

    print("📍 BASIC INFO")
    print(f"  Name: {result.get('name', 'N/A')}")
    print(f"  Phone: {result.get('phone', 'N/A')}")
    print(f"  Address: {result.get('address', 'N/A')}")

    website = result.get('website', 'N/A')
    emails = result.get('emails', [])
    photos = result.get('photos', [])
    reviews = result.get('reviews', [])
    quality = result.get('data_quality_score', 0)

    print(f"\n🌐 WEBSITE")
    print(f"  Extracted: {website}")
    is_google = 'google.com' in str(website).lower()
    print(f"  Is Google URL: {'YES ⚠️' if is_google else 'NO ✅'}")

    print(f"\n📧 EMAIL EXTRACTION")
    print(f"  Found: {len(emails)}")
    if emails:
        for email in emails:
            print(f"    - {email}")
        print(f"  Status: ✅ WORKING")
    else:
        print(f"  Status: ❌ NOT WORKING")
        if is_google:
            print(f"  Reason: Website is Google URL, not actual business website")

    print(f"\n🖼️  IMAGE EXTRACTION")
    print(f"  Found: {len(photos)}")
    if photos:
        for i, photo in enumerate(photos[:2], 1):
            print(f"    {i}. {photo[:80]}...")
        print(f"  Status: ✅ WORKING")
    else:
        print(f"  Status: ❌ NOT WORKING")

    print(f"\n⭐ REVIEWS: {len(reviews)}")
    print(f"  Quality Score: {quality}/100")
    print(f"  Time: {elapsed:.1f}s")

    print(f"\n{'='*90}")
    if emails and len(photos) > 0:
        print("✅ BOTH EMAIL AND IMAGE EXTRACTION WORKING!")
    elif emails:
        print("⚠️  EMAIL WORKING, IMAGE NEEDS FIX")
    elif len(photos) > 0:
        print("⚠️  IMAGE WORKING, EMAIL NEEDS FIX")
    else:
        print("❌ BOTH NEED DEBUGGING")

else:
    print(f"❌ Failed: {result.get('error')}")

print("="*90 + "\n")
