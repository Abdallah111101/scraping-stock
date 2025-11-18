"""
FastAPI application for EGX Stock Scraper with Browserless support
Designed for Railway deployment
"""

from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
from datetime import datetime
import pandas as pd
import time
import threading
from pathlib import Path
from contextlib import asynccontextmanager
import asyncio

# Import scraping logic
from scraper import scrape_egx_stocks

# Configuration
EXCEL_DIR = "excel_files"
UPDATE_INTERVAL = 8 * 60 * 60  # 8 hours

# Create excel directory if it doesn't exist
Path(EXCEL_DIR).mkdir(exist_ok=True)

# Global state
class AppState:
    last_scrape_time = None
    last_scrape_file = None
    is_scraping = False
    error_message = None

app_state = AppState()

# Startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown"""
    print("🚀 Starting EGX Stock Scraper API...")
    print(f"📁 Excel files directory: {EXCEL_DIR}")
    print(f"🔄 Update interval: {UPDATE_INTERVAL} seconds")
    yield
    print("🛑 Shutting down EGX Stock Scraper API...")

app = FastAPI(
    title="EGX Stock Scraper API",
    description="Real-time EGX stock data scraper with FastAPI",
    version="1.0.0",
    lifespan=lifespan
)

# Mount static files
try:
    app.mount("/excel_files", StaticFiles(directory=EXCEL_DIR), name="excel_files")
except Exception as e:
    print(f"Warning: Could not mount static files: {e}")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "EGX Stock Scraper API",
        "version": "1.0.0",
        "endpoints": {
            "scrape": "/scrape",
            "status": "/status",
            "latest": "/latest",
            "download": "/download/{filename}",
            "health": "/health"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "is_scraping": app_state.is_scraping
    }


@app.post("/scrape")
async def scrape(background_tasks: BackgroundTasks):
    """
    Start scraping EGX stocks
    Returns immediately, scraping runs in background
    """
    if app_state.is_scraping:
        raise HTTPException(status_code=409, detail="Scraping already in progress")
    
    background_tasks.add_task(run_scraper)
    
    return {
        "status": "started",
        "message": "Scraping has been started in background",
        "timestamp": datetime.now().isoformat()
    }


def run_scraper():
    """Run the scraper in background"""
    app_state.is_scraping = True
    app_state.error_message = None
    
    try:
        print("\n" + "=" * 60)
        print("🕷️  Starting EGX Stock Scraping...")
        print("=" * 60)
        
        # Run scraper
        df, header_text = scrape_egx_stocks()
        
        # Generate filename
        filename = f"egx_stocks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        filepath = os.path.join(EXCEL_DIR, filename)
        
        # Save to Excel
        df.to_excel(filepath, index=False, engine='openpyxl')
        
        # Update state
        app_state.last_scrape_time = datetime.now().isoformat()
        app_state.last_scrape_file = filename
        
        print(f"\n✅ Scraping completed!")
        print(f"📊 Total stocks: {len(df)}")
        print(f"💾 Saved to: {filepath}")
        print("=" * 60 + "\n")
        
    except Exception as e:
        app_state.error_message = str(e)
        print(f"\n❌ Scraping failed: {str(e)}")
        print("=" * 60 + "\n")
    
    finally:
        app_state.is_scraping = False


@app.get("/status")
async def status():
    """Get current scraping status"""
    return {
        "is_scraping": app_state.is_scraping,
        "last_scrape_time": app_state.last_scrape_time,
        "last_scrape_file": app_state.last_scrape_file,
        "error_message": app_state.error_message,
        "excel_dir": EXCEL_DIR
    }


@app.get("/latest")
async def latest():
    """Get link to latest scrape file"""
    if not app_state.last_scrape_file:
        raise HTTPException(status_code=404, detail="No scrape file found yet. Run /scrape first.")
    
    return {
        "filename": app_state.last_scrape_file,
        "timestamp": app_state.last_scrape_time,
        "download_url": f"/download/{app_state.last_scrape_file}"
    }


@app.get("/download/{filename}")
async def download(filename: str):
    """Download excel file"""
    filepath = os.path.join(EXCEL_DIR, filename)
    
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        filepath,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=filename
    )


@app.get("/files")
async def list_files():
    """List all available scrape files"""
    if not os.path.exists(EXCEL_DIR):
        return {"files": []}
    
    files = sorted(
        [f for f in os.listdir(EXCEL_DIR) if f.endswith('.xlsx')],
        reverse=True
    )
    
    return {
        "count": len(files),
        "files": files,
        "directory": EXCEL_DIR
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
