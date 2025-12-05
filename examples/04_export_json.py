#!/usr/bin/env python3
"""
Example 4: Export to JSON

Save extraction results to a JSON file.
"""

import asyncio
import json
from bob import PlaywrightExtractorOptimized


async def main():
    """Extract and export to JSON."""
    
    print("🔱 BOB Google Maps v4.3.0 - Export to JSON")
    print("=" * 60)
    
    extractor = PlaywrightExtractorOptimized(headless=True)
    
    # Extract multiple businesses
    queries = [
        "Starbucks Times Square NYC",
        "Apple Store Fifth Avenue NYC"
    ]
    
    results = []
    
    for query in queries:
        print(f"\n📍 Extracting: {query}")
        result = await extractor.extract_business_optimized(
            query,
            include_reviews=False
        )
        
        if result.get('success'):
            results.append({
                'name': result.get('name'),
                'phone': result.get('phone'),
                'address': result.get('address'),
                'website': result.get('website'),
                'rating': result.get('rating'),
                'latitude': result.get('latitude'),
                'longitude': result.get('longitude'),
                'quality_score': result.get('quality_score')
            })
            print(f"   ✅ {result.get('name')}")
        else:
            print(f"   ❌ Failed")
    
    # Export to JSON
    output_file = 'businesses.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Saved {len(results)} businesses to {output_file}")


if __name__ == "__main__":
    asyncio.run(main())
