# Quick Start Guide

## What You Have

✅ **FastAPI Backend** - REST API for scraping  
✅ **Browserless Integration** - No Chrome setup needed on Railway  
✅ **Backup.py Code** - Integrated into `scraper.py`  
✅ **Production Ready** - Docker + Railway configured  

## 3-Minute Setup

### Option 1: Deploy to Railway (Recommended)

```powershell
# 1. Push to GitHub
cd e:\scraping stocks
git add .
git commit -m "Add FastAPI with Browserless"
git push origin main

# 2. Go to Railway Dashboard
# https://railway.app/dashboard

# 3. Create New Project → Deploy from GitHub
# Select your scraping-stock repo

# 4. Done! Railway auto-deploys
```

### Option 2: Test Locally First

```powershell
# 1. Start Browserless
docker run -p 3000:3000 browserless/chrome:latest

# 2. In another terminal
cd e:\scraping stocks
$env:BROWSERLESS_URL = "http://localhost:3000/webdriver"
python -m uvicorn main:app --reload

# 3. Visit API
# http://localhost:8000
```

## Using the API

### Start Scraping
```powershell
curl -X POST http://localhost:8000/scrape
# or on Railway: https://your-app.railway.app/scrape
```

### Check Status
```powershell
curl http://localhost:8000/status
```

### Download Results
```powershell
curl http://localhost:8000/files
curl http://localhost:8000/latest
```

## Key Files

| File | Purpose |
|------|---------|
| `main.py` | FastAPI app with endpoints |
| `scraper.py` | Backup.py code (integrated) |
| `Dockerfile` | Production image |
| `railway.yml` | Railway configuration |
| `.railway/nixpacks.toml` | Build config |

## What's Different from Backup.py?

✅ **Backup.py code** → Extracted to `scraper.py`  
✅ **Local Chrome** → Now uses Browserless  
✅ **CLI only** → Now has REST API endpoints  
✅ **Manual run** → Now background tasks + scheduling  

## Next Steps

### 1. Commit & Push
```powershell
git add .
git commit -m "Add FastAPI + Browserless"
git push origin main
```

### 2. Deploy to Railway
- Go to https://railway.app/dashboard
- New Project → Deploy from GitHub
- Select repo → Auto-deploy!

### 3. Monitor
- Railway Dashboard → web-scraper → Logs
- Look for: `✓ Uvicorn running on 0.0.0.0:8000`

### 4. Test
```powershell
# Get your Railway URL from dashboard
$url = "https://your-app.railway.app"

# Test endpoint
curl "$url/health"

# Start scraping
curl -X POST "$url/scrape"

# Check status
curl "$url/status"
```

## Troubleshooting

### Error: "Browserless connection refused"
- Make sure Browserless is running: `docker ps`
- Set `BROWSERLESS_URL` env var

### Error: "Module not found"
- Run: `pip install -r requirements.txt`
- Check Python 3.11+ is installed

### Error: "Port 8000 in use"
- Kill process: `lsof -i :8000` (Mac/Linux)
- Or use different port: `--port 8001`

## API Documentation

Once deployed, visit:
- **Local**: http://localhost:8000/docs
- **Railway**: https://your-app.railway.app/docs

Swagger UI shows all endpoints with try-it-out feature!

---

**Ready?** → Run: `git push origin main`
