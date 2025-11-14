# 🔧 BOB Google Maps - Utility Scripts

This directory contains utility scripts for deployment, maintenance, and operations.

## Available Scripts

### 1. `deploy.sh` - Deployment Script
Handles deployment to different environments.

**Usage:**
```bash
# Deploy to production (with tests)
./scripts/deploy.sh production

# Deploy to staging (skip tests)
./scripts/deploy.sh staging true

# Deploy to development
./scripts/deploy.sh development
```

**Features:**
- Checks prerequisites
- Pulls latest code
- Sets up virtual environment
- Installs dependencies
- Runs tests (optional)
- Builds package
- Environment-specific deployment
- Health check

---

### 2. `backup_cache.sh` - Cache Backup
Creates backups of the cache database with automatic retention management.

**Usage:**
```bash
# Create backup
./scripts/backup_cache.sh
```

**Features:**
- Creates timestamped backup
- Compresses backup with gzip
- Automatic cleanup (30-day retention)
- Shows backup history

**Backup Location:** `backups/cache/`

---

### 3. `clean_cache.sh` - Cache Cleaning
Cleans expired entries from the cache database.

**Usage:**
```bash
# Clean entries older than 30 days (default)
./scripts/clean_cache.sh

# Clean entries older than 7 days
./scripts/clean_cache.sh 7
```

**Features:**
- Creates automatic backup before cleaning
- Removes expired entries
- Runs VACUUM to reclaim space
- Shows before/after statistics

---

### 4. `run_tests.sh` - Test Runner
Runs comprehensive test suite with various options.

**Usage:**
```bash
# Run all tests with coverage
./scripts/run_tests.sh all true

# Run unit tests only
./scripts/run_tests.sh unit

# Run integration tests without coverage
./scripts/run_tests.sh integration false

# Run fast tests only
./scripts/run_tests.sh fast

# Run end-to-end tests
./scripts/run_tests.sh e2e
```

**Test Types:**
- `all` - All tests (default)
- `unit` - Unit tests only
- `integration` - Integration tests only
- `e2e` - End-to-end tests only
- `fast` - Fast tests only (excludes slow tests)

**Features:**
- Coverage reporting (HTML + terminal)
- Parallel test execution
- Detailed failure output

---

### 5. `benchmark.sh` - Performance Benchmarking
Runs performance benchmarks and generates reports.

**Usage:**
```bash
# Run benchmarks
./scripts/benchmark.sh
```

**Benchmarks:**
1. Import speed test
2. Extractor initialization
3. Cache performance
4. Memory usage analysis

**Results Location:** `benchmarks/results/benchmark_YYYYMMDD_HHMMSS.txt`

---

## Making Scripts Executable

```bash
# Make all scripts executable
chmod +x scripts/*.sh

# Make individual script executable
chmod +x scripts/deploy.sh
```

---

## Script Requirements

### All Scripts
- Bash shell
- Linux/Unix environment

### Deployment Script
- Python 3.8+
- pip
- git
- Playwright
- Docker (optional)

### Cache Scripts
- sqlite3 command-line tool
- gzip

### Test Runner
- pytest
- pytest-cov
- pytest-xdist

### Benchmark Script
- Python 3.8+
- GNU time utility

---

## Best Practices

### 1. Always Backup Before Major Operations
```bash
# Before cleaning cache
./scripts/backup_cache.sh
./scripts/clean_cache.sh
```

### 2. Test Before Deployment
```bash
# Run tests first
./scripts/run_tests.sh all

# Then deploy
./scripts/deploy.sh production
```

### 3. Monitor Performance
```bash
# Run benchmarks regularly
./scripts/benchmark.sh

# Compare results over time
diff benchmarks/results/benchmark_old.txt benchmarks/results/benchmark_new.txt
```

### 4. Regular Maintenance
```bash
# Weekly cache backup
./scripts/backup_cache.sh

# Monthly cache cleaning
./scripts/clean_cache.sh 90
```

---

## Automation with Cron

### Example Crontab Entries

```cron
# Daily cache backup at 2 AM
0 2 * * * /path/to/BOB-Google-Maps/scripts/backup_cache.sh

# Weekly cache cleaning (Sunday 3 AM)
0 3 * * 0 /path/to/BOB-Google-Maps/scripts/clean_cache.sh 30

# Monthly performance benchmark (1st of month, 4 AM)
0 4 1 * * /path/to/BOB-Google-Maps/scripts/benchmark.sh
```

**Setup:**
```bash
# Edit crontab
crontab -e

# Add entries above
# Save and exit
```

---

## Troubleshooting

### Script Permission Denied
```bash
chmod +x scripts/script_name.sh
```

### Python Not Found
```bash
# Update script shebang or use full path
which python3
# Then update script: #!/usr/bin/python3.10
```

### Database Locked Error
```bash
# Stop any running BOB processes
pkill -f "python.*bob"

# Then retry script
```

### Out of Disk Space
```bash
# Clean old backups
find backups/cache -name "*.gz" -mtime +30 -delete

# Clean old benchmark results
find benchmarks/results -name "*.txt" -mtime +90 -delete
```

---

## Environment Variables

Scripts respect these environment variables:

```bash
# Python executable
export PYTHON_BIN=/usr/bin/python3.10

# Cache database path
export BOB_CACHE_DB=./bob_cache_ultimate.db

# Backup directory
export BOB_BACKUP_DIR=./backups

# Test options
export PYTEST_ADDOPTS="--tb=short -v"
```

---

## Contributing

To add a new script:

1. Create script in `scripts/` directory
2. Add shebang line: `#!/bin/bash`
3. Add header comment with description
4. Make executable: `chmod +x scripts/your_script.sh`
5. Document in this README
6. Test thoroughly before committing

---

## Security Considerations

- Scripts should not contain hardcoded credentials
- Use environment variables for sensitive data
- Review scripts before execution
- Run scripts with appropriate permissions
- Backup before destructive operations

---

**🔱 JAI SHREE KRISHNA!**
*Built with Nishkaam Karma Yoga principles*

---

**Version:** 4.2.0
**Last Updated:** November 14, 2025
