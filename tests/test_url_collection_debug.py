#!/usr/bin/env python3
"""
Deep diagnostic test to capture JavaScript console logs during URL collection.
This will help us understand why available_urls array is empty.
"""

import asyncio
import sys
sys.path.insert(0, '/Users/apple31/16 Nov 2025/BOB-Google-Maps')

from playwright.async_api import async_playwright

async def test_url_collection_with_console_logs():
    """Test URL collection with console log capture."""

    print("\n" + "="*90)
    print("🔍 DEEP DIAGNOSTIC TEST: URL Collection Debug")
    print("="*90)
    print("Testing: Gypsy Vegetarian Restaurant Jodhpur")
    print("="*90 + "\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Capture all console messages
        console_logs = []

        def on_console(msg):
            console_logs.append({
                'type': msg.type,
                'text': msg.text
            })
            print(f"[CONSOLE {msg.type.upper()}] {msg.text}")

        page.on("console", on_console)

        try:
            # Navigate to Google Maps search
            search_url = "https://www.google.com/maps/search/Gypsy+Vegetarian+Restaurant+Jodhpur?hl=en"
            print(f"📍 Navigating to: {search_url}\n")

            await page.goto(search_url, wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)

            # Try to navigate to first business
            print("🔗 Looking for first business link...\n")
            try:
                business_link = await page.query_selector('a[href*="/place/"]')
                if business_link:
                    await business_link.click()
                    await page.wait_for_timeout(3000)
                    print("✅ Navigated to business page\n")
            except Exception as e:
                print(f"⚠️ Navigation failed: {e}\n")

            # Get page text
            page_text = await page.locator("body").text_content()
            print(f"📄 Page text length: {len(page_text)} characters\n")

            # Now execute the JavaScript with console logging
            print("🧪 Executing JavaScript URL collection code...\n")

            result = await page.evaluate("""
                () => {
                    const result = {};
                    const websiteLinks = [];
                    const selectors = [
                        'a[data-item-id="authority"]',
                        'a[href*="http"]',
                        'a[href*="www"]'
                    ];

                    // Debug: Log selector results
                    console.log("🔍 URL Collection Debug:");
                    for (const selector of selectors) {
                        const elems = document.querySelectorAll(selector);
                        console.log(`  Selector '${selector}': found ${elems.length} elements`);
                        for (const elem of elems) {
                            if (elem.href) {
                                console.log(`    - ${elem.href.substring(0, 100)}`);
                                websiteLinks.push(elem.href);
                            }
                        }
                    }

                    console.log(`  Total collected (before dedup): ${websiteLinks.length}`);
                    result.available_urls = Array.from(new Set(websiteLinks));
                    console.log(`  Total after dedup: ${result.available_urls.length}`);

                    if (result.available_urls.length > 0) {
                        result.website = result.available_urls[0];
                        console.log(`  Primary website: ${result.website.substring(0, 100)}`);
                    }

                    return result;
                }
            """)

            print("\n" + "="*90)
            print("JAVASCRIPT EXECUTION RESULT")
            print("="*90)
            print(f"Available URLs collected: {len(result.get('available_urls', []))}")
            if result.get('available_urls'):
                print(f"\nURLs found:")
                for url in result['available_urls']:
                    print(f"  - {url[:80]}")
            else:
                print("\n❌ NO URLs COLLECTED!")

            print("\n" + "="*90)
            print("CONSOLE LOGS CAPTURED")
            print("="*90)
            if console_logs:
                for log in console_logs:
                    print(f"[{log['type'].upper()}] {log['text']}")
            else:
                print("⚠️ NO CONSOLE LOGS CAPTURED")

            # Direct selector tests
            print("\n" + "="*90)
            print("DIRECT SELECTOR TESTS")
            print("="*90)

            authority_links = await page.query_selector_all('a[data-item-id="authority"]')
            print(f"\n✓ 'a[data-item-id=\"authority\"]': found {len(authority_links)} elements")
            for i, link in enumerate(authority_links[:3]):
                href = await link.get_attribute("href")
                text = await link.text_content()
                print(f"  [{i+1}] href: {href[:80]}")
                print(f"      text: {text[:50]}")

            http_links = await page.query_selector_all('a[href*="http"]')
            print(f"\n✓ 'a[href*=\"http\"]': found {len(http_links)} elements")
            for i, link in enumerate(http_links[:5]):
                href = await link.get_attribute("href")
                print(f"  [{i+1}] {href[:80]}")

        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()

        finally:
            await browser.close()

    print("\n" + "="*90)
    print("✅ DIAGNOSTIC TEST COMPLETE")
    print("="*90 + "\n")

if __name__ == "__main__":
    asyncio.run(test_url_collection_with_console_logs())
