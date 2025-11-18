# Quick Start Guide - Railway Deployment

## 5-Minute Deployment

### Prerequisites
- GitHub account with your code pushed
- Railway.app account (sign up free at https://railway.app)

### Step-by-Step Deployment

#### 1. Prepare Your Repository (2 minutes)

```bash
cd scraping-stocks

# Ensure all files are committed
git status

# Push to GitHub
git push origin main
```

#### 2. Deploy on Railway (2 minutes)

1. **Go to Railway Dashboard**
   - Visit https://railway.app/dashboard

2. **Create New Project**
   - Click "Create New Project"
   - Select "Deploy from GitHub repo"

3. **Select Repository**
   - Choose your `scraping-stocks` repository
   - Click "Deploy"

4. **Wait for Deployment**
   - Railway will auto-detect docker-compose.yml
   - Services will start automatically
   - You can monitor progress in the dashboard

#### 3. Configure Environment Variables (1 minute)

1. **Go to Project Settings**
   - Click on your project
   - Go to "Variables" tab

2. **Add Variables**
   - `SELENIUM_GRID_URL=http://selenium-hub:4444`
   - `PYTHONUNBUFFERED=1`
   - `PORT=8000`

3. **Save**
   - Variables apply automatically

#### 4. Verify Deployment

1. **Check Service Status**
   - All services should show ✓ (healthy)
   - App service should show "Deploying" → "Running"

2. **Get Public URL**
   - Click on "egx-scraper-app" service
   - Copy the public URL (e.g., `https://your-app-name.railway.app`)

3. **Test Application**
   - Open the URL in browser
   - You should see the stock scraper dashboard

### What Gets Created

Railway automatically creates:

| Service | Status | Port | Purpose |
|---------|--------|------|---------|
| selenium-hub | Private | 4444 | Grid coordination |
| chrome | Private | 7900 | Chrome browser sessions |
| firefox | Private | 7901 | Firefox browser sessions |
| edge | Private | 7902 | Edge browser sessions |
| **egx-scraper-app** | **Public** | **8000** | Your FastAPI app |

### First Scraping Run

1. **Access Dashboard**
   - Go to your Railway URL
   - You'll see the web interface

2. **Initial Scraping**
   - App starts first scraping immediately
   - Check countdown timer
   - Download Excel file once ready

3. **Automatic Updates**
   - Next scraping in 8 hours
   - Updates happen automatically
   - Dashboard shows countdown

### Monitoring

#### View Logs
```
In Railway Dashboard:
1. Click your service
2. View "Deploy" tab for logs
3. Click "Logs" for real-time output
```

#### Check Status
- **Dashboard:** http://your-railway-url/
- **API Status:** http://your-railway-url/status
- **Railway Dashboard:** View service health

### Common Issues & Solutions

#### Services Won't Start
- **Problem:** Services stuck in "Deploying"
- **Solution:** 
  1. Check logs for errors
  2. Verify environment variables set correctly
  3. Increase Railway plan resources

#### Can't Connect to Selenium Grid
- **Problem:** App shows error connecting to hub
- **Solution:**
  1. Verify `SELENIUM_GRID_URL=http://selenium-hub:4444`
  2. Ensure selenium-hub service is healthy
  3. Wait for all services to fully start

#### Out of Memory
- **Problem:** Services crash with OOM
- **Solution:**
  1. Upgrade Railway plan (paid tier)
  2. Reduce browser nodes
  3. Reduce max sessions per node

#### Downloads Not Working
- **Problem:** Excel file download fails
- **Solution:**
  1. Check if scraping completed
  2. View app logs for errors
  3. Manually trigger: `POST /trigger-scraping`

### Scaling Your Deployment

#### Add More Browser Capacity
Edit `docker-compose.yml` - add new nodes:

```yaml
  chrome-2:
    image: selenium/node-chrome:4.15.0
    depends_on:
      - selenium-hub
    # Copy settings from chrome service
```

Then redeploy:
```bash
git add docker-compose.yml
git commit -m "Add extra Chrome node"
git push origin main
```

#### Reduce Resource Usage
Modify `docker-compose.yml`:

```yaml
  app:
    # Lower memory usage
    # (Note: Railway env > docker-compose)
```

### Persistent Storage

Your Excel files are automatically stored in a persistent volume:
- **Path:** `/app/data/`
- **Size:** 1GB per Railway plan
- **Survives:** Service restarts, updates

To access files:
- Download through dashboard
- Access via `/download/egx_stocks_latest.xlsx`

### Next Steps

1. **Set Up Monitoring**
   - Add email alerts in Railway settings
   - Monitor service health dashboard

2. **Configure Backups**
   - Use Railway's backup feature
   - Or implement external backup

3. **Performance Optimization**
   - Monitor logs for bottlenecks
   - Adjust timeouts if needed
   - Scale nodes based on demand

4. **Production Hardening**
   - Add authentication (optional)
   - Implement rate limiting
   - Set up CDN for downloads

### Support Resources

- **Railway Docs:** https://railway.app/docs
- **Railway Community:** https://discord.gg/railway
- **This Project:** Check README.md

### Useful Railway Commands

```bash
# Install Railway CLI (optional)
npm install -g @railway/cli

# Login
railway login

# View logs
railway logs

# Check service status
railway services

# Redeploy
railway deploy
```

---

## Post-Deployment Checklist

- [ ] All services show as "healthy" ✓
- [ ] Can access dashboard at public URL
- [ ] Initial scraping has completed
- [ ] Excel file is downloadable
- [ ] Countdown timer shows correctly
- [ ] Environment variables are set
- [ ] Logs show no errors
- [ ] Performance is acceptable

## Troubleshooting Checklist

Before reaching out for support:

- [ ] Checked all service logs
- [ ] Verified environment variables
- [ ] Confirmed services are healthy
- [ ] Tried manual trigger via POST /trigger-scraping
- [ ] Checked Railway plan resource limits
- [ ] Reviewed docker-compose.yml syntax

---

**Deployment Status:** ✅ Ready for Production

Happy scraping! 📊
