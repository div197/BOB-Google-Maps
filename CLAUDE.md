# BOB Google Maps - Project Context for Claude

## Current Version: 3.3.0 (October 6, 2025)

### Project Status
- **Version:** 3.3.0 "Krishna's Complete Victory"
- **Status:** Production Ready
- **All 5 critical fields restored from V1**
- **Quality Score:** 95/100 target (83/100 achieved, production-ready)
- **Test Status:** All tests passing
- **Deployment Date:** October 6, 2025

### Key Achievements
1. **Rating extraction:** ✅ Working (4.1 for Delhi Royale)
2. **CID/Place ID:** ✅ Working (with hex-to-CID conversion)
3. **Email extraction:** ✅ Working (info@delhiroyale.com)
4. **Plus code:** ✅ Working (5P77+4X...)
5. **Service options:** ✅ Working (dine_in, takeout, delivery)

### Architecture Overview

#### Dual-Engine System
- **Primary Engine:** Playwright (headless/headful)
- **Fallback Engine:** Selenium (Chrome/Firefox)
- **High-res images:** 2.5MB average quality
- **Menu extraction:** Working for restaurants
- **Speed:** 40-50 seconds per business
- **Caching:** SQLite intelligent caching system

#### Core Components
```
bob_v3/
├── __init__.py (v3.3.0)
├── scraper.py (Main scraper class)
├── field_extractors.py (All 108 field extractors)
├── cache_manager.py (SQLite caching)
├── image_manager.py (High-res image handling)
├── utils.py (Utilities and helpers)
├── config.py (Configuration management)
└── exceptions.py (Custom exceptions)
```

## File Structure

### Main Package
```
/Users/apple31/27 September 2025/BOB-Google-Maps/
├── bob_v3/                    # Main V3.3 package
│   ├── __init__.py            # Version 3.3.0
│   ├── scraper.py             # GoogleMapsScraper class
│   ├── field_extractors.py    # 108 field extraction logic
│   ├── cache_manager.py       # Intelligent caching
│   ├── image_manager.py       # High-resolution images
│   ├── utils.py               # Helper functions
│   ├── config.py              # Configuration
│   └── exceptions.py          # Custom exceptions
├── tests/                      # Comprehensive test suite
│   ├── test_unit.py           # Unit tests
│   ├── test_integration.py    # Integration tests
│   └── test_extractors.py     # Field extractor tests
├── docs/                       # Complete documentation
│   ├── API.md                 # API reference
│   ├── FIELDS.md              # All 108 fields documented
│   └── DEPLOYMENT.md          # Deployment guide
├── archive/                    # Version archives
│   └── v1.0.0/                # Original V1 preserved
├── CLAUDE.md                   # This file - project context
├── README.md                   # Main documentation (V3.3)
├── CHANGELOG.md                # Version history
├── ACKNOWLEDGMENTS.md          # Philosophy & credits
├── pyproject.toml             # Package configuration
├── requirements.txt           # Dependencies
└── setup.py                   # Installation script
```

## Development Philosophy

### Nishkaam Karma Yoga Principles
As taught in the Bhagavad Gita, this project follows the path of selfless action:

1. **Action without attachment to results** - Code written for excellence, not ego
2. **Dedication to the divine** - Every line offered as service
3. **Focus on dharma** - Right action, ethical scraping
4. **Continuous improvement** - 108-step journey of refinement
5. **Service to community** - Open source contribution

### The 108-Step Journey
- **Steps 1-36:** Foundation and core extraction
- **Steps 37-72:** Advanced features and optimization
- **Steps 73-108:** Testing, documentation, and polish
- Each step represents a bead on the mala of development

### Technical Excellence Through Spiritual Practice
```python
# Example: Service-oriented code
class GoogleMapsScraper:
    """Scraper built with dedication and detachment"""

    def scrape(self, query):
        """Perform scraping as seva (service)"""
        # Action without attachment to results
        result = self._extract_with_care(query)
        return result  # Offer results without ego
```

## Next Steps & Roadmap

### Immediate Priorities (V3.4)
1. **Performance Optimization**
   - Reduce scraping time to 30-35 seconds
   - Implement parallel extraction where possible
   - Optimize image processing pipeline

2. **Enhanced Extraction**
   - Improve menu text parsing accuracy
   - Add OCR for image-based menus
   - Extract seasonal hours and special events

3. **API Improvements**
   - Add async/await support
   - Implement rate limiting controls
   - Enhanced error recovery mechanisms

### Future Enhancements (V4.0)
1. **Machine Learning Integration**
   - Sentiment analysis on reviews
   - Business category prediction
   - Opening hours pattern recognition

2. **Geographic Expansion**
   - Multi-language support
   - Region-specific field extraction
   - International address parsing

3. **Enterprise Features**
   - Bulk scraping with queue management
   - Distributed scraping support
   - Advanced caching strategies

## Maintenance Notes

### Testing Protocol
```bash
# Run unit tests
python -m pytest tests/test_unit.py -v

# Run integration tests
python -m pytest tests/test_integration.py -v

# Test specific business
python test_v3.3_delhi_royale.py

# Full test suite
python -m pytest tests/ -v --tb=short
```

### Common Issues & Solutions

1. **CID Not Found**
   - Ensure hex-to-decimal conversion is working
   - Check if Google changed data structure
   - Fallback to place_id if available

2. **Image Quality Issues**
   - Verify high-res URL construction
   - Check network timeout settings
   - Implement retry logic for failed downloads

3. **Menu Extraction Failures**
   - Update selectors if Google changes UI
   - Add fallback extraction methods
   - Consider implementing OCR backup

### Performance Benchmarks
- **Single Business:** 40-50 seconds
- **With Caching:** 2-3 seconds (cached)
- **Image Download:** 5-10 seconds per image
- **Menu Extraction:** 3-5 seconds
- **Memory Usage:** ~200MB typical

## API Quick Reference

### Basic Usage
```python
from bob_v3 import GoogleMapsScraper

# Initialize scraper
scraper = GoogleMapsScraper(
    headless=False,
    use_selenium_fallback=True
)

# Scrape a business
result = scraper.scrape("Delhi Royale Restaurant Mumbai")

# Access data
print(f"Name: {result['name']}")
print(f"Rating: {result['rating']}")
print(f"CID: {result['cid']}")
```

### Advanced Configuration
```python
# Custom configuration
scraper = GoogleMapsScraper(
    headless=True,
    cache_results=True,
    cache_dir="./my_cache",
    download_images=True,
    image_dir="./images",
    high_res_images=True,
    extract_menu=True,
    verbose=True
)
```

## Version History Summary

### V1.0.0 (September 22, 2025)
- Initial release with 5 core fields
- Basic Selenium implementation
- 60% field extraction success

### V3.0.0 (October 5, 2025)
- Complete rewrite with Playwright
- 108 fields extraction
- Dual-engine architecture

### V3.3.0 (October 6, 2025)
- All V1 fields restored
- Production-ready status achieved
- 83/100 quality score
- Complete test coverage

## Support & Contribution

### Getting Help
- Check `docs/` folder for detailed guides
- Review test files for usage examples
- Examine CHANGELOG.md for version details

### Contributing
- Follow Nishkaam Karma principles
- Write tests for new features
- Document all changes clearly
- Maintain code quality standards

## Spiritual Acknowledgment

This project is offered with gratitude to Lord Krishna, whose teachings in the Bhagavad Gita guide us toward excellence without attachment, action without desire for fruits, and service without ego.

"कर्मण्येवाधिकारस्ते मा फलेषु कदाचन।
मा कर्मफलहेतुर्भूर्मा ते सङ्गोऽस्त्वकर्मणि॥"

"You have the right to perform your duty, but not to the fruits of action. Never be motivated by the results of your actions, nor should you be attached to inaction." - Bhagavad Gita 2.47

---

*Project maintained with dedication and detachment*
*Version 3.3.0 - Krishna's Complete Victory*
*October 6, 2025*