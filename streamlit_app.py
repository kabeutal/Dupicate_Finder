import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import re

# Page configuration
st.set_page_config(
    page_title="Duplicate Finder with Interpretability",
    page_icon="🔍",
    layout="wide"
)

# Initialize session state
if 'dataset' not in st.session_state:
    st.session_state.dataset = None
if 'tfidf_vectorizer' not in st.session_state:
    st.session_state.tfidf_vectorizer = None
if 'tfidf_matrix' not in st.session_state:
    st.session_state.tfidf_matrix = None
if 'selected_column' not in st.session_state:
    st.session_state.selected_column = None
if 'text_data' not in st.session_state:
    st.session_state.text_data = None

st.title("🔍 Duplicate Finder with Interpretability")
st.markdown("**TF-IDF + Cosine Similarity for Duplicate Detection**")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    threshold = st.slider("Similarity Threshold", 0.0, 1.0, 0.7, 0.05)
    max_features = st.slider("Max TF-IDF Features", 100, 10000, 5000, 100)
    show_interpretability = st.checkbox("Show Interpretability", value=True)

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📥 Input")
    
    # File upload
    uploaded_file = st.file_uploader("Upload CSV Dataset", type=['csv'])
    
    if uploaded_file is not None:
        try:
            st.session_state.dataset = pd.read_csv(uploaded_file)
            st.success(f"✅ Dataset loaded: {len(st.session_state.dataset)} rows")
            
            # Column selection
            st.session_state.selected_column = st.selectbox(
                "Select Text Column to Analyze",
                options=st.session_state.dataset.columns.tolist()
            )
            
            if st.session_state.selected_column:
                # Train model button
                if st.button("🚀 Train Model", type="primary"):
                    with st.spinner("Training TF-IDF model..."):
                        # Prepare text data
                        st.session_state.text_data = st.session_state.dataset[
                            st.session_state.selected_column
                        ].fillna('').astype(str).tolist()
                        
                        # Train TF-IDF
                        st.session_state.tfidf_vectorizer = TfidfVectorizer(
                            max_features=max_features,
                            stop_words='english'
                        )
                        st.session_state.tfidf_matrix = st.session_state.tfidf_vectorizer.fit_transform(
                            st.session_state.text_data
                        )
                        st.success("✅ Model trained successfully!")
                        
                        # Show model info
                        st.info(f"📊 Vocabulary size: {len(st.session_state.tfidf_vectorizer.vocabulary_)}")
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
    
    # Item input
    st.subheader("🔎 Check New Item")
    item_input = st.text_area(
        "Enter item description to check for duplicates:",
        height=100,
        placeholder="Enter item name or description..."
    )
    
    check_button = st.button("🔍 Check for Duplicates", type="primary", disabled=st.session_state.tfidf_vectorizer is None)

with col2:
    st.header("📤 Output")
    
    if check_button and item_input:
        if st.session_state.tfidf_vectorizer is None:
            st.warning("⚠️ Please train the model first!")
        else:
            with st.spinner("Analyzing..."):
                # Vectorize input
                item_vector = st.session_state.tfidf_vectorizer.transform([item_input])
                
                # Calculate similarity
                similarities = cosine_similarity(item_vector, st.session_state.tfidf_matrix)[0]
                
                # Find duplicates
                duplicate_indices = np.where(similarities >= threshold)[0]
                
                if len(duplicate_indices) > 0:
                    st.error(f"⚠️ **DUPLICATE DETECTED!** Found {len(duplicate_indices)} similar item(s)")
                    
                    # Create results dataframe
                    results = []
                    for idx in duplicate_indices:
                        results.append({
                            'Item': st.session_state.dataset.iloc[idx][st.session_state.selected_column],
                            'Similarity Score': f"{similarities[idx]:.3f}",
                            'Similarity %': f"{similarities[idx]*100:.1f}%"
                        })
                    
                    results_df = pd.DataFrame(results)
                    results_df = results_df.sort_values('Similarity Score', ascending=False)
                    st.dataframe(results_df, use_container_width=True)
                    
                    # Store for interpretability
                    st.session_state.duplicate_results = {
                        'item': item_input,
                        'duplicates': [
                            {
                                'index': int(idx),
                                'item': st.session_state.dataset.iloc[idx][st.session_state.selected_column],
                                'similarity': float(similarities[idx])
                            }
                            for idx in duplicate_indices
                        ],
                        'similarities': similarities
                    }
                else:
                    st.success("✅ **No duplicates found!** This item is unique.")
                    st.session_state.duplicate_results = None

# Interpretability Section
if show_interpretability and 'duplicate_results' in st.session_state and st.session_state.duplicate_results:
    st.header("🔬 Interpretability")
    
    results = st.session_state.duplicate_results
    
    # Tabs for different interpretability views
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Similarity Distribution",
        "🔤 Feature Importance",
        "📈 Top Matches Analysis",
        "💬 Word Comparison"
    ])
    
    with tab1:
        st.subheader("Similarity Score Distribution")
        
        # Create histogram
        fig = px.histogram(
            x=results['similarities'],
            nbins=50,
            labels={'x': 'Cosine Similarity Score', 'y': 'Count'},
            title="Distribution of Similarity Scores"
        )
        fig.add_vline(
            x=threshold,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Threshold: {threshold}"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Mean Similarity", f"{np.mean(results['similarities']):.3f}")
        with col2:
            st.metric("Max Similarity", f"{np.max(results['similarities']):.3f}")
        with col3:
            st.metric("Min Similarity", f"{np.min(results['similarities']):.3f}")
        with col4:
            st.metric("Above Threshold", f"{len(results['duplicates'])}")
    
    with tab2:
        st.subheader("TF-IDF Feature Importance")
        
        if len(results['duplicates']) > 0:
            # Get top match
            top_match = results['duplicates'][0]
            top_idx = top_match['index']
            
            # Get feature names
            feature_names = st.session_state.tfidf_vectorizer.get_feature_names_out()
            
            # Get TF-IDF vectors
            input_vector = st.session_state.tfidf_vectorizer.transform([results['item']])
            match_vector = st.session_state.tfidf_matrix[top_idx]
            
            # Convert to arrays
            input_array = input_vector.toarray()[0]
            match_array = match_vector.toarray()[0]
            
            # Get top contributing features
            # Use product of both vectors to find important shared features
            shared_features = input_array * match_array
            top_feature_indices = np.argsort(shared_features)[-20:][::-1]
            
            # Create feature importance dataframe
            feature_importance = []
            for idx in top_feature_indices:
                if shared_features[idx] > 0:
                    feature_importance.append({
                        'Feature': feature_names[idx],
                        'Input TF-IDF': f"{input_array[idx]:.4f}",
                        'Match TF-IDF': f"{match_array[idx]:.4f}",
                        'Shared Importance': f"{shared_features[idx]:.4f}"
                    })
            
            if feature_importance:
                importance_df = pd.DataFrame(feature_importance)
                st.dataframe(importance_df, use_container_width=True)
                
                # Bar chart
                fig = px.bar(
                    importance_df.head(10),
                    x='Feature',
                    y='Shared Importance',
                    title="Top 10 Most Important Shared Features",
                    labels={'Shared Importance': 'TF-IDF Product'}
                )
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Top Matches Detailed Analysis")
        
        # Sort duplicates by similarity
        sorted_duplicates = sorted(results['duplicates'], key=lambda x: x['similarity'], reverse=True)
        
        for i, dup in enumerate(sorted_duplicates[:5], 1):
            with st.expander(f"Match #{i}: Similarity = {dup['similarity']:.3f} ({dup['similarity']*100:.1f}%)"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Input Item:**")
                    st.write(results['item'])
                
                with col2:
                    st.write("**Matched Item:**")
                    st.write(dup['item'])
                
                # Show similarity score
                st.progress(dup['similarity'])
                st.caption(f"Similarity: {dup['similarity']:.3f}")
    
    with tab4:
        st.subheader("Word-Level Comparison")
        
        if len(results['duplicates']) > 0:
            top_match = results['duplicates'][0]
            
            # Extract words
            def extract_words(text):
                words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
                return words
            
            input_words = Counter(extract_words(results['item']))
            match_words = Counter(extract_words(top_match['item']))
            
            # Find common words
            common_words = set(input_words.keys()) & set(match_words.keys())
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write("**Input Words:**")
                st.write(list(input_words.keys())[:20])
                st.metric("Unique Words", len(input_words))
            
            with col2:
                st.write("**Match Words:**")
                st.write(list(match_words.keys())[:20])
                st.metric("Unique Words", len(match_words))
            
            with col3:
                st.write("**Common Words:**")
                st.write(list(common_words)[:20])
                st.metric("Common Words", len(common_words))
            
            # Word frequency comparison
            if common_words:
                common_word_freq = []
                for word in list(common_words)[:15]:
                    common_word_freq.append({
                        'Word': word,
                        'Input Count': input_words[word],
                        'Match Count': match_words[word]
                    })
                
                freq_df = pd.DataFrame(common_word_freq)
                
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=freq_df['Word'],
                    y=freq_df['Input Count'],
                    name='Input',
                    marker_color='lightblue'
                ))
                fig.add_trace(go.Bar(
                    x=freq_df['Word'],
                    y=freq_df['Match Count'],
                    name='Match',
                    marker_color='lightcoral'
                ))
                fig.update_layout(
                    title="Common Word Frequency Comparison",
                    xaxis_title="Word",
                    yaxis_title="Frequency",
                    barmode='group'
                )
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("**How it works:**")
st.markdown("""
1. **TF-IDF Vectorization**: Converts text into numerical vectors based on term frequency and inverse document frequency
2. **Cosine Similarity**: Measures the angle between vectors to determine similarity (0 = different, 1 = identical)
3. **Threshold-based Detection**: Items with similarity above the threshold are flagged as duplicates
4. **Interpretability**: Shows which features (words) contribute most to the similarity score
""")
