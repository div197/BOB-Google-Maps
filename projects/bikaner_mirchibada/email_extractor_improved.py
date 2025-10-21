#!/usr/bin/env python3
"""
🔧 IMPROVED EMAIL EXTRACTION MODULE
V3.4.1 - Parse Google redirects + Direct website fetching

Status: ⚠️ SAFE TO USE - No breaking changes to existing system
"""

import requests
import re
from urllib.parse import urlparse, parse_qs, unquote

def extract_real_url_from_google_redirect(google_redirect_url):
    """
    Parse Google redirect URL to get actual website URL.

    Input:  https://www.google.com/url?q=http://www.lallgarhpalace.com/&opi=...
    Output: http://www.lallgarhpalace.com/

    Args:
        google_redirect_url: Google-wrapped redirect URL

    Returns:
        str: Actual website URL, or original if not a redirect
    """
    if not google_redirect_url:
        return None

    try:
        # Check if it's a Google redirect
        if 'google.com/url' not in google_redirect_url:
            return google_redirect_url

        # Parse the URL
        parsed = urlparse(google_redirect_url)
        query_params = parse_qs(parsed.query)

        # Extract 'q' parameter (the actual URL)
        if 'q' in query_params:
            real_url = query_params['q'][0]
            # Decode URL-encoded characters
            real_url = unquote(real_url)
            return real_url

        return google_redirect_url
    except Exception as e:
        print(f"  ⚠️ Error parsing Google redirect: {str(e)[:50]}")
        return google_redirect_url

def extract_emails_v31(website_url, timeout=10):
    """
    Enhanced email extraction with redirect parsing.

    Improvements over V3.0:
    1. Parses Google redirect URLs
    2. Multiple regex patterns
    3. Enhanced spam filtering
    4. Better error handling

    Args:
        website_url: Website URL (possibly wrapped in Google redirect)
        timeout: Request timeout in seconds

    Returns:
        list: Email addresses found
    """
    if not website_url:
        return []

    emails = []

    # STEP 1: Parse Google redirect if present
    print(f"  🔍 Checking for redirect wrapper...")
    real_url = extract_real_url_from_google_redirect(website_url)

    if real_url != website_url:
        print(f"  ✅ Redirect parsed: {real_url[:50]}...")
    else:
        print(f"  ℹ️ No redirect wrapper, using URL as-is")

    # Skip if it's still a Google URL
    if 'google' in real_url.lower():
        print(f"  ⚠️ Still a Google URL, skipping")
        return []

    # STEP 2: Ensure URL has protocol
    if not real_url.startswith(('http://', 'https://')):
        real_url = 'https://' + real_url

    # STEP 3: Fetch website with better error handling
    try:
        print(f"  🌐 Fetching: {real_url[:50]}...")

        response = requests.get(
            real_url,
            timeout=timeout,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            },
            allow_redirects=True
        )

        if response.status_code != 200:
            print(f"  ⚠️ HTTP {response.status_code}: {real_url[:40]}...")
            return []

        print(f"  ✅ Website fetched ({len(response.text)} bytes)")

    except requests.Timeout:
        print(f"  ⚠️ Request timeout ({timeout}s): {real_url[:40]}...")
        return []
    except requests.ConnectionError:
        print(f"  ⚠️ Connection error: {real_url[:40]}...")
        return []
    except Exception as e:
        print(f"  ⚠️ Request failed: {str(e)[:40]}...")
        return []

    # STEP 4: Extract emails with multiple patterns
    print(f"  🔎 Searching for emails...")

    patterns = [
        # Standard email
        r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        # Mailto links
        r'mailto:([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
        # Explicit email fields: email: user@domain.com
        r'(?:email|e-mail|contact)[\s:=]+([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
    ]

    found_emails = set()
    for pattern in patterns:
        matches = re.findall(pattern, response.text, re.IGNORECASE)
        for match in matches:
            # Handle tuple results (from group captures)
            if isinstance(match, tuple):
                match = match[-1] if match[-1] else match[0]
            found_emails.add(match.lower())

    print(f"  📧 Found {len(found_emails)} unique email(s)")

    # STEP 5: Filter out spam/test emails
    print(f"  🧹 Filtering spam...")

    spam_keywords = [
        'example', 'test', 'noreply', 'no-reply', 'donotreply', 'do-not-reply',
        'temp', 'fake', 'dummy', 'sample', 'placeholder',
        'admin@localhost', 'root@localhost',
    ]

    filtered_emails = []
    for email in found_emails:
        # Skip if contains spam keyword
        if any(keyword in email for keyword in spam_keywords):
            print(f"    ⏭️ Skipped (spam): {email}")
            continue

        # Skip if not a single @ sign
        if email.count('@') != 1:
            print(f"    ⏭️ Skipped (invalid): {email}")
            continue

        # Skip if has no domain extension
        if '.' not in email.split('@')[1]:
            print(f"    ⏭️ Skipped (no extension): {email}")
            continue

        filtered_emails.append(email)
        print(f"    ✅ Accepted: {email}")

    # Return up to 5 emails
    result = filtered_emails[:5]
    print(f"  ✨ Final result: {len(result)} email(s) extracted")

    return result

def test_email_extraction():
    """Test the improved email extraction"""

    print("\n" + "="*70)
    print("🧪 TESTING IMPROVED EMAIL EXTRACTION V3.1")
    print("="*70 + "\n")

    # Test 1: Real Lalgarh Palace website
    print("TEST 1: Lalgarh Palace Website")
    print("-" * 70)
    emails = extract_emails_v31("http://www.lallgarhpalace.com/", timeout=10)
    print(f"Result: {emails}\n")

    # Test 2: Test with timeout
    print("TEST 2: Timeout Test (very short)")
    print("-" * 70)
    emails = extract_emails_v31("http://www.lallgarhpalace.com/", timeout=0.1)
    print(f"Result: {emails}\n")

    # Test 3: Invalid URL
    print("TEST 3: Invalid URL")
    print("-" * 70)
    emails = extract_emails_v31("not-a-real-url.invalid", timeout=5)
    print(f"Result: {emails}\n")

if __name__ == "__main__":
    test_email_extraction()
