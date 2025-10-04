# BOB Google Maps V3.0 - Production Dockerfile
# Author: Divyanshu Singh Chouhan
# Release: October 3, 2025

FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
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

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN python -m playwright install chromium
RUN python -m playwright install-deps

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/cache /app/logs /app/data /app/exports

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV BOB_HEADLESS=true
ENV BOB_CACHE_ENABLED=true
ENV BOB_LOG_LEVEL=INFO

# Expose port (if running as API server in future)
EXPOSE 8000

# Default command
CMD ["python", "bob_maps_ultimate.py", "--help"]
