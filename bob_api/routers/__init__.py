"""bob_api.routers

FastAPI routers for BOB Google Maps API v0.6.0
Modular endpoint organization with divine architecture.

Made with 🙏 following Niṣkāma Karma Yoga principles
"""

from . import scraper, batch, health, metrics, admin, zeroth_law, thermodynamics

__all__ = ["scraper", "batch", "health", "metrics", "admin", "zeroth_law", "thermodynamics"] 