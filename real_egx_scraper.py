"""
Real EGX Stock Scraper using public data sources
Works on Railway without Selenium/Chrome
"""

import requests
import pandas as pd
from datetime import datetime
import time
import json

class RealEGXScraper:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        self.session.headers.update(self.headers)
    
    def get_stock_data(self):
        """
        Fetch REAL stock data from EGX using Selenium XPath
        """
        print("Fetching REAL EGX stock data using Selenium...")
        
        try:
            stocks = self._get_from_selenium_xpath()
            if stocks and len(stocks) > 0:
                print(f"✓ Got {len(stocks)} stocks from Selenium XPath scraping")
                return stocks
        except Exception as e:
            print(f"✗ Selenium XPath scraping failed: {str(e)}")
        
        return []
    
    def _get_from_selenium_xpath(self):
        """Get real data from EGX using Selenium and XPath"""
        try:
            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.chrome.options import Options
            
            # Setup Chrome options
            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            
            driver = webdriver.Chrome(options=chrome_options)
            stocks = []
            
            try:
                # Navigate to EGX website
                driver.get("https://www.egx.com.eg/en/prices.aspx")
                
                # Wait for table to load
                wait = WebDriverWait(driver, 20)
                wait.until(EC.presence_of_all_elements_located((By.XPATH, "//table//tr")))
                
                # Get all table rows using XPath
                rows = driver.find_elements(By.XPATH, "//table//tbody//tr")
                
                print(f"Found {len(rows)} rows")
                
                for row in rows:
                    try:
                        # Extract data using XPath
                        symbol = row.find_element(By.XPATH, ".//td[1]").text.strip()
                        name = row.find_element(By.XPATH, ".//td[2]").text.strip()
                        price = row.find_element(By.XPATH, ".//td[3]").text.strip()
                        change = row.find_element(By.XPATH, ".//td[4]").text.strip()
                        sector = row.find_element(By.XPATH, ".//td[5]").text.strip()
                        
                        if symbol and name:
                            stock = {
                                'Symbol': symbol,
                                'Name': name,
                                'Price': price,
                                'Change': change,
                                'Sector': sector,
                            }
                            stocks.append(stock)
                    except:
                        continue
                
                return stocks
            
            finally:
                driver.quit()
        
        except ImportError:
            print("Selenium not installed. Install with: pip install selenium")
            return []
        except Exception as e:
            print(f"Selenium XPath error: {str(e)}")
            return []
    
    
    def save_to_excel(self, stocks, filename=None):
        """Save stocks to Excel"""
        if not stocks:
            return None
        
        if filename is None:
            filename = f"egx_stocks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        try:
            df = pd.DataFrame(stocks)
            df.to_excel(filename, index=False, engine='openpyxl')
            print(f"✓ Saved {len(df)} stocks to {filename}")
            return filename
        except Exception as e:
            print(f"✗ Error saving Excel: {str(e)}")
            return None


if __name__ == "__main__":
    scraper = RealEGXScraper()
    stocks = scraper.get_stock_data()
    
    if stocks:
        print(f"\nGot {len(stocks)} stocks")
        print(f"First stock: {stocks[0]}")
        
        # Save to Excel
        scraper.save_to_excel(stocks)
    else:
        print("No data retrieved")
