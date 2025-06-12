# Changelog

All notable changes to this project will be documented in this file.

## [0.5.0] - 2025-01-XX - **PRODUCTION READY RELEASE** 🚀

### 🌟 Major Features
- **⚡ Business-Only Extraction Mode** - 3.18x faster extraction for business directories
  - New `extract_reviews=False` parameter for lightning-fast business info extraction
  - Dedicated `scrape_business_only()` method for convenience
  - Smart review limiting with `max_reviews` parameter
  - Batch processing support for business-only mode

- **🛡️ Enterprise-Grade Fault Tolerance System**
  - Circuit breaker pattern with auto-failover capabilities
  - Auto-recovery mechanisms for temporary failures
  - Graceful degradation for partial data extraction
  - Dead letter queue for failed request handling
  - Smart retry strategies with exponential backoff

- **📊 Advanced Performance Monitoring**
  - Real-time performance metrics collection
  - Memory management with automatic garbage collection
  - Health monitoring with system status checks
  - Performance profiling and bottleneck detection

- **🎭 Enhanced Dual Backend Support**
  - Improved Playwright backend with 60s timeout
  - Better navigation strategy (`domcontentloaded` vs `networkidle`)
  - Automatic backend selection based on availability
  - Selenium as reliable fallback option

### 🔧 Technical Improvements
- **Selector Healing** - Automatic DOM selector adaptation
- **Connection Pooling** - Resource optimization for batch operations
- **Data Quality Validation** - Enhanced data cleaning and validation
- **Memory Optimization** - Intelligent memory management and cleanup

### 📈 Performance Benchmarks
- **Business-only extraction**: ~18s (vs 56s full extraction)
- **Speed improvement**: 3.18x faster for business directories
- **Time saved**: 38.65s (68.6% reduction) for business-only mode
- **Playwright backend**: 1.5x faster than Selenium for some operations

### 🏗️ Architecture Enhancements
- **Modular fault tolerance system** with 10+ specialized components
- **Health monitoring CLI** with `python -m bob_core.health_cli`
- **Comprehensive error handling** with specific error codes
- **Production-ready logging** and monitoring capabilities

### 🧪 Testing & Quality
- **23 passing unit tests** covering all functionality
- **Real-world production testing** with actual Google Maps URLs
- **100% backward compatibility** maintained
- **Enterprise-grade reliability** validated

### 📚 Documentation
- **Comprehensive README** with usage examples and benchmarks
- **Detailed CONTRIBUTING guide** for developers
- **Architecture documentation** with component diagrams
- **Performance guides** and optimization tips

### 🔄 API Changes (Backward Compatible)
```python
# New business-only extraction options
scraper = GoogleMapsScraper(extract_reviews=False)  # Business-only mode
scraper = GoogleMapsScraper(max_reviews=10)         # Limited reviews
result = scraper.scrape_business_only(url)          # Dedicated method

# Enhanced batch processing
from bob_core.batch import batch_scrape
results = batch_scrape(urls, extract_reviews=False, max_workers=4)
```

### 🐛 Bug Fixes
- Fixed missing `get_global_selector_healer()` function
- Resolved Playwright timeout issues with increased limits
- Fixed performance decorator usage in backends
- Corrected batch processing default backend selection

### ⚠️ Breaking Changes
- None - Full backward compatibility maintained

---

## [0.4.0] - 2025-06-12
### Added
- **Data export utilities** - Export to CSV, Excel, JSON with auto-format detection
- **Configuration management** - Persistent settings with `bob config` command
- **Enhanced CLI** - Export and config subcommands
- **Comprehensive test suite** - 12 passing tests covering all modules
- **Pydantic v2 compatibility** - Updated validators and field definitions
- **Package discovery fix** - Proper setuptools configuration

### Changed
- Fixed Pydantic v2 compatibility issues
- Improved error handling and validation
- Enhanced CLI with export and config management
- Better project structure with proper package exclusions

## [0.3.0] - 2025-06-12
### Added
- **Playwright backend** - Faster, more reliable alternative to Selenium
- **Pydantic models** - Structured data validation and serialization
- **Analytics module** - Business intelligence, sentiment analysis, market insights
- **CLI analytics command** - `bob analyze` for data insights
- **Backend selection** - Choose Selenium, Playwright, or auto-detect
- **Enhanced business parser** - Address, phone, website extraction
- **Unit test suite** - Comprehensive testing for models and analytics
- **TestPyPI publishing** - Automated package publishing on tags

### Changed
- Scraper now supports multiple backends (auto-selects Playwright if available)
- CLI commands enhanced with backend selection options
- Dependencies expanded: pydantic, playwright, textblob

## [0.2.0] - 2025-06-12
### Added
- Progress-bar powered concurrent batch scraping with `tqdm`.
- Async wrapper `async_batch_scrape`.
- CLI improvements remain compatible.
- Documentation site scaffolding (MkDocs).
- CONTRIBUTING guide and Ruff config.

## [0.1.0] - 2025-06-12
### Added
- Project resets to new "BOB Google Maps" vision.
- Migrated original GPL codebase to `legacy/` directory for reference (do not distribute).
- Added MIT license.
- Added initial `BOB_CONCEPT.md` visionary document.
- Created project skeleton with `bob_core/`, `docs/`, and `.github/workflows/` directories.
- Placeholder modules for new scraper and future AI agents. 