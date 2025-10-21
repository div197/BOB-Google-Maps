#!/usr/bin/env python3
"""
⏰ IMPROVED BUSINESS HOURS EXTRACTION MODULE
V3.4.1 - Enhanced patterns + Better parsing

Status: ✅ SAFE TO USE
"""

import re
import requests
from typing import Optional, Dict

def extract_business_hours(website_url: str, timeout: int = 10) -> Optional[Dict]:
    """
    Extract business hours from website with multiple patterns.

    Supports:
    - 9:00 AM - 5:00 PM
    - 09:00 - 17:00
    - Mon-Fri: 9 AM - 5 PM
    - Open 24/7
    - Closed

    Args:
        website_url: Website URL
        timeout: Request timeout

    Returns:
        dict: Hours data or None
    """
    if not website_url or 'google' in website_url.lower():
        return None

    # Ensure URL has protocol
    if not website_url.startswith(('http://', 'https://')):
        website_url = 'https://' + website_url

    try:
        print(f"  ⏰ Fetching website for hours...")
        response = requests.get(
            website_url,
            timeout=timeout,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
            allow_redirects=True
        )

        if response.status_code != 200:
            print(f"  ⚠️ Could not fetch website ({response.status_code})")
            return None

        html = response.text.lower()  # Search in lowercase
        print(f"  📄 Website fetched ({len(html)} bytes)")

    except Exception as e:
        print(f"  ⚠️ Fetch failed: {str(e)[:40]}")
        return None

    # PATTERN 1: Open 24/7
    if re.search(r'24\s*[/x-]?\s*7|open\s+24\s+hours|24\s+hour|open\s+around\s+clock', html):
        print(f"  ✅ Found: Open 24/7")
        return {
            "status": "Open 24/7",
            "pattern": "24x7_keyword",
            "full_hours": "24 Hours - 7 Days"
        }

    # PATTERN 2: Closed
    if re.search(r'permanently\s+closed|closed\s+indefinitely|out\s+of\s+business', html):
        print(f"  ✅ Found: Closed")
        return {
            "status": "Closed",
            "pattern": "closed_keyword",
            "full_hours": "Not Operating"
        }

    # PATTERN 3: Hours with AM/PM (9:00 AM - 5:00 PM)
    pattern_ampm = r'(\d{1,2}):?(\d{2})?\s*(?:am|a\.m\.|a\.?m?\.?)\s*(?:-|to)\s*(\d{1,2}):?(\d{2})?\s*(?:pm|p\.m\.|p\.?m?\.?)'
    match = re.search(pattern_ampm, html, re.IGNORECASE)
    if match:
        print(f"  ✅ Found: Hours with AM/PM")
        return {
            "status": "Hours Found (12-hour format)",
            "pattern": "ampm_hours",
            "match": match.group(0),
            "note": "Use website contact or Google Maps for full details"
        }

    # PATTERN 4: 24-hour format (09:00 - 17:00)
    pattern_24h = r'(\d{1,2}):(\d{2})\s*(?:-|to)\s*(\d{1,2}):(\d{2})'
    match = re.search(pattern_24h, html)
    if match:
        print(f"  ✅ Found: Hours (24-hour format)")
        return {
            "status": "Hours Found (24-hour format)",
            "pattern": "24h_hours",
            "match": match.group(0),
            "note": "Use website contact or Google Maps for full details"
        }

    # PATTERN 5: Day-specific hours
    pattern_days = r'(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\s*:?\s*(\d{1,2}):?(\d{2})?\s*(?:-|to)\s*(\d{1,2}):?(\d{2})?'
    match = re.search(pattern_days, html, re.IGNORECASE)
    if match:
        print(f"  ✅ Found: Day-specific hours")
        return {
            "status": "Day-specific Hours Found",
            "pattern": "day_specific_hours",
            "match": match.group(0),
            "note": "Use website contact or Google Maps for full details"
        }

    # PATTERN 6: "Hours:" or "Opening Hours:"
    pattern_label = r'(?:opening\s+)?hours?\s*:?\s*([^\n<]+?)(?:\n|<|$)'
    match = re.search(pattern_label, html, re.IGNORECASE)
    if match and len(match.group(1).strip()) > 5:
        content = match.group(1).strip()[:50]
        if any(char.isdigit() for char in content):
            print(f"  ✅ Found: Hours section")
            return {
                "status": "Hours Section Found",
                "pattern": "hours_label",
                "content": content,
                "note": "Use website contact or Google Maps for full details"
            }

    print(f"  ⚠️ No standard hours pattern found")
    return None

def test_hours_extraction():
    """Test hours extraction"""

    print("\n" + "="*70)
    print("⏰ TESTING IMPROVED HOURS EXTRACTION V3.1")
    print("="*70 + "\n")

    print("TEST 1: Lalgarh Palace Website")
    print("-" * 70)
    result = extract_business_hours("http://www.lallgarhpalace.com/")
    if result:
        for key, value in result.items():
            print(f"  {key}: {value}")
    else:
        print("  No hours found (normal - not all sites have explicit hours)")
    print()

    print("TEST 2: Invalid URL")
    print("-" * 70)
    result = extract_business_hours("https://not-real-website-xyz.invalid/")
    if result:
        for key, value in result.items():
            print(f"  {key}: {value}")
    else:
        print("  No result (expected)")
    print()

if __name__ == "__main__":
    test_hours_extraction()
