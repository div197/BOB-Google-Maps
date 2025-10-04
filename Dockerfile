# BOB Google Maps V3.0.1 - Production Dockerfile
# Author: Divyanshu Singh Chouhan
# Release: October 3, 2025
# Updated: October 4, 2025 (Refactored)

FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies for Playwright & Selenium
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
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

# Copy requirements first for better Docker caching
COPY requirements.txt .
COPY pyproject.toml .
COPY setup.py .

# Install BOB package
RUN pip install --no-cache-dir -e .

# Install Playwright browsers
RUN python -m playwright install chromium chromium-headless-shell
RUN python -m playwright install-deps

# Copy application code
COPY bob_v3/ ./bob_v3/
COPY tests/ ./tests/
COPY *.md ./
COPY *.sh ./
COPY config.yaml .
COPY .env.example .

# Create necessary directories with correct permissions
RUN mkdir -p /app/cache /app/logs /app/data /app/exports && \
    chmod 777 /app/cache /app/logs /app/data /app/exports

# Set environment variables (can be overridden via docker-compose)
ENV PYTHONUNBUFFERED=1 \
    BOB_HEADLESS=true \
    BOB_CACHE_ENABLED=true \
    BOB_CACHE_PATH=/app/cache/bob_cache.db \
    BOB_LOG_LEVEL=INFO \
    BOB_MAX_CONCURRENT=10 \
    BOB_PARALLEL_ENABLED=true \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import bob_v3; print('healthy')" || exit 1

# Default command - show help
CMD ["python", "-m", "bob_v3", "--help"]
