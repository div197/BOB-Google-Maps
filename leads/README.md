# Business Leads Data Directory

## 📊 Overview

This directory contains extracted business intelligence data from BOB Google Maps v3.4.1 extraction missions. All data is organized by business category, geography, and extraction project.

## 📂 Data Organization

### By Business Category

**Architecture & Design:**
- `architecture_firms_leads.json` - Premium architecture firms
- Residential, commercial, and mixed-use projects

**Commercial & Furniture:**
- `consolidated_commercial_leads.json` - All commercial leads consolidated
- `commercial_office_leads.json` - Office space and commercial offices
- `commercial_fitout_leads.json` - Commercial fitout and design
- `commercial_furniture_leads.json` - Furniture supplier networks
- `commercial_furniture_suppliers_leads.json` - Specialized furniture suppliers

**Real Estate:**
- `real_estate_developers_leads.json` - Real estate development companies
- `dubai_marina_luxury.json` - Dubai Marina luxury properties
- `dubai_hills_villa.json` - Dubai Hills residential villas
- `downtown_dubai_luxury_*.json` - Downtown Dubai luxury segments
- `emirates_hills_*.json` - Emirates Hills developments
- `palm_jumeirah_*.json` - Palm Jumeirah luxury estates

**Hospitality & Retail:**
- `hospitality_industry_leads.json` - Hotels, restaurants, cafes
- `hospitality_retail_comprehensive_leads.json` - Complete hospitality + retail
- `shopping_mall_*.json` - Shopping mall networks
- `retail_chain_*.json` - Retail chain operations

**Healthcare:**
- `healthcare_facilities_leads.json` - Medical centers, hospitals, clinics

**Government & Municipal:**
- `government_municipal_projects_leads.json` - Government projects
- `bikaner_municipality.json` - Municipal services

**Education:**
- `education_institutions_leads.json` - Schools, colleges, universities

### By Geography

**UAE:**
- `dubai_*` - Dubai region extractions
- `abu_dhabi_*` - Abu Dhabi region
- `sharjah_*` - Sharjah region

**Saudi Arabia:**
- `riyadh_*` - Riyadh extractions
- `jeddah_*` - Jeddah region
- `dammam_*` - Dammam region

**Other GCC:**
- `kuwait_*` - Kuwait extractions
- `qatar_*` - Qatar extractions
- `oman_*` - Oman extractions
- `bahrain_*` - Bahrain extractions

### Export Formats

**CRM Integration Files:**
- `*_crm_import.csv` - Universal CSV format for CRM systems
- Includes: Commercial leads, hospitality & retail leads

**Batch Search Files:**
- `healthcare_search_batch_*.txt` - Healthcare search queries
- Used for batch processing and verification

## 📈 Data Statistics

### Total Lead Files: 172+
### Coverage Areas:
- **Geographic**: UAE, Saudi Arabia, Qatar, Kuwait, Oman, Bahrain
- **Business Types**: 15+ categories
- **Data Quality**: 68-100/100 quality score range

## 🔍 File Naming Convention

Format: `[region_]business_type[_specification].json`

Examples:
- `dubai_interior_design_comprehensive_leads.json`
- `saudi_arabia_interior_design_comprehensive_report.json`
- `gcc_luxury_expansion_leads.json`
- `uae_residential_expansion_leads.json`

## 📋 Data Fields

Standard business lead includes:
- Business name and ID
- Contact information (phone, email, website)
- Location and GPS coordinates
- Business category and rating
- Reviews and photos
- Operating hours
- Service offerings
- Quality score (0-100)

## 💾 Accessing the Data

### Direct JSON Access
```bash
cat leads/dubai_interior_design_comprehensive_leads.json | python3 -m json.tool
```

### Using Python
```python
import json

with open('leads/dubai_marina_luxury.json', 'r') as f:
    leads = json.load(f)
    for lead in leads:
        print(f"{lead['name']}: {lead['phone']}")
```

### CRM Import
1. Choose appropriate CSV file for your CRM
2. Follow CRM-specific import guidelines
3. Map fields as needed

## 🔄 Maintenance

### Adding New Leads
1. Follow naming convention
2. Ensure consistent JSON structure
3. Include metadata (extraction date, quality score)
4. Update this README with category info

### Updating Existing Data
- Maintain extraction date timestamp
- Track version/iteration numbers
- Document major changes in commit messages

### Data Quality
- All leads have quality scoring
- Scores reflect completeness and accuracy
- Filter by quality score for critical tasks

## ⚠️ Data Accuracy

**Important Notes:**
- Data extracted via web scraping
- Subject to web page changes
- Regular verification recommended
- Contact information may change
- Quality scores indicate data confidence

## 🎯 Use Cases

- **Lead Generation**: Direct business outreach
- **Market Research**: Competitor analysis
- **CRM Campaigns**: Bulk communication
- **Business Intelligence**: Market trends
- **Network Expansion**: Partnership identification

## 🔐 Privacy & Compliance

- Data sourced from public Google Maps listings
- For business development purposes only
- Respect privacy and anti-spam regulations
- Follow local regulations for each region

---

**Directory Created:** October 21, 2025
**System Version:** BOB Google Maps v3.4.1
**Last Updated:** October 21, 2025
**Total Leads Cataloged:** 172+ business intelligence files

