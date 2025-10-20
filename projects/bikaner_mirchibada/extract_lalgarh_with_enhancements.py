#!/usr/bin/env python3
"""
🏛️ LALGARH PALACE V3.4 ENHANCED EXTRACTION
Direct extraction with email + GPS + hours improvements
"""

import json
import requests
import re
import sys
from pathlib import Path
from datetime import datetime

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from bob import HybridExtractorOptimized

def extract_emails_enhanced(website_url):
    """Enhanced email extraction from website"""
    if not website_url or "google" in website_url.lower():
        return []

    try:
        response = requests.get(website_url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

        if response.status_code == 200:
            patterns = [
                r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
                r'mailto:([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
            ]

            emails = set()
            for pattern in patterns:
                found = re.findall(pattern, response.text)
                emails.update([e.lower() for e in found])

            # Filter spam
            spam_keywords = ['example', 'test', 'noreply', 'no-reply', 'temp', 'fake']
            filtered = [e for e in emails if not any(k in e for k in spam_keywords)]
            return list(filtered)[:5]
    except Exception as e:
        print(f"  ℹ️ Email extraction: {str(e)[:40]}")

    return []

def extract_gps(address):
    """Extract GPS from address"""
    if not address:
        return None

    try:
        from geopy.geocoders import Nominatim
        geolocator = Nominatim(user_agent="bob_lalgarh_v34")
        location = geolocator.geocode(address, timeout=10)

        if location:
            return {
                "latitude": round(location.latitude, 6),
                "longitude": round(location.longitude, 6),
                "method": "Nominatim Geocoding",
                "maps_url": f"https://www.google.com/maps/@{location.latitude},{location.longitude},15z"
            }
    except Exception as e:
        print(f"  ℹ️ GPS extraction: {str(e)[:40]}")

    return None

def extract_hours(website_url):
    """Try to extract hours"""
    if not website_url or "google" in website_url.lower():
        return None

    try:
        response = requests.get(website_url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

        if response.status_code == 200:
            patterns = [
                r'(\d{1,2}):(\d{2})\s*(?:am|pm|AM|PM)?\s*-\s*(\d{1,2}):(\d{2})',
                r'([0-2][0-3]):([0-5][0-9])\s*-\s*([0-2][0-3]):([0-5][0-9])',
            ]

            for pattern in patterns:
                if re.search(pattern, response.text):
                    return {"status": "Found in website", "method": "HTML pattern"}
    except:
        pass

    return None

def main():
    print("\n" + "="*70)
    print("🏛️ LALGARH PALACE BIKANER - ENHANCED EXTRACTION V3.4")
    print("="*70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # STEP 1: Core extraction
    print("📍 STEP 1: Core Extraction")
    print("-"*70)

    extractor = HybridExtractorOptimized(
        prefer_playwright=True,
        memory_optimized=True
    )

    result = extractor.extract_business("Lalgarh Palace", include_reviews=True, max_reviews=5)

    print(f"✅ Extraction successful: {result.get('success', False)}")
    print(f"   Extraction Time: {result.get('extraction_time_seconds', 'N/A')}s")
    print(f"   Quality Score: {result.get('quality_score', 'N/A')}/100")

    # Prepare enhanced data
    enhanced_data = {
        "extraction_version": "V3.4",
        "timestamp": datetime.now().isoformat(),
        "raw_result": result,  # Store everything
        "enhancements": {}
    }

    # Try to extract improvements
    if result.get('success'):
        # Get extracted data (handle different result formats)
        business_data = result.get('business', result)

        # Email extraction
        print("\n📧 STEP 2: Email Extraction")
        print("-"*70)
        website = business_data.get('website') if isinstance(business_data, dict) else None
        if website:
            emails = extract_emails_enhanced(website)
            if emails:
                print(f"✅ Found {len(emails)} email(s):")
                for e in emails:
                    print(f"   📧 {e}")
                enhanced_data["enhancements"]["emails"] = {"status": "✅", "count": len(emails), "emails": emails}
            else:
                print("⚠️ No emails found")
                enhanced_data["enhancements"]["emails"] = {"status": "⚠️", "count": 0}
        else:
            print("⚠️ Website not available for email extraction")
            enhanced_data["enhancements"]["emails"] = {"status": "⚠️", "reason": "No website"}

        # GPS extraction
        print("\n🧭 STEP 3: GPS Extraction")
        print("-"*70)
        address = business_data.get('address') if isinstance(business_data, dict) else None
        if address:
            gps = extract_gps(address)
            if gps:
                print(f"✅ GPS Coordinates:")
                print(f"   📍 Lat: {gps['latitude']}")
                print(f"   📍 Lon: {gps['longitude']}")
                print(f"   🗺️  {gps['maps_url']}")
                enhanced_data["enhancements"]["gps"] = {"status": "✅", "data": gps}
            else:
                print("⚠️ Geocoding failed")
                enhanced_data["enhancements"]["gps"] = {"status": "⚠️"}
        else:
            print("⚠️ Address not available")
            enhanced_data["enhancements"]["gps"] = {"status": "⚠️", "reason": "No address"}

        # Hours extraction
        print("\n⏰ STEP 4: Hours Extraction")
        print("-"*70)
        if website:
            hours = extract_hours(website)
            if hours:
                print(f"✅ Hours found: {hours}")
                enhanced_data["enhancements"]["hours"] = {"status": "✅", "data": hours}
            else:
                print("⚠️ Hours not detected in HTML")
                enhanced_data["enhancements"]["hours"] = {"status": "⚠️"}
        else:
            print("⚠️ Website not available")
            enhanced_data["enhancements"]["hours"] = {"status": "⚠️"}

    # Save results
    print("\n" + "="*70)
    print("💾 SAVING RESULTS")
    print("="*70)

    output_dir = Path(__file__).parent / "data"
    output_dir.mkdir(exist_ok=True)

    json_path = output_dir / "lalgarh_palace_enhanced_v34.json"
    with open(json_path, 'w') as f:
        json.dump(enhanced_data, f, indent=2, default=str)

    print(f"✅ Saved to: {json_path}")
    print(f"\n✨ ENHANCEMENT SUMMARY:")
    print(f"   📧 Emails: {enhanced_data['enhancements'].get('emails', {}).get('status', 'N/A')}")
    print(f"   🧭 GPS: {enhanced_data['enhancements'].get('gps', {}).get('status', 'N/A')}")
    print(f"   ⏰ Hours: {enhanced_data['enhancements'].get('hours', {}).get('status', 'N/A')}")
    print("\n🎉 ENHANCED EXTRACTION COMPLETE")

if __name__ == "__main__":
    main()
