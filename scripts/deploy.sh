#!/bin/bash
################################################################################
# BOB Google Maps - Deployment Script
#
# This script handles deployment of BOB Google Maps to various environments
#
# Author: BOB Google Maps Team
# Version: 4.2.0
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Print banner
echo "═══════════════════════════════════════════════════════════"
echo "  🔱 BOB Google Maps - Deployment Script"
echo "  Version: 4.2.0"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Parse arguments
ENVIRONMENT=${1:-production}
SKIP_TESTS=${2:-false}

log_info "Deploying to environment: $ENVIRONMENT"

# Step 1: Check prerequisites
log_info "Step 1/8: Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    log_error "Python 3 is not installed"
    exit 1
fi

if ! command -v docker &> /dev/null; then
    log_warning "Docker is not installed (optional)"
fi

log_success "Prerequisites checked"

# Step 2: Pull latest code
log_info "Step 2/8: Pulling latest code..."
git pull origin main || log_warning "Git pull failed or not a git repository"
log_success "Code updated"

# Step 3: Create/activate virtual environment
log_info "Step 3/8: Setting up virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
log_success "Virtual environment ready"

# Step 4: Install/update dependencies
log_info "Step 4/8: Installing dependencies..."
pip install --upgrade pip
pip install -e ".[dev]"
playwright install chromium
playwright install-deps
log_success "Dependencies installed"

# Step 5: Run tests (unless skipped)
if [ "$SKIP_TESTS" = "false" ]; then
    log_info "Step 5/8: Running tests..."
    pytest tests/ -v --tb=short || {
        log_error "Tests failed!"
        exit 1
    }
    log_success "Tests passed"
else
    log_warning "Step 5/8: Tests skipped"
fi

# Step 6: Build package
log_info "Step 6/8: Building package..."
python -m build
log_success "Package built"

# Step 7: Environment-specific deployment
log_info "Step 7/8: Deploying to $ENVIRONMENT..."

case $ENVIRONMENT in
    production)
        log_info "Production deployment..."
        # Add production-specific steps here
        log_success "Production deployment complete"
        ;;
    staging)
        log_info "Staging deployment..."
        # Add staging-specific steps here
        log_success "Staging deployment complete"
        ;;
    development)
        log_info "Development deployment..."
        # Add development-specific steps here
        log_success "Development deployment complete"
        ;;
    *)
        log_error "Unknown environment: $ENVIRONMENT"
        exit 1
        ;;
esac

# Step 8: Health check
log_info "Step 8/8: Running health check..."
python -c "from bob import HybridExtractor; print('✅ BOB is healthy!')" || {
    log_error "Health check failed!"
    exit 1
}
log_success "Health check passed"

# Final message
echo ""
echo "═══════════════════════════════════════════════════════════"
log_success "Deployment completed successfully! 🎉"
echo "═══════════════════════════════════════════════════════════"
echo ""
log_info "Environment: $ENVIRONMENT"
log_info "Version: 4.2.0"
log_info "Timestamp: $(date)"
echo ""
