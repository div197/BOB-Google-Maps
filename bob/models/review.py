"""
Enhanced Review Data Model - BOB V1.2.0 (Nishkaam Karma Yoga Optimized)

State-of-the-Art review extraction with minimal resource usage and complete data capture.
Built with enlightened optimization principles for maximum efficiency through minimal consumption.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import datetime


@dataclass
class Review:
    """
    ENHANCED Review data model - State of the Art V1.2.0
    
    Nishkaam Karma Principles:
    1. Complete data extraction without attachment to storage
    2. Minimal memory footprint through enlightened design
    3. Comprehensive capture without resource waste
    4. Pure extraction process with zero cache dependency
    
    Attributes:
        Basic Review Information:
        - review_index: Position in review list
        - reviewer_name: Name of the reviewer
        - reviewer_photo: URL to reviewer profile picture
        - reviewer_total_reviews: Total reviews by this reviewer
        
        Rating Information:
        - rating: Star rating (1-5)
        - rating_text: Text representation of rating
        - rating_confidence: Confidence score for rating extraction
        
        Content Information:
        - review_text: Full review text content
        - text_length: Character count of review
        - text_language: Detected language of review
        
        Temporal Information:
        - review_date: Date of review
        - relative_time: Relative time (e.g., "2 weeks ago")
        - extracted_at: When this review was extracted
        
        Engagement Metrics:
        - helpful_count: Number of helpful votes
        - response_count: Number of responses
        - owner_response: Business owner's response
        
        Quality Metrics:
        - extraction_confidence: Overall confidence in data quality
        - data_completeness: Percentage of fields successfully extracted
        - extraction_method: Which engine/method extracted this
        
        Technical Metadata:
        - review_id: Unique identifier if available
        - source_element: DOM element source information
        - processing_time: Time taken to extract this review
    """

    # Basic Review Information
    review_index: int
    reviewer_name: Optional[str] = None
    reviewer_photo: Optional[str] = None
    reviewer_total_reviews: Optional[int] = None
    
    # Rating Information
    rating: Optional[int] = None  # 1-5 stars
    rating_text: Optional[str] = None  # "5 stars", "4.5 stars", etc.
    rating_confidence: Optional[float] = None  # 0-100 confidence score
    
    # Content Information
    review_text: Optional[str] = None
    text_length: Optional[int] = None
    text_language: Optional[str] = None
    
    # Temporal Information
    review_date: Optional[str] = None  # ISO format date
    relative_time: Optional[str] = None  # "2 weeks ago", etc.
    extracted_at: datetime = field(default_factory=datetime.now)
    
    # Engagement Metrics
    helpful_count: Optional[int] = None
    response_count: Optional[int] = None
    owner_response: Optional[str] = None
    
    # Quality Metrics
    extraction_confidence: Optional[float] = None  # 0-100
    data_completeness: Optional[float] = None  # 0-100 percentage
    extraction_method: Optional[str] = None  # "Playwright", "Selenium", etc.
    
    # Technical Metadata
    review_id: Optional[str] = None
    source_element: Optional[str] = None
    processing_time: Optional[float] = None  # milliseconds

    def __post_init__(self):
        """Post-initialization processing with Nishkaam Karma efficiency."""
        # Calculate text length if not provided
        if self.text_length is None and self.review_text:
            self.text_length = len(self.review_text)
        
        # Calculate data completeness automatically
        if self.data_completeness is None:
            self.data_completeness = self._calculate_completeness()
        
        # Set default extraction method if not provided
        if self.extraction_method is None:
            self.extraction_method = "Enhanced V1.2.0"

    def _calculate_completeness(self) -> float:
        """
        Calculate data completeness percentage (Nishkaam Karma optimized).
        
        Returns:
            float: Percentage of fields successfully filled (0-100)
        """
        total_fields = 15  # Total number of important fields
        filled_fields = 0
        
        # Check important fields
        important_fields = [
            self.reviewer_name,
            self.rating,
            self.review_text,
            self.review_date,
            self.helpful_count,
            self.reviewer_photo,
            self.reviewer_total_reviews,
            self.owner_response,
            self.rating_text,
            self.relative_time,
            self.review_id,
            self.text_language,
            self.rating_confidence,
            self.extraction_confidence,
            self.response_count
        ]
        
        for field in important_fields:
            if field is not None and field != "":
                filled_fields += 1
        
        return round((filled_fields / total_fields) * 100, 1)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary with Nishkaam Karma optimization.
        
        Returns:
            Dict[str, Any]: Dictionary representation with minimal memory usage
        """
        result = {}
        
        # Include all non-None fields for efficiency
        for key, value in self.__dict__.items():
            if value is not None:
                if isinstance(value, datetime):
                    result[key] = value.isoformat()
                else:
                    result[key] = value
        
        return result

    def get_quality_score(self) -> int:
        """
        Calculate overall quality score (0-100) following Nishkaam Karma principles.
        
        Returns:
            int: Quality score based on data completeness and accuracy
        """
        score = 0
        
        # Basic information (40 points)
        if self.reviewer_name: score += 10
        if self.rating: score += 15
        if self.review_text and len(self.review_text) > 10: score += 15
        
        # Enhanced information (30 points)
        if self.review_date: score += 10
        if self.helpful_count is not None: score += 10
        if self.reviewer_photo: score += 5
        if self.reviewer_total_reviews: score += 5
        
        # Advanced information (20 points)
        if self.owner_response: score += 10
        if self.rating_text: score += 5
        if self.relative_time: score += 5
        
        # Quality metrics (10 points)
        if self.extraction_confidence and self.extraction_confidence > 80: score += 5
        if self.data_completeness and self.data_completeness > 70: score += 5
        
        return min(score, 100)

    def is_high_quality(self) -> bool:
        """
        Determine if this is a high-quality review following Nishkaam Karma standards.
        
        Returns:
            bool: True if review meets quality threshold
        """
        return (self.get_quality_score() >= 70 and 
                self.review_text and len(self.review_text) > 20 and
                self.rating is not None)

    def __str__(self) -> str:
        """String representation with Nishkaam Karma efficiency."""
        name = self.reviewer_name or "Anonymous"
        rating = f"{self.rating}★" if self.rating else "No rating"
        text_preview = (self.review_text[:50] + "...") if self.review_text and len(self.review_text) > 50 else (self.review_text or "No text")
        
        return f"Review by {name} ({rating}): {text_preview}"

    def __repr__(self) -> str:
        """Detailed representation for debugging."""
        return (f"Review(index={self.review_index}, name='{self.reviewer_name}', "
                f"rating={self.rating}, quality={self.get_quality_score()})")


@dataclass
class ReviewSummary:
    """
    Review summary statistics - Nishkaam Karma optimized for minimal memory usage.
    
    Provides aggregated insights about extracted reviews without storing individual reviews.
    """

    total_reviews: int = 0
    average_rating: Optional[float] = None
    rating_distribution: Dict[int, int] = field(default_factory=dict)
    total_helpful_votes: int = 0
    reviews_with_responses: int = 0
    average_review_length: Optional[float] = None
    extraction_confidence: Optional[float] = None
    extraction_method: Optional[str] = None

    def add_review(self, review: Review) -> None:
        """
        Add a review to the summary with Nishkaam Karma efficiency.
        
        Args:
            review: Review to add to summary
        """
        self.total_reviews += 1
        
        # Update rating
        if review.rating is not None:
            if self.average_rating is None:
                self.average_rating = review.rating
            else:
                self.average_rating = ((self.average_rating * (self.total_reviews - 1)) + review.rating) / self.total_reviews
            
            # Update distribution
            if review.rating not in self.rating_distribution:
                self.rating_distribution[review.rating] = 0
            self.rating_distribution[review.rating] += 1
        
        # Update helpful votes
        if review.helpful_count:
            self.total_helpful_votes += review.helpful_count
        
        # Update response count
        if review.owner_response:
            self.reviews_with_responses += 1
        
        # Update average length
        if review.text_length:
            if self.average_review_length is None:
                self.average_review_length = review.text_length
            else:
                self.average_review_length = ((self.average_review_length * (self.total_reviews - 1)) + review.text_length) / self.total_reviews
        
        # Update extraction confidence
        if review.extraction_confidence:
            if self.extraction_confidence is None:
                self.extraction_confidence = review.extraction_confidence
            else:
                self.extraction_confidence = ((self.extraction_confidence * (self.total_reviews - 1)) + review.extraction_confidence) / self.total_reviews
        
        # Set extraction method
        if review.extraction_method and not self.extraction_method:
            self.extraction_method = review.extraction_method

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with minimal memory usage."""
        return {
            'total_reviews': self.total_reviews,
            'average_rating': round(self.average_rating, 2) if self.average_rating else None,
            'rating_distribution': self.rating_distribution,
            'total_helpful_votes': self.total_helpful_votes,
            'reviews_with_responses': self.reviews_with_responses,
            'average_review_length': round(self.average_review_length, 1) if self.average_review_length else None,
            'extraction_confidence': round(self.extraction_confidence, 1) if self.extraction_confidence else None,
            'extraction_method': self.extraction_method
        }
