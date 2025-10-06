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
    place_id_original: Optional[str] = None  # Original format before conversion
    place_id_confidence: Optional[str] = None  # HIGH/MEDIUM/LOW
    place_id_format: Optional[str] = None  # hex/ChIJ/cid
    is_real_cid: Optional[bool] = False  # True if real CID, False if pseudo-CID
    place_id_url: Optional[str] = None  # Direct Google Maps URL

    # Basic info
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    emails: List[str] = field(default_factory=list)  # Email addresses from website

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
    current_status: Optional[str] = None  # Open/Closed now
    price_range: Optional[str] = None

    # Service Options
    service_options: Dict[str, bool] = field(default_factory=dict)  # dine_in, takeout, delivery

    # Rich data
    attributes: List[str] = field(default_factory=list)
    photos: List[str] = field(default_factory=list)
    reviews: List[Any] = field(default_factory=list)
    popular_times: Dict[str, Any] = field(default_factory=dict)  # Popular times by day
    social_media: Dict[str, str] = field(default_factory=dict)  # Social media links
    menu_items: List[str] = field(default_factory=list)  # Menu items for restaurants

    # Metadata
    extracted_at: datetime = field(default_factory=datetime.now)
    data_quality_score: int = 0
    extraction_method: str = "unknown"
    extraction_time_seconds: Optional[float] = None
    extractor_version: str = "3.3.0"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            # Core identification
            "place_id": self.place_id,
            "cid": self.cid,
            "place_id_original": self.place_id_original,
            "place_id_confidence": self.place_id_confidence,
            "place_id_format": self.place_id_format,
            "is_real_cid": self.is_real_cid,
            "place_id_url": self.place_id_url,
            # Basic info
            "name": self.name,
            "phone": self.phone,
            "address": self.address,
            "emails": self.emails,
            # Location
            "latitude": self.latitude,
            "longitude": self.longitude,
            "plus_code": self.plus_code,
            # Business details
            "category": self.category,
            "rating": self.rating,
            "review_count": self.review_count,
            "website": self.website,
            "hours": self.hours,
            "current_status": self.current_status,
            "price_range": self.price_range,
            # Service options
            "service_options": self.service_options,
            # Rich data
            "attributes": self.attributes,
            "photos": self.photos,
            "reviews": [r if isinstance(r, dict) else r.__dict__ for r in self.reviews],
            "popular_times": self.popular_times,
            "social_media": self.social_media,
            "menu_items": self.menu_items,
            # Metadata
            "extracted_at": self.extracted_at.isoformat(),
            "data_quality_score": self.data_quality_score,
            "extraction_method": self.extraction_method,
            "extraction_time_seconds": self.extraction_time_seconds,
            "extractor_version": self.extractor_version,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Business":
        """Create Business object from dictionary."""
        if "extracted_at" in data and isinstance(data["extracted_at"], str):
            data["extracted_at"] = datetime.fromisoformat(data["extracted_at"])
        return cls(**data)

    def calculate_quality_score(self) -> int:
        """Calculate data quality score (0-100) - V3.3 Enhanced."""
        score = 0

        # Essential fields (35 points)
        if self.name: score += 10
        if self.address: score += 8
        if self.latitude and self.longitude: score += 9
        if self.phone: score += 8

        # Important identifiers (20 points)
        if self.cid: score += 10  # Critical for direct links
        if self.place_id: score += 5
        if self.place_id_url: score += 5

        # Business details (25 points)
        if self.rating is not None: score += 10  # Critical missing field
        if self.category: score += 5
        if self.website: score += 5
        if self.hours: score += 3
        if self.price_range: score += 2

        # Contact & Service (10 points)
        if self.emails: score += 5  # Critical missing field
        if self.service_options: score += 3
        if self.plus_code: score += 2

        # Rich content (10 points)
        if self.photos:
            photo_score = min(len(self.photos), 5) * 1.5  # Up to 7.5 points for photos
            score += int(photo_score)
        if self.reviews:
            review_score = min(len(self.reviews), 5) * 0.5  # Up to 2.5 points for reviews
            score += int(review_score)

        self.data_quality_score = min(score, 100)
        return self.data_quality_score
