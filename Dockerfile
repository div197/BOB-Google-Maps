# BOB Google Maps V3.0.1 - Production Dockerfile
# Author: Divyanshu Singh Chouhan
# Release: October 3, 2025
# Updated: October 4, 2025 (Fixed Docker browser configuration)
#
# FIXES APPLIED (Oct 2025 Research):
# 1. PLAYWRIGHT_BROWSERS_PATH set BEFORE browser installation
# 2. Package installed BEFORE browsers
# 3. Chromium binary configured for Selenium
# 4. Proper installation order for reliability

FROM python:3.10-slim

# Set working directory
WORKDIR /app

# CRITICAL FIX #1: Set Playwright browser path BEFORE any installation
# Source: Playwright official Docker documentation
ENV PLAYWRIGHT_BROWSERS_PATH=/app/ms-playwright
ENV PYTHONUNBUFFERED=1

# Install system dependencies for Playwright & Selenium
# Including Chromium and ChromeDriver for Selenium support
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    chromium \
    chromium-driver \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libwayland-client0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# CRITICAL FIX #2: Set Chrome binary location for Selenium
# Source: SeleniumHQ docker-selenium documentation
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Copy requirements first for better Docker caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# CRITICAL FIX #3: Copy and install package BEFORE installing browsers
# This ensures Playwright can find correct browser versions
# Source: GitHub playwright issues, Stack Overflow solutions
COPY bob_v3/ ./bob_v3/
COPY tests/ ./tests/
COPY pyproject.toml .
COPY setup.py .
COPY *.md ./
COPY scripts/ ./scripts/
COPY config.yaml .
COPY .env.example .

# Install BOB package in editable mode
RUN pip install --no-cache-dir -e .

# CRITICAL FIX #4: Install Playwright browsers AFTER package installation
# Use --with-deps to install browser dependencies
# Source: Playwright Python documentation
RUN python -m playwright install --with-deps chromium

# Create necessary directories with correct permissions
RUN mkdir -p /app/cache /app/logs /app/data /app/exports /app/ms-playwright && \
    chmod 777 /app/cache /app/logs /app/data /app/exports /app/ms-playwright

# Set environment variables (can be overridden via docker-compose)
ENV BOB_HEADLESS=true \
    BOB_CACHE_ENABLED=true \
    BOB_CACHE_PATH=/app/cache/bob_cache.db \
    BOB_LOG_LEVEL=INFO \
    BOB_MAX_CONCURRENT=10 \
    BOB_PARALLEL_ENABLED=true

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import bob_v3; print('healthy')" || exit 1

# Default command - show help
CMD ["python", "-m", "bob_v3", "--help"]
