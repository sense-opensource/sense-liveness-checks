import { useRef, useState, useEffect } from "react";
import "./App.css";
import senseLogo from './images/sense-js-logo.svg';

function App() {
  const [mode, setMode] = useState("image");
  const [image, setImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const fileInputRef = useRef(null);
  const MAX_FILE_SIZE = 5 * 1024 * 1024;

  const startWebcam = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.play();
      }
    } catch (err) {
      setError("Unable to access webcam.");
      console.error(err);
    }
  };

  const stopWebcam = () => {
    const stream = videoRef.current?.srcObject;
    if (stream) {
      stream.getTracks().forEach((track) => track.stop());
    }
  };

  useEffect(() => {
    return () => stopWebcam();
  }, []);

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (!file) {
      console.log("No file selected.");
      return;
    }

    if (file.size > MAX_FILE_SIZE) {
      setError("File size exceeds 5MB.");
      setImage(null);
      setPreviewUrl(null);
      return;
    }

    if (!file.type.startsWith("image/")) {
      setError("Please upload a valid image file.");
      setImage(null);
      setPreviewUrl(null);
      return;
    }

    console.log("File selected:", file.name);
    setImage(file);
    setPreviewUrl(URL.createObjectURL(file));
    setError(null);
    setResult(null);
  };

  const triggerFileInput = () => {
    if (mode === "image" && fileInputRef.current) {
      fileInputRef.current.click();
    } else {
      console.log("Mode is not 'image' or file input ref is invalid.");
    }
  };

  const captureFromWebcam = () => {
    const canvas = canvasRef.current;
    const context = canvas.getContext("2d");
    context.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
    canvas.toBlob((blob) => {
      setImage(blob);
      setPreviewUrl(URL.createObjectURL(blob));
      setResult(null);
      setError(null);
    }, "image/jpeg");
  };

  const handleSubmit = async () => {
    if (!image) {
      setError("Please upload or capture an image.");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("image", image);

    try {
      const res = await fetch("http://localhost:3016/liveness", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      setError("Submission failed.");
    } finally {
      setLoading(false);
    }
  };

  const switchMode = (newMode) => {
    console.log("Switching to:", newMode);
    setImage(null);
    setPreviewUrl(null);
    setResult(null);
    setError(null);
    setMode(newMode);
    if (newMode === "webcam") startWebcam();
    else stopWebcam();
  };

  return (
    <div className="app-container">
     <header className="app-header">
      <img src={senseLogo} alt="Sense Logo" className="app-logo" />
    </header>


      <h1 className="app-title">Liveness Detection</h1>

      <div className="mode-toggle">
        <button
          className={`mode-button ${mode === "image" ? "active" : ""}`}
          onClick={() => {
            switchMode("image");
            triggerFileInput();
          }}
        >
          Upload Image
        </button>
        <button
          className={`mode-button ${mode === "webcam" ? "active" : ""}`}
          onClick={() => switchMode("webcam")}
        >
          Use Webcam
        </button>
      </div>

      <input
        type="file"
        accept="image/*"
        ref={fileInputRef}
        onChange={handleFileSelect}
        style={{ display: "none" }}
      />

      {mode === "webcam" && (
        <div className="webcam-section">
          <video ref={videoRef} className="webcam-preview" autoPlay muted />
          <canvas ref={canvasRef} width="320" height="240" hidden />
          <button
            onClick={captureFromWebcam}
            disabled={loading}
            className="action-button capture-button"
          >
            Capture Image
          </button>
        </div>
      )}

      {previewUrl && (
        <div className="preview-section">
          <img src={previewUrl} alt="Preview" className="preview-image" />
        </div>
      )}

      <button
        onClick={handleSubmit}
        disabled={loading || !image}
        className="action-button submit-button"
      >
        {loading ? (
          <span className="spinner" /> + " Processing..."
        ) : (
          "Submit for Liveness Detection"
        )}
      </button>

      {error && <div className="error-message">{error}</div>}

      {result && (
        <div className="result-card">
          <h3 className="result-title">Result</h3>
          <p>
            <strong>Status:</strong> {result.label}
          </p>
        </div>
      )}
      <footer className="app-footer">
      <p>&copy; {new Date().getFullYear()} Sense. All rights reserved.</p>
    </footer>
    </div>
  );
}

export default App;