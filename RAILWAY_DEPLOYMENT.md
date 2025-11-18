# 🚀 Deploy to Railway - Complete Guide

Railway is a platform to deploy your FastAPI app online. Here's how:

---

## 📋 Prerequisites

1. **GitHub account** (free at github.com)
2. **Railway account** (free at railway.app)
3. Your project on GitHub

---

## ✅ Step-by-Step Deployment

### Step 1: Create GitHub Repository

1. Go to **github.com**
2. Click **"New repository"** (top right)
3. Name: `stock-scraper` (or any name)
4. Description: `EGX Stock Scraper with FastAPI`
5. Click **"Create repository"**
6. Copy the repository URL (looks like: `https://github.com/YOUR_USERNAME/stock-scraper.git`)

---

### Step 2: Upload Your Project to GitHub

Open PowerShell in your project folder (`e:\scraping stocks`) and run:

```powershell
# Initialize git
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Stock scraper app"

# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/stock-scraper.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Replace** `YOUR_USERNAME` with your actual GitHub username.

---

### Step 3: Prepare Railway Configuration Files

We need to add 2 files to your project:

#### File 1: `Procfile`
This tells Railway how to run your app.

Create a file named `Procfile` (no extension) in your project root with:

```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

#### File 2: `runtime.txt`
This specifies Python version.

Create a file named `runtime.txt` with:

```
python-3.11.0
```

---

### Step 4: Update requirements.txt for Railway

Add `gunicorn` for production. Update your `requirements.txt` to:

```
fastapi==0.104.1
uvicorn==0.24.0
gunicorn==21.2.0
selenium==4.15.2
pandas==2.1.3
openpyxl==3.10.10
python-dotenv==1.0.0
requests==2.31.0
beautifulsoup4==4.12.2
webdriver-manager==4.0.1
```

Note: Added `gunicorn` and `webdriver-manager`

---

### Step 5: Create Railway Configuration (optional but recommended)

Create `railway.json` in your project root:

```json
{
  "build": {
    "builder": "heroku.buildpacks"
  }
}
```

---

### Step 6: Commit and Push Changes

Back in PowerShell:

```powershell
# Add the new files
git add Procfile runtime.txt requirements.txt railway.json

# Commit
git commit -m "Add deployment configuration for Railway"

# Push
git push origin main
```

---

### Step 7: Deploy on Railway

1. Go to **railway.app**
2. Click **"Login"** (top right)
3. Login with GitHub or create account
4. After login, click **"New Project"**
5. Click **"Deploy from GitHub repo"**
6. Select your `stock-scraper` repository
7. Railway will auto-detect FastAPI and deploy!
8. Wait 2-5 minutes for deployment to complete
9. You'll get a URL like: `https://stock-scraper-production.railway.app`

---

### Step 8: Test Your Deployment

Once deployed:

1. Go to your Railway URL: `https://stock-scraper-production.railway.app`
2. You should see the dashboard
3. Download button should work
4. Scraping should start automatically

---

## 🎯 Important Notes for Railway

### Database for Storing Excel Files

Railway doesn't keep files between restarts. We need to store Excel files elsewhere.

**Options:**

#### Option A: Store on Railway (Simple, Limited)
Files delete after 24 hours (Railway clears disk space)
- Currently works as-is
- Good for testing
- Not recommended for production

#### Option B: Store on AWS S3 (Recommended for Production)
Permanent storage, costs ~$1/month

#### Option C: Store on Azure Blob Storage
Similar to S3, permanent storage

---

## 🔧 Issues You Might Face

### Issue 1: Port Error
**Error**: `Address already in use`

**Fix**: Railway automatically handles ports. The app uses `$PORT` environment variable. Already configured in `Procfile`.

---

### Issue 2: Selenium/Chrome Driver Not Found
**Error**: `ChromeDriver not found`

**Fix**: Already added `webdriver-manager==4.0.1` to handle this

**In your code**, update main.py to use webdriver-manager:

```python
# OLD:
# driver = webdriver.Chrome()

# NEW:
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)
```

---

### Issue 3: Excel Files Not Saving
**Error**: Files not found on next visit

**Fix**: This is expected on Railway. Use storage option (S3/Azure) or redesign to generate Excel on-demand.

---

## 📊 Current Status on Railway

Your app WILL work on Railway but with limitations:

✅ **Works**:
- Scraping stocks
- Dashboard display
- Excel generation
- Download Excel

⚠️ **Limited**:
- Excel files stored in `/tmp` (delete after restart)
- Background scheduler runs but files don't persist
- Only 1 instance runs

---

## 🚀 Full Deployment Checklist

- [ ] GitHub account created
- [ ] Repository created
- [ ] Project pushed to GitHub
- [ ] `Procfile` created
- [ ] `runtime.txt` created
- [ ] `requirements.txt` updated
- [ ] `railway.json` created
- [ ] Changes pushed to GitHub
- [ ] Railway account created
- [ ] Project connected to Railway
- [ ] Deployment successful
- [ ] App running and accessible
- [ ] Dashboard loads
- [ ] Download works

---

## 📞 Quick Commands Reference

### First Time Setup
```powershell
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/stock-scraper.git
git branch -M main
git push -u origin main
```

### Updates After First Deploy
```powershell
git add .
git commit -m "Description of changes"
git push origin main
```

Railway auto-redeploys after you push!

---

## 🎉 After Successful Deployment

1. **Share Your App**: Give friends/colleagues your Railway URL
2. **Monitor**: Check Railway dashboard for logs
3. **Update**: Any push to GitHub auto-deploys
4. **Scale**: Railway handles traffic automatically

---

## 💾 Optional: Add Persistent Storage (S3)

If files need to persist, add to `requirements.txt`:

```
boto3==1.28.85
```

Then update code to upload Excel to S3 bucket instead of local storage.

---

## 🆘 Still Not Working?

1. Check Railway logs:
   - Go to railway.app dashboard
   - Select your project
   - Click "Logs" tab
   - See error messages

2. Check common issues:
   - Is GitHub repo public?
   - Is `Procfile` named correctly?
   - Is port configured? (Should use `$PORT`)

3. Ask Railway support or GitHub issues

---

**Ready to deploy?** Follow steps 1-7 above! 🚀
