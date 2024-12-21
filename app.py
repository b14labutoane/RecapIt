import os
from flask import Flask, flash, request, redirect, url_for, request, jsonify, send_from_directory, render_template
from werkzeug.utils import secure_filename
from pdf2image import convert_from_path

UPLOAD_FOLDER = "C:\\Users\\bianc\\RecapIt\\uploads"
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route('/display')
def display():
    return render_template('display.html')

import fitz  # PyMuPDF

def pdf_to_jpg(pdf_path, output_folder):
    """
    Convert a PDF to JPG images using PyMuPDF.
    
    Args:
        pdf_path (str): Path to the PDF file.
        output_folder (str): Path to save the converted images.
    """
    # Open the PDF
    pdf_document = fitz.open(pdf_path)

    for page_num in range(len(pdf_document)):
        # Get page
        page = pdf_document.load_page(page_num)
        
        # Render page to a pixmap (image)
        pix = page.get_pixmap()
        
        # Define output path
        output_path = f"{output_folder}/page_{page_num + 1}.jpg"
        
        # Save image as JPG
        pix.save(output_path)
        print(f"Saved: {output_path}")

    # Close the PDF document
    pdf_document.close()

pdf_file = "C:\\Users\\bianc\\RecapIt\\uploads\\ASD1_Tema2.pdf"  # Replace with your PDF file path
output_dir = "C:\\Users\\bianc\\RecapIt\\static\\images"  # Replace with your output folder

pdf_to_jpg(pdf_file, output_dir)
