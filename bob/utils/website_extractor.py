#!/usr/bin/env python3
"""
🔧 INDIE HACKER STYLE WEBSITE EXTRACTION
Advanced methodology to extract actual business websites from Google Maps listings.

The problem: Google Maps sometimes shows provider chooser URLs or booking URLs
instead of actual business websites. Solution: Multi-layer extraction that
examines the full page context, extracts all URLs, filters intelligently.
"""

import re
from urllib.parse import urlparse, parse_qs, unquote
from typing import Optional


def extract_website_intelligent(page_text: str, available_urls: list) -> Optional[str]:
    """
    Smart website extraction using "indie hacker" methodology.

    Strategy:
    1. Filter out Google internal URLs
    2. Look for patterns like "website:", "visit:", "contact"
    3. Validate URLs for business legitimacy
    4. Prefer actual domains over Google URLs

    Args:
        page_text: Full page text from Google Maps listing
        available_urls: List of URLs extracted from page elements

    Returns:
        Actual business website URL or None
    """

    filtered_urls = []

    # Step 1: Filter and categorize URLs
    for url in available_urls:
        if not url:
            continue

        # Skip Google internal URLs UNLESS they're redirects we can parse
        if 'google.com' in url.lower():
            # Check if it's a redirect we can parse
            if '/url?' in url or 'q=' in url:
                # This might be a Google redirect with actual URL
                actual = parse_google_redirect(url)
                if actual and 'google.com' not in actual.lower():
                    filtered_urls.append(('redirect', actual))
            # Skip provider chooser URLs, Maps URLs, etc
            continue

        # Keep non-Google URLs
        if _is_valid_business_url(url):
            filtered_urls.append(('direct', url))

    # Step 2: Look for website mentions in page text with context
    pattern_based_urls = _extract_urls_from_patterns(page_text)
    for url in pattern_based_urls:
        if url not in [u[1] for u in filtered_urls]:
            filtered_urls.append(('pattern', url))

    # Step 3: Score and select best URL
    if filtered_urls:
        # Prefer direct URLs > pattern-based > redirects
        priority_order = {'direct': 0, 'pattern': 1, 'redirect': 2}
        filtered_urls.sort(key=lambda x: priority_order.get(x[0], 99))
        return filtered_urls[0][1]

    return None


def parse_google_redirect(google_url: str) -> Optional[str]:
    """
    Parse Google redirect URL to extract actual website.

    Example:
    Input:  https://www.google.com/url?q=http://www.business.com/&opi=...
    Output: http://www.business.com/
    """
    try:
        if 'google.com/url' not in google_url or 'q=' not in google_url:
            return google_url

        parsed = urlparse(google_url)
        query_params = parse_qs(parsed.query)

        if 'q' in query_params and query_params['q']:
            real_url = query_params['q'][0]
            real_url = unquote(real_url)
            return real_url

        return google_url
    except:
        return google_url


def _is_valid_business_url(url: str) -> bool:
    """
    Check if URL looks like a legitimate business website.

    Filters out:
    - Facebook/Instagram profiles (not primary websites)
    - Booking platforms (ZomatoOneTableResy, etc) - these are intermediaries
    - Maps/review sites
    - Email addresses (shouldn't be here but just in case)
    - localhost/private IPs
    """

    if not url:
        return False

    url_lower = url.lower()

    # Block specific intermediary platforms
    blocked_keywords = [
        'maps.google',
        'google.com/maps',
        '/maps/reserve',
        '/maps/place',
        'maps-booking',
        # Social media (not primary business website)
        'facebook.com',
        'instagram.com',
        'twitter.com',
        'youtube.com',
        # Booking platforms (intermediaries, not business website)
        'zomato.com',
        'swiggy.com',
        'booking.com',
        'tripadvisor',
        'yelp.com',
        'justdial',
        'urban piper',
        'deliveroo',
        'ubereats',
        'doordash',
        'grubhub',
        # Review/rating sites
        'trustpilot',
        'glassdoor',
        'g2.com',
        # Email addresses
        '@',
        'mailto',
        # Private/local IPs
        'localhost',
        '127.0.0.1',
        '192.168',
        '10.0',
    ]

    for keyword in blocked_keywords:
        if keyword in url_lower:
            return False

    # Should look like a real URL
    try:
        parsed = urlparse(url)
        # Must have a domain
        if not parsed.netloc:
            return False
        # Should be http/https
        if parsed.scheme not in ('http', 'https', ''):
            return False
        return True
    except:
        return False


def _extract_urls_from_patterns(text: str) -> list:
    """
    Extract URLs from page text using patterns like:
    - "website: www.example.com"
    - "visit: example.com"
    - "contact: www.example.com"
    - Direct URLs in text
    """

    urls = []

    # Pattern 1: "website:", "visit:", "web:", "contact us at:" followed by URL
    pattern1 = r'(?:website|visit|web|contact us at|our site|home page|homepage)[\s:]*(?:www\.)?([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9](?:\.[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9])*(?:\.[a-zA-Z]{2,})?)'
    matches = re.finditer(pattern1, text, re.IGNORECASE)
    for match in matches:
        domain = match.group(1)
        if not domain.startswith('www'):
            domain = 'www.' + domain
        url = f'https://{domain}'
        if _is_valid_business_url(url):
            urls.append(url)

    # Pattern 2: Direct URLs (but not Google/Maps URLs)
    url_pattern = r'https?://(?:www\.)?([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9](?:\.[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9])*(?:\.[a-zA-Z]{2,})(?:[/?#][^\s]*)?)'
    matches = re.finditer(url_pattern, text)
    for match in matches:
        url = match.group(0)
        # Remove trailing punctuation that isn't part of URL
        url = re.sub(r'[.,;:!?\)\]]+$', '', url)
        if _is_valid_business_url(url) and url not in urls:
            urls.append(url)

    return urls


def extract_website_from_page(page_locator) -> Optional[str]:
    """
    Extract website from Playwright page using multi-layer approach.

    Args:
        page_locator: Playwright page object or locator

    Returns:
        Business website URL or None
    """

    try:
        # Try to get page text (if it's a page object)
        if hasattr(page_locator, 'content'):
            page_text = page_locator.content()
        elif hasattr(page_locator, 'text_content'):
            page_text = page_locator.text_content()
        else:
            page_text = ""

        # Collect all URLs from various selectors
        available_urls = []

        # Primary selector
        selectors = [
            "a[data-item-id='authority']",
            "a[aria-label*='website']",
            "a[aria-label*='Website']",
            ".lVcKpb a[href*='http']",
            "a[href*='http']",
        ]

        for selector in selectors:
            try:
                # Try Playwright API
                if hasattr(page_locator, 'query_selector'):
                    elem = page_locator.query_selector(selector)
                    if elem:
                        href = elem.get_attribute("href")
                        if href:
                            available_urls.append(href)
                # Or sync version
                elif hasattr(page_locator, 'find_element'):
                    elems = page_locator.find_elements("css selector", selector)
                    for elem in elems:
                        href = elem.get_attribute("href")
                        if href:
                            available_urls.append(href)
            except:
                continue

        # Use intelligent extraction
        website = extract_website_intelligent(page_text, available_urls)
        return website

    except Exception as e:
        print(f"⚠️ Website extraction error: {str(e)[:50]}")
        return None


# Export functions for use in extractors
__all__ = [
    'extract_website_intelligent',
    'parse_google_redirect',
    'extract_website_from_page',
]
