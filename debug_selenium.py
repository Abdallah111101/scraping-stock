#!/usr/bin/env python3
"""
Debug Selenium Script - See exactly what's happening
Run this to see the Chrome browser window and watch the scraping happen
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

print("="*70)
print("SELENIUM DEBUG TEST - Watch the browser window")
print("="*70)
print()

url = "https://www.egx.com.eg/ar/prices.aspx"

print("Step 1: Initializing Chrome driver...")
print("  - You WILL see a Chrome browser window appear")
print("  - DO NOT close it while the script runs")
print("  - Watch what happens on the website")
print()

options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
# NOT using --headless so you can see it!

driver = webdriver.Chrome(options=options)
driver.maximize_window()

try:
    print("Step 2: Navigating to EGX website...")
    print(f"  URL: {url}")
    print()
    
    driver.get(url)
    
    print("✓ Page loaded!")
    print(f"  Page title: {driver.title}")
    print(f"  Page URL: {driver.current_url}")
    print()
    
    # Wait for page to fully load
    time.sleep(5)
    
    print("Step 3: Looking for the button...")
    button_xpath = "/html/body/form/table/tbody/tr[2]/td/center/center/div/table/tbody/tr[4]/td/table[1]/tbody/tr[2]/td/div/div/ul/li[1]/a"
    
    try:
        button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, button_xpath))
        )
        print("✓ Button found!")
        
        print("Step 4: Clicking the button...")
        driver.execute_script("arguments[0].click();", button)
        print("✓ Button clicked!")
        
        time.sleep(3)
        
        # Check for alerts
        try:
            alert = driver.switch_to.alert
            print(f"⚠ Alert appeared: {alert.text}")
            alert.accept()
            print("✓ Alert dismissed")
        except:
            print("✓ No alert (good!)")
        
        print("Step 5: Waiting for table to load...")
        time.sleep(10)
        
        print("Step 6: Checking for table data...")
        tables = driver.find_elements(By.TAG_NAME, "table")
        print(f"✓ Found {len(tables)} tables on page")
        
        # Look for data
        rows = driver.find_elements(By.XPATH, "//table//tr")
        print(f"✓ Found {len(rows)} rows in tables")
        
        print()
        print("✓ SUCCESS - Website is working!")
        print("  The error might be specific to your network or firewall")
        print()
        
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")
        print()
        print("This means:")
        print("  1. The button couldn't be found (page structure changed)")
        print("  2. Or the website is down")
        print("  3. Or there's a network issue")
        
except Exception as e:
    print(f"✗ CRITICAL ERROR: {str(e)}")
    print()
    print("This means:")
    print("  1. Can't reach the website at all")
    print("  2. Network/internet issue")
    print("  3. Firewall blocking the connection")

finally:
    print()
    print("Step 7: Closing browser...")
    time.sleep(3)
    driver.quit()
    print("✓ Done")
    print()
    print("="*70)
    print("If you see the browser window with the website, connection works!")
    print("If you see ERROR, check your internet and firewall settings")
    print("="*70)
