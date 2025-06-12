"""bob_core.business_parser

Extracts core business information (name, rating, category) from a loaded
Google Maps place page.

Selectors verified as of December 2024 (English UI forced with `hl=en`).
"""
from __future__ import annotations

from typing import Dict, Any, Optional, List

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

from .utils import safe_find_element, safe_get_text, safe_get_attribute

__all__ = ["BusinessParser"]


class BusinessParser:  # noqa: D101 – simple data extractor
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def _extract_with_fallback_selectors(self, selectors: List[str], attribute: str = "text") -> Optional[str]:
        """Extract content using fallback selectors for resilience."""
        for selector in selectors:
            try:
                elem = safe_find_element(self.driver, By.CSS_SELECTOR, selector, timeout=5)
                if elem:
                    if attribute == "text":
                        text = safe_get_text(elem)
                        if text and text.strip():
                            return text.strip()
                    else:
                        attr_value = safe_get_attribute(elem, attribute)
                        if attr_value and attr_value.strip():
                            return attr_value.strip()
            except Exception:
                continue
        return None

    def parse(self) -> Dict[str, Any]:  # noqa: D401 – simple method
        """Return a dictionary with extracted business information."""
        info: Dict[str, Any] = {}

        # Enhanced name extraction with multiple selectors
        name_selectors = [
            "h1.DUwDvf.lfPIob",  # Primary selector
            "h1[data-attrid='title']",  # Alternative
            "h1.x3AX1-LfntMc-header-title-title",  # New UI
            "[data-value='title'] h1",  # Fallback
            "h1.qrShPb",  # Updated selector
            ".x3AX1-LfntMc-header-title-title",  # Without h1
            ".DUwDvf.lfPIob",  # Without h1
            "h1",  # Generic h1 as last resort
        ]
        name = self._extract_with_fallback_selectors(name_selectors, "text")
        info["name"] = name or "Unknown"

        # Enhanced rating extraction
        rating_selectors = [
            "span.ceNzKf",  # Primary
            "[data-value='rating'] span",  # Alternative
            ".gm2-display-2",  # New UI
            "span[aria-label*='stars']",  # Aria-label based
            ".F7nice span",  # Updated selector
            "div.F7nice span",  # With div parent
            "span.kvMYJc",  # Review rating selector
        ]
        rating = self._extract_with_fallback_selectors(rating_selectors, "aria-label")
        info["rating"] = rating or "Unrated"

        # Enhanced category extraction
        category_selectors = [
            "button.DkEaL",  # Primary
            "[data-value='category'] button",  # Alternative
            ".YhemCb",  # New UI
            "button[jsaction*='category']",  # Action-based
            ".DkEaL",  # Without button
            "button.DkEaL span",  # With span child
            ".section-hero-header-title-description",  # Description area
        ]
        category = self._extract_with_fallback_selectors(category_selectors, "text")
        info["category"] = category or "Unknown"

        # Enhanced address extraction
        address_selectors = [
            "div.QSFF4-text",  # Primary
            "[data-value='address'] div",  # Alternative
            ".CsEnBe",  # New UI
            "button[data-item-id='address']",  # Button format
            ".rogA2c .Io6YTe",  # Updated path
            "[data-item-id='address'] .fontBodyMedium",  # With font class
            ".section-info-line",  # Info line
        ]
        address = self._extract_with_fallback_selectors(address_selectors, "text")
        info["address"] = address or "Unknown"

        # Enhanced phone extraction
        try:
            phone_selectors = [
                "a[href^='tel:']",  # Primary
                "button[data-item-id='phone']",  # Button format
                "[data-value='phone'] a",  # Alternative
                "a[aria-label*='phone']",  # Aria-label based
            ]
            phone_elem = None
            for selector in phone_selectors:
                phone_elem = safe_find_element(self.driver, By.CSS_SELECTOR, selector, timeout=3)
                if phone_elem:
                    break
            
            if phone_elem:
                href = safe_get_attribute(phone_elem, "href")
                if href and href.startswith("tel:"):
                    info["phone"] = href.replace("tel:", "")
                else:
                    # Try to get text content
                    phone_text = safe_get_text(phone_elem)
                    info["phone"] = phone_text or "Unavailable"
            else:
                info["phone"] = "Unavailable"
        except Exception:
            info["phone"] = "Unavailable"

        # Enhanced website extraction
        try:
            website_selectors = [
                "a[href^='http'][rel*='noopener']",  # Primary
                "button[data-item-id='authority']",  # Button format
                "[data-value='website'] a",  # Alternative
                "a[aria-label*='website']",  # Aria-label based
                "a[href^='https://']",  # HTTPS links
            ]
            website_elem = None
            for selector in website_selectors:
                website_elem = safe_find_element(self.driver, By.CSS_SELECTOR, selector, timeout=3)
                if website_elem:
                    break
            
            if website_elem:
                href = safe_get_attribute(website_elem, "href")
                if href and (href.startswith("http://") or href.startswith("https://")):
                    info["website"] = href
                else:
                    info["website"] = "Unavailable"
            else:
                info["website"] = "Unavailable"
        except Exception:
            info["website"] = "Unavailable"

        return info 