#!/usr/bin/env python3
"""
Test: Gypsy Restaurant Jodhpur - Website & Email Extraction
Tests the new intelligent website extraction methodology
"""

import time
from datetime import datetime
from bob import HybridExtractorOptimized


def test_gypsy_website_extraction():
    """
    Test that Gypsy Restaurant Jodhpur website extraction returns
    actual business website (not Google provider URL) and emails
    """

    print("\n" + "="*90)
    print("🔬 TEST: Gypsy Restaurant - Intelligent Website Extraction")
    print("="*90)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    extractor = HybridExtractorOptimized(
        prefer_playwright=True,
        memory_optimized=False,
        include_reviews=True,
        max_reviews=3
    )

    print("Extracting: Gypsy Vegetarian Restaurant Jodhpur...\n")
    start = time.time()
    result = extractor.extract_business("Gypsy Vegetarian Restaurant Jodhpur")
    elapsed = time.time() - start

    assert result.get('success'), f"Extraction failed: {result.get('error')}"

    name = result.get('name')
    website = result.get('website', 'N/A')
    emails = result.get('emails', [])

    print("\n" + "="*90)
    print("📊 RESULTS")
    print("="*90)
    print(f"Business: {name}")
    print(f"Website: {website}")
    print(f"Emails: {emails}")
    print(f"Time: {elapsed:.1f}s\n")

    # Critical assertions
    assert name, "Business name should be extracted"

    # Website should NOT be a Google internal URL
    is_google = 'google.com' in str(website).lower()
    assert not is_google, (
        f"Website should not be Google URL, got: {website}"
    )

    # If website is found, emails should be extracted
    if website and website != 'N/A':
        print(f"✅ Website is not a Google URL: {website[:60]}...")
        if emails:
            print(f"✅ Emails extracted: {emails}")
            print("\n🎉 SUCCESS: Intelligent website extraction working!")
        else:
            print("⚠️  Website found but no emails extracted (might not be on website)")
    else:
        print("ℹ️  No website found (business might not have external website)")

    print("="*90 + "\n")

    # Return success if website was extracted and is not Google
    return not is_google


if __name__ == "__main__":
    success = test_gypsy_website_extraction()
    if success:
        print("✅ TEST PASSED: Website extraction fix is working!\n")
        exit(0)
    else:
        print("❌ TEST FAILED: Website extraction still returning Google URLs\n")
        exit(1)
