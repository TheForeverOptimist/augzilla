import os, secrets
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpeg', 'jpg', 'tiff', 'heic', 'webp'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = secrets.token_hex(16)

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/begin.html')
def begin():
    return render_template('begin.html')

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/begin', methods =['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        #check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        #if user does not select a file, the browser submits an empty file without a file name
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #generating a unique filename using the original filename and a timestamp
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            unique_filename = f"{timestamp}_{filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],unique_filename))
            flash('File uploaded successfully', 'success')
            return redirect(url_for('augment', filename=unique_filename, show_filename=True))
        else:
            flash ('Invalid file')
            return redirect(request.url)
    
    return render_template('begin.html')
    

@app.route('/augment/')
def augment():
    filename = request.args.get('filename')
    if filename:
        show_filename = f"Let's Augment {filename}"
        return render_template('augment.html', show_filename=show_filename)
    else:
        flash('No filename found', 'error')
        return redirect(url_for('begin'))




@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)





