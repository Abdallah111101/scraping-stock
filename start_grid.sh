#!/bin/bash
# Quick start script for Selenium Grid on Railway/Docker

set -e

echo "=================================================="
echo "EGX Stock Scraper - Selenium Grid Setup"
echo "=================================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

echo "✓ Docker found"

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install it first."
    exit 1
fi

echo "✓ Docker Compose found"
echo ""

# Menu
echo "Select action:"
echo "1) Start Selenium Grid locally"
echo "2) Stop Selenium Grid"
echo "3) View Grid status"
echo "4) Run scraper (local grid)"
echo "5) View Grid dashboard"
echo "6) Check Grid logs"
echo ""
read -p "Enter choice (1-6): " choice

case $choice in
    1)
        echo ""
        echo "Starting Selenium Grid with Chrome, Firefox, and Edge nodes..."
        docker-compose up -d
        
        echo ""
        echo "⏳ Waiting for Grid to be ready (30 seconds)..."
        sleep 30
        
        echo ""
        echo "✓ Selenium Grid started!"
        echo "📊 Dashboard: http://localhost:4444"
        echo ""
        echo "Services running:"
        docker-compose ps
        ;;
    
    2)
        echo ""
        echo "Stopping Selenium Grid..."
        docker-compose down
        echo "✓ Grid stopped"
        ;;
    
    3)
        echo ""
        echo "Checking Selenium Grid status..."
        
        if curl -s http://localhost:4444/status | grep -q "ready"; then
            echo "✓ Grid is ready!"
            curl -s http://localhost:4444/status | python -m json.tool
        else
            echo "❌ Grid is not ready or not running"
            echo "Start it with: bash start_grid.sh"
        fi
        ;;
    
    4)
        echo ""
        echo "Running scraper with local Selenium Grid..."
        
        if ! curl -s http://localhost:4444/status | grep -q "ready"; then
            echo "❌ Grid is not running!"
            echo "Start it first: bash start_grid.sh"
            exit 1
        fi
        
        export SELENIUM_GRID_URL=http://localhost:4444
        python selenium_grid_railway.py
        ;;
    
    5)
        echo ""
        echo "Opening Grid Dashboard at http://localhost:4444"
        
        # Try to open browser (works on most systems)
        if command -v xdg-open &> /dev/null; then
            xdg-open http://localhost:4444
        elif command -v open &> /dev/null; then
            open http://localhost:4444
        else
            echo "Please open http://localhost:4444 in your browser"
        fi
        ;;
    
    6)
        echo ""
        echo "Selenium Hub logs:"
        docker-compose logs -f selenium-hub
        ;;
    
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
