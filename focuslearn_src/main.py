import time
from Utils import process_frame as pf
import cv2
import json
from flask import Flask, jsonify, request
import numpy as np

app = Flask(__name__)

@app.route('/web_test', methods=['GET'])
def online_test_for_local_laptop():
    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()
        coordinates = pf.get_centroid_coords_from(frame)
        time.sleep(1)
        yield json.dumps(coordinates)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return "No image file found in the request", 400
    
    file = request.files['image']
    file.save('./Resources/' + file.filename)
    
    np_img = np.array(file, dtype=np.uint8)
    coordinates = pf.get_centroid_coords_from(np_img)

    with open('./Resources/coords.txt', 'w') as f:
        f.write(json.dumps(coordinates))
        
data_storage = []

@app.route('/test', methods=['POST'])
def post_data():
    data = request.get_json()
    np_img = np.array(data, dtype=np.uint8)
    coordinates = pf.get_centroid_coords_from(np_img)
    data_storage.append(coordinates)
    
    # result = logic(coordinates) # TODO
    # data_storage.append(result)
    
    print(coordinates)
    
    return jsonify({"status": "success", "data": coordinates}), 200

@app.route('/test', methods=['GET'])
def get_data():
    return jsonify({"status": "success", "data": data_storage}), 200


if __name__ == "__main__":
    app.run(host='25.36.163.151', port=5000)
