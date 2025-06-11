"""Tests for analytics module."""

import pytest
from bob_core.analytics import BusinessAnalyzer, ReviewAnalyzer, MarketAnalyzer


def test_business_analyzer():
    """Test business scoring."""
    business_data = {
        "business_info": {
            "name": "Test Restaurant",
            "rating": "4.5 stars",
            "category": "Restaurant",
            "address": "123 Main St",
            "phone": "+1234567890",
            "website": "https://example.com"
        },
        "reviews": [
            {"content": "Great food!", "rating": "5 stars"},
            {"content": "Good service", "rating": "4 stars"}
        ]
    }
    
    analyzer = BusinessAnalyzer(business_data)
    score = analyzer.overall_score()
    
    assert "overall_score" in score
    assert "grade" in score
    assert score["overall_score"] > 0


def test_review_analyzer():
    """Test review analysis."""
    reviews = [
        {"content": "Amazing experience!", "rating": "5 stars"},
        {"content": "Terrible service", "rating": "1 star"},
        {"content": "Average food", "rating": "3 stars"}
    ]
    
    analyzer = ReviewAnalyzer(reviews)
    
    # Test rating analysis
    ratings = analyzer.rating_analysis()
    assert "average_rating" in ratings
    assert ratings["total_ratings"] == 3
    
    # Test keyword analysis
    keywords = analyzer.keyword_analysis()
    assert "top_keywords" in keywords


def test_market_analyzer():
    """Test market analysis."""
    businesses = [
        {
            "business_info": {"category": "Restaurant", "rating": "4.0 stars"},
            "reviews": []
        },
        {
            "business_info": {"category": "Restaurant", "rating": "3.5 stars"},
            "reviews": []
        },
        {
            "business_info": {"category": "Cafe", "rating": "4.5 stars"},
            "reviews": []
        }
    ]
    
    analyzer = MarketAnalyzer(businesses)
    
    # Test category analysis
    categories = analyzer.category_analysis()
    assert "category_rankings" in categories
    assert categories["total_businesses"] == 3
    
    # Test opportunities
    opportunities = analyzer.market_opportunities()
    assert "opportunities" in opportunities 