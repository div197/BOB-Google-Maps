"""BOB Core Package

This package contains the MIT-licensed, refactored codebase for the BOB Google Maps project.

Version: 0.1.0 (2025-06-12)
"""

__all__ = [
    "scraper",
    "analytics", 
    "models",
    "playwright_backend",
]

__version__ = "0.3.0"

from .cli import main as _cli_main

def cli():
    """Entry-point wrapper for console_scripts."""
    _cli_main() 