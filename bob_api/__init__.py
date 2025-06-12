"""bob_api

FastAPI-based REST API for BOB Google Maps v0.6.0
Enterprise-grade deployment-ready web service with divine architecture.

Made with 🙏 following Niṣkāma Karma Yoga principles
"""

__version__ = "0.6.0"
__author__ = "Divyanshu Singh Chouhan"
__email__ = "divyanshu@abcsteps.com"

from .main import app
from .models import *
from .routers import *

__all__ = ["app"] 