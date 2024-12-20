# PDF to Text Converter - Flask Version

This is the Flask version of the PDF to Text Converter application. It provides the same functionality as the Streamlit version but with a more traditional web interface.

## Features

- PDF text extraction with OCR support
- Multiple language support
- Page range selection
- Image enhancement
- Text processing options
- Beautiful and responsive UI
- Real-time processing feedback
- Page-by-page viewing of results

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install the requirements:
```bash
pip install -r requirements.txt
```

3. Make sure you have Tesseract OCR installed on your system:
- Windows: Download and install from https://github.com/UB-Mannheim/tesseract/wiki
- Linux: `sudo apt-get install tesseract-ocr`
- Mac: `brew install tesseract`

## Running the Application

1. Navigate to the flask_app directory:
```bash
cd flask_app
```

2. Run the Flask application:
```bash
python app.py
```

3. Open your browser and go to:
```
http://localhost:5000
```

## Usage

1. Upload a PDF file by dragging and dropping or clicking the upload area
2. Configure the conversion settings:
   - Language detection (automatic or manual selection)
   - Page range (all pages or specific range)
   - OCR settings
   - Text enhancement options
3. Click "Convert PDF to Text"
4. View the results page by page
5. Copy the extracted text or save it

## Directory Structure

```
flask_app/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css  # Application styles
│   └── js/
│       └── main.js    # Frontend JavaScript
├── templates/
│   └── index.html     # Main HTML template
└── uploads/           # Temporary file storage
```

## Contributing

Feel free to submit issues and enhancement requests!
