"""bob_core.playwright_backend

Playwright-based scraper backend (faster, more reliable than Selenium).
"""
from __future__ import annotations

import time
from typing import Dict, Any, Optional

try:
    from playwright.sync_api import sync_playwright, Page, Browser
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    Page = Browser = None

from .error_codes import ErrorCodes
from .business_parser import BusinessParser
from .review_parser import ReviewParser

__all__ = ["PlaywrightScraper", "PLAYWRIGHT_AVAILABLE"]


class PlaywrightScraper:
    """Playwright-based Google Maps scraper."""
    
    def __init__(self, headless: bool = True, timeout: int = 30):
        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError("Playwright not installed. Run: pip install playwright")
        
        self.headless = headless
        self.timeout = timeout * 1000  # Playwright uses milliseconds
        
    def scrape(self, url: str) -> Dict[str, Any]:
        """Scrape a Google Maps URL using Playwright."""
        result: Dict[str, Any] = {
            "url": url,
            "success": False,
            "error_code": ErrorCodes.SUCCESS,
            "error_message": "",
            "business_info": {},
            "reviews": [],
            "reviews_count": 0,
        }
        
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(
                    headless=self.headless,
                    args=[
                        "--no-sandbox",
                        "--disable-dev-shm-usage",
                        "--disable-blink-features=AutomationControlled"
                    ]
                )
                
                context = browser.new_context(
                    viewport={"width": 1920, "height": 1080},
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                )
                
                page = context.new_page()
                page.set_default_timeout(self.timeout)
                
                # Navigate to URL
                page.goto(url, wait_until="networkidle")
                time.sleep(2)  # Let page settle
                
                # Extract business info
                business_info = self._extract_business_info(page)
                result["business_info"] = business_info
                
                # Extract reviews
                reviews = self._extract_reviews(page)
                result["reviews"] = reviews
                result["reviews_count"] = len(reviews)
                
                result["success"] = True
                return result
                
            except Exception as exc:
                result["error_code"] = ErrorCodes.UNEXPECTED_ERROR
                result["error_message"] = str(exc)
                return result
            finally:
                try:
                    browser.close()
                except:
                    pass
    
    def _extract_business_info(self, page: Page) -> Dict[str, Any]:
        """Extract business information from the page."""
        info = {}
        
        try:
            # Name
            name_elem = page.query_selector("h1.DUwDvf.lfPIob")
            info["name"] = name_elem.inner_text().strip() if name_elem else "Unknown"
            
            # Rating
            rating_elem = page.query_selector("span.ceNzKf")
            info["rating"] = rating_elem.get_attribute("aria-label") if rating_elem else "Unrated"
            
            # Category
            category_elem = page.query_selector("button.DkEaL")
            info["category"] = category_elem.inner_text().strip() if category_elem else "Unknown"
            
            # Address
            address_elem = page.query_selector("div.QSFF4-text")
            info["address"] = address_elem.inner_text().strip() if address_elem else "Unknown"
            
            # Phone
            phone_elem = page.query_selector("a[href^='tel:']")
            if phone_elem:
                info["phone"] = phone_elem.get_attribute("href").replace("tel:", "")
            else:
                info["phone"] = "Unavailable"
            
            # Website
            website_elem = page.query_selector("a[href^='http'][rel*='noopener']")
            if website_elem:
                info["website"] = website_elem.get_attribute("href")
            else:
                info["website"] = "Unavailable"
                
        except Exception:
            pass  # Return partial info on error
            
        return info
    
    def _extract_reviews(self, page: Page) -> list:
        """Extract reviews from the page."""
        reviews = []
        
        try:
            # Try to click Reviews tab
            reviews_selectors = [
                "//div[@class='LRkQ2']//div[text()='Reviews']",
                "//button[contains(text(), 'Reviews')]",
                "//div[contains(text(), 'Reviews')]"
            ]
            
            clicked = False
            for selector in reviews_selectors:
                elem = page.query_selector(f"xpath={selector}")
                if elem:
                    elem.click()
                    clicked = True
                    break
            
            if not clicked:
                return reviews
                
            time.sleep(2)
            
            # Scroll to load more reviews
            container = page.query_selector("div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde")
            if container:
                for _ in range(10):  # Scroll up to 10 times
                    page.evaluate("arguments[0].scrollTop = arguments[0].scrollHeight", container)
                    time.sleep(1)
            
            # Extract review elements
            review_elements = page.query_selector_all("div.jftiEf.fontBodyMedium")
            
            for elem in review_elements:
                try:
                    username = elem.get_attribute("aria-label") or "Anonymous"
                    
                    content_elem = elem.query_selector("span.wiI7pd")
                    content = content_elem.inner_text().strip() if content_elem else ""
                    
                    rating_elem = elem.query_selector("span.kvMYJc")
                    rating = rating_elem.get_attribute("aria-label") if rating_elem else "Unrated"
                    
                    time_elem = elem.query_selector("span.rsqaWe")
                    timestamp = time_elem.inner_text().strip() if time_elem else ""
                    
                    reviews.append({
                        "username": username,
                        "content": content,
                        "rating": rating,
                        "time": timestamp,
                    })
                    
                except Exception:
                    continue
                    
        except Exception:
            pass  # Return partial results
            
        return reviews 