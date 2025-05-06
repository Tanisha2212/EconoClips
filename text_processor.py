import re
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Dictionary of economic terms and their simplified versions
ECON_TERMS = {
    "inflation": "rising prices",
    "recession": "economic downturn",
    "GDP": "total value of goods and services",
    "fiscal policy": "government spending and tax decisions",
    "monetary policy": "central bank's control of money supply",
    "quantitative easing": "when central banks buy securities to increase money supply",
    "interest rates": "cost of borrowing money",
    "bull market": "rising stock market",
    "bear market": "falling stock market",
    "volatility": "rapid price changes",
    "liquidity": "how easily assets can be converted to cash",
    "yield": "return on investment",
    "bonds": "loans to companies or governments",
    "equities": "stocks or shares",
    "commodities": "raw materials like gold or oil",
    "deficit": "when spending exceeds income",
    "debt": "money that is owed",
    "leverage": "using borrowed money to invest",
    "appreciation": "increase in value",
    "depreciation": "decrease in value",
    "stimulus": "government actions to boost the economy",
    "austerity": "reduced government spending",
    "stagflation": "inflation with stagnant economic growth",
    "supply and demand": "relationship between availability and desire for products",
    "Federal Reserve": "US central bank",
    "ECB": "European Central Bank",
    "IPO": "Initial Public Offering (when a company first sells shares)",
    "hedge fund": "investment fund using various strategies to make money",
    "derivatives": "financial contracts based on other assets",
    "securities": "tradable financial assets",
    "collateral": "assets pledged as security for a loan",
    "capital gains": "profit from selling investments",
    "dividend": "portion of profits paid to shareholders",
    "portfolio": "collection of investments",
    "diversification": "spreading investments across different assets",
    "merger": "two companies joining together",
    "acquisition": "one company buying another",
    "valuation": "estimated worth of a company",
    "P/E ratio": "price-to-earnings ratio (stock price divided by earnings per share)",
    "market cap": "total value of a company's shares",
    "index": "measure of a section of the stock market",
    "S&P 500": "index tracking 500 large US companies",
    "Dow Jones": "index tracking 30 large US companies",
    "NASDAQ": "US technology stock exchange",
    "NYSE": "New York Stock Exchange",
    "futures": "contracts to buy or sell assets at future dates",
    "options": "contracts giving the right to buy or sell assets at set prices",
    "cryptocurrency": "digital or virtual currency",
    "blockchain": "digital ledger technology behind cryptocurrencies",
    "bitcoin": "the first and most popular cryptocurrency",
    "unemployment rate": "percentage of people without jobs",
    "CPI": "Consumer Price Index (measures inflation)",
    "PPI": "Producer Price Index (measures wholesale inflation)",
    "basis points": "one hundredth of a percentage point",
    "FOMC": "Federal Open Market Committee (sets US interest rates)",
    "treasury bonds": "US government debt securities",
    "corporate bonds": "company debt securities",
    "junk bonds": "high-risk, high-reward bonds",
    "ETF": "Exchange-Traded Fund (basket of securities)",
    "mutual fund": "professionally managed investment fund",
    "REIT": "Real Estate Investment Trust",
    "short selling": "betting that an asset will fall in value",
    "margin": "borrowing money to invest",
    "arbitrage": "exploiting price differences in different markets",
    "liquidity risk": "risk of not being able to sell an asset quickly",
    "default risk": "risk that a borrower won't repay a loan",
    "systemic risk": "risk affecting the entire financial system",
    "forex": "foreign exchange market",
    "trade deficit": "when imports exceed exports",
    "tariffs": "taxes on imported goods",
    "sanctions": "penalties imposed on a country",
    "devaluation": "deliberate lowering of a currency's value",
    "emerging markets": "developing economies",
    "developed markets": "advanced economies",
}

def simplify_terms(text):
    """
    Replaces economic jargon with simplified explanations.
    
    Args:
        text (str): Text containing economic terms
        
    Returns:
        str: Text with simplified terms in parentheses
    """
    # Make a copy of the text to avoid modifying it during iteration
    simplified_text = text
    
    # Case-insensitive replacement for key terms
    for term, simple in ECON_TERMS.items():
        # Use regex for case-insensitive matching
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        # Check if the term exists in the text
        if pattern.search(simplified_text):
            # Replace with original text plus definition
            match = pattern.search(simplified_text).group(0)  # Get the actual match with its casing
            replacement = f"{match} ({simple})"
            simplified_text = pattern.sub(replacement, simplified_text, count=1)  # Only replace first occurrence
    
    return simplified_text

def create_econoclip(text, summarizer_model):
    """
    Creates an EconoClip summary from text.
    
    Args:
        text (str): Original text content
        summarizer_model: Pre-loaded summarization model
        
    Returns:
        str: Simplified and summarized text
    """
    try:
        # Clean the text
        cleaned_text = clean_text(text)
        
        # Skip if text too short
        if len(cleaned_text.split()) < 30:
            return simplify_terms(cleaned_text)
        
        # Summarize to ~30 seconds of reading (approximately 75-100 words)
        # Calculate max_length based on original text length to avoid too short summaries
        max_length = min(100, max(75, len(cleaned_text.split()) // 3))
        min_length = min(75, max(40, len(cleaned_text.split()) // 4))
        
        # Ensure min_length is less than max_length
        if min_length >= max_length:
            min_length = max_length - 10
        
        # Generate summary
        summary = summarizer_model(cleaned_text, max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text']
        
        # Simplify economic terms
        simplified = simplify_terms(summary)
        
        # Add bullet point indicators for key points
        final_text = highlighted_points(simplified)
        
        return final_text
        
    except Exception as e:
        logger.error(f"Error in create_econoclip: {str(e)}")
        # Return simplified original text if summarization fails
        return simplify_terms(text[:500] + "...")

def clean_text(text):
    """
    Cleans text by removing unnecessary characters and formatting.
    
    Args:
        text (str): Raw text
        
    Returns:
        str: Cleaned text
    """
    # Remove any HTML tags
    text = re.sub(r'<.*?>', '', text)
    
    # Remove multiple spaces and newlines
    text = re.sub(r'\s+', ' ', text)
    
    # Remove common NewsAPI suffixes like "[+2900 chars]"
    text = re.sub(r'\[\+\d+ chars\]', '', text)
    
    return text.strip()

def highlighted_points(text):
    """
    Formats text with highlighted key points.
    
    Args:
        text (str): Simplified text
        
    Returns:
        str: Formatted text with highlights
    """
    # For simplicity, we'll just add a couple of bullet points
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    # If there are fewer than 3 sentences, return the original text
    if len(sentences) < 3:
        return text
    
    # Create a bulleted list for better readability
    result = "<strong>Key Points:</strong><ul>"
    
    # Add first sentence as a key point
    result += f"<li>{sentences[0]}</li>"
    
    # Add middle sentence as a key point
    mid_point = len(sentences) // 2
    if sentences[mid_point] != sentences[0]:
        result += f"<li>{sentences[mid_point]}</li>"
    
    # Add last sentence as a key point
    if sentences[-1] != sentences[0] and sentences[-1] != sentences[mid_point]:
        result += f"<li>{sentences[-1]}</li>"
    
    result += "</ul>"
    
    # Add the full text below
    result += f"<br><strong>Full Summary:</strong><br>{text}"
    
    return result