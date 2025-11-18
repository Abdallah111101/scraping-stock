#!/usr/bin/env python3
"""
Diagnostic tool to test connection and Chrome driver
Run this before running main.py to ensure everything works
"""

import sys
import time
from datetime import datetime

print("="*60)
print("Stock Scraper Diagnostic Tool")
print("="*60)
print(f"Time: {datetime.now()}")
print()

# Test 1: Check Python version
print("1. Checking Python version...")
print(f"   Python {sys.version}")
print(f"   ✓ OK" if sys.version_info >= (3, 8) else "   ✗ FAILED - Python 3.8+ required")
print()

# Test 2: Check network connectivity
print("2. Checking network connectivity...")
try:
    import requests
    response = requests.head("https://www.google.com", timeout=5)
    print(f"   ✓ OK - Google: {response.status_code}")
except Exception as e:
    print(f"   ✗ FAILED - {str(e)}")
print()

# Test 3: Check EGX website
print("3. Checking EGX website connectivity...")
try:
    import requests
    response = requests.head("https://www.egx.com.eg", timeout=10, allow_redirects=True)
    print(f"   ✓ OK - EGX: {response.status_code}")
except Exception as e:
    print(f"   ✗ FAILED - {str(e)}")
    print("   Note: Website might be down or blocking requests")
print()

# Test 4: Check Chrome/ChromeDriver
print("4. Checking Chrome/ChromeDriver...")
try:
    from selenium import webdriver
    print("   - Selenium installed ✓")
    
    # Try to find Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    print("   - Attempting to initialize Chrome driver...")
    driver = webdriver.Chrome(options=options)
    print("   ✓ OK - Chrome driver initialized")
    driver.quit()
except Exception as e:
    print(f"   ✗ FAILED - {str(e)}")
    print()
    print("   SOLUTION:")
    print("   1. Download ChromeDriver from: https://chromedriver.chromium.org/")
    print("   2. Place it in your project directory")
    print("   3. Or add it to system PATH")
print()

# Test 5: Check dependencies
print("5. Checking Python dependencies...")
dependencies = ['fastapi', 'uvicorn', 'selenium', 'pandas', 'openpyxl', 'requests']
missing = []

for dep in dependencies:
    try:
        __import__(dep)
        print(f"   ✓ {dep}")
    except ImportError:
        print(f"   ✗ {dep} - MISSING")
        missing.append(dep)

if missing:
    print()
    print("   SOLUTION: Run this command to install missing packages:")
    print(f"   pip install {' '.join(missing)}")
print()

# Test 6: Check file permissions
print("6. Checking file permissions...")
try:
    import os
    os.makedirs("excel_files", exist_ok=True)
    test_file = os.path.join("excel_files", ".test")
    with open(test_file, 'w') as f:
        f.write("test")
    os.remove(test_file)
    print("   ✓ OK - Can read/write in project directory")
except Exception as e:
    print(f"   ✗ FAILED - {str(e)}")
print()

print("="*60)
print("Diagnostic complete!")
print("="*60)
print()
print("If all tests passed, you can run: python main.py")
print()
