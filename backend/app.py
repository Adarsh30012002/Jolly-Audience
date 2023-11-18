from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64
import concurrent.futures

app = Flask(__name__)
CORS(app)

def detect_happy_face(frame, smile_percentage_threshold=30, min_happy_faces=1):
    # Load Haar Cascade classifier for face and smile detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    smiling_count = 0

    for (x, y, w, h) in faces:
        # Extract the region of interest (ROI) for smile detection
        roi_gray = gray[y:y+h, x:x+w]

        # Detect smiles in the ROI
        smiles = smile_cascade.detectMultiScale(
            roi_gray,
            scaleFactor=1.1,
            minNeighbors=15,
            minSize=(30, 30),
        )

        smiling_count += len(smiles)

    # Check if the number of happy faces is at least the specified threshold
    return smiling_count >= min_happy_faces

def is_similar_frame(frame1, frame2, similarity_threshold=0.85):
    # Convert frames to grayscale
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # Resize frames for better performance
    resized_gray1 = cv2.resize(gray1, (100, 100))
    resized_gray2 = cv2.resize(gray2, (100, 100))

    # Calculate histograms for both frames
    hist1 = cv2.calcHist([resized_gray1], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([resized_gray2], [0], None, [256], [0, 256])

    # Compare histograms using correlation
    correlation = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)

    return correlation > similarity_threshold

def process_frames(frames, frame_skip=10):
    happy_frames = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_frame, frame) for frame in frames[::frame_skip]]

    # Wait for all futures to complete
    concurrent.futures.wait(futures)

    # Get the results
    happy_frames = [result for future in futures if (result := future.result()) is not None]

    return happy_frames

def process_frame(frame):
    # Convert frame to NumPy array
    frame_np = np.array(frame)

    if detect_happy_face(frame_np):
        return frame_np
    return None

@app.route('/extract_happy_frames', methods=['POST'])
def extract_happy_frames():
    print("Received request")

    try:
        video_file = request.files['video']
        video_path = 'tmp_video.mp4'
        video_file.save(video_path)

        print("Processing video...")

        # Use cv2.VideoCapture without specifying additional parameters
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print("Error: Could not open video file.")
            return jsonify({'error': 'Could not open video file.'}), 500

        # Get the total number of frames
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frames = []

        # Read every frame
        for _ in range(total_frames):
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)

        cap.release()

        # Extract frames with happy face detection and similarity check
        happy_frames = process_frames(frames)

        print("Sending response...")

        # Convert happy frames to base64
        happy_frames_base64 = [base64.b64encode(cv2.imencode('.jpg', frame)[1]).decode('utf-8') for frame in happy_frames]

        return jsonify({'happy_frames': happy_frames_base64})

    except Exception as e:
        print("Error:", str(e))
        import traceback
        traceback.print_exc()  # This will print the exception traceback to the console
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
