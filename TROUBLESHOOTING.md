# 🔧 Troubleshooting Guide

## Connection Errors

### Error: `net::ERR_CONNECTION_RESET`

**Cause**: Network connectivity issue with the EGX website

**Solutions**:

1. **Check Internet Connection**
   ```bash
   ping google.com
   ping www.egx.com.eg
   ```

2. **Run Diagnostic Tool**
   ```bash
   python diagnostic.py
   ```

3. **Check Firewall/Proxy**
   - Temporarily disable antivirus/firewall
   - Check if behind corporate proxy
   - Try with VPN if available

4. **Wait and Retry**
   - The website might be temporarily down
   - Wait 5-10 minutes and try again
   - Check EGX website status: https://www.egx.com.eg

5. **Update ChromeDriver**
   - Download latest from: https://chromedriver.chromium.org/
   - Ensure it matches your Chrome version exactly
   ```bash
   # Check Chrome version
   # Windows: Check Settings > About Chrome
   # macOS: Chrome > About Google Chrome
   # Linux: google-chrome --version
   ```

6. **Try Alternative Port/Network**
   ```bash
   # Edit main.py last line:
   uvicorn.run(app, host="127.0.0.1", port=8000)
   ```

---

## ChromeDriver Issues

### Error: `chromedriver not found`

1. **Download ChromeDriver**
   - Go to: https://chromedriver.chromium.org/
   - Select your Chrome version
   - Download for your OS

2. **Extract to Project Folder**
   - Extract the zip file
   - Place `chromedriver.exe` (Windows) or `chromedriver` (Mac/Linux) in project root

3. **Add to System PATH** (Alternative)
   - Windows: 
     1. Press Win+X, search "Environment Variables"
     2. Add chromedriver folder to PATH
     3. Restart terminal
   - Mac/Linux:
     ```bash
     export PATH=$PATH:/path/to/chromedriver/folder
     ```

---

## Port Already in Use

### Error: `Address already in use: ('0.0.0.0', 8000)`

**Solution 1: Kill existing process**

Windows (PowerShell):
```powershell
netstat -ano | findstr :8000
# Find PID, then:
taskkill /PID <PID> /F
```

Mac/Linux:
```bash
lsof -i :8000
# Find PID, then:
kill -9 <PID>
```

**Solution 2: Use different port**

Edit `main.py` last line:
```python
uvicorn.run(app, host="0.0.0.0", port=8080)  # Change 8000 to 8080
```

Then access: `http://localhost:8080`

---

## Virtual Environment Issues

### Error: `No module named 'fastapi'`

1. **Activate Virtual Environment**

   Windows:
   ```bash
   venv\Scripts\activate
   ```

   Mac/Linux:
   ```bash
   source venv/bin/activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## Browser/Selenium Issues

### Error: `Session info: chrome=... not available`

**Solution**: Update Selenium and ChromeDriver

```bash
pip install --upgrade selenium
# Download latest ChromeDriver from https://chromedriver.chromium.org/
```

### Chrome crashes during scraping

1. **Disable GPU**
   - Already included in main.py

2. **Increase Memory**
   - Close other applications
   - Restart the scraper

3. **Use lighter Chrome options**
   - Edit `scrape_egx_stocks()` in main.py
   - Add: `options.add_argument('--disable-extensions')`

---

## File Download Issues

### Error: `File not found when downloading`

1. **Initial Scrape Not Complete**
   - Wait for first scrape to finish
   - Check console for "Data saved to..." message

2. **Check Excel Files Folder**
   ```bash
   # Windows
   dir excel_files
   
   # Mac/Linux
   ls -la excel_files
   ```

3. **Permissions Issue**
   - Ensure write permissions to project folder
   - Run diagnostic: `python diagnostic.py`

---

## Memory Issues

### Application running slow or crashes

1. **Close Browser Windows**
   - ChromeDriver launches real Chrome instances
   - Can consume significant memory

2. **Reduce Update Frequency**
   - Edit main.py:
   ```python
   UPDATE_INTERVAL = 24 * 60 * 60  # Change from 8 hours to 24 hours
   ```

3. **Monitor System Resources**
   - Windows Task Manager
   - Mac Activity Monitor
   - Linux: `top` or `htop`

---

## Website Structure Changed

### Error: `XPath not found` or very few records scraped

1. **EGX Website Updated**
   - Website layout might have changed
   - XPaths need updating

2. **Solution**:
   - Use original file: `scrapying_alternatoive.py`
   - Manually inspect website with DevTools
   - Update XPath selectors

---

## Server Won't Start

### Verify Setup

1. **Run Diagnostic**
   ```bash
   python diagnostic.py
   ```

2. **Check Requirements**
   ```bash
   pip show fastapi
   pip show uvicorn
   ```

3. **Install Missing**
   ```bash
   pip install -r requirements.txt
   ```

4. **Check Python Version**
   ```bash
   python --version
   # Must be 3.8 or higher
   ```

---

## Dashboard Not Loading

### Can't access http://localhost:8000

1. **Check if server is running**
   - Look for "Uvicorn running on" in console

2. **Try different address**
   - `http://127.0.0.1:8000` (instead of 0.0.0.0)

3. **Check firewall**
   - Windows: Allow Python through firewall
   - Mac: System Preferences > Security & Privacy

4. **Different port**
   - Edit main.py to use port 8080, 9000, etc.

---

## Quick Fixes Checklist

- [ ] Run `python diagnostic.py`
- [ ] Check internet connection
- [ ] Update ChromeDriver
- [ ] Verify Chrome installed
- [ ] Activate virtual environment
- [ ] Install requirements: `pip install -r requirements.txt`
- [ ] Check firewall/antivirus
- [ ] Try different port
- [ ] Restart application
- [ ] Restart computer

---

## Still Having Issues?

1. **Check Application Logs**
   - Copy full error message from console
   - Search error online

2. **Verify Website is Up**
   - Visit https://www.egx.com.eg manually
   - Check if website is accessible

3. **Try Network Diagnostics**
   ```bash
   # Test connection
   ping www.egx.com.eg
   
   # Check DNS
   nslookup www.egx.com.eg
   ```

4. **Contact Support**
   - EGX website might be down
   - Check their Twitter/social media
   - Try again later

---

## Network Diagnostic Commands

### Windows (PowerShell)
```powershell
# Check connection
Test-Connection www.egx.com.eg

# Check open ports
netstat -ano

# Check DNS
nslookup www.egx.com.eg

# Trace route
tracert www.egx.com.eg
```

### Mac/Linux
```bash
# Check connection
ping www.egx.com.eg

# Check open ports
netstat -tlnp

# Check DNS
dig www.egx.com.eg

# Trace route
traceroute www.egx.com.eg
```

---

Made with ❤️ for troubleshooting ease
