"""
Selenium Grid setup for Railway
Uses Railway's pre-configured Selenium Grid template with Chrome, Firefox, and Edge browsers
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
import time
import os

class SeleniumGridScraper:
    def __init__(self, grid_url=None):
        """
        Initialize Selenium Grid connection for Railway
        
        Args:
            grid_url: URL to Selenium Grid Hub (e.g., "http://localhost:4444" for local, 
                     or Railway service URL)
        """
        # Use Railway Selenium Grid URL or local for development
        self.grid_url = grid_url or os.getenv('SELENIUM_GRID_URL', 'http://localhost:4444')
        self.driver = None
    
    def initialize_chrome_driver(self):
        """Initialize Chrome driver connected to Selenium Grid"""
        try:
            print(f"Connecting to Selenium Grid at {self.grid_url}...")
            
            options = webdriver.ChromeOptions()
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--window-size=1920,1080')
            
            # Connect to Selenium Grid
            self.driver = webdriver.Remote(
                command_executor=f'{self.grid_url}/wd/hub',
                options=options
            )
            
            print("✓ Connected to Chrome via Selenium Grid")
            return self.driver
        
        except Exception as e:
            print(f"✗ Failed to connect to Selenium Grid: {str(e)}")
            raise
    
    def initialize_firefox_driver(self):
        """Initialize Firefox driver connected to Selenium Grid"""
        try:
            print(f"Connecting to Selenium Grid at {self.grid_url}...")
            
            options = webdriver.FirefoxOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            # Connect to Selenium Grid
            self.driver = webdriver.Remote(
                command_executor=f'{self.grid_url}/wd/hub',
                options=options
            )
            
            print("✓ Connected to Firefox via Selenium Grid")
            return self.driver
        
        except Exception as e:
            print(f"✗ Failed to connect to Selenium Grid: {str(e)}")
            raise
    
    def initialize_edge_driver(self):
        """Initialize Edge driver connected to Selenium Grid"""
        try:
            print(f"Connecting to Selenium Grid at {self.grid_url}...")
            
            options = webdriver.EdgeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            # Connect to Selenium Grid
            self.driver = webdriver.Remote(
                command_executor=f'{self.grid_url}/wd/hub',
                options=options
            )
            
            print("✓ Connected to Edge via Selenium Grid")
            return self.driver
        
        except Exception as e:
            print(f"✗ Failed to connect to Selenium Grid: {str(e)}")
            raise
    
    def scrape_egx_stocks(self):
        """
        Scrapes stock data from Egyptian Exchange website using Selenium Grid
        """
        url = "https://www.egx.com.eg/ar/prices.aspx"
        
        columns = [
            'اسم الشركة',
            'القطاع',
            'الإقفال السابق',
            'سعر الفتح',
            'سعر الاغلاق',
            'نسبة التغير%',
            'آخر سعر',
            'اعلى سعر',
            'اقل سعر',
            'القيمة (جنيه)',
            'الكمية',
            'عدد العمليات',
            'رأس المال السوقى (مليون جنيه)'
        ]
        
        try:
            # Initialize Chrome driver via Selenium Grid
            self.initialize_chrome_driver()
            
            # Navigate to the URL
            print(f"Navigating to {url}...")
            self.driver.get(url)
            
            # Wait for page to load
            print("Waiting for page to load (10 seconds)...")
            time.sleep(10)
            
            # Click the button using XPath
            button_xpath = "/html/body/form/table/tbody/tr[2]/td/center/center/div/table/tbody/tr[4]/td/table[1]/tbody/tr[2]/td/div/div/ul/li[1]/a"
            print("Clicking the button...")
            
            max_attempts = 3
            for attempt in range(max_attempts):
                try:
                    button = WebDriverWait(self.driver, 15).until(
                        EC.element_to_be_clickable((By.XPATH, button_xpath))
                    )
                    
                    self.driver.execute_script("arguments[0].click();", button)
                    print(f"Button clicked (attempt {attempt + 1})")
                    
                    time.sleep(2)
                    
                    # Check for and dismiss any alerts
                    try:
                        alert = self.driver.switch_to.alert
                        alert_text = alert.text
                        print(f"Alert detected: {alert_text}")
                        alert.accept()
                        print("Alert dismissed, retrying...")
                        time.sleep(2)
                        continue
                    except:
                        break
                        
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed: {str(e)}")
                    if attempt < max_attempts - 1:
                        print("Retrying...")
                        time.sleep(3)
                    else:
                        raise
            
            # Wait for table to appear
            print("Waiting for table to load (20 seconds)...")
            time.sleep(20)
            
            # Check for any remaining alerts
            try:
                alert = self.driver.switch_to.alert
                print(f"Alert found: {alert.text}")
                alert.accept()
                time.sleep(2)
            except:
                pass
            
            # Initialize data storage
            stock_data = []
            
            # Scrape rows from 2 to 220
            print("Scraping stock data...")
            consecutive_empty = 0
            
            for i in range(2, 221):
                try:
                    row_data = {}
                    
                    # Scrape company name (column 2)
                    company_xpath = f"/html/body/form/table/tbody/tr[2]/td/center/center/div/table/tbody/tr[4]/td/div/div/table/tbody/tr[{i}]/td[2]/div/div[2]/a/span"
                    try:
                        company_name = self.driver.find_element(By.XPATH, company_xpath).text
                        row_data['اسم الشركة'] = company_name
                    except NoSuchElementException:
                        try:
                            alt_company_xpath = f"/html/body/form/table/tbody/tr[2]/td/center/center/div/table/tbody/tr[4]/td/div/div/table/tbody/tr[{i}]/td[2]"
                            company_name = self.driver.find_element(By.XPATH, alt_company_xpath).text
                            row_data['اسم الشركة'] = company_name
                        except:
                            row_data['اسم الشركة'] = ""
                    
                    # Scrape sector (column 3)
                    sector_xpath = f"/html/body/form/table/tbody/tr[2]/td/center/center/div/table/tbody/tr[4]/td/div/div/table/tbody/tr[{i}]/td[3]/div"
                    try:
                        sector = self.driver.find_element(By.XPATH, sector_xpath).text
                        row_data['القطاع'] = sector
                    except NoSuchElementException:
                        try:
                            alt_sector_xpath = f"/html/body/form/table/tbody/tr[2]/td/center/center/div/table/tbody/tr[4]/td/div/div/table/tbody/tr[{i}]/td[3]"
                            sector = self.driver.find_element(By.XPATH, alt_sector_xpath).text
                            row_data['القطاع'] = sector
                        except:
                            row_data['القطاع'] = ""
                    
                    # Scrape remaining columns (4 to 14)
                    for col_num in range(4, 15):
                        col_index = col_num - 2
                        col_name = columns[col_index]
                        
                        cell_xpath = f"/html/body/form/table/tbody/tr[2]/td/center/center/div/table/tbody/tr[4]/td/div/div/table/tbody/tr[{i}]/td[{col_num}]"
                        try:
                            cell_value = self.driver.find_element(By.XPATH, cell_xpath).text
                            row_data[col_name] = cell_value
                        except NoSuchElementException:
                            row_data[col_name] = ""
                    
                    # Check if row has any data
                    if row_data['اسم الشركة'] or any(row_data.get(col, "") for col in columns):
                        stock_data.append(row_data)
                        consecutive_empty = 0
                        if len(stock_data) % 20 == 0:
                            print(f"Scraped {len(stock_data)} stocks... (current row: {i})")
                    else:
                        consecutive_empty += 1
                        if consecutive_empty > 5:
                            print(f"Reached end of table at row {i} (5 consecutive empty rows)")
                            break
                    
                except Exception as e:
                    consecutive_empty += 1
                    if consecutive_empty > 5:
                        print(f"Reached end of table at row {i}")
                        break
            
            print(f"Total stocks scraped: {len(stock_data)}")
            
            # Create DataFrame
            df = pd.DataFrame(stock_data, columns=columns)
            
            # Save to Excel
            filename = f"egx_stocks_grid_{time.strftime('%Y%m%d_%H%M%S')}.xlsx"
            df.to_excel(filename, index=False, engine='openpyxl')
            print(f"\n✓ Data saved to {filename}")
            print(f"Total rows: {len(df)}")
            
            # Display first few rows
            print("\nFirst 5 rows:")
            print(df.head())
            
            return df
            
        except Exception as e:
            print(f"✗ An error occurred: {str(e)}")
            raise
            
        finally:
            # Close the browser
            if self.driver:
                print("\nClosing browser...")
                self.driver.quit()


if __name__ == "__main__":
    print("=" * 60)
    print("EGX Stock Data Scraper - Selenium Grid (Railway)")
    print("=" * 60)
    print()
    
    try:
        # Initialize scraper (uses SELENIUM_GRID_URL env var if set)
        scraper = SeleniumGridScraper()
        
        # Scrape data
        df = scraper.scrape_egx_stocks()
        
        print("\n" + "=" * 60)
        print("Scraping completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Scraping failed: {str(e)}")
        print("Make sure Selenium Grid is running and accessible.")
