# EGX Stock Scraper - FastAPI + Browserless on Railway

FastAPI-based stock scraper for Egyptian Exchange (EGX) with Browserless Chrome integration on Railway.

## Architecture

```
FastAPI App (Port 8000)
    ↓
Browserless Chrome (Port 3000)
    ↓
EGX Website
    ↓
Excel Output
```

## Features

✅ **FastAPI REST API** - Full HTTP endpoints for scraping  
✅ **Browserless Integration** - No local Chrome needed on Railway  
✅ **Background Scraping** - Non-blocking async operations  
✅ **Excel Export** - Automatic data persistence  
✅ **Health Checks** - Built-in monitoring  
✅ **File Management** - Download and list scrape results  

## API Endpoints

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info and available endpoints |
| `/health` | GET | Health check status |
| `/scrape` | POST | Start scraping (background task) |
| `/status` | GET | Current scraping status |
| `/latest` | GET | Latest scrape file info |

### File Management

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/files` | GET | List all scrape files |
| `/download/{filename}` | GET | Download specific file |

## Local Development

### Prerequisites

- Docker Desktop installed
- Python 3.11+
- pip

### Setup

1. **Clone and install:**
```bash
cd scraping-stocks
pip install -r requirements.txt
```

2. **Start Browserless locally:**
```bash
docker run -p 3000:3000 browserless/chrome:latest
```

3. **In another terminal, run FastAPI:**
```bash
export BROWSERLESS_URL=http://localhost:3000/webdriver
python -m uvicorn main:app --reload
```

4. **Access API:**
```
http://localhost:8000
```

### Test Scraping

```bash
# Start scraping
curl -X POST http://localhost:8000/scrape

# Check status
curl http://localhost:8000/status

# List files
curl http://localhost:8000/files

# Download latest
curl -O "http://localhost:8000/latest"
```

## Railway Deployment

### Step 1: Connect to Railway

1. Go to https://railway.app/dashboard
2. Click "New Project"
3. Select "Deploy from GitHub"
4. Select your `scraping-stock` repository

### Step 2: Configure Services

Railway auto-detects `railway.yml` and creates:
- **browserless** - Chrome service (Port 3000)
- **web-scraper** - FastAPI app (Port 8000)

### Step 3: Set Environment Variables

For **web-scraper** service:
```
BROWSERLESS_URL=http://browserless:3000/webdriver
PYTHONUNBUFFERED=1
PORT=8000
```

### Step 4: Deploy

```bash
git add .
git commit -m "Add FastAPI + Browserless for Railway"
git push origin main
```

Railway auto-deploys!

## Monitoring in Railway

1. Go to Railway Dashboard
2. Click your project
3. Select **web-scraper** service
4. View logs in real-time

### Expected Success Output

```
Starting EGX Stock Scraper API...
✓ Uvicorn running on 0.0.0.0:8000
Application startup complete
```

## Usage Examples

### cURL

```bash
# Start scraping
curl -X POST https://your-app.railway.app/scrape

# Check status
curl https://your-app.railway.app/status

# List files
curl https://your-app.railway.app/files

# Download latest file
curl -O "https://your-app.railway.app/latest"
```

### Python

```python
import requests
import json

BASE_URL = "https://your-app.railway.app"

# Start scraping
response = requests.post(f"{BASE_URL}/scrape")
print(json.dumps(response.json(), indent=2))

# Check status
status = requests.get(f"{BASE_URL}/status").json()
print(f"Is scraping: {status['is_scraping']}")

# Download file
latest = requests.get(f"{BASE_URL}/latest").json()
file_url = f"{BASE_URL}{latest['download_url']}"
print(f"Download: {file_url}")
```

### JavaScript/Node.js

```javascript
const BASE_URL = "https://your-app.railway.app";

// Start scraping
fetch(`${BASE_URL}/scrape`, { method: 'POST' })
  .then(r => r.json())
  .then(data => console.log(data));

// Check status
fetch(`${BASE_URL}/status`)
  .then(r => r.json())
  .then(data => console.log('Scraping:', data.is_scraping));
```

## File Structure

```
├── main.py                  # FastAPI application
├── scraper.py              # Scraping logic
├── Dockerfile              # Multi-stage Docker build
├── railway.yml             # Railway services config
├── .railway/nixpacks.toml  # Railway build config
├── Procfile               # Railway process file
├── requirements.txt        # Python dependencies
├── config.ini             # Configuration
└── excel_files/           # Output directory (created at runtime)
```

## Troubleshooting

### Issue: "Connection refused" to Browserless

**Solution**: Verify Browserless is running
```bash
curl http://localhost:3000  # Local
# OR check Railway logs for browserless service
```

### Issue: "Port already in use"

**Solution**: Kill process on port 3000/8000
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Mac/Linux
lsof -i :3000
kill -9 <PID>
```

### Issue: Long scraping time

**Solution**: Browserless is working! Large pages take time. Monitor via `/status` endpoint.

### Issue: "Service Unavailable" on Railway

**Solution**: Check logs
```
Railway Dashboard → Services → web-scraper → Logs
```

Common fixes:
- Ensure `BROWSERLESS_URL` env var is set correctly
- Rebuild with: Push to GitHub again
- Check Browserless service is healthy

## Performance

- **Browserless startup**: ~10-15 seconds
- **Page load**: ~30 seconds
- **Scraping**: ~2-5 minutes (depending on data volume)
- **Total time**: ~3-7 minutes per run

## Limits

| Resource | Limit |
|----------|-------|
| Build time | 20 minutes |
| Memory | 512MB (Browserless) + 256MB (FastAPI) |
| Disk | 1GB |
| Timeout | 30 minutes per request |

## Advanced Configuration

### Custom Browserless Options

Edit `scraper.py`:
```python
def get_chrome_driver():
    browserless_url = os.getenv('BROWSERLESS_URL')
    options = webdriver.ChromeOptions()
    options.add_argument('--custom-arg')  # Add here
```

### Scheduled Scraping

Add a scheduler task (requires external service like cron):
```python
# Use schedule library
import schedule
schedule.every(8).hours.do(run_scraper)
```

## Support

- **Railway Docs**: https://docs.railway.app
- **Browserless Docs**: https://www.browserless.io/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Selenium Docs**: https://www.selenium.dev/documentation

## Security

⚠️ **Important**:
- Don't expose Browserless directly
- Use Railway's authentication
- Keep dependencies updated
- Monitor API access

---

**Ready to deploy?**

```bash
git push origin main
# Watch Railway Dashboard for auto-deploy
```
