"""
BOB Google Maps - Setup Configuration
Free Google Maps data extraction tool
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8")

setup(
    name="bob-google-maps",
    version="1.0.0",
    author="BOB Team",
    author_email="contact@bobmaps.com",
    description="Free Google Maps data extraction - Business info, images, reviews at zero cost",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/div197/BOB-Google-Maps",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Office/Business",
        "Topic :: Education",
    ],
    python_requires=">=3.8",
    install_requires=[
        "selenium>=4.15.0",
        "requests>=2.31.0",
        "urllib3>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
        "export": [
            "pandas>=2.0.0",
            "openpyxl>=3.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "bob-google-maps=bob_maps:main",
            "bob=bob_maps:main",
        ],
    },
    keywords=[
        "google-maps", "scraping", "business-intelligence", "data-extraction",
        "market-research", "academic-research", "free-alternative",
        "images", "coordinates", "reviews", "businesses", "open-source"
    ],
    project_urls={
        "Documentation": "https://github.com/div197/BOB-Google-Maps/blob/main/DOCUMENTATION/",
        "Source": "https://github.com/div197/BOB-Google-Maps",
        "Tracker": "https://github.com/div197/BOB-Google-Maps/issues",
        "Changelog": "https://github.com/div197/BOB-Google-Maps/blob/main/CHANGELOG.md"
    },
    include_package_data=True,
    zip_safe=False,
)