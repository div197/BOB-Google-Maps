#!/usr/bin/env python3
"""
Debug exactly what website extraction is returning
"""
import time
from bob import HybridExtractorOptimized

extractor = HybridExtractorOptimized(prefer_playwright=True, memory_optimized=False)

# Test Gypsy Restaurant which is known to have gypsyfoods.in
result = extractor.extract_business("Gypsy Vegetarian Restaurant Jodhpur")

print("\n" + "="*90)
print("🔍 WEBSITE EXTRACTION DEBUG")
print("="*90)

website = result.get('website', 'NONE')

print(f"\nExtracted Website: {website}\n")

# Analyze what was returned
if 'google.com' in str(website).lower():
    print("❌ PROBLEM: Website is still a Google URL!")
    print(f"\nTypes of Google URLs found:")
    if 'viewer/chooseprovider' in website:
        print("  - Google Maps provider chooser")
    elif 'maps/reserve' in website:
        print("  - Google Maps booking/reservation")
    elif 'maps/place' in website:
        print("  - Google Maps place page")
    elif '/url?' in website:
        print("  - Google redirect with ?q= parameter")
        # Try to extract actual URL
        from bob.utils.email_extractor import extract_real_url_from_google_redirect
        actual = extract_real_url_from_google_redirect(website)
        print(f"  - Actual URL from redirect: {actual}")
    else:
        print(f"  - Unknown Google URL type")

    print(f"\n⚠️  EMAIL EXTRACTION FAILED because website is Google URL")
    print(f"✅ EMAIL EXTRACTOR correctly rejects Google URLs (designed safety feature)")
else:
    print("✅ Website is NOT a Google URL - good!")
    print(f"Website domain: {website.split('/')[2] if '/' in website else 'UNKNOWN'}")

print("\n" + "="*90)
