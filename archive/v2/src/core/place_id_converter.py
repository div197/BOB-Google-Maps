#!/usr/bin/env python3
"""
Place ID Format Converter for Google Maps
September 2025 - Convert between different Place ID formats

Google Maps uses multiple Place ID formats:
1. ChIJ... format (standard, 27 chars)
2. GhIJ... format (alternative)
3. Hex format: 0x...:0x... (feature ID:location ID)
4. CID format: numeric customer ID
5. FID format: feature ID
"""

import re
import base64

class PlaceIDConverter:
    """
    Convert between different Place ID formats.

    Note: Some conversions are one-way only as Google's encoding is proprietary.
    """

    @staticmethod
    def identify_format(place_id):
        """
        Identify the format of a Place ID.

        Returns:
            dict with 'format' and 'components'
        """
        if not place_id:
            return {'format': 'unknown', 'components': None}

        place_id = str(place_id).strip()

        # ChIJ format (standard)
        if place_id.startswith('ChIJ'):
            return {
                'format': 'ChIJ',
                'standard': True,
                'length': len(place_id),
                'valid': len(place_id) == 27
            }

        # GhIJ format
        if place_id.startswith('GhIJ'):
            return {
                'format': 'GhIJ',
                'standard': True,
                'length': len(place_id),
                'valid': True
            }

        # Hex format (0x...:0x...)
        hex_match = re.match(r'^(0x[a-f0-9]+):(0x[a-f0-9]+)$', place_id.lower())
        if hex_match:
            return {
                'format': 'hex',
                'standard': False,
                'components': {
                    'feature_id': hex_match.group(1),
                    'location_id': hex_match.group(2)
                },
                'feature_id_int': int(hex_match.group(1), 16),
                'location_id_int': int(hex_match.group(2), 16)
            }

        # CID format (numeric)
        if place_id.isdigit():
            return {
                'format': 'cid',
                'standard': False,
                'numeric_value': int(place_id)
            }

        # Long base64 format (addresses/intersections)
        if re.match(r'^[A-Za-z0-9+/=_-]{30,}$', place_id):
            return {
                'format': 'base64_long',
                'standard': False,
                'length': len(place_id)
            }

        # Unknown but valid-looking
        if re.match(r'^[A-Za-z0-9_-]+$', place_id):
            return {
                'format': 'unknown_valid',
                'standard': False,
                'length': len(place_id)
            }

        return {'format': 'unknown', 'components': None}

    @staticmethod
    def hex_to_cid(hex_place_id):
        """
        Convert hex format Place ID to CID (Customer ID) format.

        Example: 0x89c25a31ebfbc6bf:0xb80ba2960244e4f4 -> CID number

        The CID is derived from the location_id (second hex value).
        """
        format_info = PlaceIDConverter.identify_format(hex_place_id)

        if format_info['format'] != 'hex':
            return {'error': 'Not a hex format Place ID'}

        components = format_info['components']

        # Convert to decimal representations
        feature_decimal = format_info['feature_id_int']
        location_decimal = format_info['location_id_int']

        # The CID is typically the location_id in decimal
        # This is the standard Google CID format
        cid = location_decimal

        return {
            'original': hex_place_id,
            'format': 'hex',
            'cid': cid,
            'cid_string': str(cid),
            'feature_id': components['feature_id'],
            'location_id': components['location_id'],
            'feature_decimal': feature_decimal,
            'location_decimal': location_decimal,
            'note': 'CID is the decimal representation of location_id'
        }

    @staticmethod
    def normalize_place_id(place_id):
        """
        Normalize any Place ID format to CID format for consistent storage.

        ALL formats are converted to CID (Customer ID) for uniformity.

        Returns:
            dict with 'normalized_id' (as CID) and 'original_format'
        """
        if not place_id:
            return {'normalized_id': None, 'original_format': None, 'cid': None}

        format_info = PlaceIDConverter.identify_format(place_id)

        # Hex format - convert to CID
        if format_info['format'] == 'hex':
            hex_info = PlaceIDConverter.hex_to_cid(place_id)
            return {
                'normalized_id': str(hex_info['cid']),
                'cid': hex_info['cid'],
                'original_format': 'hex',
                'original_id': place_id,
                'is_cid': True
            }

        # Already CID format
        if format_info['format'] == 'cid':
            return {
                'normalized_id': place_id,
                'cid': int(place_id),
                'original_format': 'cid',
                'original_id': place_id,
                'is_cid': True
            }

        # ChIJ or GhIJ format - cannot convert to CID without Google's API
        # But we can create a pseudo-CID using hash
        if format_info.get('standard'):
            import hashlib
            # Create a consistent CID-like number from the Place ID
            hash_digest = hashlib.sha256(place_id.encode()).digest()
            # Use first 8 bytes as integer (creates a large but valid CID-like number)
            pseudo_cid = int.from_bytes(hash_digest[:8], 'big')

            return {
                'normalized_id': str(pseudo_cid),
                'cid': pseudo_cid,
                'original_format': format_info['format'],
                'original_id': place_id,
                'is_cid': False,  # It's a pseudo-CID
                'note': 'Pseudo-CID generated from hash'
            }

        # Unknown format - create pseudo-CID
        if format_info['format'] in ['unknown_valid', 'base64_long']:
            import hashlib
            hash_digest = hashlib.sha256(str(place_id).encode()).digest()
            pseudo_cid = int.from_bytes(hash_digest[:8], 'big')

            return {
                'normalized_id': str(pseudo_cid),
                'cid': pseudo_cid,
                'original_format': format_info['format'],
                'original_id': place_id,
                'is_cid': False,
                'note': 'Pseudo-CID for unknown format'
            }

        # Completely unknown
        return {
            'normalized_id': None,
            'cid': None,
            'original_format': 'unknown',
            'original_id': place_id,
            'is_cid': False
        }

    @staticmethod
    def is_valid_place_id(place_id):
        """
        Check if a Place ID is valid (any format).
        """
        format_info = PlaceIDConverter.identify_format(place_id)
        return format_info['format'] != 'unknown'

    @staticmethod
    def get_place_url(place_id):
        """
        Generate a Google Maps URL from any Place ID format.
        """
        if not place_id:
            return None

        format_info = PlaceIDConverter.identify_format(place_id)

        # Standard formats can be used directly
        if format_info.get('standard'):
            return f"https://www.google.com/maps/place/?q=place_id:{place_id}"

        # Hex format - use as ftid parameter
        if format_info['format'] == 'hex':
            return f"https://www.google.com/maps/search/?api=1&ftid={place_id}"

        # CID format
        if format_info['format'] == 'cid':
            return f"https://www.google.com/maps?cid={place_id}"

        # Unknown - try as query
        return f"https://www.google.com/maps/search/{place_id}"


# Utility function for the main extractor
def enhance_place_id(place_id):
    """
    Enhance Place ID with CID normalization.
    All Place IDs are converted to CID format for consistency.
    """
    converter = PlaceIDConverter()

    format_info = converter.identify_format(place_id)
    normalized = converter.normalize_place_id(place_id)

    return {
        'raw': place_id,
        'format': format_info['format'],
        'cid': normalized.get('cid'),  # The CID (real or pseudo)
        'normalized': normalized['normalized_id'],  # CID as string
        'is_real_cid': normalized.get('is_cid', False),  # True if real CID
        'url': converter.get_place_url(normalized.get('cid') or place_id),
        'valid': converter.is_valid_place_id(place_id),
        'metadata': format_info
    }


# Example usage and testing
if __name__ == "__main__":
    # Test different Place ID formats
    test_ids = [
        "ChIJN1t_tDeuEmsRUsoyG83frY4",  # Standard ChIJ
        "GhIJQWDl0CIeQUARxks3icF8U8A",    # GhIJ format
        "0x89c25a31ebfbc6bf:0xb80ba2960244e4f4",  # Hex format
        "12345678901234567890",  # CID format
        "InvalidID!!!",  # Invalid
    ]

    converter = PlaceIDConverter()

    for test_id in test_ids:
        print(f"\n{'='*60}")
        print(f"Testing: {test_id}")
        print(f"{'='*60}")

        # Identify format
        format_info = converter.identify_format(test_id)
        print(f"Format: {format_info}")

        # Normalize
        normalized = converter.normalize_place_id(test_id)
        print(f"Normalized: {normalized}")

        # Get URL
        url = converter.get_place_url(test_id)
        print(f"URL: {url}")

        # If hex, show conversion
        if format_info['format'] == 'hex':
            hex_info = converter.hex_to_cid(test_id)
            print(f"Hex conversion: {hex_info}")