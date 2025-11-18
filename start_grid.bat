@echo off
REM Quick start script for Selenium Grid on Railway/Docker (Windows)

setlocal enabledelayedexpansion

echo ==================================================
echo EGX Stock Scraper - Selenium Grid Setup
echo ==================================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo X Docker is not installed. Please install Docker Desktop first.
    exit /b 1
)

echo o Docker found

REM Check if docker-compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo X Docker Compose is not installed.
    exit /b 1
)

echo o Docker Compose found
echo.

REM Menu
echo Select action:
echo 1) Start Selenium Grid locally
echo 2) Stop Selenium Grid
echo 3) View Grid status
echo 4) Run scraper (local grid)
echo 5) View Grid logs
echo.
set /p choice="Enter choice (1-5): "

if "%choice%"=="1" (
    echo.
    echo Starting Selenium Grid with Chrome, Firefox, and Edge nodes...
    docker-compose up -d
    
    echo.
    echo Waiting for Grid to be ready (30 seconds^)...
    timeout /t 30 /nobreak
    
    echo.
    echo o Selenium Grid started!
    echo Dashboard: http://localhost:4444
    echo.
    echo Services running:
    docker-compose ps
    
) else if "%choice%"=="2" (
    echo.
    echo Stopping Selenium Grid...
    docker-compose down
    echo o Grid stopped
    
) else if "%choice%"=="3" (
    echo.
    echo Checking Selenium Grid status...
    
    curl -s http://localhost:4444/status >nul 2>&1
    if errorlevel 0 (
        echo o Grid is ready!
        curl -s http://localhost:4444/status
    ) else (
        echo X Grid is not running
        echo Start it with: start_grid.bat
    )
    
) else if "%choice%"=="4" (
    echo.
    echo Running scraper with local Selenium Grid...
    
    curl -s http://localhost:4444/status >nul 2>&1
    if errorlevel 1 (
        echo X Grid is not running!
        echo Start it first: start_grid.bat
        exit /b 1
    )
    
    set SELENIUM_GRID_URL=http://localhost:4444
    python selenium_grid_railway.py
    
) else if "%choice%"=="5" (
    echo.
    echo Showing Selenium Hub logs...
    docker-compose logs -f selenium-hub
    
) else (
    echo X Invalid choice
    exit /b 1
)

echo.
pause
