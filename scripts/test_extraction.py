#!/usr/bin/env python3
"""
Test script to understand BOB extraction result structure
"""

import json
from bob import HybridExtractorOptimized

def test_single_extraction():
    """Test extraction to understand the result structure."""
    extractor = HybridExtractorOptimized()

    # Test with a simple query
    result = extractor.extract_business("Emaar Properties Dubai")

    print("RESULT TYPE:", type(result))
    print("RESULT KEYS:", result.keys() if isinstance(result, dict) else "Not a dict")

    # Save result to file for inspection
    with open("test_result_structure.json", "w", encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print("Result saved to test_result_structure.json")

    # Print first few keys and values
    if isinstance(result, dict):
        for key, value in list(result.items())[:10]:
            print(f"Key: {key}, Value Type: {type(value)}, Value Preview: {str(value)[:100]}...")

if __name__ == "__main__":
    test_single_extraction()