![Open CV Github Frame](https://github.com/TH-Activities/saturday-hack-night-template/assets/90635335/78554b37-32b2-4488-a10c-5c68098d7776)

# Jolly Audience - Post-Event Photo Generator

This project extracts happy moments from event videos, providing a collection of post-event photos featuring smiling faces. It utilizes facial recognition and similarity checks to curate images that capture the joyous expressions of the audience.

## Team members
1. [Name 1](https://github.com/your-username)
2. [Name 2](https://github.com/your-username)

## Link to product walkthrough
[Link to video](Link Here)

## How it Works ?
1. **Happy Face Detection:** Utilizes Haar Cascade classifiers for face and smile detection to identify happy faces in each frame of a given video.
2. **Similarity Check:** Performs a similarity check between frames to avoid redundancy and ensure a diverse collection of happy moments.
3. **Multiple Happy Faces:** Extracts frames with a minimum number of happy faces, enhancing the inclusivity of the generated photos.
4. **Easy-to-Use Web Interface:** The web interface allows you to upload event videos effortlessly and receive a collection of curated happy frames.

## Libraries used
- **Flask:** Backend web framework for Python - Version X.X
- **React:** Frontend JavaScript library for building user interfaces - Version X.X
- **OpenCV:** Computer vision library for facial detection - Version X.X
- **concurrent.futures:** Library for parallelizing tasks in Python - Version X.X
- **axios:** HTTP client for making requests in React applications - Version X.X

## How to configure
### Prerequisites
Before running the application, ensure you have the following installed:
- Python 3.x
- pip (Python package installer)

### Installation
1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/your-username/jolly-audience.git
   ```
2. Navigate to the project directory:
   ```bash
   cd jolly-audience
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
   npm install
   npm start
   ```
   This will start the React development server at http://localhost:3000.
3. Open your web browser and go to http://localhost:3000 to access the application.
