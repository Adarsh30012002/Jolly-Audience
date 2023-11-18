import { useState } from "react";
import "./App.css";

function App() {
  const [videoFile, setVideoFile] = useState(null);
  const [happyFrames, setHappyFrames] = useState([]);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [loading, setLoading] = useState(false);
  const [selectedImage, setSelectedImage] = useState(null);

  const handleFileChange = (event) => {
    setVideoFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("video", videoFile);

    try {
      setLoading(true);

      const response = await fetch(
        "http://localhost:5000/extract_happy_frames",
        {
          method: "POST",
          body: formData,
          onUploadProgress: (progressEvent) => {
            const progress = Math.round(
              (progressEvent.loaded / progressEvent.total) * 100
            );
            setUploadProgress(progress);
          },
        }
      );

      if (response.ok) {
        const result = await response.json();
        setHappyFrames(result.happy_frames);
      } else {
        console.error("Error processing video:", response.statusText);
      }
    } catch (error) {
      console.error("Network error during video upload:", error);
    } finally {
      setLoading(false);
      setUploadProgress(0);
    }
  };

  const handleImageClick = (index) => {
    setSelectedImage(happyFrames[index]);
  };

  const handleCloseModal = () => {
    setSelectedImage(null);
  };

  return (
    <div className="App">
      <header>
        <h1> Jolly Audience</h1>
      </header>
      <section className="file-section">
        <input type="file" accept="video/*" onChange={handleFileChange} />
        <button onClick={handleUpload}>Extract happy frames</button>
      </section>

      {loading && (
        <div className="loading-container">
          <div className="kinetic"></div>
          <h2>Processing...</h2>
        </div>
      )}

      {uploadProgress > 0 && uploadProgress < 100 && (
        <div>
          <h2>Uploading...</h2>
          <progress value={uploadProgress} max="100" />
        </div>
      )}

      {happyFrames.length > 0 && (
        <div>
          <h2>Happy Faces:</h2>
          <div className="image-container">
            {happyFrames.map((frame, index) => (
              <div
                key={index}
                className="image-card"
                onClick={() => handleImageClick(index)}
              >
                <img
                  src={`data:image/jpeg;base64,${frame}`}
                  alt={`Happy Face ${index}`}
                />
              </div>
            ))}
          </div>
        </div>
      )}

      {selectedImage && (
        <div className="modal" onClick={handleCloseModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <span className="close" onClick={handleCloseModal}>
              &times;
            </span>
            <img
              src={`data:image/jpeg;base64,${selectedImage}`}
              alt="Selected Image"
            />
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
