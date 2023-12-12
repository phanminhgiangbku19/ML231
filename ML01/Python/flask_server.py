from __future__ import unicode_literals
from detect_video import *
from youtube import *
from flask import Flask, request, jsonify
import ssl
import os
from flask_cors import CORS

ssl._create_default_https_context = ssl._create_unverified_context
app = Flask(__name__, static_url_path='/static')
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route("/")
def hello_world():
    # resutl = DetectImage(
    #     '/Users/macbook/Downloads/v09044g40000ci3j71jc77uc86cs080g.mov')

    return 'ok'


@app.route("/api/detect", methods=['GET'])
def detect_url():
    path = request.args.get("query")
    file_name = downloadYoutubeVideo(path)
    PREFIX_PATH = "/Users/macbook/documentOfKhanh/Mask_Detect/video/"
    resutl = DetectImage(PREFIX_PATH + file_name, file_name)

    return jsonify({'file_name': file_name})


@app.route("/api/get-list-filenames", methods=['GET'])
def get_list_filenames():
    path = request.args.get("folder")
    path = "static/" + path
    arr = os.listdir(path)

    return jsonify(arr)


if __name__ == "__main__":
    Flask.run(app, debug=True, host='0.0.0.0', port=8080)
