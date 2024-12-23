import os
import fitz  # PyMuPDF
from flask import Flask, flash, request, redirect, url_for, request, jsonify, send_from_directory, render_template
from werkzeug.utils import secure_filename
from pdf2image import convert_from_path

UPLOAD_FOLDER = "C:\\Users\\bianc\\RecapIt\\uploads"
ALLOWED_EXTENSIONS = {'pdf'}
IMAGES_FOLDER = "C:\\Users\\bianc\\RecapIt\\static\\images"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['IMAGES_FOLDER'] = IMAGES_FOLDER
pdf_file = "C:\\Users\\bianc\\RecapIt\\uploads\\ASD1_Tema2.pdf"  # Replace with your PDF file path
output_dir = "C:\\Users\\bianc\\RecapIt\\static\\images"  # Replace with your output folder

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def pdf_to_jpg(pdf_path, output_folder):
    pdf_document = fitz.open(pdf_path)
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        output_path = f"{output_folder}/page_{page_num + 1}.jpg"
        pix.save(output_path)
        print(f"Saved: {output_path}")
    pdf_document.close()

@app.route('/newlearn', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(pdf_path)
            pdf_name = os.path.splitext(filename)[0]
            images_folder = os.path.join(app.config['IMAGES_FOLDER'], pdf_name)
            os.makedirs(images_folder, exist_ok=True)
            pdf_to_jpg(pdf_path, images_folder)
            
            return redirect(url_for('learning'))

    return render_template('newlearn.html')

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route('/display')
def display():
    return render_template('display.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/learning')
def learning():
    # Get the most recent folder with converted images (from the upload process)
    pdf_folders = [f for f in os.listdir(app.config['IMAGES_FOLDER']) if os.path.isdir(os.path.join(app.config['IMAGES_FOLDER'], f))]
    if not pdf_folders:
        return render_template('learning.html', image_urls=[])

    latest_folder = max(pdf_folders, key=lambda folder: os.path.getmtime(os.path.join(app.config['IMAGES_FOLDER'], folder)))
    images_folder = os.path.join(app.config['IMAGES_FOLDER'], latest_folder)

    # Get all the image files in the folder
    image_files = [f"/static/images/{latest_folder}/{img}" for img in os.listdir(images_folder) if img.endswith('.jpg')]

    # Shuffle images randomly
    import random
    random.shuffle(image_files)

    # Pass the list of images to the template
    return render_template('learning.html', image_urls=image_files)

@app.route('/test')
def test():
    return render_template('test.html')




