#!/usr/bin/env python3
"""
Example 7: City-Wide Extraction

Extract all businesses from a specific city category.
This example shows how to do bulk extraction like in the jodhpur/ folder.
"""

import asyncio
from playwright.async_api import async_playwright
from bob import PlaywrightExtractorOptimized
from bob.utils.exporters import export_to_json, export_to_csv


async def collect_business_urls(query: str, max_results: int = 20) -> list:
    """
    Collect business URLs from a Google Maps category search.
    
    Args:
        query: Search query like "restaurants in Mumbai"
        max_results: Maximum businesses to collect
    
    Returns:
        List of Google Maps place URLs
    """
    urls = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        page = await context.new_page()
        
        # Navigate to search
        search_url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}?hl=en"
        await page.goto(search_url)
        await page.wait_for_timeout(3000)
        
        # Scroll to load results
        feed = page.locator('div[role="feed"]')
        for _ in range(5):
            try:
                await feed.evaluate('el => el.scrollTop = el.scrollHeight')
                await page.wait_for_timeout(1000)
            except:
                break
        
        # Collect URLs
        links = await page.locator('a[href*="/place/"]').all()
        seen = set()
        
        for link in links[:max_results]:
            try:
                href = await link.get_attribute('href')
                if href and href not in seen:
                    seen.add(href)
                    urls.append(href)
            except:
                pass
        
        await browser.close()
    
    return urls


async def extract_city_category(
    city: str,
    category: str,
    max_businesses: int = 10,
    output_file: str = None
):
    """
    Extract all businesses from a city category.
    
    Args:
        city: City name (e.g., "Mumbai")
        category: Business category (e.g., "restaurants")
        max_businesses: Maximum businesses to extract
        output_file: Output JSON file path
    """
    query = f"{category} in {city}"
    
    print(f"\n🔱 BOB Google Maps v4.3.0 - City Extraction")
    print("=" * 60)
    print(f"📍 City: {city}")
    print(f"📂 Category: {category}")
    print(f"📊 Max businesses: {max_businesses}")
    print("=" * 60)
    
    # Step 1: Collect URLs
    print(f"\n🔍 Searching for '{query}'...")
    urls = await collect_business_urls(query, max_businesses)
    print(f"   Found {len(urls)} businesses")
    
    if not urls:
        print("❌ No businesses found")
        return []
    
    # Step 2: Extract each business
    print(f"\n📦 Extracting business data...")
    
    extractor = PlaywrightExtractorOptimized(headless=True)
    results = []
    
    for i, url in enumerate(urls, 1):
        print(f"   [{i}/{len(urls)}] ", end="", flush=True)
        
        result = await extractor.extract_business_optimized(
            url,
            include_reviews=True,
            max_reviews=3
        )
        
        if result.get('success'):
            results.append(result)
            print(f"✅ {result.get('name', 'Unknown')[:30]}")
        else:
            print(f"❌ Failed")
        
        # Rate limiting
        if i < len(urls):
            await asyncio.sleep(2)
    
    # Step 3: Save results
    if results and output_file:
        export_to_json(results, output_file)
        
        # Also create CSV
        csv_file = output_file.replace('.json', '.csv')
        export_to_csv(results, csv_file)
    
    # Summary
    print("\n" + "=" * 60)
    print(f"✅ EXTRACTION COMPLETE")
    print(f"   Extracted: {len(results)}/{len(urls)} businesses")
    
    if results:
        avg_quality = sum(r.get('quality_score', 0) for r in results) / len(results)
        print(f"   Average Quality: {avg_quality:.0f}/100")
        
        if output_file:
            print(f"   Output: {output_file}")
    
    return results


async def main():
    """Example: Extract top 10 restaurants in Mumbai."""
    
    results = await extract_city_category(
        city="Mumbai",
        category="restaurants",
        max_businesses=5,  # Keep small for example
        output_file="output/mumbai_restaurants.json"
    )
    
    # Show extracted data
    if results:
        print("\n📋 Extracted Businesses:")
        for r in results:
            print(f"   • {r.get('name')} - {r.get('rating')}⭐ - {r.get('phone', 'N/A')}")


if __name__ == "__main__":
    asyncio.run(main())
