import os
import base64
import requests
import pandas as pd
import language_tool_python
from flask import Flask, request, render_template, send_file, jsonify
from PIL import Image
from io import BytesIO
import tempfile

# Constants
API_KEY = 'K87266024688957'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Flask app setup
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# LanguageTool instance
tool = language_tool_python.LanguageToolPublicAPI('en-US')

# OCR function using OCR.space
def ocr_space_extract(image_path, api_key=API_KEY):
    try:
        with open(image_path, 'rb') as image_file:
            response = requests.post(
                'https://api.ocr.space/parse/image',
                files={'filename': image_file},
                data={'apikey': api_key, 'language': 'eng'},
                timeout=15
            )
        result = response.json()

        # Check for successful parsing
        if result.get('IsErroredOnProcessing'):
            raise ValueError(result.get('ErrorMessage', 'OCR API error'))

        parsed_results = result.get('ParsedResults')
        if not parsed_results or not parsed_results[0].get('ParsedText'):
            raise ValueError('No text extracted from image.')

        return parsed_results[0]['ParsedText'].strip()

    except Exception as e:
        raise RuntimeError(f"OCR failed: {e}")

# Grammar correction function
def correct_grammar(text):
    matches = tool.check(text)
    return language_tool_python.utils.correct(text, matches)

# Save and resize image from URL
def save_image_from_url(url, save_path):
    response = requests.get(url, timeout=15)
    image = Image.open(BytesIO(response.content))

    if image.mode == 'P':
        image = image.convert('RGB')

    image.thumbnail((1024, 1024))
    image.save(save_path)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_url', methods=['POST'])
def upload_url():
    image_url = request.form['image_url']
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'from_url.jpg')
    try:
        save_image_from_url(image_url, image_path)
        raw_text = ocr_space_extract(image_path)
        corrected_text = correct_grammar(raw_text)
    except Exception as e:
        corrected_text = f"Error processing image URL: {e}"
    return render_template('index.html', corrected_text=corrected_text)

@app.route('/upload_excel', methods=['POST'])
def upload_excel():
    file = request.files['excel_file']
    if not file:
        return "No file uploaded"

    df = pd.read_excel(file)
    if 'Image_URL' not in df.columns:
        return "Excel must have a column named 'Image_URL'"

    results = []
    for url in df['Image_URL']:
        try:
            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
                save_image_from_url(url, tmp.name)
                text = ocr_space_extract(tmp.name)
                corrected = correct_grammar(text)
                results.append(corrected)
        except Exception as e:
            results.append(f"Error: {e}")

    df['Extracted_Text'] = results
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'results.xlsx')
    df.to_excel(output_path, index=False)

    return send_file(output_path, as_attachment=True)

@app.route('/upload_image', methods=['POST'])
def upload_image():
    image = request.files['image_file']
    if not image:
        return "No image file uploaded"

    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
    image.save(image_path)

    try:
        raw_text = ocr_space_extract(image_path)
        corrected_text = correct_grammar(raw_text)
    except Exception as e:
        corrected_text = f"Error processing image: {e}"

    return render_template('index.html', corrected_text=corrected_text)

@app.route('/upload_base64', methods=['POST'])
def upload_base64():
    try:
        image_data = request.form['image']
        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]

        image_bytes = base64.b64decode(image_data)

        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            tmp.write(image_bytes)
            tmp.flush()
            tmp_path = tmp.name

        raw_text = ocr_space_extract(tmp_path)
        corrected_text = correct_grammar(raw_text)

        return jsonify({'text': corrected_text})

    except Exception as e:
        return jsonify({'error': f"Base64 upload failed: {e}"}), 400

if __name__ == '__main__':
    app.run(debug=True)
