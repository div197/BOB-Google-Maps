# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2025-06-12
### Added
- Project resets to new "BOB Google Maps" vision.
- Migrated original GPL codebase to `legacy/` directory for reference (do not distribute).
- Added MIT license.
- Added initial `BOB_CONCEPT.md` visionary document.
- Created project skeleton with `bob_core/`, `docs/`, and `.github/workflows/` directories.
- Placeholder modules for new scraper and future AI agents.

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