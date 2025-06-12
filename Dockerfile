# BOB Google Maps v0.5.0 - Production Docker Image
# Enterprise-grade Google Maps scraper with fault tolerance
# Made with 🙏 following Niṣkāma Karma Yoga principles

FROM python:3.9-slim

# Metadata
LABEL maintainer="Divyanshu Singh Chouhan <divyanshu@abcsteps.com>"
LABEL version="0.5.0"
LABEL description="BOB Google Maps - Enterprise-grade Google Maps scraper"
LABEL org.opencontainers.image.source="https://github.com/div197/BOB-Google-Maps"

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome for Selenium
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Install ChromeDriver
RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` \
    && wget -N http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && rm chromedriver_linux64.zip \
    && mv chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver

# Create app directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and browsers
RUN pip install playwright \
    && playwright install chromium \
    && playwright install-deps

# Copy application code
COPY bob_core/ ./bob_core/
COPY examples/ ./examples/
COPY tests/ ./tests/
COPY pyproject.toml .
COPY README.md .
COPY CHANGELOG.md .
COPY LICENSE .

# Install BOB in development mode
RUN pip install -e .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash bob \
    && chown -R bob:bob /app
USER bob

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -m bob_core.health_cli status || exit 1

# Default command
CMD ["python", "-m", "bob_core.cli", "--help"]

# Usage examples:
# 
# Build:
# docker build -t bob-google-maps:0.5.0 .
#
# Run business-only extraction:
# docker run --rm bob-google-maps:0.5.0 python -m bob_core.cli single "https://maps.google.com/?q=restaurant&hl=en" --business-only
#
# Run with volume for output:
# docker run --rm -v $(pwd)/output:/app/output bob-google-maps:0.5.0 python examples/quick_start.py
#
# Interactive mode:
# docker run --rm -it bob-google-maps:0.5.0 /bin/bash
#
# Health check:
# docker run --rm bob-google-maps:0.5.0 python -m bob_core.health_cli status 