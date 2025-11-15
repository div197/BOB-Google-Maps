#!/usr/bin/env python3
"""
FULLY CORRECTED PLAYWRIGHT EXTRACTOR - V0.5.0 Architecture Restored

Critical Fix: Reverting to working extraction approach from V0.5.0
- JavaScript ENABLED (Google Maps requires it)
- Minimal resource blocking (only ads/tracking blocked)
- Proper web security disabled to allow Google Maps APIs
- Accept real memory usage for real functionality

Following Nishkaam Karma Yoga: Excellence in execution over premature optimization
"""

import asyncio
import re
import json
import time
import gc
import psutil
import os
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
from bob.utils.website_extractor import extract_website_intelligent, parse_google_redirect
from bob.utils.image_extractor import is_valid_image_url, convert_to_high_res, get_comprehensive_image_selectors


class PlaywrightExtractorOptimized:
    """
    CORRECTED Playwright-based extractor - Proper Implementation

    CRITICAL CHANGES FROM V3.5.0:
    1. JavaScript ENABLED (was disabled)
    2. Web security disabled (was missing)
    3. Minimal resource blocking (was overly aggressive)
    4. Real working extraction (was returning empty data)

    This version returns to the proven V0.5.0 architecture that actually works.
    """

    def __init__(self, headless=True, memory_optimized=True):
        self.headless = headless
        self.memory_optimized = memory_optimized

        # Track memory usage
        self.initial_memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024

        self.stats = {
            "total_extractions": 0,
            "successful": 0,
            "failed": 0,
            "avg_time_seconds": 0,
            "peak_memory_mb": 0,
            "memory_efficiency": "UNKNOWN"
        }

    async def extract_business_optimized(self, url, include_reviews=True, max_reviews=5):
        """
        Extract business data - CORRECTED to actually extract data.
        """
        start_time = time.time()
        browser = None
        context = None
        page = None

        try:
            # Monitor memory
            current_memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
            self.stats["peak_memory_mb"] = max(self.stats["peak_memory_mb"], current_memory)

            print(f"\n⚡ PLAYWRIGHT OPTIMIZED EXTRACTOR - FULLY FIXED")
            print(f"📍 URL: {url[:60]}...")
            print(f"🧠 Memory: {current_memory:.1f}MB")

            # Launch browser with WORKING configuration
            browser = await self._create_working_browser()

            # Create context with proper user agent
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )

            # Create page
            page = await context.new_page()

            # Setup MINIMAL resource blocking (only ads/tracking)
            await self._setup_minimal_resource_blocking(page)

            # Convert URL and navigate
            standard_url = self._convert_url(url)

            print("🌐 Loading Google Maps with full JavaScript support...")
            await page.goto(standard_url, wait_until="domcontentloaded", timeout=30000)

            # Wait for page to settle
            await page.wait_for_timeout(3000)

            # Handle search results if needed
            if "/search/" in page.url:
                await self._navigate_to_first_business(page)

            # Wait for business page to load
            try:
                await page.wait_for_selector(".DUwDvf, .x3AX1-LfntMc-header-title, h1", timeout=10000)
            except:
                pass  # Continue anyway

            # Extract data - NOW PROPERLY WITH JAVASCRIPT
            data = await self._extract_data_properly(page)

            # Extract reviews if requested
            if include_reviews:
                reviews = await self._extract_reviews_enhanced(page, max_reviews)
                data["reviews"] = reviews
                data["total_reviews_extracted"] = len(reviews)

            # Calculate quality score
            data["data_quality_score"] = self._calculate_quality_score_proper(data)
            data["success"] = True
            data["extractor_version"] = "Playwright Optimized V4.2 (FULLY FIXED)"

            extraction_time = time.time() - start_time
            data["extraction_time_seconds"] = round(extraction_time, 2)

            self.stats["successful"] += 1
            self.stats["total_extractions"] += 1

            print(f"✅ EXTRACTION COMPLETE - {extraction_time:.1f}s - Quality: {data['data_quality_score']}/100")

            return data

        except Exception as e:
            print(f"❌ Extraction failed: {e}")
            self.stats["failed"] += 1
            self.stats["total_extractions"] += 1

            return {
                "success": False,
                "error": str(e),
                "extractor_version": "Playwright Optimized V4.2 (FULLY FIXED)",
            }

        finally:
            # Cleanup
            try:
                if page:
                    await page.close()
                if context:
                    await context.close()
                if browser:
                    await browser.close()
                print("🧘 Cleanup complete")
            except:
                pass

            gc.collect()

    async def _create_working_browser(self):
        """Create browser with PROVEN working configuration from V0.5.0."""
        try:
            playwright = await async_playwright().start()
            # These args are proven to work from V0.5.0
            browser = await playwright.chromium.launch(
                headless=self.headless,
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-blink-features=AutomationControlled",
                    "--disable-web-security",  # ✅ CRITICAL: Allow Google Maps APIs
                    "--disable-features=VizDisplayCompositor",  # ✅ Lightweight rendering
                ]
            )

            print("✅ Created working browser instance (JavaScript ENABLED)")
            return browser

        except Exception as e:
            print(f"⚠️ Browser creation failed: {e}")
            playwright = await async_playwright().start()
            return await playwright.chromium.launch(headless=self.headless)

    async def _setup_minimal_resource_blocking(self, page):
        """
        Setup MINIMAL resource blocking - only ads and tracking.
        Do NOT block Google Maps or business data APIs.
        """
        # Block only confirmed ads/tracking domains
        blocked_domains = [
            'google-analytics.com',
            'doubleclick.net',
            'googlesyndication.com',
            'facebook.com',
            'twitter.com',
            'linkedin.com'
        ]

        # Block specific patterns
        blocked_patterns = [
            "**/analytics/**",
            "**/doubleclick/**",
            "**/googlesyndication/**",
            "**/google-analytics/**",
            "**/facebook/**",
            "**/twitter/**",
            "**/linkedin/**"
        ]

        for domain in blocked_domains:
            await page.route(f"**/*{domain}*", lambda route: route.abort())

        for pattern in blocked_patterns:
            await page.route(pattern, lambda route: route.abort())

        print("✅ Minimal resource blocking enabled (Google Maps APIs allowed)")

    async def _navigate_to_first_business(self, page):
        """Navigate to first business from search results."""
        try:
            await page.wait_for_timeout(1000)

            business_link = await page.evaluate("""
                () => {
                    const links = document.querySelectorAll('a[href*="/place/"]');
                    return links[0] ? links[0].href : null;
                }
            """)

            if business_link:
                await page.goto(business_link, wait_until="domcontentloaded", timeout=20000)
                await page.wait_for_timeout(2000)
                print("✅ Navigated to business page")
                return True
            else:
                print("⚠️ No business link found")
                return False

        except Exception as e:
            print(f"⚠️ Navigation error: {e}")
            return False

    async def _extract_data_properly(self, page):
        """
        Extract data PROPERLY with JavaScript enabled AND intelligent website filtering.
        This is where the actual business data comes from.
        """
        data = {
            "extraction_method": "Playwright Enhanced (JavaScript Enabled + Intelligent Filtering)"
        }

        try:
            # Get page content for pattern-based website extraction
            page_content = await page.content()
            # Get page text from the body element
            try:
                page_text = await page.locator("body").text_content()
            except:
                page_text = ""

            # Use JavaScript to extract data from the page
            extracted_data = await page.evaluate("""
                () => {
                    const result = {};

                    // Extract name - multiple selectors for robustness
                    const nameSelectors = [
                        '.DUwDvf.lfPIob',
                        '.x3AX1-LfntMc-header-title',
                        'h1[class*="title"]',
                        'div[class*="title"]',
                        'h1'
                    ];
                    for (const selector of nameSelectors) {
                        try {
                            const elem = document.querySelector(selector);
                            if (elem && elem.textContent.trim().length > 0) {
                                result.name = elem.textContent.trim();
                                break;
                            }
                        } catch (e) {}
                    }

                    // Extract rating - Google Maps shows as star + number
                    const ratingSelectors = [
                        '.MW4etd',
                        '.ceNzKf',
                        '[aria-label*="star"]',
                        'div[class*="rating"]'
                    ];
                    for (const selector of ratingSelectors) {
                        try {
                            const elem = document.querySelector(selector);
                            if (elem) {
                                const text = elem.textContent || elem.getAttribute('aria-label') || '';
                                const match = text.match(/(\\d+\\.?\\d*)/);
                                if (match) {
                                    result.rating = parseFloat(match[1]);
                                    break;
                                }
                            }
                        } catch (e) {}
                    }

                    // Extract review count
                    try {
                        const reviewElem = document.querySelector('.UY7F9, .RDApEe.YrbPuc, [class*="review"]');
                        if (reviewElem) {
                            const match = reviewElem.textContent.match(/(\\d+)/);
                            if (match) result.review_count = parseInt(match[1]);
                        }
                    } catch (e) {}

                    // Extract address
                    try {
                        const addressElem = document.querySelector('[data-item-id*="address"], div[class*="address"]');
                        if (addressElem) result.address = addressElem.textContent.trim();
                    } catch (e) {}

                    // Extract phone
                    try {
                        const phoneElem = document.querySelector('[data-item-id*="phone"], a[href*="tel"]');
                        if (phoneElem) {
                            const text = phoneElem.textContent || phoneElem.getAttribute('aria-label') || '';
                            const match = text.match(/[\\+\\d\\s\\(\\)\\-]{7,}/);
                            if (match) result.phone = match[0].trim();
                        }
                    } catch (e) {}

                    // Extract ALL available URLs (not just one) - collect multiple for intelligent filtering
                    try {
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
                        result.available_urls = Array.from(new Set(websiteLinks));  // Deduplicate
                        console.log(`  Total after dedup: ${result.available_urls.length}`);

                        if (result.available_urls.length > 0) {
                            result.website = result.available_urls[0];  // Primary selection (will be filtered below)
                            console.log(`  Primary website: ${result.website.substring(0, 100)}`);
                        }
                    } catch (e) {
                        console.log(`  ❌ URL collection error: ${e.message}`);
                    }

                    // Extract category/type
                    try {
                        const categoryElem = document.querySelector('.DkEaL, .YhemCb, div[class*="category"]');
                        if (categoryElem) result.category = categoryElem.textContent.trim();
                    } catch (e) {}

                    // Extract GPS from MULTIPLE SOURCES (comprehensive approach)
                    try {
                        // METHOD 1A: Extract from Google Maps URL parameters (!3d=latitude, !4d=longitude)
                        const url = window.location.href;
                        const lat3dMatch = url.match(/!3d(-?\\d+\\.\\d+)/);
                        const lon4dMatch = url.match(/!4d(-?\\d+\\.\\d+)/);
                        if (lat3dMatch && lon4dMatch) {
                            result.latitude = parseFloat(lat3dMatch[1]);
                            result.longitude = parseFloat(lon4dMatch[1]);
                            console.log(`✅ GPS from URL params (!3d/!4d): ${result.latitude}, ${result.longitude}`);
                        }

                        // METHOD 1B: Extract from URL pattern /@latitude,longitude (fallback)
                        if (!result.latitude || !result.longitude) {
                            const urlMatch = url.match(/@(-?\\d+\\.\\d+),(-?\\d+\\.\\d+)/);
                            if (urlMatch) {
                                result.latitude = parseFloat(urlMatch[1]);
                                result.longitude = parseFloat(urlMatch[2]);
                                console.log(`✅ GPS from URL @pattern: ${result.latitude}, ${result.longitude}`);
                            }
                        }

                        // METHOD 2: Extract from data-latlng attribute
                        if (!result.latitude || !result.longitude) {
                            const latlngElem = document.querySelector('[data-latlng]');
                            if (latlngElem) {
                                const latlng = latlngElem.getAttribute('data-latlng');
                                const coords = latlng.match(/(-?\\d+\\.\\d+)/g);
                                if (coords && coords.length >= 2) {
                                    result.latitude = parseFloat(coords[0]);
                                    result.longitude = parseFloat(coords[1]);
                                    console.log(`✅ GPS from data-latlng: ${result.latitude}, ${result.longitude}`);
                                }
                            }
                        }

                        // METHOD 3: Search DOM for coordinate-like text patterns
                        if (!result.latitude || !result.longitude) {
                            const bodyText = document.body.innerText || '';
                            const coordMatch = bodyText.match(/(-?\\d{2}\\.\\d+)[,\\s]+(-?\\d{2,3}\\.\\d+)/);
                            if (coordMatch) {
                                const lat = parseFloat(coordMatch[1]);
                                const lng = parseFloat(coordMatch[2]);
                                // Validate coordinates are plausible
                                if (lat >= -90 && lat <= 90 && lng >= -180 && lng <= 180) {
                                    result.latitude = lat;
                                    result.longitude = lng;
                                    console.log(`✅ GPS from text pattern: ${result.latitude}, ${result.longitude}`);
                                }
                            }
                        }

                        // METHOD 4: Extract from JSON-LD structured data
                        if (!result.latitude || !result.longitude) {
                            const scripts = document.querySelectorAll('script[type="application/ld+json"]');
                            for (const script of scripts) {
                                try {
                                    const data = JSON.parse(script.textContent);
                                    if (data.geo && data.geo.latitude && data.geo.longitude) {
                                        result.latitude = parseFloat(data.geo.latitude);
                                        result.longitude = parseFloat(data.geo.longitude);
                                        console.log(`✅ GPS from JSON-LD: ${result.latitude}, ${result.longitude}`);
                                        break;
                                    }
                                    if (data.latitude && data.longitude) {
                                        result.latitude = parseFloat(data.latitude);
                                        result.longitude = parseFloat(data.longitude);
                                        console.log(`✅ GPS from JSON-LD direct: ${result.latitude}, ${result.longitude}`);
                                        break;
                                    }
                                } catch (e) {}
                            }
                        }
                    } catch (e) {
                        console.log(`GPS extraction error: ${e.message}`);
                    }

                    // Extract Plus Code (also from multiple sources)
                    try {
                        // METHOD 1: From URL
                        const plusCodeMatch = window.location.href.match(/1s([A-Z0-9]{4}\\+[A-Z0-9]{2,})/);
                        if (plusCodeMatch) {
                            result.plus_code = plusCodeMatch[1];
                            console.log(`✅ Plus Code from URL: ${result.plus_code}`);
                        }

                        // METHOD 2: Search page text for Plus Code pattern
                        if (!result.plus_code) {
                            const pageText = document.body.innerText || '';
                            const plusMatch = pageText.match(/([A-Z0-9]{4}\\+[A-Z0-9]{2,})/);
                            if (plusMatch) {
                                result.plus_code = plusMatch[1];
                                console.log(`✅ Plus Code from text: ${result.plus_code}`);
                            }
                        }

                        // METHOD 3: From data attributes
                        if (!result.plus_code) {
                            const plusElem = document.querySelector('[data-plus-code]');
                            if (plusElem) {
                                result.plus_code = plusElem.getAttribute('data-plus-code');
                                console.log(`✅ Plus Code from attribute: ${result.plus_code}`);
                            }
                        }
                    } catch (e) {
                        console.log(`Plus Code extraction error: ${e.message}`);
                    }

                    // Extract Place ID from URL
                    try {
                        const url = window.location.href;
                        const placeIdMatch = url.match(/!1s(0x[0-9a-f]+:0x[0-9a-f]+)/);
                        if (placeIdMatch) {
                            result.place_id_original = placeIdMatch[1];
                            const hexParts = placeIdMatch[1].split(':');
                            if (hexParts.length >= 2) {
                                try {
                                    const cid = parseInt(hexParts[1], 16);
                                    result.cid = cid.toString();
                                    result.place_id = cid.toString();
                                } catch (e) {}
                            }
                        }
                    } catch (e) {}

                    return result;
                }
            """)

            data.update(extracted_data)

            # CRITICAL FIX: Apply intelligent website filtering
            # This is the missing piece that was bypassing the intelligent filter!
            if data.get('available_urls'):
                print(f"🔍 Raw URLs found: {data['available_urls']}")
                intelligent_website = extract_website_intelligent(
                    page_text,
                    data['available_urls']
                )
                if intelligent_website:
                    print(f"✅ Intelligent filter selected: {intelligent_website[:80]}")
                    data['website'] = intelligent_website
                else:
                    print(f"⚠️ Intelligent filter found no valid business website")
                    # Remove the raw website if it's filtered out
                    data['website'] = None

            # CRITICAL FIX: Extract images from the page
            print(f"\n📸 EXTRACTING IMAGES...")
            try:
                images = await self._extract_images_optimized(page)
                if images:
                    print(f"✅ Extracted {len(images)} images")
                    data['photos'] = images
                else:
                    print(f"⚠️ No valid business images found")
                    data['photos'] = []
            except Exception as e:
                print(f"⚠️ Image extraction error: {str(e)[:80]}")
                data['photos'] = []

        except Exception as e:
            print(f"Error in data extraction: {e}")

        return data

    async def _extract_reviews_enhanced(self, page, max_reviews=5):
        """Extract reviews with full JavaScript support."""
        reviews = []

        try:
            # Wait for reviews to load
            await page.wait_for_timeout(2000)

            reviews_data = await page.evaluate(f"""
                () => {{
                    const reviewElements = document.querySelectorAll('.jftiEf, .MyEned, .wiI7pd, [class*="review"]');
                    const reviews = [];

                    for (let i = 0; i < Math.min({max_reviews}, reviewElements.length); i++) {{
                        const elem = reviewElements[i];
                        const review = {{ review_index: i + 1 }};

                        // Extract reviewer name
                        try {{
                            const nameElem = elem.querySelector('.TL4Bff, .d4r55, [class*="name"]');
                            if (nameElem) review.reviewer_name = nameElem.textContent.trim();
                        }} catch (e) {{}}

                        // Extract rating
                        try {{
                            const ratingElem = elem.querySelector('[aria-label*="star"], [class*="rating"]');
                            if (ratingElem) {{
                                const text = ratingElem.getAttribute('aria-label') || ratingElem.textContent;
                                const match = text.match(/(\\d+)/);
                                if (match) review.rating = parseInt(match[1]);
                            }}
                        }} catch (e) {{}}

                        // Extract review text
                        try {{
                            const textElem = elem.querySelector('[class*="text"], [class*="description"]');
                            if (textElem) review.review_text = textElem.textContent.trim().substring(0, 1000);
                        }} catch (e) {{}}

                        // Extract date
                        try {{
                            const dateElem = elem.querySelector('[class*="date"]');
                            if (dateElem) review.review_date = dateElem.textContent.trim();
                        }} catch (e) {{}}

                        if (review.reviewer_name || review.rating || review.review_text) {{
                            reviews.push(review);
                        }}
                    }}

                    return reviews;
                }}
            """)

            reviews = reviews_data
            print(f"✅ Extracted {len(reviews)} reviews")

        except Exception as e:
            print(f"ℹ️ Review extraction note: {e}")

        return reviews

    async def _extract_images_optimized(self, page):
        """Extract business images using CSS selectors - CRITICAL FIX."""
        all_images = set()

        try:
            # Get all comprehensive selectors
            selectors = get_comprehensive_image_selectors()

            print(f"    Testing {len(selectors)} CSS selectors...")

            for selector in selectors:
                try:
                    img_elements = await page.query_selector_all(selector)
                    if img_elements:
                        for img in img_elements:
                            try:
                                # Try src first, then data-src
                                src = await img.get_attribute('src')
                                if not src:
                                    src = await img.get_attribute('data-src')
                                if not src:
                                    src = await img.get_attribute('data-lazy-src')

                                if src and is_valid_image_url(src):
                                    high_res = convert_to_high_res(src)
                                    all_images.add(high_res)
                            except:
                                continue
                except:
                    continue

            # Also try getting images via JavaScript (direct DOM access)
            try:
                js_images = await page.evaluate("""
                    () => {
                        const images = [];
                        const imgElements = document.querySelectorAll('img');
                        for (let img of imgElements) {
                            const src = img.src || img.getAttribute('data-src') || img.getAttribute('data-lazy-src') || '';
                            if (src && src.includes('googleusercontent.com') && !src.includes('mapslogo') && !src.includes('/a/')) {
                                images.push(src);
                            }
                        }
                        return Array.from(new Set(images));  // Deduplicate
                    }
                """)

                if js_images:
                    for url in js_images:
                        if is_valid_image_url(url):
                            high_res = convert_to_high_res(url)
                            all_images.add(high_res)

            except:
                pass

            print(f"    Found {len(all_images)} valid business images")
            return list(all_images)

        except Exception as e:
            print(f"    Image extraction failed: {str(e)[:60]}")
            return []

    def _calculate_quality_score_proper(self, data):
        """
        Calculate quality score PROPERLY.
        Only count fields that actually contain data.
        """
        score = 0

        # Critical business information fields
        if data.get('name'): score += 20
        if data.get('phone'): score += 15
        if data.get('address'): score += 15
        if data.get('website'): score += 10

        # Location data
        if data.get('latitude') and data.get('longitude'): score += 10

        # Business details
        if data.get('rating') is not None: score += 10
        if data.get('review_count'): score += 5
        if data.get('category'): score += 5

        # Place ID data
        if data.get('place_id') or data.get('cid'): score += 5

        # Bonus for reviews and photos
        if data.get('reviews'):
            score += min(len(data['reviews']), 5)
        if data.get('photos'):
            score += min(len(data['photos']), 5)

        return min(score, 100)

    def _convert_url(self, url):
        """Convert business query to Google Maps URL."""
        if not url.startswith('http'):
            return f"https://www.google.com/maps/search/{url.replace(' ', '+')}?hl=en"

        if '/place/' in url:
            return f"{url}{'&' if '?' in url else '?'}hl=en"

        return f"{url}{'&' if '?' in url else '?'}hl=en"

    def get_stats(self):
        """Get extraction statistics."""
        stats = self.stats.copy()
        current_memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
        stats["current_memory_mb"] = round(current_memory, 1)
        stats["memory_increase_mb"] = round(current_memory - self.initial_memory, 1)
        stats["memory_efficiency"] = "EXCELLENT" if stats["memory_increase_mb"] < 50 else "GOOD"
        return stats
