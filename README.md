# EconoClips
# EconoClips

EconoClips is a tool that simplifies economic news for students and young professionals by converting complex economic articles into 30-second summaries with simplified terminology.

## Features

- **Daily Economic News**: Get the latest economic news from various categories (business, finance, markets, technology)
- **Article Simplification**: Convert complex economic articles into easy-to-understand 30-second summaries
- **URL Analysis**: Paste any economic news URL to get an instant simplified summary
- **Screenshot Analysis**: Upload screenshots of economic news to extract and simplify the content
- **Term Simplification**: Automatic explanation of complex economic terms

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- NewsAPI key (get one at [newsapi.org](https://newsapi.org/))
- Tesseract OCR (for image analysis)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Tanisha2212/econoclips.git
   cd econoclips
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Tesseract OCR:
   - Windows: Download from [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)
   - Mac: `brew install tesseract`
   - Linux: `sudo apt-get install tesseract-ocr`

4. Create a secrets file:
   - Create a directory named `.streamlit` in the project root if it doesn't exist
   - Create a file `.streamlit/secrets.toml` with the following content:
     ```toml
     NEWS_API_KEY = "your_newsapi_key_here"
     ```

### Running the Application

Run the Streamlit application:
```bash
streamlit run app.py
```

## Project Structure

- `app.py`: Main Streamlit application
- `news_fetcher.py`: News API integration
- `text_processor.py`: NLP summarization and term simplification
- `url_analyzer.py`: URL content extraction
- `image_analyzer.py`: Screenshot analysis
- `preloader.py`: Model preloading functionality
- `requirements.txt`: Dependencies
- `.streamlit/secrets.toml`: API keys and configuration

## Usage Tips

1. **Daily News**: Use this tab to browse the latest economic news and get simplified summaries

2. **URL Analysis**: Paste any economic news article URL to get an instant simplified explanation

3. **Screenshot Analysis**: Upload screenshots of economic news (from newspapers, PDFs, or websites) to extract and simplify the content

## Limitations

- The free tier of NewsAPI has usage restrictions (100 requests per day, limited to headlines)
- OCR accuracy depends on the quality of the uploaded images
- For very technical or specialized economic content, some terms might not be simplified

## Future Enhancements

- Add more economic terms to the simplification dictionary
- Implement user accounts to save favorite articles
- Add support for multiple languages
- Create mobile application versions

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [NewsAPI](https://newsapi.org/) for providing the news data
- [Hugging Face Transformers](https://huggingface.co/transformers/) for NLP capabilities
- [Streamlit](https://streamlit.io/) for the web framework
