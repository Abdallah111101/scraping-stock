"""
Alternative scraper using direct HTTP requests instead of Selenium
This bypasses the bot detection that's blocking headless Chrome
"""

import requests
import pandas as pd
from datetime import datetime
import time
import json

class EGXScraper:
    def __init__(self):
        self.session = requests.Session()
        # Mimic a real browser to bypass bot detection
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.7444.163 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
        }
        self.session.headers.update(self.headers)
    
    def get_stock_data(self, max_retries=3):
        """
        Fetch stock data from EGX using API or direct requests
        """
        url = "https://www.egx.com.eg/ar/prices.aspx"
        
        print("Fetching stock data from EGX...")
        
        for attempt in range(max_retries):
            try:
                print(f"Attempt {attempt + 1}/{max_retries}")
                
                # Try with timeout and retries
                response = self.session.get(
                    url,
                    timeout=30,
                    allow_redirects=True,
                    verify=True
                )
                
                response.raise_for_status()
                print(f"✓ Connection successful (Status: {response.status_code})")
                
                # Parse the HTML
                stocks = self._parse_html(response.text)
                
                if stocks:
                    print(f"✓ Successfully scraped {len(stocks)} stocks")
                    return stocks
                else:
                    print("⚠ No data found in response")
                    
            except requests.exceptions.ConnectionError as e:
                print(f"✗ Connection error (attempt {attempt + 1}): {str(e)}")
                if attempt < max_retries - 1:
                    wait_time = 10 * (attempt + 1)
                    print(f"  Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                    
            except requests.exceptions.Timeout as e:
                print(f"✗ Timeout error (attempt {attempt + 1}): {str(e)}")
                if attempt < max_retries - 1:
                    wait_time = 10 * (attempt + 1)
                    print(f"  Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                    
            except Exception as e:
                print(f"✗ Error (attempt {attempt + 1}): {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(5)
        
        return None
    
    def _parse_html(self, html):
        """
        Parse HTML response to extract stock data
        """
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            print("BeautifulSoup4 not installed. Installing...")
            import subprocess
            subprocess.check_call(['pip', 'install', 'beautifulsoup4'])
            from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(html, 'html.parser')
        stocks = []
        
        # Look for price table
        tables = soup.find_all('table')
        print(f"  Found {len(tables)} tables in page")
        
        # Try to find the main data table
        for table in tables:
            rows = table.find_all('tr')
            if len(rows) > 10:  # Main table should have many rows
                print(f"  Found main table with {len(rows)} rows")
                
                for row in rows[1:]:  # Skip header
                    cells = row.find_all('td')
                    if len(cells) >= 14:  # We need at least 14 columns
                        try:
                            stock = {
                                'اسم الشركة': cells[1].get_text(strip=True),
                                'القطاع': cells[2].get_text(strip=True),
                                'الإقفال السابق': cells[3].get_text(strip=True),
                                'سعر الفتح': cells[4].get_text(strip=True),
                                'سعر الاغلاق': cells[5].get_text(strip=True),
                                'نسبة التغير%': cells[6].get_text(strip=True),
                                'آخر سعر': cells[7].get_text(strip=True),
                                'اعلى سعر': cells[8].get_text(strip=True),
                                'اقل سعر': cells[9].get_text(strip=True),
                                'القيمة (جنيه)': cells[10].get_text(strip=True),
                                'الكمية': cells[11].get_text(strip=True),
                                'عدد العمليات': cells[12].get_text(strip=True),
                                'رأس المال السوقى (مليون جنيه)': cells[13].get_text(strip=True),
                            }
                            
                            # Only add if has company name
                            if stock['اسم الشركة']:
                                stocks.append(stock)
                        except (IndexError, AttributeError):
                            continue
        
        return stocks if stocks else None
    
    def save_to_excel(self, stocks, filename=None):
        """
        Save stock data to Excel file
        """
        if not stocks:
            print("✗ No data to save")
            return None
        
        if filename is None:
            filename = f"egx_stocks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        try:
            df = pd.DataFrame(stocks)
            df.to_excel(filename, index=False, engine='openpyxl')
            print(f"✓ Data saved to {filename}")
            print(f"  Total records: {len(df)}")
            return filename
        except Exception as e:
            print(f"✗ Error saving to Excel: {str(e)}")
            return None


def scrape_with_requests():
    """
    Main function using HTTP requests instead of Selenium
    """
    print("\n" + "="*60)
    print("EGX Stock Scraper (HTTP Requests Method)")
    print("="*60 + "\n")
    
    scraper = EGXScraper()
    
    # Get stock data
    stocks = scraper.get_stock_data(max_retries=3)
    
    if stocks:
        # Save to Excel
        filename = scraper.save_to_excel(stocks)
        
        # Show preview
        df = pd.DataFrame(stocks)
        print("\nFirst 5 records:")
        print(df.head())
        
        print("\n" + "="*60)
        print("✓ Scraping completed successfully!")
        print("="*60 + "\n")
        
        return df, filename
    else:
        print("\n" + "="*60)
        print("✗ Failed to scrape data after all attempts")
        print("="*60 + "\n")
        return None, None


if __name__ == "__main__":
    df, filename = scrape_with_requests()
