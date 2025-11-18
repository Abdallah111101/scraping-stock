# Railway Selenium Grid Deployment Guide

## Overview
This guide explains how to deploy the EGX Stock Scraper using Selenium Grid on Railway with pre-configured Chrome, Firefox, and Edge browsers.

## Prerequisites
- Railway account (https://railway.app)
- Docker installed locally (for testing)
- Git repository connected to Railway

## Local Testing with Docker Compose

### 1. Start Selenium Grid Locally
```bash
docker-compose up -d
```

This starts:
- **Selenium Hub**: http://localhost:4444
- **Chrome Node**: Browser for scraping
- **Firefox Node**: Alternative browser
- **Edge Node**: Alternative browser

### 2. Verify Grid is Running
```bash
curl http://localhost:4444/status
```

Expected response: `{"ready":true}`

### 3. Run the Scraper Locally
```bash
# With local Selenium Grid (default)
python selenium_grid_railway.py

# Or specify custom grid URL
SELENIUM_GRID_URL=http://localhost:4444 python selenium_grid_railway.py
```

### 4. View Grid Dashboard
Open browser to: http://localhost:4444

## Deploying to Railway

### Step 1: Create Railway Project

1. Go to https://railway.app/dashboard
2. Click "New Project"
3. Select "Deploy from GitHub"
4. Choose your scraping-stock repository

### Step 2: Add Services via railway.yml

Railway will detect the `railway.yml` file and create services:

- **selenium-hub**: Grid Hub (Port 4444)
- **chrome-node**: Chrome browser
- **firefox-node**: Firefox browser  
- **edge-node**: Edge browser
- **web-scraper**: Python scraper application

### Step 3: Configure Environment Variables

In Railway Dashboard, set these for the **web-scraper** service:

```
SELENIUM_GRID_URL=http://selenium-hub:4444
PYTHONUNBUFFERED=1
```

### Step 4: Set Resource Limits

In Railway Dashboard for each browser node:

- **Memory**: 512MB per node
- **CPU**: 0.5x

For hub:
- **Memory**: 256MB
- **CPU**: 0.25x

### Step 5: Deploy

Push your changes to GitHub:

```bash
git add .
git commit -m "Add Selenium Grid configuration"
git push origin main
```

Railway will automatically deploy!

## File Structure

```
├── selenium_grid_railway.py   # Main scraper with Grid support
├── docker-compose.yml         # Local development setup
├── railway.yml                # Railway deployment config
├── Dockerfile                 # Container image
├── requirements.txt           # Python dependencies
└── excel_files/               # Output directory for results
```

## Usage

### Chrome Browser (Default)
```python
scraper = SeleniumGridScraper()
df = scraper.scrape_egx_stocks()
```

### Firefox Browser
```python
scraper = SeleniumGridScraper()
scraper.initialize_firefox_driver()
df = scraper.scrape_egx_stocks()
```

### Edge Browser
```python
scraper = SeleniumGridScraper()
scraper.initialize_edge_driver()
df = scraper.scrape_egx_stocks()
```

## Monitoring

### View Logs in Railway

1. Go to Railway Dashboard
2. Select your project
3. Click on **web-scraper** service
4. View real-time logs

### Grid Status

Check Selenium Grid status:
```bash
curl https://your-railway-url:4444/status
```

## Troubleshooting

### Issue: "Connection refused"
**Solution**: Make sure Selenium Hub is running and accessible
```bash
# Local test
docker-compose ps

# Check hub is ready
docker-compose logs selenium-hub
```

### Issue: "Browser timeout"
**Solution**: Increase timeout in selenium_grid_railway.py
```python
WebDriverWait(self.driver, 30)  # Increased from 15s
```

### Issue: "Out of memory"
**Solution**: 
- Reduce browser nodes from 3 to 2 per node
- Increase Railway resource allocation
- Edit `docker-compose.yml` shm_size

### Issue: "Grid hub not found"
**Solution**: Verify service names in railway.yml match environment variables

```bash
# Check service connectivity
docker-compose exec web-scraper ping selenium-hub
```

## Performance Tips

1. **Parallel Requests**: Use multiple nodes
   - Chrome, Firefox, Edge can run simultaneously
   - Max 9 concurrent sessions (3 per node × 3 nodes)

2. **Session Reuse**: Keep driver alive for multiple scrapes

3. **Resource Allocation**: 
   - Hub: 256MB minimum
   - Each node: 512MB minimum
   - Python app: 256-512MB

## Stopping Services

### Locally
```bash
docker-compose down
```

### On Railway
- Go to Dashboard
- Click "Pause" on project
- Or click "Delete" to remove services

## Advanced: Custom Browser Configuration

Edit `selenium_grid_railway.py` to add custom browser options:

```python
options = webdriver.ChromeOptions()
options.add_argument('--incognito')  # Private mode
options.add_argument('--disable-popup-blocking')
options.set_capability('pageLoadStrategy', 'eager')
```

## Support

- Railway Docs: https://docs.railway.app
- Selenium Docs: https://www.selenium.dev/documentation
- Docker Compose: https://docs.docker.com/compose

---

**Next Steps**:
1. Run locally with docker-compose
2. Test the scraper
3. Push to GitHub
4. Railway auto-deploys
5. Monitor in Railway Dashboard
