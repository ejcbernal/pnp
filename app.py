from flask import *
import os
import pymongo
from bson.objectid import ObjectId
from bson.binary import Binary
from bson import BSON
import datetime
from werkzeug.utils import secure_filename
from PIL import Image
from io import BytesIO
from webcamvideostream import WebcamVideoStream
import time
import cv2

DB_NAME = 'heroku_6q3vw2q0'  
DB_HOST = 'ds257054.mlab.com'
DB_PORT = 57054
DB_USER = 'admin' 
DB_PASS = 'password123'

myclient = pymongo.MongoClient(DB_HOST, DB_PORT)
mydb = myclient[DB_NAME]
mydb.authenticate(DB_USER, DB_PASS)

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']

app = Flask(__name__)
app.secret_key = 'pnp-secret-key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    try:
        if endpoint == 'static':
            filename = values.get('filename', None)
            if filename:
                file_path = os.path.join(app.root_path,
                                        endpoint, filename)
                values['q'] = int(os.stat(file_path).st_mtime)
        return url_for(endpoint, **values)
    except FileNotFoundError:
        return url_for(
			"static",
			filename='images/not_found.png'
	)

##
# PAGES
##

@app.route('/')
def home():
	return render_template('home.html')	

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(
		gen(WebcamVideoStream().start()),
        mimetype='multipart/x-mixed-replace; boundary=frame'
	)


def gen(camera):
	time.sleep(10.0)
	while True:
		frame = camera.read()

if(__name__ == '__main__'):
    app.run(
		host='localhost',
		port=5000,
		debug=True,
		threaded=True
	)