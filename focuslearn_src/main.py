import cv2
import time
import json
import numpy as np
from Utils import process_frame as pf
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/web_test', methods=['GET'])
def online_test_for_local_laptop():
    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()
        coordinates = pf.get_centroid_coords_from(frame)
        time.sleep(1)
        yield json.dumps(coordinates)

data_storage = []
request_id = 0

@app.route('/test', methods=['POST'])
def post_data():
    global request_id
    
    data = request.get_json()
    np_img = np.array(data, dtype=np.uint8)
    coordinates = pf.get_centroid_coords_from(np_img)
    
    data_storage.append(coordinates)
    request_id += 1
    
    response = {
        "request_id": request_id,
        "result": data_storage[-1],
    }
    
    return jsonify(response), 200

@app.route('/test', methods=['GET'])
def get_data():
    return jsonify({"data": data_storage[-1], "request_id": request_id}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
