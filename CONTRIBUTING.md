# Contributing to BOB Google Maps

*Jai Shree Krishna!* 🙏 Welcome to the BOB Google Maps contributor community!

We follow the principles of **Niṣkāma Karma Yoga** - selfless action with excellence. Every contribution, no matter how small, is valued and appreciated.

## 🌟 Philosophy

BOB is built with:
- **Excellence without attachment** to results
- **Service-oriented** development mindset
- **Zero-compromise** quality standards
- **Community-first** approach

## 🚀 Quick Start for Contributors

### 1. Development Setup

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/BOB-Google-Maps.git
cd BOB-Google-Maps

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8 mypy

# Install Playwright (optional)
pip install playwright
playwright install chromium

# Verify installation
python -m bob_core.health_cli status
```

### 2. Run Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=bob_core --cov-report=html

# Run specific test
python -m pytest tests/test_circuit_breaker.py -v

# Test business-only functionality
python -c "
import bob_core
scraper = bob_core.GoogleMapsScraper(extract_reviews=False)
result = scraper.scrape('https://maps.google.com/?q=restaurant&hl=en')
print(f'Success: {result[\"success\"]}')
"
```

### 3. Code Quality

```bash
# Format code
black bob_core/ tests/

# Check linting
flake8 bob_core/ tests/

# Type checking
mypy bob_core/

# All quality checks
black bob_core/ tests/ && flake8 bob_core/ tests/ && mypy bob_core/
```

## 📋 Contribution Types

### 🐛 Bug Reports
- Use GitHub Issues with the "bug" label
- Include minimal reproduction case
- Provide system information (OS, Python version)
- Include error logs and stack traces

### ✨ Feature Requests
- Use GitHub Issues with the "enhancement" label
- Describe the use case and business value
- Consider backward compatibility
- Propose API design if applicable

### 🔧 Code Contributions
- Fork the repository
- Create feature branch: `git checkout -b feature/amazing-feature`
- Follow coding standards (see below)
- Add tests for new functionality
- Update documentation
- Submit pull request

### 📚 Documentation
- Improve README, docstrings, or examples
- Add tutorials or use case guides
- Fix typos or clarify explanations
- Update API documentation

## 🏗️ Architecture Overview

### Core Components

```text
bob_core/
├── scraper.py              # Main interface - GoogleMapsScraper class
├── playwright_backend.py   # Playwright implementation
├── business_parser.py      # Business info extraction logic
├── review_parser.py        # Review extraction and parsing
├── analytics.py            # Business intelligence features
├── batch.py                # Batch processing utilities
├── cli.py                  # Command line interface
├── models.py               # Pydantic data models
└── export.py               # Data export functionality
```

### Fault Tolerance System

```text
├── circuit_breaker.py      # Circuit breaker pattern
├── auto_recovery.py        # Self-healing capabilities
├── graceful_degradation.py # Partial failure handling
├── memory_management.py    # Resource optimization
├── performance_monitoring.py # Metrics collection
├── health_check.py         # System health monitoring
├── dead_letter_queue.py    # Failed request handling
├── retry_strategy.py       # Smart retry logic
├── selector_healing.py     # DOM selector adaptation
├── data_quality.py         # Data validation
└── connection_pooling.py   # Resource pooling
```

## 🎯 Development Guidelines

### Code Style

```python
# Use type hints
def scrape_business(url: str, timeout: int = 60) -> Dict[str, Any]:
    """Extract business information from Google Maps URL.
    
    Args:
        url: Google Maps URL to scrape
        timeout: Maximum wait time in seconds
        
    Returns:
        Dictionary containing business information
        
    Raises:
        ScrapingError: If extraction fails
    """
    pass

# Use descriptive variable names
business_info = extract_business_details(page)
review_count = len(extracted_reviews)

# Follow PEP 8
class GoogleMapsScraper:
    """Enterprise-grade Google Maps scraper."""
    
    def __init__(self, extract_reviews: bool = True):
        self.extract_reviews = extract_reviews
```

### Testing Standards

```python
# Test file: tests/test_feature.py
import pytest
from bob_core import GoogleMapsScraper

class TestBusinessOnlyExtraction:
    """Test business-only extraction functionality."""
    
    def test_business_only_faster_than_full(self):
        """Business-only should be significantly faster."""
        scraper_business = GoogleMapsScraper(extract_reviews=False)
        scraper_full = GoogleMapsScraper(extract_reviews=True)
        
        # Test with timing assertions
        # ... implementation
        
    def test_business_only_no_reviews(self):
        """Business-only should not extract reviews."""
        scraper = GoogleMapsScraper(extract_reviews=False)
        result = scraper.scrape(TEST_URL)
        
        assert result['reviews_count'] == 0
        assert len(result['reviews']) == 0
```

### Error Handling

```python
from bob_core.error_codes import ErrorCode
from bob_core.exceptions import ScrapingError

def extract_business_info(page) -> Dict[str, Any]:
    """Extract business information with proper error handling."""
    try:
        # Extraction logic
        return business_data
    except TimeoutError:
        raise ScrapingError(
            ErrorCode.TIMEOUT_ERROR,
            "Page load timeout exceeded"
        )
    except Exception as e:
        raise ScrapingError(
            ErrorCode.EXTRACTION_ERROR,
            f"Failed to extract business info: {str(e)}"
        )
```

### Performance Considerations

```python
# Use performance monitoring
from bob_core.performance_monitoring import performance_monitor

@performance_monitor.track_execution_time
def extract_reviews(page, max_reviews: int = None):
    """Extract reviews with performance tracking."""
    # Implementation with early exit for max_reviews
    pass

# Memory management
from bob_core.memory_management import get_global_memory_manager

def batch_process(urls: List[str]):
    """Process URLs with memory monitoring."""
    memory_manager = get_global_memory_manager()
    
    for url in urls:
        if memory_manager.should_trigger_gc():
            memory_manager.force_garbage_collection()
        # Process URL
```

## 🧪 Testing Strategy

### Test Categories

1. **Unit Tests** (`tests/test_*.py`)
   - Individual function testing
   - Mock external dependencies
   - Fast execution (< 1s per test)

2. **Integration Tests** (`tests/integration/`)
   - Component interaction testing
   - Real browser automation
   - Moderate execution time

3. **End-to-End Tests** (`tests/e2e/`)
   - Full workflow testing
   - Real Google Maps URLs
   - Slower execution (production-like)

### Test Data

```python
# Use consistent test URLs
TEST_URLS = {
    'restaurant': 'https://maps.google.com/?q=restaurant+paris&hl=en',
    'cafe': 'https://maps.google.com/?q=cafe+london&hl=en',
    'hotel': 'https://maps.google.com/?q=hotel+tokyo&hl=en'
}

# Mock data for unit tests
MOCK_BUSINESS_DATA = {
    'name': 'Test Restaurant',
    'rating': 4.5,
    'reviews_count': 150,
    'address': '123 Test Street'
}
```

## 🔄 Pull Request Process

### 1. Before Submitting

```bash
# Ensure all tests pass
python -m pytest tests/ -v

# Check code quality
black bob_core/ tests/
flake8 bob_core/ tests/
mypy bob_core/

# Test your changes
python -c "
import bob_core
# Test your specific changes
"
```

### 2. PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Performance Impact
- [ ] No performance impact
- [ ] Performance improvement: X% faster
- [ ] Performance regression: justified because...

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added for new functionality
```

### 3. Review Process

1. **Automated Checks**: CI/CD pipeline runs tests
2. **Code Review**: Maintainer reviews code quality
3. **Testing**: Manual testing of new features
4. **Documentation**: Ensure docs are updated
5. **Merge**: Squash and merge to main

## 🏷️ Release Process

### Version Numbering
- **Major** (1.0.0): Breaking changes
- **Minor** (0.5.0): New features, backward compatible
- **Patch** (0.5.1): Bug fixes

### Release Checklist
1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Run full test suite
4. Update documentation
5. Create GitHub release
6. Publish to PyPI (maintainers only)

## 🎯 Priority Areas for Contribution

### High Priority
- **Performance Optimization**: Make business-only extraction even faster
- **Error Handling**: Improve graceful degradation
- **Documentation**: More examples and tutorials
- **Testing**: Increase test coverage

### Medium Priority
- **New Backends**: Support for other automation tools
- **Analytics**: Enhanced business intelligence features
- **Export Formats**: Additional data export options
- **CLI Improvements**: Better command-line experience

### Low Priority
- **UI/Dashboard**: Web interface for BOB
- **API Server**: REST API wrapper
- **Integrations**: Third-party service connections
- **Mobile Support**: Mobile-specific optimizations

## 🤝 Community Guidelines

### Communication
- **Be Respectful**: Treat everyone with kindness
- **Be Constructive**: Provide helpful feedback
- **Be Patient**: Remember we're all learning
- **Be Inclusive**: Welcome newcomers

### Code of Conduct
- Follow the [Contributor Covenant](https://www.contributor-covenant.org/)
- Report issues to maintainers
- Focus on technical merit
- Maintain professional discourse

## 📞 Getting Help

### Resources
- **Documentation**: README.md and inline docs
- **Examples**: See `examples/` directory
- **Issues**: Search existing GitHub issues
- **Discussions**: Use GitHub Discussions for questions

### Contact
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Email**: divyanshu@abcsteps.com (maintainer)

## 🙏 Recognition

All contributors are recognized in:
- **CONTRIBUTORS.md**: List of all contributors
- **GitHub Contributors**: Automatic GitHub recognition
- **Release Notes**: Major contributions highlighted
- **Documentation**: Examples and tutorials credited

## 📈 Metrics and Goals

### Current Status (v0.5.0)
- **Test Coverage**: 85%+
- **Performance**: 3.18x improvement for business-only
- **Reliability**: Enterprise-grade fault tolerance
- **Documentation**: Comprehensive guides

### Goals for v0.6.0
- **Test Coverage**: 95%+
- **Performance**: 5x improvement target
- **New Features**: Advanced analytics
- **Community**: 10+ active contributors

---

## 🌟 Thank You!

Every contribution makes BOB better for the entire community. Whether you're fixing a typo, adding a feature, or helping other users, your efforts are deeply appreciated.

**Made with 🙏 in the spirit of Niṣkāma Karma Yoga**

*Excellence without attachment, Service without expectation* 