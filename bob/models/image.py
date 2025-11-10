"""
Image Data Model - BOB V3.0
"""

from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
from datetime import datetime


@dataclass
class Image:
    """
    Image data model.

    Attributes:
        url: Image URL
        resolution: Image resolution (e.g., "4096x4096")
        width: Image width in pixels
        height: Image height in pixels
        thumbnail: Thumbnail URL
        extracted_at: When this image was extracted
    """

    url: str
    resolution: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    thumbnail: Optional[str] = None
    extracted_at: Optional[datetime] = None

    def __post_init__(self):
        if self.extracted_at is None:
            self.extracted_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert Image to dictionary.

        Returns:
            Dict[str, Any]: Dictionary representation of Image
        """
        data = asdict(self)
        # Convert datetime to ISO format
        if isinstance(data.get('extracted_at'), datetime):
            data['extracted_at'] = data['extracted_at'].isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Image':
        """
        Reconstruct Image from dictionary.

        Args:
            data: Dictionary containing image data

        Returns:
            Image: Reconstructed Image instance
        """
        # Handle datetime fields
        if 'extracted_at' in data and isinstance(data['extracted_at'], str):
            data = data.copy()
            data['extracted_at'] = datetime.fromisoformat(data['extracted_at'])

        return cls(**data)
