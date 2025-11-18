#!/bin/bash
# Stock Scraper Startup Script for macOS/Linux

echo ""
echo "========================================"
echo "Stock Scraper - FastAPI Application"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    echo "Please install Python from https://www.python.org"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
if ! pip show fastapi &> /dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Run the application
echo ""
echo "Starting Stock Scraper Application..."
echo ""
echo "The application will be available at: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

python main.py

