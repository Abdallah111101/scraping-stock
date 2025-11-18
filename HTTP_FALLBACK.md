# 🔄 Fallback HTTP Scraper Method

## Problem Solved

The EGX website is **blocking headless Chrome** (Selenium) connections. This is a common anti-bot measure.

## Solution: Dual Method Approach

The application now uses a **hybrid approach**:

```
Attempt 1: Try Selenium/Chrome (faster, more reliable)
   ↓ If blocked or fails
Attempt 2: Fallback to HTTP requests (mimics real browser)
   ↓ If still fails
Attempt 3: Retry with exponential backoff
```

---

## How It Works

### Method 1: Selenium/Chrome (Primary)
- Pros: JavaScript rendering, full page interaction
- Cons: Heavy resource, detected by bot protection
- Status: **May be blocked by EGX**

### Method 2: HTTP Requests (Fallback)
- Pros: Lightweight, faster, less likely to be detected
- Cons: No JavaScript rendering
- Status: **More likely to work**

---

## Files Added

### `http_scraper.py`
- Direct HTTP requests implementation
- Mimics real browser with proper headers
- Automatic retry logic
- BeautifulSoup HTML parsing

### `test_http.py`
- Test connectivity to EGX
- Test HTTP scraper independently
- Verify before running main app

---

## Quick Start

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- `beautifulsoup4` - HTML parsing
- `requests` - HTTP library
- All other dependencies

### Step 2: Test HTTP Connection
```bash
python test_http.py
```

This tests:
- Internet connectivity
- EGX website reachability
- HTTP scraper functionality

### Step 3: Run Main Application
```bash
python main.py
```

The app will now:
1. Try Selenium first (primary method)
2. If blocked, automatically fallback to HTTP (secondary method)
3. Retry up to 3 times with backoff
4. Schedule next update in 8 hours

---

## What You'll See in Console

### Success Scenario:
```
Starting scrape at 2025-11-18 20:15:30.123456
Method: Selenium/Chrome
✓ Page loaded successfully
✓ Data saved to egx_stocks_20251118_201530.xlsx
✓ Successfully scraped 165 stocks
```

### Fallback Scenario:
```
Starting scrape at 2025-11-18 20:15:30.123456
Method: Selenium/Chrome
⚠ Selenium method failed: net::ERR_CONNECTION_RESET...
Falling back to HTTP requests method...
Fetching stock data from EGX...
Attempt 1/3
✓ Connection successful (Status: 200)
✓ Successfully scraped 165 stocks
✓ Data saved to egx_stocks_20251118_201530.xlsx
```

### Retry Scenario:
```
Scraping attempt 1 failed: net::ERR_CONNECTION_RESET...
Retrying in 10 seconds...

Scraping attempt 2 failed: Connection timeout...
Retrying in 20 seconds...

Scraping attempt 3 failed...
All 3 attempts failed. Retrying at next scheduled time.
```

---

## Testing Each Method Independently

### Test HTTP Scraper Only
```bash
python http_scraper.py
```

### Test Main App
```bash
python main.py
```

### Test Connectivity
```bash
python test_http.py
```

---

## Error Handling

### "Connection Reset"
- EGX might be temporarily down
- Firewall/antivirus blocking
- ISP rate limiting

**Solution**: App retries automatically

### "Timeout"
- Website is slow
- Network latency

**Solution**: App waits and retries

### "No data found"
- Website structure changed
- XPaths became invalid

**Solution**: HTTP parser is more flexible

---

## Browser Headers (HTTP Method)

The HTTP scraper mimics a real browser:

```python
{
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...',
    'Accept': 'text/html,application/xhtml+xml...',
    'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}
```

This makes the request appear to be from a real browser, not a bot.

---

## Performance Comparison

| Method | Speed | Reliability | Resource Usage | Bot Detection |
|--------|-------|-------------|-----------------|---|
| Selenium | Medium | Medium | High | High |
| HTTP | Fast | High | Low | Low |
| Fallback | Medium | High | Medium | Low |

---

## Troubleshooting HTTP Scraper

### "No module named 'beautifulsoup4'"
```bash
pip install beautifulsoup4
```

### "No module named 'requests'"
```bash
pip install requests
```

### "Connection refused"
- Check internet connection
- Check if EGX is down
- Try: `ping www.egx.com.eg`

### "No data returned"
- Website structure might have changed
- HTML parsing logic might need updating
- Edit `http_scraper.py` to adjust parsing

---

## Manual Testing HTTP Scraper

```python
from http_scraper import EGXScraper

scraper = EGXScraper()
stocks = scraper.get_stock_data()
print(f"Scraped {len(stocks)} stocks")
```

---

## Advantages of Dual Method

✅ **Reliability**: Multiple fallback options  
✅ **Speed**: HTTP fallback is faster  
✅ **Flexibility**: Can handle website changes  
✅ **Resilience**: Automatic retry and fallback  
✅ **Less Detection**: HTTP appears more like real browser  

---

## Dashboard Still Works

Both methods produce the same Excel file:
- Same columns
- Same data format
- Same filename format
- Same auto-update schedule

The dashboard doesn't care which method was used!

---

## Next Steps if Still Not Working

1. **Run diagnostic**: `python diagnostic.py`
2. **Test HTTP**: `python test_http.py`
3. **Check website**: Visit https://www.egx.com.eg manually
4. **Check network**: `ping www.egx.com.eg`
5. **Check firewall**: Allow Python and Chrome through
6. **Wait and retry**: Website might be temporarily down

---

## Advanced Configuration

### Increase Retry Attempts
Edit `perform_scrape()` in `main.py`:
```python
max_retries = 5  # Change from 3 to 5
```

### Increase Wait Between Retries
Edit `perform_scrape()` in `main.py`:
```python
wait_time = 15 * retry_count  # Change from 10 to 15
```

### Disable Selenium, Use HTTP Only
Edit `perform_scrape()` in `main.py`:
```python
# Try HTTP first instead:
if HTTP_SCRAPER_AVAILABLE:
    filepath, filename = scrape_with_http_requests()
else:
    filepath, filename = scrape_egx_stocks()
```

---

## Summary

Your application now has **two scraping methods** with **automatic fallback**:

1. **Primary**: Selenium Chrome (detailed page interaction)
2. **Secondary**: HTTP Requests (lightweight, fast)

If one fails, it automatically tries the other!

---

**Status**: ✅ Ready for dual-method scraping
