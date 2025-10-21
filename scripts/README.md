# Scripts Directory

## 📜 Overview

This directory contains utility scripts for business extraction, testing, and development tasks for BOB Google Maps v3.4.1.

## 📂 Structure

### Extraction Specialist Scripts
These are domain-specific extraction agents for specialized business intelligence:

- **architecture_firms_specialist.py** - Extract premium architecture firms with collaboration potential
- **government_municipal_specialist.py** - Government and municipal services extraction
- **healthcare_facilities_leads.py** - Healthcare facilities and medical services
- **real_estate_developer_extractor.py** - Real estate and property development companies

### Commercial & Furniture Extraction
- **extract_commercial_furniture_suppliers.py** - Commercial furniture supplier leads
- **comprehensive_furniture_extraction.py** - Comprehensive furniture market extraction
- **focused_furniture_extraction.py** - Targeted furniture extraction
- **manual_commercial_furniture_extraction.py** - Manual furniture lead extraction

### Testing & Debugging
- **test_extraction.py** - Core extraction testing
- **test_imports.sh** - Import verification script
- **test_simple.py** - Simple sanity checks
- **debug_extraction.py** - Debugging extraction issues

## 🚀 Usage

### Running an Extraction Specialist
```bash
python3 scripts/architecture_firms_specialist.py
python3 scripts/healthcare_facilities_leads.py
```

### Running Tests
```bash
python3 scripts/test_extraction.py
python3 scripts/test_simple.py
bash scripts/test_imports.sh
```

### Debugging Issues
```bash
python3 scripts/debug_extraction.py
```

## 🔧 Development

### Creating New Extraction Scripts
1. Follow the specialist pattern from existing scripts
2. Include proper error handling
3. Add documentation and usage examples
4. Test thoroughly before committing

### Script Template
```python
#!/usr/bin/env python3
"""
Script Description - BOB Google Maps v3.4.1
Purpose and capabilities
"""

# Standard imports
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from bob import HybridExtractor

# Implementation
```

## 📋 Best Practices

1. **Keep It Focused**: Each script should have a clear, specific purpose
2. **Error Handling**: Graceful failures with informative error messages
3. **Documentation**: Include docstrings and usage comments
4. **Logging**: Use structured logging for debugging
5. **Testing**: Include test cases or verification code

## 🔄 Integration

Scripts in this directory are:
- **Autonomous**: Can be run independently
- **Reusable**: Can be imported and used in other scripts
- **Testable**: Include verification and error checking
- **Documented**: Clear purpose and usage

## 📊 Performance Expectations

- Typical extraction: 6-8 seconds per business
- With rate limiting (20s): 26-28 seconds per business
- Memory usage: 17-56MB per extraction
- Success rate: 95%+ on real data

## 🐛 Troubleshooting

### Import Errors
```bash
bash scripts/test_imports.sh
```

### Extraction Failures
```bash
python3 scripts/debug_extraction.py
```

### Performance Issues
Check: BOB Google Maps v3.4.1 documentation for optimization techniques

---

**Last Updated:** October 21, 2025
**System Version:** BOB Google Maps v3.4.1
**Philosophy:** Nishkaam Karma Yoga - Reliable, focused utility scripts
