#!/usr/bin/env python3
"""
CLI version of Duplicate Finder with Interpretability
Usage: python cli_app.py <csv_file> <column_name> <item_to_check> [--threshold THRESHOLD]
"""

import argparse
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
import re
import sys

def extract_words(text):
    """Extract words from text"""
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    return words

def print_separator(char="=", length=80):
    """Print a separator line"""
    print(char * length)

def print_header(text):
    """Print a formatted header"""
    print_separator()
    print(f"  {text}")
    print_separator()

def check_duplicates(csv_file, column_name, item_to_check, threshold=0.7, max_features=5000):
    """
    Check for duplicates in a CSV file
    
    Args:
        csv_file: Path to CSV file
        column_name: Name of the column to analyze
        item_to_check: Item to check for duplicates
        threshold: Similarity threshold (default: 0.7)
        max_features: Max TF-IDF features (default: 5000)
    """
    try:
        # Load dataset
        print(f"📂 Loading dataset from {csv_file}...")
        dataset = pd.read_csv(csv_file)
        print(f"✅ Loaded {len(dataset)} rows")
        
        if column_name not in dataset.columns:
            print(f"❌ Error: Column '{column_name}' not found in dataset")
            print(f"Available columns: {', '.join(dataset.columns)}")
            return
        
        # Prepare text data
        print(f"\n🔧 Preparing text data from column '{column_name}'...")
        text_data = dataset[column_name].fillna('').astype(str).tolist()
        
        # Train TF-IDF model
        print("🚀 Training TF-IDF model...")
        tfidf_vectorizer = TfidfVectorizer(
            max_features=max_features,
            stop_words='english'
        )
        tfidf_matrix = tfidf_vectorizer.fit_transform(text_data)
        print(f"✅ Model trained! Vocabulary size: {len(tfidf_vectorizer.vocabulary_)}")
        
        # Check for duplicates
        print(f"\n🔍 Checking for duplicates of: '{item_to_check}'")
        print(f"   Threshold: {threshold}")
        
        # Vectorize input
        item_vector = tfidf_vectorizer.transform([item_to_check])
        
        # Calculate similarity
        similarities = cosine_similarity(item_vector, tfidf_matrix)[0]
        
        # Find duplicates
        duplicate_indices = np.where(similarities >= threshold)[0]
        
        # OUTPUT SECTION
        print_header("📤 OUTPUT")
        
        if len(duplicate_indices) > 0:
            print(f"⚠️  DUPLICATE DETECTED! Found {len(duplicate_indices)} similar item(s)\n")
            
            # Sort by similarity
            duplicate_data = []
            for idx in duplicate_indices:
                duplicate_data.append({
                    'index': idx,
                    'item': dataset.iloc[idx][column_name],
                    'similarity': similarities[idx]
                })
            duplicate_data.sort(key=lambda x: x['similarity'], reverse=True)
            
            # Display results
            print("Similar Items Found:")
            print_separator("-")
            for i, dup in enumerate(duplicate_data, 1):
                print(f"\nMatch #{i}:")
                print(f"  Item: {dup['item']}")
                print(f"  Similarity: {dup['similarity']:.3f} ({dup['similarity']*100:.1f}%)")
                print(f"  Index: {dup['index']}")
        else:
            print("✅ No duplicates found! This item is unique.")
            duplicate_data = []
        
        # INTERPRETABILITY SECTION
        if len(duplicate_indices) > 0:
            print_header("🔬 INTERPRETABILITY")
            
            top_match = duplicate_data[0]
            top_idx = top_match['index']
            
            # Feature Importance
            print("\n📊 Feature Importance Analysis")
            print_separator("-")
            
            feature_names = tfidf_vectorizer.get_feature_names_out()
            input_vector = tfidf_vectorizer.transform([item_to_check])
            match_vector = tfidf_matrix[top_idx]
            
            input_array = input_vector.toarray()[0]
            match_array = match_vector.toarray()[0]
            
            # Get top contributing features
            shared_features = input_array * match_array
            top_feature_indices = np.argsort(shared_features)[-20:][::-1]
            
            print("\nTop 10 Most Important Shared Features:")
            print(f"{'Feature':<20} {'Input TF-IDF':<15} {'Match TF-IDF':<15} {'Shared':<15}")
            print_separator("-")
            for idx in top_feature_indices[:10]:
                if shared_features[idx] > 0:
                    print(f"{feature_names[idx]:<20} {input_array[idx]:<15.4f} {match_array[idx]:<15.4f} {shared_features[idx]:<15.4f}")
            
            # Word Comparison
            print("\n💬 Word-Level Comparison")
            print_separator("-")
            
            input_words = Counter(extract_words(item_to_check))
            match_words = Counter(extract_words(top_match['item']))
            common_words = set(input_words.keys()) & set(match_words.keys())
            
            print(f"\nInput Item: '{item_to_check}'")
            print(f"  Unique words: {len(input_words)}")
            print(f"  Words: {', '.join(list(input_words.keys())[:15])}")
            
            print(f"\nMatched Item: '{top_match['item']}'")
            print(f"  Unique words: {len(match_words)}")
            print(f"  Words: {', '.join(list(match_words.keys())[:15])}")
            
            print(f"\nCommon Words ({len(common_words)}):")
            if common_words:
                print(f"  {', '.join(list(common_words)[:20])}")
                
                print("\nCommon Word Frequencies:")
                print(f"{'Word':<20} {'Input Count':<15} {'Match Count':<15}")
                print_separator("-")
                for word in sorted(common_words, key=lambda w: input_words[w] + match_words[w], reverse=True)[:15]:
                    print(f"{word:<20} {input_words[word]:<15} {match_words[word]:<15}")
            
            # Similarity Statistics
            print("\n📈 Similarity Statistics")
            print_separator("-")
            print(f"Mean Similarity: {np.mean(similarities):.3f}")
            print(f"Max Similarity: {np.max(similarities):.3f}")
            print(f"Min Similarity: {np.min(similarities):.3f}")
            print(f"Items Above Threshold: {len(duplicate_indices)}")
            print(f"Total Items: {len(similarities)}")
        
        print_separator()
        print("✅ Analysis complete!")
        
    except FileNotFoundError:
        print(f"❌ Error: File '{csv_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Duplicate Finder with Interpretability - CLI Version",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli_app.py data.csv product_name "iPhone 13 Pro"
  python cli_app.py data.csv description "laptop computer" --threshold 0.8
        """
    )
    
    parser.add_argument('csv_file', help='Path to CSV file')
    parser.add_argument('column_name', help='Name of the column to analyze')
    parser.add_argument('item_to_check', help='Item to check for duplicates')
    parser.add_argument('--threshold', type=float, default=0.7,
                       help='Similarity threshold (default: 0.7)')
    parser.add_argument('--max-features', type=int, default=5000,
                       help='Max TF-IDF features (default: 5000)')
    
    args = parser.parse_args()
    
    # Print header
    print_header("🔍 DUPLICATE FINDER WITH INTERPRETABILITY")
    print(f"CSV File: {args.csv_file}")
    print(f"Column: {args.column_name}")
    print(f"Item to Check: {args.item_to_check}")
    print(f"Threshold: {args.threshold}")
    print()
    
    # Run analysis
    check_duplicates(
        args.csv_file,
        args.column_name,
        args.item_to_check,
        args.threshold,
        args.max_features
    )

if __name__ == '__main__':
    main()

