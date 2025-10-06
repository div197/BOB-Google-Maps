#!/usr/bin/env python3
"""
Quick test of Starbucks extraction with V3.3
"""

import asyncio
import json
import time
from bob.extractors.playwright import PlaywrightExtractor

async def test_starbucks():
    """Test Starbucks extraction"""

    print("\n" + "="*60)
    print("🎯 Testing V3.3 with Starbucks Jodhpur")
    print("="*60)

    extractor = PlaywrightExtractor(headless=True)

    start_time = time.time()

    try:
        result = await extractor.extract_business("Starbucks Jodhpur")
        extraction_time = time.time() - start_time

        print(f"\n✅ Extraction completed in {extraction_time:.1f}s")
        print(f"\n📊 Results:")
        print(f"  Name: {result.get('name', 'N/A')}")
        print(f"  Rating: {result.get('rating', 'N/A')}")
        print(f"  CID: {result.get('cid', 'N/A')}")
        print(f"  Emails: {result.get('emails', [])}")
        print(f"  Plus Code: {result.get('plus_code', 'N/A')}")
        print(f"  Service Options: {result.get('service_options', {})}")
        print(f"  Photos: {len(result.get('photos', []))}")
        print(f"  Quality Score: {result.get('data_quality_score', 0)}/100")

        # Save results
        output_file = "/tmp/starbucks_v3.3_results.json"
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\n💾 Results saved to: {output_file}")

        # Validate critical fields
        if result.get('rating') and result.get('cid'):
            print("\n✅ V3.3 VALIDATION: SUCCESS")
            print("Critical fields extracted successfully!")
        else:
            print("\n⚠️ V3.3 VALIDATION: PARTIAL SUCCESS")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

    finally:
        await extractor.close()

if __name__ == "__main__":
    asyncio.run(test_starbucks())