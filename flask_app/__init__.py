import os
from flask import Flask
app = Flask(__name__)

app.secret_key = "this one is for one."

UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER