# D Corner Living - Data Architecture Strategy

## 🎯 **Project Overview**

**Company**: D Corner Living (Furniture Manufacturer & Distributor)
**Mission**: Build comprehensive business intelligence database for furniture market expansion
**Tool**: BOB Google Maps Ultimate V3.0 for data extraction

## 🏗️ **Data Architecture Decision: CENTRALIZED + DISTRIBUTED HYBRID**

### **Why Hybrid Architecture?**

#### **Centralized Component (Master Database)**
- **Purpose**: Single source of truth for business intelligence
- **Benefits**: Consistency, unified analysis, reporting
- **Technology**: SQLite with intelligent caching

#### **Distributed Component (Mission-Specific Datasets)**
- **Purpose**: Mission-specific extractions with different requirements
- **Benefits**: Flexibility, scalability, mission isolation
- **Technology**: Individual JSON datasets per mission

## 📊 **Data Model Design**

### **🔥 Core Entity: BusinessIntelligence**

```python
@dataclass
class BusinessIntelligence:
    # Primary Identification
    business_id: str                    # Internal unique ID
    google_cid: str                     # Google Maps CID
    business_name: str                  # Official business name
    business_type: BusinessType         # Enum: INTERIOR_DESIGNER, FURNITURE_STORE, etc.

    # Contact Information
    primary_phone: str
    emails: List[str]
    website: str
    social_media: Dict[str, str]        # LinkedIn, Instagram, Facebook

    # Location Intelligence
    address: str
    city: str
    country: str
    latitude: float
    longitude: float
    logistics_zone: str                 # Dubai Central, Abu Dhabi North, etc.

    # Business Intelligence
    business_size: BusinessSize         # Enum: SMALL, MEDIUM, LARGE, ENTERPRISE
    estimated_revenue: RevenueRange     # Enum: <100K, 100K-500K, 500K-1M, >1M
    years_in_business: int
    employee_count: EmployeeRange

    # Quality Metrics
    google_rating: float
    review_count: int
    trust_score: int                    # 0-100 based on reviews, age, etc.

    # D Corner Living Specific
    lead_score: int                     # 0-100 priority scoring
    potential_value: PotentialValue     # Enum: LOW, MEDIUM, HIGH, CRITICAL
    product_match: List[str]            # ["Office Furniture", "Luxury Residential"]
    approach_strategy: ApproachStrategy # Enum: PARTNERSHIP, DIRECT_SALES, DISTRIBUTOR

    # Market Intelligence
    specialties: List[str]              # ["Hotel Furniture", "Office Design"]
    current_suppliers: List[str]        # Known competitors they work with
    project_frequency: ProjectRange     # Projects per year

    # Extraction Metadata
    extraction_date: datetime
    last_updated: datetime
    extraction_source: str              # "BOB Google Maps Ultimate V3.0"
    data_quality_score: int             # 0-100 completeness

    # Relationship Data
    related_companies: List[str]        # Partner companies, branches
    decision_makers: List[DecisionMaker] # Key contacts
```

### **🎯 Specialized Entities**

#### **Lead Scoring Model**
```python
@dataclass
class LeadScore:
    business_id: str

    # Contact Availability (30 points)
    has_email: bool = False
    has_phone: bool = False
    has_website: bool = False

    # Business Quality (25 points)
    high_rating: bool = False          # 4.5+ stars
    established_business: bool = False  # 5+ years
    substantial_reviews: bool = False  # 50+ reviews

    # Market Fit (25 points)
    location_strategic: bool = False   # Near industrial/design districts
    business_type_match: bool = False  # Interior designer, furniture store
    size_appropriate: bool = False     # Medium+ size businesses

    # D Corner Living Fit (20 points)
    product_alignment: bool = False    # Matches our product categories
    partnership_potential: bool = False # Can be distribution partner
    immediate_need: bool = False       # Active projects indicated

    def calculate_score(self) -> int:
        # Implementation of weighted scoring
        pass
```

#### **Decision Maker Intelligence**
```python
@dataclass
class DecisionMaker:
    business_id: str
    name: str
    title: str                          # Design Director, Procurement Manager, Owner
    email: str
    phone: str
    linkedin_profile: str
    decision_level: DecisionLevel       # FINAL, INFLUENTIAL, OPERATIONAL
    contact_frequency: ContactFrequency # WEEKLY, MONTHLY, QUARTERLY
```

## 🗄️ **Database Schema Design**

### **SQLite Central Database Schema**

```sql
-- Main Business Intelligence Table
CREATE TABLE businesses (
    business_id TEXT PRIMARY KEY,
    google_cid TEXT UNIQUE,
    business_name TEXT NOT NULL,
    business_type TEXT NOT NULL,

    -- Contact Information
    primary_phone TEXT,
    emails TEXT, -- JSON array
    website TEXT,
    social_media TEXT, -- JSON object

    -- Location Intelligence
    address TEXT,
    city TEXT,
    country TEXT,
    latitude REAL,
    longitude REAL,
    logistics_zone TEXT,

    -- Business Intelligence
    business_size TEXT,
    estimated_revenue TEXT,
    years_in_business INTEGER,
    employee_count TEXT,

    -- Quality Metrics
    google_rating REAL,
    review_count INTEGER,
    trust_score INTEGER,

    -- D Corner Living Specific
    lead_score INTEGER,
    potential_value TEXT,
    product_match TEXT, -- JSON array
    approach_strategy TEXT,

    -- Market Intelligence
    specialties TEXT, -- JSON array
    current_suppliers TEXT, -- JSON array
    project_frequency TEXT,

    -- Metadata
    extraction_date TEXT,
    last_updated TEXT,
    extraction_source TEXT,
    data_quality_score INTEGER
);

-- Decision Makers Table
CREATE TABLE decision_makers (
    decision_maker_id TEXT PRIMARY KEY,
    business_id TEXT,
    name TEXT NOT NULL,
    title TEXT,
    email TEXT,
    phone TEXT,
    linkedin_profile TEXT,
    decision_level TEXT,
    contact_frequency TEXT,
    FOREIGN KEY (business_id) REFERENCES businesses(business_id)
);

-- Mission Tracking Table
CREATE TABLE missions (
    mission_id TEXT PRIMARY KEY,
    mission_name TEXT NOT NULL,
    mission_type TEXT NOT NULL,
    target_business_type TEXT,
    geographic_scope TEXT,
    search_terms TEXT, -- JSON array
    status TEXT, -- PLANNING, ACTIVE, COMPLETED, FAILED
    start_date TEXT,
    end_date TEXT,
    businesses_extracted INTEGER,
    high_quality_leads INTEGER,
    created_at TEXT,
    updated_at TEXT
);

-- Extraction Logs Table
CREATE TABLE extraction_logs (
    log_id TEXT PRIMARY KEY,
    mission_id TEXT,
    business_name TEXT,
    extraction_status TEXT, -- SUCCESS, FAILED, PARTIAL
    error_message TEXT,
    extraction_time_seconds REAL,
    data_quality_score INTEGER,
    extracted_at TEXT,
    FOREIGN KEY (mission_id) REFERENCES missions(mission_id)
);
```

## 🎯 **Mission-Based Data Strategy**

### **Mission Types**

#### **1. GEOGRAPHIC MISSIONS**
```json
{
  "mission_id": "GEO_UAE_DUBAI_001",
  "mission_name": "Dubai Interior Design Companies",
  "mission_type": "GEOGRAPHIC",
  "target_business_type": "INTERIOR_DESIGNER",
  "geographic_scope": "Dubai, UAE",
  "search_terms": [
    "interior design company Dubai",
    "luxury interior design Dubai",
    "office interior design Dubai Marina"
  ],
  "expected_results": 50,
  "priority": "HIGH"
}
```

#### **2. BUSINESS TYPE MISSIONS**
```json
{
  "mission_id": "TYPE_OFFICE_FURNITURE_001",
  "mission_name": "GCC Office Furniture Distributors",
  "mission_type": "BUSINESS_TYPE",
  "target_business_type": "OFFICE_FURNITURE",
  "geographic_scope": "GCC Countries",
  "search_terms": [
    "office furniture Saudi Arabia",
    "corporate furniture Dubai",
    "commercial furniture Qatar"
  ],
  "expected_results": 100,
  "priority": "MEDIUM"
}
```

#### **3. COMPETITIVE INTELLIGENCE MISSIONS**
```json
{
  "mission_id": "COMP_MANUFACTURERS_001",
  "mission_name": "UAE Furniture Manufacturers Analysis",
  "mission_type": "COMPETITIVE_INTELLIGENCE",
  "target_business_type": "FURNITURE_MANUFACTURER",
  "geographic_scope": "UAE Industrial Areas",
  "search_terms": [
    "furniture manufacturer Dubai",
    "custom furniture UAE",
    "furniture factory Dubai Industrial Area"
  ],
  "expected_results": 25,
  "priority": "LOW"
}
```

## 📈 **Data Processing Pipeline**

### **Stage 1: Raw Data Collection**
- **Input**: BOB Google Maps extraction results
- **Format**: JSON files per mission
- **Location**: `data/raw/mission_{id}/extracted_{timestamp}.json`

### **Stage 2: Data Processing & Enrichment**
- **Process**: Clean, validate, and enrich raw data
- **Enrichments**: Lead scoring, geographic mapping, quality assessment
- **Output**: Processed datasets with intelligence added
- **Location**: `data/processed/mission_{id}/processed_{timestamp}.json`

### **Stage 3: Central Database Integration**
- **Process**: Merge processed data into central SQLite database
- **Deduplication**: Identify and merge duplicate businesses
- **Relationships**: Link related companies and decision makers
- **Location**: `data/cache/dcorner_master.db`

### **Stage 4: Analytics & Reporting**
- **Process**: Generate insights and reports
- **Reports**: Daily extraction reports, weekly market analysis
- **Location**: `reports/{daily,weekly,monthly}/`

## 🔧 **Technical Implementation Strategy**

### **Phase 1: Infrastructure Setup (Week 1)**
1. **Database Setup**: SQLite master database with schema
2. **Base Models**: Python dataclasses for core entities
3. **Processing Pipeline**: Data cleaning and enrichment scripts
4. **Quality Assurance**: Data validation and scoring systems

### **Phase 2: Mission Execution (Week 2-4)**
1. **Mission 1**: Dubai Interior Designers (50 businesses)
2. **Mission 2**: UAE Furniture Showrooms (30 businesses)
3. **Mission 3**: GCC Office Furniture Distributors (100 businesses)
4. **Data Integration**: Merge all missions into master database

### **Phase 3: Intelligence Generation (Week 5-6)**
1. **Lead Scoring**: Calculate priority scores for all businesses
2. **Market Analysis**: Generate market insights and reports
3. **Relationship Mapping**: Identify partnerships and competitive opportunities
4. **Action Plans**: Create outreach strategies for top prospects

## 🎯 **Success Metrics**

### **Data Quality Metrics**
- **Contact Information Completeness**: >90% phone/email coverage
- **Data Accuracy**: >95% verified contact information
- **Coverage**: 80%+ of target market businesses
- **Freshness**: Data updated within last 30 days

### **Business Intelligence Metrics**
- **Lead Quality**: 70%+ of leads classified as Medium+ potential
- **Market Coverage**: Complete coverage of target business types
- **Competitive Insights**: 95%+ of major competitors identified
- **Opportunity Identification**: 50+ partnership opportunities identified

### **Operational Metrics**
- **Extraction Success Rate**: >95% successful extractions
- **Processing Efficiency**: <1 hour from extraction to database integration
- **Mission Completion**: 100% of planned missions completed on time
- **Data Quality Score**: >85 average quality score across all records

## 🚀 **Next Steps**

1. **Implement Core Models**: Create Python dataclasses and database schema
2. **Build Processing Pipeline**: Data cleaning and enrichment scripts
3. **Execute First Mission**: Dubai Interior Designers extraction
4. **Iterate and Refine**: Improve models based on real data

This architecture provides the foundation for building a comprehensive business intelligence database that will give D Corner Living a significant competitive advantage in the UAE furniture market.