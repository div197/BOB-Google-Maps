#!/usr/bin/env python3
"""
D Corner Living - Business Intelligence Entities

Core data models for business intelligence and lead scoring.
Designed for furniture manufacturer's B2B expansion strategy.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum


class BusinessType(Enum):
    """Business categories relevant to D Corner Living"""
    INTERIOR_DESIGNER = "interior_designer"
    FURNITURE_STORE = "furniture_store"
    OFFICE_FURNITURE = "office_furniture"
    FURNITURE_MANUFACTURER = "furniture_manufacturer"
    HOTEL_FURNITURE = "hotel_furniture"
    FURNITURE_DISTRIBUTOR = "furniture_distributor"
    REAL_ESTATE_DEVELOPER = "real_estate_developer"
    ARCHITECTURE_FIRM = "architecture_firm"


class BusinessSize(Enum):
    """Business size classification"""
    SMALL = "small"          # < 10 employees, < $100K revenue
    MEDIUM = "medium"        # 10-50 employees, $100K-1M revenue
    LARGE = "large"          # 50-200 employees, $1M-10M revenue
    ENTERPRISE = "enterprise" # >200 employees, >$10M revenue


class PotentialValue(Enum):
    """Potential value for D Corner Living"""
    LOW = "low"              # < $50K/year potential
    MEDIUM = "medium"        # $50K-200K/year potential
    HIGH = "high"            # $200K-500K/year potential
    CRITICAL = "critical"    # > $500K/year potential


class ApproachStrategy(Enum):
    """Recommended approach strategy"""
    PARTNERSHIP = "partnership"     # Partnership opportunity
    DIRECT_SALES = "direct_sales"   # Direct B2B sales
    DISTRIBUTOR = "distributor"     # Become their distributor
    COMPETITIVE = "competitive"     # Competitor analysis only
    STRATEGIC_ALLIANCE = "strategic_alliance"  # Strategic partnership


class DecisionLevel(Enum):
    """Decision maker authority level"""
    FINAL = "final"            # Final decision maker
    INFLUENTIAL = "influential"  # Influences decisions
    OPERATIONAL = "operational"  # Day-to-day contact


@dataclass
class DecisionMaker:
    """Key contact person at a business"""
    name: str
    title: str
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin_profile: Optional[str] = None
    decision_level: DecisionLevel = DecisionLevel.OPERATIONAL
    contact_frequency: str = "monthly"  # weekly, monthly, quarterly


@dataclass
class BusinessIntelligence:
    """Main business intelligence entity for D Corner Living"""

    # Primary Identification
    business_id: str                    # Internal unique ID
    google_cid: str                     # Google Maps CID
    business_name: str                  # Official business name
    business_type: BusinessType         # Categorized business type

    # Contact Information
    primary_phone: str
    emails: List[str] = field(default_factory=list)
    website: Optional[str] = None
    social_media: Dict[str, str] = field(default_factory=dict)

    # Location Intelligence
    address: str
    city: str
    country: str
    latitude: float
    longitude: float
    logistics_zone: str = "unknown"    # Dubai Central, Abu Dhabi North, etc.

    # Business Intelligence
    business_size: BusinessSize = BusinessSize.SMALL
    estimated_revenue: PotentialValue = PotentialValue.LOW
    years_in_business: int = 0
    employee_count: int = 0

    # Quality Metrics
    google_rating: float = 0.0
    review_count: int = 0
    trust_score: int = 0                # 0-100 trustworthiness score

    # D Corner Living Specific
    lead_score: int = 0                 # 0-100 priority scoring
    potential_value: PotentialValue = PotentialValue.LOW
    product_match: List[str] = field(default_factory=list)  # ["Office Furniture", "Luxury Residential"]
    approach_strategy: ApproachStrategy = ApproachStrategy.DIRECT_SALES

    # Market Intelligence
    specialties: List[str] = field(default_factory=list)      # ["Hotel Furniture", "Office Design"]
    current_suppliers: List[str] = field(default_factory=list) # Known competitors
    project_frequency: str = "unknown"   # Projects per year estimate
    decision_makers: List[DecisionMaker] = field(default_factory=list)

    # Extraction Metadata
    extraction_date: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    extraction_source: str = "BOB Google Maps Ultimate V3.0"
    data_quality_score: int = 0         # 0-100 data completeness

    def calculate_lead_score(self) -> int:
        """
        Calculate lead score based on multiple factors.
        Used for prioritizing outreach efforts.
        """
        score = 0

        # Contact Availability (30 points)
        if self.emails:
            score += 15
        if self.primary_phone:
            score += 10
        if self.website:
            score += 5

        # Business Quality (25 points)
        if self.google_rating >= 4.5:
            score += 10
        if self.review_count >= 50:
            score += 8
        if self.years_in_business >= 5:
            score += 7

        # Market Fit (25 points)
        if self.business_type in [BusinessType.INTERIOR_DESIGNER, BusinessType.OFFICE_FURNITURE]:
            score += 10
        if self.business_size in [BusinessSize.MEDIUM, BusinessSize.LARGE]:
            score += 8
        if self.estimated_revenue in [PotentialValue.HIGH, PotentialValue.CRITICAL]:
            score += 7

        # D Corner Living Fit (20 points)
        if self.product_match:
            score += 10
        if self.approach_strategy != ApproachStrategy.COMPETITIVE:
            score += 10

        self.lead_score = min(score, 100)
        return self.lead_score

    def calculate_data_quality_score(self) -> int:
        """
        Calculate data quality score (0-100).
        Higher score means more complete and reliable data.
        """
        score = 0

        # Essential fields (40 points)
        if self.business_name: score += 10
        if self.primary_phone: score += 10
        if self.address: score += 10
        if self.business_type: score += 10

        # Enhanced fields (30 points)
        if self.emails: score += 10
        if self.website: score += 8
        if self.google_rating > 0: score += 7
        if self.review_count > 0: score += 5

        # Business intelligence (20 points)
        if self.specialties: score += 8
        if self.years_in_business > 0: score += 7
        if self.employee_count > 0: score += 5

        # Contact enrichment (10 points)
        if self.decision_makers: score += 5
        if self.social_media: score += 5

        self.data_quality_score = min(score, 100)
        return self.data_quality_score

    def get_priority_level(self) -> str:
        """Get priority level based on lead score"""
        if self.lead_score >= 80:
            return "CRITICAL"
        elif self.lead_score >= 60:
            return "HIGH"
        elif self.lead_score >= 40:
            return "MEDIUM"
        else:
            return "LOW"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            # Primary Identification
            "business_id": self.business_id,
            "google_cid": self.google_cid,
            "business_name": self.business_name,
            "business_type": self.business_type.value if self.business_type else None,

            # Contact Information
            "primary_phone": self.primary_phone,
            "emails": self.emails,
            "website": self.website,
            "social_media": self.social_media,

            # Location Intelligence
            "address": self.address,
            "city": self.city,
            "country": self.country,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "logistics_zone": self.logistics_zone,

            # Business Intelligence
            "business_size": self.business_size.value if self.business_size else None,
            "estimated_revenue": self.estimated_revenue.value if self.estimated_revenue else None,
            "years_in_business": self.years_in_business,
            "employee_count": self.employee_count,

            # Quality Metrics
            "google_rating": self.google_rating,
            "review_count": self.review_count,
            "trust_score": self.trust_score,

            # D Corner Living Specific
            "lead_score": self.lead_score,
            "potential_value": self.potential_value.value if self.potential_value else None,
            "product_match": self.product_match,
            "approach_strategy": self.approach_strategy.value if self.approach_strategy else None,

            # Market Intelligence
            "specialties": self.specialties,
            "current_suppliers": self.current_suppliers,
            "project_frequency": self.project_frequency,
            "decision_makers": [
                {
                    "name": dm.name,
                    "title": dm.title,
                    "email": dm.email,
                    "phone": dm.phone,
                    "decision_level": dm.decision_level.value,
                    "contact_frequency": dm.contact_frequency
                }
                for dm in self.decision_makers
            ],

            # Metadata
            "extraction_date": self.extraction_date.isoformat(),
            "last_updated": self.last_updated.isoformat(),
            "extraction_source": self.extraction_source,
            "data_quality_score": self.data_quality_score,

            # Computed fields
            "priority_level": self.get_priority_level()
        }

    @classmethod
    def from_raw_extraction(cls, raw_data: Dict[str, Any], business_id: str) -> "BusinessIntelligence":
        """
        Create BusinessIntelligence from BOB Google Maps raw extraction data.
        """
        # Map business type
        business_type_mapping = {
            "Interior designer": BusinessType.INTERIOR_DESIGNER,
            "Office furniture store": BusinessType.OFFICE_FURNITURE,
            "Furniture store": BusinessType.FURNITURE_STORE,
            "Furniture manufacturer": BusinessType.FURNITURE_MANUFACTURER,
        }

        category = raw_data.get("category", "").lower()
        business_type = business_type_mapping.get(category, BusinessType.FURNITURE_STORE)

        # Create business intelligence object
        business = cls(
            business_id=business_id,
            google_cid=str(raw_data.get("cid", "")),
            business_name=raw_data.get("name", ""),
            business_type=business_type,
            primary_phone=raw_data.get("phone", ""),
            emails=raw_data.get("emails", []),
            website=raw_data.get("website", ""),
            address=raw_data.get("address", ""),
            city="Dubai",  # Extract from address or default
            country="UAE",  # Extract from address or default
            latitude=raw_data.get("latitude", 0.0),
            longitude=raw_data.get("longitude", 0.0),
            google_rating=raw_data.get("rating", 0.0),
            review_count=raw_data.get("review_count", 0),
            extraction_source=raw_data.get("extraction_method", "Unknown")
        )

        # Calculate scores
        business.calculate_data_quality_score()
        business.calculate_lead_score()

        return business