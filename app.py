import os
import fitz  # PyMuPDF
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

@app.route('/learn', methods=['GET', 'POST'])
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
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <link rel="icon" type="image/png" sizes="32x32" href="static/images/favicon-32x32.png"/>
        <link rel="stylesheet" href="static/style.css" />
        <script src="static/script.js"></script>
        <title>Recap It</title>
    </head>

    <body>
        <div class="navbar">
            <ul class="nav-links">
                <li><a href = "/display">Home</a></li><!--Unde dai upload-->
                <li><a href = "/learn">Learn</a></li><!--Unde iti apare random-->
                <li><a href = "/about">About</a></li>
            </ul>
        </div>
        <div class="container">
            <h2>Upload new File</h2>
                    <form method="post" enctype="multipart/form-data">
                        <input type="file" name="file" id="file" class="file-input" onchange="showFileName()">
                        <p id="file-name" class="file-name">No file chosen</p>
                        <label for="file" class="file-label">Choose File</label> 
                        <button type="submit" class="file-label">Upload</button>
                    </form>
        </div>
        <div class="attribution">
            Coded by <a href="https://github.com/b14labutoane">Bianca Badescu</a>.
        </div>
  </body>
</html>
    '''

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route('/display')
def display():
    return render_template('display.html')
@app.route('/about')
def about():
    return render_template('about.html')

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
