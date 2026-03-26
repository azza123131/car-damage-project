import { useState } from "react";
import "./App.css";
import { useNavigate } from "react-router-dom";

function App() {
  const [file, setFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [confidenceThreshold, setConfidenceThreshold] = useState(0.5);
  const [mAP, setMAP] = useState("0.85"); // example mAP
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  // Handle image upload
  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    setImagePreview(URL.createObjectURL(selectedFile));
  };

  // Send image to backend for prediction
  const handlePredict = async () => {
    if (!file) return alert("Please select an image first");
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://localhost:8000/predict", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();

      // Filter predictions by confidence
      const filteredDetections = data.detections.filter(
        (d) => d.confidence >= confidenceThreshold
      );

      setPrediction({
        image_url: "http://localhost:8000" + data.image_url,
        detections: filteredDetections,
      });
    } catch (err) {
      console.error(err);
      alert("Prediction failed");
    }

    setLoading(false);
  };

  return (
    <div className="container">
      {/* Left panel: upload and controls */}
      <div className="left-panel">
        <h2>Upload Image</h2>
        <input type="file" onChange={handleFileChange} accept="image/*" />
        <button onClick={handlePredict} disabled={loading}>
          {loading ? "Predicting..." : "Predict"}
        </button>
      </div>

      {/* Center panel: image output */}
      <div className="center-panel">
        {imagePreview && (
          <div className="image-wrapper">
            <img
              src={prediction ? prediction.image_url : imagePreview}
              alt="Car"
              className="output-image"
            />
            {prediction && (
              <div className="object-count">
                {prediction?.detections?.length
                  ? `${prediction.detections.length} damage detected`
                  : "No damage detected"}
              </div>
            )}
          </div>
        )}
      </div>

    {/* Right panel */}
<div className="right-panel">

  <button
    className="model-button"
    onClick={() => navigate("/model")}
  >
    Model
  </button>
  <button
    className="graphs-button"
    onClick={() => navigate("/Graph")}
  >
    Model Graphs
  </button>
  <h3>Predictions</h3>

  {prediction && prediction.detections && prediction.detections.length > 0 ? (
    <ul>

      {prediction.detections.map((d, index) => {

        const bbox = d.bbox?.[0] || []

        return (
    

            <p className="prediction-desc">
             <strong>Damage Type:</strong> {d.class} <br/>

             <strong>Confidence:</strong> {(d.confidence * 100).toFixed(1)}% <br/>

            {bbox.length === 4 && (
             <>
              <strong>Bounding Box:</strong> [{bbox.map(v => Math.round(v)).join(", ")}]
             </>
            )}
            </p>

        )
      })}

    </ul>

  ) : (
    <p>No predictions yet</p>
  )}

</div>
    </div>
  );
}

export default App;