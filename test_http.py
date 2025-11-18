#!/usr/bin/env python3
"""
Quick test of the HTTP scraper - Run this first to test connectivity
"""

import sys
import requests

print("="*60)
print("Testing HTTP Connection to EGX")
print("="*60)
print()

# Test basic connectivity
print("1. Testing basic internet connectivity...")
try:
    response = requests.head("https://www.google.com", timeout=5)
    print(f"   ✓ Google reachable (Status: {response.status_code})")
except Exception as e:
    print(f"   ✗ Cannot reach Google: {str(e)}")
    print("   No internet connection!")
    sys.exit(1)

print()

# Test EGX connectivity
print("2. Testing EGX website connectivity...")
try:
    response = requests.head(
        "https://www.egx.com.eg",
        timeout=10,
        allow_redirects=True
    )
    print(f"   ✓ EGX reachable (Status: {response.status_code})")
except Exception as e:
    print(f"   ✗ Cannot reach EGX: {str(e)}")
    print("   Website might be down or blocking requests")

print()

# Test with proper headers
print("3. Testing EGX with browser headers...")
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
try:
    response = requests.get(
        "https://www.egx.com.eg/ar/prices.aspx",
        headers=headers,
        timeout=15
    )
    print(f"   ✓ EGX prices page reachable (Status: {response.status_code})")
    print(f"   Response size: {len(response.text)} bytes")
    
    # Check if page has table data
    if '<table' in response.text:
        print("   ✓ Found table data in response")
    else:
        print("   ⚠ No table data found in response")
        
except Exception as e:
    print(f"   ✗ Failed: {str(e)}")

print()
print("="*60)
print()

# Now try the HTTP scraper
print("4. Testing HTTP scraper...")
try:
    from http_scraper import scrape_with_requests
    df, filename = scrape_with_requests()
    
    if df is not None and not df.empty:
        print(f"✓ SUCCESS! Scraped {len(df)} stocks")
        print(f"✓ Saved to: {filename}")
    else:
        print("✗ Scraper returned empty data")
        
except ImportError as e:
    print(f"✗ Cannot import http_scraper: {str(e)}")
    print("  Make sure http_scraper.py exists in the project directory")
except Exception as e:
    print(f"✗ Scraper failed: {str(e)}")

print()
print("="*60)
