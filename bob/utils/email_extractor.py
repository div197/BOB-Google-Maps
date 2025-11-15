#!/usr/bin/env python3
"""
Email Extraction Module - Handles Google Redirect URLs

Key Feature: Parses Google redirect URLs to get actual business websites
Then extracts emails from those websites
"""

import requests
import re
from urllib.parse import urlparse, parse_qs, unquote


def extract_real_url_from_google_redirect(google_redirect_url):
    """
    Parse Google redirect URL to get actual website URL.

    Examples:
    - Input:  https://www.google.com/url?q=http://www.lallgarhpalace.com/&opi=...
    - Output: http://www.lallgarhpalace.com/

    - Input:  https://www.google.com/viewer/chooseprovider?mid=/g/1td74zyg&g2lbs=...
    - Output: None (unrecognized Google format - return original)
    """
    if not google_redirect_url:
        return None

    try:
        # Check if it's a Google redirect with 'q' parameter
        if 'google.com/url' in google_redirect_url and 'q=' in google_redirect_url:
            # Parse the URL
            parsed = urlparse(google_redirect_url)
            query_params = parse_qs(parsed.query)

            # Extract 'q' parameter (the actual URL)
            if 'q' in query_params and query_params['q']:
                real_url = query_params['q'][0]
                # Decode URL-encoded characters
                real_url = unquote(real_url)
                return real_url

        # If not a recognized Google redirect format, return original
        return google_redirect_url

    except Exception as e:
        print(f"  ⚠️ Error parsing redirect: {str(e)[:50]}")
        return google_redirect_url


def extract_emails_from_website(website_url, timeout=10):
    """
    Extract emails from business website, handling Google redirect URLs.

    Process:
    1. Parse Google redirects if present
    2. Validate URL format
    3. Fetch website content
    4. Search for emails with multiple regex patterns
    5. Filter out spam/fake emails

    Args:
        website_url: Website URL (may be Google redirect)
        timeout: Request timeout in seconds

    Returns:
        list: Email addresses found (max 5)
    """
    if not website_url:
        return []

    emails = []

    # STEP 1: Parse Google redirect if present
    real_url = extract_real_url_from_google_redirect(website_url)

    # STEP 2: Skip if still a Google URL (unrecognized format)
    if 'google' in real_url.lower():
        return []

    # STEP 3: Ensure URL has protocol
    if not real_url.startswith(('http://', 'https://')):
        real_url = 'https://' + real_url

    # STEP 4: Fetch website
    try:
        response = requests.get(
            real_url,
            timeout=timeout,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            },
            allow_redirects=True
        )

        if response.status_code != 200:
            return []

    except (requests.Timeout, requests.ConnectionError, Exception):
        return []

    # STEP 5: Extract emails with multiple patterns
    patterns = [
        # Standard email format
        r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        # Mailto links
        r'mailto:([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
        # Email field labels
        r'(?:email|e-mail|contact)[\s:=]+([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
    ]

    found_emails = set()
    for pattern in patterns:
        try:
            matches = re.findall(pattern, response.text, re.IGNORECASE)
            for match in matches:
                # Handle tuple results from group captures
                if isinstance(match, tuple):
                    match = match[-1] if match[-1] else match[0]
                found_emails.add(match.lower())
        except:
            pass

    # STEP 6: Filter out spam/fake emails
    spam_keywords = [
        'example', 'test', 'noreply', 'no-reply', 'donotreply', 'do-not-reply',
        'temp', 'fake', 'dummy', 'sample', 'placeholder', 'mail',
        'admin@localhost', 'root@localhost',
    ]

    filtered_emails = []
    for email in found_emails:
        # Skip if contains spam keyword
        if any(keyword in email for keyword in spam_keywords):
            continue

        # Validate email format
        if email.count('@') != 1:
            continue

        # Ensure domain has extension
        if '.' not in email.split('@')[1]:
            continue

        filtered_emails.append(email)

    # Return up to 5 emails
    return filtered_emails[:5]
