# Installation Guide - BOB Google Maps v4.3.0# Installation Guide - BOB Google Maps



## RequirementsComplete installation instructions for all platforms.



- **Python:** 3.9+ (3.11+ recommended)## System Requirements

- **RAM:** 512MB minimum

- **Storage:** 500MB for dependencies- **Python:** 3.8 or higher (3.10+ recommended)

- **OS:** macOS, Linux, or Windows- **RAM:** 2GB minimum

- **Storage:** 1GB for cache and dependencies

## One-Click Installation (Recommended)- **Browser:** Chrome/Chromium installed

- **Network:** Stable internet connection

```bash- **OS:** macOS, Linux, or Windows

git clone https://github.com/div197/BOB-Google-Maps.git

cd BOB-Google-Maps## Quick Installation (5 minutes)

chmod +x setup.sh && ./setup.sh

```### Step 1: Clone Repository

```bash

The setup script:git clone https://github.com/div197/bob-google-maps.git

1. Creates virtual environment (`.venv`)cd bob-google-maps

2. Installs all dependencies```

3. Installs Playwright browsers

4. Verifies installation### Step 2: Create Virtual Environment

```bash

Activate environment:python3 -m venv venv

```bashsource venv/bin/activate  # macOS/Linux

source .venv/bin/activate# or

```venv\Scripts\activate  # Windows

```

## Manual Installation

### Step 3: Install Package

### Step 1: Clone Repository```bash

pip install -e .

```bash```

git clone https://github.com/div197/BOB-Google-Maps.git

cd BOB-Google-Maps### Step 4: Verify Installation

``````bash

python -c "from bob import PlaywrightExtractorOptimized; print('✅ Ready!')"

### Step 2: Create Virtual Environment```



```bash## Platform-Specific Installation

python3 -m venv .venv

source .venv/bin/activate  # macOS/Linux### macOS

# or```bash

.venv\Scripts\activate     # Windowsbrew install python@3.10 chromium

```python3.10 -m venv venv

source venv/bin/activate

### Step 3: Install Dependenciespip install -e .

```

```bash

pip install -r requirements.txt### Linux (Ubuntu/Debian)

``````bash

sudo apt update && sudo apt install python3.10 python3-pip python3-venv chromium-browser

### Step 4: Install Playwright Browserspython3.10 -m venv venv

source venv/bin/activate

```bashpip install -e .

playwright install chromium```

```

### Windows

### Step 5: Verify Installation```bash

# Install Python 3.10+ from python.org

```bashpython -m venv venv

python -c "from bob import HybridExtractorOptimized; print('✅ Ready!')"venv\Scripts\activate

```pip install -e .

```

## Platform-Specific Notes

## Docker Installation

### macOS

```bash

```bashdocker build -t bob-google-maps .

# If you need to install Pythondocker run -it bob-google-maps

brew install python@3.11```



# Then follow manual installation## Configuration

```

Create `config.yaml` in project root:

### Ubuntu/Debian

```yaml

```bashextraction:

# Install Python and dependencies  default_engine: "hybrid"

sudo apt update  timeout: 30

sudo apt install python3.11 python3.11-venv python3-pip  max_concurrent: 3



# Playwright may need additional librariesmemory:

playwright install-deps chromium  optimized: true



# Then follow manual installationcache:

```  enabled: true

  expiration_hours: 24

### Windows```



1. Install Python 3.11+ from [python.org](https://python.org)## Troubleshooting

2. Open PowerShell or Command Prompt

3. Follow manual installation steps### Chrome not found

- **macOS:** `brew install chromium`

## Docker Installation- **Linux:** `sudo apt install chromium-browser`

- **Windows:** Download from https://www.chromium.org/

```bash

docker build -t bob-google-maps .### Import errors

docker run -it bob-google-maps python -m bob "Starbucks NYC"```bash

```pip install --upgrade -e ".[dev]"

```

Or with docker-compose:

### Out of memory

```bash```python

docker-compose up --buildfrom bob import HybridExtractorOptimized

```extractor = HybridExtractorOptimized(memory_optimized=True, max_concurrent=1)

```

## Troubleshooting

## Development Setup

### "playwright not found"

```bash

```bashpip install -e ".[dev]"

pip install playwrightpytest tests/ -v

playwright install chromiumblack bob/ && flake8 bob/

``````



### "ModuleNotFoundError: No module named 'psutil'"## Next Steps



```bash1. Read [QUICKSTART.md](QUICKSTART.md)

pip install psutil2. Check [examples/](../examples/)

```3. See [API_REFERENCE.md](API_REFERENCE.md)



### Browser fails to launch---



```bash**Ready to extract business data!** Start with [QUICKSTART.md](QUICKSTART.md).

# Install browser dependencies (Linux)
playwright install-deps chromium
```

### Permission denied on setup.sh

```bash
chmod +x setup.sh
./setup.sh
```

## Verifying Everything Works

```bash
# Run unit tests
python -m pytest tests/unit/ -v

# Quick extraction test
python -m bob "Starbucks Times Square NYC"
```

Expected output:
```
🔱 BOB GOOGLE MAPS v4.3.0 - PRODUCTION EDITION
✅ Extraction successful
Name: Starbucks
Quality: 95/100
```

---

**v4.3.0** | December 5, 2025
