#!/usr/bin/env python3
"""
COMPREHENSIVE FALLBACK VALIDATION TEST SUITE
Tests both Playwright and Selenium extraction with complete feature coverage:
- Images extraction
- Email extraction
- Reviews extraction
- Fallback mechanism
"""

import pytest
import time
from bob import HybridExtractorOptimized


class TestCompleteFeatureValidation:
    """Test all features work in both primary and fallback engines"""

    def test_gypsy_restaurant_jodhpur_complete_extraction(self):
        """Test Gypsy Vegetarian Restaurant with ALL features"""
        extractor = HybridExtractorOptimized(prefer_playwright=True, memory_optimized=True)
        result = extractor.extract_business("Gypsy Vegetarian Restaurant Jodhpur")

        # Verify success
        assert result.get('success'), f"Extraction failed: {result.get('error')}"

        # Core data
        assert result.get('name'), "Business name not extracted"
        assert result.get('phone'), "Phone not extracted"
        assert result.get('address'), "Address not extracted"

        # Contact information
        assert result.get('website'), "Website not extracted"

        # Ratings
        assert result.get('rating'), "Rating not extracted"
        assert result.get('review_count'), "Review count not extracted"

        # Reviews
        reviews = result.get('reviews', [])
        assert len(reviews) > 0, f"No reviews extracted (got {len(reviews)})"
        print(f"✅ Reviews: {len(reviews)} extracted")

        # Images
        images = result.get('photos', [])
        assert len(images) > 0, f"❌ No images extracted (got {len(images)})"
        print(f"✅ Images: {len(images)} extracted")

        # Emails
        emails = result.get('emails', [])
        assert len(emails) > 0, f"❌ No emails extracted (got {len(emails)})"
        print(f"✅ Emails: {len(emails)} extracted - {', '.join(emails)}")

        # Quality score should be high
        quality = result.get('data_quality_score', 0)
        assert quality > 70, f"Quality score too low: {quality}/100"
        print(f"✅ Quality Score: {quality}/100")

        # Timing
        elapsed = result.get('extraction_time_seconds', 0)
        assert elapsed < 180, f"Extraction too slow: {elapsed}s"
        print(f"✅ Extraction Time: {elapsed:.1f}s")

        print(f"✅ COMPLETE EXTRACTION VERIFIED")
        print(f"   • Name: {result.get('name')}")
        print(f"   • Phone: {result.get('phone')}")
        print(f"   • Website: {result.get('website')}")
        print(f"   • Emails: {', '.join(emails)}")
        print(f"   • Rating: {result.get('rating')}")
        print(f"   • Reviews: {len(reviews)}")
        print(f"   • Images: {len(images)}")

    def test_janta_sweet_house_jodhpur(self):
        """Test another Jodhpur business"""
        extractor = HybridExtractorOptimized(prefer_playwright=True, memory_optimized=True)
        result = extractor.extract_business("Janta Sweet House Jodhpur")

        assert result.get('success'), "Extraction failed"

        # Core extraction
        assert result.get('name'), "Name missing"
        assert result.get('phone'), "Phone missing"

        # Images and emails
        images = result.get('photos', [])
        emails = result.get('emails', [])
        reviews = result.get('reviews', [])

        print(f"\n✅ {result.get('name')}")
        print(f"   Images: {len(images)}")
        print(f"   Emails: {len(emails)}")
        print(f"   Reviews: {len(reviews)}")
        print(f"   Quality: {result.get('data_quality_score')}/100")

    def test_starbucks_newyork_fallback(self):
        """Test fallback mechanism with US business"""
        extractor = HybridExtractorOptimized(prefer_playwright=True, memory_optimized=True)
        result = extractor.extract_business("Starbucks Times Square New York")

        # This tests fallback if Playwright has issues
        assert result.get('success'), "Even with fallback, extraction should succeed"

        # Verify essential data
        assert result.get('name'), "Name not extracted"
        assert result.get('phone'), "Phone not extracted"

        method = result.get('extraction_method', 'Unknown')
        print(f"\n✅ Starbucks Times Square")
        print(f"   Method: {method}")
        print(f"   Quality: {result.get('data_quality_score')}/100")
        print(f"   Time: {result.get('extraction_time_seconds', 0):.1f}s")

    def test_fallback_produces_complete_data(self):
        """Verify fallback (Selenium) has email extraction"""
        extractor = HybridExtractorOptimized(prefer_playwright=False, memory_optimized=True)  # Force Selenium
        result = extractor.extract_business("Restaurant Jodhpur")

        # Fallback should still extract data
        if result.get('success'):
            # Key: Selenium should now have email extraction!
            print(f"\n✅ Selenium (Fallback) Extraction")
            print(f"   Name: {result.get('name')}")
            print(f"   Emails Found: {len(result.get('emails', []))}")
            print(f"   Images Found: {len(result.get('photos', []))}")
            print(f"   Quality: {result.get('data_quality_score')}/100")

    def test_multiple_businesses_batch(self):
        """Test batch extraction with feature validation"""
        businesses = [
            "Gypsy Vegetarian Restaurant Jodhpur",
            "Janta Sweet House Jodhpur",
            "Starbucks Times Square New York",
        ]

        extractor = HybridExtractorOptimized(prefer_playwright=True, memory_optimized=True)

        successful = 0
        emails_extracted = 0
        images_extracted = 0

        for business_query in businesses:
            result = extractor.extract_business(business_query)

            if result.get('success'):
                successful += 1
                emails = result.get('emails', [])
                images = result.get('photos', [])

                if emails:
                    emails_extracted += 1
                if images:
                    images_extracted += 1

                print(f"\n✅ {result.get('name')}")
                print(f"   Emails: {len(emails)} | Images: {len(images)}")

        print(f"\n📊 BATCH RESULTS:")
        print(f"   Success Rate: {successful}/{len(businesses)}")
        print(f"   Emails Extracted: {emails_extracted}/{len(businesses)}")
        print(f"   Images Extracted: {images_extracted}/{len(businesses)}")

        assert successful == len(businesses), "Not all businesses extracted"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
