"""
Image Data Model - BOB V3.0
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Image:
    """
    Image data model.

    Attributes:
        url: Image URL
        resolution: Image resolution (e.g., "4096x4096")
        extracted_at: When this image was extracted
    """

    url: str
    resolution: Optional[str] = None
    extracted_at: datetime = None

    def __post_init__(self):
        if self.extracted_at is None:
            self.extracted_at = datetime.now()
