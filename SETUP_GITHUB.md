# GitHub Setup for kabeutal

## Quick Setup Commands

Replace `YOUR_REPO_NAME` with your desired repository name (e.g., `duplicate-finder-app`)

### Step 1: Initialize Git Repository

```bash
git init
git add .
git commit -m "Initial commit: Duplicate Finder with Interpretability"
git branch -M main
```

### Step 2: Create Repository on GitHub

1. Go to: https://github.com/new
2. Repository name: `duplicate-finder-app` (or your preferred name)
3. Description: "Duplicate Finder with Interpretability using TF-IDF and Cosine Similarity"
4. Set to **Public** (required for free Streamlit Cloud)
5. **DO NOT** check "Initialize with README"
6. Click "Create repository"

### Step 3: Connect and Push

After creating the repository on GitHub, run:

```bash
git remote add origin https://github.com/kabeutal/YOUR_REPO_NAME.git
git push -u origin main
```

**Example** (if repo name is `duplicate-finder-app`):
```bash
git remote add origin https://github.com/kabeutal/duplicate-finder-app.git
git push -u origin main
```

### Step 4: Deploy to Streamlit Cloud

1. Go to: https://share.streamlit.io
2. Sign in with GitHub (use your kabeutal account)
3. Click "New app"
4. Repository: Select `kabeutal/YOUR_REPO_NAME`
5. Branch: `main`
6. Main file path: `streamlit_app.py`
7. Click "Deploy"

## Your Repository URL

Once created, your repository will be at:
```
https://github.com/kabeutal/YOUR_REPO_NAME
```

## Your Streamlit App URL

After deployment, your app will be at:
```
https://YOUR-APP-NAME.streamlit.app
```

## Files Ready for Deployment

✅ `streamlit_app.py` - Main application  
✅ `requirements.txt` - Dependencies  
✅ `.gitignore` - Git configuration  
✅ `README.md` - Documentation

## Authentication Note

When pushing to GitHub, you may need to:
- Use a **Personal Access Token** (recommended)
- Or use GitHub Desktop for easier authentication

To create a Personal Access Token:
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token
3. Select scopes: `repo` (full control)
4. Copy token and use it as password when pushing

