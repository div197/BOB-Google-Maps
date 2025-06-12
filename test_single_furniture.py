#!/usr/bin/env python3
"""Test single furniture manufacturer extraction"""

import asyncio
import sys
sys.path.append('.')

async def test_single_furniture():
    try:
        from bob_core.scraper import GoogleMapsScraper
        
        print('🔍 Testing Single Furniture Manufacturer Extraction')
        print('=' * 60)
        
        scraper = GoogleMapsScraper(headless=True)
        
        # Search for furniture manufacturer in KL
        url = 'https://maps.google.com/maps?q=furniture+manufacturer+kuala+lumpur&hl=en'
        
        print(f'🌐 Searching: {url}')
        
        result = scraper.scrape_url(
            url=url,
            extract_reviews=True,
            max_reviews=5,
            business_only=False
        )
        
        if result['success']:
            business = result['business_info']
            print(f'✅ Found: {business.get("name", "Unknown")}')
            print(f'📍 Address: {business.get("address", "N/A")}')
            print(f'⭐ Rating: {business.get("rating", "N/A")}')
            print(f'📞 Phone: {business.get("phone", "N/A")}')
            print(f'🌐 Website: {business.get("website", "N/A")}')
            print(f'💬 Reviews: {len(result.get("reviews", []))}')
            
            # Show first review if available
            reviews = result.get('reviews', [])
            if reviews:
                print(f'📝 Latest Review: {reviews[0].get("text", "")[:100]}...')
            
            print('🔱 Single extraction successful!')
            return True
        else:
            print(f'❌ Failed: {result.get("error_message", "Unknown error")}')
            return False
            
    except Exception as e:
        print(f'❌ Error: {e}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_single_furniture())
    print(f'\n🕉️ Test Result: {"SUCCESS" if success else "FAILED"} 🕉️') 