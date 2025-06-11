"""bob_core.scraper

High-level Scraper interface (pre-alpha).

Planned features:
- Single-business scrape (profile + reviews)
- Batch processing wrapper
- Pluggable browser backend (Selenium, Playwright)

All logic will be implemented incrementally in upcoming milestones.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Any
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

from .error_codes import ErrorCodes
from .business_parser import BusinessParser
from .review_parser import ReviewParser
from .playwright_backend import PlaywrightScraper, PLAYWRIGHT_AVAILABLE

__all__ = ["GoogleMapsScraper"]

class GoogleMapsScraper:
    """Multi-backend Google Maps scraper (Selenium + Playwright)."""

    def __init__(self, headless: bool = True, timeout: int = 30, backend: str = "auto"):
        """Initialize scraper with backend selection.
        
        Parameters
        ----------
        headless : bool
            Run browser in headless mode.
        timeout : int
            Timeout in seconds.
        backend : str
            Backend choice: "selenium", "playwright", or "auto" (prefer Playwright).
        """
        self.headless = headless
        self.timeout = timeout
        self.backend = self._select_backend(backend)
    
    def _select_backend(self, backend: str) -> str:
        """Select the best available backend."""
        if backend == "playwright":
            if not PLAYWRIGHT_AVAILABLE:
                raise ImportError("Playwright not available. Install with: pip install playwright")
            return "playwright"
        elif backend == "selenium":
            return "selenium"
        elif backend == "auto":
            return "playwright" if PLAYWRIGHT_AVAILABLE else "selenium"
        else:
            raise ValueError(f"Unknown backend: {backend}")

    def scrape(self, url: str) -> Dict[str, Any]:
        """Scrape a single Google Maps place page using selected backend."""
        if self.backend == "playwright":
            scraper = PlaywrightScraper(headless=self.headless, timeout=self.timeout)
            return scraper.scrape(url)
        else:
            return self._scrape_selenium(url)
    
    def _scrape_selenium(self, url: str) -> Dict[str, Any]:
        """Fallback Selenium implementation."""
        result: Dict[str, Any] = {
            "url": url,
            "success": False,
            "error_code": ErrorCodes.SUCCESS,
            "error_message": "",
            "business_info": {},
        }

        options = Options()
        if self.headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1200")

        driver = None
        try:
            driver = webdriver.Chrome(options=options)
            driver.set_page_load_timeout(self.timeout)
            driver.get(url)

            # Extract business info and reviews
            business_info = BusinessParser(driver).parse()
            reviews = ReviewParser(driver).parse_reviews()

            result["business_info"] = business_info
            result["reviews"] = reviews
            result["reviews_count"] = len(reviews)
            result["success"] = True
            return result
        except WebDriverException as exc:
            result["error_code"] = ErrorCodes.BROWSER_INIT_FAILED
            result["error_message"] = str(exc)
            return result
        except Exception as exc:
            result["error_code"] = ErrorCodes.UNEXPECTED_ERROR
            result["error_message"] = str(exc)
            return result
        finally:
            if driver:
                try:
                    driver.quit()
                except Exception:
                    pass

    def scrape_batch(self, urls: List[str]) -> List[Dict[str, Any]]:
        """Bulk-scrape convenience wrapper (placeholder)."""
        return [self.scrape(u) for u in urls] 