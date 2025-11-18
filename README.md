# 📊 Stock Data Scraper with FastAPI

A beautiful web application that automatically scrapes Egyptian Exchange stock data every 8 hours, generates Excel files, and provides a modern UI for downloading the latest data.

## ✨ Features

- **Automatic Updates**: Scrapes stock data every 8 hours automatically
- **Excel Export**: Generates Excel files with all scraped data
- **Beautiful UI**: Modern, responsive HTML interface with real-time countdown
- **Download Management**: Easy download of the latest Excel file
- **Status Tracking**: Shows last update time and next update time
- **Background Processing**: Non-blocking background tasks
- **API Endpoints**: RESTful API for programmatic access

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Chrome/Chromium browser (for Selenium)
- ChromeDriver (compatible with your Chrome version)

### Installation

1. **Clone/Download the project** to your machine

2. **Create a virtual environment** (recommended):
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Download ChromeDriver**:
   - Download from: https://chromedriver.chromium.org/
   - Extract it to your project directory or add it to PATH
   - Ensure it matches your Chrome version

### Running the Application

```bash
python main.py
```

The application will start on `http://localhost:8000`

Open your browser and navigate to:
- **Main Interface**: http://localhost:8000/
- **API Status**: http://localhost:8000/api/status
- **Download File**: http://localhost:8000/download

## 🎨 Interface Features

### Dashboard
- **Countdown Timer**: Shows remaining time until next update (updates every second)
- **Status Information**: 
  - Last update timestamp
  - Next scheduled update
  - Current file status
- **Download Button**: Download the latest Excel file
- **Refresh Button**: Manually refresh the status

### Responsive Design
- Works on desktop, tablet, and mobile devices
- Beautiful gradient background
- Smooth animations and transitions
- Arabic language support (RTL)

## 📁 File Structure

```
scraping stocks/
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── excel_files/           # Generated Excel files (auto-created)
├── scrapying_alternatoive.py  # Original scraper
└── backup.py              # Backup scraper
```

## 🔧 Configuration

### Update Interval

To change the update interval from 8 hours, edit `main.py`:

```python
UPDATE_INTERVAL = 8 * 60 * 60  # Change this value (in seconds)
```

Examples:
- 1 hour: `1 * 60 * 60`
- 4 hours: `4 * 60 * 60`
- 12 hours: `12 * 60 * 60`
- 24 hours: `24 * 60 * 60`

### Port Configuration

To run on a different port:

```bash
python main.py --port 8080
```

Or modify the last line in `main.py`:

```python
uvicorn.run(app, host="0.0.0.0", port=8080)
```

## 📡 API Endpoints

### GET `/`
Returns the main HTML dashboard

**Response**: HTML page

### GET `/download`
Downloads the current Excel file

**Response**: Excel file (.xlsx)

**Example**:
```bash
curl http://localhost:8000/download --output stocks.xlsx
```

### GET `/api/status`
Returns the current status as JSON

**Response**:
```json
{
    "last_update": "2025-11-18T10:30:45.123456",
    "next_update": "2025-11-18T18:30:45.123456",
    "file": {
        "path": "excel_files/egx_stocks_20251118_103045.xlsx",
        "name": "egx_stocks_20251118_103045.xlsx"
    },
    "is_scraping": false
}
```

## 🐛 Troubleshooting

### ChromeDriver Issues

**Problem**: "chromedriver not found"

**Solution**:
1. Download ChromeDriver from https://chromedriver.chromium.org/
2. Extract to project directory
3. Or add to system PATH

### Port Already in Use

**Problem**: "Address already in use"

**Solution**:
```bash
# On Windows (PowerShell):
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# On macOS/Linux:
lsof -i :8000
kill -9 <PID>
```

### Selenium/Browser Issues

**Problem**: "Failed to start browser"

**Solution**:
- Ensure Chrome is installed
- Update ChromeDriver to match Chrome version
- Check ChromeDriver compatibility with your OS

### Excel File Not Downloading

**Problem**: "File not found" error

**Solution**:
- First scrape hasn't completed yet (wait for initial scrape)
- Check if `excel_files` folder has the file
- Check application logs for errors

## 📊 Data

The scraper collects the following fields:
- Company Name (اسم الشركة)
- Sector (القطاع)
- Previous Close (الإقفال السابق)
- Opening Price (سعر الفتح)
- Closing Price (سعر الاغلاق)
- Change % (نسبة التغير%)
- Last Price (آخر سعر)
- High Price (اعلى سعر)
- Low Price (اقل سعر)
- Value in EGP (القيمة - جنيه)
- Volume (الكمية)
- Number of Transactions (عدد العمليات)
- Market Cap in Millions (رأس المال السوقى)

## 🔒 Security Notes

- The application runs on localhost by default
- For production deployment:
  - Use HTTPS
  - Add authentication
  - Run behind a reverse proxy
  - Set appropriate CORS headers
  - Use environment variables for sensitive config

## 📝 Logs

Application logs are printed to console showing:
- Scraping progress
- Update schedule
- Error messages
- File generation status

## 🚀 Deployment

### Local Network Access

To access from other machines on your network:

```python
# In main.py, change:
uvicorn.run(app, host="0.0.0.0", port=8000)

# Access from other machines:
# http://<your-machine-ip>:8000
```

### Docker Deployment (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

Build and run:
```bash
docker build -t stock-scraper .
docker run -p 8000:8000 stock-scraper
```

## 📄 License

This project is provided as-is for educational and personal use.

## 💡 Tips

1. **First Run**: Initial scrape will happen immediately on startup
2. **Background Processing**: The app performs scraping in the background, so UI remains responsive
3. **No Manual Intervention**: Once running, the application handles everything automatically
4. **Excel Format**: Files are saved in modern .xlsx format for compatibility

## 🤝 Support

For issues:
1. Check the troubleshooting section
2. Review application console logs
3. Verify all dependencies are installed
4. Check network connectivity for web scraping

---

Made with ❤️ for stock market enthusiasts
