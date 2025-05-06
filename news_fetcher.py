import requests
import logging
import streamlit as st

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_news(api_key, category="business", country="us", page_size=10):
    """
    Fetches news articles from NewsAPI based on category.
    
    Args:
        api_key (str): NewsAPI key
        category (str): News category (business, economy, etc.)
        country (str): Country code (us, gb, etc.)
        page_size (int): Number of articles to fetch
        
    Returns:
        dict: JSON response from NewsAPI or None if error
    """
    try:
        # Map Streamlit category selections to NewsAPI categories
        category_mapping = {
            "economy": "business",  # NewsAPI doesn't have 'economy' category
            "finance": "business",  # Map finance to business
            "markets": "business",  # Map markets to business
            "technology": "technology"
        }
        
        # Use mapped category or default to the original if not in mapping
        api_category = category_mapping.get(category, category)
        
        # Add relevant search terms for finance-related queries when using business category
        if category in ["economy", "finance", "markets"]:
            # Use q parameter for specific keywords within business category
            query_terms = {
                "economy": "economy OR economic OR GDP OR inflation",
                "finance": "finance OR financial OR banks OR investment",
                "markets": "stock OR market OR trading OR investors"
            }
            url = f"https://newsapi.org/v2/top-headlines?country={country}&category=business&q={query_terms[category]}&pageSize={page_size}&apiKey={api_key}"
        else:
            # Standard category query
            url = f"https://newsapi.org/v2/top-headlines?country={country}&category={api_category}&pageSize={page_size}&apiKey={api_key}"
        
        logger.info(f"Fetching news for category: {category}")
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            logger.info(f"Successfully fetched {len(data.get('articles', []))} articles")
            return data
        else:
            logger.error(f"Error fetching news: {response.status_code}, {response.text}")
            return None
            
    except Exception as e:
        logger.error(f"Exception in get_news: {str(e)}")
        return None