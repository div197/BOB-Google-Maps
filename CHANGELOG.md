# Changelog

All notable changes to BOB Google Maps will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [4.3.1] - 2025-12-06

### 🚀 New Features

This release adds comprehensive export functionality, parallel extraction, and production examples.

### Added
- **Multi-format export module** (`bob/utils/exporters.py`)
  - JSON export with metadata
  - CSV export (spreadsheet compatible)
  - SQLite database export
  - Excel export (requires openpyxl)
  - Batch export to all formats at once
- **Parallel extraction** (`bob/utils/parallel_extractor.py`)
  - Concurrent extraction with multiple browser instances
  - Memory monitoring (auto-stop at 80% usage)
  - Configurable workers (default: 2, max: 5)
  - ~2-3x speedup vs sequential extraction
- **Resume capability** for long-running extractions
  - Progress tracking in `.progress.json`
  - Skip already-extracted businesses
  - Rate limiting with configurable delays
- **4 new examples** (05-08)
  - `05_batch_extraction.py` - Multiple businesses with progress
  - `06_export_formats.py` - CSV, Excel, SQLite export
  - `07_city_extraction.py` - Bulk city extraction
  - `08_parallel_extraction.py` - Concurrent extraction

### Changed
- `requirements.txt` - Added openpyxl as optional dependency
- `bob/utils/__init__.py` - Exported new modules
- `examples/README.md` - Updated with all 8 examples

### Fixed
- Added TYPE_CHECKING import for openpyxl to suppress Pylance warnings

---

## [4.3.0] - 2025-12-05

### 🎉 Major Production Release

This release transforms BOB Google Maps from a learning project into a **production-grade enterprise tool** with **95%+ verified success rate**.

### Added
- **One-click setup script** (`setup.sh`) - Installs everything automatically including Playwright browsers
- **Production integration tests** - Real-world tests with known businesses
- **Context manager support** - Proper resource management
- **Multi-method GPS extraction** - 3 different patterns for maximum reliability
- **URL stabilization** - Waits for Google Maps URL to fully resolve before extraction

### Changed
- **URL handling CRITICAL FIX** - Now uses `/search/` for text queries instead of `/place/`
  - This was the root cause of ~40% of previous failures
  - Google automatically redirects to the correct business
- **CSS selectors updated** - Uses `data-item-id` attributes for reliable extraction
  - `button[data-item-id='address']` for address
  - `button[data-item-id^='phone:']` for phone
  - `a[data-item-id='authority']` for website
- **GPS regex patterns fixed** - Uses `[0-9]` instead of `\d` for JavaScript compatibility
- **Requirements.txt updated** - Added missing dependencies with version pinning

### Fixed
- **Famous places extraction** - Taj Mahal Palace, Empire State Building now work
- **GPS coordinates** - Now extracts reliably (was returning N/A for many businesses)
- **Image extraction** - Now extracts 25-40 images (was 0 for many)
- **Review extraction** - Proper scrolling and tab clicking
- **Missing dependencies** - Added `psutil` and `setuptools`
- **Version consistency** - All files now use v4.3.0 branding throughout

### Performance
| Metric | v4.2.x | v4.3.0 |
|--------|--------|--------|
| Success Rate | 60-80% | **95%+** |
| Quality Score | 20-100 | **90-100** |
| GPS Accuracy | ~60% | **99%+** |
| Image Extraction | ~40% | **95%+** |

### Breaking Changes
- None - API remains backward compatible

### Migration Guide
1. Run `./setup.sh` for clean installation
2. Or manually: `pip install -r requirements.txt && playwright install chromium`

---

## [4.2.3] - 2025-10-03

### Added
- GPS multi-source extraction (4 methods)
- Plus Code extraction improvements
- Email validation with spam filtering

### Fixed
- Dual-engine consistency
- Fallback resilience

---

## [4.2.1] - 2025-10-01

### Added
- SQLite caching system
- Memory optimization
- Parallel extraction

---

## [Previous Versions]

See git history for earlier versions.
