from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os
import json
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import asyncio
from pathlib import Path
import logging
from scraper import scrape_egx_stocks

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(title="EGX Stock Scraper", version="1.0.0")

# Directories
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# Global state
class ScrapingState:
    current_file: str = None
    last_update: datetime = None
    next_update: datetime = None
    is_scraping: bool = False
    error_message: str = None

state = ScrapingState()

# Scheduler
scheduler = AsyncIOScheduler()

# Paths
EXCEL_FILENAME = "egx_stocks_latest.xlsx"
EXCEL_PATH = DATA_DIR / EXCEL_FILENAME

async def scheduled_scraping():
    """Execute scraping every 1 hours"""
    global state
    
    if state.is_scraping:
        logger.warning("Scraping already in progress, skipping this run")
        return
    
    try:
        state.is_scraping = True
        state.error_message = None
        logger.info("Starting scheduled scraping...")
        
        # Run scraper (convert to async if needed)
        df, header_text = await asyncio.to_thread(scrape_egx_stocks)
        
        # Save file
        df.to_excel(EXCEL_PATH, index=False, engine='openpyxl')
        
        # Update state
        state.current_file = EXCEL_FILENAME
        state.last_update = datetime.now()
        state.next_update = datetime.now() + timedelta(hours=1)
        
        logger.info(f"Scraping completed successfully. File saved: {EXCEL_PATH}")
        logger.info(f"Next update scheduled for: {state.next_update}")
        
    except Exception as e:
        logger.error(f"Scraping failed: {str(e)}", exc_info=True)
        state.error_message = str(e)
        
    finally:
        state.is_scraping = False

@app.on_event("startup")
async def startup_event():
    """Initialize scheduler on startup"""
    global state
    
    logger.info("Starting up application...")
    
    # Check if file exists from previous run
    if EXCEL_PATH.exists():
        state.current_file = EXCEL_FILENAME
        state.last_update = datetime.fromtimestamp(EXCEL_PATH.stat().st_mtime)
        state.next_update = state.last_update + timedelta(hours=1)
    else:
        # First run immediately
        await scheduled_scraping()
        state.next_update = datetime.now() + timedelta(hours=1)
    
    # Start scheduler
    scheduler.add_job(
        scheduled_scraping,
        IntervalTrigger(hours=1),
        id='scraping_job',
        name='EGX Stock Scraping',
        replace_existing=True
    )
    
    if not scheduler.running:
        scheduler.start()
        logger.info("Scheduler started - Next update in 1 hours")

@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown scheduler"""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler stopped")

@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    """Render dashboard with status and download link"""
    
    time_remaining = ""
    download_enabled = "disabled"
    download_link = "#"
    last_update_text = "Never"
    scraping_status = "Idle"
    error_display = "none"
    error_text = ""
    
    if state.next_update:
        time_diff = state.next_update - datetime.now()
        if time_diff.total_seconds() > 0:
            hours = int(time_diff.total_seconds() // 3600)
            minutes = int((time_diff.total_seconds() % 3600) // 60)
            seconds = int(time_diff.total_seconds() % 60)
            time_remaining = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            time_remaining = "00:00:00"
    
    if state.last_update:
        last_update_text = state.last_update.strftime("%Y-%m-%d %H:%M:%S")
    
    if state.current_file and EXCEL_PATH.exists():
        download_enabled = ""
        download_link = f"/download/{state.current_file}"
    
    if state.is_scraping:
        scraping_status = "Scraping in Progress..."
    
    if state.error_message:
        error_display = "block"
        error_text = state.error_message
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>EGX Stock Scraper Dashboard</title>
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
                border-radius: 10px;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
                max-width: 600px;
                width: 100%;
                padding: 40px;
            }}
            
            .header {{
                text-align: center;
                margin-bottom: 30px;
            }}
            
            .header h1 {{
                color: #333;
                margin-bottom: 10px;
                font-size: 2.5em;
            }}
            
            .header p {{
                color: #666;
                font-size: 1.1em;
            }}
            
            .status-card {{
                background: #f8f9fa;
                border-left: 4px solid #667eea;
                padding: 20px;
                margin-bottom: 20px;
                border-radius: 5px;
            }}
            
            .status-row {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 15px;
                padding-bottom: 15px;
                border-bottom: 1px solid #e0e0e0;
            }}
            
            .status-row:last-child {{
                margin-bottom: 0;
                padding-bottom: 0;
                border-bottom: none;
            }}
            
            .status-label {{
                font-weight: 600;
                color: #333;
                font-size: 1em;
            }}
            
            .status-value {{
                color: #667eea;
                font-weight: 500;
                font-size: 1em;
            }}
            
            .timer {{
                font-size: 1.3em;
                font-weight: bold;
                color: #764ba2;
                font-family: 'Courier New', monospace;
            }}
            
            .scraping-indicator {{
                display: inline-block;
                width: 12px;
                height: 12px;
                background: #28a745;
                border-radius: 50%;
                margin-right: 8px;
                animation: pulse 2s infinite;
            }}
            
            .scraping-indicator.active {{
                background: #ffc107;
                animation: pulse 1s infinite;
            }}
            
            @keyframes pulse {{
                0% {{ opacity: 1; }}
                50% {{ opacity: 0.5; }}
                100% {{ opacity: 1; }}
            }}
            
            .download-section {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 25px;
                border-radius: 5px;
                text-align: center;
                margin-bottom: 20px;
            }}
            
            .download-section h3 {{
                margin-bottom: 15px;
                font-size: 1.2em;
            }}
            
            .download-btn {{
                display: inline-block;
                background: white;
                color: #667eea;
                padding: 12px 30px;
                border-radius: 5px;
                text-decoration: none;
                font-weight: 600;
                cursor: pointer;
                border: none;
                transition: all 0.3s ease;
            }}
            
            .download-btn:hover:not(:disabled) {{
                transform: translateY(-2px);
                box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
            }}
            
            .download-btn:disabled {{
                opacity: 0.5;
                cursor: not-allowed;
            }}
            
            .error-alert {{
                background: #f8d7da;
                border: 1px solid #f5c6cb;
                color: #721c24;
                padding: 15px;
                border-radius: 5px;
                margin-bottom: 20px;
                display: {error_display};
            }}
            
            .info-text {{
                background: #d1ecf1;
                border: 1px solid #bee5eb;
                color: #0c5460;
                padding: 15px;
                border-radius: 5px;
                margin-top: 20px;
                font-size: 0.95em;
            }}
            
            @media (max-width: 600px) {{
                .container {{
                    padding: 20px;
                }}
                
                .header h1 {{
                    font-size: 1.8em;
                }}
                
                .status-row {{
                    flex-direction: column;
                    align-items: flex-start;
                }}
                
                .status-value {{
                    margin-top: 5px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📊 EGX Stock Scraper</h1>
                <p>Real-time Egyptian Exchange Stock Data</p>
            </div>
            
            <div class="error-alert">
                <strong>Error:</strong> {error_text}
            </div>
            
            <div class="status-card">
                <div class="status-row">
                    <span class="status-label">
                        <span class="scraping-indicator{'active' if state.is_scraping else ''}"></span>
                        Status
                    </span>
                    <span class="status-value">{scraping_status}</span>
                </div>
                <div class="status-row">
                    <span class="status-label">Last Update</span>
                    <span class="status-value">{last_update_text}</span>
                </div>
                <div class="status-row">
                    <span class="status-label">Next Update In</span>
                    <span class="status-value timer" id="countdown">{time_remaining}</span>
                </div>
            </div>
            
            <div class="download-section">
                <h3>📥 Download Latest Data</h3>
                <a href="{download_link}" class="download-btn" id="downloadBtn" {download_enabled}>
                    Download Excel File
                </a>
            </div>
            
            <div class="info-text">
                <strong>ℹ️ How it works:</strong> The system automatically scrapes EGX stock data every 1 hours and saves it to an Excel file. You can download the latest data using the button above. The countdown shows when the next update will occur.
            </div>
        </div>
        
        <script>
            // Update countdown timer
            function updateCountdown() {{
                const countdownEl = document.getElementById('countdown');
                if (!countdownEl) return;
                
                const timeText = countdownEl.textContent;
                const parts = timeText.split(':');
                if (parts.length !== 3) return;
                
                let hours = parseInt(parts[0]);
                let minutes = parseInt(parts[1]);
                let seconds = parseInt(parts[2]);
                
                // Decrement countdown
                if (seconds > 0) {{
                    seconds--;
                }} else if (minutes > 0) {{
                    minutes--;
                    seconds = 59;
                }} else if (hours > 0) {{
                    hours--;
                    minutes = 59;
                    seconds = 59;
                }}
                
                countdownEl.textContent = 
                    String(hours).padStart(2, '0') + ':' +
                    String(minutes).padStart(2, '0') + ':' +
                    String(seconds).padStart(2, '0');
                
                // Refresh page when timer reaches 0
                if (hours === 0 && minutes === 0 && seconds === 0) {{
                    location.reload();
                }}
            }}
            
            // Update countdown every second
            setInterval(updateCountdown, 1000);
            
            // Auto-refresh page every 30 seconds to sync with server
            setInterval(() => {{
                fetch('/')
                    .then(response => response.text())
                    .then(html => {{
                        if (document.documentElement.innerHTML !== html) {{
                            location.reload();
                        }}
                    }})
                    .catch(() => {{}});
            }}, 30000);
        </script>
    </body>
    </html>
    """
    
    return html_content

@app.get("/status")
async def get_status():
    """Get current status as JSON"""
    return {
        "current_file": state.current_file,
        "last_update": state.last_update.isoformat() if state.last_update else None,
        "next_update": state.next_update.isoformat() if state.next_update else None,
        "is_scraping": state.is_scraping,
        "error_message": state.error_message,
        "file_exists": EXCEL_PATH.exists()
    }

@app.get("/download/{filename}")
async def download_file(filename: str):
    """Download the Excel file"""
    if filename != EXCEL_FILENAME:
        return {"error": "Invalid filename"}, 404
    
    if not EXCEL_PATH.exists():
        return {"error": "File not found"}, 404
    
    return FileResponse(
        path=EXCEL_PATH,
        filename=filename,
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

@app.post("/trigger-scraping")
async def trigger_scraping(background_tasks: BackgroundTasks):
    """Manually trigger scraping (for testing)"""
    if state.is_scraping:
        return {"error": "Scraping already in progress"}, 409
    
    background_tasks.add_task(scheduled_scraping)
    return {"message": "Scraping triggered"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
