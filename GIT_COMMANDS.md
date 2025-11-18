# 📚 Git Commands Cheat Sheet for Deployment

## First Time Setup (One Time Only)

### 1. Initialize Git in Your Folder

```powershell
cd "e:\scraping stocks"
git init
```

### 2. Configure Git (Your Name & Email)

```powershell
git config user.email "your-email@gmail.com"
git config user.name "Your Name"
```

*Only needed once on your computer*

### 3. Add All Files

```powershell
git add .
```

This stages all files for commit.

### 4. Create Your First Commit

```powershell
git commit -m "Initial commit: Stock scraper app"
```

### 5. Connect to GitHub

First, create a repository on github.com, then:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/stock-scraper.git
```

Replace `YOUR_USERNAME` with your GitHub username.

### 6. Set Default Branch to "main"

```powershell
git branch -M main
```

### 7. Push to GitHub

```powershell
git push -u origin main
```

This uploads everything to GitHub!

---

## After First Deploy (For Updates)

Whenever you change files and want to update:

### 1. Check What Changed

```powershell
git status
```

Shows modified files.

### 2. Stage Changes

```powershell
git add .
```

Or add specific files:

```powershell
git add main.py requirements.txt
```

### 3. Commit Changes

```powershell
git commit -m "Description of what you changed"
```

Examples:
```
git commit -m "Fixed scraping bug"
git commit -m "Added new feature for export"
git commit -m "Updated dependencies"
```

### 4. Push to GitHub (Railway Auto-Deploys!)

```powershell
git push origin main
```

---

## Common Git Commands

### See Your Commit History

```powershell
git log
```

Shows all commits with timestamps and messages.

### See Which Files Changed

```powershell
git diff
```

Shows exact changes (before commit).

### Undo Last Commit (Before Push)

```powershell
git reset --soft HEAD~1
```

Undoes commit but keeps changes staged.

### See Remote Repositories

```powershell
git remote -v
```

Shows connected repositories (should show your GitHub repo).

### See Current Branch

```powershell
git branch
```

Shows which branch you're on.

### Create New Branch (Optional)

```powershell
git branch feature-name
git checkout feature-name
```

Or shorter:
```powershell
git checkout -b feature-name
```

### Switch Back to Main Branch

```powershell
git checkout main
```

---

## Full Workflow Example

Let's say you want to fix a bug and deploy it:

```powershell
# 1. Make changes to your files
# (Edit main.py, requirements.txt, etc in VS Code)

# 2. Check what changed
git status

# 3. Stage changes
git add .

# 4. Commit
git commit -m "Fixed connection timeout bug"

# 5. Push to GitHub
git push origin main

# ✨ Railway auto-deploys! (2-5 minutes)
```

---

## If You Made a Mistake

### Oops! Committed Wrong File

```powershell
# Undo the commit (keeps changes)
git reset --soft HEAD~1

# Or undo and discard changes
git reset --hard HEAD~1
```

### Oops! Pushed Wrong Changes

Contact Railway support or:
1. Fix the files locally
2. Commit the fix
3. Push again
4. Railway redeploys with fix

### Need to See What's in Staging

```powershell
git diff --cached
```

---

## Important Notes

- **Git is local** - Lives on your computer in `.git` folder
- **GitHub is remote** - Your code backed up in the cloud
- **Railway watches GitHub** - Redeploys automatically when you push
- **Always commit before push** - Can't push without committing

---

## Command Quick Reference

```powershell
# Setup (first time)
git init
git config user.email "your-email@gmail.com"
git config user.name "Your Name"
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/stock-scraper.git
git branch -M main
git push -u origin main

# Updates (every time after)
git add .
git commit -m "Description"
git push origin main
```

---

## 🎯 The Only Commands You Really Need

### First Deploy:
```powershell
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/stock-scraper.git
git branch -M main
git push -u origin main
```

### Every Update After:
```powershell
git add .
git commit -m "Description"
git push origin main
```

---

**That's it! Two sets of commands and you're good.** 🚀
