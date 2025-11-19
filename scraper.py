from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
import pandas as pd
import time
import os
import logging

logger = logging.getLogger(__name__)

def get_selenium_grid_driver():
    """
    Connect to local Chrome browser using Selenium
    """
    logger.info("Initializing local Chrome driver")
    
    last_error = None
    
    # Try Chrome with local binary
    for attempt in range(3):  # Retry up to 3 times
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--start-maximized')
            chrome_options.add_argument('--disable-web-resources')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-default-apps')
            
            # Use chromium binary (Debian package name)
            chrome_options.binary_location = '/usr/bin/chromium'
            
            driver = webdriver.Chrome(options=chrome_options)
            logger.info("Connected with local Chrome")
            return driver
        except Exception as e:
            last_error = e
            logger.warning(f"Chrome attempt {attempt + 1} failed: {str(e)}")
            if attempt < 2:
                time.sleep(2)  # Wait before retrying
    
    error_msg = str(last_error) if last_error else "Unknown error"
    logger.error(f"Failed to initialize Chrome after all attempts: {error_msg}")
    raise Exception(f"Could not initialize Chrome: {error_msg}")

def scrape_egx_stocks():
    """
    Scrapes stock data from Egyptian Exchange website using Selenium Grid
    Returns: (DataFrame, header_text)
    """
    # URL to scrape
    url = "https://www.egx.com.eg/ar/prices.aspx"
    
    # Column names in Arabic
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
    
    # Initialize driver from Selenium Grid
    logger.info("Initializing Selenium Grid driver...")
    driver = get_selenium_grid_driver()
    
    try:
        # Navigate to the URL
        logger.info(f"Navigating to {url}...")
        driver.get(url)
        
        # Wait for page to load
        logger.info("Waiting for page to load (10 seconds)...")
        time.sleep(10)
        
        # Click the button using XPath
        button_xpath = "/html/body/form/table/tbody/tr[2]/td/center/center/div/table/tbody/tr[4]/td/table[1]/tbody/tr[2]/td/div/div/ul/li[1]/a"
        logger.info("Clicking the button...")
        
        # Try multiple times in case of alert errors
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                button = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, button_xpath))
                )
                
                # Use JavaScript click as alternative
                driver.execute_script("arguments[0].click();", button)
                logger.info(f"Button clicked (attempt {attempt + 1})")
                
                # Wait a moment for any alerts
                time.sleep(2)
                
                # Check for and dismiss any alerts
                try:
                    alert = driver.switch_to.alert
                    alert_text = alert.text
                    logger.info(f"Alert detected: {alert_text}")
                    alert.accept()
                    logger.info("Alert dismissed, retrying...")
                    time.sleep(2)
                    continue
                except:
                    # No alert, success
                    break
                    
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_attempts - 1:
                    logger.info("Retrying...")
                    time.sleep(3)
                else:
                    raise
        
        # Wait for table to appear
        logger.info("Waiting for table to load (20 seconds)...")
        time.sleep(20)
        
        # Check for any remaining alerts
        try:
            alert = driver.switch_to.alert
            logger.info(f"Alert found: {alert.text}")
            alert.accept()
            time.sleep(2)
        except:
            pass
        
        # Scrape the header text
        header_xpath = "/html/body/form/table/tbody/tr[2]/td/center/center/div/table/tbody/tr[4]/td/div/div/table/tbody/tr[1]/td[2]/p"
        try:
            header_text = driver.find_element(By.XPATH, header_xpath).text
            logger.info(f"Header text: {header_text}")
        except NoSuchElementException:
            header_text = "Not found"
            logger.warning("Header text not found")
        
        # Initialize data storage
        stock_data = []
        
        # Scrape rows from 2 to 220
        logger.info("Scraping stock data...")
        consecutive_empty = 0
        
        for i in range(2, 221):
            try:
                row_data = {}
                
                # Scrape company name (column 2)
                company_xpath = f"/html/body/form/table/tbody/tr[2]/td/center/center/div/table/tbody/tr[4]/td/div/div/table/tbody/tr[{i}]/td[2]/div/div[2]/a/span"
                try:
                    company_name = driver.find_element(By.XPATH, company_xpath).text
                    row_data['اسم الشركة'] = company_name
                except NoSuchElementException:
                    try:
                        alt_company_xpath = f"/html/body/form/table/tbody/tr[2]/td/center/center/div/table/tbody/tr[4]/td/div/div/table/tbody/tr[{i}]/td[2]"
                        company_name = driver.find_element(By.XPATH, alt_company_xpath).text
                        row_data['اسم الشركة'] = company_name
                    except:
                        row_data['اسم الشركة'] = ""
                
                # Scrape sector (column 3)
                sector_xpath = f"/html/body/form/table/tbody/tr[2]/td/center/center/div/table/tbody/tr[4]/td/div/div/table/tbody/tr[{i}]/td[3]/div"
                try:
                    sector = driver.find_element(By.XPATH, sector_xpath).text
                    row_data['القطاع'] = sector
                except NoSuchElementException:
                    try:
                        alt_sector_xpath = f"/html/body/form/table/tbody/tr[2]/td/center/center/div/table/tbody/tr[4]/td/div/div/table/tbody/tr[{i}]/td[3]"
                        sector = driver.find_element(By.XPATH, alt_sector_xpath).text
                        row_data['القطاع'] = sector
                    except:
                        row_data['القطاع'] = ""
                
                # Scrape remaining columns (4 to 14)
                for col_num in range(4, 15):
                    col_index = col_num - 2
                    col_name = columns[col_index]
                    
                    cell_xpath = f"/html/body/form/table/tbody/tr[2]/td/center/center/div/table/tbody/tr[4]/td/div/div/table/tbody/tr[{i}]/td[{col_num}]"
                    try:
                        cell_value = driver.find_element(By.XPATH, cell_xpath).text
                        row_data[col_name] = cell_value
                    except NoSuchElementException:
                        row_data[col_name] = ""
                
                # Check if row has any data
                if row_data['اسم الشركة'] or any(row_data.get(col, "") for col in columns):
                    stock_data.append(row_data)
                    consecutive_empty = 0
                    if len(stock_data) % 20 == 0:
                        logger.info(f"Scraped {len(stock_data)} stocks... (current row: {i})")
                else:
                    consecutive_empty += 1
                    if consecutive_empty > 5:
                        logger.info(f"Reached end of table at row {i} (5 consecutive empty rows)")
                        break
                
            except Exception as e:
                consecutive_empty += 1
                if consecutive_empty > 5:
                    logger.info(f"Reached end of table at row {i}")
                    break
        
        logger.info(f"Total stocks scraped: {len(stock_data)}")
        
        # Create DataFrame
        df = pd.DataFrame(stock_data, columns=columns)
        
        logger.info(f"Data prepared. Total rows: {len(df)}")
        logger.info(f"First 5 rows:\n{df.head()}")
        
        return df, header_text
        
    except Exception as e:
        logger.error(f"An error occurred during scraping: {str(e)}")
        raise
        
    finally:
        # Close the browser
        logger.info("Closing Selenium Grid connection...")
        driver.quit()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    logger.info("=" * 60)
    logger.info("EGX Stock Data Scraper (Selenium Grid)")
    logger.info("=" * 60)
    
    try:
        df, header = scrape_egx_stocks()
        logger.info("\n" + "=" * 60)
        logger.info("Scraping completed successfully!")
        logger.info("=" * 60)
    except Exception as e:
        logger.error(f"\nScraping failed: {str(e)}")
