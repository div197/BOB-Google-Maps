#!/usr/bin/env python3
"""
Debug extraction to understand what websites and images are being extracted
"""

import time
from datetime import datetime
from bob import HybridExtractorOptimized

# Test with one specific restaurant
restaurant = "Gypsy Vegetarian Restaurant Jodhpur"

print(f"\n🔍 DEBUGGING EXTRACTION FOR: {restaurant}\n")

extractor = HybridExtractorOptimized(
    prefer_playwright=True,
    memory_optimized=True
)

start = time.time()
result = extractor.extract_business(restaurant)
elapsed = time.time() - start

print(f"\n{'='*80}")
print("FULL EXTRACTION RESULT")
print(f"{'='*80}\n")

if result.get('success'):
    print(f"✅ Success")
    print(f"Name: {result.get('name')}")
    print(f"Phone: {result.get('phone')}")
    print(f"Address: {result.get('address')}")
    print(f"Rating: {result.get('rating')}")
    print(f"Website: {result.get('website')}")
    print(f"Category: {result.get('category')}")
    print(f"Quality Score: {result.get('data_quality_score')}")
    print(f"Time: {elapsed:.1f}s")

    print(f"\n{'='*80}")
    print("📧 EMAIL EXTRACTION RESULT")
    print(f"{'='*80}")
    emails = result.get('emails', [])
    print(f"Emails found: {len(emails)}")
    for email in emails:
        print(f"  - {email}")

    print(f"\n{'='*80}")
    print("📸 IMAGE EXTRACTION RESULT")
    print(f"{'='*80}")
    photos = result.get('photos', [])
    print(f"Images found: {len(photos)}")
    for i, photo in enumerate(photos[:3], 1):
        print(f"  {i}. {photo[:100]}...")

    print(f"\n{'='*80}")
    print("⭐ REVIEW EXTRACTION RESULT")
    print(f"{'='*80}")
    reviews = result.get('reviews', [])
    print(f"Reviews found: {len(reviews)}")

else:
    print(f"❌ Failed: {result.get('error')}")
