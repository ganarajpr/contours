import os
from flask import Flask, request, redirect, url_for, send_from_directory,jsonify
from werkzeug import secure_filename
from contour import getBoundingBoxes
import uuid

UPLOAD_FOLDER = '/home/ganaraj/github/detection/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

def getFileExtension(filename):
    filename, file_extension = os.path.splitext(filename)
    return file_extension

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['wireframe']
    if file and allowed_file(file.filename):
        filename = str(uuid.uuid4()) + getFileExtension(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],
                    filename))
        return jsonify(bbox=getBoundingBoxes(
                        os.path.join(app.config['UPLOAD_FOLDER'], filename)))
    return jsonify(error='Mismatch file type')

app.run(debug=True)
