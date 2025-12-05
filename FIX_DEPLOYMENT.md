# Fix for Deployment Error: ModuleNotFoundError: No module named 'sklearn'

## Problem
The error shows that `scikit-learn` is not being installed on Streamlit Cloud, even though it's in `requirements.txt`.

## Solution

### Step 1: Update and Commit requirements.txt

Make sure your `requirements.txt` file is committed to your GitHub repository:

```bash
git add requirements.txt
git commit -m "Fix: Add scikit-learn to requirements"
git push
```

### Step 2: Verify requirements.txt Content

Your `requirements.txt` should contain:
```
streamlit>=1.28.0
pandas>=1.5.0
scikit-learn>=1.2.0
numpy>=1.24.0
plotly>=5.14.0
```

### Step 3: Redeploy on Streamlit Cloud

1. Go to your Streamlit Cloud dashboard
2. Click on your app
3. Click the "⋮" (three dots) menu → "Redeploy"
4. Or wait for automatic redeploy after pushing to GitHub

## Alternative: Pin Specific Versions

If the issue persists, try pinning specific versions in `requirements.txt`:

```
streamlit==1.52.1
pandas==2.2.3
scikit-learn==1.5.2
numpy==2.1.3
plotly==5.24.1
```

## Verify Installation

After redeploying, check the logs to ensure scikit-learn is installed. You should see it in the "Installed packages" list.

## If Still Not Working

1. Check Streamlit Cloud logs for any error messages during package installation
2. Try removing version constraints temporarily:
   ```
   streamlit
   pandas
   scikit-learn
   numpy
   plotly
   ```
3. Make sure `requirements.txt` is in the root directory of your repository
4. Ensure there are no hidden characters or encoding issues in `requirements.txt`

