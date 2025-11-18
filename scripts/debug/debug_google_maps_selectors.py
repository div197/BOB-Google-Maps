#!/usr/bin/env python3
"""
🔍 DEEP PENETRATION TESTING: Google Maps DOM Inspector
Finds the ACTUAL CSS selectors Google Maps is currently using for business results
"""

import asyncio
import re
import json
from pathlib import Path
from playwright.async_api import async_playwright


async def debug_google_maps_selectors():
    """Inspect Google Maps DOM to find current working selectors"""

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Show browser for visual inspection
        page = await browser.new_page(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )

        try:
            print("\n" + "="*90)
            print("🔍 GOOGLE MAPS DOM INSPECTOR - Finding Current Working Selectors")
            print("="*90)

            # Test business
            test_business = "Gypsy Vegetarian Restaurant Jodhpur"
            search_url = f"https://www.google.com/maps/search/{test_business.replace(' ', '+')}"

            print(f"\n🌐 Opening: {search_url}")
            await page.goto(search_url, wait_until="networkidle", timeout=30000)
            await page.wait_for_timeout(3000)

            print("✅ Page loaded. Inspecting DOM structure...")
            await page.wait_for_timeout(2000)

            # Get the full HTML of search results area
            print("\n📋 Extracting DOM information...")

            # 1. Find all divs/sections/articles that might contain business results
            all_elements = await page.query_selector_all("div, section, article")
            print(f"   Total elements on page: {len(all_elements)}")

            # 2. Try different class/selector combinations
            selectors_to_test = [
                # Current attempt selectors
                ".m6QErb",
                ".bHzsHc",
                ".lI9IFe",
                ".hfpxzc",
                ".Io6Yb.fontHeadlineSmall",

                # Likely candidates for result containers
                "[data-result-index]",
                "[role='button']",
                ".Nv2PK",
                ".TmJjof",
                ".jAkbff",
                ".JAVqpe",
                ".yjjb3c",
                ".TbKl4d",
                ".VfPpkd-K6x18-Bz112c",

                # Links in results
                "a[href*='/maps/place/']",
                "a[href*='/place/']",
                ".vwVdIc",
                ".SHxrf",
                ".soLcae",

                # Data-driven selectors
                "[data-href*='/place/']",
                "[aria-label*='Directions']",

                # Result list containers
                ".m6QErb.DxyBCb",
                "[role='listbox']",
                "[role='presentation']",
                ".ypCqFe",
                ".RQ7Gcf",
            ]

            print("\n🎯 Testing Selectors:")
            print("-" * 90)

            found_working_selectors = {}

            for selector in selectors_to_test:
                try:
                    elements = await page.query_selector_all(selector)
                    if elements:
                        found_working_selectors[selector] = len(elements)
                        print(f"✅ {selector:45} -> {len(elements):3} elements found")

                        # Get sample attributes from first element
                        if len(elements) > 0:
                            first_elem = elements[0]
                            classes = await first_elem.get_attribute("class")
                            aria_label = await first_elem.get_attribute("aria-label")
                            data_attrs = await first_elem.get_attribute("data-index")

                            if classes:
                                print(f"   └─ Classes: {classes[:80]}")
                            if aria_label:
                                print(f"   └─ aria-label: {aria_label[:80]}")
                            if data_attrs:
                                print(f"   └─ data-index: {data_attrs}")
                except:
                    pass

            # 3. Inspect the actual result items more deeply
            print("\n🔬 Detailed Result Item Analysis:")
            print("-" * 90)

            # Get all potential result containers
            result_containers = await page.query_selector_all(
                "[data-result-index], .Nv2PK, .TmJjof, .jAkbff, [role='button']"
            )

            if result_containers:
                first_result = result_containers[0]
                html = await first_result.inner_html()

                print(f"\nFirst result element HTML (first 500 chars):")
                print("-" * 90)
                print(html[:500])

                # Extract all classes from this element and its children
                classes_on_page = set()
                child_elements = await page.query_selector_all("[class]")
                for elem in child_elements[:100]:  # Sample first 100
                    cls = await elem.get_attribute("class")
                    if cls:
                        # Add individual classes
                        for c in cls.split():
                            if c and not c.startswith('_'):  # Skip private classes
                                classes_on_page.add(c)

                print(f"\n📚 Interesting CSS Classes Found:")
                print("-" * 90)
                interesting_classes = sorted([c for c in classes_on_page if len(c) < 20])
                for cls in interesting_classes[:30]:
                    print(f"   .{cls}")

            # 4. Try to find links that lead to business detail pages
            print("\n🔗 Business Links Analysis:")
            print("-" * 90)

            business_links = await page.query_selector_all("a[href*='/maps/place/'], a[href*='/place/']")
            print(f"Found {len(business_links)} links with '/place/' in href")

            if business_links:
                for i, link in enumerate(business_links[:3]):
                    href = await link.get_attribute("href")
                    text = await link.text_content()
                    aria = await link.get_attribute("aria-label")
                    print(f"\n   Link {i+1}:")
                    print(f"   href: {href[:100]}")
                    print(f"   text: {text[:80]}")
                    if aria:
                        print(f"   aria-label: {aria[:80]}")

            # 5. Capture network and storage info
            print("\n💾 Page Information:")
            print("-" * 90)

            # Get page title
            title = await page.title()
            print(f"   Title: {title}")

            # Get URL
            url = page.url
            print(f"   URL: {url}")

            # Check for API responses
            print("\n📡 Attempting to intercept API responses...")

            # 6. Look for CID patterns in the page
            page_content = await page.content()
            cid_pattern = re.findall(r'(!1s0x[0-9a-f]+:0x[0-9a-f]+|cid[=_]*(\d+))', page_content)
            if cid_pattern:
                print(f"   Found potential CID patterns: {cid_pattern[:3]}")

            # Save detailed report
            report = {
                "timestamp": str(asyncio.get_event_loop().time()),
                "business_searched": test_business,
                "working_selectors": found_working_selectors,
                "selectors_tested": selectors_to_test,
                "notes": [
                    "Look for selectors with > 0 elements",
                    "Priority: Find clickable result items that lead to /place/ URLs",
                    "Check parent containers for navigation structure"
                ]
            }

            print("\n" + "="*90)
            print("📊 SUMMARY - Working Selectors Found:")
            print("="*90)

            if found_working_selectors:
                for selector, count in sorted(found_working_selectors.items(),
                                             key=lambda x: -x[1])[:10]:
                    print(f"✅ {selector:45} -> {count} elements")
            else:
                print("⚠️  No selectors returned elements. Google Maps structure may have changed significantly.")

            # Save report
            report_file = Path("/Users/apple31/16 Nov 2025/BOB-Google-Maps/DOM_INSPECTION_REPORT.json")
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)

            print(f"\n📁 Report saved to: {report_file}")
            print("\n🔍 Keep this browser open to manually inspect in DevTools if needed.")
            print("   Press Ctrl+C to close when done inspecting.")

            # Keep browser open for manual inspection
            await page.wait_for_timeout(30000)  # 30 seconds for manual inspection

        except Exception as e:
            print(f"\n❌ Error during inspection: {e}")
            import traceback
            traceback.print_exc()

        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(debug_google_maps_selectors())
