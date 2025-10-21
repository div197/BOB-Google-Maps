#!/usr/bin/env python3
"""
🧭 IMPROVED GPS EXTRACTION MODULE
V3.4.1 - Retry logic + Fallback geocoding

Status: ✅ SAFE TO USE - Non-breaking improvements
"""

import time
from typing import Optional, Dict

def extract_gps_with_retry(address: str, max_retries: int = 3, timeout: int = 10) -> Optional[Dict]:
    """
    Extract GPS coordinates from address with retry logic.

    Strategy:
    1. Try geopy.Nominatim (OpenStreetMap) - free, reliable
    2. On timeout, retry with longer timeout
    3. On all failures, return fallback data with attempt count

    Args:
        address: Full address string
        max_retries: Number of retry attempts
        timeout: Request timeout in seconds

    Returns:
        dict: GPS data or None
    """
    if not address:
        return None

    try:
        from geopy.geocoders import Nominatim
        from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
    except ImportError:
        print("  ⚠️ geopy not installed, returning None")
        return None

    # Initialize geocoder
    geolocator = Nominatim(user_agent="bob_gps_v34")

    attempt = 0
    last_error = None

    # RETRY LOOP
    for attempt in range(max_retries):
        try:
            # Calculate timeout with backoff
            current_timeout = timeout + (attempt * 5)  # 10s, 15s, 20s
            attempt_num = attempt + 1

            print(f"  🔄 Geocoding attempt {attempt_num}/{max_retries} (timeout: {current_timeout}s)...")

            # Try to geocode
            location = geolocator.geocode(address, timeout=current_timeout)

            if location:
                print(f"  ✅ Success on attempt {attempt_num}!")
                return {
                    "latitude": round(location.latitude, 6),
                    "longitude": round(location.longitude, 6),
                    "method": "Nominatim Geocoding (OSM)",
                    "full_address": location.address,
                    "attempts": attempt_num,
                    "status": "success"
                }

            print(f"  ⚠️ No location found on attempt {attempt_num}")
            last_error = "No location found"

        except GeocoderTimedOut:
            last_error = f"Timeout on attempt {attempt_num}"
            print(f"  ⏱️ {last_error}")
            if attempt < max_retries - 1:
                print(f"  ⏸️ Waiting 2 seconds before retry...")
                time.sleep(2)
            continue

        except GeocoderUnavailable:
            last_error = f"Service unavailable on attempt {attempt_num}"
            print(f"  🚫 {last_error}")
            if attempt < max_retries - 1:
                print(f"  ⏸️ Waiting 3 seconds before retry...")
                time.sleep(3)
            continue

        except Exception as e:
            last_error = f"Error on attempt {attempt_num}: {str(e)[:40]}"
            print(f"  ❌ {last_error}")
            if attempt < max_retries - 1:
                time.sleep(1)
            continue

    # ALL RETRIES FAILED
    print(f"  ❌ All {max_retries} geocoding attempts failed")
    print(f"  Last error: {last_error}")

    # Return fallback data
    return {
        "latitude": None,
        "longitude": None,
        "method": "Nominatim Geocoding (OSM)",
        "full_address": address,
        "attempts": attempt + 1,
        "status": "failed",
        "last_error": last_error,
        "note": "Could not geocode - address may be incomplete or service unavailable"
    }

def test_gps_extraction():
    """Test the improved GPS extraction"""

    print("\n" + "="*70)
    print("🧪 TESTING IMPROVED GPS EXTRACTION V3.1")
    print("="*70 + "\n")

    test_addresses = [
        ("28RJ+6F3, Samta Nagar, Bikaner, Rajasthan 334001", "Lalgarh Palace"),
        ("Bikaner, Rajasthan, India", "Bikaner city"),
        ("Invalid #@$% Address #@$%", "Invalid address"),
    ]

    for address, description in test_addresses:
        print(f"TEST: {description}")
        print(f"Address: {address}")
        print("-" * 70)

        result = extract_gps_with_retry(address, max_retries=2, timeout=5)

        if result:
            print(f"Result:")
            for key, value in result.items():
                print(f"  {key}: {value}")
        else:
            print(f"Result: None")

        print()

if __name__ == "__main__":
    test_gps_extraction()
