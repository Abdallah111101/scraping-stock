# Deployment Checklist

## Pre-Deployment Checklist

### Code Quality
- [ ] All Python files follow PEP 8 style
- [ ] No hardcoded credentials or secrets
- [ ] All imports are used
- [ ] No debug print statements
- [ ] Error handling is comprehensive
- [ ] Logging is configured

### Documentation
- [ ] README.md is complete and accurate
- [ ] QUICK_START_RAILWAY.md is tested
- [ ] RAILWAY_DEPLOYMENT.md covers all scenarios
- [ ] Code comments explain complex logic
- [ ] .env.example has all required variables

### Testing
- [ ] Run local verification: `python verify_setup.py`
- [ ] Test with Docker locally: `docker-compose up -d`
- [ ] Access dashboard at http://localhost:8000
- [ ] Test download functionality
- [ ] Check logs for errors: `docker-compose logs`
- [ ] Verify data/directory has Excel file
- [ ] Trigger manual scrape: `curl -X POST http://localhost:8000/trigger-scraping`

### Configuration
- [ ] SELENIUM_GRID_URL is correct
- [ ] PORT is set to 8000
- [ ] PYTHONUNBUFFERED=1 is set
- [ ] All environment variables documented
- [ ] .gitignore prevents committing data files
- [ ] .gitignore prevents committing .env files

### Dependencies
- [ ] requirements.txt is complete
- [ ] All versions are pinned
- [ ] No conflicting versions
- [ ] Docker base image is stable (python:3.11-slim)

### Docker Files
- [ ] Dockerfile syntax is correct
- [ ] docker-compose.yml syntax is valid YAML
- [ ] All services have health checks
- [ ] Memory limits are reasonable
- [ ] Port mappings are correct
- [ ] Volumes are properly configured

### Git Repository
- [ ] All files are committed
- [ ] No uncommitted changes: `git status`
- [ ] Remote is set correctly: `git remote -v`
- [ ] Branch is main or deploy branch
- [ ] No merge conflicts

---

## Railway Deployment Checklist

### Before Deploying
- [ ] Completed all pre-deployment checks above
- [ ] GitHub repository is public or Railway has access
- [ ] Railway account is created and verified
- [ ] Payment method is added (if on paid plan)

### Deployment Steps
- [ ] Pushed code to GitHub: `git push origin main`
- [ ] Created new project in Railway dashboard
- [ ] Selected "Deploy from GitHub"
- [ ] Connected repository successfully
- [ ] Deployment started automatically
- [ ] No build errors in logs

### Post-Deployment
- [ ] All services show ✓ (healthy)
- [ ] Services are "Running" not "Deploying"
- [ ] Public URL is accessible
- [ ] Environment variables are set:
  - [ ] SELENIUM_GRID_URL=http://selenium-hub:4444
  - [ ] PYTHONUNBUFFERED=1
  - [ ] PORT=8000
- [ ] Dashboard loads at public URL
- [ ] Status endpoint responds: `/status`
- [ ] Initial scraping has completed
- [ ] Excel file is downloadable

### Monitoring
- [ ] Check logs for errors
- [ ] Monitor service health
- [ ] Verify countdown timer works
- [ ] Test manual trigger (if possible)
- [ ] Monitor resource usage

---

## Common Pre-Deployment Issues

### Docker Issues
```
Issue: Docker daemon not running
Fix: Start Docker Desktop (Windows/Mac) or systemctl start docker (Linux)

Issue: Port 8000 already in use
Fix: Kill process: lsof -ti:8000 | xargs kill (Linux/Mac)
     or: netstat -ano | findstr :8000 (Windows)

Issue: docker-compose not found
Fix: Install Docker Desktop (includes compose) or: pip install docker-compose
```

### Python Issues
```
Issue: ModuleNotFoundError for dependencies
Fix: pip install -r requirements.txt

Issue: Selenium can't find Chrome
Fix: This is expected - Chrome is in Docker container
     Use docker-compose up instead of running locally
```

### Permission Issues
```
Issue: Permission denied for data directory
Fix: chmod 755 data/ (Linux/Mac)
     or: Right-click > Properties > Security (Windows)

Issue: .gitignore not working
Fix: git rm -r --cached . && git add . (to reindex)
```

---

## Performance Verification Checklist

### Response Times
- [ ] GET / loads in < 200ms
- [ ] GET /status responds in < 100ms
- [ ] GET /download starts in < 500ms

### Resource Usage
- [ ] App container: < 500MB RAM idle
- [ ] Total memory: < 4GB (with Selenium Grid)
- [ ] CPU usage: < 5% idle

### Scraping Performance
- [ ] Scraping completes in < 10 minutes
- [ ] All 220+ companies are scraped
- [ ] Excel file is > 50KB

---

## Security Verification Checklist

### Before Production
- [ ] No hardcoded passwords in code
- [ ] No API keys in repository
- [ ] Environment variables for secrets
- [ ] HTTPS enforced (Railway provides auto-SSL)
- [ ] Input validation on all endpoints
- [ ] File path validation prevents traversal

### After Deployment
- [ ] HTTPs works (https:// URL)
- [ ] No console errors in browser (F12)
- [ ] No sensitive data in logs
- [ ] CORS headers are appropriate
- [ ] File downloads work securely

---

## Rollback Procedures

### If Deployment Fails

```bash
# 1. Check Railway logs for specific error
# (Go to Railway dashboard > Service > Deploy tab)

# 2. Local rollback to working version
git revert HEAD
git push origin main

# 3. Re-deploy in Railway
# (Usually automatic on git push)

# 4. Verify services are healthy
```

### If Services Won't Start

```bash
# 1. Check individual service logs in Railway
# 2. Verify environment variables are set
# 3. Check service resource limits
# 4. Try restarting service from dashboard
# 5. Redeploy from dashboard (if needed)
```

### Emergency Procedures

**If app is completely broken:**
1. Stop service in Railway dashboard
2. Fix code locally
3. Push to GitHub
4. Railway will auto-redeploy
5. Monitor logs until healthy

**If data is corrupted:**
1. SSH into Railway container (if available)
2. Check `/app/data/` directory
3. Delete corrupted file if necessary
4. Manual trigger will create new file

---

## Post-Deployment Maintenance

### Daily Tasks
- [ ] Monitor service status (no alerts)
- [ ] Check app logs for errors
- [ ] Verify automatic scraping runs

### Weekly Tasks
- [ ] Review error logs
- [ ] Check data quality
- [ ] Monitor resource usage
- [ ] Verify download functionality

### Monthly Tasks
- [ ] Update dependencies (check for security patches)
- [ ] Review performance metrics
- [ ] Test backup/restore procedures
- [ ] Update documentation if needed

### Quarterly Tasks
- [ ] Security audit
- [ ] Performance optimization review
- [ ] Database/data cleanup
- [ ] Update all base images

---

## Troubleshooting Quick Reference

| Issue | Solution |
|-------|----------|
| Services won't start | Check Railway logs, verify env vars |
| Out of memory | Reduce browser sessions, upgrade plan |
| Download fails | Check if scraping completed (/status) |
| Selenium timeout | Check EGX website availability |
| Timer not updating | Clear browser cache, check JS console |
| Files not persisting | Verify volume is mounted |
| Slow performance | Check Railway plan, scale nodes |

---

## Sign-Off

**Deployment Ready:** ✅  
**Date:** _____________  
**Tested By:** _____________  
**Deployed By:** _____________  

---

## Next Deployment

When deploying a new version:

1. Run verification: `python verify_setup.py`
2. Local testing: `docker-compose up -d`
3. Run through checklist above
4. Push to GitHub
5. Monitor Railway deployment
6. Verify public URL works
7. Test all functionality

---

Good luck with your deployment! 🚀
