# Dockerfile for EGX Stock Scraper with Selenium Grid support on Railway

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies (includes openpyxl)
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY selenium_grid_railway.py .
COPY config.ini .

# Create excel_files directory
RUN mkdir -p /app/excel_files

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV SELENIUM_GRID_URL=http://selenium-hub:4444

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:4444/status')" || exit 1

# Run the scraper
CMD ["python", "selenium_grid_railway.py"]
