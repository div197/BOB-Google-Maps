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

from .error_codes import ErrorCodes, handle_error
from .business_parser import BusinessParser
from .review_parser import ReviewParser
from .playwright_backend import PlaywrightScraper, PLAYWRIGHT_AVAILABLE
from .circuit_breaker import get_circuit_breaker
from .retry_strategy import retry_with_backoff, web_scraping_retry

__all__ = ["GoogleMapsScraper"]

class GoogleMapsScraper:
    """Multi-backend Google Maps scraper (Selenium + Playwright)."""

    def __init__(self, headless: bool = True, timeout: int = 30, backend: str = "auto", 
                 extract_reviews: bool = True, max_reviews: int = None):
        """Initialize scraper with backend selection and extraction options.
        
        Parameters
        ----------
        headless : bool
            Run browser in headless mode.
        timeout : int
            Timeout in seconds.
        backend : str
            Backend choice: "selenium", "playwright", or "auto" (prefer Playwright).
        extract_reviews : bool
            Whether to extract reviews (False for business-only mode).
        max_reviews : int, optional
            Maximum number of reviews to extract (None for unlimited).
        """
        self.headless = headless
        self.timeout = timeout
        self.backend = self._select_backend(backend)
        self.extract_reviews = extract_reviews
        self.max_reviews = max_reviews
        
        # Initialize circuit breakers for different operations
        self.browser_circuit_breaker = get_circuit_breaker(
            f"browser_{backend}", 
            failure_threshold=3,
            recovery_timeout=60
        )
        self.parsing_circuit_breaker = get_circuit_breaker(
            "parsing",
            failure_threshold=5,
            recovery_timeout=30
        )
    
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
            return scraper.scrape(url, extract_reviews=self.extract_reviews, max_reviews=self.max_reviews)
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

            # Extract business info
            business_info = BusinessParser(driver).parse()
            result["business_info"] = business_info
            
            # Extract reviews only if requested
            if self.extract_reviews:
                review_parser = ReviewParser(driver)
                if self.max_reviews:
                    # Calculate max_scrolls based on max_reviews (roughly 10 reviews per scroll)
                    max_scrolls = min(30, max(1, self.max_reviews // 10))
                    review_parser.max_scrolls = max_scrolls
                
                reviews = review_parser.parse_reviews()
                
                # Limit reviews if max_reviews specified
                if self.max_reviews and len(reviews) > self.max_reviews:
                    reviews = reviews[:self.max_reviews]
                
                result["reviews"] = reviews
                result["reviews_count"] = len(reviews)
            else:
                result["reviews"] = []
                result["reviews_count"] = 0
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

    def scrape_business_only(self, url: str) -> Dict[str, Any]:
        """Scrape only business information (no reviews) for maximum speed."""
        # Temporarily disable review extraction
        original_extract_reviews = self.extract_reviews
        self.extract_reviews = False
        
        try:
            result = self.scrape(url)
            return result
        finally:
            # Restore original setting
            self.extract_reviews = original_extract_reviews
    
    def scrape_batch(self, urls: List[str]) -> List[Dict[str, Any]]:
        """Bulk-scrape convenience wrapper (placeholder)."""
        return [self.scrape(u) for u in urls] 