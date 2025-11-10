# Installation Guide - BOB Google Maps

Complete installation instructions for all platforms.

## System Requirements

- **Python:** 3.8 or higher (3.10+ recommended)
- **RAM:** 2GB minimum
- **Storage:** 1GB for cache and dependencies
- **Browser:** Chrome/Chromium installed
- **Network:** Stable internet connection
- **OS:** macOS, Linux, or Windows

## Quick Installation (5 minutes)

### Step 1: Clone Repository
```bash
git clone https://github.com/div197/bob-google-maps.git
cd bob-google-maps
```

### Step 2: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows
```

### Step 3: Install Package
```bash
pip install -e .
```

### Step 4: Verify Installation
```bash
python -c "from bob import PlaywrightExtractorOptimized; print('✅ Ready!')"
```

## Platform-Specific Installation

### macOS
```bash
brew install python@3.10 chromium
python3.10 -m venv venv
source venv/bin/activate
pip install -e .
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update && sudo apt install python3.10 python3-pip python3-venv chromium-browser
python3.10 -m venv venv
source venv/bin/activate
pip install -e .
```

### Windows
```bash
# Install Python 3.10+ from python.org
python -m venv venv
venv\Scripts\activate
pip install -e .
```

## Docker Installation

```bash
docker build -t bob-google-maps .
docker run -it bob-google-maps
```

## Configuration

Create `config.yaml` in project root:

```yaml
extraction:
  default_engine: "hybrid"
  timeout: 30
  max_concurrent: 3

memory:
  optimized: true

cache:
  enabled: true
  expiration_hours: 24
```

## Troubleshooting

### Chrome not found
- **macOS:** `brew install chromium`
- **Linux:** `sudo apt install chromium-browser`
- **Windows:** Download from https://www.chromium.org/

### Import errors
```bash
pip install --upgrade -e ".[dev]"
```

### Out of memory
```python
from bob import HybridExtractorOptimized
extractor = HybridExtractorOptimized(memory_optimized=True, max_concurrent=1)
```

## Development Setup

```bash
pip install -e ".[dev]"
pytest tests/ -v
black bob/ && flake8 bob/
```

## Next Steps

1. Read [QUICKSTART.md](QUICKSTART.md)
2. Check [examples/](../examples/)
3. See [API_REFERENCE.md](API_REFERENCE.md)

---

**Ready to extract business data!** Start with [QUICKSTART.md](QUICKSTART.md).
