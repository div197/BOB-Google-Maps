"""
Business Data Model - BOB V3.0
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime


@dataclass
class Business:
    """
    Business data model with comprehensive fields.

    Attributes:
        place_id: Google Place ID
        cid: Google Customer ID
        name: Business name
        phone: Contact phone number
        address: Full address
        latitude: GPS latitude
        longitude: GPS longitude
        category: Business category
        rating: Star rating (0-5)
        review_count: Total number of reviews
        website: Business website URL
        hours: Operating hours
        price_range: Price range indicator
        attributes: List of business attributes
        photos: List of photo URLs
        reviews: List of Review objects
        extracted_at: Extraction timestamp
        data_quality_score: Quality score (0-100)
        metadata: Additional metadata
    """

    # Core identification
    place_id: Optional[str] = None
    cid: Optional[int] = None

    # Basic info
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

    # Location
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    plus_code: Optional[str] = None

    # Business details
    category: Optional[str] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    website: Optional[str] = None
    hours: Optional[str] = None
    price_range: Optional[str] = None

    # Rich data
    attributes: List[str] = field(default_factory=list)
    photos: List[str] = field(default_factory=list)
    reviews: List[Any] = field(default_factory=list)

    # Metadata
    extracted_at: datetime = field(default_factory=datetime.now)
    data_quality_score: int = 0
    extraction_method: str = "unknown"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "place_id": self.place_id,
            "cid": self.cid,
            "name": self.name,
            "phone": self.phone,
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "plus_code": self.plus_code,
            "category": self.category,
            "rating": self.rating,
            "review_count": self.review_count,
            "website": self.website,
            "hours": self.hours,
            "price_range": self.price_range,
            "attributes": self.attributes,
            "photos": self.photos,
            "reviews": [r if isinstance(r, dict) else r.__dict__ for r in self.reviews],
            "extracted_at": self.extracted_at.isoformat(),
            "data_quality_score": self.data_quality_score,
            "extraction_method": self.extraction_method,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Business":
        """Create Business object from dictionary."""
        if "extracted_at" in data and isinstance(data["extracted_at"], str):
            data["extracted_at"] = datetime.fromisoformat(data["extracted_at"])
        return cls(**data)

    def calculate_quality_score(self) -> int:
        """Calculate data quality score (0-100)."""
        score = 0

        # Critical fields (50 points)
        if self.name: score += 15
        if self.phone: score += 10
        if self.address: score += 10
        if self.latitude: score += 8
        if self.longitude: score += 7

        # Important fields (30 points)
        if self.category: score += 8
        if self.rating: score += 7
        if self.hours: score += 7
        if self.website: score += 8

        # Bonus (20 points)
        if self.photos: score += min(len(self.photos) * 2, 10)
        if self.reviews: score += min(len(self.reviews) * 2, 10)

        self.data_quality_score = min(score, 100)
        return self.data_quality_score
