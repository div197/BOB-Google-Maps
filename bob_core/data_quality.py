"""bob_core.data_quality

Comprehensive data quality metrics and validation system.
"""
from __future__ import annotations

import re
import logging
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import statistics
from collections import defaultdict

__all__ = [
    "DataQualityMetrics",
    "DataValidator", 
    "QualityScore",
    "ValidationRule",
    "DataCleaner",
    "QualityReport"
]


class QualityDimension(Enum):
    """Data quality dimensions."""
    COMPLETENESS = "completeness"
    ACCURACY = "accuracy"
    CONSISTENCY = "consistency"
    VALIDITY = "validity"
    UNIQUENESS = "uniqueness"
    TIMELINESS = "timeliness"


class QualityLevel(Enum):
    """Quality level classifications."""
    EXCELLENT = "excellent"  # 90-100%
    GOOD = "good"           # 75-89%
    FAIR = "fair"           # 60-74%
    POOR = "poor"           # 0-59%


@dataclass
class QualityScore:
    """Quality score for a specific dimension."""
    dimension: QualityDimension
    score: float  # 0.0 to 1.0
    total_records: int
    passed_records: int
    failed_records: int
    issues: List[str] = field(default_factory=list)
    
    @property
    def percentage(self) -> float:
        """Get score as percentage."""
        return self.score * 100
    
    @property
    def level(self) -> QualityLevel:
        """Get quality level based on score."""
        if self.score >= 0.9:
            return QualityLevel.EXCELLENT
        elif self.score >= 0.75:
            return QualityLevel.GOOD
        elif self.score >= 0.6:
            return QualityLevel.FAIR
        else:
            return QualityLevel.POOR
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "dimension": self.dimension.value,
            "score": self.score,
            "percentage": self.percentage,
            "level": self.level.value,
            "total_records": self.total_records,
            "passed_records": self.passed_records,
            "failed_records": self.failed_records,
            "issues": self.issues
        }


@dataclass
class ValidationRule:
    """Data validation rule."""
    name: str
    dimension: QualityDimension
    validator: Callable[[Any], bool]
    description: str = ""
    error_message: str = ""
    
    def validate(self, value: Any) -> bool:
        """Validate a value against this rule."""
        try:
            return self.validator(value)
        except Exception:
            return False


class DataValidator:
    """Comprehensive data validator for business and review data."""
    
    def __init__(self):
        self.rules: Dict[str, List[ValidationRule]] = defaultdict(list)
        self._logger = logging.getLogger("bob_core.data_validator")
        self._setup_default_rules()
    
    def _setup_default_rules(self):
        """Setup default validation rules for Google Maps data."""
        
        # Business name rules
        self.add_rule("business_name", ValidationRule(
            name="not_empty",
            dimension=QualityDimension.COMPLETENESS,
            validator=lambda x: x and str(x).strip() != "" and str(x).strip().lower() != "unknown",
            description="Business name should not be empty or 'Unknown'",
            error_message="Business name is empty or 'Unknown'"
        ))
        
        # Rating rules
        self.add_rule("rating", ValidationRule(
            name="valid_rating_format",
            dimension=QualityDimension.VALIDITY,
            validator=lambda x: self._is_valid_rating(x),
            description="Rating should be in valid format",
            error_message="Rating format is invalid"
        ))
    
    def _is_valid_rating(self, rating: Any) -> bool:
        """Check if rating is in valid format."""
        if not rating:
            return False
        
        rating_str = str(rating).lower()
        if rating_str in ["unrated", "unavailable"]:
            return True
        
        # Check for patterns like "4.5 stars"
        patterns = [r'^\d+\.?\d*\s*stars?$', r'^\d+\.?\d*$']
        return any(re.match(pattern, rating_str) for pattern in patterns)
    
    def add_rule(self, field: str, rule: ValidationRule):
        """Add a validation rule for a field."""
        self.rules[field].append(rule)
    
    def validate_dataset(self, records: List[Dict[str, Any]]) -> Dict[str, QualityScore]:
        """Validate entire dataset and return quality scores."""
        dimension_results = defaultdict(lambda: {"total": 0, "passed": 0, "issues": []})
        
        for record in records:
            for field, rules in self.rules.items():
                value = record.get(field)
                for rule in rules:
                    dimension = rule.dimension
                    dimension_results[dimension]["total"] += 1
                    if rule.validate(value):
                        dimension_results[dimension]["passed"] += 1
                    else:
                        dimension_results[dimension]["issues"].append(rule.error_message)
        
        # Calculate quality scores
        quality_scores = {}
        for dimension, results in dimension_results.items():
            if results["total"] > 0:
                score = results["passed"] / results["total"]
                quality_scores[dimension.value] = QualityScore(
                    dimension=dimension,
                    score=score,
                    total_records=results["total"],
                    passed_records=results["passed"],
                    failed_records=results["total"] - results["passed"],
                    issues=list(set(results["issues"]))
                )
        
        return quality_scores


class DataCleaner:
    """Data cleaning and normalization utilities."""
    
    def __init__(self):
        self._logger = logging.getLogger("bob_core.data_cleaner")
    
    def clean_business_name(self, name: str) -> str:
        """Clean and normalize business name."""
        if not name:
            return "Unknown"
        return re.sub(r'\s+', ' ', str(name).strip())
    
    def clean_rating(self, rating: str) -> str:
        """Clean and normalize rating."""
        if not rating:
            return "Unrated"
        
        rating_str = str(rating).strip()
        match = re.search(r'(\d+\.?\d*)', rating_str)
        if match:
            numeric_rating = float(match.group(1))
            if 0 <= numeric_rating <= 5:
                return f"{numeric_rating} stars"
        return rating_str
    
    def clean_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Clean an entire record."""
        cleaned = record.copy()
        
        if "business_info" in cleaned:
            business_info = cleaned["business_info"]
            if "name" in business_info:
                business_info["name"] = self.clean_business_name(business_info["name"])
            if "rating" in business_info:
                business_info["rating"] = self.clean_rating(business_info["rating"])
        
        return cleaned


@dataclass
class QualityReport:
    """Comprehensive data quality report."""
    
    timestamp: datetime = field(default_factory=datetime.now)
    total_records: int = 0
    quality_scores: Dict[str, QualityScore] = field(default_factory=dict)
    overall_score: float = 0.0
    recommendations: List[str] = field(default_factory=list)
    
    @property
    def overall_level(self) -> QualityLevel:
        """Get overall quality level."""
        if self.overall_score >= 0.9:
            return QualityLevel.EXCELLENT
        elif self.overall_score >= 0.75:
            return QualityLevel.GOOD
        elif self.overall_score >= 0.6:
            return QualityLevel.FAIR
        else:
            return QualityLevel.POOR
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "total_records": self.total_records,
            "overall_score": self.overall_score,
            "overall_percentage": self.overall_score * 100,
            "overall_level": self.overall_level.value,
            "quality_scores": {
                name: score.to_dict() for name, score in self.quality_scores.items()
            },
            "recommendations": self.recommendations
        }


class DataQualityMetrics:
    """Main data quality metrics system."""
    
    def __init__(self):
        self.validator = DataValidator()
        self.cleaner = DataCleaner()
        self._logger = logging.getLogger("bob_core.data_quality")
    
    def analyze_quality(self, data: List[Dict[str, Any]]) -> QualityReport:
        """Perform comprehensive data quality analysis."""
        if not data:
            return QualityReport(total_records=0)
        
        quality_scores = self.validator.validate_dataset(data)
        
        if quality_scores:
            overall_score = statistics.mean(score.score for score in quality_scores.values())
        else:
            overall_score = 0.0
        
        recommendations = self._generate_recommendations(quality_scores)
        
        return QualityReport(
            total_records=len(data),
            quality_scores=quality_scores,
            overall_score=overall_score,
            recommendations=recommendations
        )
    
    def _generate_recommendations(self, quality_scores: Dict[str, QualityScore]) -> List[str]:
        """Generate improvement recommendations."""
        recommendations = []
        
        for dimension_name, score in quality_scores.items():
            if score.level == QualityLevel.POOR:
                recommendations.append(
                    f"Improve {dimension_name} quality: {score.failed_records} records need attention"
                )
        
        if not recommendations:
            recommendations.append("Data quality is good! Continue monitoring.")
        
        return recommendations
    
    def clean_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Clean and normalize data."""
        cleaned_data = []
        
        for record in data:
            try:
                cleaned_record = self.cleaner.clean_record(record)
                cleaned_data.append(cleaned_record)
            except Exception as e:
                self._logger.warning(f"Failed to clean record: {e}")
                cleaned_data.append(record)
        
        return cleaned_data 