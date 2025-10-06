#!/bin/bash
# BOB Google Maps V3.0.1 - Automated Setup Script
# Author: Divyanshu Singh Chouhan
# Platform: Linux/macOS

set -e  # Exit on error

echo "🔱 BOB Google Maps V3.0.1 - Automated Setup"
echo "==========================================="
echo ""

# Detect OS
OS="$(uname -s)"
case "${OS}" in
    Linux*)     MACHINE=Linux;;
    Darwin*)    MACHINE=Mac;;
    *)          MACHINE="UNKNOWN:${OS}"
esac

echo "📍 Detected OS: ${MACHINE}"
echo ""

# Check Python version
echo "🐍 Checking Python version..."
PYTHON_CMD=""
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    PYTHON_CMD="python3"
    echo "✅ Python ${PYTHON_VERSION} found"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version | cut -d' ' -f2)
    PYTHON_CMD="python"
    echo "✅ Python ${PYTHON_VERSION} found"
else
    echo "❌ Python not found. Please install Python 3.10+"
    exit 1
fi

# Check if Python version is 3.10+
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]); then
    echo "❌ Python 3.10+ required. Found: ${PYTHON_VERSION}"
    exit 1
fi

echo ""
echo "📦 Installing BOB package..."
$PYTHON_CMD -m pip install -e . --quiet

echo ""
echo "🎭 Installing Playwright browsers..."
$PYTHON_CMD -m playwright install chromium --quiet

echo ""
echo "🔧 Verifying installation..."
$PYTHON_CMD -c "from bob_v3 import __version__; print(f'✅ BOB v{__version__} installed successfully')"

echo ""
echo "🎉 Setup Complete!"
echo ""
echo "📋 Quick Start:"
echo "  Single extraction:    python3 -m bob_v3 'Business Name'"
echo "  Batch extraction:     python3 -m bob_v3 --batch urls.txt --parallel"
echo "  Docker deployment:    docker compose up -d"
echo ""
echo "📚 Documentation: README.md"
echo "🔱 Jai Shree Krishna!"
