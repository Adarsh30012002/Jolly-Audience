from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64
import concurrent.futures
import os

app = Flask(__name__)
CORS(app)

def detect_happy_face(frame, min_happy_faces=1):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    smiling_count = 0
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        smiles = smile_cascade.detectMultiScale(
            roi_gray,
            scaleFactor=1.1,
            minNeighbors=15,
            minSize=(30, 30),
        )
        smiling_count += len(smiles)
    return smiling_count >= min_happy_faces

def process_frames(frames, frame_skip=15):
    happy_frames = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_frame, frame) for frame in frames[::frame_skip]]
    concurrent.futures.wait(futures)
    for future in futures:
        result = future.result()
        if result is not None:
            happy_frames.append(result)
    return happy_frames

def process_frame(frame):
    frame_np = np.array(frame)
    if detect_happy_face(frame_np):
        return frame_np
    return None

@app.route('/extract_happy_frames', methods=['POST'])
def extract_happy_frames():
    try:
        video_file = request.files['video']
        video_path = 'tmp_video.mp4'
        video_file.save(video_path)
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return jsonify({'error': 'Could not open video file.'}), 500
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frames = []

        for _ in range(total_frames):
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)

        cap.release()
        happy_frames = process_frames(frames)

        happy_frames_base64 = [base64.b64encode(cv2.imencode('.jpg', frame)[1]).decode('utf-8') for frame in happy_frames]
        os.remove(video_path)
        return jsonify({'happy_frames': happy_frames_base64})

    except Exception as e:
        print("Error:", str(e))
        import traceback
        traceback.print_exc()  
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
