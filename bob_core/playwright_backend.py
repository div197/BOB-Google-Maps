"""bob_core.playwright_backend

Enhanced Playwright-based scraper backend with divine fault tolerance.
Follows the principles of Niṣkāma Karma Yoga - selfless service with perfect execution.
"""
from __future__ import annotations

import time
import logging
from typing import Dict, Any, Optional

try:
    from playwright.sync_api import sync_playwright, Page, Browser, TimeoutError as PlaywrightTimeoutError
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    Page = Browser = PlaywrightTimeoutError = None

from .error_codes import ErrorCodes, create_error_context, handle_error
from .business_parser import BusinessParser
from .review_parser import ReviewParser
from .circuit_breaker import get_circuit_breaker
from .dead_letter_queue import get_global_dlq, FailureReason
from .graceful_degradation import get_global_degradation_manager
from .performance_monitoring import get_global_performance_monitor

__all__ = ["PlaywrightScraper", "PLAYWRIGHT_AVAILABLE"]


class PlaywrightScraper:
    """
    Enhanced Playwright-based Google Maps scraper with divine fault tolerance.
    
    Features:
    - Adaptive timeout management
    - Circuit breaker protection
    - Dead letter queue integration
    - Performance monitoring
    - Graceful degradation
    - Self-healing capabilities
    """
    
    def __init__(self, headless: bool = True, timeout: int = 60):
        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError("Playwright not installed. Run: pip install playwright")
        
        self.headless = headless
        self.base_timeout = timeout
        self.timeout = timeout * 1000  # Playwright uses milliseconds
        self.adaptive_timeout_multiplier = 1.0
        
        # Initialize divine systems
        self.circuit_breaker = get_circuit_breaker("playwright_scraper", 
                                                  failure_threshold=3, 
                                                  recovery_timeout=60)
        self.dlq = get_global_dlq()
        self.degradation_manager = get_global_degradation_manager()
        self.performance_monitor = get_global_performance_monitor()
        
        self._logger = logging.getLogger("bob_core.playwright_scraper")
        
    def scrape(self, url: str, extract_reviews: bool = True, max_reviews: int = None) -> Dict[str, Any]:
        """Scrape a Google Maps URL with divine fault tolerance."""
        # Track performance
        with self.performance_monitor.profiler.profile("playwright_scrape", {"url": url}):
            return self._scrape_with_circuit_breaker(url, extract_reviews, max_reviews)
    
    def _scrape_with_circuit_breaker(self, url: str, extract_reviews: bool = True, max_reviews: int = None) -> Dict[str, Any]:
        """Execute scraping with circuit breaker protection."""
        try:
            return self.circuit_breaker.call(self._scrape_internal, url, extract_reviews, max_reviews)
        except Exception as e:
            # Circuit breaker is open or other error
            return self._handle_circuit_breaker_failure(url, e)
    
    def _scrape_internal(self, url: str, extract_reviews: bool = True, max_reviews: int = None) -> Dict[str, Any]:
        """Internal scraping logic with enhanced error handling."""
        result: Dict[str, Any] = {
            "url": url,
            "success": False,
            "error_code": ErrorCodes.SUCCESS,
            "error_message": "",
            "business_info": {},
            "reviews": [],
            "reviews_count": 0,
        }
        
        browser = None
        context = None
        page = None
        
        try:
            # Adaptive timeout based on recent performance
            current_timeout = int(self.timeout * self.adaptive_timeout_multiplier)
            self._logger.info(f"Starting scrape with timeout: {current_timeout}ms")
            
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=self.headless,
                    args=[
                        "--no-sandbox",
                        "--disable-dev-shm-usage",
                        "--disable-blink-features=AutomationControlled",
                        "--disable-web-security",
                        "--disable-features=VizDisplayCompositor"
                    ]
                )
                
                context = browser.new_context(
                    viewport={"width": 1920, "height": 1080},
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                )
                
                page = context.new_page()
                page.set_default_timeout(current_timeout)
                
                # Navigate with retry logic
                self._navigate_with_retry(page, url)
                
                # Extract business info with graceful degradation
                business_info = self._extract_business_info_safe(page, url)
                result["business_info"] = business_info
                
                # Extract reviews only if requested
                if extract_reviews:
                    reviews = self._extract_reviews_safe(page, url, max_reviews)
                    result["reviews"] = reviews
                    result["reviews_count"] = len(reviews)
                else:
                    result["reviews"] = []
                    result["reviews_count"] = 0
                
                result["success"] = True
                self._adjust_timeout_on_success()
                return result
                
        except PlaywrightTimeoutError as e:
            return self._handle_timeout_error(url, e, result)
        except Exception as e:
            return self._handle_general_error(url, e, result)
        finally:
            self._cleanup_browser_resources(browser, context, page)
    
    def _navigate_with_retry(self, page: Page, url: str, max_retries: int = 3) -> None:
        """Navigate to URL with retry logic and adaptive timeout."""
        for attempt in range(max_retries):
            try:
                self._logger.info(f"Navigation attempt {attempt + 1} for {url}")
                page.goto(url, wait_until="domcontentloaded", timeout=self.timeout)
                time.sleep(3)  # Let page settle and load dynamic content
                return
            except PlaywrightTimeoutError as e:
                if attempt == max_retries - 1:
                    raise
                self._logger.warning(f"Navigation timeout on attempt {attempt + 1}, retrying...")
                self._increase_adaptive_timeout()
                time.sleep(2 ** attempt)  # Exponential backoff
    
    def _extract_business_info_safe(self, page: Page, url: str) -> Dict[str, Any]:
        """Extract business info with graceful degradation."""
        try:
            return self._extract_business_info(page)
        except Exception as e:
            self._logger.warning(f"Business info extraction failed for {url}: {e}")
            # Return minimal info in degraded mode
            return self.degradation_manager.get_minimal_business_info(url)
    
    def _extract_reviews_safe(self, page: Page, url: str, max_reviews: int = None) -> list:
        """Extract reviews with graceful degradation."""
        try:
            return self._extract_reviews(page, max_reviews)
        except Exception as e:
            self._logger.warning(f"Reviews extraction failed for {url}: {e}")
            # Return empty reviews in degraded mode
            return []
    
    def _extract_business_info(self, page: Page) -> Dict[str, Any]:
        """Extract business information from the page with enhanced selectors."""
        info = {}
        
        try:
            # Enhanced name extraction with multiple selectors
            name_selectors = [
                "h1.DUwDvf.lfPIob",
                "h1[data-attrid='title']",
                "h1.x3AX1-LfntMc-header-title-title",
                "[data-value='title'] h1"
            ]
            name = self._extract_with_fallback_selectors(page, name_selectors, "text")
            info["name"] = name or "Unknown"
            
            # Enhanced rating extraction
            rating_selectors = [
                "span.ceNzKf",
                "[data-value='rating'] span",
                ".gm2-display-2"
            ]
            rating = self._extract_with_fallback_selectors(page, rating_selectors, "aria-label")
            info["rating"] = rating or "Unrated"
            
            # Enhanced category extraction
            category_selectors = [
                "button.DkEaL",
                "[data-value='category'] button",
                ".YhemCb"
            ]
            category = self._extract_with_fallback_selectors(page, category_selectors, "text")
            info["category"] = category or "Unknown"
            
            # Enhanced address extraction
            address_selectors = [
                "div.QSFF4-text",
                "[data-value='address'] div",
                ".CsEnBe"
            ]
            address = self._extract_with_fallback_selectors(page, address_selectors, "text")
            info["address"] = address or "Unknown"
            
            # Phone extraction
            phone_elem = page.query_selector("a[href^='tel:']")
            if phone_elem:
                info["phone"] = phone_elem.get_attribute("href").replace("tel:", "")
            else:
                info["phone"] = "Unavailable"
            
            # Website extraction
            website_elem = page.query_selector("a[href^='http'][rel*='noopener']")
            if website_elem:
                info["website"] = website_elem.get_attribute("href")
            else:
                info["website"] = "Unavailable"
                
        except Exception as e:
            self._logger.error(f"Error extracting business info: {e}")
            
        return info
    
    def _extract_with_fallback_selectors(self, page: Page, selectors: list, attribute: str) -> Optional[str]:
        """Extract content using fallback selectors for resilience."""
        for selector in selectors:
            try:
                elem = page.query_selector(selector)
                if elem:
                    if attribute == "text":
                        return elem.inner_text().strip()
                    else:
                        return elem.get_attribute(attribute)
            except Exception:
                continue
        return None
    
    def _extract_reviews(self, page: Page, max_reviews: int = None) -> list:
        """Extract reviews with enhanced selectors and error handling."""
        reviews = []
        
        try:
            # Enhanced reviews tab detection
            reviews_selectors = [
                "//div[@class='LRkQ2']//div[text()='Reviews']",
                "//button[contains(text(), 'Reviews')]",
                "//div[contains(text(), 'Reviews')]",
                "//span[contains(text(), 'reviews')]",
                "[data-value='reviews'] button"
            ]
            
            clicked = False
            for selector in reviews_selectors:
                try:
                    if selector.startswith("//"):
                        elem = page.query_selector(f"xpath={selector}")
                    else:
                        elem = page.query_selector(selector)
                    
                    if elem and elem.is_visible():
                        elem.click()
                        clicked = True
                        self._logger.info("Successfully clicked reviews tab")
                        break
                except Exception:
                    continue
            
            if not clicked:
                self._logger.warning("Could not find or click reviews tab")
                return reviews
                
            time.sleep(3)  # Wait for reviews to load
            
            # Enhanced scrolling for more reviews
            container_selectors = [
                "div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde",
                "[data-value='reviews-container']",
                ".section-scrollbox"
            ]
            
            container = None
            for selector in container_selectors:
                container = page.query_selector(selector)
                if container:
                    break
            
            if container:
                # Intelligent scrolling with performance monitoring
                scroll_attempts = 0
                max_scrolls = 15
                
                # Optimize scrolling based on max_reviews
                if max_reviews:
                    # Estimate scrolls needed (roughly 10 reviews per scroll)
                    estimated_scrolls = min(max_scrolls, max(1, max_reviews // 10))
                    max_scrolls = estimated_scrolls
                
                last_review_count = 0
                
                while scroll_attempts < max_scrolls:
                    page.evaluate("(element) => element.scrollTop = element.scrollHeight", container)
                    time.sleep(1.5)
                    
                    # Check if new reviews loaded
                    current_reviews = page.query_selector_all("div.jftiEf.fontBodyMedium")
                    if len(current_reviews) == last_review_count:
                        break  # No new reviews loaded
                    
                    # Stop early if we have enough reviews
                    if max_reviews and len(current_reviews) >= max_reviews:
                        break
                    
                    last_review_count = len(current_reviews)
                    scroll_attempts += 1
            
            # Enhanced review extraction
            review_selectors = [
                "div.jftiEf.fontBodyMedium",
                "[data-review-id]",
                ".section-review"
            ]
            
            review_elements = []
            for selector in review_selectors:
                review_elements = page.query_selector_all(selector)
                if review_elements:
                    break
            
            for elem in review_elements:
                try:
                    review_data = self._extract_single_review(elem)
                    if review_data:
                        reviews.append(review_data)
                        
                        # Stop if we've reached max_reviews
                        if max_reviews and len(reviews) >= max_reviews:
                            break
                except Exception as e:
                    self._logger.debug(f"Failed to extract single review: {e}")
                    continue
                    
        except Exception as e:
            self._logger.error(f"Error extracting reviews: {e}")
            
        self._logger.info(f"Extracted {len(reviews)} reviews")
        return reviews
    
    def _extract_single_review(self, elem) -> Optional[Dict[str, Any]]:
        """Extract data from a single review element."""
        try:
            # Username
            username_selectors = ["aria-label", "data-reviewer-name"]
            username = "Anonymous"
            for attr in username_selectors:
                value = elem.get_attribute(attr)
                if value:
                    username = value
                    break
            
            # Content
            content_selectors = ["span.wiI7pd", ".section-review-text", "[data-review-text]"]
            content = ""
            for selector in content_selectors:
                content_elem = elem.query_selector(selector)
                if content_elem:
                    content = content_elem.inner_text().strip()
                    break
            
            # Rating
            rating_selectors = ["span.kvMYJc", "[data-rating]", ".section-review-stars"]
            rating = "Unrated"
            for selector in rating_selectors:
                rating_elem = elem.query_selector(selector)
                if rating_elem:
                    rating = rating_elem.get_attribute("aria-label") or "Unrated"
                    break
            
            # Timestamp
            time_selectors = ["span.rsqaWe", "[data-review-time]", ".section-review-publish-date"]
            timestamp = ""
            for selector in time_selectors:
                time_elem = elem.query_selector(selector)
                if time_elem:
                    timestamp = time_elem.inner_text().strip()
                    break
            
            return {
                "username": username,
                "content": content,
                "rating": rating,
                "time": timestamp,
            }
            
        except Exception:
            return None
    
    def _handle_timeout_error(self, url: str, error: Exception, result: Dict[str, Any]) -> Dict[str, Any]:
        """Handle timeout errors with proper categorization and recovery."""
        error_message = str(error)
        
        # Categorize timeout type
        if "Page.goto" in error_message:
            error_code = ErrorCodes.NETWORK_TIMEOUT
            failure_reason = FailureReason.TIMEOUT
        elif "networkidle" in error_message:
            error_code = ErrorCodes.NETWORK_TIMEOUT
            failure_reason = FailureReason.NETWORK_ERROR
        else:
            error_code = ErrorCodes.BROWSER_TIMEOUT
            failure_reason = FailureReason.TIMEOUT
        
        result["error_code"] = error_code
        result["error_message"] = error_message
        
        # Add to dead letter queue for retry
        self.dlq.add_failed_request({
            "id": f"timeout_{int(time.time())}",
            "url": url,
            "failure_reason": failure_reason,
            "error_message": error_message,
            "timestamp": time.time(),
            "context": {"timeout": self.timeout, "adaptive_multiplier": self.adaptive_timeout_multiplier}
        })
        
        # Increase adaptive timeout for future requests
        self._increase_adaptive_timeout()
        
        self._logger.error(f"Timeout error for {url}: {error_message}")
        return result
    
    def _handle_general_error(self, url: str, error: Exception, result: Dict[str, Any]) -> Dict[str, Any]:
        """Handle general errors with proper categorization."""
        error_message = str(error)
        
        # Categorize error type
        if "browser" in error_message.lower() or "chromium" in error_message.lower():
            error_code = ErrorCodes.BROWSER_INIT_FAILED
            failure_reason = FailureReason.UNKNOWN_ERROR
        elif "network" in error_message.lower() or "connection" in error_message.lower():
            error_code = ErrorCodes.CONNECTION_REFUSED
            failure_reason = FailureReason.NETWORK_ERROR
        else:
            error_code = ErrorCodes.UNEXPECTED_ERROR
            failure_reason = FailureReason.UNKNOWN_ERROR
        
        result["error_code"] = error_code
        result["error_message"] = error_message
        
        # Add to dead letter queue
        self.dlq.add_failed_request({
            "id": f"error_{int(time.time())}",
            "url": url,
            "failure_reason": failure_reason,
            "error_message": error_message,
            "timestamp": time.time(),
            "context": {"error_type": type(error).__name__}
        })
        
        self._logger.error(f"General error for {url}: {error_message}")
        return result
    
    def _handle_circuit_breaker_failure(self, url: str, error: Exception) -> Dict[str, Any]:
        """Handle circuit breaker failures with graceful degradation."""
        result = {
            "url": url,
            "success": False,
            "error_code": ErrorCodes.CIRCUIT_BREAKER_OPEN,
            "error_message": f"Circuit breaker is open: {str(error)}",
            "business_info": {},
            "reviews": [],
            "reviews_count": 0,
        }
        
        # Try graceful degradation
        degraded_info = self.degradation_manager.get_cached_business_info(url)
        if degraded_info:
            result["business_info"] = degraded_info
            result["error_message"] += " (using cached data)"
        
        return result
    
    def _cleanup_browser_resources(self, browser, context, page) -> None:
        """Safely cleanup browser resources."""
        try:
            if page:
                page.close()
        except Exception:
            pass
        
        try:
            if context:
                context.close()
        except Exception:
            pass
        
        try:
            if browser:
                browser.close()
        except Exception:
            pass
    
    def _adjust_timeout_on_success(self) -> None:
        """Adjust adaptive timeout on successful scraping."""
        if self.adaptive_timeout_multiplier > 1.0:
            self.adaptive_timeout_multiplier = max(1.0, self.adaptive_timeout_multiplier * 0.9)
            self._logger.info(f"Reduced adaptive timeout multiplier to {self.adaptive_timeout_multiplier:.2f}")
    
    def _increase_adaptive_timeout(self) -> None:
        """Increase adaptive timeout on failures."""
        self.adaptive_timeout_multiplier = min(3.0, self.adaptive_timeout_multiplier * 1.2)
        self._logger.info(f"Increased adaptive timeout multiplier to {self.adaptive_timeout_multiplier:.2f}")
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get scraper performance metrics."""
        return {
            "base_timeout": self.base_timeout,
            "current_timeout": self.timeout,
            "adaptive_multiplier": self.adaptive_timeout_multiplier,
            "circuit_breaker_metrics": self.circuit_breaker.get_metrics(),
            "dlq_stats": self.dlq.get_statistics()
        } 