#!/bin/bash
################################################################################
# BOB Google Maps - Cache Backup Script
#
# This script creates backups of the BOB cache database
#
# Author: BOB Google Maps Team
# Version: 4.2.0
################################################################################

set -e

# Configuration
CACHE_DB="bob_cache_ultimate.db"
BACKUP_DIR="backups/cache"
RETENTION_DAYS=30

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "🔱 BOB Google Maps - Cache Backup Script"
echo "════════════════════════════════════════"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Generate backup filename with timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/bob_cache_${TIMESTAMP}.db"

# Check if cache database exists
if [ ! -f "$CACHE_DB" ]; then
    echo -e "${YELLOW}⚠️  Cache database not found: $CACHE_DB${NC}"
    exit 1
fi

# Get database size
DB_SIZE=$(du -h "$CACHE_DB" | cut -f1)

# Create backup
echo "📦 Creating backup..."
echo "   Source: $CACHE_DB ($DB_SIZE)"
echo "   Destination: $BACKUP_FILE"

cp "$CACHE_DB" "$BACKUP_FILE"

# Compress backup
echo "🗜️  Compressing backup..."
gzip "$BACKUP_FILE"
COMPRESSED_SIZE=$(du -h "${BACKUP_FILE}.gz" | cut -f1)

echo -e "${GREEN}✅ Backup created successfully!${NC}"
echo "   Compressed size: $COMPRESSED_SIZE"

# Clean up old backups
echo ""
echo "🧹 Cleaning up old backups (>$RETENTION_DAYS days)..."
find "$BACKUP_DIR" -name "bob_cache_*.db.gz" -mtime +$RETENTION_DAYS -delete
REMAINING=$(ls -1 "$BACKUP_DIR" | wc -l)
echo -e "${GREEN}✅ Cleanup complete. $REMAINING backups remaining.${NC}"

# Show backup list
echo ""
echo "📋 Recent backups:"
ls -lht "$BACKUP_DIR" | head -6

echo ""
echo "════════════════════════════════════════"
echo -e "${GREEN}✅ Backup completed successfully!${NC}"
