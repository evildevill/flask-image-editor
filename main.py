# pip3 install flask opencv-python
from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
from flask_restful import Resource, Api
import cv2, os
import logging
from PIL import Image
from PIL.ExifTags import TAGS
import numpy as np
from flask_limiter import Limiter

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'webp', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
api = Api(app)
app.secret_key = 'e2c90d64679fe91b4c9cc7cee2e2146334c0e843618094f998'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processImage(filename, operation):
    print(f"the operation is {operation} and filename is {filename}")
    img = cv2.imread(f"uploads/{filename}")
    match operation:
        case "cwebp": # used for saving the image as a webp ok
            newFilename = f"static/{filename.split('.')[0]}.webp"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cjpg": # used for saving the image as a jpg ok
            newFilename = f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cpng": # used for saving the image as a png ok
            newFilename = f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cgif": # used for saving the image as a gif ok
            newFilename = f"static/{filename.split('.')[0]}.gif"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cjpeg": # used for saving the image as a jpeg ok
            newFilename = f"static/{filename.split('.')[0]}.jpeg"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cblur": # used for blurring the image ok
            imgProcessed = cv2.GaussianBlur(img, (5, 5), 0)
            newFilename = f"static/{filename}"
            cv2.imwrite(newFilename, imgProcessed)
            return newFilename
        case "csharpen": # used for sharpening the image ok
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            imgProcessed = cv2.filter2D(img, -1, kernel)
            newFilename = f"static/{filename}"
            cv2.imwrite(newFilename, imgProcessed)
            return newFilename
        case "csmooth": # used for smoothing the image ok
            imgProcessed = cv2.medianBlur(img, 5)
            newFilename = f"static/{filename}"
            cv2.imwrite(newFilename, imgProcessed)
            return newFilename
        case "cemboss": # used for embossing the image ok
            kernel = np.array([[0,-1,-1], [1,0,-1], [1,1,0]])
            imgProcessed = cv2.filter2D(img, -1, kernel)
            newFilename = f"static/{filename}"
            cv2.imwrite(newFilename, imgProcessed)
            return newFilename
            # crotate
        case "crotate": # used for rotating the image ok
            imgProcessed = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            newFilename = f"static/{filename}"
            cv2.imwrite(newFilename, imgProcessed)
            return newFilename
        case "cedges": # used for detecting edges in the image ok
            imgProcessed = cv2.Canny(img, 100, 200)
            newFilename = f"static/{filename}"
            cv2.imwrite(newFilename, imgProcessed)
            return newFilename
        case "csepia": # used for converting the image to sepia ok
            imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            imgProcessed = cv2.cvtColor(imgProcessed, cv2.COLOR_GRAY2BGR)
            newFilename = f"static/{filename}"
            cv2.imwrite(newFilename, imgProcessed)
            return newFilename
        case "cinvert": # used for inverting the image ok 
            imgProcessed = cv2.bitwise_not(img)
            newFilename = f"static/{filename}"
            cv2.imwrite(newFilename, imgProcessed)
            return newFilename
        case "ccartoon": # used for converting the image to a cartoon ok 
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.medianBlur(gray, 5)
            edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
            color = cv2.bilateralFilter(img, 9, 300, 300)
            imgProcessed = cv2.bitwise_and(color, color, mask=edges)
            newFilename = f"static/{filename}"
            cv2.imwrite(newFilename, imgProcessed)
            return newFilename
        case "cgray": # used for converting the image to grayscale ok
            imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            newFilename = f"static/{filename}"
            cv2.imwrite(newFilename, imgProcessed)
            return newFilename
        case "ccompress": # used for compressing the image ok
            newFilename = f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(newFilename, img, [cv2.IMWRITE_WEBP_QUALITY, 50])
            return newFilename
    pass

@app.route("/")
def home():
    try:
        return render_template("index.html")
    except Exception as e:
        logging.error(f"Failed to load the home page: {e}")
        return str(e)

@app.route("/about")
def about():
    try:
        return render_template("about.html")
    except Exception as e:
        logging.error(f"Failed to load the about page: {e}")
        return str(e)

@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST": 
        operation = request.form.get("operation")
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "error"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "error no selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = processImage(filename, operation)
            flash(f"Your image has been processed and is available <a href='/{new}' target='_blank'>here</a>")
            return render_template("index.html")

    return render_template("index.html")

# Initialize the Flask Limiter
limiter = Limiter(app, key_func=get_remote_address)

# API
class ImageProcessAPI(Resource):
    decorators = [limiter.limit("100/day;10/hour;1/minute")]

    def post(self):
        operation = request.form.get("operation")
        parameters = request.form.get("parameters")
        if parameters is not None:
            try:
                parameters = json.loads(parameters)
            except json.JSONDecodeError:
                return {"error": "Invalid parameters"}, 400
        # check if the post request has the file part
        if 'file' not in request.files:
            return {"error": "No file part"}, 400
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return {"error": "No selected file"}, 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            try:
                new = processImage(filename, operation, parameters)
            except Exception as e:
                return {"error": str(e)}, 500
            if new is None:
                return {"error": "Failed to process image"}, 500
            else:
                # Get image metadata
                image = Image.open(new)
                width, height = image.size
                file_size = os.path.getsize(new)
                return {
                    "file": send_file(new, mimetype='image/*'),
                    "metadata": {
                        "width": width,
                        "height": height,
                        "file_size": file_size
                    }
                }

api.add_resource(ImageProcessAPI, '/api/process')

app.run(debug=True)