# 🚀 Quick Deploy Steps (Copy-Paste Ready)

## Step 1: Initialize Git & Push to GitHub

```powershell
cd "e:\scraping stocks"

# Initialize git
git init

# Configure git (first time only)
git config user.email "your-email@gmail.com"
git config user.name "Your Name"

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Stock scraper app"

# Add remote (REPLACE YOUR_USERNAME and stock-scraper with your values)
git remote add origin https://github.com/YOUR_USERNAME/stock-scraper.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## Step 2: Go to Railway.app

1. Visit **https://railway.app**
2. Click **"Start a New Project"**
3. Click **"Deploy from GitHub repo"**
4. Select your `stock-scraper` repository
5. Click **"Deploy"**
6. Wait 2-5 minutes
7. Get your public URL (looks like: `https://stock-scraper-production.railway.app`)

---

## Step 3: Test Your Deployment

Open your browser and go to: `https://stock-scraper-production.railway.app`

You should see:
- Dashboard with stock data
- Download button
- Next update time

---

## Step 4: Updates (After First Deploy)

Every time you want to update:

```powershell
cd "e:\scraping stocks"

# Make your changes

# Commit and push
git add .
git commit -m "Description of changes"
git push origin main
```

Railway will auto-redeploy! ✨

---

## ✅ Files Already Created for Deployment

- ✅ `Procfile` - Tells Railway how to run your app
- ✅ `runtime.txt` - Specifies Python version
- ✅ `railway.json` - Railway configuration
- ✅ `requirements.txt` - Updated with gunicorn & webdriver-manager
- ✅ `main.py` - Updated to use webdriver-manager
- ✅ `.gitignore` - Excludes unnecessary files
- ✅ `RAILWAY_DEPLOYMENT.md` - Full documentation

---

## 🎯 Deployment Checklist

Before you push to GitHub, make sure:

- [ ] All files are in `e:\scraping stocks` folder
- [ ] `Procfile` exists (no .txt extension)
- [ ] `runtime.txt` exists
- [ ] `requirements.txt` has gunicorn and webdriver-manager
- [ ] `main.py` imports webdriver-manager
- [ ] `.gitignore` exists

---

## ⚠️ Important Notes

### Files That Get Deleted on Railway
- Excel files in `excel_files/` folder (auto-cleaned)
- Any files in `/tmp` directory

### Files That Persist
- Configuration files
- Source code

### For Permanent Storage
You'd need to use S3 or Azure Blob Storage (optional, beyond this guide)

---

## 🎉 You're Ready!

Follow Step 1 above to push your project to GitHub, then Step 2 to deploy on Railway.

Your app will be live on the internet in less than 5 minutes! 🚀
