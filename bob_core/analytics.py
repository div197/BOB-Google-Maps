"""bob_core.analytics

Business intelligence and analytics for scraped Google Maps data.
"""
from __future__ import annotations

import re
from typing import List, Dict, Any, Optional, Tuple
from collections import Counter, defaultdict
from statistics import mean, median

try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False

__all__ = [
    "ReviewAnalyzer",
    "BusinessAnalyzer", 
    "MarketAnalyzer",
    "SentimentScore"
]


class SentimentScore:
    """Sentiment analysis result."""
    
    def __init__(self, polarity: float, subjectivity: float):
        self.polarity = polarity  # -1 (negative) to 1 (positive)
        self.subjectivity = subjectivity  # 0 (objective) to 1 (subjective)
    
    @property
    def sentiment_label(self) -> str:
        """Human-readable sentiment label."""
        if self.polarity > 0.1:
            return "positive"
        elif self.polarity < -0.1:
            return "negative"
        else:
            return "neutral"


class ReviewAnalyzer:
    """Analyze review data for insights."""
    
    def __init__(self, reviews: List[Dict[str, Any]]):
        self.reviews = reviews
    
    def sentiment_analysis(self) -> Dict[str, Any]:
        """Analyze sentiment of all reviews."""
        if not TEXTBLOB_AVAILABLE:
            return {"error": "TextBlob not available for sentiment analysis"}
        
        sentiments = []
        for review in self.reviews:
            content = review.get("content", "")
            if content:
                blob = TextBlob(content)
                sentiments.append(SentimentScore(blob.sentiment.polarity, blob.sentiment.subjectivity))
        
        if not sentiments:
            return {"sentiment": "no_data"}
        
        avg_polarity = mean(s.polarity for s in sentiments)
        avg_subjectivity = mean(s.subjectivity for s in sentiments)
        
        sentiment_counts = Counter(s.sentiment_label for s in sentiments)
        
        return {
            "average_polarity": avg_polarity,
            "average_subjectivity": avg_subjectivity,
            "overall_sentiment": SentimentScore(avg_polarity, avg_subjectivity).sentiment_label,
            "sentiment_distribution": dict(sentiment_counts),
            "total_reviews_analyzed": len(sentiments)
        }
    
    def rating_analysis(self) -> Dict[str, Any]:
        """Analyze rating distribution."""
        ratings = []
        for review in self.reviews:
            rating_text = review.get("rating", "")
            # Extract numeric rating
            match = re.search(r'(\d+)', rating_text)
            if match:
                ratings.append(int(match.group(1)))
        
        if not ratings:
            return {"rating": "no_data"}
        
        rating_counts = Counter(ratings)
        
        return {
            "average_rating": mean(ratings),
            "median_rating": median(ratings),
            "rating_distribution": dict(rating_counts),
            "total_ratings": len(ratings),
            "five_star_percentage": (rating_counts.get(5, 0) / len(ratings)) * 100,
            "one_star_percentage": (rating_counts.get(1, 0) / len(ratings)) * 100
        }
    
    def keyword_analysis(self, top_n: int = 20) -> Dict[str, Any]:
        """Extract most common keywords from reviews."""
        all_text = " ".join(review.get("content", "") for review in self.reviews)
        
        # Simple keyword extraction (remove common words)
        stop_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", 
            "of", "with", "by", "is", "was", "are", "were", "be", "been", "have",
            "has", "had", "do", "does", "did", "will", "would", "could", "should",
            "this", "that", "these", "those", "i", "you", "he", "she", "it", "we", "they"
        }
        
        words = re.findall(r'\b[a-zA-Z]{3,}\b', all_text.lower())
        filtered_words = [w for w in words if w not in stop_words]
        
        word_counts = Counter(filtered_words)
        
        return {
            "top_keywords": dict(word_counts.most_common(top_n)),
            "total_words": len(filtered_words),
            "unique_words": len(word_counts)
        }


class BusinessAnalyzer:
    """Analyze individual business data."""
    
    def __init__(self, business_data: Dict[str, Any]):
        self.business_data = business_data
        self.business_info = business_data.get("business_info", {})
        self.reviews = business_data.get("reviews", [])
    
    def overall_score(self) -> Dict[str, Any]:
        """Calculate overall business health score."""
        score = 0
        factors = {}
        
        # Rating factor (40% weight)
        rating_text = self.business_info.get("rating", "")
        rating_match = re.search(r'(\d+\.?\d*)', rating_text)
        if rating_match:
            rating = float(rating_match.group(1))
            rating_score = (rating / 5.0) * 40
            score += rating_score
            factors["rating_score"] = rating_score
        
        # Review count factor (30% weight)
        review_count = len(self.reviews)
        if review_count > 100:
            review_score = 30
        elif review_count > 50:
            review_score = 25
        elif review_count > 20:
            review_score = 20
        elif review_count > 5:
            review_score = 15
        else:
            review_score = 10
        
        score += review_score
        factors["review_count_score"] = review_score
        
        # Sentiment factor (20% weight)
        if self.reviews:
            analyzer = ReviewAnalyzer(self.reviews)
            sentiment = analyzer.sentiment_analysis()
            if "average_polarity" in sentiment:
                # Convert polarity (-1 to 1) to score (0 to 20)
                sentiment_score = (sentiment["average_polarity"] + 1) * 10
                score += sentiment_score
                factors["sentiment_score"] = sentiment_score
        
        # Information completeness (10% weight)
        info_fields = ["name", "address", "phone", "website", "category"]
        complete_fields = sum(1 for field in info_fields 
                            if self.business_info.get(field, "Unknown") not in ["Unknown", "Unavailable"])
        completeness_score = (complete_fields / len(info_fields)) * 10
        score += completeness_score
        factors["completeness_score"] = completeness_score
        
        return {
            "overall_score": round(score, 2),
            "score_breakdown": factors,
            "grade": self._score_to_grade(score)
        }
    
    def _score_to_grade(self, score: float) -> str:
        """Convert numeric score to letter grade."""
        if score >= 90:
            return "A+"
        elif score >= 85:
            return "A"
        elif score >= 80:
            return "A-"
        elif score >= 75:
            return "B+"
        elif score >= 70:
            return "B"
        elif score >= 65:
            return "B-"
        elif score >= 60:
            return "C+"
        elif score >= 55:
            return "C"
        elif score >= 50:
            return "C-"
        else:
            return "F"


class MarketAnalyzer:
    """Analyze market trends across multiple businesses."""
    
    def __init__(self, businesses: List[Dict[str, Any]]):
        self.businesses = businesses
    
    def category_analysis(self) -> Dict[str, Any]:
        """Analyze business categories and their performance."""
        category_data = defaultdict(list)
        
        for business in self.businesses:
            category = business.get("business_info", {}).get("category", "Unknown")
            if category != "Unknown":
                analyzer = BusinessAnalyzer(business)
                score = analyzer.overall_score()
                category_data[category].append(score["overall_score"])
        
        category_stats = {}
        for category, scores in category_data.items():
            if scores:
                category_stats[category] = {
                    "average_score": mean(scores),
                    "business_count": len(scores),
                    "top_score": max(scores),
                    "bottom_score": min(scores)
                }
        
        # Sort by average score
        sorted_categories = sorted(category_stats.items(), 
                                 key=lambda x: x[1]["average_score"], 
                                 reverse=True)
        
        return {
            "category_rankings": dict(sorted_categories),
            "total_categories": len(category_stats),
            "total_businesses": len(self.businesses)
        }
    
    def market_opportunities(self) -> Dict[str, Any]:
        """Identify potential market opportunities."""
        opportunities = []
        
        # Low competition categories (few businesses)
        category_counts = Counter()
        category_scores = defaultdict(list)
        
        for business in self.businesses:
            category = business.get("business_info", {}).get("category", "Unknown")
            if category != "Unknown":
                category_counts[category] += 1
                analyzer = BusinessAnalyzer(business)
                score = analyzer.overall_score()
                category_scores[category].append(score["overall_score"])
        
        for category, count in category_counts.items():
            if count < 5:  # Low competition threshold
                avg_score = mean(category_scores[category]) if category_scores[category] else 0
                opportunities.append({
                    "category": category,
                    "business_count": count,
                    "average_score": avg_score,
                    "opportunity_type": "low_competition"
                })
        
        # Poor performance categories (low scores)
        for category, scores in category_scores.items():
            if scores and mean(scores) < 60:  # Poor performance threshold
                opportunities.append({
                    "category": category,
                    "business_count": len(scores),
                    "average_score": mean(scores),
                    "opportunity_type": "poor_performance"
                })
        
        return {
            "opportunities": opportunities,
            "total_opportunities": len(opportunities)
        } 