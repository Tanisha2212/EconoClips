import requests
from bs4 import BeautifulSoup
import logging
import re
from urllib.parse import urlparse
import streamlit as st

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Headers to simulate a browser request
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0',
}

def extract_from_url(url):
    """
    Extracts content from a URL.
    
    Args:
        url (str): URL of the article
        
    Returns:
        str: Extracted text content or None if error
    """
    try:
        # Validate URL
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            logger.error(f"Invalid URL format: {url}")
            return None
        
        # Request with timeout and headers
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()  # Raise exception for 4XX/5XX responses
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            element.decompose()
        
        # Extract website-specific content based on domain
        domain = parsed_url.netloc
        
        # Try common article containers first
        article_content = None
        
        # Special handling for common news sites
        if 'bloomberg.com' in domain:
            article_content = soup.find('div', class_='body-content')
        elif 'wsj.com' in domain:
            article_content = soup.find('div', class_='article-content')
        elif 'reuters.com' in domain:
            article_content = soup.find('div', class_='article-body')
        elif 'nytimes.com' in domain:
            article_content = soup.find('section', {'name': 'articleBody'})
        elif 'cnbc.com' in domain:
            article_content = soup.find('div', class_='ArticleBody-articleBody')
        elif 'economist.com' in domain:
            article_content = soup.find('div', class_='article__body')
        elif 'ft.com' in domain:
            article_content = soup.find('div', class_='article__content')
        
        # If we found specific article content
        if article_content:
            paragraphs = article_content.find_all('p')
        else:
            # Generic extraction - look for article, main content, or just paragraphs
            article = soup.find('article') or soup.find('main') or soup
            paragraphs = article.find_all('p')
        
        # Extract and filter paragraph text
        texts = []
        for p in paragraphs:
            text = p.get_text().strip()
            # Filter out short or irrelevant paragraphs
            if len(text) > 20 and not re.match(r'^(Copyright|©|All rights reserved)', text):
                texts.append(text)
        
        # Get the article title
        title = soup.find('h1')
        if title:
            title_text = title.get_text().strip()
            texts.insert(0, title_text)  # Add title at the beginning
        
        # Combine paragraphs
        content = ' '.join(texts)
        
        # If content is too short, try a broader approach
        if len(content) < 200:
            # Extract all text from the body
            body = soup.find('body')
            if body:
                # Get all text nodes but filter out very short lines and navigation
                all_text = [t.strip() for t in body.get_text().split('\n') 
                           if len(t.strip()) > 30 and not re.search(r'(menu|sign in|subscribe|copyright)', t.lower())]
                content = ' '.join(all_text)
        
        # If still too short, the URL might not be a news article
        if len(content) < 100:
            logger.warning(f"Extracted content too short for {url}. Length: {len(content)}")
            return None
            
        logger.info(f"Successfully extracted content from {url}. Length: {len(content)}")
        return content
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error for {url}: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Error extracting content from {url}: {str(e)}")
        return None

@st.cache_data(ttl=3600)  # Cache URL content for 1 hour
def cached_url_extract(url):
    """
    Cached version of extract_from_url to prevent redundant requests.
    
    Args:
        url (str): URL of the article
        
    Returns:
        str: Extracted text content or None if error
    """
    return extract_from_url(url)
