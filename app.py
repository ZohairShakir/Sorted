import os
import shutil
from flask import Flask, request, jsonify, render_template,send_file
from werkzeug.utils import secure_filename
import fitz  # PyMuPDF
import zipfile
import threading
import time 
import joblib

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
CATEGORIZED_FOLDER = 'categorized'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model = joblib.load("model.pkl")

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CATEGORIZED_FOLDER, exist_ok=True)

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        files = request.files.getlist('files')
        if not files:
            return jsonify({'error': 'No files uploaded'}), 400

        # Create folder for categorized PDFs
        base_output_dir = "categorized"
        corrupted_dir = os.path.join(base_output_dir, "corrupted")
        if os.path.exists(base_output_dir):
            shutil.rmtree(base_output_dir)
        os.makedirs(base_output_dir)
        os.makedirs(corrupted_dir)

        predictions = {}
        for file in files:
            filename = secure_filename(file.filename)
            file_path = os.path.join("uploads", filename)
            file.save(file_path)

            try:
                text = extract_text_from_pdf(file_path)
                if not text.strip():
                    raise ValueError("No text extracted")

                category = model.predict([text])[0]
                predictions[filename] = category

                cat_folder = os.path.join(base_output_dir, category)
                os.makedirs(cat_folder, exist_ok=True)
                shutil.copy(file_path, os.path.join(cat_folder, filename))

            except Exception as file_error:
                print(f"[!] Corrupted: {filename} -> {file_error}")
                shutil.copy(file_path, os.path.join(corrupted_dir, filename))
                predictions[filename] = "corrupted"

        # Create ZIP
        shutil.make_archive("categorized", 'zip', base_output_dir)
        return jsonify({'predicted': predictions})
    
    except Exception as e:
        print(f"Error with file {file.filename if 'file' in locals() else 'unknown'}: {e}")
        return jsonify({'error': str(e)}), 500



def zip_categorized_files(base_dir='categorized'):
    zipf = zipfile.ZipFile('categorized.zip', 'w', zipfile.ZIP_DEFLATED)
    for root, _, files in os.walk(base_dir):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, base_dir)
            zipf.write(file_path, arcname)
    zipf.close()

@app.route('/download')
def download():
    zip_path = "categorized.zip"
    if os.path.exists(zip_path):
        # Serve the file
        response = send_file(zip_path, as_attachment=True)
        
        # Schedule deletion of both ZIP and folder
        def delete_zip_and_folder():
            time.sleep(5)
            if os.path.exists(zip_path):
                os.remove(zip_path)
            if os.path.exists('categorized'):
                shutil.rmtree('categorized')

        threading.Thread(target=delete_zip_and_folder).start()
        return response
    else:
        return "File not found", 404


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
