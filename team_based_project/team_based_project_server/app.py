from flask import Flask 
from flask import flash, request, redirect, render_template, send_from_directory
from flask_cors import CORS

import os
import urllib.request
from werkzeug.utils import secure_filename
import DLmodel
import make_caption


file_path="./uploads/"
output_path = "./downloads/"
store_path="./deep_learning_application/extracted_image"
file_name="test.docx"

ALLOWED_EXTENSIONS = set(['docx', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processFile(file_name):
    make_caption.extractImg(file_path, file_name, store_path)
    arr = os.listdir('./deep_learning_application/extracted_image')
    arr.sort()
    prediction = DLmodel.generateAll(arr)
    print (prediction)
    make_caption.changeCaption(file_path,file_name, prediction, output_path, 'out_' + file_name)
    return 

UPLOAD_FOLDER = './uploads'
DOWNLOAD_FOLDER = './downloads'
processedFileName = "Hello"

app = Flask(__name__)
CORS(app)


app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            processFile(file_name)
            processedFileName = file.filename
            print (processedFileName)
            flash('File successfully uploaded')
            return redirect('/')
        else:
            flash('Allowed file types are docx, txt, pdf, png, jpg, jpeg, gif')
            return redirect(request.url)

@app.route('/downloads/<filename>')
def download_file(filename):
    #processFile(file_name)
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/excute')
def excute():
    processFile("test.docx")
    return {'hello': 'world'}
if __name__ == "__main__":
    #processFile(file_name)
    #processFile("test.docx")
    #app.run() 
    app.run(host="127.0.0.1",port=5000,threaded=False)