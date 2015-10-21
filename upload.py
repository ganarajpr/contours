import os
from flask import Flask, request, redirect, url_for, send_from_directory,jsonify
from werkzeug import secure_filename
from contour import getBoundingBoxes
import uuid
from flask.ext.cors import CORS
import subprocess

UPLOAD_FOLDER = '/home/ganaraj/contours/upload'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
cors = CORS(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

def getFileExtension(filename):
    filename, file_extension = os.path.splitext(filename)
    return file_extension

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

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



#docker run -v /home/ganaraj/nndetect:/detect -w /detect/prediction -it --rm opecv3
@app.route('/detect', methods=['POST'])
def detect_file():
    file = request.files['wireframe']
    if file and allowed_file(file.filename):
        filename = str(uuid.uuid4()) + getFileExtension(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],
                    filename))
	p = subprocess.Popen(["docker","run","-v","/home/ganaraj/contours/upload:/detect","-w",
			"/detect","-it","--rm","opecv3", "./prediction",
                   filename ], stdout=subprocess.PIPE)
	output, err = p.communicate()
	return jsonify(result=output.rstrip())
    return jsonify(error='Mismatch file type')

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=9000)
