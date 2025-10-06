"""
BOB Google Maps V3.0 - Data Models Unit Tests
Author: Divyanshu Singh Chouhan
Release: October 3, 2025

Real tests for Business, Review, and Image data models.
"""

import pytest
from datetime import datetime
from bob.models import Business, Review, Image


class TestBusinessModel:
    """Test suite for Business data model."""

    def test_business_creation(self):
        """Test creating a Business instance."""
        business = Business(
            place_id="ChIJ123",
            cid=456789,
            name="Test Restaurant",
            phone="+1-234-567-8900",
            address="123 Main St, New York, NY",
            latitude=40.7128,
            longitude=-74.0060,
            category="Restaurant",
            rating=4.5,
            review_count=100
        )

        assert business.name == "Test Restaurant"
        assert business.phone == "+1-234-567-8900"
        assert business.rating == 4.5
        assert business.latitude == 40.7128
        assert business.longitude == -74.0060

    def test_business_to_dict(self):
        """Test Business to_dict() method."""
        business = Business(
            name="Test Cafe",
            phone="+1-555-1234",
            rating=4.2
        )

        data = business.to_dict()

        assert isinstance(data, dict)
        assert data['name'] == "Test Cafe"
        assert data['phone'] == "+1-555-1234"
        assert data['rating'] == 4.2
        assert 'extracted_at' in data

    def test_business_from_dict(self):
        """Test Business from_dict() method."""
        data = {
            'name': 'Test Store',
            'phone': '+1-555-5678',
            'rating': 4.0,
            'address': '456 Oak Ave',
            'latitude': 34.0522,
            'longitude': -118.2437
        }

        business = Business.from_dict(data)

        assert business.name == 'Test Store'
        assert business.phone == '+1-555-5678'
        assert business.rating == 4.0
        assert business.address == '456 Oak Ave'

    def test_quality_score_calculation(self):
        """Test data quality score calculation."""
        # High quality business with many fields
        business_high = Business(
            place_id="ChIJ123",
            cid=456789,
            name="Complete Business",
            phone="+1-234-567-8900",
            address="123 Main St",
            latitude=40.7128,
            longitude=-74.0060,
            category="Restaurant",
            rating=4.5,
            review_count=100,
            website="https://example.com",
            hours="Mon-Fri: 9AM-5PM"
        )
        business_high.photos = ["url1", "url2", "url3"]
        business_high.reviews = [Review(reviewer="John", rating=5, text="Great!")]

        score_high = business_high.calculate_quality_score()

        # Low quality business with minimal fields
        business_low = Business(
            name="Minimal Business"
        )

        score_low = business_low.calculate_quality_score()

        assert score_high > score_low
        assert score_high >= 70
        assert score_low < 50

    def test_empty_business(self):
        """Test creating empty Business instance."""
        business = Business()

        assert business.name is None
        assert business.phone is None
        assert business.rating is None
        assert business.photos == []
        assert business.reviews == []
        assert business.data_quality_score == 0


class TestReviewModel:
    """Test suite for Review data model."""

    def test_review_creation(self):
        """Test creating a Review instance."""
        review = Review(
            reviewer="John Doe",
            rating=5,
            text="Excellent service!",
            date="2 days ago"
        )

        assert review.reviewer == "John Doe"
        assert review.rating == 5
        assert review.text == "Excellent service!"
        assert review.date == "2 days ago"

    def test_review_to_dict(self):
        """Test Review to_dict() method."""
        review = Review(
            reviewer="Jane Smith",
            rating=4,
            text="Good experience",
            date="1 week ago"
        )

        data = review.to_dict()

        assert isinstance(data, dict)
        assert data['reviewer'] == "Jane Smith"
        assert data['rating'] == 4
        assert data['text'] == "Good experience"

    def test_review_from_dict(self):
        """Test Review from_dict() method."""
        data = {
            'reviewer': 'Bob Johnson',
            'rating': 3,
            'text': 'Average',
            'date': '3 weeks ago'
        }

        review = Review.from_dict(data)

        assert review.reviewer == 'Bob Johnson'
        assert review.rating == 3
        assert review.text == 'Average'


class TestImageModel:
    """Test suite for Image data model."""

    def test_image_creation(self):
        """Test creating an Image instance."""
        image = Image(
            url="https://example.com/image.jpg",
            thumbnail="https://example.com/thumb.jpg",
            width=1920,
            height=1080
        )

        assert image.url == "https://example.com/image.jpg"
        assert image.thumbnail == "https://example.com/thumb.jpg"
        assert image.width == 1920
        assert image.height == 1080

    def test_image_to_dict(self):
        """Test Image to_dict() method."""
        image = Image(
            url="https://example.com/photo.jpg",
            width=800,
            height=600
        )

        data = image.to_dict()

        assert isinstance(data, dict)
        assert data['url'] == "https://example.com/photo.jpg"
        assert data['width'] == 800
        assert data['height'] == 600

    def test_image_from_dict(self):
        """Test Image from_dict() method."""
        data = {
            'url': 'https://example.com/pic.jpg',
            'thumbnail': 'https://example.com/pic_thumb.jpg',
            'width': 1024,
            'height': 768
        }

        image = Image.from_dict(data)

        assert image.url == 'https://example.com/pic.jpg'
        assert image.thumbnail == 'https://example.com/pic_thumb.jpg'
        assert image.width == 1024
