"""bob_core.url_validator

URL validation utilities for Google Maps URLs.
Divine validation following Niṣkāma Karma Yoga principles.

Made with 🙏 for interconnected excellence
"""

import re
from urllib.parse import urlparse, parse_qs
from typing import Dict, Any, Optional


def is_valid_google_maps_url(url: str) -> bool:
    """
    Validate if a URL is a valid Google Maps business URL.
    
    Args:
        url: The URL to validate
        
    Returns:
        bool: True if valid Google Maps URL, False otherwise
    """
    if not url or not isinstance(url, str):
        return False
    
    try:
        parsed = urlparse(url.strip())
        
        # Check domain
        if not parsed.netloc or 'google' not in parsed.netloc.lower():
            return False
        
        # Valid Google Maps domains
        valid_domains = [
            'maps.google.com',
            'www.google.com',
            'google.com',
            'maps.google.co.in',
            'maps.google.co.uk',
            'maps.google.ca',
            'maps.google.com.au'
        ]
        
        domain_valid = any(domain in parsed.netloc.lower() for domain in valid_domains)
        if not domain_valid:
            return False
        
        # Check path patterns
        path = parsed.path.lower()
        
        # Common Google Maps URL patterns
        valid_patterns = [
            r'/maps/place/',
            r'/maps/dir/',
            r'/maps/@',
            r'/maps/search/',
            r'/search\?.*tbm=map',
            r'/maps\?.*q=',
            r'/place/'
        ]
        
        pattern_match = any(re.search(pattern, url.lower()) for pattern in valid_patterns)
        
        # Check query parameters for maps-related content
        query_params = parse_qs(parsed.query)
        maps_params = ['q', 'place_id', 'cid', 'ftid', 'data', 'tbm']
        has_maps_params = any(param in query_params for param in maps_params)
        
        # Check for maps in the URL string
        has_maps_keyword = 'maps' in url.lower()
        
        return pattern_match or has_maps_params or has_maps_keyword
        
    except Exception:
        return False


def extract_place_id(url: str) -> Optional[str]:
    """
    Extract place ID from Google Maps URL if available.
    
    Args:
        url: Google Maps URL
        
    Returns:
        str or None: Place ID if found, None otherwise
    """
    if not is_valid_google_maps_url(url):
        return None
    
    try:
        # Look for place_id in query parameters
        parsed = urlparse(url)
        query_params = parse_qs(parsed.query)
        
        if 'place_id' in query_params:
            return query_params['place_id'][0]
        
        # Look for place_id in the URL path or fragment
        place_id_pattern = r'place_id:([A-Za-z0-9_-]+)'
        match = re.search(place_id_pattern, url)
        if match:
            return match.group(1)
        
        # Look for ChIJ pattern (common in place IDs)
        chij_pattern = r'(ChIJ[A-Za-z0-9_-]+)'
        match = re.search(chij_pattern, url)
        if match:
            return match.group(1)
        
        return None
        
    except Exception:
        return None


def extract_coordinates(url: str) -> Optional[Dict[str, float]]:
    """
    Extract latitude and longitude from Google Maps URL if available.
    
    Args:
        url: Google Maps URL
        
    Returns:
        dict or None: {'lat': float, 'lng': float} if found, None otherwise
    """
    if not is_valid_google_maps_url(url):
        return None
    
    try:
        # Look for @lat,lng pattern
        coord_pattern = r'@(-?\d+\.?\d*),(-?\d+\.?\d*)'
        match = re.search(coord_pattern, url)
        if match:
            return {
                'lat': float(match.group(1)),
                'lng': float(match.group(2))
            }
        
        # Look for ll parameter
        parsed = urlparse(url)
        query_params = parse_qs(parsed.query)
        
        if 'll' in query_params:
            coords = query_params['ll'][0].split(',')
            if len(coords) == 2:
                return {
                    'lat': float(coords[0]),
                    'lng': float(coords[1])
                }
        
        return None
        
    except Exception:
        return None


def normalize_google_maps_url(url: str) -> str:
    """
    Normalize Google Maps URL to a standard format.
    
    Args:
        url: Google Maps URL to normalize
        
    Returns:
        str: Normalized URL
    """
    if not is_valid_google_maps_url(url):
        return url
    
    try:
        # Remove unnecessary parameters
        parsed = urlparse(url)
        
        # Keep only essential parameters
        essential_params = ['q', 'place_id', 'cid', 'ftid']
        query_params = parse_qs(parsed.query)
        
        filtered_params = {
            key: value for key, value in query_params.items()
            if key in essential_params
        }
        
        # Reconstruct URL
        if filtered_params:
            query_string = '&'.join(
                f"{key}={value[0]}" for key, value in filtered_params.items()
            )
            normalized_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{query_string}"
        else:
            normalized_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        
        return normalized_url
        
    except Exception:
        return url


def get_url_info(url: str) -> Dict[str, Any]:
    """
    Get comprehensive information about a Google Maps URL.
    
    Args:
        url: Google Maps URL to analyze
        
    Returns:
        dict: URL information including validity, place_id, coordinates, etc.
    """
    return {
        'url': url,
        'is_valid': is_valid_google_maps_url(url),
        'place_id': extract_place_id(url),
        'coordinates': extract_coordinates(url),
        'normalized_url': normalize_google_maps_url(url),
        'domain': urlparse(url).netloc if url else None
    } 