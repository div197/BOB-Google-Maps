#!/usr/bin/env python3
"""
Debug extraction to understand result format
"""

import sys
import json

# Add the project root to Python path
sys.path.insert(0, '/Users/aaple30/Documents/3-10-2025/BOB-Google-Maps')

from bob.extractors.selenium_optimized import SeleniumExtractorOptimized

def main():
    """Debug extraction to understand result format."""
    print("🔱 DEBUG EXTRACTION")
    print("=" * 40)

    # Test with one query
    business_name = "Office Furniture Dubai"
    print(f"🔍 Extracting: {business_name}")

    extractor = SeleniumExtractorOptimized(headless=True)
    result = extractor.extract_business_optimized(business_name, include_reviews=False, max_reviews=0)

    print(f"   Result type: {type(result)}")
    print(f"   Result keys: {list(result.keys()) if result else 'None'}")
    print(f"   Success: {result.get('success') if result else 'None'}")

    if result:
        print(f"   Name: {result.get('name', 'N/A')}")
        print(f"   Rating: {result.get('rating', 'N/A')}")
        print(f"   Address: {result.get('address', 'N/A')}")
        print(f"   Phone: {result.get('phone', 'N/A')}")
        print(f"   Website: {result.get('website', 'N/A')}")
        print(f"   Category: {result.get('category', 'N/A')}")
        print(f"   Quality Score: {result.get('data_quality_score', 'N/A')}")

        # Save full result for inspection
        with open('/Users/aaple30/Documents/3-10-2025/BOB-Google-Maps/debug_result.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Full result saved to debug_result.json")

if __name__ == "__main__":
    main()
