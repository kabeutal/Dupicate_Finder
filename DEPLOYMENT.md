# Deployment Guide for Streamlit Community Cloud

This guide will help you deploy the Duplicate Finder app to Streamlit Community Cloud.

## Prerequisites

1. **GitHub Account**: You need a GitHub account to host your code
2. **Streamlit Account**: Sign up at [share.streamlit.io](https://share.streamlit.io) (free)

## Step-by-Step Deployment

### Step 1: Initialize Git Repository

Open your terminal/command prompt in the project directory and run:

```bash
# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Duplicate Finder with Interpretability"
```

### Step 2: Create GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click the "+" icon in the top right → "New repository"
3. Name your repository (e.g., `duplicate-finder-app`)
4. **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click "Create repository"

### Step 3: Connect Local Repository to GitHub

Copy the commands from GitHub (they'll look like this, but with your username/repo):

```bash
# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

**Note**: You may need to authenticate. GitHub may ask for:
- Personal Access Token (recommended)
- Or username/password

### Step 4: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app" button
4. Fill in the deployment form:
   - **Repository**: Select your repository from the dropdown
   - **Branch**: `main` (or `master` if that's your default)
   - **Main file path**: `streamlit_app.py`
   - **App URL**: Choose a custom subdomain (optional)
5. Click "Deploy"

### Step 5: Wait for Deployment

- Streamlit Cloud will automatically:
  - Install dependencies from `requirements.txt`
  - Run your app
  - Provide you with a public URL

The deployment usually takes 1-2 minutes.

## Important Files for Deployment

✅ **Required Files** (already created):
- `streamlit_app.py` - Your main application
- `requirements.txt` - Python dependencies
- `.gitignore` - Excludes unnecessary files

## Troubleshooting

### Common Issues

1. **"Module not found" error**
   - Check that all dependencies are in `requirements.txt`
   - Make sure versions are compatible

2. **"File not found" error**
   - Ensure `streamlit_app.py` is in the root directory
   - Check the main file path in Streamlit Cloud settings

3. **Deployment fails**
   - Check the logs in Streamlit Cloud dashboard
   - Ensure Python version is 3.7+ (auto-detected)
   - Verify all imports are available in requirements.txt

### Updating Your App

After making changes:

```bash
git add .
git commit -m "Update app"
git push
```

Streamlit Cloud will automatically redeploy your app!

## Your App URL

Once deployed, your app will be available at:
```
https://YOUR-APP-NAME.streamlit.app
```

You can share this URL with anyone!

## Security Notes

- Your code is public if the GitHub repo is public
- Uploaded CSV files are processed in memory (not stored)
- No data is persisted between sessions

## Support

If you encounter issues:
1. Check Streamlit Cloud logs
2. Verify all files are committed to GitHub
3. Ensure `requirements.txt` is correct
4. Check [Streamlit Community Cloud docs](https://docs.streamlit.io/streamlit-community-cloud)

