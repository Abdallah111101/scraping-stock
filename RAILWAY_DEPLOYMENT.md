# Railway Deployment Configuration
# This file documents the deployment setup for Railway.app

## Railway.app Deployment Guide

### Prerequisites
- Railway account (free tier available)
- GitHub repository connected to Railway
- Docker images available

### Deployment Options

#### Option 1: Using Railway Selenium Grid Template (Recommended)
Railway offers pre-configured Selenium Grid templates that include:
- Selenium Hub
- Chrome, Firefox, and Edge nodes
- Automatic scaling and management

Steps:
1. Go to Railway.app dashboard
2. Create new project
3. Search for "Selenium Grid" template
4. Deploy template

#### Option 2: Deploy with Docker Compose
1. Connect your GitHub repository to Railway
2. Configure environment variables:
   - `SELENIUM_GRID_URL=http://selenium-hub:4444`
   - `PORT=8000`

3. Railway will automatically detect docker-compose.yml

#### Option 3: Deploy Individual Services
Create multiple Railway services:

**Service 1: Selenium Hub**
- Docker Image: `selenium/hub:4.15.0`
- Ports: 4444, 4442, 4443
- Environment: GRID_MAX_SESSION=10

**Service 2: Chrome Node**
- Docker Image: `selenium/node-chrome:4.15.0`
- Links: Connect to Selenium Hub
- Memory: 2GB recommended

**Service 3: Firefox Node**
- Docker Image: `selenium/node-firefox:4.15.0`
- Links: Connect to Selenium Hub
- Memory: 2GB recommended

**Service 4: Edge Node**
- Docker Image: `selenium/node-edge:4.15.0`
- Links: Connect to Selenium Hub
- Memory: 2GB recommended

**Service 5: FastAPI App**
- Build from Dockerfile
- Port: 8000 (public)
- Links: Connect to Selenium Hub
- Environment:
  - SELENIUM_GRID_URL: From Selenium Hub service
  - PYTHONUNBUFFERED=1

### Environment Variables
Set these in Railway project settings:

```
SELENIUM_GRID_URL=http://selenium-hub:4444
PORT=8000
PYTHONUNBUFFERED=1
```

### Volume Mounting
- Mount `/data` directory to persist Excel files
- Railway provides persistent storage out of the box

### Scaling
- Selenium nodes can be scaled up for concurrent sessions
- FastAPI app can be scaled for multiple instances

### Monitoring
- Railway dashboard shows real-time logs
- Health checks automatically manage service restarts
- Monitor CPU, memory, and network usage

### Cost Optimization
- Use Railway's free tier for development
- Optimize Selenium node count (default: 3 sessions per node)
- Set appropriate SESSION_TIMEOUT values

### Deployment Steps:

1. **Push code to GitHub:**
   ```bash
   git add .
   git commit -m "Add FastAPI scraper with Selenium Grid"
   git push origin main
   ```

2. **Connect to Railway:**
   - Go to https://railway.app
   - Click "New Project"
   - Select "Deploy from GitHub"
   - Choose your repository

3. **Configure services:**
   - If using docker-compose.yml, Railway auto-detects it
   - Set environment variables in project settings
   - Configure port exposure (8000 for FastAPI)

4. **Deploy:**
   - Railway auto-deploys on git push
   - Monitor deployment logs
   - Verify health checks pass

5. **Access application:**
   - Railway provides a unique URL
   - Your app will be available at: `https://<railway-url>/`

### Troubleshooting

**Selenium Grid connection fails:**
- Verify Selenium Hub service is running
- Check SELENIUM_GRID_URL environment variable
- Increase timeout values in scraper.py

**Out of memory errors:**
- Scale down number of browser nodes
- Increase available memory per service
- Review browser session timeout settings

**Slow scraping:**
- Add more browser nodes
- Optimize XPath selectors
- Review network latency with Railway

### Additional Notes

- The application stores Excel files in `/data` volume
- Ensure persistent storage is configured for data retention
- Set up notifications for scraping failures
- Consider rate limiting for the API endpoints

### Local Testing Before Railway:

```bash
# Build and run locally
docker-compose up -d

# Access at http://localhost:8000
# Download scraped data from the dashboard
# Check logs: docker-compose logs -f app
```

### Railway CLI Commands:

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Deploy
railway up

# View logs
railway logs

# List services
railway services

# Stop service
railway stop [service-name]
```

### Support
For Railway-specific issues, visit: https://railway.app/docs
For Selenium Grid issues, visit: https://www.selenium.dev/documentation/grid/
