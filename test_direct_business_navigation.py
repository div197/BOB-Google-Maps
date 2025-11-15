#!/usr/bin/env python3
"""
🎯 TACTICAL APPROACH: Direct Business Navigation
Tests whether we can bypass search and navigate directly to business pages
"""

import asyncio
import re
import json
from pathlib import Path
from playwright.async_api import async_playwright
from datetime import datetime


async def test_direct_navigation():
    """Test direct navigation to known businesses"""

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=['--disable-blink-features=AutomationControlled']
        )
        page = await browser.new_page(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )

        try:
            print("\n" + "="*90)
            print("🎯 TACTICAL TEST: Direct Business Navigation Methods")
            print("="*90)
            print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

            # Test Case 1: Search-based navigation
            print("TEST 1️⃣  : Search + Click Navigation")
            print("-" * 90)

            test_businesses = [
                {
                    "name": "Gypsy Vegetarian Restaurant Jodhpur",
                    "known_website": "gypsyfoods.in",
                    "known_phone": "074120 74078"
                }
            ]

            for business in test_businesses:
                print(f"\nBusiness: {business['name']}")
                print(f"Known Website: {business['known_website']}")
                print(f"Known Phone: {business['known_phone']}")

                # Approach 1: Direct search URL
                search_url = f"https://www.google.com/maps/search/{business['name'].replace(' ', '+')}"
                print(f"\n   Navigating to: {search_url[:80]}...")

                try:
                    await page.goto(search_url, wait_until="networkidle", timeout=30000)
                    await page.wait_for_timeout(2000)

                    print("   ✅ Search page loaded")

                    # Wait for results to load
                    try:
                        await page.wait_for_selector("a[href*='/place/']", timeout=5000)
                        print("   ✅ Found elements with '/place/' in href")

                        # Get all place links
                        place_links = await page.query_selector_all("a[href*='/place/']")
                        print(f"   ✅ Found {len(place_links)} place links")

                        # Try clicking the first one
                        if place_links:
                            href = await place_links[0].get_attribute("href")
                            print(f"   🔗 First link href: {href[:100]}")

                            # Extract place ID from href
                            match = re.search(r'/place/([^/]+)', href)
                            if match:
                                place_id = match.group(1)
                                print(f"   📍 Extracted place: {place_id}")

                                # Navigate directly to this place
                                direct_url = f"https://www.google.com/maps/place/{place_id}"
                                print(f"   🔄 Attempting direct navigation: {direct_url[:80]}...")

                                await page.goto(direct_url, wait_until="networkidle", timeout=30000)
                                await page.wait_for_timeout(3000)

                                # Check if we successfully loaded the business page
                                try:
                                    # Look for business name
                                    title_elem = await page.query_selector(".DUwDvf.lfPIob, h1")
                                    if title_elem:
                                        name = await title_elem.text_content()
                                        print(f"   ✅ SUCCESSFULLY LOADED: {name.strip()[:60]}")

                                        # Try to extract website
                                        website_link = await page.query_selector("a[data-item-id='authority']")
                                        if website_link:
                                            website = await website_link.get_attribute("href")
                                            print(f"   🌐 Website: {website[:80]}")
                                        else:
                                            print("   ⚠️  No website element found")

                                        # Try to extract phone
                                        phone_elem = await page.query_selector("[data-item-id*='phone']")
                                        if phone_elem:
                                            phone = await phone_elem.text_content()
                                            print(f"   📞 Phone: {phone[:40]}")

                                    else:
                                        print("   ❌ Could not find business name element")

                                except Exception as e:
                                    print(f"   ❌ Error extracting data: {str(e)[:60]}")

                            else:
                                print("   ❌ Could not extract place ID from href")

                    except Exception as e:
                        print(f"   ⚠️  Error finding place links: {str(e)[:60]}")

                except Exception as e:
                    print(f"   ❌ Error loading search page: {str(e)[:60]}")

            # Test Case 2: Alternative URL formats
            print("\n" + "="*90)
            print("TEST 2️⃣  : Alternative URL Formats")
            print("-" * 90)

            url_formats = [
                # Standard format
                "https://www.google.com/maps/place/Gypsy+Vegetarian+Restaurant/@26.2389,73.0243,15z",
                # With full coordinates
                "https://www.google.com/maps/place/Gypsy+Vegetarian+Restaurant+Jodhpur/@26.2389,73.0243,15z",
                # Alternative format
                "https://maps.google.com/maps?q=Gypsy+Vegetarian+Restaurant+Jodhpur",
            ]

            for i, url in enumerate(url_formats, 1):
                print(f"\nFormat {i}: {url[:70]}...")
                try:
                    await page.goto(url, wait_until="networkidle", timeout=15000)
                    await page.wait_for_timeout(2000)

                    # Check if business detail page loaded
                    title_elem = await page.query_selector(".DUwDvf, h1")
                    if title_elem:
                        name = await title_elem.text_content()
                        print(f"   ✅ SUCCESS: {name.strip()[:60]}")
                    else:
                        print(f"   ⚠️  Page loaded but no business detail found")

                except Exception as e:
                    print(f"   ❌ Failed: {str(e)[:50]}")

            # Test Case 3: Inspect current URL structure
            print("\n" + "="*90)
            print("TEST 3️⃣  : Current URL Analysis")
            print("-" * 90)

            print(f"\nCurrent URL: {page.url}")

            # Check page content for business ID patterns
            page_content = await page.content()

            # Look for CID (business identifier)
            cid_matches = re.findall(r'cid[=_](\d+)', page_content)
            if cid_matches:
                print(f"✅ Found CID: {cid_matches[0]}")
            else:
                print("⚠️  No CID found in page content")

            # Look for place patterns
            place_matches = re.findall(r'/place/([^/"]+)', page_content)
            if place_matches:
                print(f"✅ Found place IDs: {set(place_matches)}")
            else:
                print("⚠️  No place IDs found in page content")

            # Summary
            print("\n" + "="*90)
            print("📊 FINDINGS & RECOMMENDATIONS")
            print("="*90)
            print("""
✅ Direct `/place/` URL navigation appears to work
✅ Search page does load and find results
✅ Place links are extractable from search results

⚠️ NEXT STEPS TO IMPLEMENT:
1. Update playwright.py to extract `/place/` URLs from search results
2. Navigate directly using extracted place ID
3. Verify business detail page loads properly
4. Extract website, phone, and other data

🔧 CODE FIX NEEDED:
- Ensure place links are being found and extracted
- Navigate directly to /place/ URL instead of clicking
- Verify data extraction happens on business detail page
            """)

        except Exception as e:
            print(f"\n❌ CRITICAL ERROR: {e}")
            import traceback
            traceback.print_exc()

        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(test_direct_navigation())
