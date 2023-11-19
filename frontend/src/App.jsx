import { useState } from "react";
import JSZip from "jszip";
import { saveAs } from "file-saver";

import "./App.css";

function App() {
  const [videoFile, setVideoFile] = useState(null);
  const [happyFrames, setHappyFrames] = useState([]);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [loading, setLoading] = useState(false);
  const [selectedImage, setSelectedImage] = useState(null);
  const [selectedImages, setSelectedImages] = useState([]);

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

  const handleImageSelection = (index) => {
    const isSelected = selectedImages.includes(index);
    if (isSelected) {
      setSelectedImages(selectedImages.filter((i) => i !== index));
    } else {
      setSelectedImages([...selectedImages, index]);
    }
  };

  const handleImageDownload = () => {
    if (selectedImages.length > 0) {
      const zip = new JSZip();
      const folder = zip.folder("happy_images");

      selectedImages.forEach((index, i) => {
        const image = happyFrames[index];
        folder.file(`happy_image_${i}_${new Date().getTime()}.jpeg`, image, {
          base64: true,
        });
      });

      zip.generateAsync({ type: "blob" }).then((content) => {
        saveAs(content, "happy_images.zip");
      });
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
        <div className="happyframes">
          <h2>Happy Faces:</h2>
          <div className="image-container">
            {happyFrames.map((frame, index) => (
              <div key={index} className="image-card">
                <input
                  type="checkbox"
                  checked={selectedImages.includes(index)}
                  onChange={() => handleImageSelection(index)}
                />
                <img
                  src={`data:image/jpeg;base64,${frame}`}
                  alt={`Happy Face ${index}`}
                  onClick={() => handleImageClick(index)}
                />
              </div>
            ))}
          </div>
          <div>
            <button onClick={handleImageDownload}>Download Images</button>
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
