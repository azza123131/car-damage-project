function Model() {
  const modelInfo = {
    name: "YOLOv8m",
    image_size: 640,
    epochs: 150,
    batch_size: 16,
  };

  return (
    <div style={{ padding: "40px" }}>
      <h1>Model Characteristics</h1>

      <div style={{ marginTop: "20px", lineHeight: "1.8" }}>
        <p><strong>Model:</strong> {modelInfo.name}</p>
        <p><strong>Image Size:</strong> {modelInfo.image_size}</p>
        <p><strong>Epochs:</strong> {modelInfo.epochs}</p>
        <p><strong>Batch Size:</strong> {modelInfo.batch_size}</p>

        <hr />
      </div>
    </div>
  );
}

export default Model;