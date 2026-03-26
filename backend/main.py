from fastapi import FastAPI, UploadFile, File, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
import numpy as np
import cv2
import os
import uuid
from fastapi import Request

app = FastAPI(title="Car Damage Detection API")

# Allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
model = YOLO("model/best.pt")

# Create required folders
os.makedirs("outputs", exist_ok=True)
os.makedirs("uploads", exist_ok=True)

# Serve images
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")


@app.get("/")
def home():
    return {"message": "Car Damage Detection API running"}


@app.post("/predict")
async def predict(request: Request, file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Run YOLO
    results = model(image)

    # Draw detections
    img_with_boxes = results[0].plot()
    filename = f"prediction_{uuid.uuid4().hex}.png"
    filepath = os.path.join("outputs", filename)
    cv2.imwrite(filepath, img_with_boxes)

    # Extract detections
    detections = []
    for box in results[0].boxes:
        detections.append({
            "class": model.names[int(box.cls)],
            "confidence": float(box.conf),
            "bbox": box.xyxy.tolist()
        })

    return {
        "detections": detections,
        "image_url": f"/outputs/{filename}"
    }


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_location = f"uploads/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return {"filename": file.filename}
