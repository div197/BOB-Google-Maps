"""bob_core.business_parser

Extracts core business information (name, rating, category) from a loaded
Google Maps place page.

Selectors verified as of June 2025 (English UI forced with `hl=en`).
"""
from __future__ import annotations

from typing import Dict, Any

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

from .utils import safe_find_element, safe_get_text, safe_get_attribute

__all__ = ["BusinessParser"]


class BusinessParser:  # noqa: D101 – simple data extractor
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def parse(self) -> Dict[str, Any]:  # noqa: D401 – simple method
        """Return a dictionary with extracted business information."""
        info: Dict[str, Any] = {}

        # Name
        name_elem = safe_find_element(
            self.driver, By.CSS_SELECTOR, "h1.DUwDvf.lfPIob", timeout=15
        )
        info["name"] = safe_get_text(name_elem, "Unknown")

        # Rating – stored in aria-label like "4.6 stars"
        rating_elem = safe_find_element(
            self.driver, By.CSS_SELECTOR, "span.ceNzKf", timeout=10
        )
        info["rating"] = safe_get_attribute(rating_elem, "aria-label", "Unrated")

        # Category – appears as a <button>
        category_elem = safe_find_element(
            self.driver, By.CSS_SELECTOR, "button.DkEaL", timeout=10
        )
        info["category"] = safe_get_text(category_elem, "Unknown")

        # Address line
        address_elem = safe_find_element(
            self.driver, By.CSS_SELECTOR, "div.QSFF4-text", timeout=10
        )
        info["address"] = safe_get_text(address_elem, "Unknown")

        # Phone (look for buttons with tel link)
        try:
            phone_elem = self.driver.find_element(By.XPATH, "//a[contains(@href,'tel:')]")
            info["phone"] = phone_elem.get_attribute("href").replace("tel:", "")
        except Exception:
            info["phone"] = "Unavailable"

        # Website (anchor with http)
        try:
            site_elem = self.driver.find_element(By.XPATH, "//a[contains(@href,'http') and contains(@rel,'noopener')]")
            info["website"] = site_elem.get_attribute("href")
        except Exception:
            info["website"] = "Unavailable"

        # TODO: Extract address, phone, website etc.
        return info 