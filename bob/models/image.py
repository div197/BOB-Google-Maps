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

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            'url': self.url,
            'resolution': self.resolution,
            'extracted_at': self.extracted_at.isoformat() if self.extracted_at else None
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Image':
        """
        Recreate Image from dictionary (for cache/database recovery).

        Args:
            data: Dictionary with image data

        Returns:
            Image: Reconstructed Image object
        """
        # Parse datetime if provided as ISO string
        extracted_at = data.get('extracted_at')
        if isinstance(extracted_at, str):
            extracted_at = datetime.fromisoformat(extracted_at)

        return cls(
            url=data.get('url'),
            resolution=data.get('resolution'),
            extracted_at=extracted_at or datetime.now()
        )
