#!/bin/bash
# ============================================================================
# BOB Google Maps v4.3.0 - One-Click Enterprise Setup
# ============================================================================
# 
# This script sets up a complete, production-ready environment.
# 
# Usage:
#   chmod +x setup.sh
#   ./setup.sh
#
# What it does:
#   1. Creates a Python virtual environment
#   2. Installs all dependencies with exact versions
#   3. Installs Playwright browsers automatically
#   4. Verifies the installation
#   5. Runs a quick test to confirm everything works
#
# Author: BOB Google Maps Team
# Version: 4.3.0
# ============================================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "============================================================================"
echo "🔱 BOB GOOGLE MAPS v4.3.0 - ENTERPRISE SETUP"
echo "============================================================================"
echo -e "${NC}"

# Check Python version
echo -e "${YELLOW}📋 Checking Python version...${NC}"
PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 9 ]); then
    echo -e "${RED}❌ Python 3.9+ is required. Found: $PYTHON_VERSION${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python $PYTHON_VERSION detected${NC}"

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Step 1: Create virtual environment
echo ""
echo -e "${YELLOW}📦 Step 1/5: Creating virtual environment...${NC}"
if [ -d ".venv" ]; then
    echo "   Virtual environment already exists, recreating..."
    rm -rf .venv
fi
python3 -m venv .venv
echo -e "${GREEN}✅ Virtual environment created${NC}"

# Step 2: Activate virtual environment and upgrade pip
echo ""
echo -e "${YELLOW}🔧 Step 2/5: Setting up pip...${NC}"
source .venv/bin/activate
pip install --upgrade pip wheel setuptools > /dev/null 2>&1
echo -e "${GREEN}✅ Pip upgraded${NC}"

# Step 3: Install dependencies
echo ""
echo -e "${YELLOW}📥 Step 3/5: Installing dependencies...${NC}"
pip install -r requirements.txt
echo -e "${GREEN}✅ All dependencies installed${NC}"

# Step 4: Install Playwright browsers
echo ""
echo -e "${YELLOW}🌐 Step 4/5: Installing Playwright browsers...${NC}"
playwright install chromium
echo -e "${GREEN}✅ Playwright Chromium installed${NC}"

# Step 5: Verify installation
echo ""
echo -e "${YELLOW}🔍 Step 5/5: Verifying installation...${NC}"

# Test imports
python3 -c "
import sys
success = True
modules = ['selenium', 'playwright', 'psutil', 'requests']
for mod in modules:
    try:
        __import__(mod)
        print(f'  ✅ {mod}')
    except ImportError as e:
        print(f'  ❌ {mod}: {e}')
        success = False

# Test bob package
try:
    from bob.extractors.hybrid_optimized import HybridExtractorOptimized
    print('  ✅ bob package')
except Exception as e:
    print(f'  ❌ bob package: {e}')
    success = False

if not success:
    sys.exit(1)
"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ All imports verified${NC}"
else
    echo -e "${RED}❌ Import verification failed${NC}"
    exit 1
fi

# Run unit tests
echo ""
echo -e "${YELLOW}🧪 Running unit tests...${NC}"
python3 -m pytest tests/unit/ -v --tb=short -q 2>&1 | tail -5
echo -e "${GREEN}✅ Unit tests completed${NC}"

# Final summary
echo ""
echo -e "${BLUE}============================================================================${NC}"
echo -e "${GREEN}🎉 SETUP COMPLETE! BOB Google Maps v4.3.0 is ready.${NC}"
echo -e "${BLUE}============================================================================${NC}"
echo ""
echo -e "To activate the environment:"
echo -e "  ${YELLOW}source .venv/bin/activate${NC}"
echo ""
echo -e "Quick test:"
echo -e "  ${YELLOW}python -m bob \"Starbucks Times Square NYC\" --max-reviews 5${NC}"
echo ""
echo -e "For help:"
echo -e "  ${YELLOW}python -m bob --help${NC}"
echo ""
