# BOB Google Maps - State-of-the-Art Production Dockerfile
# Author: Divyanshu Singh Chouhan
# Release: October 7, 2025
# Built with Nishkaam Karma Yoga principles - Ultimate optimization through minimal resource usage

FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Set Playwright browser path BEFORE any installation
ENV PLAYWRIGHT_BROWSERS_PATH=/app/ms-playwright
ENV PYTHONUNBUFFERED=1

# Install system dependencies for optimized Playwright & Selenium
# Minimal footprint for memory optimization
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

# Set Chrome binary location for optimized Selenium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Copy requirements first for better Docker caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy optimized BOB package structure
COPY bob/ ./bob/
COPY tests/ ./tests/
COPY pyproject.toml .
COPY setup.py .
COPY *.md ./
COPY scripts/ ./scripts/
COPY config.yaml .
COPY .env.example .

# Install BOB package in editable mode
RUN pip install --no-cache-dir -e .

# Install Playwright browsers AFTER package installation
RUN python -m playwright install --with-deps chromium

# Create necessary directories with correct permissions
RUN mkdir -p /app/cache /app/logs /app/data /app/exports /app/ms-playwright && \
    chmod 777 /app/cache /app/logs /app/data /app/exports /app/ms-playwright

# Set environment variables for optimized extraction
ENV BOB_HEADLESS=true \
    BOB_MEMORY_OPTIMIZED=true \
    BOB_CACHE_ENABLED=false \
    BOB_LOG_LEVEL=INFO \
    BOB_MAX_CONCURRENT=3 \
    BOB_PARALLEL_ENABLED=true

# Healthcheck for optimized system
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import bob; print('Optimized system healthy')" || exit 1

# Default command - show help
CMD ["python", "-m", "bob", "--help"]
