from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from ultralytics import YOLO
import cv2
import os
import uuid
import base64

app = FastAPI(title="Car Damage Detection API")

# ─────────────────────────────────────────────
# CORS (React frontend)
# ─────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────
# Load model
# ─────────────────────────────────────────────
model = YOLO("model/best.pt")

# ─────────────────────────────────────────────
# Create folders
# ─────────────────────────────────────────────
os.makedirs("outputs/images", exist_ok=True)
os.makedirs("outputs/labels", exist_ok=True)
os.makedirs("outputs/annotated", exist_ok=True)

# ─────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────
@app.get("/")
def home():
    return {"message": "Car Damage Detection API running"}


@app.post("/predict")
async def predict(file: UploadFile = File(...), conf: float = 0.25):

    contents = await file.read()

    # Unique ID for this sample
    file_id = str(uuid.uuid4())

    # Paths
    input_path = f"temp_{file_id}.jpg"
    image_path = f"outputs/images/{file_id}.jpg"
    label_path = f"outputs/labels/{file_id}.txt"
    annotated_path = f"outputs/annotated/{file_id}.jpg"

    # Save temp + dataset image
    with open(input_path, "wb") as f:
        f.write(contents)

    with open(image_path, "wb") as f:
        f.write(contents)

    # ───────── YOLO inference ─────────
    results = model(input_path, conf=conf)[0]

    # Annotated image
    annotated = results.plot()
    cv2.imwrite(annotated_path, annotated)

    # Image size
    img = cv2.imread(input_path)
    h, w, _ = img.shape

    detections = []
    yolo_lines = []

    for box in results.boxes:
        cls_id = int(box.cls)
        conf_score = float(box.conf)
        x1, y1, x2, y2 = box.xyxy[0].tolist()

        # JSON detection (for frontend)
        detections.append({
            "class": model.names[cls_id],
            "confidence": conf_score,
            "bbox": [x1, y1, x2, y2]
        })

        # YOLO format (normalized)
        x_center = ((x1 + x2) / 2) / w
        y_center = ((y1 + y2) / 2) / h
        width = (x2 - x1) / w
        height = (y2 - y1) / h

        yolo_lines.append(f"{cls_id} {x_center} {y_center} {width} {height}")

    # Save YOLO label file
    with open(label_path, "w") as f:
        f.write("\n".join(yolo_lines))

    # Convert annotated image → base64
    _, buffer = cv2.imencode(".jpg", annotated)
    image_base64 = base64.b64encode(buffer).decode("utf-8")

    # Cleanup temp file
    os.remove(input_path)

    # ───────── RESPONSE ─────────
    return JSONResponse({
        "image_base64": image_base64,
        "detections": detections,
        "infer_ms": round(results.speed["inference"], 1),
        "conf": conf
    })


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_location = f"uploads/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return {"filename": file.filename}