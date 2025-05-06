import logging
from transformers import pipeline
import streamlit as st

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize models at startup
@st.cache_resource
def load_summarizer_model():
    """
    Preloads the summarization model.
    
    Returns:
        transformers.Pipeline: Loaded summarization model
    """
    try:
        logger.info("Loading summarization model...")
        # Use a fast, lightweight model suitable for summarization
        # Facebook/bart-large-cnn is good for news summarization
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)  # device=-1 for CPU
        logger.info("Summarization model successfully loaded!")
        return summarizer
    except Exception as e:
        logger.error(f"Error loading summarization model: {str(e)}")
        # Fallback to a smaller model if loading fails
        logger.info("Attempting to load smaller fallback model...")
        try:
            summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-6-6", device=-1)
            logger.info("Fallback summarization model successfully loaded!")
            return summarizer
        except Exception as e2:
            logger.error(f"Error loading fallback model: {str(e2)}")
            st.error("Failed to load summarization models. Please try restarting the application.")
            return None

# Load the model at startup
summarizer_model = load_summarizer_model()