from flask import Flask, render_template, request, jsonify, session, send_file
from flask_session import Session
from werkzeug.utils import secure_filename
import os
import sys
from pathlib import Path

# Add the root directory to the Python path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from utils.pdf_processing import convert_pdf_to_images_and_text
from utils.text_processing import format_text

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Default settings
DEFAULT_SETTINGS = {
    'use_ocr': True,
    'auto_detect_lang': True,
    'manual_langs': [('eng', 'English - الإنجليزية'), ('ara', 'Arabic - العربية')],
    'enhance_images': True,
    'preview_enhanced': False,
    'correct_spelling': True,
    'remove_extra_spaces': True,
    'line_spacing': False,
    'add_margins': False,
    'output_format': 'txt'
}

@app.route('/')
def index():
    if 'settings' not in session:
        session['settings'] = DEFAULT_SETTINGS
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Only PDF files are allowed'}), 400
    
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        session['current_pdf_path'] = filepath
        return jsonify({'success': True, 'filename': filename})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/process', methods=['POST'])
def process_pdf():
    if 'current_pdf_path' not in session:
        return jsonify({'error': 'No PDF file uploaded'}), 400
    
    try:
        settings = request.json
        page_range = settings.get('page_range') if not settings.get('process_all') else None
        languages = [lang[0] for lang in settings['manual_langs']] if not settings['auto_detect_lang'] else None
        
        text, total_pages, page_languages, pages_processed = convert_pdf_to_images_and_text(
            session['current_pdf_path'],
            page_range=page_range,
            languages=languages
        )
        
        if settings['remove_extra_spaces']:
            text = " ".join(text.split())
        
        pages = text.split('\n--- Page')
        session['converted_pages'] = [page.strip() for page in pages if page.strip()]
        
        return jsonify({
            'success': True,
            'total_pages': total_pages,
            'pages_processed': len(pages_processed),
            'page_languages': page_languages
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/view/<int:page>')
def view_page(page):
    if 'converted_pages' not in session or not session['converted_pages']:
        return jsonify({'error': 'No converted text available'}), 404
    
    total_pages = len(session['converted_pages'])
    if page < 1 or page > total_pages:
        return jsonify({'error': 'Invalid page number'}), 400
    
    page_text = session['converted_pages'][page - 1]
    image_path = f"{session['current_pdf_path']}_page_{page}.png"
    has_image = os.path.exists(image_path)
    
    return jsonify({
        'text': page_text,
        'has_image': has_image,
        'total_pages': total_pages,
        'current_page': page
    })

@app.route('/image/<int:page>')
def get_page_image(page):
    if 'current_pdf_path' not in session:
        return jsonify({'error': 'No PDF file uploaded'}), 404
    
    image_path = f"{session['current_pdf_path']}_page_{page}.png"
    if not os.path.exists(image_path):
        return jsonify({'error': 'Image not found'}), 404
    
    return send_file(image_path, mimetype='image/png')

@app.route('/clear', methods=['POST'])
def clear_results():
    if 'current_pdf_path' in session:
        # Delete temporary image files
        for img_file in Path(app.config['UPLOAD_FOLDER']).glob(f"{session['current_pdf_path']}_page_*.png"):
            try:
                os.remove(img_file)
            except:
                pass
        try:
            os.remove(session['current_pdf_path'])
        except:
            pass
    
    session.pop('converted_pages', None)
    session.pop('current_pdf_path', None)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
