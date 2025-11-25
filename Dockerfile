# Production Dockerfile for FastAPI + Selenium (Local Chrome)
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including Chrome, virtual display and dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    chromium \
    chromium-driver \
    xvfb \
    x11-utils \
    libxss1 \
    fonts-liberation \
    libappindicator3-1 \
    libatk-bridge2.0-0 \
    libatspi2.0-0 \
    libgtk-3-0 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-xlib-2.0-0 \
    libdbus-1-3 \
    libcups2 \
    libpulse0 \
    lsb-release \
    xdg-utils \
    wget \
    ca-certificates \
    libnss3 \
    libxrandr2 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libx11-6 \
    libxcb1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .
COPY scraper.py .

# Create data directory
RUN mkdir -p data

# Expose port
EXPOSE 8000

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:99

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/status')" || exit 1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
