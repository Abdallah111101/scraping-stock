# 🚀 IMMEDIATE ACTION: Run These Commands

## Step 1: Update Dependencies (1 minute)

```powershell
pip install -r requirements.txt
```

**What it does**: Installs `beautifulsoup4` and `requests` for HTTP fallback

**Expected output**:
```
Successfully installed beautifulsoup4-4.12.2 requests-2.31.0
```

---

## Step 2: Test Connectivity (2 minutes) - OPTIONAL but RECOMMENDED

```powershell
python test_http.py
```

**What it does**: Tests if HTTP scraper can connect to EGX

**Expected output**:
```
Testing HTTP Connection to EGX
✓ Google reachable (Status: 200)
✓ EGX reachable (Status: 200)
✓ EGX prices page reachable (Status: 200)
✓ Found table data in response
Testing HTTP scraper...
✓ SUCCESS! Scraped 165 stocks
✓ Saved to: egx_stocks_20251118_203045.xlsx
```

**If it fails**: 
- Check internet: `ping google.com`
- Check EGX: Visit https://www.egx.com.eg manually
- Run diagnostic: `python diagnostic.py`

---

## Step 3: Run Application (5 minutes)

```powershell
python main.py
```

**What it does**: Starts FastAPI server with both scraping methods

**Expected output**:
```
Starting Stock Scraper Service...
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000

Starting scrape at 2025-11-18 20:15:30.123456
Method: Selenium/Chrome
✓ Page loaded successfully
✓ Successfully scraped 165 stocks
✓ Data saved to egx_stocks_20251118_201530.xlsx
Next update scheduled for: 2025-11-19 04:15:30.123456
```

**Or if Selenium fails** (also OK!):
```
Starting scrape at 2025-11-18 20:15:30.123456
Method: Selenium/Chrome
⚠ Selenium method failed: net::ERR_CONNECTION_RESET
Falling back to HTTP requests method...
Fetching stock data from EGX...
✓ Connection successful (Status: 200)
✓ Successfully scraped 165 stocks
✓ Data saved to egx_stocks_20251118_201530.xlsx
```

---

## Step 4: Access Dashboard (30 seconds)

Open your browser to:
```
http://localhost:8000
```

**You should see**:
- Countdown timer to next update
- Last update time
- Next update time
- File status badge (green = ready)
- Download button
- Refresh button

---

## Step 5: Download Excel File (10 seconds)

1. Click **"⬇️ تحميل ملف Excel"** button
2. File downloads to your Downloads folder
3. Open with Excel/LibreOffice
4. View scraped stock data

---

## 🎯 Complete Workflow in 4 Commands

```powershell
# 1. Install dependencies
pip install -r requirements.txt

# 2. Test connectivity (optional)
python test_http.py

# 3. Run application (keep running)
python main.py

# 4. In browser, visit:
# http://localhost:8000
```

---

## ⏱️ Timeline

| Step | Command | Duration | Status |
|------|---------|----------|--------|
| 1 | Install | 1-2 min | ⏳ Do this first |
| 2 | Test | 1-2 min | ✅ Optional |
| 3 | Run | Immediate | ⏳ Keep running |
| 4 | Scrape | 10-40 sec | ⏳ Happens auto |
| 5 | Dashboard | 1 sec | ✅ Browse to it |
| 6 | Download | 10 sec | ✅ Click button |

---

## 📊 What to Expect

### Initial Startup
1. App starts
2. Immediate scrape begins
3. Takes 10-40 seconds (depends on method)
4. Excel file created
5. Dashboard ready

### Continuous Operation
- Updates every 8 hours automatically
- Dashboard shows countdown
- One-click Excel download
- No manual intervention needed

---

## 🆘 If Something Goes Wrong

### Issue: "Module not found"
```powershell
pip install -r requirements.txt
```

### Issue: "Port already in use"
```powershell
# Find process
netstat -ano | findstr :8000

# Kill it (replace XXXX with PID)
taskkill /PID XXXX /F

# Then restart
python main.py
```

### Issue: "Connection refused"
```powershell
# Check internet
ping google.com

# Check EGX website
ping www.egx.com.eg
```

### Issue: "No data returned"
```powershell
# Test HTTP scraper
python test_http.py

# Run diagnostic
python diagnostic.py
```

---

## ✅ Success Checklist

As you follow these steps:

- [ ] Ran `pip install -r requirements.txt`
- [ ] Ran `python test_http.py` (if you chose to test)
- [ ] Ran `python main.py` and saw "Uvicorn running"
- [ ] Opened http://localhost:8000 in browser
- [ ] See dashboard with countdown timer
- [ ] Clicked download button (or saw it ready)
- [ ] Excel file downloaded successfully

---

## 🎉 You're Done!

Your application is now running with:
- ✅ Dual scraping methods
- ✅ Automatic fallback
- ✅ Beautiful dashboard
- ✅ Excel export
- ✅ 8-hour auto-updates

---

## 💡 Tips

1. **Keep the app running**: `python main.py` should stay in terminal
2. **Multiple browsers**: You can access dashboard from multiple browsers
3. **Multiple downloads**: Download as many times as you want
4. **Check console**: All important info is logged to console
5. **Ctrl+C to stop**: Press Ctrl+C to stop the app

---

## 📚 Additional Commands

```powershell
# Test HTTP scraper directly
python http_scraper.py

# Run diagnostics
python diagnostic.py

# Kill process on port 8000 (if stuck)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Change port in main.py if needed
# Edit last line: uvicorn.run(app, host="0.0.0.0", port=8080)
```

---

## 🔗 Important Links

- Dashboard: http://localhost:8000
- API Status: http://localhost:8000/api/status
- EGX Website: https://www.egx.com.eg
- Excel Files: `./excel_files/` folder

---

**Ready?** Start with: `pip install -r requirements.txt`

Then: `python main.py`

Then: Open http://localhost:8000

✅ That's it!
