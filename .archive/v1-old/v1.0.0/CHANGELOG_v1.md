# Changelog
All notable changes to BOB Google Maps will be documented in this file.

## [1.0.0] - 2025-09-22

### 🎉 Initial Production Release

#### ✨ Features
- **Core Extraction**: Business name, address, phone, rating, category (85-95% success)
- **CID System**: Universal identifier for ALL Place ID formats
- **Image Extraction**: 4-20 high-resolution images (impossible via Google API)
- **Review Extraction**: 2-5 customer reviews with reviewer names
- **GPS Coordinates**: Latitude/longitude extraction from URLs
- **Multiple Exports**: JSON, CSV, Excel formats
- **Batch Processing**: Process multiple businesses
- **Retry Logic**: 3 attempts with exponential backoff
- **Data Quality**: 0-100 quality scoring system

#### 🏗️ Architecture
- 2,613 lines of clean, focused code (reduced from 40,000+)
- 5 core modules with clear separation
- 3 minimal dependencies
- Production-grade error handling

#### 🔑 CID Normalization
- Converts all Place ID formats to universal CID
- Handles ChIJ, GhIJ, hex, and numeric formats
- Real vs pseudo-CID distinction
- Database-friendly identifiers

#### 📊 Performance
- 75% overall success rate
- 30-60 seconds per business
- < 500MB memory usage
- Handles 100+ businesses

#### 🐛 Bug Fixes
- Fixed website URL extraction
- Fixed Place ID extraction for multiple formats
- Fixed image filtering to exclude UI elements
- Fixed CSV export encoding issues

#### 📝 Documentation
- Complete production documentation
- Honest capability assessment
- Clear usage examples
- Developer guide (CLAUDE.md)

#### 🙏 Philosophy
- Created with Nishkaam Karma Yoga
- Focused on truth over marketing
- Simplified from complex to simple
- Free forever commitment

### Known Issues
- Email extraction not implemented
- Popular times selectors outdated
- Social media links not working
- Menu extraction incomplete

### Coming in v1.1
- Email extraction from websites
- Popular times graph data
- Social media link detection
- Restaurant menu extraction
- Extended review history
- Proxy support
- REST API server

---

*For detailed release information, see [docs/RELEASE_NOTES.md](docs/RELEASE_NOTES.md)*