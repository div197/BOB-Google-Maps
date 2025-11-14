#!/bin/bash
################################################################################
# BOB Google Maps - Cache Cleaning Script
#
# This script cleans expired entries from the cache database
#
# Author: BOB Google Maps Team
# Version: 4.2.0
################################################################################

set -e

CACHE_DB="bob_cache_ultimate.db"
EXPIRY_DAYS=${1:-30}

echo "🔱 BOB Google Maps - Cache Cleaning Script"
echo "════════════════════════════════════════"

if [ ! -f "$CACHE_DB" ]; then
    echo "❌ Cache database not found: $CACHE_DB"
    exit 1
fi

# Get current size
BEFORE_SIZE=$(du -h "$CACHE_DB" | cut -f1)
BEFORE_ENTRIES=$(sqlite3 "$CACHE_DB" "SELECT COUNT(*) FROM businesses;" 2>/dev/null || echo "0")

echo "📊 Current state:"
echo "   Database size: $BEFORE_SIZE"
echo "   Total entries: $BEFORE_ENTRIES"
echo ""

# Create backup first
echo "📦 Creating backup..."
cp "$CACHE_DB" "${CACHE_DB}.backup"
echo "✅ Backup created: ${CACHE_DB}.backup"
echo ""

# Clean expired entries
echo "🧹 Cleaning entries older than $EXPIRY_DAYS days..."
EXPIRY_TIMESTAMP=$(date -d "$EXPIRY_DAYS days ago" +%s)

sqlite3 "$CACHE_DB" "DELETE FROM businesses WHERE extracted_at < datetime($EXPIRY_TIMESTAMP, 'unixepoch');"
sqlite3 "$CACHE_DB" "VACUUM;"

# Get new statistics
AFTER_SIZE=$(du -h "$CACHE_DB" | cut -f1)
AFTER_ENTRIES=$(sqlite3 "$CACHE_DB" "SELECT COUNT(*) FROM businesses;")
REMOVED=$((BEFORE_ENTRIES - AFTER_ENTRIES))

echo ""
echo "📊 Cleanup results:"
echo "   Entries removed: $REMOVED"
echo "   Entries remaining: $AFTER_ENTRIES"
echo "   Size before: $BEFORE_SIZE"
echo "   Size after: $AFTER_SIZE"

echo ""
echo "════════════════════════════════════════"
echo "✅ Cache cleaning completed!"
