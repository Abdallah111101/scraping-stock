# Selenium Grid Quick Reference

## What is Selenium Grid?
Selenium Grid is a distributed testing platform that allows you to run browser automation across multiple machines and browsers simultaneously.

For Railway deployment, we use pre-configured Docker images:
- **Chrome** (`selenium/node-chrome`)
- **Firefox** (`selenium/node-firefox`)
- **Edge** (`selenium/node-edge`)
- **Hub** (`selenium/hub`)

## Quick Commands

### Local Development

```bash
# Start Grid (all 3 browsers + hub)
docker-compose up -d

# Stop Grid
docker-compose down

# View running services
docker-compose ps

# View logs
docker-compose logs -f selenium-hub
docker-compose logs -f chrome-node
```

### Windows Users
```bash
# Run the batch script instead
start_grid.bat

# Then choose option 1 to start
```

### Mac/Linux Users
```bash
# Run the shell script
bash start_grid.sh

# Then choose option 1 to start
```

## Testing the Scraper

```bash
# Make sure Grid is running first
docker-compose up -d

# Then run the scraper
python selenium_grid_railway.py

# To use specific browser, edit selenium_grid_railway.py:
# Change: scraper.initialize_chrome_driver()
# To:     scraper.initialize_firefox_driver()
# Or:     scraper.initialize_edge_driver()
```

## Railway Deployment Steps

### 1. Add to Railway Project
- Create `railway.yml` in repo (✓ Done)
- Create `Dockerfile` (✓ Done)
- Commit and push to GitHub

### 2. Set Environment Variables
In Railway Dashboard:
```
SELENIUM_GRID_URL=http://selenium-hub:4444
PYTHONUNBUFFERED=1
```

### 3. Deploy
```bash
git push origin main
# Railway auto-deploys!
```

## File Reference

| File | Purpose |
|------|---------|
| `selenium_grid_railway.py` | Main scraper with Grid support |
| `docker-compose.yml` | Local development setup |
| `railway.yml` | Railway cloud deployment config |
| `Dockerfile` | Container image specification |
| `start_grid.sh` | Quick start script (Mac/Linux) |
| `start_grid.bat` | Quick start script (Windows) |
| `SELENIUM_GRID_RAILWAY.md` | Full deployment guide |

## Troubleshooting

### Grid not starting
```bash
# Check Docker is running
docker ps

# View logs
docker-compose logs

# Rebuild
docker-compose down
docker-compose up -d --build
```

### Connection timeout
```bash
# Verify Grid is accessible
curl http://localhost:4444/status

# Check service logs
docker-compose logs selenium-hub
```

### Browser crashes
```bash
# Increase shared memory
# In docker-compose.yml, update:
shm_size: 3gb

# Or restart with more memory
docker-compose down
docker-compose up -d
```

### Python dependencies missing
```bash
# Update requirements.txt
pip freeze > requirements.txt

# Rebuild Docker image
docker-compose build --no-cache
docker-compose up -d
```

## Performance Notes

- **Max parallel sessions**: 9 (3 per browser × 3 browsers)
- **Session timeout**: 300 seconds (configurable)
- **Memory per node**: ~512MB minimum
- **Hub memory**: ~256MB minimum

## Next Steps

1. ✅ Created Selenium Grid setup
2. ✅ Created Docker Compose configuration  
3. ✅ Created Railway deployment config
4. ⬜ Test locally with `start_grid.bat`
5. ⬜ Verify scraper works
6. ⬜ Push to GitHub
7. ⬜ Deploy to Railway

---

**For detailed instructions**: See `SELENIUM_GRID_RAILWAY.md`
