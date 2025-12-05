# Duplicate Finder with Interpretability

A machine learning application for detecting duplicate items in datasets using TF-IDF vectorization and cosine similarity, with comprehensive interpretability features.

## Features

### 🔍 Core Functionality
- **TF-IDF Vectorization**: Converts text into numerical vectors
- **Cosine Similarity**: Measures similarity between items (0 = different, 1 = identical)
- **Threshold-based Detection**: Configurable similarity threshold
- **Batch Processing**: Analyze entire CSV datasets

### 🔬 Interpretability Features
- **Similarity Distribution**: Histogram of all similarity scores
- **Feature Importance**: Shows which words/features contribute most to similarity
- **Top Matches Analysis**: Detailed breakdown of top duplicate matches
- **Word Comparison**: Word-level analysis showing common and unique words

## Installation

```bash
pip install streamlit pandas scikit-learn numpy plotly
```

## Usage

### Option 1: Streamlit App (Interactive UI) ⭐ Recommended

Run the interactive web application:

```bash
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

**Features:**
- Upload CSV files via drag-and-drop
- Interactive visualizations
- Real-time interpretability analysis
- Configurable parameters via sidebar

### Option 2: CLI Application

Run from command line:

```bash
python cli_app.py <csv_file> <column_name> <item_to_check> [options]
```

**Arguments:**
- `csv_file`: Path to your CSV file
- `column_name`: Name of the text column to analyze
- `item_to_check`: Item description to check for duplicates

**Options:**
- `--threshold`: Similarity threshold (default: 0.7)
- `--max-features`: Max TF-IDF features (default: 5000)

**Example:**
```bash
python cli_app.py products.csv product_name "iPhone 13 Pro" --threshold 0.8
```

### Option 3: Jupyter Notebook

Open `notebook.ipynb` and run the cells:
1. Install dependencies (Cell 1)
2. Run Streamlit app code (Cell 4)
3. Or use Flask app (Cell 2)

## Input → Output → Interpretability Flow

### 1. Input 📥
- Upload CSV dataset
- Select text column to analyze
- Enter item to check for duplicates
- Configure similarity threshold

### 2. Output 📤
- Duplicate detection results
- Similarity scores for each match
- Sorted by relevance

### 3. Interpretability 🔬
- **Similarity Distribution**: Histogram showing distribution of all similarity scores
- **Feature Importance**: Top 10 words/features that contribute to similarity
- **Top Matches Analysis**: Side-by-side comparison of input vs matched items
- **Word Comparison**: Common words, unique words, and frequency analysis

## How It Works

1. **TF-IDF Vectorization**: 
   - Converts text into numerical vectors
   - Weights words by frequency and rarity
   - Removes common stop words

2. **Cosine Similarity**:
   - Measures angle between vectors
   - Returns value between 0 (different) and 1 (identical)
   - Higher values = more similar

3. **Threshold-based Detection**:
   - Items with similarity ≥ threshold are flagged as duplicates
   - Adjustable threshold for different use cases

4. **Interpretability**:
   - Shows which features (words) contribute most to similarity
   - Visualizes similarity distribution
   - Provides word-level analysis

## Example Output

```
📤 OUTPUT
⚠️  DUPLICATE DETECTED! Found 3 similar item(s)

Match #1:
  Item: iPhone 13 Pro Max 256GB
  Similarity: 0.892 (89.2%)
  
Match #2:
  Item: iPhone 13 Pro 128GB
  Similarity: 0.756 (75.6%)

🔬 INTERPRETABILITY
📊 Feature Importance Analysis
Top 10 Most Important Shared Features:
Feature              Input TF-IDF    Match TF-IDF    Shared        
iphone               0.4521          0.4892          0.2211
pro                  0.3124          0.3456          0.1079
...
```

## Requirements

- Python 3.7+
- pandas
- scikit-learn
- numpy
- streamlit (for web app)
- plotly (for visualizations)

## Deployment to Streamlit Community Cloud

### Prerequisites
1. GitHub account
2. Streamlit Community Cloud account (sign up at [share.streamlit.io](https://share.streamlit.io))

### Steps to Deploy

1. **Create a GitHub Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Duplicate Finder app"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Connect your GitHub account
   - Select your repository
   - Set the main file path to: `streamlit_app.py`
   - Click "Deploy"

3. **Required Files** (already included)
   - ✅ `streamlit_app.py` - Main application file
   - ✅ `requirements.txt` - Python dependencies
   - ✅ `.gitignore` - Git ignore file

### Deployment Configuration

The app is ready for deployment with:
- **Main file**: `streamlit_app.py`
- **Python version**: 3.7+ (auto-detected by Streamlit Cloud)
- **Dependencies**: Listed in `requirements.txt`

## File Structure

```
.
├── streamlit_app.py        # Main Streamlit application (for deployment)
├── cli_app.py              # Command-line interface
├── notebook.ipynb          # Jupyter notebook with all code
├── requirements.txt        # Python dependencies (for deployment)
├── .gitignore             # Git ignore file
└── README.md              # This file
```

## License

MIT License

