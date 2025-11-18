from fastapi import FastAPI, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from contextlib import asynccontextmanager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time
import os
from datetime import datetime, timedelta
import threading
import asyncio
from pathlib import Path
import requests
from urllib.parse import urljoin

try:
    from http_scraper import EGXScraper
    HTTP_SCRAPER_AVAILABLE = True
except ImportError:
    HTTP_SCRAPER_AVAILABLE = False

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    print("Starting Stock Scraper Service...")
    start_background_scheduler()
    yield
    # Shutdown
    print("Shutting down Stock Scraper Service...")

app = FastAPI(title="Stock Data Scraper", lifespan=lifespan)

# Configuration
EXCEL_DIR = "excel_files"
UPDATE_INTERVAL = 8 * 60 * 60  # 8 hours in seconds

# Global state
class ScrapeState:
    def __init__(self):
        self.last_update = None
        self.next_update = None
        self.current_file = None
        self.is_scraping = False
        self.lock = threading.Lock()

state = ScrapeState()

# Create excel_files directory if it doesn't exist
os.makedirs(EXCEL_DIR, exist_ok=True)

def scrape_egx_stocks():
    """
    Scrapes stock data from Egyptian Exchange website
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
    
    print("Initializing Chrome driver...")
    print("NOTE: Chrome browser window will appear (not in headless mode)")
    print("This allows you to see what's happening during scraping")
    
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-plugins')
    options.add_argument('--disable-default-apps')
    options.add_argument('--no-default-browser-check')
    # REMOVED: --headless mode (so you can see the browser)
    # options.add_argument('--headless')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-web-resources')
    options.add_argument('--disable-client-side-phishing-detection')
    # Add timeout preferences
    prefs = {
        'profile.default_content_settings.popups': 0,
        'profile.managed_default_content_settings.images': 2
    }
    options.add_experimental_option('prefs', prefs)
    
    # Use webdriver-manager to auto-download and manage ChromeDriver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.set_page_load_timeout(60)  # 60 second timeout for page load
    driver.implicitly_wait(10)  # 10 second implicit wait
    
    try:
        print(f"Navigating to {url}...")
        max_nav_attempts = 3
        for nav_attempt in range(max_nav_attempts):
            try:
                print(f"  Attempt {nav_attempt + 1}/{max_nav_attempts}")
                driver.get(url)
                print("✓ Page navigation successful")
                print(f"  Page title: {driver.title}")
                break
            except Exception as nav_error:
                print(f"  ✗ Navigation failed: {str(nav_error)[:100]}")
                if nav_attempt < max_nav_attempts - 1:
                    print(f"  Retrying in 5 seconds...")
                    time.sleep(5)
                else:
                    raise
        
        print("Waiting for page to load (10 seconds)...")
        time.sleep(10)
        print("✓ Page loaded")
        
        button_xpath = "/html/body/form/table/tbody/tr[2]/td/center/center/div/table/tbody/tr[4]/td/table[1]/tbody/tr[2]/td/div/div/ul/li[1]/a"
        print("Looking for button to click...")
        
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                print(f"  Attempt {attempt + 1}/{max_attempts}")
                button = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, button_xpath))
                )
                
                print("  ✓ Button found, clicking...")
                driver.execute_script("arguments[0].click();", button)
                print(f"  ✓ Button clicked (attempt {attempt + 1})")
                
                time.sleep(2)
                
                try:
                    alert = driver.switch_to.alert
                    alert_text = alert.text
                    print(f"  ⚠ Alert detected: {alert_text}")
                    alert.accept()
                    print("  Alert dismissed, retrying...")
                    time.sleep(2)
                    continue
                except:
                    print("  ✓ No alert, proceeding...")
                    break
                    
            except Exception as e:
                print(f"  ✗ Attempt {attempt + 1} failed: {str(e)[:100]}")
                if attempt < max_attempts - 1:
                    print("  Retrying...")
                    time.sleep(3)
                else:
                    raise
        
        print("Waiting for table to load (20 seconds)...")
        time.sleep(20)
        
        try:
            alert = driver.switch_to.alert
            print(f"Alert found: {alert.text}")
            alert.accept()
            time.sleep(2)
        except:
            pass
        
        stock_data = []
        print("Scraping stock data...")
        consecutive_empty = 0
        
        for i in range(2, 221):
            try:
                row_data = {}
                
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
                
                for col_num in range(4, 15):
                    col_index = col_num - 2
                    col_name = columns[col_index]
                    
                    cell_xpath = f"/html/body/form/table/tbody/tr[2]/td/center/center/div/table/tbody/tr[4]/td/div/div/table/tbody/tr[{i}]/td[{col_num}]"
                    try:
                        cell_value = driver.find_element(By.XPATH, cell_xpath).text
                        row_data[col_name] = cell_value
                    except NoSuchElementException:
                        row_data[col_name] = ""
                
                if row_data['اسم الشركة'] or any(row_data.get(col, "") for col in columns):
                    stock_data.append(row_data)
                    consecutive_empty = 0
                    if len(stock_data) % 20 == 0:
                        print(f"Scraped {len(stock_data)} stocks...")
                else:
                    consecutive_empty += 1
                    if consecutive_empty > 5:
                        print(f"Reached end of table at row {i}")
                        break
                
            except Exception as e:
                consecutive_empty += 1
                if consecutive_empty > 5:
                    print(f"Reached end of table at row {i}")
                    break
        
        print(f"Total stocks scraped: {len(stock_data)}")
        
        df = pd.DataFrame(stock_data, columns=columns)
        
        filename = f"egx_stocks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        filepath = os.path.join(EXCEL_DIR, filename)
        df.to_excel(filepath, index=False, engine='openpyxl')
        print(f"Data saved to {filepath}")
        
        return filepath, filename
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise
        
    finally:
        print("Closing browser...")
        driver.quit()

def scrape_with_http_requests():
    """
    Fallback method using HTTP requests instead of Selenium
    """
    print("\nUsing HTTP requests scraper...")
    
    if not HTTP_SCRAPER_AVAILABLE:
        raise Exception("HTTP scraper not available")
    
    scraper = EGXScraper()
    stocks = scraper.get_stock_data(max_retries=2)
    
    if not stocks:
        raise Exception("Failed to retrieve stock data via HTTP requests")
    
    # Save to Excel
    filename = f"egx_stocks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    filepath = os.path.join(EXCEL_DIR, filename)
    
    try:
        df = pd.DataFrame(stocks)
        df.to_excel(filepath, index=False, engine='openpyxl')
        print(f"Data saved to {filepath}")
        print(f"Total rows: {len(df)}")
        return filepath, filename
    except Exception as e:
        print(f"Error saving to Excel: {str(e)}")
        raise

def perform_scrape():
    """Perform the scraping task with Selenium first, HTTP fallback"""
    with state.lock:
        if state.is_scraping:
            print("Scrape already in progress, skipping...")
            return
        state.is_scraping = True
    
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            print("\n" + "="*60)
            print(f"Starting scrape at {datetime.now()} (Attempt {retry_count + 1}/{max_retries})")
            print("="*60)
            
            # Try Selenium first
            print("Method: Selenium/Chrome")
            try:
                filepath, filename = scrape_egx_stocks()
            except Exception as selenium_error:
                print(f"\n⚠ Selenium method failed: {str(selenium_error)[:100]}...")
                
                # Fallback to HTTP requests
                if HTTP_SCRAPER_AVAILABLE:
                    print("Falling back to HTTP requests method...")
                    filepath, filename = scrape_with_http_requests()
                else:
                    raise
            
            with state.lock:
                state.last_update = datetime.now()
                state.next_update = state.last_update + timedelta(seconds=UPDATE_INTERVAL)
                state.current_file = {"path": filepath, "name": filename}
            
            print(f"Next update scheduled for: {state.next_update}")
            print("="*60 + "\n")
            break  # Success, exit retry loop
            
        except Exception as e:
            retry_count += 1
            print(f"Scraping attempt {retry_count} failed: {str(e)[:100]}...")
            
            if retry_count < max_retries:
                wait_time = 10 * retry_count  # 10s, 20s, 30s
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"All {max_retries} attempts failed. Retrying at next scheduled time.")
                
        finally:
            if retry_count == max_retries or retry_count > 0:
                with state.lock:
                    state.is_scraping = False

def start_background_scheduler():
    """Start background scheduler for periodic scraping"""
    def scheduler():
        # Initial scrape
        perform_scrape()
        
        # Periodic scrapes
        while True:
            time.sleep(UPDATE_INTERVAL)
            perform_scrape()
    
    thread = threading.Thread(target=scheduler, daemon=True)
    thread.start()

@app.get("/", response_class=HTMLResponse)
async def get_home():
    """Serve the main HTML interface"""
    
    with state.lock:
        last_update_str = state.last_update.strftime("%Y-%m-%d %H:%M:%S") if state.last_update else "Never"
        next_update_str = state.next_update.strftime("%Y-%m-%d %H:%M:%S") if state.next_update else "Calculating..."
        has_file = state.current_file is not None
        file_name = state.current_file["name"] if has_file else "N/A"
    
    html = f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>نظام تحديث بيانات الأسهم</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }}
            
            .container {{
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                max-width: 600px;
                width: 100%;
                padding: 40px;
            }}
            
            .header {{
                text-align: center;
                margin-bottom: 40px;
            }}
            
            .header h1 {{
                color: #333;
                font-size: 28px;
                margin-bottom: 10px;
            }}
            
            .header p {{
                color: #666;
                font-size: 14px;
            }}
            
            .status-box {{
                background: #f8f9fa;
                border-radius: 15px;
                padding: 20px;
                margin-bottom: 20px;
                border-left: 5px solid #667eea;
            }}
            
            .status-item {{
                margin-bottom: 15px;
            }}
            
            .status-item:last-child {{
                margin-bottom: 0;
            }}
            
            .status-label {{
                color: #666;
                font-size: 13px;
                font-weight: 600;
                margin-bottom: 5px;
                text-transform: uppercase;
            }}
            
            .status-value {{
                color: #333;
                font-size: 16px;
                font-weight: 500;
            }}
            
            .countdown {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-radius: 15px;
                padding: 30px;
                text-align: center;
                margin-bottom: 30px;
            }}
            
            .countdown-label {{
                font-size: 14px;
                margin-bottom: 10px;
                opacity: 0.9;
            }}
            
            .countdown-timer {{
                font-size: 36px;
                font-weight: bold;
                font-family: 'Courier New', monospace;
                letter-spacing: 2px;
            }}
            
            .button-group {{
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
            }}
            
            .btn {{
                flex: 1;
                min-width: 150px;
                padding: 12px 20px;
                border: none;
                border-radius: 10px;
                font-size: 15px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                text-decoration: none;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
            }}
            
            .btn-primary {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }}
            
            .btn-primary:hover {{
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
            }}
            
            .btn-primary:disabled {{
                opacity: 0.5;
                cursor: not-allowed;
                transform: none;
            }}
            
            .btn-secondary {{
                background: #f0f0f0;
                color: #333;
                border: 2px solid #e0e0e0;
            }}
            
            .btn-secondary:hover {{
                background: #e0e0e0;
            }}
            
            .status-badge {{
                display: inline-block;
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 600;
                margin-left: 10px;
            }}
            
            .badge-ready {{
                background: #d4edda;
                color: #155724;
            }}
            
            .badge-loading {{
                background: #fff3cd;
                color: #856404;
            }}
            
            .info-text {{
                background: #e7f3ff;
                border-left: 4px solid #2196F3;
                padding: 15px;
                border-radius: 5px;
                margin-top: 20px;
                color: #0c5aa0;
                font-size: 14px;
            }}
            
            @media (max-width: 480px) {{
                .container {{
                    padding: 20px;
                }}
                
                .header h1 {{
                    font-size: 22px;
                }}
                
                .countdown-timer {{
                    font-size: 28px;
                }}
                
                .button-group {{
                    flex-direction: column;
                }}
                
                .btn {{
                    min-width: unset;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📊 نظام تحديث بيانات الأسهم</h1>
                <p>الحصول على أحدث بيانات أسعار الأسهم من البورصة المصرية</p>
            </div>
            
            <div class="countdown">
                <div class="countdown-label">الوقت المتبقي للتحديث التالي</div>
                <div class="countdown-timer" id="timer">08:00:00</div>
            </div>
            
            <div class="status-box">
                <div class="status-item">
                    <div class="status-label">آخر تحديث</div>
                    <div class="status-value">{last_update_str}</div>
                </div>
                
                <div class="status-item">
                    <div class="status-label">التحديث التالي</div>
                    <div class="status-value">{next_update_str}</div>
                </div>
                
                <div class="status-item">
                    <div class="status-label">ملف البيانات</div>
                    <div class="status-value">
                        {file_name}
                        <span class="status-badge {'badge-ready' if has_file else 'badge-loading'}">
                            {'جاهز للتحميل' if has_file else 'قيد التحديث'}
                        </span>
                    </div>
                </div>
            </div>
            
            <div class="button-group">
                <button class="btn btn-primary" onclick="downloadFile()" {'disabled' if not has_file else ''}>
                    ⬇️ تحميل ملف Excel
                </button>
                <button class="btn btn-secondary" onclick="refreshStatus()">
                    🔄 تحديث البيانات
                </button>
            </div>
            
            <div class="info-text">
                ℹ️ يتم تحديث البيانات تلقائياً كل 8 ساعات. يمكنك الآن تحميل آخر ملف متوفر.
            </div>
        </div>
        
        <script>
            const UPDATE_INTERVAL = 8 * 60 * 60 * 1000; // 8 hours in milliseconds
            let nextUpdateTime = new Date("{next_update_str}").getTime();
            
            function updateCountdown() {{
                const now = new Date().getTime();
                const timeLeft = nextUpdateTime - now;
                
                if (timeLeft <= 0) {{
                    document.getElementById('timer').textContent = '00:00:00';
                    refreshStatus();
                    return;
                }}
                
                const hours = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
                const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);
                
                const timerText = 
                    String(hours).padStart(2, '0') + ':' +
                    String(minutes).padStart(2, '0') + ':' +
                    String(seconds).padStart(2, '0');
                
                document.getElementById('timer').textContent = timerText;
            }}
            
            function downloadFile() {{
                fetch('/download')
                    .then(response => {{
                        if (!response.ok) throw new Error('Download failed');
                        return response.blob();
                    }})
                    .then(blob => {{
                        const url = window.URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = 'stock_data.xlsx';
                        document.body.appendChild(a);
                        a.click();
                        window.URL.revokeObjectURL(url);
                        a.remove();
                    }})
                    .catch(error => {{
                        alert('خطأ في التحميل: ' + error.message);
                    }});
            }}
            
            function refreshStatus() {{
                location.reload();
            }}
            
            // Update countdown every second
            setInterval(updateCountdown, 1000);
            updateCountdown();
        </script>
    </body>
    </html>
    """
    
    return html

@app.get("/download")
async def download_excel():
    """Download the current Excel file"""
    with state.lock:
        if state.current_file is None:
            return {"error": "No file available yet"}
        
        filepath = state.current_file["path"]
        filename = state.current_file["name"]
    
    if not os.path.exists(filepath):
        return {"error": "File not found"}
    
    return FileResponse(
        path=filepath,
        filename=filename,
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

@app.get("/api/status")
async def get_status():
    """Get current status as JSON"""
    with state.lock:
        return {
            "last_update": state.last_update.isoformat() if state.last_update else None,
            "next_update": state.next_update.isoformat() if state.next_update else None,
            "file": state.current_file,
            "is_scraping": state.is_scraping
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
