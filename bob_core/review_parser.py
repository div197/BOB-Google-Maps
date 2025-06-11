"""bob_core.review_parser

Extracts review data from a Google Maps place page.

Process:
1. Click the *Reviews* tab/button (several selector fallbacks).
2. Scroll the review container until no new content for *n* iterations.
3. Parse individual review blocks into dicts.
"""
from __future__ import annotations

import time
from typing import List, Dict, Any

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from .utils import safe_find_element, safe_get_text, safe_get_attribute

__all__ = ["ReviewParser", "ReviewParseResult"]


class ReviewParseResult(Dict[str, Any]):
    """Alias for readability – extends dict."""


class ReviewParser:  # noqa: D101
    def __init__(self, driver: WebDriver, *, max_scrolls: int = 30):
        self.driver = driver
        self.max_scrolls = max_scrolls

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------
    def parse_reviews(self) -> List[ReviewParseResult]:  # noqa: D401
        """Return a list of extracted review dictionaries."""
        if not self._open_reviews_tab():
            return []

        self._scroll_reviews()
        return self._collect_reviews()

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------
    def _open_reviews_tab(self) -> bool:
        """Attempt to click the Reviews tab. Return *True* on success."""
        selectors = [
            "//div[@class='LRkQ2']//div[text()='Reviews']",
            "//button[contains(text(), 'Reviews')]",
            "//div[contains(text(), 'Reviews')]",
            "//span[contains(text(), 'Reviews')]",
        ]
        for sel in selectors:
            els = self.driver.find_elements(By.XPATH, sel)
            if els:
                self.driver.execute_script("arguments[0].click();", els[0])
                time.sleep(2)
                return True
        return False

    def _scroll_reviews(self) -> None:
        container = safe_find_element(
            self.driver,
            By.CSS_SELECTOR,
            "div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde",
            timeout=10,
            required=False,
        )
        if container is None:
            return

        last_height = 0
        same_count = 0
        no_change_max = 3
        for _ in range(self.max_scrolls):
            current_height = self.driver.execute_script(
                "return arguments[0].scrollHeight", container
            )
            if current_height == last_height:
                same_count += 1
                if same_count >= no_change_max:
                    break
            else:
                same_count = 0
            self.driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight", container
            )
            last_height = current_height
            time.sleep(1)

    def _collect_reviews(self) -> List[ReviewParseResult]:
        review_blocks = self.driver.find_elements(By.CSS_SELECTOR, "div.jftiEf.fontBodyMedium")
        reviews: List[ReviewParseResult] = []
        for block in review_blocks:
            try:
                username = safe_get_attribute(block, "aria-label", "Anonymous")
                content_span = block.find_element(By.CSS_SELECTOR, "span.wiI7pd")
                content = safe_get_text(content_span)
                rating_span = block.find_element(By.CSS_SELECTOR, "span.kvMYJc")
                rating = safe_get_attribute(rating_span, "aria-label", "Unrated")
                time_span = block.find_element(By.CSS_SELECTOR, "span.rsqaWe")
                ts = safe_get_text(time_span)

                reviews.append(
                    {
                        "username": username,
                        "content": content,
                        "rating": rating,
                        "time": ts,
                    }
                )
            except (NoSuchElementException, TimeoutException):
                continue
        return reviews 