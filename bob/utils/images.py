#!/usr/bin/env python3
"""
Advanced Image Extractor for Google Maps

Extracts all available business images from Google Maps using
multiple strategies including gallery navigation, scroll loading,
and comprehensive DOM scanning.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import re

class AdvancedImageExtractor:
    """
    Advanced image extraction from Google Maps.
    Uses multiple strategies to find all available images.
    """

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def extract_all_images_comprehensive(self):
        """
        Extract all available images using multiple techniques.
        Combines various strategies to maximize image discovery.
        """
        print("📸 Starting comprehensive image extraction...")

        all_image_urls = set()
        extraction_log = []

        # Phase 1: Extract all visible images immediately
        initial_images = self._extract_immediate_images()
        all_image_urls.update(initial_images)
        extraction_log.append(f"Phase 1: {len(initial_images)} immediate images")

        # Phase 2: Try to open main photo gallery
        gallery_opened = self._open_main_photo_gallery()
        if gallery_opened:
            gallery_images = self._extract_gallery_images()
            all_image_urls.update(gallery_images)
            extraction_log.append(f"Phase 2: {len(gallery_images)} gallery images")

        # Phase 3: Try Photos tab/button
        photos_tab_opened = self._open_photos_tab()
        if photos_tab_opened:
            photos_tab_images = self._extract_photos_tab_images()
            all_image_urls.update(photos_tab_images)
            extraction_log.append(f"Phase 3: {len(photos_tab_images)} photos tab images")

        # Phase 4: Scroll and extract more
        scroll_images = self._scroll_and_extract()
        all_image_urls.update(scroll_images)
        extraction_log.append(f"Phase 4: {len(scroll_images)} scroll images")

        # Phase 5: Look for hidden image containers
        hidden_images = self._extract_hidden_images()
        all_image_urls.update(hidden_images)
        extraction_log.append(f"Phase 5: {len(hidden_images)} hidden images")

        # Phase 6: Extract from street view and 360° photos
        special_images = self._extract_special_view_images()
        all_image_urls.update(special_images)
        extraction_log.append(f"Phase 6: {len(special_images)} special view images")

        # Convert all to high resolution and remove duplicates
        high_res_images = list(set([self._convert_to_ultra_high_res(url) for url in all_image_urls]))

        print(f"✅ Extracted {len(high_res_images)} unique images")
        for log in extraction_log:
            print(f"   📊 {log}")

        return {
            "photos": high_res_images,
            "image_count": len(high_res_images),
            "extraction_phases": len(extraction_log),
            "extraction_method": "comprehensive_multi_phase"
        }

    def _extract_immediate_images(self):
        """Extract all immediately visible images."""
        image_urls = set()

        # Comprehensive image selectors
        selectors = [
            "img[src*='googleusercontent.com']",
            "img[src*='gstatic.com']",
            "img[data-src*='googleusercontent.com']",
            "img[data-src*='gstatic.com']",
            ".section-hero-header img",
            ".section-hero-header-image img",
            ".section-hero-header-image-container img",
            ".gallery-image img",
            ".photo-container img",
            ".section-image img",
            "[role='img']",
            "img[src*='maps']",
            "img[src*='streetview']",
            ".streetview img",
            ".panorama img"
        ]

        for selector in selectors:
            try:
                images = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for img in images:
                    src = img.get_attribute('src') or img.get_attribute('data-src')
                    if src and self._is_valid_image_url(src):
                        image_urls.add(src)
            except:
                continue

        return image_urls

    def _open_main_photo_gallery(self):
        """Try to open the main photo gallery."""
        main_photo_selectors = [
            ".section-hero-header-image img",
            ".section-hero-header-image-container img",
            "[data-photo-index='0'] img",
            ".gallery-image-high-res",
            ".section-hero-header img",
            ".hero-image img",
            ".main-photo img"
        ]

        for selector in main_photo_selectors:
            try:
                photo = self.driver.find_element(By.CSS_SELECTOR, selector)
                # Try clicking the photo
                ActionChains(self.driver).click(photo).perform()
                time.sleep(4)

                # Check if gallery opened by looking for gallery indicators
                gallery_indicators = [
                    ".gallery-container",
                    ".photo-gallery",
                    ".image-viewer",
                    "[role='dialog']"
                ]

                for indicator in gallery_indicators:
                    try:
                        if self.driver.find_element(By.CSS_SELECTOR, indicator):
                            print("📸 Main photo gallery opened")
                            return True
                    except:
                        continue

            except:
                continue

        return False

    def _extract_gallery_images(self):
        """Extract images from opened gallery."""
        gallery_urls = set()

        # Wait for gallery to load
        time.sleep(3)

        # Gallery-specific selectors
        gallery_selectors = [
            ".gallery-container img",
            ".photo-gallery img",
            ".image-viewer img",
            ".gallery-image img",
            "[role='dialog'] img",
            ".photo-carousel img",
            ".image-carousel img"
        ]

        for selector in gallery_selectors:
            try:
                images = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for img in images:
                    src = img.get_attribute('src') or img.get_attribute('data-src')
                    if src and self._is_valid_image_url(src):
                        gallery_urls.add(src)
            except:
                continue

        return gallery_urls

    def _open_photos_tab(self):
        """Try to open Photos tab/button."""
        photos_selectors = [
            "button[data-value='Photos']",
            "[data-tab-index='1']",
            "button[aria-label*='photo']",
            "button[aria-label*='Photo']",
            ".section-tab[data-value='photos']",
            "button[jsaction*='photos']",
            "div[data-value='Photos']",
            "span:contains('Photos')",
            "button:contains('Photos')"
        ]

        for selector in photos_selectors:
            try:
                if "contains" not in selector:  # CSS selectors only
                    tab = self.driver.find_element(By.CSS_SELECTOR, selector)
                    ActionChains(self.driver).click(tab).perform()
                    time.sleep(5)
                    print("📸 Photos tab opened")
                    return True
            except:
                continue

        # Try finding by text content
        try:
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            for button in buttons:
                if "photo" in button.text.lower():
                    ActionChains(self.driver).click(button).perform()
                    time.sleep(5)
                    print("📸 Photos button found and clicked")
                    return True
        except:
            pass

        return False

    def _extract_photos_tab_images(self):
        """Extract images from Photos tab."""
        photos_urls = set()

        # Wait for photos to load
        time.sleep(4)

        # Photos tab specific selectors
        photos_selectors = [
            ".section-scrollbox img",
            ".section-layout img",
            ".photos-section img",
            ".photo-grid img",
            ".image-grid img",
            ".scrollable-photos img"
        ]

        for selector in photos_selectors:
            try:
                images = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for img in images:
                    src = img.get_attribute('src') or img.get_attribute('data-src')
                    if src and self._is_valid_image_url(src):
                        photos_urls.add(src)
            except:
                continue

        return photos_urls

    def _scroll_and_extract(self):
        """Scroll to load more images and extract them."""
        scroll_urls = set()

        # Scroll multiple times to load lazy-loaded images
        for i in range(10):
            try:
                # Scroll down
                self.driver.execute_script("window.scrollBy(0, 500);")
                time.sleep(1)

                # Extract new images after scroll
                new_images = self.driver.find_elements(By.CSS_SELECTOR, "img[src*='googleusercontent.com']")
                for img in new_images:
                    src = img.get_attribute('src')
                    if src and self._is_valid_image_url(src):
                        scroll_urls.add(src)

                # Try horizontal scroll if in gallery
                self.driver.execute_script("window.scrollBy(500, 0);")
                time.sleep(1)

            except:
                break

        return scroll_urls

    def _extract_hidden_images(self):
        """Extract images from hidden containers."""
        hidden_urls = set()

        # Look for hidden image containers
        hidden_selectors = [
            "[style*='display: none'] img",
            ".hidden img",
            ".invisible img",
            "[aria-hidden='true'] img",
            ".lazy img",
            ".lazyload img"
        ]

        for selector in hidden_selectors:
            try:
                images = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for img in images:
                    src = img.get_attribute('src') or img.get_attribute('data-src') or img.get_attribute('data-lazy-src')
                    if src and self._is_valid_image_url(src):
                        hidden_urls.add(src)
            except:
                continue

        return hidden_urls

    def _extract_special_view_images(self):
        """Extract street view and 360° images."""
        special_urls = set()

        # Look for street view and 360° images
        special_selectors = [
            "img[src*='streetview']",
            "img[src*='panorama']",
            ".streetview-container img",
            ".panoramic-image img",
            ".street-view img",
            "img[src*='cbk']",  # Street view callback
            "img[src*='photosphere']"
        ]

        for selector in special_selectors:
            try:
                images = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for img in images:
                    src = img.get_attribute('src')
                    if src and self._is_valid_image_url(src):
                        special_urls.add(src)
            except:
                continue

        return special_urls

    def _is_valid_image_url(self, url):
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
        ]

        for pattern in valid_patterns:
            if pattern in url:
                return True

        return False

    def _convert_to_ultra_high_res(self, image_url):
        """Convert image URL to ACTUAL ultra-high resolution using multiple strategies."""
        if not image_url:
            return image_url

        # Strategy 1: Remove ALL size restrictions for maximum resolution
        if 'googleusercontent.com' in image_url:
            # Remove all size parameters completely
            base_url = re.sub(r'=w\d+.*$', '', image_url)
            base_url = re.sub(r'=s\d+.*$', '', base_url)
            base_url = re.sub(r'=h\d+.*$', '', base_url)

            # Try multiple high-resolution patterns
            high_res_variants = [
                base_url,  # No size restriction (best)
                f"{base_url}=w0",  # Width 0 = original
                f"{base_url}=s0",  # Size 0 = original
                f"{base_url}=w4096-h4096",  # Explicit large size
                f"{base_url}=w2048-h2048-no-k",  # Large with no-k flag
                f"{base_url}=d",  # Download flag for full resolution
            ]

            # Return the first variant (no restrictions)
            return high_res_variants[0]

        # Strategy 2: For other image hosts
        if '=w' in image_url and '=h' in image_url:
            url = re.sub(r'=w\d+', '=w4096', image_url)
            url = re.sub(r'=h\d+', '=h4096', url)
            return url
        elif '=w' in image_url:
            return re.sub(r'=w\d+', '=w4096', image_url)
        elif '=s' in image_url:
            return re.sub(r'=s\d+', '=s4096', image_url)
        else:
            return f"{image_url}=w4096" if '?' not in image_url else f"{image_url}&w=4096"