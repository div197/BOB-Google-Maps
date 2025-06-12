"""bob_api.services.analytics_service

Analytics Service for BOB Google Maps API v0.6.0
Divine analytics implementation following Niṣkāma Karma Yoga principles.

Made with 🙏 for interconnected excellence
"""

import asyncio
import time
import statistics
from typing import Dict, Any, List, Optional
from collections import Counter, defaultdict

from .interfaces import AnalyticsService, CacheService, MetricsService
from bob_core import analyze_business_data


class AnalyticsServiceImpl(AnalyticsService):
    """Divine analytics service implementation."""
    
    def __init__(
        self,
        cache_service: Optional[CacheService] = None,
        metrics_service: Optional[MetricsService] = None
    ):
        self.cache_service = cache_service
        self.metrics_service = metrics_service
        self._initialized = False
    
    async def initialize(self):
        """Initialize the analytics service."""
        if self._initialized:
            return
        
        self._initialized = True
    
    async def analyze_business(self, business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze business data with divine insights."""
        try:
            # Check cache first
            cache_key = f"analytics:business:{hash(str(business_data))}"
            if self.cache_service:
                cached_result = await self.cache_service.get(cache_key)
                if cached_result:
                    return cached_result
            
            # Use BOB Core analytics
            core_analysis = analyze_business_data(business_data)
            
            # Enhanced analytics
            enhanced_analysis = await self._enhance_business_analysis(business_data, core_analysis)
            
            # Cache the result
            if self.cache_service:
                await self.cache_service.set(cache_key, enhanced_analysis, ttl=1800)  # 30 minutes
            
            return enhanced_analysis
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": time.time()
            }
    
    async def analyze_reviews(self, reviews: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze reviews with sentiment analysis."""
        try:
            if not reviews:
                return {
                    "total_reviews": 0,
                    "sentiment": {"positive": 0, "neutral": 0, "negative": 0},
                    "insights": []
                }
            
            # Basic sentiment analysis
            sentiment_scores = []
            rating_distribution = Counter()
            keyword_frequency = Counter()
            monthly_trends = defaultdict(int)
            
            for review in reviews:
                # Rating analysis
                rating = review.get('rating', 0)
                if rating:
                    rating_distribution[rating] += 1
                    
                    # Simple sentiment scoring
                    if rating >= 4:
                        sentiment_scores.append(1)  # Positive
                    elif rating >= 3:
                        sentiment_scores.append(0)  # Neutral
                    else:
                        sentiment_scores.append(-1)  # Negative
                
                # Text analysis
                text = review.get('text', '').lower()
                if text:
                    # Extract keywords (simple approach)
                    words = text.split()
                    for word in words:
                        if len(word) > 3:  # Filter short words
                            keyword_frequency[word] += 1
                
                # Time trends
                date = review.get('date')
                if date:
                    try:
                        # Extract month-year for trending
                        month_year = date[:7] if len(date) >= 7 else date
                        monthly_trends[month_year] += 1
                    except:
                        pass
            
            # Calculate sentiment distribution
            total_sentiment = len(sentiment_scores)
            sentiment_distribution = {
                "positive": sentiment_scores.count(1) / total_sentiment if total_sentiment > 0 else 0,
                "neutral": sentiment_scores.count(0) / total_sentiment if total_sentiment > 0 else 0,
                "negative": sentiment_scores.count(-1) / total_sentiment if total_sentiment > 0 else 0
            }
            
            # Generate insights
            insights = await self._generate_review_insights(
                reviews, rating_distribution, sentiment_distribution, keyword_frequency
            )
            
            return {
                "total_reviews": len(reviews),
                "average_rating": statistics.mean([r.get('rating', 0) for r in reviews if r.get('rating')]) if reviews else 0,
                "rating_distribution": dict(rating_distribution),
                "sentiment": sentiment_distribution,
                "top_keywords": dict(keyword_frequency.most_common(10)),
                "monthly_trends": dict(monthly_trends),
                "insights": insights,
                "timestamp": time.time()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": time.time()
            }
    
    async def generate_market_insights(self, businesses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate market insights from multiple businesses."""
        try:
            if not businesses:
                return {"insights": [], "market_summary": {}}
            
            # Market analysis
            categories = Counter()
            locations = Counter()
            rating_stats = []
            price_levels = Counter()
            
            for business in businesses:
                # Category analysis
                category = business.get('category', 'Unknown')
                categories[category] += 1
                
                # Location analysis
                location = business.get('address', {}).get('city', 'Unknown')
                locations[location] += 1
                
                # Rating analysis
                rating = business.get('rating')
                if rating:
                    rating_stats.append(float(rating))
                
                # Price level analysis
                price_level = business.get('price_level', 'Unknown')
                price_levels[price_level] += 1
            
            # Calculate market statistics
            market_summary = {
                "total_businesses": len(businesses),
                "top_categories": dict(categories.most_common(5)),
                "top_locations": dict(locations.most_common(5)),
                "average_rating": statistics.mean(rating_stats) if rating_stats else 0,
                "rating_std": statistics.stdev(rating_stats) if len(rating_stats) > 1 else 0,
                "price_distribution": dict(price_levels)
            }
            
            # Generate insights
            insights = await self._generate_market_insights(market_summary, businesses)
            
            return {
                "market_summary": market_summary,
                "insights": insights,
                "competitive_analysis": await self._analyze_competition(businesses),
                "timestamp": time.time()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": time.time()
            }
    
    async def calculate_business_score(self, business_data: Dict[str, Any]) -> float:
        """Calculate overall business score."""
        try:
            score = 0.0
            max_score = 100.0
            
            # Rating score (40% weight)
            rating = business_data.get('rating', 0)
            if rating:
                score += (float(rating) / 5.0) * 40
            
            # Review count score (20% weight)
            review_count = business_data.get('review_count', 0)
            if review_count:
                # Logarithmic scaling for review count
                import math
                review_score = min(math.log10(review_count + 1) * 10, 20)
                score += review_score
            
            # Business completeness score (20% weight)
            completeness_factors = [
                business_data.get('name'),
                business_data.get('address'),
                business_data.get('phone'),
                business_data.get('website'),
                business_data.get('hours')
            ]
            completeness = sum(1 for factor in completeness_factors if factor) / len(completeness_factors)
            score += completeness * 20
            
            # Photo count score (10% weight)
            photo_count = len(business_data.get('photos', []))
            photo_score = min(photo_count / 10 * 10, 10)  # Max 10 points for 10+ photos
            score += photo_score
            
            # Engagement score (10% weight)
            # Based on recent reviews, responses to reviews, etc.
            engagement_score = 5  # Base score
            if business_data.get('responds_to_reviews'):
                engagement_score += 3
            if business_data.get('recent_activity'):
                engagement_score += 2
            score += min(engagement_score, 10)
            
            return min(score, max_score)
            
        except Exception as e:
            return 0.0
    
    async def _enhance_business_analysis(self, business_data: Dict[str, Any], core_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance business analysis with additional insights."""
        enhanced = core_analysis.copy()
        
        # Calculate business score
        business_score = await self.calculate_business_score(business_data)
        enhanced['business_score'] = business_score
        
        # Add competitive positioning
        enhanced['competitive_position'] = await self._assess_competitive_position(business_data)
        
        # Add growth indicators
        enhanced['growth_indicators'] = await self._analyze_growth_indicators(business_data)
        
        # Add recommendations
        enhanced['recommendations'] = await self._generate_business_recommendations(business_data, business_score)
        
        return enhanced
    
    async def _generate_review_insights(
        self, 
        reviews: List[Dict[str, Any]], 
        rating_distribution: Counter,
        sentiment_distribution: Dict[str, float],
        keyword_frequency: Counter
    ) -> List[str]:
        """Generate insights from review analysis."""
        insights = []
        
        # Rating insights
        if rating_distribution:
            avg_rating = sum(rating * count for rating, count in rating_distribution.items()) / sum(rating_distribution.values())
            if avg_rating >= 4.5:
                insights.append("Excellent customer satisfaction with consistently high ratings")
            elif avg_rating >= 4.0:
                insights.append("Good customer satisfaction with mostly positive reviews")
            elif avg_rating >= 3.0:
                insights.append("Mixed customer feedback - room for improvement")
            else:
                insights.append("Poor customer satisfaction - immediate attention needed")
        
        # Sentiment insights
        if sentiment_distribution['positive'] > 0.7:
            insights.append("Overwhelmingly positive customer sentiment")
        elif sentiment_distribution['negative'] > 0.3:
            insights.append("Significant negative sentiment detected - investigate common issues")
        
        # Keyword insights
        top_keywords = keyword_frequency.most_common(5)
        if top_keywords:
            positive_keywords = ['great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'best']
            negative_keywords = ['bad', 'terrible', 'awful', 'worst', 'horrible', 'disappointing']
            
            for keyword, count in top_keywords:
                if keyword in positive_keywords:
                    insights.append(f"Customers frequently mention '{keyword}' positively")
                elif keyword in negative_keywords:
                    insights.append(f"Customers frequently mention '{keyword}' negatively - needs attention")
        
        return insights
    
    async def _generate_market_insights(self, market_summary: Dict[str, Any], businesses: List[Dict[str, Any]]) -> List[str]:
        """Generate market insights."""
        insights = []
        
        # Category insights
        top_categories = market_summary.get('top_categories', {})
        if top_categories:
            dominant_category = max(top_categories, key=top_categories.get)
            insights.append(f"Market dominated by {dominant_category} businesses ({top_categories[dominant_category]} out of {market_summary['total_businesses']})")
        
        # Rating insights
        avg_rating = market_summary.get('average_rating', 0)
        if avg_rating >= 4.0:
            insights.append("High-quality market with above-average customer satisfaction")
        elif avg_rating < 3.5:
            insights.append("Market opportunity exists - many businesses have room for improvement")
        
        # Competition insights
        total_businesses = market_summary['total_businesses']
        if total_businesses > 50:
            insights.append("Highly competitive market with many established players")
        elif total_businesses < 10:
            insights.append("Emerging market with limited competition - good opportunity for new entrants")
        
        return insights
    
    async def _analyze_competition(self, businesses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze competitive landscape."""
        if not businesses:
            return {}
        
        # Sort by rating and review count
        sorted_businesses = sorted(
            businesses,
            key=lambda b: (b.get('rating', 0) * b.get('review_count', 0)),
            reverse=True
        )
        
        return {
            "market_leaders": sorted_businesses[:3],
            "average_competitors": sorted_businesses[len(sorted_businesses)//3:2*len(sorted_businesses)//3],
            "underperformers": sorted_businesses[-3:],
            "competitive_intensity": "High" if len(businesses) > 20 else "Medium" if len(businesses) > 10 else "Low"
        }
    
    async def _assess_competitive_position(self, business_data: Dict[str, Any]) -> str:
        """Assess competitive position of a business."""
        rating = business_data.get('rating', 0)
        review_count = business_data.get('review_count', 0)
        
        if rating >= 4.5 and review_count >= 100:
            return "Market Leader"
        elif rating >= 4.0 and review_count >= 50:
            return "Strong Competitor"
        elif rating >= 3.5:
            return "Average Performer"
        else:
            return "Needs Improvement"
    
    async def _analyze_growth_indicators(self, business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze growth indicators."""
        indicators = {
            "recent_reviews": len([r for r in business_data.get('reviews', []) if self._is_recent_review(r)]),
            "photo_activity": len(business_data.get('photos', [])),
            "business_completeness": self._calculate_completeness(business_data),
            "engagement_level": "High" if business_data.get('responds_to_reviews') else "Low"
        }
        
        return indicators
    
    async def _generate_business_recommendations(self, business_data: Dict[str, Any], business_score: float) -> List[str]:
        """Generate business improvement recommendations."""
        recommendations = []
        
        if business_score < 50:
            recommendations.append("Focus on improving customer service and addressing negative reviews")
        
        if not business_data.get('website'):
            recommendations.append("Create a professional website to improve online presence")
        
        if len(business_data.get('photos', [])) < 5:
            recommendations.append("Add more high-quality photos to attract customers")
        
        if business_data.get('review_count', 0) < 20:
            recommendations.append("Encourage satisfied customers to leave reviews")
        
        if not business_data.get('hours'):
            recommendations.append("Update business hours information for better customer experience")
        
        return recommendations
    
    def _is_recent_review(self, review: Dict[str, Any]) -> bool:
        """Check if review is recent (within last 6 months)."""
        try:
            review_date = review.get('date', '')
            # Simple check - in real implementation, would parse date properly
            return '2024' in review_date or '2023' in review_date
        except:
            return False
    
    def _calculate_completeness(self, business_data: Dict[str, Any]) -> float:
        """Calculate business profile completeness."""
        required_fields = ['name', 'address', 'phone', 'website', 'hours', 'category']
        completed = sum(1 for field in required_fields if business_data.get(field))
        return completed / len(required_fields)
    
    def is_healthy(self) -> bool:
        """Check if the service is healthy."""
        return self._initialized
    
    async def shutdown(self):
        """Shutdown the service gracefully."""
        self._initialized = False 