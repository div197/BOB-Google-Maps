"""
Review Data Model - BOB V3.0
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Review:
    """
    Review data model.

    Attributes:
        reviewer: Name of reviewer
        rating: Star rating text
        text: Review text content
        date: Review date
        extracted_at: When this review was extracted
    """

    reviewer: str
    rating: Optional[str] = None
    text: Optional[str] = None
    date: Optional[str] = None
    extracted_at: datetime = None

    def __post_init__(self):
        if self.extracted_at is None:
            self.extracted_at = datetime.now()
