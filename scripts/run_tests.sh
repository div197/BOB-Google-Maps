#!/bin/bash
################################################################################
# BOB Google Maps - Test Runner Script
#
# This script runs comprehensive test suite with options
#
# Author: BOB Google Maps Team
# Version: 4.2.0
################################################################################

set -e

# Configuration
TEST_TYPE=${1:-all}
COVERAGE=${2:-true}

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "🔱 BOB Google Maps - Test Runner"
echo "════════════════════════════════════════"
echo ""

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo -e "${RED}❌ pytest is not installed${NC}"
    echo "Installing pytest..."
    pip install pytest pytest-cov pytest-xdist
fi

# Determine test path and options
PYTEST_ARGS="-v --tb=short"

if [ "$COVERAGE" = "true" ]; then
    PYTEST_ARGS="$PYTEST_ARGS --cov=bob --cov-report=term-missing --cov-report=html"
fi

case $TEST_TYPE in
    unit)
        echo -e "${BLUE}🧪 Running unit tests...${NC}"
        TEST_PATH="tests/unit/"
        ;;
    integration)
        echo -e "${BLUE}🔗 Running integration tests...${NC}"
        TEST_PATH="tests/integration/"
        ;;
    e2e)
        echo -e "${BLUE}🚀 Running end-to-end tests...${NC}"
        TEST_PATH="tests/e2e/"
        ;;
    fast)
        echo -e "${BLUE}⚡ Running fast tests only...${NC}"
        TEST_PATH="tests/"
        PYTEST_ARGS="$PYTEST_ARGS -m 'not slow'"
        ;;
    all)
        echo -e "${BLUE}🎯 Running all tests...${NC}"
        TEST_PATH="tests/"
        ;;
    *)
        echo -e "${RED}❌ Unknown test type: $TEST_TYPE${NC}"
        echo "Valid options: unit, integration, e2e, fast, all"
        exit 1
        ;;
esac

echo ""
echo "Test path: $TEST_PATH"
echo "Options: $PYTEST_ARGS"
echo ""
echo "════════════════════════════════════════"
echo ""

# Run tests
pytest $TEST_PATH $PYTEST_ARGS

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo "════════════════════════════════════════"
    echo -e "${GREEN}✅ All tests passed successfully!${NC}"
    if [ "$COVERAGE" = "true" ]; then
        echo ""
        echo "📊 Coverage report generated in htmlcov/"
    fi
else
    echo ""
    echo "════════════════════════════════════════"
    echo -e "${RED}❌ Some tests failed!${NC}"
    exit 1
fi
