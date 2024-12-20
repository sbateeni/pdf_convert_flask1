import os
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import PyPDF2

def convert_pdf_to_images_and_text(pdf_path, page_range=None, languages=None):
    """
    Convert PDF pages to images and extract text using OCR
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    # Get total number of pages
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        total_pages = len(pdf_reader.pages)
    
    # Convert pages to images
    try:
        # Try with default PATH
        images = convert_from_path(pdf_path)
    except Exception as e:
        # If Poppler is not in PATH, try with specific poppler path
        poppler_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'poppler', 'bin')
        if os.path.exists(poppler_path):
            images = convert_from_path(pdf_path, poppler_path=poppler_path)
        else:
            raise Exception("Poppler not found. Please install Poppler and add it to PATH or place it in 'poppler' folder.")
    
    # Process specified pages or all pages
    pages_to_process = range(len(images))
    if page_range:
        start, end = map(int, page_range.split('-'))
        pages_to_process = range(start-1, min(end, len(images)))
    
    text = ""
    page_languages = {}
    pages_processed = []
    
    for i in pages_to_process:
        # Extract text using OCR
        if languages:
            text += pytesseract.image_to_string(images[i], lang='+'.join(languages))
        else:
            text += pytesseract.image_to_string(images[i])
        
        text += f"\n--- Page {i+1} ---\n"
        pages_processed.append(i+1)
        page_languages[i+1] = languages if languages else ['auto']
    
    return text, total_pages, page_languages, pages_processed
