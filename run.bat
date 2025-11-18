@echo off
REM Stock Scraper Startup Script for Windows

echo.
echo ========================================
echo Stock Scraper - FastAPI Application
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if requirements are installed
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Run the application
echo.
echo Starting Stock Scraper Application...
echo.
echo The application will be available at: http://localhost:8000
echo.
echo Press Ctrl+C to stop the application
echo.

python main.py

pause
