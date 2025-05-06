import streamlit as st
import pandas as pd
from PIL import Image
import io
import base64
import time

st.set_page_config(
    page_title="EconoClips",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import custom modules
from news_fetcher import get_news
from text_processor import create_econoclip, simplify_terms
from url_analyzer import extract_from_url
from image_analyzer import extract_from_image
from preloader import summarizer_model


# Title and description
st.title("EconoClips 📈")
st.subheader("Daily Economic News in 30 Seconds")
st.markdown("---")

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .news-card {
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 15px;
        margin-bottom: 15px;
    }
    .news-title {
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)



# Cache mechanism for news
@st.cache_data(ttl=3600)  # Cache for 1 hour
def cached_news(category):
    # Get API key from secrets
    api_key = st.secrets["NEWS_API_KEY"]
    return get_news(api_key, category)

# Sidebar for navigation
with st.sidebar:
    st.header("Navigation")
    category = st.selectbox(
        "Select news category",
        ["business", "economy", "finance", "markets", "technology"],
        index=0
    )
    
    st.markdown("---")
    st.markdown("### About EconoClips")
    st.markdown("""
    EconoClips simplifies economic news for students and young professionals. 
    We use advanced AI to convert complex economic articles into 30-second summaries 
    with simplified terminology.
    """)

# Tabs for different features
tab1, tab2, tab3 = st.tabs(["Daily News", "URL Analysis", "Screenshot Analysis"])

# # Tab 1: Daily News
with tab1:
    if st.button("Get Latest Economic News", key="fetch_news"):
        with st.spinner("Fetching the latest economic news..."):
            news = cached_news(category)
            
            if news and news.get("articles"):
                for i, article in enumerate(news["articles"][:5]):
                    with st.container():
                        st.markdown(f"""
                        <div class="news-card">
                            <p class="news-title">{article['title']}</p>
                            <p>Source: {article['source']['name']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Use columns for better layout
                        col1, col2 = st.columns([1, 3])
                        
                        # If there's an image, display it
                        if article.get("urlToImage"):
                            with col1:
                                st.image(article["urlToImage"], width=150)
                        
                        with col2:
                            content = article.get("content") or article.get("description", "")
                            if content:
                                simplified = create_econoclip(content, summarizer_model)
                                st.markdown("### 🧠 30-Second Explanation:")
                                st.markdown(f"<div style='background-color:#f0f0f0; padding:10px; border-radius:5px;'>{simplified}</div>", unsafe_allow_html=True)
                            else:
                                st.error("Not enough content to create a summary.")

                        st.markdown("---")
            else:
                st.error("No news articles found. Please try again later.")

# Tab 2: URL Analysis
with tab2:
    st.header("Analyze an Economic News URL")
    url = st.text_input("Enter the URL of an economic news article:")
    
    if url and st.button("Analyze URL"):
        with st.spinner("Analyzing article..."):
            text = extract_from_url(url)
            if text:
                simplified = create_econoclip(text, summarizer_model)
                st.markdown("### 30-Second Explanation:")
                st.markdown(f"<div style='background-color:#f0f0f0; padding:10px; border-radius:5px;'>{simplified}</div>", unsafe_allow_html=True)
            else:
                st.error("Could not extract content from the URL.")

# Tab 3: Screenshot Analysis
with tab3:
    st.header("Analyze a Screenshot of Economic News")
    uploaded_file = st.file_uploader("Upload a screenshot of economic news", type=["jpg", "png", "jpeg"])
    
    if uploaded_file and st.button("Analyze Screenshot"):
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Screenshot", width=400)
        
        with st.spinner("Extracting text and analyzing..."):
            text = extract_from_image(image)
            if text and len(text) > 50:  # Minimum content check
                simplified = create_econoclip(text, summarizer_model)
                st.markdown("### 30-Second Explanation:")
                st.markdown(f"<div style='background-color:#f0f0f0; padding:10px; border-radius:5px;'>{simplified}</div>", unsafe_allow_html=True)
            else:
                st.error("Could not extract enough text from the image. Please try a clearer image.")

# Add footer
st.markdown("---")
st.markdown("Developer-Tanisha")