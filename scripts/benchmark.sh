#!/bin/bash
################################################################################
# BOB Google Maps - Benchmark Script
#
# This script runs performance benchmarks
#
# Author: BOB Google Maps Team
# Version: 4.2.0
################################################################################

set -e

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
NC='\033[0m'

echo "🔱 BOB Google Maps - Performance Benchmark"
echo "════════════════════════════════════════════"
echo ""

# Create results directory
mkdir -p benchmarks/results
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RESULTS_FILE="benchmarks/results/benchmark_${TIMESTAMP}.txt"

# Start benchmark
echo -e "${BLUE}⏱️  Running performance benchmarks...${NC}"
echo ""

# Redirect output to both console and file
{
    echo "Benchmark Results - $(date)"
    echo "════════════════════════════════════════════"
    echo ""

    # Benchmark 1: Import speed
    echo "1. Import Speed Test"
    echo "────────────────────"
    time python -c "from bob import HybridExtractor"
    echo ""

    # Benchmark 2: Extractor initialization
    echo "2. Extractor Initialization"
    echo "───────────────────────────"
    time python -c "from bob import HybridExtractor; e = HybridExtractor()"
    echo ""

    # Benchmark 3: Cache performance
    echo "3. Cache Performance"
    echo "────────────────────"
    python -c "
from bob.cache.cache_manager import CacheManager
import time

cache = CacheManager('bob_cache_ultimate.db')
start = time.time()
stats = cache.get_stats()
elapsed = time.time() - start
print(f'Cache stats query: {elapsed:.4f}s')
print(f'Total businesses: {stats[\"total_businesses\"]}')
"
    echo ""

    # Benchmark 4: Memory usage
    echo "4. Memory Usage"
    echo "───────────────"
    /usr/bin/time -v python -c "
from bob import HybridExtractor
extractor = HybridExtractor()
" 2>&1 | grep -E "Maximum resident|User time|System time"
    echo ""

    echo "════════════════════════════════════════════"
    echo "Benchmark completed at $(date)"

} | tee "$RESULTS_FILE"

echo ""
echo -e "${GREEN}✅ Benchmark complete!${NC}"
echo "Results saved to: $RESULTS_FILE"
