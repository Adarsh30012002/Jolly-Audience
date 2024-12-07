![Open CV Github Frame](https://github.com/TH-Activities/saturday-hack-night-template/assets/90635335/78554b37-32b2-4488-a10c-5c68098d7776)

# Jolly Audience - Post-Event Photo Generator

Capturing the essence of joyous moments is at the heart of every event. Jolly Audience, an innovative post-event photo generator, goes beyond traditional event photography to curate a vibrant collection of smiles and laughter. Imagine reliving the happiest moments from your event through a personalized gallery, showcasing the genuine expressions of your audience. 

## Transforming Events into Timeless Memories

Jolly Audience is not just a photo generator; it's a storyteller that encapsulates the spirit of your event. It employs advanced facial recognition technology and intelligent similarity checks to craft a unique narrative through carefully selected frames. The result? A gallery that radiates joy, inclusivity, and the unforgettable atmosphere of your event.

## Features that Set Us Apart

### 1. Happy Face Detection
Utilizing cutting-edge Haar Cascade classifiers, Jolly Audience identifies not just faces but the radiant smiles that light up each frame of your event video.

### 2. Multiple Happy Faces
We believe in inclusivity. Jolly Audience extracts frames featuring a minimum number of happy faces, guaranteeing that every moment is a shared moment.

### 3. Effortless Web Interface
Uploading event videos has never been easier. Jolly Audience provides a user-friendly web interface, allowing you to effortlessly upload videos and receive a meticulously curated collection of happy frames.

## Team members
1. Aaron Jacob [https://github.com/aaron-jacob]
2. Abhishek S [https://github.com/abhi-s-03]

## Link to product walkthrough
https://drive.google.com/file/d/1azxYALrSyxMjSUFqh4edVg25WxYShu-w/view?usp=sharing

## How it Works ?
1. **Happy Face Detection:** Utilizes Haar Cascade classifiers for face and smile detection to identify happy faces in each frame of a given video.
2. **Multiple Happy Faces:** Extracts frames with a minimum number of happy faces, enhancing the inclusivity of the generated photos.
3. **Easy-to-Use Web Interface:** The web interface allows you to upload event videos effortlessly and receive a collection of curated happy frames.

## Libraries used
- **Flask:** Backend web framework for Python - Version 3.0.0
- **React:** Frontend JavaScript library for building user interfaces - Version 18.2.0
- **OpenCV:** Computer vision library for facial detection - Version 4.8.1.78
- **concurrent.futures:** Library for parallelizing tasks in Python 

## How to configure
### Prerequisites
Before running the application, ensure you have the following installed:
- Python 3.10.6
- pip (Python package installer)

### Installation
1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/abhi-s-03/SHN-OpenCV
   ```
2. Navigate to the project directory:
   ```bash
   cd SHN-OpenCV
   ```
3. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run
1. Run the Flask backend:
   ```bash
   python app.py
   ```
   This will start the backend server at http://localhost:5000.
2. Open a new terminal window, navigate to the frontend directory, and run the React frontend:
   ```bash
   cd frontend
   pnpm install
   pnpm run dev
   ```
