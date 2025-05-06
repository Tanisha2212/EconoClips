import pytesseract
from PIL import Image
import cv2
import numpy as np
import logging
import io
import streamlit as st

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_from_image(image):
    """
    Extracts text from an image using OCR.
    
    Args:
        image (PIL.Image): Image object
        
    Returns:
        str: Extracted text or None if error
    """
    try:
        # Convert PIL Image to OpenCV format
        img_array = np.array(image)
        
        # Check if image is color or grayscale
        if len(img_array.shape) == 3:
            # Convert color image to grayscale
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
            
        # Apply image preprocessing for better OCR results
        preprocessed_image = preprocess_image(gray)
        
        # Convert back to PIL Image for Tesseract
        processed_pil = Image.fromarray(preprocessed_image)
        
        # Run OCR with improved configuration
        text = pytesseract.image_to_string(
            processed_pil,
            config='--psm 6 --oem 3 -l eng'  # Page segmentation mode 6 (assume single block of text)
        )
        
        # Clean the extracted text
        cleaned_text = clean_ocr_text(text)
        
        logger.info(f"Successfully extracted {len(cleaned_text)} characters from image")
        return cleaned_text
        
    except Exception as e:
        logger.error(f"Error extracting text from image: {str(e)}")
        return None

def preprocess_image(img):
    """
    Preprocesses the image to improve OCR quality.
    
    Args:
        img (numpy.ndarray): Grayscale image
        
    Returns:
        numpy.ndarray: Preprocessed image
    """
    try:
        # Check image size and resize if too large
        height, width = img.shape
        max_dimension = 1800
        
        if max(height, width) > max_dimension:
            scale_factor = max_dimension / max(height, width)
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            img = cv2.resize(img, (new_width, new_height))
        
        # Apply bilateral filter to preserve edges while reducing noise
        img = cv2.bilateralFilter(img, 9, 75, 75)
        
        # Apply adaptive thresholding to handle varying lighting conditions
        img = cv2.adaptiveThreshold(
            img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        
        # Apply morphological operations to clean up the image
        kernel = np.ones((1, 1), np.uint8)
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        
        return img
        
    except Exception as e:
        logger.error(f"Error in image preprocessing: {str(e)}")
        return img  # Return original image if preprocessing fails

def clean_ocr_text(text):
    """
    Cleans OCR text by removing noise and formatting issues.
    
    Args:
        text (str): Raw OCR text
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
        
    # Replace multiple newlines with single newline
    text = '\n'.join([line for line in text.split('\n') if line.strip()])
    
    # Remove non-printable characters
    text = ''.join(c for c in text if c.isprintable() or c in ['\n', ' '])
    
    # Replace multiple spaces with single space
    text = ' '.join(text.split())
    
    return text

@st.cache_data
def cached_image_extract(image_bytes):
    """
    Cached version of extract_from_image to prevent redundant processing.
    
    Args:
        image_bytes (bytes): Image file bytes
        
    Returns:
        str: Extracted text or None if error
    """
    image = Image.open(io.BytesIO(image_bytes))
    return extract_from_image(image)