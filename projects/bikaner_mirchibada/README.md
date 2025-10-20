# 🏛️ Bikaner Business Intelligence Project
## bikaner.mirchibada.com

**Objective:** Extract comprehensive business data for all leading businesses in Bikaner, Rajasthan, India

**Project Type:** Business Lead Generation & Market Research
**Status:** INITIATED - First Test Run
**Date Started:** October 20, 2025

---

## Project Overview

This project aims to build a comprehensive database of businesses in Bikaner using the BOB Google Maps extraction system.

### Target Businesses by Category

1. **Hotels & Hospitality**
   - Lalgarh Palace Hotel
   - Heritage Hotels
   - Budget Hotels
   - Guesthouses

2. **Restaurants & Cafes**
   - Fine Dining
   - Fast Food
   - Street Food Vendors
   - Cafes

3. **Shopping & Retail**
   - Shopping Malls
   - Traditional Markets
   - Boutiques
   - Department Stores

4. **Tourism & Heritage**
   - Museums
   - Historical Sites
   - Tour Operators
   - Travel Agencies

5. **Services**
   - Healthcare
   - Education
   - Transportation
   - Business Services

---

## Folder Structure

```
bikaner_mirchibada/
├── data/                  # Extracted business data (JSON)
├── scripts/              # Python extraction scripts
├── reports/              # Analysis reports and summaries
├── leads/                # CRM-ready lead lists (CSV)
├── README.md             # This file
└── PROGRESS.md           # Project progress tracking
```

---

## First Test: Lalgarh Palace Bikaner

**Business:** Lalgarh Palace Hotel
**Status:** FIRST EXTRACTION TEST
**Expected Data:**
- ✓ Business name and category
- ✓ Contact phone and website
- ✓ Complete address and location (lat/long)
- ✓ Star rating and review count
- ✓ Business hours and price range
- ✓ Photos and reviews
- ✓ Email addresses (if available)

---

## Quick Start

### Run First Test
```bash
cd /Users/aaple30/Documents/3-10-2025/BOB-Google-Maps
python projects/bikaner_mirchibada/test_extraction_lalgarh.py
```

### View Results
```bash
cat projects/bikaner_mirchibada/data/lalgarh_palace_bikaner.json | python -m json.tool
```

---

## Data Fields Extracted (108 Fields)

See CLAUDE.md and SHREE_GANESH_ANALYSIS.md for complete field documentation.

Key fields:
- `name` - Business name
- `phone` - Contact number
- `address` - Complete address
- `latitude`, `longitude` - GPS coordinates
- `rating` - Star rating (0-5)
- `review_count` - Number of reviews
- `website` - Business website
- `emails` - Contact emails
- `photos` - Business photos (URLs)
- `reviews` - Customer reviews
- `price_range` - Price indicator
- `hours` - Operating hours
- `data_quality_score` - Quality assessment (0-100)

---

## Success Criteria

✓ **Lalgarh Palace Test:** Extract all 108 fields
✓ **Quality Score:** Minimum 75/100
✓ **Execution Time:** < 2 minutes
✓ **Success Rate:** 95%+

---

## Project Timeline

- **Oct 20, 2025** - Project initiated, first test planned
- **Oct 20, 2025** - Lalgarh Palace test run
- **Oct 21, 2025** - Batch extraction of top 50 businesses
- **Oct 22-23, 2025** - Full Bikaner business extraction
- **Oct 24, 2025** - Data analysis and reporting

---

## Notes

- This project uses BOB Google Maps Ultimate V3.0
- Extraction follows Nishkaam Karma Yoga principles
- All data is publicly available business information
- Project respects Google's terms of service and robots.txt
- Rate limiting and delays are implemented
- Real-time data validated through actual extraction

---

**Contact:** Project Manager
**Last Updated:** October 20, 2025
