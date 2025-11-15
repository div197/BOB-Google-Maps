#!/usr/bin/env python3
"""
Improved Image Extraction Module - Handles Multiple Extraction Strategies

Key Features:
- Multi-phase image extraction (6 distinct phases)
- Comprehensive CSS selectors for different image types
- High-resolution URL conversion
- Works with both Selenium and Playwright
- Lazy-load image detection and extraction
"""

import re
from typing import Set, List, Dict, Any


def is_valid_image_url(url: str) -> bool:
    """Check if URL is a valid BUSINESS image URL (not maps, logos, avatars)."""
    if not url or not url.startswith('http'):
        return False

    # EXCLUDE junk URLs
    exclude_patterns = [
        '/maps/vt/pb=',  # Map tiles
        '/images/branding/',  # Google Maps logos
        '/a/', '/a-/',  # User avatars
        'mapslogo',  # Map logos
        '_ic_', '.png',  # UI icons
        'h-36-p-rp',  # Small avatar images
        'h=36', 'w=36',  # Small UI elements
    ]

    for pattern in exclude_patterns:
        if pattern in url:
            return False

    # ONLY INCLUDE real business photos
    valid_patterns = [
        'lh3.googleusercontent.com/p/',  # Business place photos
        'streetview',  # Street view photos
        'googleusercontent.com',  # Generic Google hosted images
    ]

    for pattern in valid_patterns:
        if pattern in url:
            return True

    return False


def convert_to_high_res(image_url: str) -> str:
    """Convert image URL to ACTUAL high resolution."""
    if not image_url:
        return image_url

    # Strategy 1: Remove ALL size restrictions for maximum resolution
    if 'googleusercontent.com' in image_url:
        # Remove all size parameters completely
        base_url = re.sub(r'=w\d+.*$', '', image_url)
        base_url = re.sub(r'=s\d+.*$', '', base_url)
        base_url = re.sub(r'=h\d+.*$', '', base_url)

        # Return the base URL without size restrictions (best)
        return base_url

    # Strategy 2: For other image hosts
    if '=w' in image_url and '=h' in image_url:
        url = re.sub(r'=w\d+', '=w2048', image_url)
        url = re.sub(r'=h\d+', '=h2048', url)
        return url
    elif '=w' in image_url:
        return re.sub(r'=w\d+', '=w2048', image_url)
    elif '=s' in image_url:
        return re.sub(r'=s\d+', '=s2048', image_url)
    else:
        return f"{image_url}=w2048" if '?' not in image_url else f"{image_url}&w=2048"


def get_comprehensive_image_selectors() -> List[str]:
    """
    Get comprehensive CSS selectors for image extraction.
    Multiple selectors increase chance of finding images across different Google Maps versions.
    """
    return [
        # Direct image tags with googleusercontent
        "img[src*='googleusercontent.com']",
        "img[data-src*='googleusercontent.com']",
        "img[src*='gstatic.com']",
        "img[data-src*='gstatic.com']",

        # Hero/header images
        ".section-hero-header img",
        ".section-hero-header-image img",
        ".section-hero-header-image-container img",
        ".gallery-image img",
        ".photo-container img",
        ".section-image img",

        # Gallery and carousel
        ".gallery-container img",
        ".photo-gallery img",
        ".image-viewer img",
        ".photo-carousel img",
        ".image-carousel img",

        # Photos tab and scrollable sections
        ".section-scrollbox img",
        ".section-layout img",
        ".photos-section img",
        ".photo-grid img",
        ".image-grid img",
        ".scrollable-photos img",

        # Role-based selectors
        "[role='img']",
        "[role='presentation'] img",

        # Maps and street view
        "img[src*='maps']",
        "img[src*='streetview']",
        ".streetview img",
        ".panorama img",
        ".streetview-container img",
        ".street-view img",
        "img[src*='cbk']",  # Street view callback
        "img[src*='photosphere']",

        # Lazy-loaded images
        "img[data-lazy-src]",
        ".lazy img",
        ".lazyload img",

        # Hidden/offscreen images
        "[style*='display: none'] img",
        ".hidden img",
        ".invisible img",
        "[aria-hidden='true'] img",
    ]


async def extract_images_playwright(page) -> List[str]:
    """
    Extract images using Playwright with comprehensive selectors.

    Args:
        page: Playwright page object

    Returns:
        List of high-resolution image URLs
    """
    all_images = set()

    print("📸 Starting comprehensive image extraction (Playwright)...")

    # Phase 1: Extract immediate images
    print("  Phase 1: Extracting immediate images...")
    selectors = get_comprehensive_image_selectors()

    for selector in selectors:
        try:
            img_elements = await page.query_selector_all(selector)
            for img in img_elements:
                try:
                    src = await img.get_attribute('src') or await img.get_attribute('data-src')
                    if src and is_valid_image_url(src):
                        high_res = convert_to_high_res(src)
                        all_images.add(high_res)
                except:
                    continue
        except:
            continue

    print(f"  Phase 1: Found {len(all_images)} images")

    # Phase 2: Try scrolling to load lazy-loaded images
    print("  Phase 2: Scrolling to load more images...")
    initial_count = len(all_images)

    for _ in range(5):
        try:
            await page.evaluate("window.scrollBy(0, 300)")
            await page.wait_for_load_state('networkidle', timeout=2000)
        except:
            pass

        # Extract again after scroll
        for selector in ["img[src*='googleusercontent']", "img[data-src*='googleusercontent']"]:
            try:
                img_elements = await page.query_selector_all(selector)
                for img in img_elements:
                    try:
                        src = await img.get_attribute('src') or await img.get_attribute('data-src')
                        if src and is_valid_image_url(src):
                            high_res = convert_to_high_res(src)
                            all_images.add(high_res)
                    except:
                        continue
            except:
                continue

    print(f"  Phase 2: Found {len(all_images) - initial_count} additional images (total: {len(all_images)})")

    # Phase 3: Try clicking on main photo if exists
    print("  Phase 3: Attempting to access photo gallery...")
    gallery_count = len(all_images)

    try:
        # Try to find and click main photo
        main_photo_selectors = [
            ".section-hero-header-image img",
            ".section-hero-header img",
            ".hero-image img",
        ]

        for selector in main_photo_selectors:
            try:
                element = await page.query_selector(selector)
                if element:
                    await element.click(timeout=2000)
                    await page.wait_for_load_state('networkidle', timeout=2000)
                    break
            except:
                continue

        # Extract from gallery after click
        gallery_selectors = [".gallery-container img", ".photo-gallery img", "[role='dialog'] img"]
        for selector in gallery_selectors:
            try:
                img_elements = await page.query_selector_all(selector)
                for img in img_elements:
                    try:
                        src = await img.get_attribute('src') or await img.get_attribute('data-src')
                        if src and is_valid_image_url(src):
                            high_res = convert_to_high_res(src)
                            all_images.add(high_res)
                    except:
                        continue
            except:
                continue
    except:
        pass

    print(f"  Phase 3: Found {len(all_images) - gallery_count} gallery images (total: {len(all_images)})")

    print(f"✅ Extracted {len(all_images)} unique images total")
    return list(all_images)


def extract_images_selenium(driver) -> List[str]:
    """
    Extract images using Selenium with comprehensive selectors.
    Falls back to using AdvancedImageExtractor if available.

    Args:
        driver: Selenium WebDriver object

    Returns:
        List of high-resolution image URLs
    """
    # Try to use AdvancedImageExtractor if available for maximum compatibility
    try:
        from bob.utils.images import AdvancedImageExtractor
        extractor = AdvancedImageExtractor(driver)
        result = extractor.extract_all_images_comprehensive()
        return result.get('photos', [])
    except:
        pass

    # Fallback to basic extraction
    all_images = set()

    print("📸 Starting image extraction (Selenium)...")

    selectors = get_comprehensive_image_selectors()

    for selector in selectors:
        try:
            img_elements = driver.find_elements("css selector", selector)
            for img in img_elements:
                try:
                    src = img.get_attribute('src') or img.get_attribute('data-src')
                    if src and is_valid_image_url(src):
                        high_res = convert_to_high_res(src)
                        all_images.add(high_res)
                except:
                    continue
        except:
            continue

    print(f"✅ Extracted {len(all_images)} unique images")
    return list(all_images)
