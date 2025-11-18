# EGX Stock Scraper - FastAPI + Selenium Grid

A production-ready web application that scrapes Egyptian Exchange (EGX) stock data every 8 hours and provides a web interface to download the data. Built with FastAPI, Selenium Grid, and containerized for Railway deployment.

## Features

✅ **Automated Scheduling** - Scrapes data every 8 hours automatically  
✅ **Web Dashboard** - Real-time countdown timer showing next update  
✅ **Download Management** - Direct download links for Excel files  
✅ **Selenium Grid** - Uses Chrome, Firefox, and Edge browsers for reliable scraping  
✅ **Docker Containerized** - Multi-container setup with docker-compose  
✅ **Railway Ready** - Pre-configured for deployment on Railway.app  
✅ **Health Checks** - Built-in health monitoring for all services  
✅ **Error Handling** - Comprehensive error reporting and logging  

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    FastAPI Application                   │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Web Dashboard (HTML/JS)                           │ │
│  │  - Real-time countdown timer                       │ │
│  │  - Download links                                  │ │
│  │  - Status display                                  │ │
│  └────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────┐ │
│  │  FastAPI Routes                                    │ │
│  │  - GET /           (dashboard)                     │ │
│  │  - GET /status     (JSON status)                   │ │
│  │  - GET /download   (file download)                 │ │
│  │  - POST /trigger   (manual trigger)                │ │
│  └────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Scheduler (APScheduler)                           │ │
│  │  - 8-hour intervals                                │ │
│  │  - Background tasks                                │ │
│  └────────────────────────────────────────────────────┘ │
└──────────────────┬───────────────────────────────────────┘
                   │
      ┌────────────┼────────────┐
      │            │            │
      ▼            ▼            ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ Selenium    │ │ Selenium    │ │ Selenium    │
│ Chrome Node │ │ Firefox Node│ │ Edge Node   │
│ (3 sessions)│ │ (3 sessions)│ │ (3 sessions)│
└──────┬──────┘ └──────┬──────┘ └──────┬──────┘
       │               │               │
       └───────────────┼───────────────┘
                       │
                       ▼
                ┌──────────────┐
                │ Selenium Hub │
                │ (Grid Hub)   │
                └──────────────┘
```

## Project Structure

```
scraping-stocks/
├── main.py                    # FastAPI application
├── scraper.py                 # Selenium Grid scraper
├── Dockerfile                 # App container
├── docker-compose.yml         # Multi-container orchestration
├── requirements.txt           # Python dependencies
├── railway.json              # Railway deployment config
├── RAILWAY_DEPLOYMENT.md     # Railway setup guide
├── .env.example              # Environment variables template
├── data/                     # Persistent data directory
│   └── egx_stocks_latest.xlsx
└── README.md                 # This file
```

## Prerequisites

- Docker & Docker Compose (for local development)
- Python 3.11+ (for local running without Docker)
- Railway.app account (for deployment)
- GitHub repository (to push code)

## Local Development Setup

### Using Docker Compose (Recommended)

```bash
# Clone repository
git clone <your-repo-url>
cd scraping-stocks

# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f app

# Access the application
# Open browser to http://localhost:8000

# Stop services
docker-compose down
```

### Without Docker (Development Only)

**Note:** This requires a Selenium Grid instance running separately or accessible.

```bash
# Create virtual environment
python -m venv venv

# Activate venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variable
# Windows:
set SELENIUM_GRID_URL=http://localhost:4444
# Linux/Mac:
export SELENIUM_GRID_URL=http://localhost:4444

# Run application
python main.py
# Or with uvicorn:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Dashboard
**GET** `/`
- Returns the web interface with status and download link
- Shows countdown timer for next update
- Provides download button when data available

### Status Endpoint
**GET** `/status`
- Returns JSON with current status
- Shows last update time, next update time
- Indicates if scraping is in progress

**Response:**
```json
{
  "current_file": "egx_stocks_latest.xlsx",
  "last_update": "2024-01-18T14:30:00.000000",
  "next_update": "2024-01-18T22:30:00.000000",
  "is_scraping": false,
  "error_message": null,
  "file_exists": true
}
```

### Download Endpoint
**GET** `/download/{filename}`
- Downloads the Excel file
- Filename: `egx_stocks_latest.xlsx`

### Manual Trigger
**POST** `/trigger-scraping`
- Manually trigger scraping job
- Useful for testing and emergency updates

## Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
# Selenium Grid URL (local)
SELENIUM_GRID_URL=http://selenium-hub:4444

# FastAPI
PORT=8000

# Python
PYTHONUNBUFFERED=1
```

### Docker Compose Environment

Services can be customized in `docker-compose.yml`:

- **Selenium Hub** ports: 4444, 4442, 4443
- **Chrome VNC**: 7900 (for debugging)
- **Firefox VNC**: 7901 (for debugging)
- **Edge VNC**: 7902 (for debugging)
- **FastAPI**: 8000 (public)

## Deployment to Railway

### Step 1: Prepare Repository

```bash
# Initialize git (if not done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: EGX scraper with FastAPI and Selenium Grid"

# Push to GitHub
git push origin main
```

### Step 2: Deploy on Railway

1. Go to [Railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub"
4. Select your repository
5. Railway will automatically detect the docker-compose.yml

### Step 3: Configure Environment

In Railway dashboard:
1. Go to project settings
2. Add environment variables:
   - `SELENIUM_GRID_URL=http://selenium-hub:4444`
   - `PYTHONUNBUFFERED=1`
   - `PORT=8000`

### Step 4: Configure Network

1. Set FastAPI service port to public (8000)
2. Selenium services remain private
3. Railway provides a public URL

### Step 5: Verify Deployment

1. Check deployment logs for errors
2. Wait for all services to become healthy
3. Access your app at the provided URL
4. Test the dashboard and download functionality

## Monitoring & Logs

### Local Development

```bash
# View all logs
docker-compose logs -f

# View specific service
docker-compose logs -f app
docker-compose logs -f selenium-hub
docker-compose logs -f chrome

# Check service health
docker-compose ps
```

### Railway

1. Dashboard automatically shows logs
2. Click on service to view detailed logs
3. Set up alerts for service failures

## Performance Tuning

### Browser Nodes

Adjust in `docker-compose.yml`:

```yaml
environment:
  - SE_NODE_MAX_SESSIONS=3  # Sessions per node
  - SE_NODE_SESSION_TIMEOUT=300  # Seconds
  - GRID_TIMEOUT=300  # Hub timeout
```

### Memory Limits

```yaml
services:
  chrome:
    shm_size: 2gb  # Shared memory for Chrome
  app:
    # In Railway: Set memory in service settings
```

### Scaling

Add more browser nodes in `docker-compose.yml`:

```yaml
  chrome-2:
    image: selenium/node-chrome:4.15.0
    depends_on:
      - selenium-hub
    # ... (copy from chrome service)
```

## Troubleshooting

### Selenium Grid Connection Failed

**Problem:** App can't connect to Selenium Grid

**Solutions:**
1. Check if selenium-hub is healthy: `docker-compose ps`
2. Verify SELENIUM_GRID_URL is correct
3. Check network connectivity: `docker network ls`
4. View hub logs: `docker-compose logs selenium-hub`

### Memory Issues

**Problem:** Containers keep restarting

**Solutions:**
1. Reduce SE_NODE_MAX_SESSIONS value
2. Increase available memory in docker-compose.yml
3. Remove unnecessary browser nodes
4. In Railway: Upgrade plan for more resources

### Scraping Timeouts

**Problem:** Scraper times out or incomplete data

**Solutions:**
1. Increase wait times in scraper.py
2. Add more browser nodes for parallelization
3. Check EGX website availability
4. Review XPath selectors validity

### Download Links Not Working

**Problem:** Excel file not downloadable

**Solutions:**
1. Check if scraping completed successfully
2. Verify data directory permissions
3. Check `docker-compose ps` for app status
4. View app logs for errors

## Data Persistence

- Excel files are stored in `/data` volume
- Local: `./data` directory
- Railway: Persistent volume (auto-created)
- Files survive container restarts

## Security Considerations

1. The application runs on port 8000 (public in Railway)
2. No authentication implemented (add if needed)
3. Consider adding rate limiting for production
4. Validate file downloads to prevent path traversal

## Future Enhancements

- [ ] Authentication & authorization
- [ ] Multiple data formats (CSV, JSON, PDF)
- [ ] Email notifications on updates
- [ ] Data caching for faster downloads
- [ ] Database integration (PostgreSQL)
- [ ] Advanced analytics dashboard
- [ ] API authentication (JWT/API keys)
- [ ] Webhook notifications

## Maintenance

### Regular Tasks

- Monitor disk usage for Excel files
- Check logs for recurring errors
- Verify scraping data quality
- Update dependencies quarterly
- Test Railway deployment monthly

### Backup Strategy

```bash
# Local backup
docker cp egx-scraper-app:/app/data ./data-backup

# Automate backups
# Add cron job or use Railway's backup features
```

## Support & Documentation

- **FastAPI Docs:** http://localhost:8000/docs
- **Selenium Grid:** https://www.selenium.dev/documentation/grid/
- **Railway Docs:** https://railway.app/docs
- **APScheduler:** https://apscheduler.readthedocs.io/

## License

This project is provided as-is for educational purposes.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Push and create a pull request

---

**Last Updated:** January 2024  
**Version:** 1.0.0
