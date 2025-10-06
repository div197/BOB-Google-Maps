#!/usr/bin/env python3
"""
Advanced Place ID Extractor for Google Maps
September 2025 - Enterprise-grade Place ID extraction

Place IDs are unique identifiers for each Google Maps business listing.
Format: ChIJ[base64url characters] (27 characters total)
Example: ChIJN1t_tDeuEmsRUsoyG83frY4
"""

import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PlaceIDExtractor:
    """
    Advanced Place ID extraction using multiple strategies.
    Place ID is the PRIMARY KEY for Google Maps businesses.
    """

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def extract_place_id_comprehensive(self):
        """
        Extract Place ID using ALL available methods.
        Returns the most reliable Place ID found.
        """
        print("🔍 Extracting Place ID (unique business identifier)...")

        place_id_candidates = []
        extraction_methods = []

        # Method 1: Extract from current URL
        place_id_url = self._extract_from_url()
        if place_id_url:
            place_id_candidates.append(place_id_url)
            extraction_methods.append("URL extraction")

        # Method 2: Extract from page data attributes
        place_id_attrs = self._extract_from_data_attributes()
        if place_id_attrs:
            place_id_candidates.append(place_id_attrs)
            extraction_methods.append("Data attributes")

        # Method 3: Extract from JavaScript objects
        place_id_js = self._extract_from_javascript()
        if place_id_js:
            place_id_candidates.append(place_id_js)
            extraction_methods.append("JavaScript objects")

        # Method 4: Extract from share functionality
        place_id_share = self._extract_from_share_url()
        if place_id_share:
            place_id_candidates.append(place_id_share)
            extraction_methods.append("Share URL")

        # Method 5: Extract from page source regex
        place_id_source = self._extract_from_page_source()
        if place_id_source:
            place_id_candidates.append(place_id_source)
            extraction_methods.append("Page source")

        # Method 6: Extract from data parameter
        place_id_data = self._extract_from_data_param()
        if place_id_data:
            place_id_candidates.append(place_id_data)
            extraction_methods.append("Data parameter")

        # Validate and select best Place ID
        valid_place_id = self._validate_and_select_place_id(place_id_candidates)

        if valid_place_id:
            print(f"✅ Place ID extracted: {valid_place_id}")
            print(f"   Methods successful: {', '.join(extraction_methods)}")
            return {
                "place_id": valid_place_id,
                "extraction_methods": extraction_methods,
                "candidates_found": len(place_id_candidates),
                "confidence": "HIGH" if len(place_id_candidates) > 1 else "MEDIUM"
            }
        else:
            print("⚠️ Place ID not found - using fallback")
            return {
                "place_id": None,
                "extraction_methods": [],
                "candidates_found": 0,
                "confidence": "NONE"
            }

    def _extract_from_url(self):
        """Extract Place ID from current URL."""
        try:
            current_url = self.driver.current_url

            # Standard Place ID patterns in URL (multiple formats per Google docs)
            # ChIJ format (most common)
            place_id_match = re.search(r'ChIJ[A-Za-z0-9_-]+', current_url)
            if place_id_match:
                return place_id_match.group(0)

            # GhIJ format
            place_id_match = re.search(r'GhIJ[A-Za-z0-9_-]+', current_url)
            if place_id_match:
                return place_id_match.group(0)

            # Alternative patterns
            patterns = [
                r'ftid=0x[a-f0-9]+:[a-f0-9x]+',  # Hex format
                r'place_id=([A-Za-z0-9_-]+)',     # Direct parameter
                r'cid=(\d+)',                      # CID format
            ]

            for pattern in patterns:
                match = re.search(pattern, current_url)
                if match:
                    return match.group(1)

        except Exception as e:
            print(f"   URL extraction error: {str(e)[:30]}")

        return None

    def _extract_from_data_attributes(self):
        """Extract Place ID from HTML data attributes."""
        try:
            # Common data attributes that contain Place ID
            selectors = [
                "[data-pid]",
                "[data-place-id]",
                "[data-fid]",
                "[data-feature-id]",
                "[data-location-id]",
                "[jsdata*='ChIJ']"
            ]

            for selector in selectors:
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)

                    # Try different attribute names
                    for attr in ["data-pid", "data-place-id", "data-fid", "jsdata"]:
                        value = element.get_attribute(attr)
                        if value:
                            # Extract ChIJ pattern
                            match = re.search(r'ChIJ[A-Za-z0-9_-]{23}', value)
                            if match:
                                return match.group(0)
                except:
                    continue

        except Exception as e:
            print(f"   Data attribute extraction error: {str(e)[:30]}")

        return None

    def _extract_from_javascript(self):
        """Extract Place ID from JavaScript execution."""
        try:
            # Try to access Google Maps JavaScript objects
            js_commands = [
                # Try to get from window object
                "return window.APP_INITIALIZATION_STATE?.[3]?.[6] || null;",
                "return window.APP_OPTIONS?.[6]?.[6]?.[0] || null;",
                # Try from data layer
                "return document.querySelector('[data-pid]')?.getAttribute('data-pid') || null;",
                # Try from Google's internal objects
                "try { return google.maps.places?.PlaceResult?.place_id || null; } catch(e) { return null; }",
            ]

            for js_cmd in js_commands:
                try:
                    result = self.driver.execute_script(js_cmd)
                    if result:
                        # Check if it's a valid Place ID
                        if isinstance(result, str):
                            match = re.search(r'ChIJ[A-Za-z0-9_-]{23}', result)
                            if match:
                                return match.group(0)
                            elif len(result) == 27:  # Direct Place ID
                                return result
                except:
                    continue

        except Exception as e:
            print(f"   JavaScript extraction error: {str(e)[:30]}")

        return None

    def _extract_from_share_url(self):
        """Extract Place ID from share functionality."""
        try:
            # Try to click share button
            share_selectors = [
                "button[aria-label*='Share']",
                "button[aria-label*='share']",
                "[data-value='Share']",
                "button[jsaction*='share']"
            ]

            for selector in share_selectors:
                try:
                    share_btn = self.driver.find_element(By.CSS_SELECTOR, selector)
                    share_btn.click()
                    time.sleep(1.5)

                    # Get share URL
                    url_input = self.driver.find_element(By.CSS_SELECTOR, "input[readonly]")
                    share_url = url_input.get_attribute("value")

                    # Close dialog
                    try:
                        close_btn = self.driver.find_element(By.CSS_SELECTOR, "[aria-label*='Close']")
                        close_btn.click()
                    except:
                        # Press ESC to close
                        self.driver.find_element(By.TAG_NAME, "body").send_keys(u'\ue00c')

                    if share_url:
                        # Extract Place ID from share URL
                        match = re.search(r'ChIJ[A-Za-z0-9_-]{23}', share_url)
                        if match:
                            return match.group(0)

                        # Try other patterns
                        if "place/" in share_url:
                            # Extract from place URL
                            match = re.search(r'place/([^/]+)/', share_url)
                            if match:
                                place_name = match.group(1)
                                # Sometimes the Place ID is encoded in the URL
                                return None  # Can't extract directly

                    break

                except:
                    continue

        except Exception as e:
            print(f"   Share URL extraction error: {str(e)[:30]}")

        return None

    def _extract_from_page_source(self):
        """Extract Place ID from page source using regex."""
        try:
            page_source = self.driver.page_source

            # Multiple Place ID patterns
            patterns = [
                r'ChIJ[A-Za-z0-9_-]{23}',                    # Standard format
                r'"place_id":"([^"]+)"',                     # JSON format
                r'data-pid="([^"]+)"',                       # Data attribute
                r'&amp;ftid=([^&]+)',                        # FTID format
                r'ludocid%3D(\d+)',                          # LUDOCID format
                r'"feature_id":"([^"]+)"',                   # Feature ID
                r'0x[a-f0-9]+:0x[a-f0-9]+',                 # Hex format
            ]

            place_ids_found = []

            for pattern in patterns:
                matches = re.findall(pattern, page_source)
                for match in matches:
                    if match and len(match) > 10:
                        # Validate if it looks like a Place ID
                        if match.startswith('ChIJ') and len(match) == 27:
                            place_ids_found.append(match)
                        elif 'ChIJ' not in match and len(match) > 20:
                            # Might be a different format
                            place_ids_found.append(match)

            # Return most common Place ID (if multiple found)
            if place_ids_found:
                # Count occurrences
                from collections import Counter
                place_id_counts = Counter(place_ids_found)
                most_common = place_id_counts.most_common(1)[0][0]
                return most_common

        except Exception as e:
            print(f"   Page source extraction error: {str(e)[:30]}")

        return None

    def _extract_from_data_param(self):
        """Extract Place ID from URL data parameter."""
        try:
            current_url = self.driver.current_url

            if 'data=' in current_url:
                data_param = current_url.split('data=')[1].split('&')[0]

                # Method 1: Look for ChIJ pattern
                match = re.search(r'ChIJ[A-Za-z0-9_-]{23}', data_param)
                if match:
                    return match.group(0)

                # Method 2: Parse data parameter structure
                if '!' in data_param:
                    parts = data_param.split('!')
                    for i, part in enumerate(parts):
                        # 1s prefix often contains Place ID
                        if part.startswith('1s') and len(part) > 10:
                            potential_id = part[2:]
                            # Validate format
                            if re.match(r'^[A-Za-z0-9_-]+$', potential_id):
                                return potential_id

                        # 3s prefix sometimes has Place ID
                        if part.startswith('3s') and len(part) > 10:
                            potential_id = part[2:]
                            if re.match(r'^[A-Za-z0-9_-]+$', potential_id):
                                return potential_id

        except Exception as e:
            print(f"   Data parameter extraction error: {str(e)[:30]}")

        return None

    def _validate_and_select_place_id(self, candidates):
        """
        Validate and select the best Place ID from candidates.

        Google Place IDs have specific format:
        - Start with ChIJ (most common)
        - 27 characters total length
        - Use base64url alphabet
        """
        if not candidates:
            return None

        # Priority 1: Standard ChIJ format
        for candidate in candidates:
            if candidate and candidate.startswith('ChIJ') and len(candidate) == 27:
                # Validate characters (base64url)
                if re.match(r'^ChIJ[A-Za-z0-9_-]{23}$', candidate):
                    return candidate

        # Priority 2: Other valid formats (hex, numeric)
        for candidate in candidates:
            if candidate and len(candidate) > 20:
                # Could be alternative format
                if re.match(r'^[A-Za-z0-9_-]+$', candidate):
                    return candidate

        # Priority 3: Return first non-null candidate
        for candidate in candidates:
            if candidate:
                return candidate

        return None